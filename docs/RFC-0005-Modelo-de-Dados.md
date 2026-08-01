# MHEIBOS INTELLIGENT OPERATING SYSTEM

# RFC-0005 — Modelo de Dados

**Status:** Draft para aprovação  
**Versão:** 0.1  
**Data:** 30/07/2026  
**Dependências:** RFC-0000, RFC-0001, RFC-0002, RFC-0003  
**Fonte normativa:** Inventário Oficial de Decisões Arquiteturais do Mheibos

---

## 1. Resumo

Esta RFC define o modelo conceitual de dados do Mheibos.

Seu objetivo é estabelecer quais informações constituem a realidade oficial do sistema, como elas se relacionam, como identidades e autorias são preservadas e quais fronteiras devem existir entre estado atual, histórico, arquivos, conhecimento e dados temporários de cada estação.

O modelo parte de duas centralidades complementares:

- o **Pedido** é o centro comercial e financeiro;
- o **Processo** é o centro da execução operacional.

A persistência deverá representar essa distinção sem reduzir toda a empresa a uma única tabela de pedidos, a uma sequência fixa de status ou à estrutura visual dos módulos da interface.

Esta RFC não define tabelas SQL definitivas, banco de dados, índices, formatos físicos, protocolo de sincronização, esquema completo de eventos ou regras de autorização. Esses detalhes pertencem à implementação ou aos RFCs especializados.

---

## 2. Objetivo

Esta RFC responde às seguintes perguntas:

- quais são as principais entidades persistentes do Mheibos;
- como Pedido, Processo, Fluxo, Etapa, Estado e Evidência se relacionam;
- como identidade técnica e identificação visível devem coexistir;
- como autoria comercial se diferencia de responsabilidade operacional;
- como estados comerciais, operacionais e financeiros permanecem independentes;
- como exclusões, cancelamentos e substituições devem ser representados;
- como arquivos externos são referenciados sem transformar o Mheibos em repositório documental;
- como dados locais, globais, temporários e oficiais devem ser separados;
- quais invariantes toda implementação do banco deverá preservar.

---

## 3. Princípios do modelo

### 3.1 A realidade operacional não é a interface

Telas, abas, filtros, dashboards e módulos são formas de apresentação. Eles não constituem o modelo oficial da empresa.

As entidades deverão representar a realidade do negócio independentemente da forma como ela é exibida.

### 3.2 Estado atual e histórico são diferentes

O estado atual permite responder como uma entidade está agora.

O histórico permite responder como ela chegou até esse estado.

O estado atual poderá ser atualizado. O histórico relevante não poderá ser destruído.

### 3.3 A IA não é fonte oficial dos dados

Resultados produzidos pela IA serão sugestões, interpretações, hipóteses ou propostas até que sejam validados pelos mecanismos determinísticos e, quando necessário, por um usuário autorizado.

### 3.4 A identidade não depende do nome visível

Nomes, códigos amigáveis, descrições e números apresentados ao usuário podem mudar ou repetir em contextos diferentes. Cada entidade persistente deverá possuir uma identidade técnica estável e não ambígua.

### 3.5 Relações importantes devem ser explícitas

Dependências, autoria, responsabilidade, pertencimento, bloqueios, vínculos financeiros e associação com arquivos não deverão depender apenas de texto livre ou inferência da IA.

### 3.6 Exclusão de uso não significa destruição de memória

Quando uma entidade for apagada, cancelada, substituída ou desativada na interface, sua existência anterior e seus vínculos relevantes deverão permanecer preservados conforme as regras de auditoria.

### 3.7 O modelo deve permitir evolução

A primeira versão é local e atende uma única empresa, mas o modelo não deverá tornar impossível a futura separação por organizações, a migração para nuvem ou a criação de aplicações especializadas.

---

## 4. Escopo

### 4.1 Incluído

Esta RFC define conceitualmente:

- identidade das entidades;
- organização e instalação;
- usuários, perfis e estações;
- clientes;
- pedidos e itens;
- processos, fluxos e etapas;
- estados independentes;
- responsabilidades e autorias;
- pagamentos, saldos e pendências financeiras em nível estrutural;
- missões, tarefas, conversas e notas em nível estrutural;
- referências de arquivos;
- eventos e evidências apenas como vínculos conceituais;
- dados globais e dados locais;
- ciclo de vida e preservação dos registros.

### 4.2 Fora do escopo

Não são definidos aqui:

- banco de dados definitivo;
- ORM;
- nomes finais de tabelas e colunas;
- tipos SQL;
- índices e plano de consultas;
- particionamento;
- criptografia concreta;
- protocolo de replicação;
- resolução detalhada de sincronização;
- payload completo de eventos;
- formato de evidências;
- política detalhada de permissões;
- regras completas de metas, comissões e cobrança;
- modelo vetorial ou mecanismo de memória da IA;
- contratos externos de integrações.

---

## 5. Visão geral do domínio

