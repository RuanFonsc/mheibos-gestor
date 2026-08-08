# Diagnostico de arquitetura e fluxos atuais

Data do levantamento: 2026-07-31.

Objetivo: entregar ao ChatGPT Web um mapa honesto do Mheibos Gestor atual, separando o que ja existe no codigo do que ainda e intencao de arquitetura.

## 1. Mapa da arquitetura atual

### 1.1 Visao geral

O projeto e um sistema Django 5 com templates server-side, arquivos estaticos simples e launchers Electron. O banco principal pode rodar em PostgreSQL ou SQLite por variavel de ambiente, mas a direcao do projeto e PostgreSQL. O Electron nao substitui o backend: ele abre o Django em uma janela desktop.

Camadas reais:

- `config`: settings, URLs globais, middleware de licenca, integridade, primeiro admin e login de operador.
- `apps.clientes`: cadastro e CRM simples de clientes.
- `apps.pedidos`: pedidos, itens, artes, pagamentos, ordem de servico, atendimento, entrega e a maior parte das transicoes operacionais.
- `apps.catalogo`: produtos/servicos, categorias, operadores, permissoes, preferencias de UI, licenca, configuracoes, assistencia de envio, producao e APIs para widgets/launcher.
- `apps.financeiro`: categorias, contas, lancamentos, metas, dashboard, relatorios PDF e sincronizacao financeira a partir de pedido/pagamento.
- `apps.vendas`: interface simplificada para vendedores criarem pedidos que entram em atendimento.
- `apps.aprendizado`: coleta de conversas WhatsApp/Evolution para treinamento; nao operacionaliza pedido automaticamente.
- `apps.legacy_migration`: importacao e normalizacao do legado.
- `electron` e `tools`: launchers, empacotamento e utilitarios.

Fontes principais:

- Apps instalados em `config/settings.py`.
- Rotas globais em `config/urls.py`.
- Modelos de dominio em `apps/*/models.py`.
- Fluxo legado e direcao de migracao em `docs/MAPA_MIGRACAO.md`.

### 1.2 Modulos

#### Clientes

Responsabilidade atual:

- Manter `Cliente`.
- Separar cliente cadastrado de cliente criado automaticamente a partir de pedido.
- Exibir lista, busca, painel do cliente e pedidos vinculados.

Modelo:

- `Cliente`: nome, email, telefones, CPF/CNPJ, endereco, observacoes, `status_cadastro`, timestamps.
- `StatusCadastroCliente`: `CADASTRADO`, `NAO_CADASTRADO`.

Ponto importante: um pedido pode criar cliente com `NAO_CADASTRADO`; a tela de clientes so lista `CADASTRADO`.

#### Pedidos

Responsabilidade atual:

- CRUD operacional de pedido.
- Itens normalizados.
- Upload de artes como arquivo.
- Pagamentos vinculados ao pedido.
- Alteracao de status por tela de detalhe, edicao, acoes em massa, assistencia, producao e rejeicao.
- Ordem de servico HTML.

Modelos:

- `Pedido`: cliente, tema, datas, status, origem, canal, valores, prioridade, usuario de cadastro, caminho Corel, campos legados.
- `PedidoItem`: produto/categoria, nome, descricao, quantidade, preco e custo estimado.
- `ArtePedido`: arquivo e metadados.
- `PagamentoPedido`: valor, forma, data, status.
- `HistoricoStatusPedido`: existe, mas hoje so aparece de forma consistente na rejeicao da producao.

#### Catalogo

Responsabilidade atual:

- Produtos e categorias de servico.
- Regras de prazo/alerta por categoria.
- Operadores, papeis, perfil da empresa, configuracao da OS.
- Login de operador, login de producao, login de vendas.
- Assistencia de envio e tela de producao.
- Preferencias de UI e APIs de widget.
- Licenciamento e integridade.

Modelos relevantes:

