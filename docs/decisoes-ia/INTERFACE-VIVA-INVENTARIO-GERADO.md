# Inventário gerado da Interface Viva

Este inventário foi derivado das rotas, formulários, modelos e ferramentas presentes no código do Mheibos Gestor. Ele é a fonte operacional para nomes de telas, campos e comandos que a IA pode propor.

## Regras

- A IA nunca manipula o DOM livremente e não recebe acesso ao ORM.
- Navegação, foco e destaque são comandos temporários e reversíveis.
- Preenchimento é apenas proposta até confirmação humana.
- Salvar, alterar status ou qualquer operação persistente passa pelo caso de uso determinístico e auditoria.
- Rótulos devem vir do formulário oficial; a IA não deve inventar sinônimos quando houver nome canônico.

## Telas inicialmente inventariadas

| Identificador | Rota | Capacidade |
|---|---|---|
| `novo_pedido` | `/pedidos/novo/` | criação assistida e preenchimento proposto |
| `pedidos` | `/pedidos/` | pesquisa e abertura |
| `pedido_detalhe` | `/pedidos/{pedido_id}/` | consulta e ações confirmáveis |
| `dashboard` | `/dashboard/` | navegação |
| `assistencia_impressao` | `/assistencia-envio/` | navegação |
| `entregas` | `/pedidos/entrega/` | navegação |
| `clientes` | `/clientes/` | navegação |
| `produtos` | `/produtos/` | navegação |

## Novo Pedido

O nome canônico do campo é `data_entrega`, com rótulo **Data de Entrega**, tipo data e obrigatoriedade definida pelo `PedidoCreateForm`. `Previsão de Entrega` não é o rótulo oficial desse formulário.

## Comandos

`navegar`, `destacar_campo`, `destacar_acao`, `preencher_campos`, `abrir_pedido` e `pesquisar_pedidos` são comandos de interface registrados. O cliente deve recusar comandos fora desse catálogo.