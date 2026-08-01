# Relatório Atual de Funcionalidades do Mheibos Gestor

## 1. Visão Geral

O Mheibos Gestor é um sistema de gestão empresarial voltado para uma operação de design, gráfica e produção personalizada.

Atualmente, o programa centraliza:

- atendimento;
- vendas;
- clientes;
- pedidos;
- artes;
- produção;
- entrega;
- pagamentos;
- controle financeiro;
- relatórios;
- usuários;
- configurações da empresa;
- coleta de conversas para aprendizado.

O núcleo do sistema funciona em Django, enquanto o Electron oferece versões em formato de aplicativo desktop.

---

## 2. Login e Identificação dos Operadores

O programa possui autenticação própria para operadores.

Cada operador pode ter:

- nome;
- foto;
- senha;
- e-mail;
- telefone;
- cargo;
- categoria de usuário;
- papel de acesso;
- canal de atendimento padrão;
- observações;
- situação ativa ou inativa.

Os papéis existentes são:

- Administrador geral;
- Administrador;
- Usuário;
- Usuário temporário.

O programa também possui:

- criação do primeiro administrador;
- logout;
- troca de senha;
- recuperação de senha por chave;
- login específico para o Mheibos Vendas;
- login específico para o Mheibos Produção;
- autenticação usada pelo launcher desktop.

As permissões afetam ações como:

- cancelar pedidos;
- gerenciar usuários;
- criar ou excluir categorias;
- acessar o CRM;
- visualizar o financeiro geral;
- excluir produtos.

---

## 3. Cadastro e Gestão de Clientes

O CRM permite cadastrar clientes com:

- nome;
- e-mail;
- telefone principal;
- telefone secundário;
- CPF ou CNPJ;
- endereço;
- observações;
- status do cadastro.

O sistema diferencia:

- cliente cadastrado;
- cliente ainda não cadastrado.

Os clientes podem ser pesquisados por nome, telefone e situação cadastral.

Cada cliente também fica relacionado aos seus respectivos pedidos.

---

## 4. Catálogo de Produtos e Serviços

O programa mantém um catálogo dos produtos e serviços vendidos pela empresa.

Cada produto pode ter:

- nome;
- categoria de serviço;
- categoria comercial;
- unidade de medida;
- preço padrão de venda;
- custo estimado;
- prazo de entrega em dias úteis;
- situação ativa ou inativa;
- informação de origem no sistema legado.

As categorias comerciais existentes incluem:

- painéis;
- bolsas;
- gráfica rápida;
- comunicação visual;
- outros.

As unidades disponíveis incluem:

- unidade;
- metro;
- metro quadrado;
- folha;
- serviço.

O usuário pode:

- cadastrar produtos;
- editar produtos;
- excluir produtos;
- organizar produtos por categoria;
- definir preço e custo;
- ativar ou desativar itens.

---

## 5. Categorias de Serviço e Prazos

Os produtos podem ser agrupados em categorias de serviço.

Cada categoria possui:

- nome;
- situação ativa;
- ordem de exibição;
- alerta de prazo;
- quantidade de dias úteis para o alerta;
- regra especial para pedidos do mesmo dia após as 14h.

Essas categorias são utilizadas para calcular quando um pedido deve aparecer na assistência de envio e nos alertas de prazo.

---

## 6. Criação e Gestão de Pedidos

O pedido é uma das entidades centrais do programa.

Ele registra:

- cliente;
- designer responsável;
- tema;
- descrição;
- data do pedido;
- data de entrega;
- hora da entrega;
- observações;
- caminho do arquivo do Corel;
- valor total;
- valor pago;
- desconto ou ajuste;
- forma de pagamento;
- prioridade;
- status;
- origem;
- canal de atendimento;
- usuário que cadastrou;
- responsável pela geração do PDF.

As origens reconhecidas são:

- balcão;
- Mheibos Vendas;
- WhatsApp;
- inteligência artificial;
- sistema legado;
- outras origens.

Os canais de atendimento são:

- presencial;
- online;
- indicação;
- outro.

---

## 7. Etapas do Pedido

O programa organiza o pedido em um fluxo completo de trabalho:

1. Em atendimento;
2. Aguardando arte;
3. Arte em preparo;
4. Aguardando aprovação;
5. Liberado para produção;
6. Em produção;
7. Pronto para entrega;
8. Entregue;
9. Cancelado.

Esses estados permitem separar os pedidos entre:

- atendimento;
- assistência de arte;
- produção;
- entrega;
- conclusão;
- cancelamento.

O sistema também registra um histórico das alterações de status, contendo:

- status anterior;
- novo status;
- observação;
- usuário responsável;
- data da alteração.

---

## 8. Prioridade dos Pedidos

Cada pedido pode receber uma prioridade:

- baixa;
- normal;
- alta;
- urgente.

A prioridade é utilizada junto com a data de entrega para organizar o trabalho e os alertas.

---

## 9. Itens Dentro dos Pedidos

Um pedido pode conter vários produtos ou serviços.

Cada item registra:

- produto relacionado;
- categoria de serviço;
- nome;
- descrição;
- quantidade;
- preço unitário;
- custo unitário estimado;
- ordem de exibição.

O programa calcula automaticamente:

- subtotal de cada item;
- custo total estimado;
- composição do valor do pedido.

---

## 10. Cadastro e Armazenamento das Artes

O sistema permite anexar várias artes a um pedido.

Cada arte possui:

- arquivo de imagem;
- nome original;
- tamanho do arquivo;
- ordem;
- data de criação;
- relacionamento com o pedido.

Os arquivos são armazenados em pastas próprias de cada pedido.

O pedido também pode guardar o caminho do arquivo editável do CorelDRAW.

---

## 11. Fluxo de Atendimento

Existe uma área própria para os pedidos que ainda estão em atendimento.

Por meio dela, o operador pode acompanhar pedidos antes da produção, especialmente os que estão:

- em atendimento;
- aguardando arte;
- com arte em preparo;
- aguardando aprovação.

---

## 12. Fluxo de Produção

Há uma aplicação separada para a equipe de produção.

Ela trabalha principalmente com pedidos:

- liberados para produção;
- em produção;
- prontos.

A produção pode:

- visualizar os pedidos liberados;
- consultar detalhes;
- mudar o andamento;
- rejeitar um pedido recebido na produção;
- devolver o pedido para correção;
- acessar configurações próprias.

O sistema também possui login e interface específicos para o Mheibos Produção.

---

## 13. Fluxo de Entrega

Existe uma área específica para os pedidos prontos para entrega.

Nela, o programa separa os pedidos com status “Pronto”, permitindo acompanhar o que está aguardando retirada, envio ou finalização.

Após a entrega, o pedido pode ser marcado como entregue.

---

## 14. Assistência de Envio e Alertas de Prazo

O programa possui uma assistência automática que identifica pedidos que precisam de atenção.

O cálculo considera:

- status do pedido;
- categoria do produto;
- data de entrega;
- quantidade de dias úteis restantes;
- limite de alerta da categoria;
- regra para pedidos do mesmo dia;
- horário atual.

A assistência pode informar:

- aguardando arte;
- pedido dentro da assistência;
- quantidade de dias úteis até entrar no alerta;
- pedido fora da assistência;
- pedido sem categoria definida.

Quando o envio ou tratamento já foi realizado, o operador pode marcar o pedido como enviado.

O programa também oferece uma API de notificações da assistência.

---

## 15. Ordem de Serviço

O programa gera uma ordem de serviço própria para cada pedido.

Essa ordem pode incluir:

- dados da empresa;
- dados do cliente;
- número do pedido;
- produtos e quantidades;
- valores;
- forma de pagamento;
- valor pago;
- saldo;
- observações;
- datas;
- responsável;
- informações de produção.

O layout da ordem de serviço pode ser configurado como:

- A5 duplicada em uma folha A4;
- A4 inteira.