- `CategoriaServico`: nome, ativo, ordem, flags de alerta e dias uteis.
- `ProdutoServico`: nome, categoria de servico, categoria legada, unidade, preco, custo, prazo.
- `OperadorGestor`: nome, senha em texto de aplicacao, papel, categoria, canal padrao, permissoes por properties.
- `PerfilEmpresa`: dados da empresa e configuracoes visuais da ordem de servico.
- `PreferenciaUI`: JSON global ou por usuario.

#### Financeiro

Responsabilidade atual:

- Dashboard financeiro/vendas.
- Categorias, contas e lancamentos.
- Metas de venda por operador.
- Relatorios PDF.
- Sincronizar receitas previstas/realizadas a partir de pedidos.

Modelos:

- `CategoriaFinanceira`, `ContaFinanceira`, `LancamentoFinanceiro`, `MetaVendasUsuario`.
- Choices: `TipoLancamento`, `StatusLancamento`, `GrupoFinanceiro`.

Servico central:

- `sincronizar_financeiro_pedido(pedido)`.

#### Vendas

Responsabilidade atual:

- Interface reduzida para vendedor.
- Cria `Pedido` com origem `VENDAS` e status inicial `EM_ATENDIMENTO`.
- Mantem dashboard pessoal e relatorios do vendedor.

Ponto importante: a criacao de pedido em `apps.vendas.services.criar_pedido_vendas` duplica parte da criacao em `apps.pedidos.views._criar_pedido`.

#### Aprendizado

Responsabilidade atual:

- Receber webhook Evolution.
- Registrar conversa, mensagem e sinais simples: lead, reclamacao, pedido.
- Gerar amostras JSON para treinamento.

Nao faz hoje:

- Nao cria cliente.
- Nao cria orcamento.
- Nao abre atendimento humano.
- Nao altera pedido.

### 1.3 Telas e rotas reais

Entradas principais:

- `/`: home.
- `/login/`, `/producao/login/`, `/vendas/login/`, `/sair/`, `/primeiro-admin/`, `/licenca/`.
- `/dashboard/`: dashboard financeiro.
- `/clientes/`: CRM de clientes.
- `/pedidos/`: lista/funil de pedidos.
- `/pedidos/atendimento/`: fila de atendimento.
- `/pedidos/novo/`: novo pedido no Gestor.
- `/pedidos/<id>/`: detalhe.
- `/pedidos/<id>/editar/`: edicao.
- `/pedidos/<id>/ordem-servico/`: OS.
- `/pedidos/entrega/`: fila de entrega.
- `/assistencia-envio/`: assistencia de envio.
- `/producao/`: fila de producao.
- `/produtos/`: catalogo.
- `/configuracoes/`: operadores, empresa, OS, alertas e banco.
- `/vendas/`: dashboard do vendedor.
- `/vendas/pedido/novo/`: novo pedido no Mheibos Vendas.
- `/aprendizado/`: painel de aprendizado.
- `/webhook` e `/aprendizado/webhook/evolution/`: webhook Evolution.
- APIs: preferencias, widget de prazos, notificacao de assistencia e launcher.

### 1.4 Banco de dados

Entidades centrais e relacoes:

- `Cliente` 1:N `Pedido`.
- `Pedido` 1:N `PedidoItem`.
- `Pedido` 1:N `ArtePedido`.
- `Pedido` 1:N `PagamentoPedido`.
- `Pedido` 1:N `HistoricoStatusPedido`.
- `Pedido` 1:N `LancamentoFinanceiro`.
- `PagamentoPedido` 1:1 opcional `LancamentoFinanceiro`.
- `ProdutoServico` 1:N `PedidoItem`.
- `CategoriaServico` 1:N `ProdutoServico` e 1:N opcional `PedidoItem`.
- `OperadorGestor` 1:N `MetaVendasUsuario`.
- `ConversaAprendizado` 1:N `MensagemAprendizado` e 1:N `AmostraTreinamento`.

Artes:

- Arquivos fisicos em `MEDIA_ROOT`.
- Banco guarda caminho/metadados em `ArtePedido`.
- Campo `caminho_arquivo_corel` guarda caminho de rede para arquivo Corel.

### 1.5 Dependencias

Python/Django:

