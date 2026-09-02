const { app, BrowserWindow, Menu, Notification, clipboard, dialog, ipcMain, safeStorage, session, shell } = require("electron");
const { execFileSync, spawn } = require("child_process");
const fs = require("fs");
const http = require("http");
const path = require("path");
const { fileURLToPath } = require("url");
const { decryptSecret, protectConfigSecrets } = require("./secure_config");
const { offlineRuntimeConfig, readOfflineIdentity } = require("./offline_runtime");
const { resolveRemoteBaseUrl } = require("./runtime_profile");
const { createManagedProcess } = require("./managed_process");

const HOST = "127.0.0.1";
const PORT = Number(process.env.MHEIBOS_PORT || 8765);
const DEV_PROJECT_ROOT = path.resolve(process.env.MHEIBOS_PROJECT_ROOT || path.join(__dirname, ".."));
function readClientConfig() {
  const candidates = [
    path.join(__dirname, "client-config.json"),
    path.join(process.resourcesPath || "", "client-config.json"),
  ];
  for (const candidate of candidates) {
    try {
      if (fs.existsSync(candidate)) return JSON.parse(fs.readFileSync(candidate, "utf8"));
    } catch {
      // Configuracao cliente invalida: usa o fallback local.
    }
  }
  return {};
}
const CLIENT_CONFIG = readClientConfig();
const REMOTE_BASE_URL = resolveRemoteBaseUrl({
  appName: app.getName(),
  envBaseUrl: process.env.MHEIBOS_BASE_URL,
  clientConfig: CLIENT_CONFIG,
});
const REMOTE_CLIENT = Boolean(REMOTE_BASE_URL);
const REMOTE_URL = REMOTE_BASE_URL.replace(/\/$/, "");
const LOCAL_PORT = REMOTE_CLIENT ? Number(process.env.MHEIBOS_OFFLINE_PORT || 8766) : PORT;
const LOCAL_BASE_URL = `http://${HOST}:${LOCAL_PORT}`;
let activeBaseUrl = REMOTE_URL || LOCAL_BASE_URL;
const djangoService = createManagedProcess({ spawnProcess: spawn });
const cognitiveService = createManagedProcess({ spawnProcess: spawn });
let mainWindow = null;
let offlineIdentityCandidate = null;
let syncTimer = null;
let syncRunning = false;
let onlineReturnOffered = false;

function modoAtual() {
  const args = process.argv.join(" ").toLowerCase();
  const appName = app.getName().toLowerCase();
  if (args.includes("--producao") || appName.includes("producao")) return "producao";
  return "gestor";
}

function destinoInicial() {
  if (modoAtual() === "producao") return "/producao/login/?next=/producao/";
  return "/login/?next=/";
}

function tituloJanela() {
  return modoAtual() === "producao" ? "Mheibos Producao" : "Mheibos Gestor";
}

function configPath() {
  return path.join(app.getPath("userData"), "mheibos-config.json");
}

function dataDir() {
  return path.join(app.getPath("userData"), "data");
}

function readConfig() {
  try {
    return JSON.parse(fs.readFileSync(configPath(), "utf8"));
  } catch {
    return null;
  }
}

function writeConfig(config) {
  const protectedConfig = protectConfigSecrets(config, safeStorage);
  fs.mkdirSync(app.getPath("userData"), { recursive: true });
  fs.mkdirSync(dataDir(), { recursive: true });
  fs.writeFileSync(configPath(), JSON.stringify(protectedConfig, null, 2), "utf8");
}

function backendExePath() {
  const candidates = [
    path.join(process.resourcesPath || "", "backend", "mheibos-backend", "mheibos-backend.exe"),
    path.join(DEV_PROJECT_ROOT, "dist", "backend", "mheibos-backend", "mheibos-backend.exe"),
  ];
  return candidates.find((candidate) => fs.existsSync(candidate));
}

function pythonCommand() {
  const venvPython = path.join(DEV_PROJECT_ROOT, ".venv", "Scripts", "python.exe");
  if (fs.existsSync(venvPython)) return { command: venvPython, argsPrefix: [] };
  return process.platform === "win32"
    ? { command: "py", argsPrefix: ["-3"] }
    : { command: "python3", argsPrefix: [] };
}