Também é possível configurar:

- cor das linhas;
- cor dos textos;
- cor das legendas;
- campos exibidos;
- cabeçalho;
- dados empresariais;
- logo.

Há ainda uma versão preparada para cópia e impressão.

---

## 16. Ações em Massa nos Pedidos

A listagem de pedidos possui uma operação própria para ações em massa.

Isso permite aplicar alterações a vários pedidos selecionados sem precisar abrir cada um individualmente.

---

## 17. Pagamentos dos Pedidos

Cada pedido pode possuir um ou vários pagamentos.

O pagamento registra:

- valor;
- forma de pagamento;
- data;
- status;
- observações;
- usuário responsável.

As formas de pagamento incluem:

- PIX;
- dinheiro;
- cartão;
- cheque;
- transferência;
- outro;
- não informado.

Os estados do pagamento são:

- pendente;
- confirmado;
- cancelado;
- estornado.

O programa calcula automaticamente:

- total pago;
- saldo em aberto;
- comparação entre pagamentos atuais e valores importados do sistema legado.

---

## 18. Gestão Financeira

O sistema possui um módulo financeiro integrado aos pedidos e pagamentos.

Ele controla:

- receitas;
- despesas;
- categorias financeiras;
- contas financeiras;
- lançamentos;
- datas de competência;
- vencimentos;
- datas de pagamento;
- situação dos lançamentos;
- observações.

Os lançamentos podem ter os estados:

- previsto;
- realizado;
- cancelado.

As categorias financeiras podem ser agrupadas em:

- vendas;
- serviços;
- custos fixos;
- custos variáveis;
- impostos;
- retiradas;
- outros.

Um lançamento pode estar relacionado diretamente a:

- um pedido;
- um pagamento de pedido;
- uma conta financeira.

---

## 19. Dashboard Financeiro

O programa possui um painel financeiro com consolidação das movimentações.

Esse painel trabalha com informações como:

- receitas;
- despesas;
- resultados;
- lançamentos realizados;
- lançamentos previstos;
- categorias financeiras;
- períodos mensais e anuais;
- desempenho por operador;
- metas de vendas.

O financeiro está conectado aos pagamentos realizados dentro dos pedidos.

---

## 20. Metas de Vendas

O programa permite cadastrar metas mensais para cada operador.

Cada meta possui:

- operador;
- ano;
- mês;
- valor esperado.

Isso possibilita acompanhar o desempenho individual de vendas por período.

---

## 21. Mheibos Vendas

Existe uma aplicação específica para vendas, separada da interface geral do Gestor.

Ela possui:

- login próprio;
- dashboard;
- listagem de pedidos de vendas;
- criação de novo pedido;
- configurações;
- relatórios por tipo.

Os pedidos criados no Mheibos Vendas entram no mesmo fluxo central de pedidos e produção.

---

## 22. Relatórios de Vendas

O módulo de vendas possui geração de relatórios por tipo.

A estrutura permite selecionar diferentes relatórios a partir do painel de vendas, relacionando pedidos, operadores, períodos, metas e valores.

---

## 23. Dashboard e Widgets Operacionais

O sistema possui widgets e painéis configuráveis para apresentar dados da operação.

Entre os dados disponíveis estão:

- pedidos por prazo;
- alertas;
- pedidos em assistência;
- pedidos por etapa;
- indicadores financeiros;
- metas;
- acompanhamento de produção.

Há APIs próprias para:

- widget de prazos;
- notificações da assistência;
- preferências visuais.

---

## 24. Preferências de Interface

O programa salva configurações da interface em formato JSON.

Isso permite manter preferências como:

- organização dos widgets;
- exibição de elementos;
- comportamento visual;
- configurações da interface do Gestor.

As preferências são armazenadas e podem ser atualizadas por API.

---

## 25. Configurações da Empresa

O usuário pode cadastrar e alterar os dados institucionais utilizados no sistema e nos documentos:

- nome fantasia;
- razão social;
- CNPJ;
- telefones;
- Instagram;
- e-mail;
- endereço;
- logo;
- observações.

Também há campos específicos para personalização da ordem de serviço.

---

## 26. Aplicativos Desktop

O projeto possui versões desktop separadas:

- Mheibos Gestor;
- Mheibos Produção;
- Mheibos Cliente;
- suíte completa.

O Electron funciona como uma janela de aplicativo para acessar o servidor Django.

O launcher também possui:

- configuração de endereço do servidor;
- login;
- troca de senha;
- recuperação de senha;
- abertura do sistema conforme o tipo de aplicativo.

---

## 27. Operação em Rede Local

O sistema pode ser iniciado como servidor acessível pela rede local.

Com isso, computadores diferentes podem acessar a mesma instalação e o mesmo banco de dados por meio do endereço IP do servidor.

Essa estrutura permite, por exemplo:

- um computador no atendimento;
- outro na produção;
- outro na administração;
- todos usando a mesma base de pedidos.

---

## 28. Licenciamento

O programa possui um sistema próprio de licença.

Há funcionalidades para:

- geração de chaves;
- emissão de licença;
- ativação;
- validação;
- tela de licenciamento;
- controle de integridade relacionado à instalação.

---

## 29. Verificação de Integridade

O repositório contém mecanismos para:

- gerar manifesto de integridade;
- verificar arquivos;
- conferir textos e componentes;
- detectar alterações em partes protegidas da aplicação.

Isso é utilizado junto ao empacotamento e licenciamento.

---

## 30. Importação do Sistema Legado

O programa possui um importador para trazer dados do antigo sistema.

A importação contempla elementos como:

- clientes;
- pedidos;
- descrições;
- valores;
- pagamentos;
- produtos;
- artes;
- identificadores legados.

O sistema mantém campos de referência ao legado para preservar a relação entre os dados importados e os registros novos.

---

## 31. Aprendizado a Partir de Conversas

O programa possui um módulo chamado Mheibos Aprendizado.

Ele recebe e armazena conversas, inicialmente vindas do WhatsApp.

Para cada conversa, registra:

- instância;
- contato;
- telefone;
- nome;
- primeira mensagem;
- última mensagem;
- quantidade total de mensagens;
- quantidade de mensagens do cliente;
- quantidade de mensagens da empresa.

O módulo identifica sinais como:

- possível lead;
- reclamação;
- possível pedido;
- conversa útil para treinamento.

As mensagens registram:

- direção: cliente, empresa ou sistema;
- tipo;
- texto;
- data;
- conteúdo completo do evento.

As conversas podem gerar amostras de treinamento dos tipos:

- conversa;
- lead;
- reclamação;
- pedido.

Cada amostra possui:

- conteúdo estruturado;
- nota de qualidade;
- estado “pronta” ou não;
- relacionamento com a conversa.

O programa também possui:

- webhook para recebimento de mensagens;
- interface de consulta;
- exportação de conversas úteis;
- organização das amostras para treinamento.

---

# Resumo Funcional

Atualmente, o Mheibos Gestor funciona como uma plataforma integrada com seis áreas principais.

## Comercial

- clientes;
- atendimento;
- vendedores;
- metas;
- novos pedidos;
- relatórios.

## Criação

- temas;
- designers;
- anexos de artes;
- arquivos do Corel;
- preparação;
- aprovação.

## Produção

- liberação;
- fila de produção;
- mudança de status;
- rejeição;
- finalização.

## Logística

- prazos;
- assistência de envio;
- alertas;
- pedidos prontos;
- entregas.

## Financeiro

- pagamentos;
- saldo;
- receitas;
- despesas;
- contas;
- categorias;
- dashboards.

## Administração

- usuários;
- permissões;
- empresa;
- catálogo;
- preferências;
- licenciamento;
- importação;
- configuração dos aplicativos.

Em termos práticos, o programa acompanha o pedido desde o primeiro atendimento até o recebimento, criação da arte, produção, pagamento e entrega.