- Django 5.
- `psycopg` para PostgreSQL.
- `python-decouple` para configuracao.
- `openpyxl` para importacao/relatorios de planilha.
- `reportlab` aparece nos relatorios PDF.

Frontend:

- Templates Django.
- JavaScript estatico em `static/js`.
- Sem SPA, sem API REST central.

Desktop/empacotamento:

- Electron e electron-builder.
- PyInstaller/spec para backend empacotado.

### 1.6 Comunicacao entre componentes

O padrao predominante e chamada direta entre apps, nao eventos.

Fluxos de comunicacao:

- Views Django recebem request e manipulam models diretamente.
- `pedidos.views` chama `financeiro.services.sincronizar_financeiro_pedido`.
- `vendas.services` cria `Pedido`, `PedidoItem`, `PagamentoPedido` e chama financeiro.
- `catalogo.assistencia` consulta pedidos/itens/produtos e tambem pode preencher categoria/produto em item.
- `catalogo.views` altera status de pedido em assistencia e producao.
- `financeiro.views` consulta `Pedido`, `PedidoItem`, `LancamentoFinanceiro` e `OperadorGestor`.
- `aprendizado.services` registra webhook e exporta JSON local em `exports/aprendizado`.
- Middleware bloqueia acesso por licenca, primeiro admin e login de operador.

Nao ha atualmente:

- Barramento de eventos.
- Service layer unificado de pedido.
- Maquina formal de estado.
- Auditoria central de transicoes.
- Workflow engine.

## 2. Mapa dos fluxos reais

### 2.1 Criacao do cliente

Fluxos existentes:

1. Tela `/clientes/` salva cliente via `ClienteForm`.
2. O nome e convertido para maiusculo.
3. `status_cadastro` vira `CADASTRADO`.
4. Se o cliente tem pedidos, aparece no painel do cliente.

Criacao indireta:

1. Criacao de pedido no Gestor usa `Cliente.objects.get_or_create(nome=...)`.
2. Cliente criado por pedido entra como `NAO_CADASTRADO`.
3. Criacao no Mheibos Vendas tambem usa `get_or_create`; pode preencher telefone/CPF/endereco se estiverem vazios.

Fragilidade:

- Dedupe e feito por nome exato em maiusculo.
- Telefone/CPF nao sao chave de identificacao.
- Cliente criado automaticamente pode ficar invisivel no CRM principal por `NAO_CADASTRADO`.

### 2.2 Orcamento

Fluxo real:

- Nao existe entidade `Orcamento`.
- O pedido faz o papel de orcamento/pedido ao mesmo tempo.
- Valores sao calculados por itens informados manualmente no form.
- Produto pode ser associado por nome exato ao catalogo.

Fragilidade:

- Nao existe fase formal de proposta, validade, versao, desconto aprovado ou aceite.
- O fluxo pode ir direto para arte/producao/pronto sem evidencias de fechamento.

### 2.3 Fechamento

Fluxo real:

- Nao existe entidade ou evento de fechamento.
- O fechamento e inferido pela criacao do `Pedido`, pela existencia de pagamento ou pelo status.
- No Gestor, o pedido ja nasce em `AGUARDANDO_ARTE`, `ARTE_EM_PREPARO` ou `PRONTO`.
- No Vendas, nasce em `EM_ATENDIMENTO`.

Fragilidade:

- Pedido sem pagamento pode entrar em producao.
- Pedido pode ser marcado pronto imediatamente.
- Nao ha validacao central de dados minimos para fechar.

### 2.4 Criacao do pedido

Gestor:

1. `/pedidos/novo/`.
2. `PedidoCreateForm` valida campos basicos.
3. `_criar_pedido` cria/obtem cliente.
4. Laco fixo de ate 5 itens monta `PedidoItem`.
5. Calcula `valor_total = subtotal + desconto_ajuste`.
6. Define status inicial:
   - `PRONTO` se `marcar_pronto`.
   - `AGUARDANDO_ARTE` se `aguardar_arte`.
   - `ARTE_EM_PREPARO` caso contrario.
7. Cria pagamento informado, se houver.
8. Salva artes.
9. Chama sincronizacao financeira.