function envFromConfig(config) {
  const env = {
    ...process.env,
    DJANGO_ALLOWED_HOSTS: process.env.DJANGO_ALLOWED_HOSTS || "localhost,127.0.0.1",
    PYTHONUNBUFFERED: "1",
    MHEIBOS_DATA_DIR: dataDir(),
  };
  if (!config || config.mode === "postgres") {
    const db = config?.postgres || {};
    env.MHEIBOS_DB_MODE = "postgres";
    env.DB_HOST = db.host || process.env.DB_HOST || "localhost";
    env.DB_PORT = db.port || process.env.DB_PORT || "5432";
    env.DB_NAME = db.name || process.env.DB_NAME || "gestor_db";
    env.DB_USER = db.user || process.env.DB_USER || "postgres";
    env.DB_PASSWORD = decryptSecret(db.passwordEncrypted, safeStorage) || db.password || process.env.DB_PASSWORD || "123456";
    env.LEGACY_DB_HOST = env.DB_HOST;
    env.LEGACY_DB_PORT = env.DB_PORT;
    env.LEGACY_DB_NAME = env.DB_NAME;
    env.LEGACY_DB_USER = env.DB_USER;
    env.LEGACY_DB_PASSWORD = env.DB_PASSWORD;
  } else {
    env.MHEIBOS_DB_MODE = "sqlite";
    env.SQLITE_DB_NAME = config.sqlite?.name || "mheibos_gestor";
  }
  env.MHEIBOS_STATION_ID = config?.stationId || "";
  env.MHEIBOS_STATION_SECRET = decryptSecret(config?.stationSecretEncrypted, safeStorage);
  env.MHEIBOS_RUNTIME_ROLE = config?.runtimeRole || "central";
  env.MHEIBOS_CENTRAL_URL = REMOTE_URL;
  return env;
}

function stationCredentials(config) {
  return {
    id: config?.stationId || "",
    secret: decryptSecret(config?.stationSecretEncrypted, safeStorage) || config?.stationSecret || "",
  };
}

function installStationHeaders(config) {
  const credentials = stationCredentials(config);
  if (!REMOTE_CLIENT || !credentials.id || !credentials.secret) return;
  session.defaultSession.webRequest.onBeforeSendHeaders(
    { urls: [`${REMOTE_URL}/*`] },
    (details, callback) => {
      details.requestHeaders["X-Mheibos-Station-ID"] = credentials.id;
      details.requestHeaders["X-Mheibos-Station-Secret"] = credentials.secret;
      callback({ requestHeaders: details.requestHeaders });
    }
  );
}

async function cacheValidatedOfflineIdentity(win, config) {
  if (!REMOTE_CLIENT || activeBaseUrl !== REMOTE_URL || !offlineIdentityCandidate) return;
  try {
    const snapshot = await win.webContents.executeJavaScript(
      `fetch('/sincronizacao/identidade-atual/', {credentials: 'same-origin'})` +
      `.then(async response => response.ok ? response.json() : null)`
    );
    const validatedName = String(snapshot?.operador?.nome || "").trim().toLocaleLowerCase();
    const candidateName = String(offlineIdentityCandidate.usuario || "").trim().toLocaleLowerCase();
    if (!snapshot || validatedName !== candidateName) return;
    const current = readConfig() || config || {};
    writeConfig({
      ...current,
      offlineIdentity: JSON.stringify({
        ...snapshot,
        senha: offlineIdentityCandidate.senha,
      }),
    });
    offlineIdentityCandidate = null;
  } catch {
    // A identidade anterior permanece protegida; uma falha de cache nao encerra a sessao online.
  }
}

function serverOnline(baseUrl = activeBaseUrl) {
  return new Promise((resolve) => {
    const req = http.get(`${baseUrl}/login/`, (res) => {
      res.resume();
      resolve(res.statusCode >= 200 && res.statusCode < 500);
    });
    req.on("error", () => resolve(false));
    req.setTimeout(900, () => {
      req.destroy();
      resolve(false);
    });
  });
}

async function waitForServer(baseUrl = activeBaseUrl, timeoutMs = 35000) {
  const startedAt = Date.now();
  while (Date.now() - startedAt < timeoutMs) {
    if (await serverOnline(baseUrl)) return true;
    await new Promise((resolve) => setTimeout(resolve, 450));
  }
  return false;
}

