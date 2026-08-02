function encryptSecret(value, safeStorage) {
  if (!value) return "";
  if (!safeStorage.isEncryptionAvailable()) {
    throw new Error("A protecao de credenciais do Windows nao esta disponivel.");
  }
  return safeStorage.encryptString(String(value)).toString("base64");
}

function decryptSecret(value, safeStorage) {
  if (!value || !safeStorage.isEncryptionAvailable()) return "";
  try {
    return safeStorage.decryptString(Buffer.from(value, "base64"));
  } catch {
    return "";
  }
}

function protectConfigSecrets(config, safeStorage) {
  const protectedConfig = JSON.parse(JSON.stringify(config || {}));
  if (protectedConfig.postgres?.password) {
    protectedConfig.postgres.passwordEncrypted = encryptSecret(
      protectedConfig.postgres.password,
      safeStorage
    );
    delete protectedConfig.postgres.password;
  }
  if (protectedConfig.stationSecret) {
    protectedConfig.stationSecretEncrypted = encryptSecret(
      protectedConfig.stationSecret,
      safeStorage
    );
    delete protectedConfig.stationSecret;
  }
  if (protectedConfig.offlineIdentity) {
    protectedConfig.offlineIdentityEncrypted = encryptSecret(
      protectedConfig.offlineIdentity,
      safeStorage
    );
    delete protectedConfig.offlineIdentity;
  }
  return protectedConfig;
}

module.exports = { decryptSecret, protectConfigSecrets };
