(() => {
  const toggle = document.getElementById("interfaceVivaToggle");
  const drawer = document.getElementById("interfaceVivaDrawer");
  const close = document.getElementById("interfaceVivaClose");
  const form = document.getElementById("interfaceVivaForm");
  const input = document.getElementById("interfaceVivaInput");
  const messages = document.getElementById("interfaceVivaMessages");
  const status = document.getElementById("interfaceVivaStatus");
  const csrf = document.querySelector('meta[name="csrf-token"]')?.content || "";
  let conversationId = "";

  function registrarAtividade(tipo, alvoTipo = "", alvoId = "", dados = {}) {
    fetch("/cognicao/atividade/", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
      credentials: "same-origin",
      body: JSON.stringify({ tipo, alvo_tipo: alvoTipo, alvo_id: alvoId, dados }),
    }).catch(() => {});
  }

  const open = () => { toggle?.classList.remove("interface-viva-has-notification"); drawer?.classList.add("is-open"); drawer?.setAttribute("aria-hidden", "false"); toggle?.setAttribute("aria-expanded", "true"); input?.focus(); };
  const hide = () => { drawer?.classList.remove("is-open"); drawer?.setAttribute("aria-hidden", "true"); toggle?.setAttribute("aria-expanded", "false"); };
  toggle?.addEventListener("click", open); close?.addEventListener("click", hide);

  function actionButton(label, command) {
    const button = document.createElement("button");
    button.type = "button"; button.className = "interface-viva-action"; button.textContent = label;
    button.addEventListener("click", () => executar(command));
    return button;
  }
  function feedbackButton(interventionId, response) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "interface-viva-feedback";
    button.textContent = response === "aceitar" ? "Entendi" : response === "resolver" ? "Marcar como tratada" : "Não agora";
    button.addEventListener("click", async () => {
      button.disabled = true;
      try {
        const result = await fetch(`/cognicao/assistente/intervencoes/${interventionId}/resposta/`, {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
          credentials: "same-origin",
          body: JSON.stringify({ resposta: response }),
        });
        const data = await result.json();
        if (!result.ok) throw new Error(data.erro || "Não foi possível registrar a resposta.");
        button.parentElement?.querySelectorAll("button").forEach((item) => { item.disabled = true; });
        button.parentElement?.setAttribute("aria-label", "Resposta da intervenção registrada");
        status.textContent = "Resposta registrada.";
      } catch (error) {
        button.disabled = false;
        status.textContent = error.message;
      }
    });
    return button;
  }
  function message(text, role, commands = [], interventionId = null) {
    const item = document.createElement("article"); item.className = `interface-viva-message ${role}`;
    const body = document.createElement("p"); body.textContent = text; item.appendChild(body);
    commands.forEach((command) => item.appendChild(actionButton(command.rotulo || "Executar", command)));
    if (interventionId) {
      const feedback = document.createElement("div");
      feedback.className = "interface-viva-feedback-list";
      feedback.setAttribute("aria-label", "Resposta à intervenção");
      feedback.appendChild(feedbackButton(interventionId, "aceitar"));
      feedback.appendChild(feedbackButton(interventionId, "resolver"));
      feedback.appendChild(feedbackButton(interventionId, "ignorar"));
      item.appendChild(feedback);
    }
    messages?.appendChild(item); messages?.scrollTo({ top: messages.scrollHeight, behavior: "smooth" });
  }
  function selectorFor(command) {
    const field = command.parametros?.campo;
    return field ? `[name="${CSS.escape(field)}"]` : "";
  }
  function executar(command) {
    const params = command.parametros || command;
    if (command.comando === "navegar" || command.comando === "navegar_pedido" || command.comando === "abrir_pedido") {
      let route = params.rota || (params.pedido_id ? `/pedidos/${params.pedido_id}/` : "");
      if (params.valores) { navegarComPreenchimento(params, route); return; }
      if (route && params.campo) { const url = new URL(route, window.location.origin); url.searchParams.set("iv_focus", params.campo); route = url.pathname + url.search; }
      if (route) window.location.assign(route); return;
    }
    if (command.comando === "destacar_campo") {
      const element = document.querySelector(selectorFor(command)); if (!element) { message("Abra a tela indicada para destacar este campo.", "mheibos"); return; }
      element.scrollIntoView({ block: "center", behavior: "smooth" }); element.classList.add("interface-viva-highlight"); element.focus(); setTimeout(() => element.classList.remove("interface-viva-highlight"), 3500); return;
    }
    if (command.comando === "destacar_acao") {
      const label = String(params.acao || params.rotulo || "").trim().toLocaleLowerCase();
      const element = [...document.querySelectorAll("button:not(.interface-viva-action):not(#interfaceVivaToggle):not(#interfaceVivaClose), a[href], input[type=submit], input[type=button]")].filter((candidate) => {
        const computedStyle = getComputedStyle(candidate);
        return candidate.getClientRects().length > 0 && computedStyle.visibility !== "hidden" && computedStyle.display !== "none" && !candidate.closest("#gestorConfirmModal, .interface-viva-drawer");
      }).sort((left, right) => {
        const leftText = (left.textContent || left.value || left.getAttribute("aria-label") || left.title || "").trim().toLocaleLowerCase();
        const rightText = (right.textContent || right.value || right.getAttribute("aria-label") || right.title || "").trim().toLocaleLowerCase();
        return Number(rightText === label) - Number(leftText === label);
      }).find((candidate) => {
        const text = (candidate.textContent || candidate.value || candidate.getAttribute("aria-label") || candidate.title || "").trim().toLocaleLowerCase();
        return label && text.includes(label);
      });
      if (!element) { message("Abra a tela indicada para destacar essa ação.", "mheibos"); return; }
      element.scrollIntoView({ block: "center", behavior: "smooth" }); element.classList.add("interface-viva-highlight"); element.focus(); setTimeout(() => element.classList.remove("interface-viva-highlight"), 3500); return;
    }
    if (command.comando === "preencher_campos") {
      preencherProposta(params.valores || {}); return;
    }
    if (command.comando === "pesquisar_pedidos") { window.location.assign(`/pedidos/?q=${encodeURIComponent(params.termo || "")}`); return; }
    if (command.comando === "confirmar_alteracao_status") { confirmarStatus(params); }
  }
  async function navegarComPreenchimento(params, route) {
    const approved = await window.GestorConfirm?.ask?.({ title: "Preencher proposta?", message: "Abrir Novo Pedido e preencher os campos com a proposta da IA? Nada será salvo até você enviar o formulário.", okText: "Abrir e preencher", cancelText: "Voltar" });
    if (!approved) return;
    const url = new URL(route, window.location.origin);
    if (params.campo) url.searchParams.set("iv_focus", params.campo);
    url.searchParams.set("iv_fill", JSON.stringify(params.valores));
    window.location.assign(url.pathname + url.search);
  }
  async function preencherProposta(values) {
    const approved = await window.GestorConfirm?.ask?.({ title: "Preencher proposta?", message: "Preencher os campos com a proposta da IA? Nada será salvo até você enviar o formulário.", okText: "Preencher", cancelText: "Voltar" });
    if (!approved) return;
    Object.entries(values).forEach(([name, value]) => {
      const element = document.querySelector(`[name="${CSS.escape(name)}"]`);
      if (!element) return;
      if (element.type === "checkbox") element.checked = Boolean(value); else element.value = value;
      element.dispatchEvent(new Event("input", { bubbles: true }));
      element.dispatchEvent(new Event("change", { bubbles: true }));
      element.classList.add("interface-viva-highlight");
      setTimeout(() => element.classList.remove("interface-viva-highlight"), 3500);
    });
    message("Campos preenchidos como proposta. Revise-os e use o botão Salvar do formulário quando estiver pronto.", "mheibos");
  }
  async function pollAlertasIA() {
    try {
      const response = await fetch("/cognicao/assistente/notificacoes-alertas/", { headers: { Accept: "application/json" }, credentials: "same-origin" });
      if (!response.ok) return;
      const data = await response.json();
      (data.notificacoes || []).forEach((notificacao) => {
        message(notificacao.texto, "mheibos", notificacao.comandos || [], notificacao.intervencao_id);
        toggle?.classList.add("interface-viva-has-notification");
        toggle?.setAttribute("aria-label", "Abrir Interface Viva — nova análise de alerta");
        if (Number(notificacao.alerta?.nivel) >= 4) {
          open();
          status.textContent = "A IA identificou um alerta crítico que exige atenção.";
        }
      });
    } catch (_) {}
  }

  async function confirmarStatus(params) {
    const approved = await window.GestorConfirm?.ask?.({ title: "Confirmar alteração", message: "Alterar o status do pedido?", okText: "Confirmar", cancelText: "Voltar" });
    if (!approved) return;
    const response = await fetch("/cognicao/assistente/acoes/alterar-status/", { method: "POST", headers: { "Content-Type": "application/json", "X-CSRFToken": csrf }, body: JSON.stringify(params) });
    const data = await response.json(); message(response.ok ? `Status confirmado: ${data.status}.` : (data.erro || "Não foi possível alterar o status."), "mheibos");
  }
  function interfaceContext() {
    const byId = new Map([...document.querySelectorAll("label[for]")].map((label) => [label.htmlFor, label.textContent.trim()]));
    const labelFor = (element) => {
      const direct = byId.get(element.id);
      if (direct) return direct;
      const wrapped = element.closest("label");
      if (wrapped) return wrapped.textContent.trim().replace(/\s+/g, " ");
      let container = element.parentElement;
      for (let depth = 0; container && depth < 4; depth += 1, container = container.parentElement) {
        const directLabel = [...container.children].find((child) => child.matches?.("label, .field-label"));
        if (directLabel && !directLabel.contains(element)) return directLabel.textContent.trim().replace(/\s+/g, " ");
      }
      return "";
    };
    const fields = [...document.querySelectorAll("input:not([type=hidden]):not(#interfaceVivaInput), select, textarea:not(#interfaceVivaInput)")]
      .filter((element) => !element.closest("#interfaceVivaDrawer"))
      .slice(0, 100)
      .map((element) => ({
        nome: element.getAttribute("name") || "",
        id: element.id || "",
        rotulo: labelFor(element),
        tipo: element.getAttribute("type") || element.tagName.toLowerCase(),
        obrigatorio: element.required,
      }))
      .filter((field) => field.nome || field.rotulo);
    const actions = [...document.querySelectorAll("button, a[href]")]
      .filter((element) => !element.closest("#interfaceVivaDrawer") && element.id !== "interfaceVivaToggle")
      .slice(0, 120)
      .map((element) => ({
        texto: (element.textContent || element.value || element.getAttribute("aria-label") || element.title || "").trim().replace(/\s+/g, " ").slice(0, 180),
        tipo: element.tagName.toLowerCase(),
        href: element.getAttribute("href") || "",
      }))
      .filter((action) => action.texto);
    let whatsapp = null;
    const whatsappContext = document.getElementById("whatsapp-context-data");
    if (whatsappContext) {
      try { whatsapp = JSON.parse(whatsappContext.textContent || "null"); } catch (_) { whatsapp = null; }
    }
    return { rota: window.location.pathname, titulo: document.querySelector("h1, h2")?.textContent?.trim() || document.title, campos: fields, acoes: actions, whatsapp };
  }
  async function poll(taskId) {
    status.textContent = "Analisando o contexto oficial…";
    for (let attempt = 0; attempt < 75; attempt += 1) {
      const response = await fetch(`/cognicao/assistente/tarefas/${taskId}/`, { headers: { Accept: "application/json" } }); const data = await response.json();
      if (["CONCLUIDA", "FALHOU", "CANCELADA"].includes(data.estado)) { if (data.resultado?.texto) message(data.resultado.texto, "mheibos", data.resultado.comandos || []); status.textContent = data.erro || ""; return; }
      await new Promise((resolve) => setTimeout(resolve, 800));
    }
    status.textContent = "A análise excedeu o tempo de resposta esperado.";
  }
  form?.addEventListener("submit", async (event) => { event.preventDefault(); const text = input.value.trim(); if (!text) return; message(text, "user"); input.value = ""; input.disabled = true; try { const response = await fetch("/cognicao/assistente/mensagens/", { method: "POST", headers: { "Content-Type": "application/json", "X-CSRFToken": csrf }, body: JSON.stringify({ texto: text, conversa_id: conversationId || null, interface_context: interfaceContext() }) }); const data = await response.json(); if (!response.ok) throw new Error(data.erro || "Não foi possível enviar a mensagem."); conversationId = String(data.conversa_id); await poll(data.tarefa_id); } catch (error) { status.textContent = error.message; } finally { input.disabled = false; input.focus(); } });
  input?.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" || event.shiftKey || event.isComposing) return;
    event.preventDefault();
    form?.requestSubmit();
  });
  const query = new URLSearchParams(window.location.search); const initialFocus = query.get("iv_focus"); const initialFill = query.get("iv_fill"); if (initialFill) { try { const values = JSON.parse(initialFill); setTimeout(() => { Object.entries(values).forEach(([name, value]) => { const element = document.querySelector(`[name="${CSS.escape(name)}"]`); if (!element) return; element.value = value; element.dispatchEvent(new Event("input", { bubbles: true })); element.dispatchEvent(new Event("change", { bubbles: true })); }); }, 60); } catch (_) {} } if (initialFocus) { const element = document.querySelector(`[name="${CSS.escape(initialFocus)}"]`); if (element) { element.scrollIntoView({ block: "center" }); element.classList.add("interface-viva-highlight"); element.focus(); setTimeout(() => element.classList.remove("interface-viva-highlight"), 3500); } }
  function prepare(text) { if (input) { input.value = text || ""; input.focus(); } open(); }
  window.InterfaceViva = { open, executar, prepare };
  const pedidoId = document.body?.dataset.pedidoId || "";
  registrarAtividade("tela_aberta", "Tela", "", { rota: window.location.pathname, titulo: document.title });
  if (pedidoId) registrarAtividade("pedido_aberto", "Pedido", pedidoId, { rota: window.location.pathname, titulo: document.title });
  setTimeout(pollAlertasIA, 1200);
  setInterval(pollAlertasIA, 15000);
})();
