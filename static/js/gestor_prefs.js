(function () {
  const STORAGE_KEY = "gestor_prefs_v1";

  const DEFAULTS = {
    tema: "dark",
    zoom: 100,
    usuario: "Ruan",
    widgets: {
      prazos: {
        ativo: true,
        modo: "periodico",
        intervalo_minutos: 30,
        visivel_segundos: 60,
        categorias: [],
      },
      assistencia: {
        ativo: true,
        modo: "periodico",
        intervalo_minutos: 15,
        visivel_segundos: 30,
      },
    },
  };

  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function mergePrefs(base, patch) {
    const result = clone(base);
    if (!patch || typeof patch !== "object") return result;
    if (patch.tema) result.tema = patch.tema;
    if (patch.zoom !== undefined) result.zoom = Number(patch.zoom) || base.zoom;
    if (patch.usuario) result.usuario = String(patch.usuario).trim() || base.usuario;
    if (patch.widgets) {
      ["prazos", "assistencia"].forEach((chave) => {
        if (!patch.widgets[chave]) return;
        result.widgets[chave] = { ...result.widgets[chave], ...patch.widgets[chave] };
      });
    }
    return result;
  }

  function serverBoot() {
    const node = document.getElementById("gestor-prefs-server");
    if (!node) return null;
    try {
      return JSON.parse(node.textContent || "{}");
    } catch (_) {
      return null;
    }
  }

  function loadPrefs() {
    const boot = serverBoot();
    if (boot) return mergePrefs(DEFAULTS, boot);
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return clone(DEFAULTS);
      return mergePrefs(DEFAULTS, JSON.parse(raw));
    } catch (_) {
      return clone(DEFAULTS);
    }
  }

  function csrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta?.content) return meta.content;
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : "";
  }

  async function persistServer(merged) {
    const response = await fetch("/api/preferencias/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "X-CSRFToken": csrfToken(),
      },
      body: JSON.stringify(merged),
      credentials: "same-origin",
    });
    if (!response.ok) throw new Error("Falha ao salvar preferências no servidor");
    return response.json();
  }

  async function savePrefs(patch) {
    const merged = mergePrefs(loadPrefs(), patch);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(merged));
    const node = document.getElementById("gestor-prefs-server");
    try {
      const saved = await persistServer(merged);
      if (node) node.textContent = JSON.stringify(saved);
      applyPrefs(saved);
      window.dispatchEvent(new CustomEvent("gestor:prefs", { detail: saved }));
      return saved;
    } catch (error) {
      if (node) node.textContent = JSON.stringify(merged);
      applyPrefs(merged);
      window.dispatchEvent(new CustomEvent("gestor:prefs", { detail: merged }));
      throw error;
    }
  }

  function applyTheme(tema) {
    document.documentElement.setAttribute("data-theme", tema === "light" ? "light" : "dark");
  }

  function applyZoom(zoom) {
    const escala = Math.max(0.75, Math.min(2, Number(zoom) / 100 || 1));
    document.documentElement.style.setProperty("--ui-scale", String(escala));
    const shell = document.querySelector(".app-shell");
    if (shell) shell.style.zoom = String(escala);
  }

  function applyUsuario(usuario) {
    const alvo = document.getElementById("topbarUsuario");
    if (alvo) alvo.textContent = `Usuário: ${usuario}`;
    const campo = document.getElementById("configUsuario");
    if (campo) campo.value = usuario;
    const select = document.getElementById("configUsuarioSelect");
    if (select) select.value = usuario;
    const hidden = document.getElementById("usuarioCadastroInput");
    if (hidden) hidden.value = usuario;
  }

  function applyPrefs(prefs) {
    applyTheme(prefs.tema);
    applyZoom(prefs.zoom);
    applyUsuario(prefs.usuario);
  }

  window.GestorPrefs = {
    DEFAULTS,
    load: loadPrefs,
    save: savePrefs,
    apply: applyPrefs,
    applyTheme,
    applyZoom,
    applyUsuario,
    persistServer,
  };

  applyPrefs(loadPrefs());
})();
