(function () {
  if (!window.GestorPrefs) return;

  const dock = document.getElementById("widgetPrazos");
  const dockItems = document.getElementById("widgetPrazosItems");
  const dockEmpty = document.getElementById("widgetPrazosEmpty");
  const dockClose = document.getElementById("widgetPrazosClose");
  const intervention = document.getElementById("alertasIntervencao");
  const interventionItems = document.getElementById("alertasIntervencaoItens");
  const interventionSummary = document.getElementById("alertasIntervencaoResumo");
  const vivaAlertas = document.getElementById("interfaceVivaAlertas");
  const vivaAlertasBadge = document.getElementById("interfaceVivaAlertasBadge");
  const vivaToggleBadge = document.getElementById("interfaceVivaAlertasButtonBadge");
  const vivaAlertasResumo = document.getElementById("interfaceVivaAlertasResumo");
  const vivaAlertasLista = document.getElementById("interfaceVivaAlertasLista");
  const vivaSugestao = document.getElementById("interfaceVivaSugestao");
  const vivaSugestaoTitulo = document.getElementById("interfaceVivaSugestaoTitulo");
  const vivaSugestaoMotivo = document.getElementById("interfaceVivaSugestaoMotivo");
  const vivaSugestaoResumo = document.getElementById("interfaceVivaSugestaoResumo");
  const vivaSugestaoLink = document.getElementById("interfaceVivaSugestaoLink");
  const vivaSugestaoPedidos = document.getElementById("interfaceVivaSugestaoPedidos");
  const vivaToggle = document.getElementById("interfaceVivaToggle");
  const toast = document.getElementById("notifAssistencia");
  const toastText = document.getElementById("notifAssistenciaTexto");
  const toastLink = document.getElementById("notifAssistenciaLink");
  const toastClose = document.getElementById("notifAssistenciaClose");

  let timers = { prazos: null, assistencia: null };
  let ocultoManualPrazos = false;
  let ocultoManualAssistencia = false;
  let ultimaNotificacaoAssistencia = "";
  let ultimaIntervencao = "";

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

  function alternar(elemento, visivel) {
    if (!elemento) return;
    elemento.classList.toggle("hidden", !visivel);
    elemento.setAttribute("aria-hidden", visivel ? "false" : "true");
  }

  function esconderDock() { alternar(dock, false); }
  function mostrarDock() { alternar(dock, true); }
  function esconderToast() { alternar(toast, false); }
  function mostrarToast() { alternar(toast, true); }
  function esconderIntervencao() { alternar(intervention, false); }

  function aplicarPosicaoToast(posicao) {
    if (!toast) return;
    toast.classList.remove("pos-superior-direita", "pos-superior-esquerda", "pos-inferior-direita", "pos-inferior-esquerda", "pos-centro");
    const classes = {
      superior_esquerda: "pos-superior-esquerda",
      inferior_direita: "pos-inferior-direita",
      inferior_esquerda: "pos-inferior-esquerda",
      centro: "pos-centro",
    };
    toast.classList.add(classes[posicao] || "pos-superior-direita");
  }

  function aplicarPosicaoDock(posicao) {
    if (!dock) return;
    dock.classList.remove("pos-superior-direita", "pos-superior-esquerda", "pos-inferior-direita", "pos-inferior-esquerda", "pos-inferior-centro", "pos-centro");
    const classes = {
      superior_direita: "pos-superior-direita",
      superior_esquerda: "pos-superior-esquerda",
      inferior_direita: "pos-inferior-direita",
      inferior_esquerda: "pos-inferior-esquerda",
      centro: "pos-centro",
    };
    dock.classList.add(classes[posicao] || "pos-inferior-centro");
  }

  function renderDock(pedidos, conf) {
    if (!dockItems) return;
    aplicarPosicaoDock(conf.posicao);
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

  function renderInterfaceVivaAlertas(resumo) {
    if (!vivaAlertas || !vivaAlertasLista) return;
    renderMissaoSugestao(resumo.missao_sugestao);
    const itens = resumo.alertas || [];
    const total = Number(resumo.total_alertas || itens.length);
    vivaAlertasLista.innerHTML = "";
    vivaAlertas.classList.toggle("is-empty", !total);
    [vivaAlertasBadge, vivaToggleBadge].forEach((badge) => {
      if (!badge) return;
      badge.textContent = String(total);
      badge.classList.toggle("hidden", !total);
      badge.setAttribute("aria-hidden", total ? "false" : "true");
    });
    if (vivaToggle) {
      vivaToggle.setAttribute("aria-label", total ? `Abrir Interface Viva — ${total} alerta(s)` : "Abrir Interface Viva");
    }
    vivaAlertasResumo.textContent = total
      ? (total > itens.length ? `${total} alerta(s); exibindo os mais urgentes.` : `${total} alerta(s) ativo(s).`)
      : "Nenhum alerta ativo.";
    itens.forEach((item) => {
      const article = document.createElement("article");
      article.className = "interface-viva-alerta";
      if (Number(item.nivel) >= 4) article.classList.add("is-critical");
      const title = document.createElement("strong");
      title.textContent = `${item.pedido_label || "Pedido"} · ${item.titulo || "Alerta operacional"}`;
      article.appendChild(title);
      const message = document.createElement("p");
      message.textContent = item.mensagem || "Consulte o pedido para ver os detalhes.";
      article.appendChild(message);
      if (item.href) {
        const link = document.createElement("a");
        link.href = item.href;
        link.textContent = item.acao_label || "Abrir alerta";
        article.appendChild(link);
      }
      vivaAlertasLista.appendChild(article);
    });
  }

  function renderMissaoSugestao(sugestao) {
    if (!vivaSugestao) return;
    if (!sugestao) {
      alternar(vivaSugestao, false);
      return;
    }
    vivaSugestaoTitulo.textContent = sugestao.titulo || "Organizar problema operacional";
    vivaSugestaoMotivo.textContent = sugestao.motivo || "Há um conjunto de pedidos que precisa de acompanhamento contínuo.";
    vivaSugestaoResumo.textContent = sugestao.resumo || "Revise a proposta antes de criar a missão.";
    vivaSugestaoLink.href = sugestao.revisar_url || "/missoes/nova/";
    vivaSugestaoPedidos.href = sugestao.pedidos_url || "/pedidos/?atrasados=1";
    alternar(vivaSugestao, true);
  }
  function renderIntervencao(resumo) {
    if (!intervention || !interventionItems) return;
    const itens = (resumo.alertas || []).filter((item) => item.exige_acao || Number(item.nivel) >= 3);
    interventionItems.innerHTML = "";
    if (!itens.length) {
      esconderIntervencao();
      ultimaIntervencao = "";
      return;
    }
    itens.forEach((item) => {
      const article = document.createElement("article");
      article.className = "alerta-intervencao-item";
      if (Number(item.nivel) >= 4) article.classList.add("is-critico");

      const badge = document.createElement("span");
      badge.className = "alerta-intervencao-badge";
      badge.textContent = Number(item.nivel) >= 4 ? "Ação crítica necessária" : "Resposta necessária";
      article.appendChild(badge);

      const title = document.createElement("h3");
      title.textContent = `${item.pedido_label || "Pedido"} · ${item.titulo || "Alerta operacional"}`;
      article.appendChild(title);

      const message = document.createElement("p");
      message.textContent = item.mensagem || "Abra o pedido para consultar a ação necessária.";
      article.appendChild(message);

      const meta = document.createElement("p");
      meta.className = "alerta-intervencao-meta";
      meta.textContent = item.pode_dispensar === false
        ? "Este alerta permanece visível até uma ação válida ser registrada."
        : "A decisão deve ser registrada no pedido.";
      article.appendChild(meta);

      if (item.href) {
        const link = document.createElement("a");
        link.href = item.href;
        link.className = "alerta-intervencao-action";
        link.textContent = item.acao_label || "Abrir e responder";
        article.appendChild(link);
      }
      interventionItems.appendChild(article);
    });
    const total = Number(resumo.total_exige_acao || itens.length);
    interventionSummary.textContent = total > itens.length
      ? `${total} decisão(ões) exigem resposta. Mostrando as mais urgentes.`
      : `${total} decisão(ões) exigem resposta.`;
    const assinatura = itens.map((item) => item.id).join("|");
    if (assinatura !== ultimaIntervencao) {
      ultimaIntervencao = assinatura;
      intervention.classList.add("is-new");
      setTimeout(() => intervention.classList.remove("is-new"), 900);
    }
    alternar(intervention, true);
  }

  function renderToast(resumo) {
    if (!toastText || !toastLink) return;
    const normais = (resumo.alertas || []).filter((item) => !item.exige_acao && Number(item.nivel) < 3);
    if (!normais.length) {
      esconderToast();
      return;
    }
    const grupos = {};
    normais.forEach((item) => {
      const chave = item.categoria_nome || "Assistência";
      grupos[chave] = (grupos[chave] || 0) + 1;
    });
    const partes = Object.entries(grupos).map(([nome, quantidade]) => `${nome}: ${quantidade}`);
    const texto = `${normais.length} pedido(s) aguardam atenção${partes.length ? ` (${partes.join(" · ")})` : ""}`;
    toastText.textContent = texto;
    toastLink.href = normais[0].href || resumo.url || "/assistencia-envio/";
    toast?.classList.remove("is-alert");
    mostrarToast();
    const assinatura = `${normais.map((item) => item.id).join("|")}`;
    if (window.mheibosDesktop?.notificar && assinatura !== ultimaNotificacaoAssistencia) {
      ultimaNotificacaoAssistencia = assinatura;
      window.mheibosDesktop.notificar({
        title: "Atenção operacional",
        body: texto,
        url: toastLink.href,
      }).catch(() => {});
    }
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
    if (!intervention && !toast) return;
    const conf = prefs().widgets.assistencia;
    try {
      const dados = await fetchJson("/api/notificacoes/assistencia/" + categoriasQuery(prefs().widgets.prazos.categorias));
      const exigeAcao = Boolean(dados.exige_acao);
      if (!dados.total && !dados.total_alertas && !dados.missao_sugestao) {
        renderInterfaceVivaAlertas({alertas: [], total_alertas: 0, missao_sugestao: null});
        esconderIntervencao();
        esconderToast();
        if (cicloCompleto) agendarAssistencia(conf, conf.intervalo_minutos * 60 * 1000);
        return;
      }
      renderInterfaceVivaAlertas(dados);
      renderIntervencao(dados);
      renderToast(dados);
      if (exigeAcao) {
        agendarAssistencia(conf, 60 * 1000);
        return;
      }
      if (!conf.ativo) {
        esconderToast();
        if (cicloCompleto) agendarAssistencia(conf, conf.intervalo_minutos * 60 * 1000);
        return;
      }
      if (ocultoManualAssistencia && conf.modo !== "sempre") {
        agendarAssistencia(conf, conf.intervalo_minutos * 60 * 1000);
        return;
      }
      aplicarPosicaoToast(conf.posicao);
      if (conf.modo === "sempre") {
        agendarAssistencia(conf, 60 * 1000);
      } else if (cicloCompleto) {
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