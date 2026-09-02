"use strict";

const assert = require("assert");
const { EventEmitter } = require("events");
const { createManagedProcess } = require("./managed_process");

const children = [];
const scheduled = [];
const spawnProcess = () => {
  const child = new EventEmitter();
  child.killed = false;
  child.kill = () => {
    if (child.killed) return;
    child.killed = true;
    child.emit("exit", null, "SIGTERM");
  };
  children.push(child);
  return child;
};

const supervisor = createManagedProcess({
  spawnProcess,
  setTimeoutFn: (callback) => {
    const handle = { callback, unref() {} };
    scheduled.push(handle);
    return handle;
  },
  clearTimeoutFn: (handle) => {
    const index = scheduled.indexOf(handle);
    if (index >= 0) scheduled.splice(index, 1);
  },
});

(async () => {
  const spec = { command: "worker", args: ["--loop"], options: {} };
  const initialStart = supervisor.start(spec);
  assert.strictEqual(children.length, 1);
  children[0].emit("spawn");
  assert.strictEqual(await initialStart, true);
  assert.strictEqual(supervisor.isRunning(), true);

  children[0].emit("exit", 1, null);
  assert.strictEqual(supervisor.isRunning(), false);
  assert.strictEqual(scheduled.length, 1);

  const restartStart = scheduled.shift().callback();
  assert.strictEqual(children.length, 2);
  children[1].emit("spawn");
  assert.strictEqual(await restartStart, true);
  assert.strictEqual(supervisor.isRunning(), true);

  supervisor.stop();
  assert.strictEqual(supervisor.isRunning(), false);
  assert.strictEqual(scheduled.length, 0);
  children[1].emit("exit", 0, null);
  assert.strictEqual(scheduled.length, 0);
  console.log("managed_process.test.js: PASS");
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