Vendas:

1. `/vendas/pedido/novo/`.
2. `VendasPedidoForm`.
3. `criar_pedido_vendas`.
4. Cria pedido com origem `VENDAS` e status `EM_ATENDIMENTO`.
5. Cria itens e pagamento.
6. Chama sincronizacao financeira.

Fragilidade:

- Duas implementacoes de criacao com regras parecidas.
- Laco fixo de 5 itens esta embutido nas views/services.
- `desconto_ajuste` somado ao subtotal, entao valor negativo vira desconto e positivo vira acrescimo; a semantica depende do usuario.

### 2.5 Desenvolvimento da arte

Fluxo real:

- Status existentes: `AGUARDANDO_ARTE`, `ARTE_EM_PREPARO`, `AGUARDANDO_APROVACAO`.
- Campo `designer` existe, mas o uso operacional predominante tambem passa por `usuario_cadastro`.
- Artes podem ser anexadas no pedido como imagens.
- `caminho_arquivo_corel` guarda caminho de rede validado para UNC.

Fragilidade:

- Nao existe tarefa de arte, responsavel formal, inicio/fim, checklist ou versao.
- Nao existe diferenca entre arte recebida do cliente, arte criada, revisao e arquivo final.

### 2.6 Aprovacao

Fluxo real:

- Existe status `AGUARDANDO_APROVACAO`.
- Nao ha entidade de aprovacao, evidencia, aprovador, data, canal ou arquivo aprovado.
- Qualquer tela que permita trocar status pode tirar o pedido dessa fase.

Fragilidade:

- Aprovacao pode ser ignorada.
- Nao ha prova do aceite do cliente.
- Nao ha impedimento para producao sem arte/aprovacao.

### 2.7 Producao

Fluxo real:

- `assistencia-envio` mostra pedidos em status de assistencia conforme categoria e prazo.
- `assistencia_marcar_enviado` muda pedido para `EM_PRODUCAO`.
- `/producao/` lista pedidos `EM_PRODUCAO` ou `PRONTO`, agrupados por categoria.
- Acoes em massa podem marcar pronto, entregar, cancelar ou enviar para producao.
- Rejeicao da producao volta de `EM_PRODUCAO` para `AGUARDANDO_ARTE` e cria `HistoricoStatusPedido`.

Fragilidade:

- Status `LIBERADO_PRODUCAO` existe, mas o fluxo usa principalmente `EM_PRODUCAO`.
- Nao ha controle de inicio/fim por etapa produtiva.
- Producao pode receber pedido sem aprovacao formal.
- Historico e excecao, nao regra geral.

### 2.8 Entrega

Fluxo real:

- `STATUS_ENTREGA = [PRONTO]`.
- `/pedidos/entrega/` lista prontos.
- Acao em massa pode marcar `ENTREGUE`.
- Dashboard/lista contam entregues.

Fragilidade:

- Nao ha protocolo de entrega, responsavel, data real, comprovante, retirado por, endereco/rota ou pendencia.
- `ENTREGUE` pode ser marcado por acao em massa sem validacao financeira ou evidencia.

### 2.9 Financeiro

Fluxo real:

- Pagamento confirmado cria lancamento `RECEITA` `REALIZADO`.
- Saldo aberto cria lancamento `RECEITA` `PREVISTO`.
- Pedido cancelado cancela lancamentos vinculados.
- Dashboards usam mistura de `LancamentoFinanceiro` e fallback em `Pedido.valor_total`.
- Despesas podem ser lancadas no CRM financeiro.
- Metas sao por operador/mes.

Fragilidade:

- A sincronizacao e chamada manualmente por pontos especificos.
- Se um caminho alterar pedido/pagamento sem chamar o service, o financeiro fica incoerente.
- Nao ha reconciliacao explicita nem evento de pagamento.
- `valor_pago_legado` convive com `PagamentoPedido`, causando duplicidade conceitual.

### 2.10 Pos-venda

Fluxo real:

- Nao ha modulo/tela/entidade formal de pos-venda.
- Reclamacoes podem ser detectadas no `aprendizado`, mas nao geram tarefa operacional.

