# Validação visual IMP-012 — 10/08/2026

**Estado:** `PASS_WITH_GAP`  
**Ambiente:** servidor local Django, SQLite temporário, usuário administrativo de validação.  
**Rotas:** `/dashboard/` e `/dashboard/analytics/`.

## Resultado observado

- Login real abriu o novo Dashboard oficial individual.
- O Dashboard exibiu Centro de comando, Missões, tarefas, Pendências, métricas operacionais e simulações recentes.
- Analytics exibiu relatório do período, registro de evidências, análise, simulação e comparação determinística.
- O Dashboard passou a exibir análises recentes de forma compacta, com estado, confiança e quantidade de evidências.
- A origem `Pedido/Processo oficial` ficou visível nas métricas.
- A mensagem de que fatos não são interpretação automática ficou visível.
- A rota financeira compatível permaneceu separada do Dashboard oficial.
- Em viewport 1280×720, `document.documentElement.scrollWidth == clientWidth == 1280`; não houve overflow horizontal.

## Gap restante

Esta validação cobre a execução e a composição visual principal em uma resolução. A matriz oficial de cinco resoluções/escalas e a interação completa com dados operacionais reais permanecem como lacunas documentadas do estado `COMPLETED_WITH_GAPS`.
