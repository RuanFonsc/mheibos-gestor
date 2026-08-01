# MHEIBOS INTELLIGENT OPERATING SYSTEM

# RFC-0006 — Eventos, Evidências e Auditoria

**Status:** Draft para aprovação  
**Versão:** 0.1  
**Data:** 30/07/2026  
**Dependências:** RFC-0000, RFC-0001, RFC-0002, RFC-0003, RFC-0005  
**Fonte normativa:** Inventário Oficial de Decisões Arquiteturais — INV-024 a INV-029

---

## 1. Resumo

Esta RFC define como o Mheibos registra acontecimentos relevantes, associa evidências, preserva o histórico e oferece rastreabilidade sobre a operação.

Toda alteração operacional, comercial, financeira, administrativa ou de segurança relevante deverá produzir um **Evento**. O Evento registrará o que aconteceu, quem ou qual componente originou a ação, quando ocorreu, em qual estação e contexto, quais entidades foram afetadas e, quando aplicável, quais eram os valores anteriores e posteriores.

A **Evidência** representa o elemento verificável que sustenta uma ocorrência, decisão, conclusão ou mudança de estado. Ela poderá ser produzida por uma ação humana, pelo próprio sistema, por uma integração, por um arquivo, por uma leitura técnica ou por outra fonte autorizada.

A **Auditoria** será formada por registros imutáveis derivados dos eventos relevantes. Ela deverá permitir responder, com precisão, quem fez o quê, quando, onde, em qual contexto, com qual autorização e qual foi o resultado.

Apagar algo na interface não significará destruir sua existência histórica. Exclusões, cancelamentos, remoções e substituições serão registrados como novos eventos, preservando o conteúdo anterior e a autoria da ação.

O registro de eventos não poderá tornar o Mheibos lento, atrasar perceptivelmente a interação do usuário, provocar perda de sincronização ou criar subnotificação. Consequências secundárias poderão ser processadas de forma desacoplada, desde que a operação principal permaneça consistente e rastreável.

---

## 2. Objetivo

Esta RFC responde às seguintes perguntas:

- o que é um Evento no Mheibos;
- quais acontecimentos devem gerar eventos;
- quais informações mínimas todo evento relevante deve preservar;
- o que é uma Evidência e como ela se relaciona com eventos e estados;
- como o histórico de auditoria será mantido de forma imutável;
- como registrar valores anteriores e posteriores;
- como exclusões e cancelamentos serão representados sem destruição silenciosa;
- como distinguir eventos produzidos online e offline;
- como eventos locais serão incorporados à Central;
- como mudanças de regras, perfis, permissões e políticas serão auditadas;
- como processar consequências secundárias sem prejudicar a resposta ao usuário;
- como evitar perda, duplicação, reordenação indevida e subnotificação;
- quais fronteiras separam evento de negócio, auditoria, evidência, notificação e log técnico.

---

## 3. Decisões fundamentais

A arquitetura de Eventos, Evidências e Auditoria adota as seguintes decisões:

1. Toda alteração relevante gera um Evento.
2. Eventos devem possuir identidade técnica estável e não reutilizável.
3. O Evento registra fato ocorrido; ele não é apenas uma mensagem textual de log.
4. O estado atual e o histórico são representações diferentes da realidade.
5. Eventos relevantes deverão registrar autoria, momento, origem, contexto e mudança realizada.
6. Quando houver alteração de dados, o sistema deverá preservar os valores anteriores e posteriores necessários à auditoria.
7. Evidências deverão possuir origem, vínculo e integridade identificáveis.
8. O histórico de auditoria será imutável para usuários comuns e administradores.
9. Exclusões serão registradas como eventos de remoção, cancelamento, desativação ou substituição, não como destruição silenciosa.
10. Eventos deverão indicar se foram produzidos online ou offline.
11. Mudanças de regras, permissões, perfis, exceções e políticas também serão auditadas.
12. A interação principal deverá ser percebida como imediata.
13. Consequências secundárias poderão ser processadas de forma desacoplada.
14. Falhas secundárias não poderão apagar o evento original nem tornar a operação invisível.
15. Notificações, projeções e integrações deverão ser derivadas dos eventos sem substituir a fonte oficial do estado.

---

## 4. Escopo

### 4.1 Incluído

Esta RFC especifica:

- conceito e estrutura de Evento;
- classificação de eventos;
- autoria humana e origem técnica;
- contexto online e offline;
- correlação e causalidade;
- valores anteriores e posteriores;
- Evidências e sua proveniência;
- registros imutáveis de auditoria;
- exclusão lógica e eventos de apagamento;
- processamento síncrono e assíncrono;
- entrega, repetição e idempotência conceitual;
- ordenação e tempo;
- falhas, reprocessamento e fila de pendências;
- projeções de estado e histórico;
- consulta e explicação da auditoria;
- retenção conceitual e integridade;
- observabilidade específica do pipeline de eventos.

### 4.2 Fora do escopo

Não são definidos aqui:

- banco de dados definitivo;
- tecnologia concreta de barramento ou fila;
- formato físico final das tabelas;
- esquema SQL;
- protocolo completo de sincronização offline;
- autenticação e permissões detalhadas;
- lista definitiva de ações sensíveis;
- regras completas de cada domínio;
- interface visual do histórico;
- política legal definitiva de retenção e anonimização;
- formato dos logs técnicos gerais;
- métricas específicas de negócio;
- implementação de notificações e escalonamentos;
- escolha de ferramentas de monitoramento.

Esses temas deverão respeitar os contratos e invariantes definidos nesta RFC.

---

## 5. Conceitos fundamentais

### 5.1 Evento

Um Evento é o registro estruturado de que algo relevante ocorreu no Mheibos.

Exemplos:

- pedido criado;
- item adicionado;
- prazo alterado;
- processo iniciado;
- etapa concluída;
- pagamento registrado;
- arquivo associado;
- pedido cancelado;
- permissão concedida;
- política alterada;
- bloqueio de edição adquirido;
- sincronização concluída;
- integração externa falhou.

Um evento descreve um fato ocorrido. Ele não representa apenas uma intenção futura nem uma sugestão da IA ainda não aprovada.

### 5.2 Evidência

Uma Evidência é um elemento verificável associado a um fato, estado, decisão ou conclusão.

Exemplos:

- confirmação explícita de um usuário;
- arquivo de arte recebido;
- comprovante registrado;
- resposta recebida por integração;
- resultado de uma leitura técnica;
- documento gerado;
- registro de conclusão de uma etapa;
- dado de origem externa identificado;
- fotografia, assinatura, hash ou referência de arquivo;
- conjunto de eventos que comprova uma sequência operacional.

A evidência não precisa ser um arquivo. Ela pode ser um registro estruturado, uma referência, uma confirmação ou outro dado cuja origem seja identificável.

### 5.3 Registro de auditoria

O Registro de Auditoria é a representação imutável, consultável e orientada à responsabilização de um evento relevante.

Ele deverá tornar compreensível:

- o que aconteceu;
- quem realizou ou originou;
- quando aconteceu;
- em qual estação e sessão;
- qual entidade foi afetada;
- qual era a situação anterior;
- qual passou a ser a situação posterior;
- qual justificativa ou autorização foi utilizada;
- se a operação ocorreu online ou offline;
- qual foi o resultado.

### 5.4 Estado atual

O Estado Atual representa como uma entidade se encontra agora.

Ele poderá ser atualizado ou recalculado como consequência de eventos.

### 5.5 Histórico

O Histórico representa a sequência de acontecimentos que levou ao estado atual.

O histórico relevante não deverá ser reescrito para parecer que uma ação nunca aconteceu.

### 5.6 Comando

Um Comando representa uma solicitação para que algo seja executado.

Exemplo:

> “Alterar o prazo do Pedido #J324 para 18/08.”

O Evento correspondente existe somente depois que a operação for validada e efetivamente aceita:

> “Prazo do Pedido #J324 alterado de 15/08 para 18/08 por Maria.”

Comando e Evento não deverão ser tratados como a mesma coisa.

### 5.7 Notificação

Notificação é a comunicação apresentada a um usuário ou sistema em consequência de um evento ou condição.

Um evento poderá gerar nenhuma, uma ou várias notificações. A ausência de notificação não apaga o evento. A notificação também não substitui o histórico.

### 5.8 Log técnico

Log técnico registra informações de execução, diagnóstico, desempenho e falha de componentes.

Ele não substitui o Evento de negócio nem o Registro de Auditoria.

---

## 6. Modelo conceitual do Evento

Todo Evento relevante deverá possuir estrutura equivalente aos seguintes campos conceituais.

### 6.1 Identidade

- identificador técnico único;
- tipo do evento;
- versão do esquema do evento;
- organização e instalação de origem.

### 6.2 Momento

- data e hora em que o fato ocorreu;
- data e hora em que o evento foi registrado localmente;
- data e hora em que foi recebido pela Central, quando diferente;
- sequência local ou outra informação necessária à ordenação.

### 6.3 Origem

- usuário responsável, quando houver;
- componente técnico responsável, quando não houver ação humana direta;
- estação;
- sessão;
- origem online ou offline;
- canal, módulo, integração ou serviço que produziu o evento.

### 6.4 Alvo

- entidade principal afetada;
- tipo da entidade;
- entidades relacionadas;
- processo, etapa, pedido, cliente, missão ou política associada, quando aplicável.

### 6.5 Mudança

- ação realizada;
- campos ou relações alteradas;
- valores anteriores relevantes;
- valores posteriores relevantes;
- estado anterior e novo estado;
- motivo, quando obrigatório;
- autorização ou reautenticação utilizada, quando aplicável.

### 6.6 Contexto

- correlação com outros eventos;
- comando ou operação que originou o evento;
- evento causador, quando existir;
- lote, transação lógica ou fluxo ao qual pertence;
- versão das regras ou políticas aplicadas;
- metadados necessários à interpretação futura.

### 6.7 Resultado

- concluído;
- rejeitado;
- compensado;
- parcialmente concluído;
- pendente de processamento secundário;
- sincronização pendente;
- falha técnica registrada.