```text
Organização / Instalação
│
├── Usuários ── Perfil ── Permissões
│      │
│      ├── Sessões
│      ├── Estações autorizadas
│      └── Código de origem comercial
│
├── Clientes
│      └── Pedidos
│           ├── Itens
│           ├── Valores e pagamentos
│           ├── Processos
│           │    ├── Fluxo instanciado
│           │    ├── Etapas
│           │    ├── Responsáveis
│           │    └── Estados operacionais
│           ├── Referências de arquivos
│           ├── Pendências
│           └── Eventos / Auditoria
│
├── Missões
│      ├── Participantes
│      ├── Tarefas
│      ├── Conversas
│      ├── Notas
│      └── Referências operacionais
│
└── Conhecimento e configurações
       ├── Modelos de fluxo
       ├── Políticas
       ├── Preferências
       └── Memórias aprovadas
```

O diagrama é conceitual. Ele não determina a quantidade de tabelas nem obriga uma estrutura relacional específica.

---

## 6. Identidade das entidades

### 6.1 Identificador técnico

Toda entidade persistente deverá possuir um identificador técnico:

- único dentro do escopo oficial da instalação;
- estável durante todo o ciclo de vida;
- independente de nome, posição, número sequencial ou usuário atual;
- não reutilizável após exclusão, desativação ou arquivamento;
- adequado à futura migração ou integração.

O formato concreto do identificador técnico será decidido na implementação.

### 6.2 Identificador visível

Entidades poderão possuir identificadores amigáveis usados pela operação.

No caso de pedidos, a identificação visível deverá combinar:

- o código permanente de origem do usuário;
- uma sequência local daquele código.

Exemplo:

```text
#J324
```

O identificador visível não substitui o identificador técnico.

### 6.3 Imutabilidade da identidade

Alterar nome, responsável, estado, cliente, origem de exibição ou descrição não poderá criar uma nova identidade silenciosamente.

Quando uma entidade for substituída por outra, a relação de substituição deverá ser explícita.

### 6.4 Códigos não reutilizáveis

Códigos de origem que já tenham identificado pedidos não poderão ser transferidos a outro usuário.

Um usuário desativado poderá continuar aparecendo no histórico como autor dos registros que originou.

---

## 7. Organização e instalação

### 7.1 Organização

A Organização representa a empresa cuja operação é gerenciada pelo Mheibos.

Na primeira versão existirá uma única organização ativa por instalação.

Mesmo assim, entidades globais deverão possuir vínculo explícito ou implicitamente garantido com a organização para que uma futura evolução multiorganizacional não exija redefinir toda a identidade dos dados.

### 7.2 Instalação

A Instalação representa a implantação técnica local do Mheibos.

Ela identifica, no mínimo:

- a organização atendida;
- a Central responsável;
- as estações registradas;
- a versão da plataforma;
- configurações locais relevantes;
- o estado técnico da implantação.

Organização e Instalação são conceitos diferentes: uma organização é o sujeito operacional; uma instalação é uma forma técnica de executar o sistema.

### 7.3 Estação

A Estação representa um computador autorizado a executar um Cliente Mheibos.

Ela deverá possuir identidade própria e permitir associar:

- sessões;
- operações locais;
- origem técnica de eventos;
- credencial offline autorizada;
- estado de conectividade;
- dados pendentes de sincronização.

---

## 8. Identidade humana e acesso

### 8.1 Usuário

O Usuário representa uma pessoa autenticável no Mheibos.

Seu registro deverá permitir distinguir:

- identidade pessoal;
- credenciais e estado de acesso;
- perfil atual;
- exceções individuais;
- código de origem comercial, quando aplicável;
- situação ativa, bloqueada ou desativada;
- relações históricas com pedidos, processos, eventos e missões.

### 8.2 Perfil

Cada usuário terá exatamente um Perfil principal.

O Perfil representa a função organizacional e o conjunto padrão de permissões.

Exceções individuais não criam um segundo perfil; elas complementam ou restringem o perfil principal.

### 8.3 Sessão

A Sessão representa um período autenticado de uso.

Ela deverá relacionar:

- usuário;
- estação;
- início e encerramento;
- origem online ou offline;
- contexto de autenticação;
- permissões efetivas utilizadas;
- existência de operações locais pendentes.

Sessões não substituem a identidade do usuário e não devem ser utilizadas como autor permanente de um registro.

### 8.4 Desativação sem perda histórica

Desativar um usuário não poderá remover:

- pedidos criados;
- alterações realizadas;
- processos concluídos;
- mensagens e notas autorizadas;
- decisões gerenciais;
- eventos de auditoria.

---

## 9. Cliente

### 9.1 Entidade Cliente

O Cliente representa a pessoa, empresa ou organização atendida comercialmente.

Ele poderá participar de múltiplos pedidos e processos ao longo do tempo.

### 9.2 Identidade e contatos