function openSetupWindow({ remote = false } = {}) {
  return new Promise((resolve) => {
    const win = new BrowserWindow({
      width: 720,
      height: 640,
      resizable: false,
      title: "Configurar Mheibos Suite",
      backgroundColor: "#171a29",
      webPreferences: {
        preload: path.join(__dirname, "preload.js"),
        contextIsolation: true,
        nodeIntegration: false,
      },
    });

    const cleanup = () => {
      ipcMain.removeHandler("setup:save");
      ipcMain.removeHandler("setup:cancel");
    };

    ipcMain.handle("setup:save", (_event, config) => {
      try {
        writeConfig(config);
      } catch (error) {
        return { ok: false, error: String(error?.message || error) };
      }
      cleanup();
      win.close();
      resolve(config);
      return { ok: true };
    });
    ipcMain.handle("setup:cancel", () => {
      cleanup();
      win.close();
      resolve(null);
    });
    win.on("closed", () => {
      cleanup();
      resolve(null);
    });
    win.loadFile(path.join(__dirname, "setup.html"), { query: { remote: remote ? "1" : "0" } });
  });
}

async function ensureConfig() {
  const existing = readConfig();
  if (existing?.postgres?.password || existing?.stationSecret) {
    writeConfig(existing);
    return readConfig();
  }
  if (REMOTE_CLIENT) {
    if (existing?.stationId && existing?.stationSecretEncrypted) {
      return { ...existing, mode: "remote" };
    }
    return await openSetupWindow({ remote: true });
  }
  if (existing) return existing;
  return await openSetupWindow();
}

function backendInvocation(args) {
  const packagedBackend = backendExePath();
  if (packagedBackend) {
    return { command: packagedBackend, args, cwd: path.dirname(packagedBackend), packaged: true };
  }
  if (!fs.existsSync(path.join(DEV_PROJECT_ROOT, "manage.py"))) return null;
  const py = pythonCommand();
  return { command: py.command, args: [...py.argsPrefix, "manage.py", ...args], cwd: DEV_PROJECT_ROOT, packaged: false };
}

function runBackendCommand(config, args, stdinPayload = "") {
  return new Promise((resolve) => {
    const invocation = backendInvocation(args);
    if (!invocation) return resolve(false);
    const child = spawn(invocation.command, invocation.args, {
      cwd: invocation.cwd,
      windowsHide: true,
      env: envFromConfig(config),
      stdio: ["pipe", "ignore", "ignore"],
    });
    child.on("error", () => resolve(false));
    child.on("exit", (code) => resolve(code === 0));
    child.stdin.on("error", () => resolve(false));
    child.stdin.end(stdinPayload);
  });
}

async function prepareOfflineBackend(config) {
  const identity = readOfflineIdentity(config, safeStorage);
  if (!identity) return null;
  const offlineConfig = offlineRuntimeConfig(config);
  const invocation = backendInvocation([]);
  if (!invocation) return null;
  if (!(await runBackendCommand(offlineConfig, ["migrate", "--noinput"]))) return null;
  if (!(await runBackendCommand(offlineConfig, ["bootstrap_identidade_offline"], JSON.stringify(identity)))) return null;
  return offlineConfig;
}

async function startLocalDjango(config) {
  if (!(await serverOnline(LOCAL_BASE_URL))) {
    if (!(await runBackendCommand(config, ["migrate", "--noinput"]))) {
      dialog.showErrorBox(
        "Mheibos",
        "Nao foi possivel preparar o banco local. Verifique a configuracao do banco de dados."
      );
      return false;
    }
    const invocation = backendInvocation(["runserver", `${HOST}:${LOCAL_PORT}`, "--noreload"]);
    if (!invocation) return false;
    const started = await djangoService.start({
      command: invocation.command,
      args: invocation.args,
      options: {
        cwd: invocation.cwd,
        windowsHide: true,
        env: envFromConfig(config),
        stdio: "ignore",
      },
    });
    if (!started) return false;

    const ok = await waitForServer(LOCAL_BASE_URL);
    if (!ok) {
      djangoService.stop();
      dialog.showErrorBox(
        "Mheibos",
        "Nao foi possivel iniciar o servidor local. Verifique a configuracao do banco de dados."
      );
      return false;
    }
  }

  const workerInvocation = backendInvocation(["processar_cognicao", "--loop"]);
  if (workerInvocation) {
    await cognitiveService.start({
      command: workerInvocation.command,
      args: workerInvocation.args,
      options: {
        cwd: workerInvocation.cwd,
        windowsHide: true,
        env: envFromConfig(config),
        stdio: "ignore",
      },
    });
  }
  return true;
}