Fragilidade:

- Sem follow-up, pesquisa, reincidencia, garantia, retrabalho, ocorrencia ou historico de relacionamento.

## 3. Maquinas de estado existentes

### 3.1 Pedido

Estados existentes:

- `EM_ATENDIMENTO`
- `AGUARDANDO_ARTE`
- `ARTE_EM_PREPARO`
- `AGUARDANDO_APROVACAO`
- `LIBERADO_PRODUCAO`
- `EM_PRODUCAO`
- `PRONTO`
- `ENTREGUE`
- `CANCELADO`

Agrupamentos auxiliares:

- Pre-producao: `EM_ATENDIMENTO`, `AGUARDANDO_ARTE`, `ARTE_EM_PREPARO`, `AGUARDANDO_APROVACAO`.
- Assistencia: `AGUARDANDO_ARTE`, `ARTE_EM_PREPARO`, `AGUARDANDO_APROVACAO`.
- Funil gestor: assistencia + `LIBERADO_PRODUCAO`, `EM_PRODUCAO`.
- Entrega: `PRONTO`.

Quem altera:

- `apps.pedidos.views._criar_pedido`: define status inicial no Gestor.
- `apps.vendas.services.criar_pedido_vendas`: define `EM_ATENDIMENTO`.
- `apps.pedidos.views._atualizar_pedido`: salva qualquer status escolhido no form de edicao.
- `apps.pedidos.views.pedido_update_status`: salva qualquer status valido no form.
- `apps.pedidos.views.pedido_bulk_action`: muda em massa para `PRONTO`, `EM_PRODUCAO`, `ENTREGUE`, `CANCELADO`.
- `apps.catalogo.views.assistencia_marcar_enviado`: muda para `EM_PRODUCAO`.
- `apps.pedidos.views.pedido_rejeitar_producao`: muda `EM_PRODUCAO` para `AGUARDANDO_ARTE`.
- Importadores/migrations podem criar estados normalizados a partir do legado.

Validacoes executadas:

- Choices do Django impedem status fora da lista quando forms/models passam pelo caminho normal.
- Permissao para cancelar: apenas admin.
- Permissao para editar: admin ou operador dono; temporario nao edita.
- Excecao: mudancas vindas de producao/assistencia/entrega podem contornar parte da permissao individual.
- Rejeicao exige motivo e status atual `EM_PRODUCAO`.

Onde pode ficar incoerente:

- Mudanca de status sem `HistoricoStatusPedido`.
- Pedido em producao sem aprovacao.
- Pedido pronto/entregue sem pagamento suficiente.
- Pedido com status de assistencia sem categoria em itens.
- Pedido com `valor_total` diferente da soma atual dos itens se alterado fora dos services/views atuais.
- `LIBERADO_PRODUCAO` existe, mas pode nao ser usado de forma coerente.
- `designer` e `usuario_cadastro` podem representar responsabilidades diferentes, mas telas misturam filtros por ambos.

Onde etapa pode ser ignorada:

- Criacao no Gestor pode nascer `PRONTO`.
- Edicao pode trocar para qualquer status.
- Acoes em massa podem enviar para producao/pronto/entregue.
- Assistencia pode enviar direto para producao.
- Aprovacao nao e obrigatoria.

### 3.2 Pagamento

Estados:

- `PENDENTE`
- `CONFIRMADO`
- `CANCELADO`
- `ESTORNADO`

Quem altera:

- Criacao/edicao de pedido sincroniza o pagamento informado.
- Vendas cria pagamento confirmado se valor pago > 0.
- Admin Django pode alterar diretamente.

Validacoes:

- Poucas validacoes de negocio alem de campos obrigatorios e choices.

Incoerencias possiveis:

- `valor_pago_legado` pode ser maior que soma de pagamentos.
- Lancamento financeiro pode ficar defasado se pagamento for alterado sem sincronizacao.
- Nao ha controle de estorno propagando para pedido de forma clara.

### 3.3 Financeiro

Estados:

- `PREVISTO`
- `REALIZADO`
- `CANCELADO`

