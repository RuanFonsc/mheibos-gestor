const assert = require("assert");

const { offlineRuntimeConfig, readOfflineIdentity } = require("./offline_runtime");

const safeStorage = {
  isEncryptionAvailable: () => true,
  decryptString: (buffer) => buffer.toString("utf8"),
};
const identity = {
  estacao_id: "station-1",
  operador: { nome: "Ana" },
  senha: "segredo-local",
};
const config = {
  stationId: "station-1",
  offlineIdentityEncrypted: Buffer.from(JSON.stringify(identity)).toString("base64"),
};

assert.deepStrictEqual(readOfflineIdentity(config, safeStorage), identity);
assert.strictEqual(readOfflineIdentity({ ...config, stationId: "station-2" }, safeStorage), null);
assert.deepStrictEqual(offlineRuntimeConfig(config), {
  ...config,
  mode: "sqlite",
  runtimeRole: "client_offline",
  sqlite: { name: "mheibos_offline" },
});

console.log("offline_runtime.test.js: PASS");