async function ensureDjango(config) {
  if (REMOTE_CLIENT && await serverOnline(REMOTE_URL)) {
    activeBaseUrl = REMOTE_URL;
    return { ok: true, config };
  }
  if (REMOTE_CLIENT) {
    const offlineConfig = await prepareOfflineBackend(config);
    if (!offlineConfig) {
      dialog.showErrorBox("Mheibos", "A Central esta indisponivel e ainda nao existe uma identidade offline valida nesta Estacao.");
      return { ok: false, config };
    }
    activeBaseUrl = LOCAL_BASE_URL;
    return { ok: await startLocalDjango(offlineConfig), config: offlineConfig };
  }
  activeBaseUrl = LOCAL_BASE_URL;
  return { ok: await startLocalDjango(config), config };
}

async function synchronizeOfflineQueue(config) {
  if (config?.runtimeRole !== "client_offline" || syncRunning) return;
  syncRunning = true;
  try {
    await runBackendCommand(config, ["enviar_fila_offline", "--limite", "10"]);
    await offerOnlineReturn(config);
  } finally {
    syncRunning = false;
  }
}

async function switchToCentral(config) {
  if (!mainWindow) return false;
  mainWindow.setEnabled(false);
  const queueClear = await runBackendCommand(config, ["verificar_retorno_online"]);
  const centralAvailable = await serverOnline(REMOTE_URL);
  if (!queueClear || !centralAvailable) {
    mainWindow.setEnabled(true);
    onlineReturnOffered = false;
    return false;
  }
  activeBaseUrl = REMOTE_URL;
  offlineIdentityCandidate = null;
  try {
    await mainWindow.loadURL(`${activeBaseUrl}${destinoInicial()}`);
  } catch {
    activeBaseUrl = LOCAL_BASE_URL;
    mainWindow.setEnabled(true);
    onlineReturnOffered = false;
    return false;
  }
  if (syncTimer) {
    clearInterval(syncTimer);
    syncTimer = null;
  }
  stopLocalServices();
  mainWindow.setEnabled(true);
  return true;
}

function stopLocalServices() {
  djangoService.stop();
  cognitiveService.stop();
}

async function offerOnlineReturn(config) {
  if (onlineReturnOffered || !mainWindow || !(await serverOnline(REMOTE_URL))) return;
  if (!(await runBackendCommand(config, ["verificar_retorno_online"]))) return;
  onlineReturnOffered = true;
  const result = await dialog.showMessageBox(mainWindow, {
    type: "info",
    title: "Central disponivel",
    message: "Todos os dados locais foram confirmados pela Central.",
    detail: "Antes de voltar, confirme que nao ha formulario ainda nao salvo. O banco local sera preservado como evidencia.",
    buttons: ["Voltar para a Central", "Continuar offline"],
    defaultId: 1,
    cancelId: 1,
    noLink: true,
  });
  if (result.response === 0) {
    await switchToCentral(config);
  }
}

function startOfflineSynchronization(config) {
  if (config?.runtimeRole !== "client_offline") return;
  synchronizeOfflineQueue(config);
  syncTimer = setInterval(() => synchronizeOfflineQueue(config), 30000);
}

function abrirCaminhoLocal(url) {
  try {
    shell.openPath(fileURLToPath(url));
  } catch {
    shell.openExternal(url);
  }
}

function normalizarCaminhoServidor(filePath) {
  const original = String(filePath || "").trim();
  if (!original) return { path: "", isNetwork: false, message: "" };
  const normalized = original.replaceAll("/", "\\");
  if (normalized.startsWith("\\\\")) {
    return { path: normalized, isNetwork: true, message: "" };
  }
  const driveMatch = normalized.match(/^([A-Za-z]):\\/);
  if (driveMatch && process.platform === "win32") {
    try {
      const drive = `${driveMatch[1].toUpperCase()}:`;
      const output = execFileSync("net", ["use", drive], { encoding: "utf8", windowsHide: true });
      const remoteLine = output
        .split(/\r?\n/)
        .map((line) => line.trim())
        .find((line) => line.includes("\\\\"));
      const remote = remoteLine?.match(/(\\\\.+)$/)?.[1]?.trim();
      if (remote) {
        return {
          path: `${remote}${normalized.slice(2)}`,
          isNetwork: true,
          message: "Unidade mapeada convertida para caminho do servidor.",
        };
      }
    } catch {
      // Sem mapeamento de rede para esta unidade.
    }
  }
  return {
    path: normalized,
    isNetwork: false,
    message: "Selecione um arquivo em uma pasta compartilhada do servidor, nao em uma pasta local deste computador.",
  };
}

