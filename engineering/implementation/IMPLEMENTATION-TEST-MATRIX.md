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