Eventos que representam somente operações aceitas deverão distinguir-se de tentativas rejeitadas. Tentativas sensíveis ou de segurança poderão também gerar eventos próprios de auditoria.

---

## 7. Classificação de eventos

### 7.1 Eventos de domínio

Representam mudanças significativas da realidade operacional ou comercial.

Exemplos:

- `PedidoCriado`;
- `ItemDoPedidoAdicionado`;
- `ProcessoConfirmado`;
- `EtapaConcluida`;
- `EntregaAutorizada`;
- `PagamentoRegistrado`.

### 7.2 Eventos administrativos

Representam mudanças de configuração e governança.

Exemplos:

- `PerfilCriado`;
- `PermissaoAlterada`;
- `PoliticaDeAcaoSensivelModificada`;
- `CriterioDeMetaAtualizado`.

### 7.3 Eventos de segurança

Representam autenticação, reautenticação, bloqueios, tentativas proibidas e alterações de acesso.

Exemplos:

- `LoginRealizado`;
- `LoginRecusado`;
- `AcaoSensivelConfirmada`;
- `PermissaoNegada`;
- `BloqueioDeEdicaoAdquirido`;
- `BloqueioLiberadoAdministrativamente`.

### 7.4 Eventos de sincronização

Representam criação local, envio, recebimento, incorporação, falha e repetição de operações offline.

Exemplos:

- `PedidoLocalCriado`;
- `SincronizacaoIniciada`;
- `EventoLocalIncorporado`;
- `SincronizacaoFalhou`;
- `SincronizacaoConcluida`.

### 7.5 Eventos de integração

Representam trocas relevantes com sistemas externos.

Exemplos:

- `MensagemRecebidaDoWhatsApp`;
- `WebhookProcessado`;
- `ArquivoExternoAssociado`;
- `IntegracaoIndisponivel`.

### 7.6 Eventos técnicos auditáveis

Alguns fatos técnicos possuem impacto operacional e deverão gerar eventos estruturados, além de logs.

Exemplos:

- restauração de backup;
- migração de dados;
- recuperação administrativa de sessão offline;
- alteração manual de relógio detectada;
- reprocessamento excepcional de eventos.

---

## 8. Critérios para geração de eventos

### 8.1 Alterações relevantes

Deverão gerar eventos, no mínimo:

- criação de entidade persistente;
- alteração de dados comerciais;
- alteração de dados financeiros;
- mudança de estado;
- mudança de responsável;
- inclusão, dispensa, reabertura ou conclusão de etapa;
- concessão, retirada ou exceção de permissão;
- alteração de política ou configuração oficial;
- exclusão, cancelamento, arquivamento ou substituição;
- ação sensível;
- operação offline relevante;
- incorporação ou falha de sincronização;
- alteração de vínculo com arquivo ou integração quando tiver impacto operacional.

### 8.2 Consultas comuns

A simples leitura de dados não precisa gerar um evento de domínio.

Consultas poderão ser auditadas quando:

- envolverem informação sensível;
- forem exigidas por política;
- representarem exportação, impressão ou compartilhamento;
- tiverem impacto de segurança;
- fizerem parte de investigação administrativa.

### 8.3 Ações temporárias de interface

Filtros, seleção de aba, destaque visual e reorganização temporária não deverão gerar eventos de negócio, salvo quando forem necessários para continuidade de missão, diagnóstico ou auditoria de intervenção crítica.

### 8.4 Sugestões da IA

Uma sugestão ainda não aceita não altera o estado oficial.

Ela poderá gerar registro cognitivo ou técnico próprio, mas o evento de domínio somente será produzido quando a ação correspondente for autorizada e executada.

---

## 9. Autoria e origem

### 9.1 Ação humana direta

Quando uma pessoa executar a ação, o evento deverá registrar o usuário autenticado.

O nome visível não será suficiente. A referência deverá usar a identidade técnica preservada no RFC-0005.

### 9.2 Ação do sistema

Quando um componente executar automaticamente uma consequência autorizada, o evento deverá registrar:

- componente de origem;
- regra, agendamento ou evento causador;
- usuário relacionado, quando houver;
- ausência de ação humana direta.

### 9.3 Ação mediada pela IA

Quando a IA sugerir e o usuário confirmar uma ação, deverão ser distinguídos:

- a proposta cognitiva;
- o usuário que autorizou;
- o componente determinístico que validou;
- o evento oficial resultante.

A autoria oficial da alteração não poderá ser atribuída apenas ao modelo de linguagem.

### 9.4 Integrações externas

Eventos externos deverão registrar:

- sistema ou canal de origem;
- identificador externo, quando disponível;
- adaptador responsável;
- momento de recebimento;
- usuário ou entidade associada;
- validade e estado de processamento.

### 9.5 Estação e sessão

Eventos originados por Clientes deverão preservar a estação e a sessão que os produziram.

A desativação posterior da estação ou do usuário não poderá apagar esse vínculo histórico.

---

## 10. Tempo e ordenação

### 10.1 Tempos distintos

A arquitetura deverá distinguir, quando necessário:

