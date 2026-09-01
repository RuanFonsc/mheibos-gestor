const assert = require("assert");

const { resolveRemoteBaseUrl } = require("./runtime_profile");

const clientConfig = { serverUrl: "http://central-teste:8001/" };

assert.strictEqual(
  resolveRemoteBaseUrl({ appName: "Mheibos Suite", clientConfig }),
  "",
  "Suite deve iniciar como Central mesmo que um client-config antigo exista"
);
assert.strictEqual(
  resolveRemoteBaseUrl({ appName: "Mheibos Gestor Cliente", clientConfig }),
  "http://central-teste:8001",
  "Cliente deve usar a Central definida no client-config"
);
assert.strictEqual(
  resolveRemoteBaseUrl({ appName: "Mheibos Suite", envBaseUrl: "http://override:8001/", clientConfig }),
  "http://override:8001",
  "Variável explícita deve continuar permitindo uma conexão remota"
);

console.log("runtime_profile.test.js: PASS");
