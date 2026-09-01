function resolveRemoteBaseUrl({ appName = "", envBaseUrl = "", clientConfig = {} } = {}) {
  const isClientBuild = String(appName).toLowerCase().includes("cliente");
  return String(envBaseUrl || (isClientBuild ? clientConfig.serverUrl : "")).replace(/\/$/, "");
}

module.exports = { resolveRemoteBaseUrl };
