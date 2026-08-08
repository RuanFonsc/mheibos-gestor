const { app, BrowserWindow, Menu, Notification, clipboard, dialog, ipcMain, shell } = require("electron");
const { execFileSync, spawn } = require("child_process");
const fs = require("fs");
const http = require("http");
const path = require("path");
const { fileURLToPath } = require("url");

const ACCESS_HOST = process.env.MHEIBOS_ACCESS_HOST || "127.0.0.1";
const BIND_HOST = process.env.MHEIBOS_BIND_HOST || "0.0.0.0";
const PORT = Number(process.env.MHEIBOS_PORT || 8001);
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
const REMOTE_BASE_URL =
  process.env.MHEIBOS_BASE_URL || (modoAtual() === "cliente" ? CLIENT_CONFIG.serverUrl : "") || "";
const BASE_URL = (REMOTE_BASE_URL || `http://${ACCESS_HOST}:${PORT}`).replace(/\/$/, "");
const REMOTE_CLIENT = Boolean(REMOTE_BASE_URL);
let djangoProcess = null;
let mainWindow = null;

function modoAtual() {
  const args = process.argv.join(" ").toLowerCase();
  const appName = app.getName().toLowerCase();
  if (args.includes("--cliente") || appName.includes("cliente")) return "cliente";
  if (args.includes("--producao") || appName.includes("producao")) return "producao";
  return "gestor";
}

function destinoInicial() {
  if (modoAtual() === "producao") return "/producao/login/?next=/producao/";
  return "/login/?next=/";
}

function tituloJanela() {
  if (modoAtual() === "cliente") return "Mheibos Gestor Cliente";
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
  fs.mkdirSync(app.getPath("userData"), { recursive: true });
  fs.mkdirSync(dataDir(), { recursive: true });
  fs.writeFileSync(configPath(), JSON.stringify(config, null, 2), "utf8");
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
    DJANGO_ALLOWED_HOSTS: process.env.DJANGO_ALLOWED_HOSTS || "*",
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
    env.DB_PASSWORD = db.password ?? process.env.DB_PASSWORD ?? "123456";
    env.LEGACY_DB_HOST = env.DB_HOST;
    env.LEGACY_DB_PORT = env.DB_PORT;
    env.LEGACY_DB_NAME = env.DB_NAME;
    env.LEGACY_DB_USER = env.DB_USER;
    env.LEGACY_DB_PASSWORD = env.DB_PASSWORD;
  } else {
    env.MHEIBOS_DB_MODE = "sqlite";
    env.SQLITE_DB_NAME = config.sqlite?.name || "mheibos_gestor";
  }
  return env;
}

function serverOnline() {
  return new Promise((resolve) => {
    const req = http.get(`${BASE_URL}/login/`, (res) => {
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

async function waitForServer(timeoutMs = 35000) {
  const startedAt = Date.now();
  while (Date.now() - startedAt < timeoutMs) {
    if (await serverOnline()) return true;
    await new Promise((resolve) => setTimeout(resolve, 450));
  }
  return false;
}

function openSetupWindow() {
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
      writeConfig(config);
      cleanup();
      win.close();
      resolve(config);
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
    win.loadFile(path.join(__dirname, "setup.html"));
  });
}

async function ensureConfig() {
  if (REMOTE_CLIENT) return readConfig() || { mode: "remote" };
  const existing = readConfig();
  if (existing) return existing;
  return await openSetupWindow();
}

async function ensureDjango(config) {
  if (await serverOnline()) return true;
  if (REMOTE_CLIENT) {
    dialog.showErrorBox("Mheibos", `Nao foi possivel acessar ${BASE_URL}. Verifique se o servidor esta aberto.`);
    return false;
  }

  const packagedBackend = backendExePath();
  let command;
  let args;
  let cwd;
  if (packagedBackend) {
    command = packagedBackend;
    args = ["runserver", `${BIND_HOST}:${PORT}`, "--noreload"];
    cwd = path.dirname(packagedBackend);
  } else {
    if (!fs.existsSync(path.join(DEV_PROJECT_ROOT, "manage.py"))) {
      dialog.showErrorBox("Mheibos", "Nao encontrei o backend do Mheibos Gestor.");
      return false;
    }
    const py = pythonCommand();
    command = py.command;
    args = [...py.argsPrefix, "manage.py", "runserver", `${BIND_HOST}:${PORT}`, "--noreload"];
    cwd = DEV_PROJECT_ROOT;
  }

  djangoProcess = spawn(command, args, {
    cwd,
    windowsHide: true,
    env: envFromConfig(config),
  });
  djangoProcess.on("exit", () => {
    djangoProcess = null;
  });

  const ok = await waitForServer();
  if (!ok) {
    dialog.showErrorBox(
      "Mheibos",
      "Nao foi possivel iniciar o servidor local. Verifique a configuracao do banco de dados."
    );
  }
  return ok;
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

function createWindow() {
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
    if (url.startsWith(BASE_URL)) return;
    if (url.startsWith("file://")) abrirCaminhoLocal(url);
    else shell.openExternal(url);
    event.preventDefault();
  });
  win.webContents.on("before-input-event", (_event, input) => {
    if (input.key === "F5" || ((input.control || input.meta) && input.key.toLowerCase() === "r")) {
      win.reload();
    }
  });
  win.loadURL(`${BASE_URL}${destinoInicial()}`);
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
        if (targetUrl.startsWith("/")) mainWindow.loadURL(`${BASE_URL}${targetUrl}`);
      }
    });
    notification.show();
    return true;
  });
  const config = await ensureConfig();
  if (!config) {
    app.quit();
    return;
  }
  if (!(await ensureDjango(config))) return;
  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("before-quit", () => {
  if (djangoProcess) {
    djangoProcess.kill();
    djangoProcess = null;
  }
});
