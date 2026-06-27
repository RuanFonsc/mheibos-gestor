(function () {
  if (!window.GestorPrefs) return;

  const dock = document.getElementById("widgetPrazos");
  const dockItems = document.getElementById("widgetPrazosItems");
  const dockEmpty = document.getElementById("widgetPrazosEmpty");
  const dockClose = document.getElementById("widgetPrazosClose");
  const toast = document.getElementById("notifAssistencia");
  const toastText = document.getElementById("notifAssistenciaTexto");
  const toastLink = document.getElementById("notifAssistenciaLink");
  const toastClose = document.getElementById("notifAssistenciaClose");

  let timers = { prazos: null, assistencia: null };
  let ocultoManualPrazos = false;
  let ocultoManualAssistencia = false;

  function prefs() {
    return GestorPrefs.load();
  }

  function categoriasQuery(prefCategorias) {
    const ids = (prefCategorias || []).filter(Boolean);
    return ids.length ? `?categorias=${ids.join(",")}` : "";
  }

  async function fetchJson(path) {
    const response = await fetch(path, { headers: { Accept: "application/json" }, credentials: "same-origin" });
    if (!response.ok) throw new Error(`Falha na consulta: ${path}`);
    return response.json();
  }

  function limparTimer(chave) {
    if (timers[chave]) {
      clearTimeout(timers[chave]);
      timers[chave] = null;
    }
  }

  function esconderDock() {
    dock?.classList.add("hidden");
    dock?.setAttribute("aria-hidden", "true");
  }

  function mostrarDock() {
    dock?.classList.remove("hidden");
    dock?.setAttribute("aria-hidden", "false");
  }

  function esconderToast() {
    toast?.classList.add("hidden");
    toast?.setAttribute("aria-hidden", "true");
  }

  function mostrarToast() {
    toast?.classList.remove("hidden");
    toast?.setAttribute("aria-hidden", "false");
  }

  function renderDock(pedidos, conf) {
    if (!dockItems) return;
    dockItems.innerHTML = "";
    if (!pedidos.length) {
      if (conf.modo === "sempre" && conf.ativo) {
        dockEmpty?.classList.remove("hidden");
        mostrarDock();
      } else {
        dockEmpty?.classList.add("hidden");
        esconderDock();
      }
      return;
    }
    dockEmpty?.classList.add("hidden");
    pedidos.forEach((pedido) => {
      const link = document.createElement("a");
      link.href = pedido.url;
      link.className = "widget-prazo-item";
      if (pedido.alerta) link.classList.add("is-alert");
      link.title = `#${pedido.legado_id || pedido.id} — ${pedido.cliente}`;
      if (pedido.arte_url) {
        const img = document.createElement("img");
        img.src = pedido.arte_url;
        img.alt = pedido.cliente;
        link.appendChild(img);
      } else {
        const placeholder = document.createElement("span");
        placeholder.className = "widget-prazo-placeholder";
        placeholder.textContent = pedido.categoria_curta || "Arte";
        link.appendChild(placeholder);
      }
      const legenda = document.createElement("span");
      legenda.className = "widget-prazo-label";
      legenda.textContent = pedido.categoria_curta || pedido.categoria_nome;
      link.appendChild(legenda);
      dockItems.appendChild(link);
    });
    mostrarDock();
  }

  function renderToast(resumo) {
    if (!toastText || !toastLink) return;
    if (!resumo.total) {
      esconderToast();
      return;
    }
    const partes = resumo.por_categoria.map((item) => `${item.nome}: ${item.count}`);
    toastText.textContent = `${resumo.total} pedido(s) na assistência de envio${partes.length ? ` (${partes.join(" · ")})` : ""}`;
    toastLink.href = resumo.url || "/assistencia-envio/";
    toast?.classList.toggle("is-alert", Boolean(resumo.alerta));
    mostrarToast();
  }

  function agendarPrazos(cfg, atrasoMs) {
    limparTimer("prazos");
    timers.prazos = setTimeout(() => atualizarPrazos(true), Math.max(1000, atrasoMs));
  }

  function agendarAssistencia(cfg, atrasoMs) {
    limparTimer("assistencia");
    timers.assistencia = setTimeout(() => atualizarAssistencia(true), Math.max(1000, atrasoMs));
  }

  async function atualizarPrazos(cicloCompleto) {
    const conf = prefs().widgets.prazos;
    if (!conf.ativo) {
      esconderDock();
      return;
    }
    if (ocultoManualPrazos && conf.modo !== "sempre") {
      agendarPrazos(conf, conf.intervalo_minutos * 60 * 1000);
      return;
    }
    try {
      const dados = await fetchJson("/api/widgets/prazos/" + categoriasQuery(conf.categorias));
      renderDock(dados.pedidos || [], conf);
      if (conf.modo === "sempre") {
        agendarPrazos(conf, 60 * 1000);
        return;
      }
      if (cicloCompleto && (dados.pedidos || []).length) {
        timers.prazos = setTimeout(() => {
          esconderDock();
          agendarPrazos(conf, conf.intervalo_minutos * 60 * 1000);
        }, conf.visivel_segundos * 1000);
      } else if (cicloCompleto) {
        agendarPrazos(conf, conf.intervalo_minutos * 60 * 1000);
      }
    } catch (error) {
      console.warn("Widget de prazos:", error);
      if (cicloCompleto) agendarPrazos(conf, conf.intervalo_minutos * 60 * 1000);
    }
  }

  async function atualizarAssistencia(cicloCompleto) {
    const conf = prefs().widgets.assistencia;
    if (!conf.ativo) {
      esconderToast();
      return;
    }
    if (ocultoManualAssistencia && conf.modo !== "sempre") {
      agendarAssistencia(conf, conf.intervalo_minutos * 60 * 1000);
      return;
    }
    try {
      const categorias = prefs().widgets.prazos.categorias;
      const dados = await fetchJson("/api/notificacoes/assistencia/" + categoriasQuery(categorias));
      if (!dados.total) {
        esconderToast();
        if (cicloCompleto) agendarAssistencia(conf, conf.intervalo_minutos * 60 * 1000);
        return;
      }
      renderToast(dados);
      if (conf.modo === "sempre") {
        agendarAssistencia(conf, 60 * 1000);
        return;
      }
      if (cicloCompleto) {
        timers.assistencia = setTimeout(() => {
          esconderToast();
          agendarAssistencia(conf, conf.intervalo_minutos * 60 * 1000);
        }, conf.visivel_segundos * 1000);
      }
    } catch (error) {
      console.warn("Notificação assistência:", error);
      if (cicloCompleto) agendarAssistencia(conf, conf.intervalo_minutos * 60 * 1000);
    }
  }

  function reiniciar() {
    Object.keys(timers).forEach(limparTimer);
    ocultoManualPrazos = false;
    ocultoManualAssistencia = false;
    atualizarPrazos(true);
    atualizarAssistencia(true);
  }

  function verificarAgora() {
    ocultoManualPrazos = false;
    ocultoManualAssistencia = false;
    atualizarPrazos(false);
    atualizarAssistencia(false);
  }

  dockClose?.addEventListener("click", () => {
    ocultoManualPrazos = true;
    esconderDock();
    const conf = prefs().widgets.prazos;
    if (conf.modo !== "sempre") agendarPrazos(conf, conf.intervalo_minutos * 60 * 1000);
  });

  toastClose?.addEventListener("click", () => {
    ocultoManualAssistencia = true;
    esconderToast();
    const conf = prefs().widgets.assistencia;
    if (conf.modo !== "sempre") agendarAssistencia(conf, conf.intervalo_minutos * 60 * 1000);
  });

  window.addEventListener("gestor:prefs", reiniciar);
  window.addEventListener("gestor:widgets-verificar", verificarAgora);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) verificarAgora();
  });

  window.GestorWidgets = { reiniciar, verificarAgora };
  document.addEventListener("DOMContentLoaded", () => setTimeout(reiniciar, 800));
})();
