# Matriz de Testes da Implementação

| Capacidade | Cenário principal | Erros | Automatizado | Teste humano | Estado |
|---|---|---|---|---|---|
| Baseline do Pedido | cálculos e caminhos de arte | pedido ainda não salvo | `PedidoDomainBaselineTests` | abrir Pedido existente | PASS |
| Transição de status | operador autorizado altera e gera histórico | operador sem permissão; status repetido | 3 testes do caso de uso e 1 de rota | alterar status no detalhe e confirmar mensagem | PASS |
| Alteração em massa | vários pedidos usam a mesma regra | pedido não autorizado é ignorado | teste de integração com dois pedidos | selecionar pedidos e executar ação | PASS |
| Rejeição da Produção | retorna para Aguardando Arte com motivo | estado inválido ou motivo vazio | teste de integração com autoria e motivo | rejeitar na tela Produção | PASS |
| Credencial do operador | senha nova persistida como hash | senha incorreta; valor legado | criação, validação, recusa e upgrade | criar usuário, trocar senha e entrar novamente | PASS |
| Sessão do operador | login registra identificador técnico | senha incorreta; renomeação | web, launcher, recusa e renomeação | entrar, renomear perfil e navegar | PASS |
