(() => {
  const page = document.querySelector("[data-whatsapp-screen]");
  if (!page) return;

  const rows = [...document.querySelectorAll("[data-chat-row]")];
  const filterButtons = [...document.querySelectorAll("[data-whatsapp-filter]")];
  const labelButtons = [...document.querySelectorAll("[data-label-filter]")];
  let currentFilter = "all";
  let currentLabel = "";

  const matchesRow = (row) => {
    const keyByFilter = {
      unread: "filterUnread",
      favorite: "filterFavorite",
      group: "filterGroup",
      lead: "filterLead",
      pedido: "filterPedido",
      atencao: "filterAtencao",
    };
    const rowMatchesFilter = currentFilter === "all" || row.dataset[keyByFilter[currentFilter]] === "true";
    const labels = (row.dataset.filterLabels || "").split("|").filter(Boolean);
    const rowMatchesLabel = !currentLabel || labels.includes(currentLabel);
    return rowMatchesFilter && rowMatchesLabel;
  };

  const applyFilters = () => {
    rows.forEach((row) => { row.hidden = !matchesRow(row); });
  };

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      currentFilter = button.dataset.whatsappFilter || "all";
      currentLabel = "";
      filterButtons.forEach((item) => item.classList.toggle("is-active", item === button));
      labelButtons.forEach((item) => item.classList.remove("is-active"));
      applyFilters();
    });
  });

  labelButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const label = (button.dataset.labelFilter || "").toLocaleLowerCase();
      currentLabel = currentLabel === label ? "" : label;
      currentFilter = "all";
      filterButtons.forEach((item) => item.classList.toggle("is-active", item.dataset.whatsappFilter === "all"));
      labelButtons.forEach((item) => item.classList.toggle("is-active", item === button && currentLabel !== ""));
      applyFilters();
    });
  });

  document.querySelector("[data-whatsapp-refresh]")?.addEventListener("click", () => window.location.reload());

  document.querySelectorAll("[data-whatsapp-ai]").forEach((button) => {
    button.addEventListener("click", () => {
      window.InterfaceViva?.prepare?.("Analise a conversa do WhatsApp selecionada usando o contexto oficial abaixo. Identifique o estado do atendimento, os sinais de lead, pedido ou atenção e indique o próximo passo seguro.");
    });
  });

  const labelForm = document.querySelector("[data-whatsapp-label-form]");
  const labelStatus = document.querySelector("[data-whatsapp-label-status]");
  labelForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const input = labelForm.querySelector("[name='nome']");
    const nome = input?.value.trim();
    if (!nome) return;
    const button = labelForm.querySelector("button[type='submit']");
    if (button) button.disabled = true;
    try {
      const response = await fetch(page.dataset.labelEndpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector('meta[name="csrf-token"]')?.content || "",
          Accept: "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({ conversa_id: page.dataset.selectedConversation, nome }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.erro || "Não foi possível criar a etiqueta.");
      if (labelStatus) labelStatus.textContent = `Etiqueta “${data.etiqueta.nome}” adicionada.`;
      input.value = "";
      window.setTimeout(() => window.location.reload(), 350);
    } catch (error) {
      if (labelStatus) labelStatus.textContent = error.message;
      if (button) button.disabled = false;
    }
  });

  const messages = document.querySelector("[data-whatsapp-messages]");
  if (messages) messages.scrollTop = messages.scrollHeight;
  applyFilters();
})();