function createWindow(config) {
  const win = new BrowserWindow({
    width: modoAtual() === "producao" ? 1360 : 1440,
    height: 860,
    minWidth: 1100,
    minHeight: 720,
    title: tituloJanela(),
    backgroundColor: "#171a29",
    show: false,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
    },
  });
  mainWindow = win;

  win.once("ready-to-show", () => win.show());
  win.setMenuBarVisibility(false);
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith("file://")) abrirCaminhoLocal(url);
    else shell.openExternal(url);
    return { action: "deny" };
  });
  win.webContents.on("will-navigate", (event, url) => {
    try {
      if (new URL(url).origin === new URL(activeBaseUrl).origin) return;
    } catch {
      // URL invalida segue bloqueada como navegacao externa.
    }
    if (url.startsWith("file://")) abrirCaminhoLocal(url);
    else shell.openExternal(url);
    event.preventDefault();
  });
  win.webContents.on("before-input-event", (_event, input) => {
    if (input.key === "F5" || ((input.control || input.meta) && input.key.toLowerCase() === "r")) {
      win.reload();
    }
  });
  win.loadURL(`${activeBaseUrl}${destinoInicial()}`);
  win.webContents.on("did-finish-load", () => cacheValidatedOfflineIdentity(win, config));
}

app.whenReady().then(async () => {
  Menu.setApplicationMenu(null);
  ipcMain.handle("corel:select-file", async () => {
    const result = await dialog.showOpenDialog({
      title: "Selecionar arquivo Corel no servidor",
      properties: ["openFile"],
      filters: [
        { name: "Arquivos Corel", extensions: ["cdr", "cdt", "cmx"] },
        { name: "Todos os arquivos", extensions: ["*"] },
      ],
    });
    if (result.canceled || !result.filePaths.length) return null;
    return normalizarCaminhoServidor(result.filePaths[0]);
  });
  ipcMain.handle("directory:select", async () => {
    const result = await dialog.showOpenDialog({
      title: "Escolher diretório das artes oficiais",
      properties: ["openDirectory", "createDirectory"],
    });
    if (result.canceled || !result.filePaths.length) return null;
    return result.filePaths[0];
  });
  ipcMain.handle("corel:normalize-path", (_event, filePath) => normalizarCaminhoServidor(filePath));
  ipcMain.handle("corel:open-path", (_event, filePath) => {
    const normalized = normalizarCaminhoServidor(filePath);
    if (!normalized.path || !normalized.isNetwork) return normalized;
    shell.openPath(normalized.path);
    return normalized;
  });
  ipcMain.handle("clipboard:read-image", () => {
    const image = clipboard.readImage();
    if (image.isEmpty()) return null;
    return image.toDataURL();
  });
  ipcMain.handle("desktop:notify", (_event, payload = {}) => {
    if (!Notification.isSupported()) return false;
    const title = String(payload.title || "Mheibos Gestor").slice(0, 80);
    const body = String(payload.body || "").slice(0, 240);
    const targetUrl = String(payload.url || "");
    const notification = new Notification({ title, body, silent: false });
    notification.on("click", () => {
      if (mainWindow) {
        mainWindow.show();
        mainWindow.focus();
        if (targetUrl.startsWith("/")) mainWindow.loadURL(`${activeBaseUrl}${targetUrl}`);
      }
    });
    notification.show();
    return true;
  });
  ipcMain.handle("offline-identity:candidate", (_event, payload = {}) => {
    const usuario = String(payload.usuario || "").slice(0, 80);
    const senha = String(payload.senha || "").slice(0, 256);
    offlineIdentityCandidate = usuario && senha ? { usuario, senha } : null;
    return Boolean(offlineIdentityCandidate);
  });
  const config = await ensureConfig();
  if (!config) {
    app.quit();
    return;
  }
  installStationHeaders(config);
  const runtime = await ensureDjango(config);
  if (!runtime.ok) return;
  createWindow(runtime.config);
  startOfflineSynchronization(runtime.config);
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow(runtime.config);
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("before-quit", () => {
  if (syncTimer) {
    clearInterval(syncTimer);
    syncTimer = null;
  }
  stopLocalServices();
});
