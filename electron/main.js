const { app, BrowserWindow, Menu, dialog, shell } = require("electron");
const { spawn } = require("child_process");
const fs = require("fs");
const http = require("http");
const path = require("path");
const { fileURLToPath } = require("url");

const PROJECT_ROOT = path.resolve(process.env.MHEIBOS_PROJECT_ROOT || path.join(__dirname, ".."));
const PORT = Number(process.env.MHEIBOS_PORT || 8765);
const HOST = "127.0.0.1";
const BASE_URL = (process.env.MHEIBOS_BASE_URL || `http://${HOST}:${PORT}`).replace(/\/$/, "");
let djangoProcess = null;

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

function pythonCommand() {
  const venvPython = path.join(PROJECT_ROOT, ".venv", "Scripts", "python.exe");
  if (fs.existsSync(venvPython)) return { command: venvPython, argsPrefix: [] };
  return process.platform === "win32"
    ? { command: "py", argsPrefix: ["-3"] }
    : { command: "python3", argsPrefix: [] };
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

async function waitForServer(timeoutMs = 25000) {
  const startedAt = Date.now();
  while (Date.now() - startedAt < timeoutMs) {
    if (await serverOnline()) return true;
    await new Promise((resolve) => setTimeout(resolve, 450));
  }
  return false;
}

async function ensureDjango() {
  if (await serverOnline()) return;
  if (process.env.MHEIBOS_BASE_URL) {
    dialog.showErrorBox(
      "Mheibos",
      `Nao foi possivel acessar ${BASE_URL}. Verifique se o servidor local do Mheibos esta aberto.`
    );
    return;
  }
  if (!fs.existsSync(path.join(PROJECT_ROOT, "manage.py"))) {
    dialog.showErrorBox(
      "Mheibos",
      "Nao encontrei o projeto Django do Mheibos. Defina MHEIBOS_PROJECT_ROOT apontando para a pasta do projeto ou abra o launcher dentro do repositorio."
    );
    return;
  }

  const py = pythonCommand();
  const args = [
    ...py.argsPrefix,
    "manage.py",
    "runserver",
    `${HOST}:${PORT}`,
    "--noreload",
  ];

  djangoProcess = spawn(py.command, args, {
    cwd: PROJECT_ROOT,
    windowsHide: true,
    env: {
      ...process.env,
      DJANGO_ALLOWED_HOSTS: process.env.DJANGO_ALLOWED_HOSTS || "localhost,127.0.0.1",
      PYTHONUNBUFFERED: "1",
    },
  });

  djangoProcess.on("exit", () => {
    djangoProcess = null;
  });

  const ok = await waitForServer();
  if (!ok) {
    dialog.showErrorBox(
      "Mheibos",
      "Nao foi possivel iniciar o servidor local do Mheibos. Verifique o ambiente Python, o banco de dados e a porta 8765."
    );
  }
}

function abrirCaminhoLocal(url) {
  try {
    shell.openPath(fileURLToPath(url));
  } catch {
    shell.openExternal(url);
  }
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

  win.once("ready-to-show", () => win.show());
  win.setMenuBarVisibility(false);

  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith("file://")) abrirCaminhoLocal(url);
    else if (!url.startsWith(BASE_URL)) shell.openExternal(url);
    return { action: "deny" };
  });

  win.webContents.on("will-navigate", (event, url) => {
    if (url.startsWith(BASE_URL)) return;
    if (url.startsWith("file://")) abrirCaminhoLocal(url);
    else shell.openExternal(url);
    event.preventDefault();
  });

  win.webContents.on("before-input-event", (event, input) => {
    if (input.key === "F5" || ((input.control || input.meta) && input.key.toLowerCase() === "r")) {
      win.reload();
    }
  });

  win.loadURL(`${BASE_URL}${destinoInicial()}`);
}

app.whenReady().then(async () => {
  Menu.setApplicationMenu(null);
  await ensureDjango();
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