Dados de contato devem ser modelados separadamente da identidade principal quando houver necessidade de múltiplos telefones, endereços, responsáveis ou canais.

O modelo deverá permitir preservar qual contato foi usado em uma operação específica, mesmo que o cadastro seja atualizado posteriormente.

### 9.3 Histórico de relacionamento

Pedidos, atendimentos, pendências, notas compartilhadas e interações deverão apontar explicitamente para o Cliente quando essa relação existir.

O histórico não deverá depender apenas de busca textual pelo nome.

---

## 10. Pedido

### 10.1 Papel

O Pedido é a entidade central da relação comercial e financeira.

Ele representa aquilo que foi vendido, para quem, por qual valor, em quais condições e com qual compromisso de entrega.

### 10.2 Estrutura mínima

Um Pedido deverá permitir representar, no mínimo:

- identidade técnica;
- identificador visível;
- cliente;
- autor comercial;
- usuário que fechou a venda, quando diferente;
- data e origem de criação;
- itens;
- valores;
- descontos;
- pagamentos;
- saldo;
- prazos;
- estados comercial, operacional e financeiro;
- processos associados;
- referências de arquivos;
- responsáveis atuais;
- origem online ou offline;
- situação ativa, cancelada, concluída, arquivada ou removida do uso normal.

### 10.3 Autoria comercial

O criador comercial do Pedido permanecerá vinculado à venda para fins de origem, metas e histórico, mesmo que outras pessoas:

- alterem o pedido;
- executem etapas;
- concluam a produção;
- realizem a entrega;
- registrem pagamentos.

Uma transferência de autoria comercial deverá ser uma ação explícita, autorizada e auditada.

### 10.4 Origem não é propriedade

O prefixo visível e a autoria comercial não concedem controle permanente sobre o Pedido.

Após integrar o estado global, qualquer usuário autorizado poderá atuar sobre ele conforme as regras de bloqueio e permissão.

### 10.5 Pedido e processo

Um Pedido poderá possuir um ou mais Processos.

O Pedido não deverá ser usado como substituto genérico de todas as etapas operacionais.

---

## 11. Item do pedido

### 11.1 Papel

O Item do Pedido representa um produto, serviço ou unidade comercializada dentro de um Pedido.

### 11.2 Dados próprios

Cada item poderá possuir:

- descrição comercial preservada;
- quantidade;
- unidade;
- preço unitário;
- descontos próprios;
- valor final;
- categoria ou tipo de serviço;
- especificações;
- prazos particulares;
- processos associados;
- arquivos relacionados;
- estado de cancelamento ou remoção.

### 11.3 Preservação da descrição histórica

Atualizar o cadastro de um produto ou serviço não deverá alterar silenciosamente a descrição, preço ou condições que foram efetivamente contratadas em pedidos anteriores.

O Pedido deverá preservar uma representação histórica das condições da venda.

### 11.4 Remoção de item

Remover um item da operação corrente não poderá apagar o fato de que ele existiu.

A remoção deverá preservar:

- conteúdo anterior;
- autor;
- momento;
- motivo quando exigido;
- impactos financeiros e operacionais.

---

## 12. Processo

### 12.1 Papel

O Processo é a entidade central da execução operacional.

Ele representa a organização concreta do trabalho necessário para alcançar um objetivo.

### 12.2 Relações

Um Processo deverá relacionar:

- objetivo;
- entidade de origem, como Pedido, Item, Cliente ou Missão;
- modelo de fluxo utilizado;
- fluxo instanciado;
- etapas;
- responsáveis;
- estado operacional atual;
- dependências e bloqueios;
- evidências;
- prazos;
- resultado esperado;
- conclusão ou encerramento.

### 12.3 Processo independente

Embora muitos processos sejam originados por pedidos, o modelo deverá permitir processos que não dependam diretamente de uma venda, como:

- cobrança;
- compra de material;
- manutenção;
- melhoria interna;
- missão administrativa.

### 12.4 Processo como instância

Cada Processo é uma instância operacional própria.

Alterar o modelo padrão de fluxo no futuro não deverá reescrever silenciosamente processos já confirmados.

---

## 13. Modelo de fluxo e fluxo instanciado

### 13.1 Modelo de fluxo

O Modelo de Fluxo é uma definição reutilizável de como determinado tipo de trabalho normalmente acontece.

Ele poderá conter:

- etapas sugeridas;
- ordem esperada;
- condições;
- dependências;
- obrigatoriedade;
- regras de entrada e saída;
- parâmetros de prazo.

### 13.2 Fluxo instanciado

Ao criar ou confirmar um Processo, o sistema produzirá um Fluxo Instanciado.

Esse fluxo representa o caminho oficial daquela ocorrência específica.

O usuário autorizado poderá incluir, retirar, dispensar ou adaptar etapas antes da confirmação.

### 13.3 Independência histórica

Depois da confirmação:

