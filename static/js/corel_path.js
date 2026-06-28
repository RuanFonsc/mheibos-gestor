(function () {
  const desktop = window.mheibosArquivos;

  function nomeArquivo(caminho) {
    return String(caminho || "").split(/[\\/]/).filter(Boolean).pop() || caminho || "";
  }

  function isRede(caminho) {
    return String(caminho || "").replaceAll("/", "\\").startsWith("\\\\");
  }

  function setFeedback(root, texto, erro) {
    const alvo = root.querySelector("[data-corel-feedback]");
    if (!alvo) return;
    alvo.textContent = texto || "";
    alvo.classList.toggle("text-[#ff4b4b]", Boolean(erro));
    alvo.classList.toggle("text-[#8892b0]", !erro);
  }

  function setValor(root, valor) {
    const input = root.querySelector("[data-corel-input]");
    const valueEl = root.querySelector("[data-corel-value]");
    const emptyEl = root.querySelector("[data-corel-empty]");
    if (!input) return;
    input.value = valor || "";
    if (valueEl) {
      valueEl.textContent = valor ? `${nomeArquivo(valor)} - ${valor}` : "";
      valueEl.classList.toggle("hidden", !valor);
    }
    emptyEl?.classList.toggle("hidden", Boolean(valor));
    setFeedback(
      root,
      valor
        ? "Caminho do servidor salvo como referencia. O arquivo nao sera enviado para o banco."
        : "Use um arquivo dentro da pasta compartilhada do servidor.",
      false
    );
  }

  async function aplicarResultado(root, resultado) {
    if (!resultado?.path) return;
    if (!resultado.isNetwork || !isRede(resultado.path)) {
      setFeedback(root, resultado.message || "Use um caminho de rede do servidor.", true);
      return;
    }
    setValor(root, resultado.path);
    if (resultado.message) setFeedback(root, resultado.message, false);
  }

  document.querySelectorAll("[data-corel-field]").forEach((root) => {
    const input = root.querySelector("[data-corel-input]");
    const drop = root.querySelector("[data-corel-drop]");
    const select = root.querySelector("[data-corel-select]");
    const clear = root.querySelector("[data-corel-clear]");

    setValor(root, input?.value || "");

    select?.addEventListener("click", async () => {
      if (!desktop?.selecionarCorel) {
        setFeedback(root, "Abra pelo Mheibos Desktop para carregar o caminho real do arquivo.", true);
        return;
      }
      await aplicarResultado(root, await desktop.selecionarCorel());
    });

    clear?.addEventListener("click", () => setValor(root, ""));

    ["dragenter", "dragover"].forEach((eventName) => {
      drop?.addEventListener(eventName, (event) => {
        event.preventDefault();
        drop.classList.add("border-[#00e5ff]", "bg-[#222842]");
      });
    });

    ["dragleave", "drop"].forEach((eventName) => {
      drop?.addEventListener(eventName, (event) => {
        event.preventDefault();
        drop.classList.remove("border-[#00e5ff]", "bg-[#222842]");
      });
    });

    drop?.addEventListener("drop", async (event) => {
      const arquivo = event.dataTransfer?.files?.[0];
      const caminho = arquivo && desktop?.caminhoArquivo ? desktop.caminhoArquivo(arquivo) : arquivo?.path;
      if (!caminho || !desktop?.normalizarCorel) {
        setFeedback(root, "Abra pelo Mheibos Desktop para arrastar e capturar o caminho real do arquivo.", true);
        return;
      }
      await aplicarResultado(root, await desktop.normalizarCorel(caminho));
    });
  });

  document.querySelectorAll("[data-corel-path]").forEach((link) => {
    link.addEventListener("click", async (event) => {
      event.preventDefault();
      const caminho = link.dataset.corelPath || "";
      if (!caminho) return;
      if (desktop?.abrirCorel) {
        const resultado = await desktop.abrirCorel(caminho);
        if (resultado && !resultado.isNetwork) alert(resultado.message || "Caminho de rede invalido.");
        return;
      }
      window.open(`file:///${caminho.replaceAll("\\", "/")}`);
    });
  });
})();
