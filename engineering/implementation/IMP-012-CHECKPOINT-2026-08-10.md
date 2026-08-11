# Checkpoint IMP-012 — Dashboard, Analytics e Simulação

**Data:** 10/08/2026  
**Estado:** `COMPLETED_WITH_GAPS`  
**Fontes:** RFC-0015, RFC-0010, RFC-0011, RFC-0016 Draft 0.1  
**Escopo desta fatia:** domínio determinístico, dashboard individual, evidências, análises e simulações salvas.

## Entregue

- Novo app `apps.analytics` com evidências tipadas, confiança, fonte, referência e dados estruturados.
- Análises determinísticas preservam pergunta, resumo, confiança e evidências usadas.
- Simulações exigem premissas e resultados internos não vazios, têm validade dinâmica e podem ser promovidas explicitamente a Missão.
- Promoção é transacional, auditada e nunca executa automaticamente o cenário.
- `/dashboard/` passou a ser o Dashboard oficial individual, com Missões, tarefas, Pendências e simulações em fila de atenção.
- `/financeiro/dashboard/` preserva a consulta financeira legada como superfície compatível, sem definir o centro do produto.
- `/dashboard/analytics/` oferece curadoria visível para evidências, análises e simulações.
- Todas as rotas funcionam sem modelo de IA.
- O Dashboard projeta fatos operacionais atuais (pedidos ativos, arte, produção, entrega, urgência e prazo próximo) com fonte explícita, sem inferência.
- Relatório do período calcula fatos de Pedido com fonte explícita e declara que nenhuma interpretação automática foi feita.
- Comparação entre dois períodos mostra somente variações factuais de pedidos, urgências e valor total, sem inferência silenciosa.
- Análises nascem como rascunho e só são validadas por autoridade humana autorizada, sempre preservando as evidências usadas.
- O Dashboard oficial exibe análises recentes em cartão compacto, com confiança, estado e quantidade de evidências, sem ampliar o cartão de pedido.

## Quality Gates desta fatia

| Gate | Resultado | Evidência |
|---|---|---|
| Fonte normativa | `PASS_WITH_GAP` | RFC-0015 aplicada; catálogo de autonomia da RFC-0016 permanece futuro. |
| Arquitetura | `PASS` | Dashboard, Analytics e Simulação são contratos próprios; financeiro fica compatível. |
| Domínio | `PASS_WITH_GAP` | evidências, confiança, análise, validade e promoção implementadas; analytics avançado ainda posterior. |
| Auditoria | `PASS` | criação de evidência, análise e simulação, além da promoção, são eventos transacionais. |
| Segurança | `PASS` | identidade ativa obrigatória; promoção exige autor ou administrador; sem autoridade implícita da IA. |
| Migração | `PASS` | `0001_initial` do app Analytics; `makemigrations --check` sem alterações. |
| Testes | `PASS` | 12 testes do Analytics e 9 do Aprendizado aprovados; baseline completo de 205 testes, Django check e migrações aprovados. |
| Tipagem | `PASS` | Ruff e mypy passaram no escopo Analytics + Aprendizado (8 arquivos), com cache temporário fora do repositório. |
| Interface | `PASS_WITH_GAP` | rotas e templates renderizam; matriz visual multi-resolução e integração completa de widgets ainda pendentes. |
| IA desligada | `PASS` | nenhum serviço, formulário ou rota depende de modelo externo. |

## Lacunas explicitamente preservadas

- árvore de causas, anomalias e planos de ação como propostas explícitas dependem da camada de IA futura e não são simulados pelo modo determinístico;
- matriz visual multi-resolução e acabamento da interface de comparação;
- validação visual real nas resoluções oficiais;
- integração posterior com a governança da RFC-0016 sem habilitar autonomia por padrão.

Essas lacunas não bloqueiam o uso atual do Dashboard nem o funcionamento com IA desligada. O IMP-012 está apto a ceder a sequência ao IMP-013, sem transformar hipóteses da RFC-0015 em fatos implementados.
