# Mapa de Migracao do Gestor

Este documento consolida a leitura inicial do legado Desktop/PyQt e a base criada para o novo Django/PostgreSQL.

## Decisao Arquitetural

O legado nao deve ser copiado tabela por tabela. Ele deve ser tratado como fonte de dados e regras de negocio. O novo sistema deve nascer orientado por dominios: clientes, pedidos, producao, financeiro, catalogo, atendimento e integracoes.

## Inventario do Legado

| Modulo legado | Papel atual | Destino no Django |
| --- | --- | --- |
| `conexao_db.py` | Conexao PostgreSQL, tabela `pedidos`, fila de atendimento humano | Apps `pedidos`, `clientes`, `legacy_migration`, futuro app `atendimento` |
| `gestor_pedidos.py` | CRUD de pedidos, calculo de total, PDF, artes Base64 | Apps `pedidos`, `catalogo`, servico de PDF, `ArtePedido` com arquivo |
| `modulo_custos.py` | Leitura da planilha de custos, classificacao de produto, custo/lucro | App `catalogo`, futuro servico de custo e margem |
| `dashboard_grafica.py` | Faturamento, ticket medio, vendas por designer/produto/status | Apps `financeiro`, `pedidos`, relatorios agregados |
| `assistencia_envio.py` e `assistencia_envio_page.py` | Fluxo de envio e marcacao de pedido pronto | Futuro app `producao` ou `atendimento` |
| `solicitacao_atendimento.py` | Fila de atendimento humano | Futuro app `atendimento` com SLA e origem WhatsApp |
| `fant_ia_bot.py` e `bot/` | WhatsApp/Evolution, FAQ, status de pedido, transferencia humana | Futuro app `integracoes` + `atendimento` |
| `assistente_sistema.py` | IA interna com ferramentas para consultar banco, PDFs e arquivos | Futuro app `assistente` depois do core estabilizado |
| `fant_print.py` | Fila/configuracao de impressao | Futuro app `impressao` |
| `relatorios.py` | Listagem/abertura de PDFs | Futuro app `documentos` |

## Regras de Negocio Identificadas

| Regra | Onde aparece | Como fica no Django |
| --- | --- | --- |
| Total do pedido = soma de quantidade x preco unitario + ajuste | `gestor_pedidos.py` | `PedidoItem` guarda quantidade/preco; `Pedido.valor_total` pode ser recalculado por service |
| Status sao texto livre no legado | `conexao_db.py`, `gestor_pedidos.py` | `StatusPedido` com choices |
| Pedido cancelado nao entra em faturamento | `dashboard_grafica.py` | Relatorios excluem `StatusPedido.CANCELADO` |
| `valor_pago` e forma de pagamento ficam no pedido | `pedidos` legado | `PagamentoPedido` normalizado |
| Receita vem dos pedidos | Dashboard e planilha Solides | `LancamentoFinanceiro` gerado a partir de pagamento/saldo |
| Despesas sao categorias mensais na planilha | Planilha Solides | `CategoriaFinanceira` + `LancamentoFinanceiro` granular |
| Artes ficam como Base64 no campo `arte` | `gestor_pedidos.py` | `ArtePedido.arquivo` em `MEDIA_ROOT` |
| Custo/lucro e margem dependem da classificacao do produto | `modulo_custos.py` | `ProdutoServico.custo_estimado`, depois service de margem |

## Schema Django Criado

### CRM

- `Cliente`: nome, email, telefones, observacoes.

### Catalogo

- `ProdutoServico`: produto/servico vendavel, categoria, unidade, preco padrao e custo estimado.

### Pedidos

- `Pedido`: cliente, designer, tema, datas tipadas, status, origem, total e campos legados preservados.
- `PedidoItem`: itens normalizados com quantidade, preco unitario, custo estimado e descricao.
- `ArtePedido`: arquivo de imagem em pasta, com metadados e hash do Base64 migrado.
- `PagamentoPedido`: pagamentos confirmados/pendentes/cancelados.
- `HistoricoStatusPedido`: trilha de mudanca de status.

### Financeiro

- `CategoriaFinanceira`: receitas/despesas por categoria e grupo.
- `ContaFinanceira`: caixa/conta/banco.
- `LancamentoFinanceiro`: receita/despesa com competencia, vencimento, pagamento, status e vinculo opcional ao pedido.

## Fluxo Pedido Para Financeiro

1. Pedido importado/criado.
2. Pagamento confirmado cria receita realizada.
3. Saldo em aberto cria receita prevista.
4. Cancelamento do pedido cancela os lancamentos vinculados.
5. Relatorio de fluxo de caixa usa `data_pagamento`.
6. Relatorio gerencial pode usar `data_competencia`.

## Artes Fora do Banco

No novo sistema, o banco guarda apenas caminho e metadados. O arquivo fisico fica em:

```text
media/pedidos/{pedido_id}/artes/
```

O importador `importar_legado` converte o Base64 antigo em arquivo e registra o hash em `ArtePedido.legado_base64_hash`.

## Equivalencia com a Planilha Solides

| Aba da planilha | Fonte no Django |
| --- | --- |
| Receitas | `LancamentoFinanceiro` tipo `RECEITA`, agrupado por mes/ano/categoria |
| Despesas | `LancamentoFinanceiro` tipo `DESPESA`, agrupado por mes/ano/categoria |
| Fluxo de Caixa | Receitas realizadas menos despesas realizadas por `data_pagamento` |
| Dashboard | Receita anual, despesa anual, lucro liquido e margem |

## Prioridades de Execucao

1. Ajustar `.env` e conectar o novo banco PostgreSQL.
2. Rodar migrations e criar categorias financeiras iniciais.
3. Importar pequena amostra do legado com `--limit`.
4. Conferir pedidos, clientes, itens, pagamentos e artes no admin.
5. Comparar totais do novo financeiro com dashboard legado.
6. Construir telas HTMX de pedidos e clientes.
7. Criar telas financeiras: lancamentos, categorias, fluxo mensal e dashboard.
8. Migrar custos/catalogo com base na planilha `tabela_custos_grafica_e_paineis_v3.xlsx`.
9. Integrar atendimento humano/WhatsApp depois que pedidos e clientes estiverem estaveis.
10. Migrar PDFs, impressao e assistente interno por ultimo.

## Riscos e Cuidados

- O campo `descricao` legado mistura itens, observacoes e texto livre; o importador tenta parsear, mas alguns pedidos vao precisar revisao.
- `valor_pago` legado nao tem data real de pagamento; a primeira importacao usa `data_pedido` como melhor aproximacao.
- Status e formas de pagamento tinham variacoes textuais; foram normalizados para choices.
- A senha local do PostgreSQL precisa ser ajustada antes de aplicar migrations.
- A copia de arquivos dentro de `PDF PEDIDOS/GESTOR NOVO` parece duplicar codigo e deve ser ignorada na migracao.

## Modulos Fora do Foco Inicial

- WhatsApp/Evolution: integrar depois via webhook Django, mantendo `Atendimento` como centro.
- IA interna: so deve entrar depois que consultas e permissoes do novo banco estiverem maduras.
- Impressao: virar fila web ou tarefa assíncrona.
- PDFs: gerar a partir de templates HTML/PDF no servidor, nao reaproveitar FPDF como nucleo.
