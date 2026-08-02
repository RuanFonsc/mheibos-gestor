const assert = require("assert");
const { decryptSecret, protectConfigSecrets } = require("./secure_config");

const safeStorage = {
  isEncryptionAvailable: () => true,
  encryptString: (value) => Buffer.from(`protegido:${value}`, "utf8"),
  decryptString: (buffer) => buffer.toString("utf8").replace(/^protegido:/, ""),
};

const original = {
  mode: "remote",
  stationId: "estacao-1",
  stationSecret: "segredo-estacao",
  postgres: { password: "segredo-banco" },
};
const protectedConfig = protectConfigSecrets(original, safeStorage);
const persisted = JSON.stringify(protectedConfig);

assert.strictEqual(original.stationSecret, "segredo-estacao");
assert.strictEqual(protectedConfig.stationSecret, undefined);
assert.strictEqual(protectedConfig.postgres.password, undefined);
assert.ok(!persisted.includes("segredo-estacao"));
assert.ok(!persisted.includes("segredo-banco"));
assert.strictEqual(
  decryptSecret(protectedConfig.stationSecretEncrypted, safeStorage),
  "segredo-estacao"
);
assert.strictEqual(
  decryptSecret(protectedConfig.postgres.passwordEncrypted, safeStorage),
  "segredo-banco"
);
assert.throws(
  () => protectConfigSecrets(original, { isEncryptionAvailable: () => false }),
  /protecao de credenciais/
);

process.stdout.write("secure_config: PASS\n");