- momento em que o fato ocorreu;
- momento em que foi registrado na origem;
- momento em que foi recebido pela Central;
- momento em que consequências secundárias foram processadas.

### 10.2 Relógio da estação

O relógio local poderá sofrer desvio. Por isso, eventos offline deverão preservar informações suficientes para ordenação local sem depender exclusivamente da hora de parede.

### 10.3 Sequência local

Cada origem capaz de produzir eventos offline deverá manter uma sequência monotônica local ou mecanismo equivalente.

### 10.4 Ordenação global

A Central deverá estabelecer uma ordem de incorporação sem apagar a ordem local original.

### 10.5 Eventos simultâneos

Eventos diferentes poderão possuir o mesmo horário visível. A identidade, a sequência e a correlação deverão permitir diferenciá-los.

### 10.6 Correção de horário

Ajustes de relógio não deverão reescrever eventos históricos. O sistema poderá registrar a correção e utilizar metadados normalizados para consulta.

---

## 11. Correlação, causalidade e operações compostas

### 11.1 Identificador de correlação

Eventos pertencentes à mesma operação deverão poder compartilhar um identificador de correlação.

Exemplo:

```text
Alteração do valor do pedido
├── PedidoValorAlterado
├── SaldoRecalculado
├── EstadoFinanceiroAlterado
└── PendenciaFinanceiraCriada
```

### 11.2 Evento causador

Uma consequência deverá poder apontar para o evento que a originou.

### 11.3 Operação principal e consequências

O evento principal registra a mudança aceita pelo caso de uso.

Consequências secundárias podem incluir:

- atualização de dashboard;
- geração de notificação;
- atualização de índice de busca;
- criação de pendência;
- preparação de contexto para IA;
- envio para integração.

### 11.4 Operações compostas

Quando uma ação alterar múltiplas entidades que precisam permanecer coerentes, a implementação deverá utilizar:

- transação lógica única; ou
- eventos coordenados com mecanismo explícito de compensação.

Não poderá existir uma alteração parcial silenciosa que deixe o estado incompatível com o histórico.

---

## 12. Evidências

### 12.1 Função

A Evidência sustenta ou comprova um fato relevante.

Ela não substitui o evento. O Evento registra que algo aconteceu; a Evidência registra o elemento que sustenta ou demonstra esse acontecimento.

### 12.2 Tipos conceituais

Uma evidência poderá ser:

- confirmação humana;
- registro produzido pelo sistema;
- arquivo externo referenciado;
- documento gerado;
- mensagem recebida;
- resultado de integração;
- leitura de sensor ou serviço;
- conjunto de dados estruturados;
- fotografia ou imagem;
- assinatura, hash ou impressão digital;
- relação com eventos anteriores.

### 12.3 Estrutura mínima

Uma Evidência deverá permitir representar:

- identidade técnica;
- tipo;
- origem;
- momento;
- autor ou componente produtor;
- entidade, processo ou etapa associada;
- localização ou conteúdo estruturado;
- integridade ou assinatura, quando aplicável;
- estado de disponibilidade;
- nível de confiança ou validação, quando pertinente;
- histórico de substituição ou invalidação.

### 12.4 Evidência externa

Quando a evidência estiver fora do Mheibos, o sistema deverá armazenar referência suficiente para localizá-la e identificar sua relação com a operação.

A ausência física posterior não deverá apagar o histórico de que ela existiu.

### 12.5 Evidência inválida ou substituída

Uma evidência considerada incorreta não deverá ser apagada silenciosamente.

Ela poderá ser marcada como:

- invalidada;
- substituída;
- indisponível;
- contestada;
- não verificada.

O motivo e a autoria deverão permanecer registrados.

### 12.6 Evidência e IA

A IA poderá interpretar evidências, mas não poderá alterar sua origem ou promovê-las a fatos oficiais sem validação dos componentes do sistema.

---

## 13. Auditoria imutável

### 13.1 Regra geral

Registros de auditoria relevantes serão imutáveis.

Nenhum usuário comum ou administrador poderá editar ou apagar diretamente um registro de auditoria para alterar o passado.

### 13.2 Correção de erro

Quando um registro estiver incorreto, a correção deverá ocorrer por meio de um novo evento que:

- identifique o evento anterior;
- explique o erro;
- registre a correção;
- preserve os dois registros.

### 13.3 Conteúdo mínimo

A auditoria deverá preservar, conforme aplicável:

- evento;
- usuário;
- estação;
- sessão;
- data e hora;
- entidade afetada;
- operação;
- valor anterior;
- valor posterior;
- motivo;
- autorização;
- origem online ou offline;
- resultado;
- correlação;
- evidências relacionadas.

### 13.4 Acesso à auditoria

A visibilidade da auditoria dependerá das permissões do usuário.

A restrição de visualização não poderá alterar ou eliminar o registro.

### 13.5 Administradores

Administradores poderão consultar e executar procedimentos autorizados sobre o sistema, mas não poderão reescrever silenciosamente o histórico.

Ações administrativas sobre a auditoria, exportação, restauração ou retenção deverão também ser auditadas.

---

## 14. Exclusões, cancelamentos e apagamentos

