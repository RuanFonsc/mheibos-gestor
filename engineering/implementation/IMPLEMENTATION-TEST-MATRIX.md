# Matriz de Testes da Implementação

| Capacidade | Cenário principal | Erros | Automatizado | Teste humano | Estado |
|---|---|---|---|---|---|
| Baseline do Pedido | cálculos e caminhos de arte | pedido ainda não salvo | `PedidoDomainBaselineTests` | abrir Pedido existente | PASS |
| Transição de status | operador autorizado altera e gera histórico | operador sem permissão; status repetido | 3 testes do caso de uso e 1 de rota | alterar status no detalhe e confirmar mensagem | PASS |
| Alteração em massa | vários pedidos usam a mesma regra | pedido não autorizado é ignorado | teste de integração com dois pedidos | selecionar pedidos e executar ação | PASS |
| Rejeição da Produção | retorna para Aguardando Arte com motivo | estado inválido ou motivo vazio | teste de integração com autoria e motivo | rejeitar na tela Produção | PASS |
| Credencial do operador | senha nova persistida como hash | senha incorreta; valor legado | criação, validação, recusa e upgrade | criar usuário, trocar senha e entrar novamente | PASS |
| Sessão do operador | login registra identificador técnico | senha incorreta; renomeação | web, launcher, recusa e renomeação | entrar, renomear perfil e navegar | PASS |
| Eventos e auditoria | status, login e criação geram eventos consultáveis | falha reverte; repetição não duplica; usuário comum recusado | imutabilidade, idempotência, rollback, dois canais e autorização | executar ações e abrir `/auditoria/` como admin | PASS |
| Estados independentes do Pedido | comercial, entrega e financeiro coexistem | entrega com saldo é recusada | estados derivados/registrados, evento e backfill legado | abrir Pedido quitado, parcial, pronto, entregue e cancelado | PASS |
| Processo piloto de Produção | entrada instancia fluxo e pronto conclui Etapa | rejeição bloqueia; evento falho reverte; final não reabre | criação, conclusão, bloqueio, retomada, idempotência, imutabilidade e rollback | mover Pedido para produção, rejeitar/retomar e marcar pronto; conferir Processo no detalhe | PASS |
| Projeção operacional integrada | Gestor, Vendas e Produção exibem o mesmo estado oficial | status legado divergente não prevalece | precedência do Processo, fallback legado, fila ativa/prontos e três views | abrir o mesmo Pedido nas três interfaces e comparar estado/fonte | PASS |
| Pendência de bloqueio | rejeição cria obrigação única e retomada encerra | falha de evento reverte Pedido/Processo/Pendência | criação, encerramento, autoria, acesso e rollback | rejeitar Produção, abrir Pendências, retomar e consultar Encerradas | PASS |
| Resumo cognitivo opcional | provider sugere resumo somente leitura | IA desligada, chave ausente, falha, vazio ou auditoria auxiliar indisponível retornam sem bloquear | 6 testes do Gateway e endpoint; conjunto total com 44 testes | comparar fallback desligado e Gemini habilitado com chave nova; confirmar estados inalterados | PASS_WITH_ONLINE_GAP |
| Pedido offline e fila durável | formulário local grava Pedido, sequência, pacote e eventos atomicamente | Estação/código inválido, evento falho, corrupção, autoria desconhecida e mutação global | 14 testes de domínio, integração, autorização, rollback e idempotência | executar com papel `client_offline`, criar Pedido, abrir `/sincronizacao/` e tentar alterar Pedido global/logout | PASS |
