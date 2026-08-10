# Backlog Integral de Implementação

| ID | Capacidade | Fontes proprietárias | Dependências | Estado | Risco | Critério de conclusão | Ciclo |
|---|---|---|---|---|---|---|---|
| IMP-000 | Proteção e caracterização do legado | ENG-0006 §3; ENG-0007 | — | COMPLETED_WITH_GAPS | médio | baseline, gates e mapa inicial existentes | 0 |
| IMP-001 | Transição auditável de status do Pedido | RFC-0002, 0006, 0007 | IMP-000 | COMPLETED | médio | caso de uso único, autorização, autoria, histórico e testes | 1 |
| IMP-002 | Identidade, sessão e autorização central | RFC-0005, 0007 | IMP-001 | COMPLETED_WITH_GAPS | alto | identidade estável, senha segura, sessão e ações sensíveis | 2 |
| IMP-003 | Eventos, evidências e auditoria aditiva | RFC-0006 | IMP-002 | COMPLETED | alto | evento versionado, correlação, ator, alvo, mudança e idempotência | 3 |
| IMP-004 | Pedido comercial com estados independentes | RFC-0005, 0013 | IMP-003 | COMPLETED_WITH_GAPS | alto | comercial, financeiro e entrega separados com migração | 4 |
| IMP-005 | Processo, Fluxo e Etapa piloto | RFC-0002, 0005, 0006 | IMP-004 | COMPLETED_WITH_GAPS | alto | fluxo versionado e processo piloto ligado ao Pedido | 5 |
| IMP-006 | Projeções e interface operacional integrada | RFC-0003, 0009 | IMP-005 | COMPLETED_WITH_GAPS | médio | Gestor/Vendas/Produção como visões da mesma realidade | 6 |
| IMP-006B | Convergência da interface operacional | RFC-0003, 0007, 0009; UI Standards | IMP-006 | COMPLETED | alto | Vendas removido da interface oficial; Produção especializada por função/Etapa; navegação do Fluxo do Pedido e matriz visual aprovadas | 6B |
| IMP-006C | Arte como pré-requisito da Produção | RFC-0002, 0005, 0006, 0009; decisão humana de 02/08/2026 | IMP-006B | COMPLETED_WITH_GAPS | alto | Pedido sem arte permanece na preparação e não avança; fila e notificação determinísticas ativas; cadência/escalonamento aguardam RFC-0012 | 6C |
| IMP-007 | Pendências e intervenções determinísticas | RFC-0009, 0012 | IMP-003 | COMPLETED_WITH_GAPS | alto | estrutura determinística concluída; política temporal aguarda RFC-0012 | 7 |
| IMP-007A | Gateway opcional de IA e adaptador Gemini | RFC-0003, 0004, 0006, 0011 | IMP-003, IMP-006 | COMPLETED_WITH_GAPS | alto | sugestão somente leitura funciona com provider real ou fallback sem alterar operação | 7A |
| IMP-008 | Operação offline restrita e sincronização | RFC-0008 | IMP-002, IMP-003 | COMPLETED_WITH_GAPS | crítico | Ciclo técnico completo e smoke HTTP real com duas bases aprovado; resta somente smoke humano do instalador Windows empacotado, ainda ausente do repositório | 8 |
| IMP-009 | Arquivos e integrações oficiais | RFC-0014 | IMP-003, IMP-005 | COMPLETED | alto | IMP-009A–M cobrem vínculo, criação oficial, criação provisória local, transferência, retenção, monitoramento, conclusão, restauração crítica e transferência autorizada | 9 |
| IMP-010 | Missões e Teamwork | RFC-0010 | IMP-002, IMP-005 | COMPLETED_WITH_GAPS | médio | missão persistente sem duplicar Processo/Etapa | 10 |
| IMP-011 | Conhecimento e memória | RFC-0011 | IMP-003, IMP-010 | COMPLETED_WITH_GAPS | alto | conhecimento fora do modelo, proveniência e validação | 11 |
| IMP-012 | Dashboard, analytics e simulação | RFC-0015 | IMP-003, IMP-005, IMP-010, IMP-011 | PENDING | alto | dashboard individual e modular; análises explicáveis/auditáveis; simulações salvas, autorizadas e promovíveis a Missão | 12 |
| IMP-013 | Governança e segurança da IA | RFC-0016 futura | IMP-002, IMP-003, IMP-011 | PENDING | crítico | aguarda RFC-0016 | posterior |
| IMP-014 | IA cognitiva final | RFC-0004, 0011, 0016 futura | IMP-001–013 | PENDING | crítico | funções cognitivas integradas por fronteiras substituíveis | última fase |

Novas RFCs serão adicionadas ao backlog quando oficializadas. A fundação opcional de IMP-007A não antecipa a governança da RFC-0016 nem torna IA obrigatória; ausência de IA não bloqueia IMP-001 a IMP-013. Na IMP-012, Dashboard, métricas, evidências, permissões e simulação determinística devem funcionar com a IA desligada; linguagem natural, análise cognitiva e reorganização inteligente conectam-se somente na fase de IA.