### 14.1 Apagar não é destruir

Na interface, “apagar” poderá significar:

- remover do uso normal;
- cancelar;
- desativar;
- arquivar;
- substituir;
- invalidar.

O significado deverá ser explícito no domínio.

### 14.2 Conteúdo preservado

O sistema deverá preservar:

- identidade do registro;
- conteúdo anterior relevante;
- relações históricas;
- usuário que realizou a ação;
- momento;
- estação;
- motivo, quando exigido;
- autorização utilizada;
- impacto produzido.

### 14.3 Exclusão de item

Ao remover um item de um Pedido, o histórico deverá permitir saber:

- que o item existiu;
- quais eram descrição, quantidade e valor;
- quem removeu;
- por quê;
- como o total foi alterado.

### 14.4 Exclusão de entidade

Entidades com relevância comercial, financeira, operacional, administrativa ou de segurança deverão usar exclusão lógica ou encerramento explícito por padrão.

### 14.5 Destruição física excepcional

A destruição física somente poderá ocorrer quando:

- não houver obrigação de auditoria ou retenção;
- não quebrar relações históricas;
- estiver prevista por política específica;
- houver autorização correspondente;
- o procedimento ficar registrado quando aplicável.

### 14.6 Direito de correção e políticas futuras

Requisitos legais futuros de anonimização, correção ou descarte deverão ser implementados sem transformar o histórico operacional em narrativa falsa.

---

## 15. Auditoria de regras, permissões e políticas

### 15.1 Abrangência

Deverão gerar registros imutáveis:

- criação, alteração e desativação de perfis;
- concessão ou retirada de permissões;
- exceções individuais;
- alteração da lista de ações sensíveis;
- alteração de exigência de justificativa;
- mudança de critérios de metas;
- alteração de política de cobrança;
- mudança de modelos de fluxo oficiais;
- alteração de parâmetros de criticidade;
- mudança de regras administrativas.

### 15.2 Conteúdo

O registro deverá preservar:

- regra anterior;
- regra nova;
- autor;
- momento;
- justificativa, quando aplicável;
- vigência;
- escopo afetado;
- versão da política.

### 15.3 Aplicação histórica

A alteração de uma regra não deverá reescrever retroativamente quais regras foram aplicadas a operações passadas, salvo procedimento formal e auditado.

### 15.4 Reconstituição

Deverá ser possível identificar qual versão de política estava vigente quando uma ação relevante foi executada.

---

## 16. Eventos online e offline

### 16.1 Identificação obrigatória

Todo evento originado por Cliente deverá indicar se foi produzido:

- com a Central disponível;
- em modo offline restrito;
- durante recuperação ou reprocessamento.

### 16.2 Eventos locais

Eventos produzidos offline deverão ser persistidos localmente antes de a interface considerar a operação concluída.

### 16.3 Vinculação

O evento offline deverá permanecer vinculado:

- ao usuário autorizado;
- à estação;
- à sessão;
- ao pedido local;
- à sequência local;
- às permissões sincronizadas utilizadas.

### 16.4 Incorporação global

Quando a Central retornar, os eventos locais aceitos deverão ser incorporados sem perder:

- identidade de origem;
- ordem local;
- momento local;
- estado criado pelo usuário;
- indicação de que foram produzidos offline.

### 16.5 Duplicação

Repetir o envio do mesmo evento não poderá aplicar a mesma alteração duas vezes.

### 16.6 Falha de incorporação

Se um evento não puder ser incorporado:

- permanecerá preservado localmente;
- será marcado como pendente;
- o motivo será registrado;
- novas tentativas poderão ocorrer;
- o usuário será informado;
- nenhuma falha poderá apagar o pedido local.

As regras completas pertencem à RFC-0008.

---

## 17. Processamento imediato e desacoplado

### 17.1 Resposta percebida como imediata

A gravação da alteração essencial e do evento correspondente deverá ocorrer antes de a operação ser apresentada como concluída.

Esse caminho principal deverá ser curto e previsível.

### 17.2 Consequências secundárias

Poderão ser processadas posteriormente:

- notificações;
- atualização de dashboards;
- geração de relatórios derivados;
- indexação de busca;
- análise cognitiva;
- webhooks;
- mensagens externas;
- cálculos não essenciais à confirmação imediata;
- atualização de caches de outras estações.

### 17.3 Não perda

Processamento assíncrono não poderá significar “tentar e esquecer”.

Consequências pendentes deverão possuir estado, tentativa, resultado e diagnóstico.

### 17.4 Subnotificação

Um evento que exige comunicação não poderá desaparecer porque o processador de notificação falhou.

A falha deverá:

- permanecer visível ao componente responsável;
- ser repetida conforme política;
- produzir diagnóstico;
- permitir recuperação;
- preservar o vínculo com o evento original.

### 17.5 Supernotificação

Um evento poderá ser agregado ou resumido para evitar ruído, desde que nenhuma obrigação ou situação crítica seja ocultada.

A política de apresentação pertence às RFCs 0009 e 0012.

### 17.6 Processamento síncrono obrigatório

Deverão permanecer no caminho principal as validações necessárias para:

