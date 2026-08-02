---
name: mheibos-ui-engineering
description: Use esta skill para criar, redesenhar, revisar ou validar qualquer interface do Mheibos, incluindo templates Django, Electron, dashboards, formulários, tabelas, modais, drawers, componentes, responsividade, overflow, Interface Viva, screenshots e migração para o design system oficial. Aplique-a também a toda correção visual ou comparação com baseline; ela exige inspeção da aplicação real, tokens compartilhados, testes funcionais e evidências visuais antes da conclusão.
---

# Mheibos UI Engineering

Transformar qualidade visual em engenharia reproduzível. Subordinar toda decisão ao `AGENTS.md`, às RFCs e às fontes canônicas indicadas em `references/NORMATIVE-SOURCES.md`.

## Aplicar invariantes

- Manter autoridade de negócio fora da interface.
- Manter a interface normal integralmente utilizável sem IA.
- Permitir influência da IA somente por comandos estruturados, autorizados e reversíveis.
- Usar densidade operacional compacta; não interpretar “moderno” como “grande”.
- Usar tokens oficiais de dimensões, espaçamento, tipografia, cor, raio, elevação e movimento.
- Reutilizar componente compartilhado antes de criar variante.
- Definir quebra, truncamento, expansão ou rolagem para todo texto variável.
- Usar cor de fundo apenas com função semântica ou estrutural.
- Testar estados normal, extremo, vazio, erro, permissão reduzida e IA indisponível quando aplicáveis.
- Não concluir tela sem aplicação real, resoluções oficiais, zoom de 125%, detector de overflow e screenshots.

## Executar o workflow bloqueante

### A. Descobrir

1. Ler `AGENTS.md` e `references/NORMATIVE-SOURCES.md`.
2. Ler integralmente o padrão global e o Visual Quality Gate.
3. Identificar RFC proprietária, permissões, estados, fluxo e processo envolvidos.
4. Abrir a aplicação real e navegar pelo fluxo com usuário representativo.
5. Inventariar componentes, CSS local, duplicações e problemas com evidências.

### B. Registrar contrato visual

Antes de codificar, registrar no relatório da fatia:

- finalidade e usuário da tela;
- ações primária e secundárias;
- hierarquia, grade, largura e expansão;
- componentes reutilizados e variantes necessárias;
- estados obrigatórios e estratégia para conteúdo longo;
- comportamento no viewport mínimo e em 125%;
- intervenções possíveis da IA e confirmações persistentes.

Se faltar token ou componente global, criar a menor definição compartilhada, provar na tela-piloto e somente depois ampliar.

### C. Implementar

- Implementar a menor fatia coerente.
- Usar HTML semântico, acessibilidade mínima e a stack existente.
- Evitar estilos inline, valores mágicos, CSS duplicado e biblioteca nova sem justificativa.
- Não mover regras para template, JavaScript ou CSS.
- Não reconstruir o programa inteiro quando uma fatia-piloto puder validar a direção.

### D. Validar funcionalmente

- Executar testes, lint, type checking e checks oficiais aplicáveis.
- Testar permissões, persistência e estados relevantes.
- Testar com IA desligada e, quando aplicável, Central indisponível.
- Testar conteúdo normal e extremo com `assets/test-data/ui-content-cases.json`.

### E. Validar visualmente

1. Executar `scripts/run_visual_audit.py`.
2. Abrir a tela em navegador real.
3. Capturar 1366x768, 1440x900, 1536x864 e 1920x1080 a 100%, além de 1366x768 a 125%.
4. Executar `scripts/detect_overflow.js` no contexto da página.
5. Capturar estados extremo, vazio, erro e sobreposições aplicáveis.
6. Comparar baselines com `scripts/compare_screenshots.py` quando existirem.
7. Corrigir até todos os gates críticos passarem.

Falha crítica produz `FAIL`; impossibilidade real de validação produz `BLOCKED`, nunca aprovação presumida.

### F. Encerrar

Registrar tela, fontes, componentes, tokens, viewports, estados, screenshots, gates, regressões, variações, limitações e commit. Usar o modelo de relatório do Visual Quality Gate.

## Proibir atalhos visuais

Não usar padding para mascarar hierarquia, cards para todo texto, badges decorativos, fundo colorido sem semântica, fonte menor para esconder overflow, `overflow: hidden` para ocultar defeito, corte sem acesso ao conteúdo, tabela substituída por cards sem razão operacional ou identidade própria por módulo.

Não aprovar por leitura estática, testes de backend isolados ou apenas porque a página renderiza.

## Migrar o Mheibos

Preservar uma aplicação integrada. Descontinuar Vendas como experiência duplicada e migrar suas capacidades para o Gestor. Manter Produção como visão especializada da mesma aplicação, selecionada por função/permissão do usuário ou pelo contexto da Etapa do Pedido. Não duplicar fonte de verdade, regra ou componente.

Tratar a relação entre assistência de envio e assistência de entrega como parte do fluxo/processo, não como duas ilhas de navegação. Usar o detalhe do Pedido como tela-piloto inicial, salvo decisão posterior registrada.

## Manter baselines

- Versionar somente screenshots aprovadas em `assets/baselines/`.
- Armazenar evidências da execução na pasta indicada pelo ciclo.
- Atualizar baseline apenas após mudança intencional aprovada; nunca sobrescrever para fazer o teste passar.
- Comparar geometria e desaparecimento de elementos, sem reprovar automaticamente antialiasing.