- o fluxo instanciado não dependerá da versão futura do modelo;
- ajustes posteriores deverão gerar alterações explícitas;
- etapas dispensadas não deverão desaparecer sem registro;
- a versão ou origem do modelo deverá permanecer identificável.

### 13.4 Exceções operacionais

O modelo deverá representar de forma distinta situações como:

- criação de arte pela empresa;
- arte fornecida e pronta;
- aguardando arquivo do cliente;
- serviço imediato;
- pronto e entregue no momento da venda.

Essas situações não devem ser comprimidas em um único campo booleano ambíguo.

---

## 14. Etapa

### 14.1 Papel

A Etapa representa uma unidade identificável do trabalho dentro de um Processo.

### 14.2 Estrutura

Uma etapa poderá possuir:

- identidade;
- nome e descrição;
- posição esperada no fluxo;
- obrigatoriedade;
- condição de aplicação;
- responsável ou grupo responsável;
- estado próprio;
- prazo;
- dependências;
- evidências necessárias;
- resultado produzido;
- motivo de dispensa, cancelamento ou reabertura.

### 14.3 Estados da etapa

O estado da Etapa deverá ser independente do estado geral do Pedido.

Estados concretos serão definidos no domínio correspondente, mas o modelo deverá permitir distinguir, no mínimo, situações equivalentes a:

- não iniciada;
- aguardando condição externa;
- pronta para execução;
- em andamento;
- bloqueada;
- concluída;
- dispensada;
- cancelada;
- reaberta.

### 14.4 Conclusão e autoria

A conclusão deverá registrar quem realizou ou confirmou a ação, sem substituir o histórico dos responsáveis anteriores.

---

## 15. Objetivo, responsabilidade e participação

### 15.1 Objetivo

Todo Processo e toda Missão deverão possuir um objetivo explícito ou identificável.

O objetivo representa o resultado esperado, não apenas o nome de uma tela ou função.

### 15.2 Responsabilidade atual

Uma entidade operacional poderá possuir um responsável atual.

Essa relação indica quem deve agir agora, mas não apaga autores e responsáveis anteriores.

### 15.3 Papéis distintos

O modelo deverá separar, quando aplicável:

- criador;
- autor comercial;
- responsável atual;
- executor;
- aprovador;
- concluidor;
- supervisor;
- participante;
- observador.

Uma única pessoa poderá ocupar mais de um papel, mas os papéis não deverão ser reduzidos a um campo genérico chamado apenas `usuario`.

### 15.4 Histórico de responsabilidade

Transferências de responsabilidade deverão preservar:

- responsável anterior;
- novo responsável;
- momento;
- autor da transferência;
- motivo, quando exigido.

---

## 16. Estados independentes

### 16.1 Regra geral

Uma entidade complexa não deverá possuir um único status usado para representar todas as dimensões da realidade.

### 16.2 Estado comercial

Representa a situação da relação de venda, como criação, confirmação, cancelamento ou encerramento comercial.

### 16.3 Estado operacional

Representa a situação da execução, derivada dos processos, etapas, bloqueios e evidências.

### 16.4 Estado financeiro

Representa a situação dos valores e pagamentos, como saldo em aberto, pagamento parcial, quitação ou pagamento adicional pendente.

### 16.5 Estado de entrega

Quando necessário, a entrega deverá possuir estado próprio e não ser inferida exclusivamente do estado financeiro ou da produção.

### 16.6 Composição

A interface poderá apresentar uma situação resumida, mas a persistência deverá manter as dimensões independentes.

Exemplo válido:

```text
Comercial: confirmado
Operacional: concluído
Entrega: entregue
Financeiro: saldo em aberto
```

### 16.7 Estado derivado e estado registrado

Alguns estados poderão ser calculados a partir de fatos e relações; outros poderão precisar de confirmação explícita.

A implementação deverá documentar quais estados são derivados e quais são registrados, evitando divergência entre múltiplas fontes de verdade.

---

## 17. Valores, pagamentos e saldo

### 17.1 Separação estrutural

O valor total do Pedido, os Pagamentos realizados e o Saldo atual são conceitos diferentes.

Pagamentos não deverão ser substituídos por um único campo de “valor pago”.

### 17.2 Pagamento

Cada Pagamento deverá possuir identidade própria e permitir representar:

- valor;
- momento;
- forma;
- autor do registro;
- pedido associado;
- situação ativa, cancelada, estornada ou corrigida;
- referência externa, quando houver;
- origem online ou offline.

### 17.3 Alteração do total

Quando o valor total do Pedido mudar:

- pagamentos existentes permanecerão preservados;
- o saldo será recalculado;
- o estado financeiro será atualizado conforme regras determinísticas;
- a alteração produzirá histórico auditável.

### 17.4 Entrega com saldo

Quando uma entrega com saldo em aberto for autorizada, o modelo deverá permitir relacionar:

- autorização;
- autor da autorização;
- motivo;
- saldo pendente;
- pendência financeira criada;
- responsável principal;
- supervisores.