- autorização;
- integridade;
- consistência financeira essencial;
- bloqueio de edição;
- preservação do evento;
- confirmação da operação principal.

---

## 18. Entrega, idempotência e reprocessamento

### 18.1 Entrega pelo menos uma vez

A arquitetura poderá repetir a entrega de eventos para evitar perda.

Por isso, consumidores deverão ser capazes de reconhecer repetições.

### 18.2 Idempotência

Processar o mesmo evento mais de uma vez não poderá produzir efeitos duplicados indevidos.

Exemplos que devem ser evitados:

- cobrar duas vezes;
- criar duas pendências iguais;
- enviar duas confirmações idênticas;
- concluir a mesma etapa duas vezes;
- duplicar um pedido offline.

### 18.3 Chave de idempotência

Eventos e comandos relevantes deverão possuir identidade ou chave suficiente para detecção de repetição.

### 18.4 Reprocessamento

Reprocessar uma consequência deverá preservar:

- evento original;
- número da tentativa;
- motivo;
- resultado;
- operador administrativo, quando manual.

### 18.5 Fila de falhas

Eventos ou consequências que excedam as tentativas normais deverão permanecer em estado de falha controlada, nunca desaparecer.

### 18.6 Compensação

Quando uma consequência já executada precisar ser desfeita, o sistema deverá gerar evento compensatório. Não deverá apagar o evento original.

---

## 19. Projeções e reconstrução de estado

### 19.1 Projeção

Uma Projeção é uma visão derivada de eventos e dados oficiais para facilitar consulta.

Exemplos:

- estado atual do pedido;
- saldo atual;
- progresso do processo;
- dashboard;
- histórico resumido;
- caixa de notificações.

### 19.2 Fonte oficial

A existência de projeções não autoriza múltiplas fontes divergentes de verdade.

A implementação deverá definir qual dado é oficial e como a projeção é reconstruída ou corrigida.

### 19.3 Reconstrução

Quando previsto, deverá ser possível reconstruir a evolução de uma entidade a partir de seus eventos e dados preservados.

Esta RFC não obriga event sourcing integral para toda a plataforma.

### 19.4 Event sourcing não obrigatório

O Mheibos poderá manter estado atual materializado junto ao histórico de eventos.

A exigência normativa é:

- registrar alterações relevantes;
- preservar auditoria imutável;
- manter coerência entre estado atual e histórico;
- permitir diagnóstico e correção.

### 19.5 Divergência

Quando uma projeção divergir da fonte oficial, deverá ser possível:

- detectar;
- identificar a causa;
- reconstruir ou corrigir;
- registrar a intervenção.

---

## 20. Consulta e apresentação da auditoria

### 20.1 Consulta por entidade

O sistema deverá permitir consultar o histórico relacionado a:

- pedido;
- item;
- processo;
- etapa;
- cliente;
- usuário;
- estação;
- perfil;
- política;
- missão;
- pendência;
- integração.

### 20.2 Consulta por período e autoria

Usuários autorizados poderão filtrar por:

- período;
- autor;
- estação;
- tipo de evento;
- origem online ou offline;
- ação sensível;
- resultado;
- entidade.

### 20.3 Linguagem compreensível

O histórico deverá possuir representação legível ao usuário, sem depender de payload técnico bruto.

Exemplo:

> Maria alterou o prazo do Pedido #J324 de 15/08/2026 para 18/08/2026 às 14:32, na Estação X.

### 20.4 Detalhamento técnico

Usuários com permissão poderão abrir detalhes estruturados, incluindo identificadores, correlação, versões e metadados.

### 20.5 Exportação

Exportações da auditoria deverão ser registradas quando envolverem dados sensíveis ou investigação formal.

### 20.6 Explicação pela IA

A IA poderá resumir e explicar históricos autorizados, mas deverá apontar para os registros oficiais e distinguir fato de interpretação.

---

## 21. Segurança e integridade

### 21.1 Proteção contra alteração

A persistência deverá impedir atualização ou exclusão comum dos registros de auditoria.

### 21.2 Integridade

A implementação deverá possuir mecanismos adequados para detectar corrupção, lacunas ou alterações indevidas.

Técnicas concretas poderão incluir:

- restrições de banco;
- assinaturas;
- hashes encadeados;
- armazenamento append-only;
- trilhas de verificação;
- backups verificados.

Esta RFC não obriga uma técnica específica.

### 21.3 Menor privilégio

Componentes deverão receber somente a capacidade necessária para publicar ou consumir eventos.

### 21.4 Dados sensíveis

O conteúdo da auditoria poderá conter informações sensíveis. Sua consulta deverá respeitar permissões, escopos e políticas.

### 21.5 Segredos

Senhas, tokens e segredos não deverão ser gravados em texto legível dentro de eventos ou logs.

### 21.6 Tentativas proibidas

Tentativas relevantes de acesso ou alteração sem permissão deverão gerar registros de segurança sem expor segredos.

---

## 22. Retenção, arquivamento e restauração

### 22.1 Retenção

A política concreta de retenção será definida posteriormente, considerando:

