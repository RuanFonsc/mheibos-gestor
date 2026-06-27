const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("mheibosSetup", {
  salvar: (config) => ipcRenderer.invoke("setup:save", config),
  cancelar: () => ipcRenderer.invoke("setup:cancel"),
});

window.addEventListener("DOMContentLoaded", () => {
  document.documentElement.dataset.desktop = "electron";
});
