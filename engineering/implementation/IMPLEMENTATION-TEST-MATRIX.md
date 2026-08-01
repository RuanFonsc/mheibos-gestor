# Matriz de Testes da Implementação

| Capacidade | Cenário principal | Erros | Automatizado | Teste humano | Estado |
|---|---|---|---|---|---|
| Baseline do Pedido | cálculos e caminhos de arte | pedido ainda não salvo | `PedidoDomainBaselineTests` | abrir Pedido existente | PASS |
| Transição de status | operador autorizado altera e gera histórico | operador sem permissão; status repetido | 3 testes do caso de uso e 1 de rota | alterar status no detalhe e confirmar mensagem | PASS |
| Alteração em massa | vários pedidos usam a mesma regra | pedido não autorizado é ignorado | teste de integração com dois pedidos | selecionar pedidos e executar ação | PASS |
| Rejeição da Produção | retorna para Aguardando Arte com motivo | estado inválido ou motivo vazio | teste de integração com autoria e motivo | rejeitar na tela Produção | PASS |