As regras de autorização e cobrança pertencem ao RFC-0013.

---

## 18. Pendência

### 18.1 Papel

A Pendência representa uma obrigação ainda não encerrada que requer acompanhamento e decisão consciente.

### 18.2 Estrutura conceitual

Uma Pendência deverá permitir associar:

- entidade de origem;
- tipo;
- descrição;
- responsável principal;
- supervisores ou destinatários;
- prazo ou vencimento;
- prioridade;
- criticidade;
- estado;
- lembretes;
- escalonamentos;
- ações realizadas;
- forma de encerramento.

### 18.3 Um registro, vários destinatários

Uma pendência poderá notificar várias pessoas sem ser duplicada.

Deverá existir um responsável principal claramente identificado.

### 18.4 Encerramento explícito

A pendência deverá terminar por uma ação identificável, como:

- resolução;
- quitação;
- cancelamento autorizado;
- renegociação;
- delegação;
- justificativa aceita;
- incorporação a outro processo.

---

## 19. Missão e Teamwork

### 19.1 Missão

A Missão representa um objetivo operacional temporário e persistente, individual ou coletivo.

Ela deverá permitir armazenar:

- objetivo;
- criador;
- origem voluntária, sugerida ou administrativa;
- responsável ou líder;
- participantes;
- plano;
- tarefas;
- progresso;
- estado;
- contexto de interface necessário para retomada;
- conversas;
- notas;
- referências relacionadas;
- conclusão e resultado.

### 19.2 Persistência do contexto

Pausar uma missão não deverá apagá-la.

O modelo deverá conservar informações suficientes para que a interface focada seja reconstruída sem transformar detalhes visuais transitórios em regras globais.

### 19.3 Participação

A participação deverá registrar:

- usuário;
- papel na missão;
- forma de entrada;
- estado de participação;
- data de entrada e saída;
- autoridade necessária para remoção.

### 19.4 Tarefa de missão

Tarefas poderão apontar para processos e etapas existentes ou representar trabalho específico da missão.

A tarefa não deverá duplicar silenciosamente um processo oficial quando for apenas uma visão ou agrupamento dele.

### 19.5 Conversa e nota

Mensagens e Notas são entidades diferentes:

- a Conversa preserva comunicação cronológica;
- a Nota preserva conhecimento ou observação consolidada.

---

## 20. Arquivos e documentos

### 20.1 Referência de arquivo

O Mheibos não será o repositório principal dos arquivos da empresa.

A persistência deverá registrar uma Referência de Arquivo, contendo conforme necessário:

- caminho ou localização;
- nome;
- tipo;
- aplicativo associado;
- entidade relacionada;
- autor ou origem;
- data conhecida;
- estado de disponibilidade;
- metadados operacionais;
- identificador de versão ou assinatura, quando implementado.

### 20.2 Vínculo contextual

Uma referência poderá estar associada a:

- Pedido;
- Item;
- Processo;
- Etapa;
- Cliente;
- Missão;
- relatório;
- ordem de serviço;
- evidência.

### 20.3 Ausência física

A inexistência temporária do arquivo no caminho conhecido não deverá apagar sua referência nem o histórico de que ele participou da operação.

### 20.4 Documentos gerados

PDFs, ordens de serviço e relatórios gerados pelo Mheibos deverão ser relacionados à entidade que lhes dá contexto, sem exigir um módulo documental independente.

---

## 21. Evidência, evento e auditoria

### 21.1 Fronteira desta RFC

Evento, Evidência e Registro de Auditoria são entidades reconhecidas pelo modelo, mas seus formatos normativos pertencem ao RFC-0006.

### 21.2 Relações obrigatórias

O modelo de dados deverá permitir que um evento ou evidência se relacione com:

- entidade afetada;
- usuário ou origem técnica;
- estação;
- sessão;
- processo e etapa;
- momento;
- contexto online ou offline;
- operação que o produziu.

### 21.3 Estado reconstruível

Sempre que definido pelo RFC-0006, deverá ser possível compreender ou reconstruir a evolução de uma entidade por meio de seus eventos, sem depender exclusivamente de um log textual não estruturado.

### 21.4 Auditoria não é observabilidade técnica

Logs técnicos de falha, desempenho e saúde não substituem eventos de negócio e registros de auditoria.

---

## 22. Configuração, política e preferência

### 22.1 Configuração da organização

Configurações que alteram o comportamento oficial da empresa deverão ser persistidas como dados organizacionais versionáveis e auditáveis.

Exemplos:

- modelos de fluxo;
- critérios de metas;
- política de ações sensíveis;
- regras de cobrança;
- limites de criticidade;
- parâmetros de escalonamento.

### 22.2 Preferência individual

Preferências de interface e comportamento pessoal deverão permanecer vinculadas ao usuário e não poderão alterar regras de negócio.

### 22.3 Estado temporário da interface

Filtros, destaques, reorganizações críticas e layouts temporários poderão ser persistidos apenas quando necessário à continuidade da sessão ou missão.