- necessidade operacional;
- auditoria;
- obrigações legais;
- privacidade;
- custo de armazenamento;
- recuperação de incidentes.

### 22.2 Arquivamento

Eventos antigos poderão ser movidos para armazenamento de longo prazo, desde que permaneçam:

- íntegros;
- consultáveis quando autorizado;
- ligados às entidades originais;
- protegidos contra alteração.

### 22.3 Backup

Backups deverão incluir estado oficial e histórico necessário à reconstrução.

### 22.4 Restauração

Toda restauração relevante deverá gerar evento administrativo contendo:

- responsável;
- data e hora;
- origem do backup;
- escopo restaurado;
- resultado;
- divergências detectadas.

### 22.5 Lacunas

A arquitetura deverá detectar e sinalizar lacunas inesperadas em sequências ou registros essenciais.

---

## 23. Observabilidade do pipeline de eventos

### 23.1 Indicadores técnicos

O sistema deverá permitir acompanhar:

- quantidade de eventos produzidos;
- eventos pendentes;
- tempo até persistência;
- tempo de processamento secundário;
- falhas e repetições;
- tamanho das filas;
- eventos offline aguardando sincronização;
- projeções atrasadas;
- consumidores indisponíveis.

### 23.2 Separação da auditoria

Métricas e logs técnicos do pipeline não substituem os registros de auditoria.

### 23.3 Alertas técnicos

Falhas que ameacem perda, atraso excessivo, subnotificação ou divergência deverão gerar alertas técnicos e, quando afetarem a operação, eventos administrativos correspondentes.

### 23.4 Diagnóstico acionável

Mensagens de erro deverão indicar:

- evento afetado;
- componente;
- tentativa;
- causa conhecida;
- próxima ação possível.

---

## 24. Fluxos arquiteturais principais

### 24.1 Alteração online comum

```text
Usuário altera um dado
        ↓
Cliente envia comando
        ↓
Central valida permissão e regras
        ↓
Persistência aplica a alteração essencial
        ↓
Evento é gravado de forma durável
        ↓
Central confirma a operação
        ↓
Cliente atualiza a interface
        ↓
Consequências secundárias são processadas
```

### 24.2 Ação sensível

```text
Usuário solicita ação sensível
        ↓
Sistema exige senha
        ↓
Usuário comum informa motivo obrigatório
        ↓
Central valida autorização
        ↓
Ação é executada
        ↓
Evento registra ação, motivo e autenticação
        ↓
Auditoria preserva conteúdo anterior
```

### 24.3 Exclusão lógica

```text
Usuário autorizado solicita apagar
        ↓
Sistema valida política
        ↓
Registro sai do uso normal
        ↓
Conteúdo anterior permanece preservado
        ↓
Evento de exclusão é gravado
        ↓
Projeções são atualizadas
```

### 24.4 Operação offline

```text
Cliente está sem Central
        ↓
Usuário cria pedido local permitido
        ↓
Estado e eventos são persistidos localmente
        ↓
Central retorna
        ↓
Cliente informa e inicia sincronização
        ↓
Central incorpora eventos idempotentemente
        ↓
Pedido passa ao estado global
        ↓
Eventos mantêm origem offline
```

### 24.5 Falha de consequência secundária

```text
Evento oficial já foi gravado
        ↓
Processador de notificação falha
        ↓
Falha é registrada
        ↓
Evento permanece pendente para o consumidor
        ↓
Nova tentativa ocorre
        ↓
Sucesso ou encaminhamento para recuperação
```

---

## 25. Relação com os demais RFCs

| RFC | Responsabilidade relacionada |
|---|---|
| RFC-0000 | Propósito do Mheibos como memória operacional ativa |
| RFC-0001 | Rastreabilidade, fonte da verdade, segurança e decisão consciente |
| RFC-0002 | Significado operacional de Processo, Estado, Evidência e transições |
| RFC-0003 | Central, Clientes, serviços e fronteiras técnicas |
| RFC-0004 | Interpretação cognitiva de eventos e evidências |
| RFC-0005 | Entidades, identidades, relações e persistência conceitual |
| RFC-0007 | Autenticação, permissões, ações sensíveis e bloqueios |
| RFC-0008 | Armazenamento local, eventos offline e sincronização |
| RFC-0009 | Apresentação visual de intervenções e notificações |
| RFC-0010 | Eventos de Missões e Teamwork |
| RFC-0011 | Proveniência de conhecimento e memória |
| RFC-0012 | Pendências, lembretes, scheduler e escalonamento |
| RFC-0013 | Eventos comerciais, financeiros, metas e cobranças |
| RFC-0014 | Eventos de arquivos, WhatsApp, webhooks e integrações |
| RFC-0015 | Projeções analíticas, dashboards e simulações |
| RFC-0016 | Auditoria de ensino, aprovação e governança da IA |

Esta RFC define o registro e a rastreabilidade dos fatos. Os demais RFCs definem o significado dos domínios, as permissões, a sincronização e a apresentação das consequências.

---

## 26. Consequências da decisão

### 26.1 Benefícios

