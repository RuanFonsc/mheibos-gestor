# Estado Canônico da Implementação

**Data da consolidação:** 10/08/2026  
**Repositório oficial:** `C:\Users\Ruan\Documents\Codex\2026-08-01\entre-no-repositorio-mheibos-gestor-do\mheibos-gestor`  
**Branch de trabalho:** `agent/engineering-baseline`  
**Remoto:** `origin/agent/engineering-baseline`  

Este documento é a referência operacional para retomada do desenvolvimento. Outras pastas existentes em `C:\Users\Ruan\Documents\Mheibos Gestor` são snapshots, artefatos de validação ou cópias de trabalho e não devem ser tratadas como raiz do projeto.

## Regra de continuidade

Antes de editar qualquer arquivo:

1. trabalhar somente na raiz indicada acima;
2. executar `git status --short --branch`;
3. ler `AGENTS.md`, `docs/ENG-SERIES-PLAN.md`, `docs/ENG-QUALITY-GATES.md`, RFCs, Inventário e o progresso de implementação;
4. preservar alterações não commitadas;
5. atualizar este documento e `engineering/implementation/IMPLEMENTATION-PROGRESS.md` após cada fatia;
6. não considerar uma capacidade concluída sem testes e Quality Gates registrados.

## Estado Git consolidado

O branch estava alinhado ao remoto, com um commit local à frente no momento desta consolidação. O último commit era:

`77872a1 feat(missoes): recover backend implementation of tasks, chat and notes for IMP-010`

Havia um arquivo não rastreado, produzido como evidência visual do IMP-010:

`engineering/implementation/IMP-010-VISUAL-VALIDATION-INVALID.md`

Esse arquivo não deve ser apagado. Deve ser revisado contra as telas realmente existentes e somente então adicionado ao commit correto.

## Estado dos IMPs

| IMP | Estado canônico | Observação |
|---|---|---|
| IMP-000 | `COMPLETED_WITH_GAPS` | Baseline preservado; lacunas normativas registradas. |
| IMP-001 | `COMPLETED` | Transição auditável de status. |
| IMP-002 | `COMPLETED_WITH_GAPS` | Identidade, sessão e autorização central; lacunas residuais documentadas. |
| IMP-003 | `COMPLETED` | Eventos aditivos, auditoria e idempotência. |
| IMP-004 | `COMPLETED_WITH_GAPS` | Estados comercial, financeiro e entrega separados; exceção de entrega com saldo permanece posterior. |
| IMP-005 | `COMPLETED_WITH_GAPS` | Processo, Fluxo e Etapa piloto; catálogo amplo e evidências formais permanecem posteriores. |
| IMP-006 | `COMPLETED_WITH_GAPS` | Projeções integradas; famílias adicionais ainda usam fallback. |
| IMP-006B | `COMPLETED` | Convergência da interface operacional; Vendas não é superfície oficial. |
| IMP-006C | `COMPLETED_WITH_GAPS` | Preparação de arte e Assistência de Impressão separadas; política temporal completa depende da RFC-0012. |
| IMP-007 | `COMPLETED_WITH_GAPS` | Pendências determinísticas; escalonamento e cadência normativa ainda são lacunas. |
| IMP-007A | `COMPLETED_WITH_GAPS` | Gateway Gemini opcional com fallback; IA desligada não bloqueia o sistema. |
| IMP-008 | `COMPLETED_WITH_GAPS` | Offline e sincronização validados; falta smoke humano do instalador Windows empacotado. |
| IMP-009 / 009A–009M | `COMPLETED` | Arquivos oficiais, criação, vinculação, monitoramento, restauração, transferência e provisório local implementados. |
| IMP-010 | `IN_PROGRESS` | Missões, Teamwork, tarefas, notas e chat contextual. O backend foi recuperado no commit `77872a1`; a validação final da fatia ainda precisa ser confirmada. |
| IMP-011 | `PENDING` | Conhecimento e memória. |
| IMP-012 | `PENDING` | Dashboard, analytics e simulação conforme RFC-0015. |
| IMP-013 | `PENDING` | Governança e segurança da IA; aguarda RFC-0016. |
| IMP-014 | `PENDING` | IA cognitiva final; última fase. |

## Próximo ponto de retomada

O próximo trabalho deve começar pela auditoria e conclusão do **IMP-010**, sem iniciar IMP-011 ou IMP-012 antes de registrar:

- testes do app `apps.missoes` aprovados;
- migrações verificadas;
- validação das rotas e telas de missões;
- revisão do relatório visual não rastreado;
- Quality Gates do IMP-010 atualizados;
- commit atômico da fatia.

Depois disso, seguir para IMP-011. O IMP-012 somente deve começar com a RFC-0015 e seus critérios de analytics/simulação tratados como fonte normativa, não como hipótese.

## Fontes oficiais de continuidade

- `AGENTS.md`
- `docs/ENG-SERIES-PLAN.md`
- `docs/ENG-QUALITY-GATES.md`
- `docs/engineering/ENG-INDEX.md`
- `docs/engineering/ENG-DEPENDENCY-MAP.md`
- `engineering/implementation/IMPLEMENTATION-BACKLOG.md`
- `engineering/implementation/IMPLEMENTATION-PROGRESS.md`
- `engineering/implementation/IMPLEMENTATION-TEST-MATRIX.md`
- `docs/RFC-0010-Missoes-e-Teamwork.md`
- `docs/RFC-0011-Conhecimento-Memoria-e-Aprendizado.md`
- `docs/RFC-0014-Arquivos-e-Integracoes.md`
- `docs/RFC-0015-Dashboard-Analytics-e-Simulacao.md`
- `docs/engineering/ENG-MIGRACAO-CLIENTE-TAURI2-REACT-TYPESCRIPT.md` — diretriz futura; não interrompe os IMPs atuais.

Nenhum agente deve usar os snapshots `imp002`, `imp003`, `implementation-work` ou `work` como destino de implementação. Eles podem ser consultados apenas para investigação histórica, quando necessário.