Eles não deverão ser confundidos com estado oficial da operação.

### 22.4 Versão e vigência

Políticas e modelos que afetem operações futuras deverão possuir versão ou vigência suficiente para preservar qual regra foi aplicada a cada registro histórico.

---

## 23. Conhecimento e memória

### 23.1 Separação do modelo de linguagem

Conhecimento, procedimentos, memória e aprendizado não deverão ser armazenados exclusivamente no modelo de linguagem.

### 23.2 Tipos conceituais

A persistência deverá permitir distinguir, no mínimo:

- conhecimento oficial do Mheibos;
- conhecimento oficial da organização;
- prática recomendada;
- solução emergente;
- hipótese;
- aprendizado aguardando validação;
- preferência individual;
- memória contextual temporária.

### 23.3 Proveniência

Conhecimento aprendido ou ensinado deverá preservar sua origem, evidências, autor, estado de validação e histórico de aprovação.

### 23.4 Privacidade

Memória individual e notas pessoais deverão possuir escopo explícito e não poderão tornar-se conhecimento compartilhado sem autorização ou governança correspondente.

A especificação completa pertence ao RFC-0011 e ao RFC-0016.

---

## 24. Dados globais, locais e temporários

### 24.1 Estado global

O estado global é a visão oficial consolidada pela Central.

Entidades sincronizadas e aceitas pela Central passam a integrar esse estado.

### 24.2 Estado local persistente

Cada Cliente poderá manter dados locais necessários a:

- cache autorizado;
- sessão offline;
- credencial offline protegida;
- novos pedidos locais;
- operações pendentes;
- preferências da estação;
- recuperação após falha.

### 24.3 Estado local exclusivo

Um Pedido criado offline permanecerá local e exclusivo da estação de origem até a sincronização bem-sucedida.

Seu identificador técnico e visível não poderão ser alterados silenciosamente ao entrar no estado global.

### 24.4 Estado temporário

Informações puramente temporárias, como seleção atual, animação, destaque visual transitório ou rascunho não salvo, não devem ser promovidas automaticamente a dado oficial.

### 24.5 Marcação de origem

Registros criados ou alterados localmente deverão preservar origem suficiente para sincronização, rastreabilidade e diagnóstico.

As regras detalhadas pertencem ao RFC-0008.

---

## 25. Ciclo de vida dos registros

### 25.1 Estados de existência

Entidades persistentes poderão possuir situações equivalentes a:

- ativa;
- concluída;
- cancelada;
- desativada;
- arquivada;
- removida do uso normal;
- substituída.

Essas situações não devem ser usadas indistintamente.

### 25.2 Exclusão lógica

A regra padrão para entidades com relevância comercial, operacional, financeira ou de segurança será exclusão lógica ou encerramento explícito, preservando histórico e relações.

### 25.3 Exclusão física excepcional

A destruição física somente poderá ocorrer quando:

- não violar auditoria ou obrigação legal;
- não quebrar relações históricas;
- estiver prevista por política específica;
- possuir autorização correspondente;
- deixar registro suficiente do procedimento, quando aplicável.

### 25.4 Referências a entidades desativadas

Relacionamentos históricos deverão continuar válidos mesmo quando a entidade relacionada estiver desativada ou arquivada.

### 25.5 Retenção

Prazos de retenção, anonimização e descarte legal serão definidos em política posterior, sem contrariar a obrigação de rastreabilidade do sistema.

---

## 26. Invariantes do modelo

Toda implementação deverá preservar as seguintes invariantes:

1. cada entidade persistente possui identidade técnica estável;
2. identificadores técnicos não são reutilizados;
3. o identificador visível do Pedido é globalmente não ambíguo dentro da instalação;
4. código de origem comercial utilizado não é transferido a outro usuário;
5. um usuário possui exatamente um Perfil principal;
6. autoria comercial não é sobrescrita por responsabilidade operacional;
7. mudanças de responsável preservam histórico;
8. Pedido e Processo são entidades distintas;
9. um Processo confirmado preserva seu fluxo instanciado;
10. alterar um modelo de fluxo não reescreve processos históricos;
11. estados comercial, operacional e financeiro não são comprimidos obrigatoriamente em um único campo;
12. pagamentos anteriores não são destruídos quando o valor do Pedido muda;
13. exclusões relevantes não apagam silenciosamente o conteúdo anterior;
14. dados temporários de interface não se tornam estado global sem operação explícita;
15. a IA não grava estado oficial sem passar pelos contratos e validações do Mheibos;
16. Clientes não tratam cache local como autoridade global;
17. um Pedido offline permanece vinculado à estação e ao usuário de origem até a sincronização;
18. após sincronização, origem não significa propriedade exclusiva;
19. referências de arquivos podem sobreviver à indisponibilidade física do arquivo;
20. entidades desativadas continuam referenciáveis pelo histórico.

---