Quem altera:

- `sincronizar_financeiro_pedido`.
- Dashboard financeiro ao criar/excluir lancamentos manuais.
- Admin Django.

Incoerencias possiveis:

- Lancamentos previstos podem ser recriados sem preservar historico.
- Cancelamento do pedido cancela tudo vinculado, mas descancelamento depende de nova sincronizacao.
- Dashboard usa fallback por `Pedido.valor_total`, mascarando falha de lancamento.

### 3.4 Cliente

Estados:

- `CADASTRADO`
- `NAO_CADASTRADO`

Quem altera:

- Tela de clientes marca como `CADASTRADO`.
- Criacao automatica pelo pedido tende a `NAO_CADASTRADO`.
- Admin/importador.

Incoerencias possiveis:

- Duplicidade por nome.
- Cliente real com pedidos fica fora da tela principal se nunca for convertido para `CADASTRADO`.

### 3.5 Aprendizado

Estados/flags:

- Conversa: `tem_lead`, `tem_reclamacao`, `tem_sinal_pedido`, `util_para_treinamento`, `revisado`.
- Amostra: `pronta`, `qualidade`, `tipo`.

Quem altera:

- Webhook Evolution e regras simples de texto.

Incoerencias possiveis:

- Sinal de pedido/reclamacao nao gera objeto operacional.
- Exportacao JSON roda como efeito colateral quando conversa vira util.

## 4. Debitos operacionais

### 4.1 Etapas sem protecao

- Orcamento e fechamento nao existem como entidades.
- Aprovacao nao tem evidencia.
- Producao nao exige aprovacao, arte final, pagamento ou checklist.
- Entrega nao exige comprovante.
- Pos-venda nao existe.

### 4.2 Automacoes frageis

- Financeiro depende de chamadas manuais a `sincronizar_financeiro_pedido`.
- Assistencia calcula regras em tempo de tela e pode salvar categorias em itens durante leitura.
- Webhook de aprendizado exporta JSON no meio do processamento.
- Widgets dependem de APIs simples e preferencias JSON.

### 4.3 Responsabilidades misturadas

- `catalogo.views` contem login, catalogo, configuracoes, assistencia, producao e APIs.
- `pedidos.views` contem CRUD, calculo de itens, pagamento, upload, status, OS e acoes em massa.
- `financeiro.views` contem dashboard, CRM financeiro, metas e geracao de PDF.
- Regras de pedido estao repartidas entre `pedidos.views`, `vendas.services`, `catalogo.assistencia` e `financeiro.services`.

### 4.4 Regras alojadas dentro da interface

- Criacao/edicao de pedido calcula total e recria itens dentro de view/helper.
- Status inicial depende de checkboxes do form.
- Acoes em massa codificam transicoes diretamente.
- Configuracoes de alerta sao salvas em POST da tela de configuracoes.
- Relatorios PDF sao montados diretamente em view.

### 4.5 Dados duplicados ou ambiguos

- `valor_pago_legado` versus `PagamentoPedido`.
- `forma_pagamento_legada` versus forma do pagamento.
- `descricao_legada`, `PedidoItem.descricao`, `observacoes` e `tema`.
- `designer` versus `usuario_cadastro`.
- Categoria em `PedidoItem` e categoria derivavel por `ProdutoServico`.
- Cliente por nome pode duplicar pessoa/empresa.

### 4.6 Telas que nao representam corretamente o processo

- Tela de pedidos permite representar fases como status unico, mas nao mostra tarefas/evidencias por etapa.
- Atendimento e pedido aparecem no mesmo modelo, sem diferenciar lead, orcamento e pedido fechado.
- Producao trabalha com status, mas nao com etapas produtivas reais.
- Entrega lista `PRONTO`, mas nao controla entrega real.
- Financeiro mostra indicadores, mas parte do valor pode vir de fallback em pedido, nao de lancamentos.

### 4.7 Ausencia de eventos, evidencias ou auditoria

