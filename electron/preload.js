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

window.addEventListener("DOMContentLoaded", () => {
  document.documentElement.dataset.desktop = "electron";
});