## 27. Agregados e fronteiras transacionais conceituais

Esta RFC não impõe uma tecnologia de Domain-Driven Design, mas estabelece fronteiras conceituais para evitar alterações parciais incoerentes.

### 27.1 Agregado Pedido

Uma operação comercial que altere Pedido, Itens, valores e estado financeiro deverá preservar consistência entre esses elementos.

### 27.2 Agregado Processo

Uma operação que altere fluxo instanciado, etapas, dependências e estado operacional deverá preservar consistência do Processo.

### 27.3 Agregado Missão

Participação, tarefas, progresso e estado da Missão deverão permanecer coerentes, sem transformar referências externas em cópias divergentes.

### 27.4 Agregado Pendência

Responsável, vencimento, escalonamento e encerramento deverão descrever uma única obrigação rastreável.

### 27.5 Relações entre agregados

Relações entre Pedido, Processo, Missão e Pendência deverão ocorrer por identidades e contratos explícitos, evitando escrita indiscriminada entre componentes.

A implementação física dessas fronteiras será definida junto ao banco e aos casos de uso.

---

## 28. Consistência e concorrência

### 28.1 Consistência central

Quando a Central estiver disponível, ela será responsável por validar e persistir alterações do estado global.

### 28.2 Bloqueio de edição

O bloqueio temporário de edição deverá ser representado como estado de coordenação, não como propriedade permanente da entidade.

O bloqueio deverá possuir, no mínimo:

- entidade bloqueada;
- usuário;
- estação ou sessão;
- início;
- expiração;
- estado de liberação.

### 28.3 Dados derivados

Totais, saldos, progresso e indicadores derivados deverão possuir fonte de cálculo identificável.

Quando forem materializados por desempenho, a implementação deverá impedir que se tornem uma segunda verdade divergente.

### 28.4 Operações compostas

Alterações que afetem múltiplas entidades deverão ser tratadas como uma unidade lógica ou produzir mecanismos claros de compensação e recuperação.

---

## 29. Requisitos de qualidade dos dados

### 29.1 Completude contextual

Um registro deverá possuir contexto suficiente para ser compreendido sem depender exclusivamente da memória humana.

### 29.2 Rastreabilidade

Dados importantes deverão indicar origem, autoria e relação com a operação correspondente.

### 29.3 Não ambiguidade

Campos genéricos e sobrecarregados deverão ser evitados quando representarem conceitos diferentes.

### 29.4 Evolução de esquema

Mudanças futuras no esquema deverão ser versionadas e migráveis, preservando os dados oficiais existentes.

### 29.5 Integridade referencial

Relações essenciais não deverão ser quebradas por exclusão, desativação ou atualização de nomes.

### 29.6 Legibilidade operacional

O modelo técnico deverá permitir gerar identificações e explicações compreensíveis ao usuário, sem expor identificadores internos como única forma de referência.

---

## 30. Fronteiras com os demais RFCs

| RFC | Responsabilidade relacionada |
|---|---|
| RFC-0002 | significado de Processo, Objetivo, Fluxo, Estado e Evidência |
| RFC-0003 | localização da persistência e separação entre Central e Clientes |
| RFC-0004 | uso cognitivo dos dados e limites da IA |
| RFC-0006 | formato de eventos, evidências, auditoria e histórico imutável |
| RFC-0007 | autenticação, perfis, permissões, ações sensíveis e bloqueios |
| RFC-0008 | armazenamento local, operação offline e sincronização |
| RFC-0009 | estado temporário de interface e intervenções visuais |
| RFC-0010 | ciclo de vida completo de Missões e Teamwork |
| RFC-0011 | conhecimento, memória e aprendizado |
| RFC-0012 | pendências, lembretes e escalonamento |
| RFC-0013 | regras de pedidos, metas, pagamentos, saldos e cobranças |
| RFC-0014 | arquivos, WhatsApp, webhooks e integrações |
| RFC-0015 | indicadores, agregações analíticas e simulações |
| RFC-0016 | aprovação, proveniência e governança do conhecimento da IA |

Esta RFC define como os conceitos podem ser representados e relacionados. Ela não substitui as regras de comportamento pertencentes aos documentos especializados.

---

## 31. Consequências da decisão

### 31.1 Benefícios

- separação clara entre venda e execução;
- preservação de autoria e responsabilidade;
- suporte a fluxos adaptáveis sem perder histórico;
- estados financeiros e operacionais não ambíguos;
- base consistente para eventos, offline e auditoria;
- substituição futura do modelo de IA sem perda de dados;
- suporte a missões, pendências e conhecimento sem misturar conceitos;
- possibilidade de evolução para nuvem e aplicações especializadas.

### 31.2 Custos

- maior quantidade de entidades e relações;
- necessidade de migrações cuidadosas;
- consultas analíticas mais complexas;
- disciplina para não colocar regras de negócio em campos genéricos;
- necessidade de distinguir cópia histórica de cadastro atual;
- exigência de integrar estado atual e histórico de eventos.