- histórico confiável da operação;
- responsabilização clara;
- suporte a investigação de erros;
- preservação de apagamentos e cancelamentos;
- base sólida para IA e analytics;
- sincronização offline rastreável;
- possibilidade de reprocessar consequências;
- redução de divergências silenciosas;
- capacidade de explicar como um estado foi alcançado;
- auditoria de regras e segurança.

### 26.2 Custos

- maior volume de armazenamento;
- necessidade de versionar esquemas de eventos;
- maior disciplina no desenho dos casos de uso;
- implementação de idempotência;
- filas e processadores secundários;
- mecanismos de recuperação;
- consultas históricas mais complexas;
- proteção adicional da auditoria.

### 26.3 Riscos

- registrar eventos genéricos demais;
- gravar texto sem estrutura suficiente;
- tratar log técnico como auditoria;
- processar consequências antes de preservar o evento;
- duplicar efeitos durante repetição;
- perder ordem durante sincronização offline;
- permitir alteração administrativa do histórico;
- armazenar segredos em payloads;
- gerar eventos excessivos sem valor operacional;
- criar lentidão por colocar tudo no caminho síncrono;
- gerar subnotificação por falhas silenciosas de consumidores;
- manter projeções divergentes do estado oficial.

---

## 27. Critérios de conformidade

Uma implementação estará em conformidade com esta RFC somente se:

1. alterações relevantes produzirem eventos estruturados;
2. cada evento relevante possuir identidade única;
3. autoria, momento, estação, sessão e origem puderem ser preservados;
4. eventos distinguirem origem online e offline;
5. alterações auditáveis preservarem valores anteriores e posteriores quando aplicável;
6. registros de auditoria não puderem ser editados ou apagados por operações comuns;
7. correções ocorrerem por novos eventos;
8. exclusões relevantes preservarem conteúdo e autoria;
9. mudanças de regras, perfis, permissões e políticas forem auditadas;
10. eventos offline forem persistidos localmente antes da confirmação visual;
11. reenvio do mesmo evento não duplicar efeitos;
12. falhas secundárias não apagarem o evento original;
13. consequências assíncronas possuírem estado e recuperação;
14. o caminho principal permanecer responsivo;
15. notificações não substituírem o histórico;
16. logs técnicos não substituírem eventos de negócio;
17. a IA não alterar eventos ou evidências oficiais diretamente;
18. projeções divergentes puderem ser detectadas e reconstruídas;
19. segredos não forem armazenados em texto legível nos eventos;
20. restaurações e reprocessamentos administrativos forem auditados.

---

## 28. Decisões adiadas

As seguintes decisões serão tomadas na implementação ou em documentos posteriores:

- tecnologia concreta de barramento;
- banco ou armazenamento dos eventos;
- uso de outbox transacional;
- formato físico do envelope de evento;
- convenção final de nomes de eventos;
- serialização;
- mecanismo de assinatura ou hash;
- política de particionamento;
- tempo de retenção;
- compressão e arquivamento;
- estratégia de snapshots;
- garantias concretas de ordenação;
- número e política de tentativas;
- fila de falhas definitiva;
- ferramenta de observabilidade;
- formato visual da auditoria;
- política de exportação;
- anonimização e descarte legal;
- mecanismo de reconstrução de projeções;
- catálogo completo de eventos por domínio.

Essas decisões deverão respeitar os princípios, invariantes e critérios de conformidade desta RFC.

---

## 29. Rastreabilidade com o Inventário Oficial

| Decisão | Seção principal desta RFC |
|---|---|
| INV-024 — alterações relevantes geram eventos | 6, 7 e 8 |
| INV-025 — operação percebida como imediata | 17 e 24 |
| INV-026 — histórico de auditoria imutável | 13 e 21 |
| INV-027 — exclusões são eventos | 14 |
| INV-028 — origem online ou offline | 9, 10 e 16 |
| INV-029 — regras e segurança também são auditadas | 15 |

---

## 30. Declaração normativa

Toda alteração operacional, comercial, financeira, administrativa ou de segurança relevante no Mheibos deverá produzir um Evento estruturado e rastreável.

O Evento deverá preservar identidade, autoria ou origem técnica, momento, estação, sessão, contexto, entidades afetadas e mudança realizada. Quando aplicável, deverá registrar valores anteriores e posteriores, justificativas, autorizações e evidências relacionadas.

O histórico de auditoria será imutável. Correções, cancelamentos, exclusões e compensações serão representados por novos eventos, nunca por reescrita silenciosa do passado. Apagar na interface não significará destruir a memória operacional.

Eventos produzidos offline deverão manter sua origem, ordem local e vínculo com usuário e estação durante a incorporação à Central. Repetições não poderão gerar efeitos duplicados.

A persistência do evento essencial deverá ocorrer antes da confirmação da operação ao usuário. Consequências secundárias poderão ser processadas de forma desacoplada, desde que não haja perda, subnotificação, inconsistência silenciosa ou desaparecimento de falhas.

A arquitetura de eventos será a base da rastreabilidade, da auditoria, da sincronização, das notificações, das projeções analíticas e da interpretação cognitiva do Mheibos, sem substituir o modelo de dados nem transformar a IA em fonte oficial da verdade.
