const { contextBridge, ipcRenderer, webUtils } = require("electron");

contextBridge.exposeInMainWorld("mheibosSetup", {
  salvar: (config) => ipcRenderer.invoke("setup:save", config),
  cancelar: () => ipcRenderer.invoke("setup:cancel"),
});

contextBridge.exposeInMainWorld("mheibosArquivos", {
  selecionarCorel: () => ipcRenderer.invoke("corel:select-file"),
  normalizarCorel: (filePath) => ipcRenderer.invoke("corel:normalize-path", filePath),
  abrirCorel: (filePath) => ipcRenderer.invoke("corel:open-path", filePath),
  caminhoArquivo: (file) => webUtils.getPathForFile(file),
});

contextBridge.exposeInMainWorld("mheibosDesktop", {
  notificar: (payload) => ipcRenderer.invoke("desktop:notify", payload),
});

contextBridge.exposeInMainWorld("mheibosClipboard", {
  lerImagem: () => ipcRenderer.invoke("clipboard:read-image"),
});

window.addEventListener("DOMContentLoaded", () => {
  document.documentElement.dataset.desktop = "electron";
  document.addEventListener("submit", (event) => {
    const form = event.target;
    const usuario = form?.querySelector?.('[name="usuario"]')?.value || "";
    const senha = form?.querySelector?.('[name="senha"]')?.value || "";
    if (usuario && senha) {
      ipcRenderer.invoke("offline-identity:candidate", { usuario, senha });
    }
  });
});