### 31.3 Riscos

- transformar Pedido em uma entidade excessivamente grande;
- duplicar estados entre Pedido, Processo e Etapa;
- usar texto livre onde deveria existir relação explícita;
- permitir exclusão física de dados auditáveis;
- usar o cache do Cliente como fonte oficial;
- misturar preferências de interface com regras organizacionais;
- armazenar conhecimento apenas no modelo de IA;
- materializar indicadores sem estratégia de consistência;
- copiar dados entre Missão e Processo, criando versões divergentes.

---

## 32. Critérios de conformidade

Uma implementação estará em conformidade com esta RFC somente se:

1. Pedido e Processo forem entidades distintas e relacionadas;
2. cada entidade persistente relevante possuir identificador técnico estável;
3. o número visível do Pedido não for usado como única identidade interna;
4. autoria comercial, responsabilidade e conclusão puderem ser representadas separadamente;
5. o fluxo confirmado de um Processo permanecer preservado independentemente de mudanças no modelo padrão;
6. estados comercial, operacional e financeiro puderem coexistir sem ambiguidade;
7. pagamentos forem registros próprios e preservados após alterações do total;
8. exclusões relevantes não destruírem silenciosamente o histórico;
9. usuários desativados permanecerem referenciáveis em registros antigos;
10. referências de arquivos não exigirem armazenamento binário dentro do Mheibos;
11. dados temporários da interface forem separados do estado oficial;
12. dados locais offline forem distinguíveis do estado global;
13. a IA não for utilizada como armazenamento oficial;
14. configurações organizacionais forem separadas de preferências individuais;
15. relações essenciais forem explícitas e preservadas;
16. mudanças de esquema puderem ser migradas sem abandonar os registros existentes.

---

## 33. Decisões adiadas

As seguintes decisões serão tomadas durante RFCs especializados ou implementação:

- banco de dados relacional, documental ou híbrido;
- mecanismo de identificação técnica;
- convenção final de nomes;
- normalização física;
- estratégia de índices;
- materialização de estados derivados;
- formato de datas e fusos na persistência;
- precisão e armazenamento monetário;
- versionamento de registros;
- estratégia de migrations;
- retenção e anonimização;
- backup e restauração;
- criptografia de campos;
- armazenamento de anexos eventualmente internos;
- modelo de busca textual e vetorial;
- formato físico de snapshots e eventos;
- políticas de arquivamento de longo prazo.

Essas escolhas deverão respeitar os princípios, invariantes e fronteiras desta RFC.

---

## 34. Rastreabilidade com o Inventário Oficial

Esta RFC especifica a representação estrutural necessária para implementar decisões distribuídas entre os RFCs proprietários, sem assumir a propriedade de suas regras de negócio.

| Decisões do Inventário | Impacto estrutural nesta RFC |
|---|---|
| INV-007 a INV-013 | Pedido, Processo, Fluxo, Etapa, estados e exceções operacionais |
| INV-015 a INV-018 | Organização, Instalação, Central, Estação e estado global/local |
| INV-024 a INV-029 | vínculos de Evento, Evidência, Auditoria e exclusão lógica |
| INV-030 a INV-040 | Usuário, Perfil, Sessão, permissões efetivas e bloqueio |
| INV-041 a INV-051 | Pedido offline, origem, dados locais e incorporação global |
| INV-059 a INV-061 | preferências individuais e contexto persistente de Missão |
| INV-065 a INV-072 | Missão, participação, tarefa, conversa e nota |
| INV-073 a INV-084 | conhecimento, memória, proveniência e validação |
| INV-085 a INV-092 | Pendência, lembrete, responsável e escalonamento |
| INV-093 a INV-101 | autoria comercial, pagamentos, saldos e cobrança |
| INV-102 a INV-106 | referências de arquivos e contexto de integração |
| INV-107 a INV-124 | separação entre dados oficiais, sugestões e conhecimento da IA |
| INV-125 a INV-127 | dados derivados, indicadores e simulações não oficiais |

---

## 35. Declaração normativa

O Modelo de Dados do Mheibos deverá representar a empresa por entidades operacionais explícitas, identidades estáveis, relações rastreáveis e estados independentes.

O Pedido será o centro comercial e financeiro. O Processo será o centro da execução. Modelos de fluxo serão reutilizáveis, mas cada Processo preservará sua própria instância confirmada. Autoria, responsabilidade, execução e conclusão serão relações distintas. Alterações, cancelamentos e exclusões relevantes não apagarão silenciosamente o passado.

A Central manterá o estado global oficial. Clientes poderão manter dados locais controlados, sem transformar cache ou estado temporário de interface em fonte da verdade. Arquivos externos serão referenciados em seu contexto operacional. Conhecimento e memória permanecerão fora do modelo de linguagem.

Toda implementação física do banco deverá respeitar estas fronteiras, invariantes e critérios de conformidade.