- `HistoricoStatusPedido` existe, mas nao e usado em toda transicao.
- Nao ha tabela de eventos de dominio.
- Nao ha log de quem criou/alterou pagamento, item, arte, aprovacao ou entrega em todos os caminhos.
- Nao ha anexos/evidencias para aprovacao, entrega, retrabalho ou pos-venda.
- Nao ha guardas formais de transicao.

## 5. Inventario de reaproveitamento

### 5.1 Pode permanecer

- Modelos basicos de `Cliente`, `Pedido`, `PedidoItem`, `ArtePedido`, `PagamentoPedido`.
- `LancamentoFinanceiro`, `CategoriaFinanceira`, `ContaFinanceira`, `MetaVendasUsuario`.
- `ProdutoServico` e `CategoriaServico`.
- Armazenamento de arte em arquivo.
- Configuracao de empresa/OS em `PerfilEmpresa`.
- Login por operador como solucao local temporaria.
- Importadores como ponte do legado.
- Electron como launcher leve.

### 5.2 Pode ser refatorado

- Criacao de pedido: mover regras para um service unico usado por Gestor e Vendas.
- Sincronizacao financeira: trocar chamada manual por evento/transacao de dominio ou service obrigatorio.
- Assistencia/producao: extrair para app ou service de workflow/producao.
- Status de pedido: centralizar transicoes em uma maquina de estado com guardas.
- Relatorios PDF: mover montagem para services/templates.
- Permissoes de operador: formalizar sem depender apenas de properties e nome salvo em sessao/preferencia.
- Preferencias UI: separar preferencias globais, por app e por usuario.
- Dashboard financeiro: remover fallback que mascara lancamentos ausentes depois da reconciliacao.
- `HistoricoStatusPedido`: transformar em auditoria obrigatoria de status.

### 5.3 Deve ser substituido

- Status unico como representacao completa do processo.
- Orcamento inexistente embutido em pedido.
- Aprovacao como mero status sem evidencia.
- Entrega como mero status sem protocolo.
- Pos-venda ausente.
- Senha de operador salva em campo simples.
- Regras de negocio espalhadas em views.
- Dedupe de cliente por nome.
- Laco fixo de 5 itens por formulario.

### 5.4 Nao tem equivalente na nova arquitetura desejada

Estes conceitos ainda nao existem como entidades de primeira classe:

- `Orcamento` / proposta / versao de proposta.
- `Fechamento` ou aceite comercial.
- `WorkflowPedido` ou `EtapaPedido`.
- `EventoPedido` / event log.
- `AprovacaoArte` com evidencia.
- `ArquivoArte` com tipo, versao e status.
- `TarefaArte` ou fila de design.
- `TarefaProducao` ou ordem de producao por setor.
- `EntregaPedido` com comprovante e responsavel.
- `OcorrenciaPosVenda`.
- `Atendimento` humano integrado ao WhatsApp.
- `Lead` vindo de IA/WhatsApp.
- `ReconciliacaoFinanceira`.
- `PoliticaTransicaoStatus`.

## 6. Recomposicao sugerida para a grande implementacao

Direcao tecnica recomendada:

1. Criar um service unico de `PedidoWorkflowService` antes de criar novas telas.
2. Criar tabela/evento de auditoria obrigatoria para toda transicao relevante.
3. Separar comercial em `Lead/Atendimento -> Orcamento -> Pedido`.
4. Separar arte em tarefa/evidencia: briefing, arquivo, revisao, aprovacao.
5. Separar producao em fila/tarefa: liberado, em producao, pronto, rejeitado.
6. Separar entrega: pronto para retirada, entregue, comprovante, pendencia.
7. Integrar financeiro por eventos do pedido e pagamento, com reconciliacao.
8. Deixar `StatusPedido` como resumo operacional, nao como unica verdade do processo.

Primeiro alvo de alto retorno:

- Centralizar todas as transicoes de status em um unico service com:
  - status atual;
  - status alvo;
  - ator;
  - origem da acao;
  - motivo;
  - guardas;
  - efeitos colaterais;
  - registro obrigatorio de historico/evento.

Isso reduz incoerencia imediatamente sem exigir redesenhar todas as telas de uma vez.

