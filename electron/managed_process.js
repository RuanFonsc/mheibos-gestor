"use strict";

/**
 * Mantém um serviço local ativo durante a vida do Electron.
 * O processo é reiniciado automaticamente quando cai, mas nunca depois de stop().
 */
function createManagedProcess({
  spawnProcess,
  restartDelayMs = 2000,
  setTimeoutFn = setTimeout,
  clearTimeoutFn = clearTimeout,
}) {
  let child = null;
  let desired = false;
  let currentSpec = null;
  let restartTimer = null;
  let startPromise = null;

  const scheduleRestart = () => {
    if (!desired || restartTimer || !currentSpec) return;
    restartTimer = setTimeoutFn(() => {
      restartTimer = null;
      return start(currentSpec);
    }, restartDelayMs);
    restartTimer.unref?.();
  };

  const start = (spec) => {
    desired = true;
    currentSpec = spec;
    if (child && !child.killed) return Promise.resolve(true);
    if (startPromise) return startPromise;

    startPromise = new Promise((resolve) => {
      let settled = false;
      const settle = (value) => {
        if (settled) return;
        settled = true;
        resolve(value);
      };
      const invocation = currentSpec;
      let spawned;
      try {
        spawned = spawnProcess(invocation.command, invocation.args, invocation.options);
      } catch {
        settle(false);
        scheduleRestart();
        return;
      }
      child = spawned;
      const handleExit = () => {
        if (child === spawned) child = null;
        settle(false);
        scheduleRestart();
      };
      spawned.once("spawn", () => settle(true));
      spawned.once("error", () => handleExit());
      spawned.once("exit", () => handleExit());
    }).finally(() => {
      startPromise = null;
    });
    return startPromise;
  };

  const stop = () => {
    desired = false;
    currentSpec = null;
    if (restartTimer) {
      clearTimeoutFn(restartTimer);
      restartTimer = null;
    }
    const running = child;
    child = null;
    if (running && !running.killed) running.kill();
  };

  return {
    start,
    stop,
    isRunning: () => Boolean(child && !child.killed),
  };
}

module.exports = { createManagedProcess };
