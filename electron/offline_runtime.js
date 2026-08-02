const { decryptSecret } = require("./secure_config");

function offlineRuntimeConfig(config) {
  return {
    ...(config || {}),
    mode: "sqlite",
    runtimeRole: "client_offline",
    sqlite: { name: "mheibos_offline" },
  };
}

function readOfflineIdentity(config, safeStorage) {
  const raw = decryptSecret(config?.offlineIdentityEncrypted, safeStorage);
  if (!raw) return null;
  try {
    const identity = JSON.parse(raw);
    if (!identity?.estacao_id || identity.estacao_id !== config?.stationId) return null;
    if (!identity?.operador?.nome || !identity?.senha) return null;
    return identity;
  } catch {
    return null;
  }
}

module.exports = { offlineRuntimeConfig, readOfflineIdentity };
