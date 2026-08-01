# MHEIBOS INTELLIGENT OPERATING SYSTEM

# RFC-0010 — Missões e Teamwork

**Status:** Draft para aprovação  
**Versão:** 0.1  
**Data:** 30/07/2026  
**Dependências:** RFC-0000, RFC-0001, RFC-0002, RFC-0003, RFC-0004, RFC-0005, RFC-0006, RFC-0007, RFC-0008, RFC-0009  
**Fonte normativa:** Inventário Oficial de Decisões Arquiteturais — INV-065 a INV-072

---

## 1. Resumo

Esta RFC define o modelo de **Missões** e **Teamwork** do Mheibos.

Uma Missão representa um objetivo operacional temporário que exige organização consciente, acompanhamento e continuidade. Ela reúne objetivo, plano, tarefas, prazos, participantes, dependências, progresso, contexto, histórico, conversas, notas, decisões e referências relacionadas.

A Missão não substitui Pedidos, Processos, Etapas ou Pendências. Ela funciona como um workspace persistente que organiza esses elementos em torno de um resultado específico.

Uma missão poderá ser:

- criada voluntariamente por um usuário;
- sugerida pela IA e aceita pelo usuário;
- atribuída formalmente por gerente ou administrador autorizado;
- individual;
- coletiva.

O Teamwork representa a colaboração organizada entre participantes de uma missão coletiva. A IA poderá sugerir distribuição de tarefas, identificar dependências, apresentar carga e progresso e recomendar ajuda entre colegas. Contudo, não poderá impor colaboração informal, transferir tarefas sem consentimento ou transformar métricas operacionais em julgamento pessoal.

Missões espontâneas e missões atribuídas possuem regras diferentes de permanência e saída. Em missões espontâneas, participantes poderão sair voluntariamente. Em missões atribuídas pela gestão, somente a autoridade responsável poderá retirar participantes ou encerrar a obrigação, preservando o direito de justificar, pedir ajuda ou solicitar revisão.

Cada missão possuirá seu próprio ambiente persistente de trabalho, incluindo chat contextual e notas consolidadas. Conversas e notas serão entidades distintas: o chat preservará a comunicação cronológica; as notas preservarão informações consolidadas relevantes à missão.

---

## 2. Objetivo

Esta RFC responde às seguintes perguntas:

- o que é uma Missão no Mheibos;
- quando um objetivo deve ou não se tornar uma missão;
- como missões são criadas, sugeridas, atribuídas, iniciadas, pausadas, retomadas e encerradas;
- como missões individuais e coletivas se diferenciam;
- quando o Teamwork pode ser ativado;
- quais poderes pertencem ao criador, líder, participante, gerente e administrador;
- como participantes entram e saem de uma missão;
- como tarefas são distribuídas e transferidas;
- como a IA pode sugerir colaboração sem impor relações entre colegas;
- como progresso, carga e dependências são apresentados;
- como impedir que métricas sejam usadas como julgamento depreciativo;
- o que compõe o workspace persistente de uma missão;
- como chat e notas se relacionam com a missão;
- como missões se relacionam com Processos, Etapas, Pedidos, Pendências e a Interface Viva;
- quais ações exigem consentimento, autoridade, confirmação ou auditoria.

Esta RFC não define o layout final da interface, o scheduler de lembretes, o modelo completo de conhecimento, o mecanismo de notificações, o algoritmo de recomendação da IA ou a implementação física do armazenamento. Esses temas pertencem a RFCs especializados ou à fase de implementação.

---

## 3. Decisões fundamentais

A arquitetura de Missões e Teamwork adota as seguintes decisões:

1. Missão representa um objetivo operacional temporário.
2. Toda missão deverá possuir objetivo explícito e resultado esperado identificável.
3. Uma missão reunirá plano, tarefas, prazos, contexto, progresso e referências relacionadas.
4. Missões poderão ser individuais ou coletivas.
5. Missões poderão ser criadas pelo usuário, sugeridas pela IA ou atribuídas pela gestão.
6. Sugestão da IA não equivale à criação obrigatória de uma missão.
7. Teamwork somente será ativado por concordância dos participantes ou por autoridade formal de gerente ou administrador.
8. A IA não poderá impor colaboração entre colegas.
9. Participantes poderão sair livremente de missões coletivas espontâneas.
10. Em missões atribuídas, somente a autoridade responsável poderá retirar participantes ou encerrar a obrigação.
11. Participantes de missões atribuídas conservarão o direito de justificar, pedir ajuda ou solicitar revisão.
12. O Teamwork deverá apresentar objetivo, progresso, dependências, tarefas e responsáveis.
13. A IA poderá sugerir distribuição conforme carga, habilidade e disponibilidade.
14. A IA não poderá transferir uma tarefa atribuída sem consentimento do responsável atual ou decisão da autoridade da missão.
15. A ajuda entre colegas deverá ser oferecida, aceita ou formalmente determinada conforme a origem da missão.
16. Métricas deverão descrever processo, risco, atraso, carga e impacto, sem gerar rankings depreciativos ou rótulos pessoais.
17. Cada missão será um workspace persistente.
18. Missões possuirão histórico, conversas, notas, decisões e referências próprias.
19. O chat preservará comunicação cronológica.
20. Notas representarão conteúdo consolidado e separado da conversa.
21. Missões poderão ser pausadas e retomadas com contexto preservado.
22. A conclusão de uma missão deverá registrar resultado, estado final e pendências remanescentes.

---

## 4. Escopo

### 4.1 Incluído

Esta RFC especifica:

- conceito de Missão;
- missão individual;
- missão coletiva;
- Teamwork;
- origem voluntária, sugerida ou administrativa;
- objetivo e resultado esperado;
- plano da missão;
- tarefas e dependências;
- participantes e papéis;
- entrada, aceite, recusa e saída;
- autoridade formal;
- distribuição e transferência de tarefas;
- consentimento entre colegas;
- progresso e estados da missão;
- pausa e retomada;
- workspace persistente;
- chat da missão;
- notas da missão;
- decisões e referências relacionadas;
- atuação da IA;
- limites éticos da comparação de desempenho;
- integração conceitual com Interface Viva, Processos, Pendências, Eventos e Permissões;
- critérios de conformidade.

### 4.2 Fora do escopo

Não são definidos aqui:

- layout visual definitivo do workspace;
- componentes PyQt6 concretos;
- tecnologia de chat em tempo real;
- protocolo de sincronização detalhado;
- notificações e escalonamentos completos;
- política definitiva de retenção das conversas;
- edição colaborativa simultânea de documentos;
- videochamadas ou chamadas de voz;
- mensageria externa;
- remuneração, comissão ou avaliação formal de desempenho;
- algoritmo definitivo de estimativa de carga;
- modelo de machine learning para habilidades;
- calendário corporativo completo;
- base de conhecimento oficial;
- mecanismo físico de busca semântica.

---

## 5. Conceitos fundamentais

### 5.1 Missão

Missão é um workspace operacional persistente criado para alcançar um objetivo temporário.

Ela deverá possuir, conforme aplicável:

- identidade técnica;
- título;
- objetivo;
- resultado esperado;
- origem;
- criador;
- autoridade responsável;
- líder ou responsável principal;
- participantes;
- plano;
- tarefas;
- dependências;
- prazos;
- progresso;
- estado;
- contexto de interface;
- conversas;
- notas;
- decisões;
- referências;
- histórico;
- resultado final.

### 5.2 Objetivo temporário

O objetivo da missão é temporário porque possui condição de encerramento identificável.

Exemplos:

- recuperar pedidos atrasados de uma semana;
- preparar uma campanha específica;
- organizar uma entrega complexa;
- concluir uma revisão de preços;
- resolver um gargalo de produção;
- implantar um novo procedimento;
- preparar uma apresentação;
- executar uma ação coletiva emergencial.

Uma função permanente, como “administrar o financeiro”, não deverá ser representada como missão única indefinida. Ela poderá originar missões específicas e temporárias.

### 5.3 Teamwork

Teamwork é o modo colaborativo de uma missão coletiva.

Ele reúne participantes em torno do mesmo objetivo, preservando:

- responsabilidades individuais;
- dependências;
- consentimento;
- autoridade formal;
- progresso compartilhado;
- comunicação contextual;
- rastreabilidade.

### 5.4 Workspace persistente

Workspace persistente é o conjunto de informações e contexto necessário para interromper e retomar uma missão sem reconstruí-la manualmente.

Ele não é apenas uma tela aberta. É uma entidade persistente que permite recriar a experiência de trabalho.

### 5.5 Participante

Participante é o usuário formalmente vinculado à missão.

A participação deverá registrar:

- usuário;
- papel;
- forma de entrada;
- estado de participação;
- tarefas relacionadas;
- momento de entrada;
- momento e motivo de saída, quando houver;
- autoridade que atribuiu ou removeu, quando aplicável.

### 5.6 Autoridade da missão

Autoridade da missão é o usuário com poder formal para atribuir, alterar composição, retirar participantes ou encerrar obrigações em missões administrativas.

Normalmente será um gerente ou administrador autorizado.

### 5.7 Líder ou responsável principal

O líder coordena o objetivo e o plano da missão, mas não recebe automaticamente poderes administrativos globais.

O líder poderá ser:

- o criador da missão espontânea;
- um participante escolhido pelo grupo;
- uma pessoa designada pela gestão;
- o próprio gerente responsável.

### 5.8 Tarefa da missão

Tarefa é uma unidade de trabalho necessária ao objetivo da missão.

Ela poderá:

- representar trabalho exclusivo da missão;
- apontar para uma Etapa já existente;
- agrupar atividades relacionadas;
- depender de outra tarefa;
- possuir responsável, prazo e critério de conclusão.

Uma tarefa não deverá duplicar silenciosamente um Processo ou Etapa oficial quando funcionar apenas como visão organizada deles.

### 5.9 Conversa

Conversa é a comunicação cronológica vinculada à missão.

Ela preserva mensagens, autoria, momento e contexto.

### 5.10 Nota

Nota é conteúdo consolidado que deve permanecer destacado da conversa comum.

Exemplos:

- decisão tomada;
- orientação importante;
- resumo de reunião;
- risco conhecido;
- referência operacional;
- aprendizado temporário da missão;
- informação que precisa ser localizada rapidamente.

### 5.11 Decisão da missão

Decisão é um registro explícito de escolha relevante tomada durante a missão.

Ela deverá preservar, conforme aplicável:

- questão analisada;
- decisão tomada;
- autor ou aprovador;
- momento;
- justificativa;
- impacto;
- tarefas afetadas;
- referências utilizadas.

---

## 6. Relação entre Missão e entidades operacionais

### 6.1 Missão não substitui Processo

O Processo representa a execução oficial de um objetivo operacional segundo fluxos, etapas, estados e regras.

A Missão organiza trabalho em torno de um objetivo temporário e poderá reunir vários processos.

### 6.2 Missão não substitui Pedido

O Pedido continua sendo a entidade comercial e financeira central.

Uma missão poderá estar relacionada a um ou vários pedidos, mas não deverá duplicar seus dados oficiais.

### 6.3 Missão não substitui Pendência

A Pendência representa obrigação não encerrada que requer acompanhamento e decisão consciente.

Uma missão poderá conter ou tratar pendências. Encerrar a missão não deverá eliminar automaticamente pendências ainda abertas.

### 6.4 Missão não substitui a Interface Viva

A RFC-0009 define como a interface focada é montada, pausada e restaurada.

Esta RFC define a entidade persistente, seus participantes, tarefas, colaboração e histórico.

### 6.5 Referência em vez de duplicação

Sempre que a missão utilizar entidade já existente, deverá preferir referência explícita.

Exemplo:

```text
Missão: Recuperar pedidos atrasados
├── Referência ao Pedido #J324
├── Referência ao Processo de Produção #P991
├── Referência à Etapa "Impressão"
└── Tarefa própria: Revisar prioridades com a equipe
```

---

## 7. Tipos de missão

### 7.1 Missão individual voluntária

Criada pelo próprio usuário para organizar um objetivo pessoal de trabalho.

Características:

- participação individual;
- início voluntário;
- pausa e encerramento pelo próprio usuário;
- sem obrigação imposta a terceiros;
- poderá receber sugestões da IA.

### 7.2 Missão individual atribuída

Atribuída formalmente por gerente ou administrador autorizado.

Características:

- possui autoridade responsável;
- o usuário não poderá simplesmente apagar a obrigação;
- poderá justificar, pedir ajuda ou solicitar revisão;
- conclusão ou cancelamento dependerá das regras da atribuição.

### 7.3 Missão coletiva espontânea

Criada por usuários que concordam em colaborar.

Características:

- participação depende de aceite;
- participantes poderão sair voluntariamente;
- mudanças de responsabilidade exigem consentimento;
- o grupo poderá definir líder e regras internas compatíveis com a plataforma.

### 7.4 Missão coletiva atribuída

Criada ou formalmente atribuída por gerente ou administrador.

Características:

- participantes podem ser designados conforme autoridade e permissões;
- somente a autoridade responsável poderá retirar participantes ou encerrar a obrigação;
- participantes poderão pedir revisão, ajuda ou justificar impedimentos;
- transferência de tarefas poderá ser decidida pela autoridade quando necessária.

### 7.5 Missão sugerida pela IA

A IA poderá preparar uma proposta de missão contendo:

- objetivo;
- justificativa;
- participantes sugeridos;
- plano inicial;
- tarefas;
- prazos;
- dependências;
- impacto esperado.

A proposta somente se tornará missão ativa após:

- aceite do usuário, quando individual;
- aceite dos participantes, quando coletiva espontânea;
- confirmação de autoridade, quando administrativa.

---

## 8. Critérios para criação de uma missão

### 8.1 Condição mínima

Uma missão deverá existir quando houver um objetivo suficientemente definido para justificar:

- continuidade entre sessões;
- organização de tarefas;
- acompanhamento de progresso;
- coordenação entre pessoas;
- preservação de contexto;
- decisões relacionadas.

### 8.2 Situações que não exigem missão

Não será necessário criar missão para:

- ação simples e imediata;
- consulta isolada;
- tarefa única sem necessidade de continuidade;
- notificação informativa;
- filtro temporário sem objetivo persistente;
- conversa comum sem plano ou resultado esperado.

### 8.3 Evitar inflação de missões

O sistema deverá evitar transformar toda pequena atividade em missão.

A criação excessiva produziria:

- fragmentação;
- sobrecarga;
- perda de prioridade;
- duplicação de tarefas;
- abandono de workspaces.

### 8.4 Sugestão proporcional

A IA deverá sugerir uma missão quando a organização persistente oferecer benefício claro.

Ela deverá explicar por que um simples alerta ou tarefa isolada não é suficiente.

---

## 9. Ciclo de vida da missão

### 9.1 Estados conceituais

Uma missão deverá suportar estados equivalentes a:

- proposta;
- aguardando aceite;
- planejada;
- ativa;
- pausada;
- bloqueada;
- em revisão;
- concluída;
- cancelada;
- arquivada.

### 9.2 Proposta

Existe conteúdo inicial, mas a missão ainda não foi aceita ou formalmente atribuída.

### 9.3 Aguardando aceite

Utilizado quando participantes precisam concordar em integrar uma missão espontânea.

### 9.4 Planejada

A missão foi criada, mas o trabalho ainda não começou.

### 9.5 Ativa

Existem atividades em execução ou acompanhamento corrente.

### 9.6 Pausada

O objetivo permanece válido, mas o trabalho está temporariamente suspenso.

Pausar deverá preservar contexto, tarefas, mensagens, notas, progresso e visão focada.

### 9.7 Bloqueada

A missão não pode avançar por uma dependência, impedimento ou decisão pendente.

### 9.8 Em revisão

A missão aguarda validação do resultado, redefinição do plano ou decisão da autoridade.

### 9.9 Concluída

O objetivo foi alcançado ou formalmente aceito como concluído.

### 9.10 Cancelada

A missão foi encerrada sem alcançar integralmente o objetivo.

O cancelamento deverá registrar motivo e autoridade correspondente.

### 9.11 Arquivada

A missão permanece consultável, mas deixa de ocupar a operação corrente.

---

## 10. Criação e ativação

### 10.1 Conteúdo mínimo

Uma missão deverá possuir, no mínimo:

- título;
- objetivo;
- origem;
- criador ou autoridade;
- responsável principal;
- estado;
- critério de conclusão.

### 10.2 Conteúdo recomendado

Quando aplicável:

- descrição do problema;
- resultado esperado;
- prazo;
- participantes;
- plano inicial;
- tarefas;
- dependências;
- referências;
- riscos;
- prioridade.

### 10.3 Criação voluntária

O usuário poderá criar uma missão dentro de suas permissões.

Adicionar outra pessoa exigirá convite e aceite, salvo autoridade formal aplicável.

### 10.4 Criação administrativa

Gerente ou administrador autorizado poderá criar e atribuir missão dentro de seu escopo.

A atribuição deverá produzir evento auditável.

### 10.5 Criação assistida pela IA

A IA poderá preencher uma proposta, mas não deverá:

- inventar autoridade;
- adicionar participantes sem consentimento ou atribuição formal;
- criar obrigação oculta;
- alterar tarefas oficiais sem confirmação;
- iniciar missão coletiva silenciosamente.

---

## 11. Participantes e papéis

### 11.1 Papéis conceituais

Uma missão poderá possuir:

- criador;
- autoridade responsável;
- líder;
- participante;
- colaborador convidado;
- observador autorizado;
- aprovador;
- responsável por tarefa.

### 11.2 Acúmulo de papéis

Um usuário poderá ocupar mais de um papel, desde que as relações permaneçam explícitas.

### 11.3 Participante

Participante contribui diretamente para o objetivo.

### 11.4 Observador

Observador poderá acompanhar informações autorizadas sem receber responsabilidade operacional automática.

### 11.5 Aprovador

Aprovador valida resultados ou decisões conforme regras externas à missão.

### 11.6 Autoridade não presumida

Ser líder da missão não concede automaticamente permissão para:

- alterar perfil;
- acessar dados restritos;
- transferir qualquer processo;
- executar ação sensível;
- impor participação fora de seu escopo.

---

## 12. Entrada, aceite e recusa

### 12.1 Convite espontâneo

Em missão espontânea, o usuário convidado deverá poder:

- aceitar;
- recusar;
- pedir mais informações;
- sugerir ajuste de participação.

### 12.2 Atribuição formal

Em missão atribuída, o participante deverá ser informado de:

- objetivo;
- autoridade responsável;
- papel;
- tarefas iniciais;
- prazo;
- impacto esperado;
- possibilidade de justificar, pedir ajuda ou solicitar revisão.

### 12.3 Recusa de convite

Recusar participação espontânea não deverá gerar punição ou julgamento automático.

### 12.4 Contestação de atribuição

Uma atribuição administrativa não deverá ser silenciosamente recusada pelo sistema, mas o usuário poderá registrar:

- impedimento;
- conflito de prioridade;
- ausência de habilidade;
- indisponibilidade;
- necessidade de apoio;
- solicitação de revisão.

A autoridade deverá avaliar o pedido.

---

## 13. Saída e remoção de participantes

### 13.1 Missões espontâneas

Participantes poderão sair voluntariamente.

Antes da saída, o sistema deverá apresentar:

- tarefas atribuídas;
- dependências afetadas;
- pendências;
- necessidade de transferência;
- impacto no objetivo.

A saída não deverá apagar contribuições anteriores.

### 13.2 Missões atribuídas

O participante não poderá encerrar unilateralmente a obrigação apenas saindo da missão.

Somente a autoridade responsável poderá:

- retirar o participante;
- substituí-lo;
- encerrar sua obrigação;
- cancelar a missão.

### 13.3 Direito de manifestação

Mesmo em missão atribuída, o usuário poderá:

- justificar dificuldade;
- pedir ajuda;
- solicitar revisão;
- informar conflito;
- apresentar risco;
- propor substituição.

### 13.4 Remoção pela autoridade

A remoção deverá preservar:

- autor da decisão;
- participante removido;
- momento;
- motivo, quando aplicável;
- tarefas afetadas;
- destino das responsabilidades;
- impacto no prazo.

---

## 14. Plano da missão

### 14.1 Estrutura

O plano poderá conter:

- objetivo;
- marcos;
- tarefas;
- ordem sugerida;
- prazos;
- responsáveis;
- dependências;
- riscos;
- critérios de conclusão;
- pontos de revisão.

### 14.2 Plano inicial e evolução

O plano poderá começar incompleto e evoluir durante a missão.

Mudanças relevantes deverão preservar histórico.

### 14.3 Plano sugerido pela IA

A IA poderá sugerir:

- decomposição do objetivo;
- ordem de execução;
- responsáveis possíveis;
- prazos;
- dependências;
- plano alternativo.

A sugestão deverá ser validada por pessoas autorizadas antes de produzir atribuições persistentes.

### 14.4 Plano e processos oficiais

Quando uma tarefa corresponde a processo ou etapa oficial, o plano deverá referenciar esse elemento em vez de criar estado paralelo contraditório.

---

## 15. Tarefas

### 15.1 Estrutura mínima

Uma tarefa deverá permitir representar:

- título;
- descrição;
- responsável;
- estado;
- prazo;
- dependências;
- prioridade;
- critério de conclusão;
- referência operacional;
- histórico de atribuição.

### 15.2 Estados conceituais

Uma tarefa poderá estar:

- proposta;
- não iniciada;
- pronta;
- em andamento;
- bloqueada;
- aguardando resposta;
- concluída;
- dispensada;
- cancelada;
- reaberta.

### 15.3 Responsável único e colaboradores

Uma tarefa deverá possuir responsável principal quando exigir ação individual clara.

Ela poderá possuir colaboradores, sem eliminar a responsabilidade principal.

### 15.4 Dependências

A dependência deverá ser explícita quando uma tarefa não puder avançar antes de outra condição.

### 15.5 Conclusão

Concluir uma tarefa deverá registrar:

- executor ou confirmador;
- momento;
- resultado;
- evidência, quando necessária;
- efeitos sobre o progresso;
- desbloqueios produzidos.

---

## 16. Distribuição de tarefas

### 16.1 Critérios de sugestão

A IA poderá sugerir distribuição considerando:

- carga atual;
- disponibilidade conhecida;
- habilidade relacionada;
- responsabilidades existentes;
- dependências;
- prazo;
- contexto da missão;
- permissões.

### 16.2 Sugestão não é atribuição

Em missão espontânea, a distribuição sugerida dependerá de aceite dos participantes envolvidos.

Em missão atribuída, a autoridade poderá confirmar a distribuição dentro de seu escopo.

### 16.3 Transparência

A sugestão deverá explicar os fatores principais utilizados.

Ela não deverá afirmar que uma pessoa é “melhor” ou “pior” de forma genérica.

### 16.4 Limites

A IA não deverá:

- atribuir tarefa a usuário sem acesso necessário;
- ignorar impedimento declarado;
- expor dados privados para justificar distribuição;
- usar diagnóstico pessoal;
- criar competição depreciativa;
- transferir responsabilidade silenciosamente.

---

## 17. Transferência e compartilhamento de tarefas

### 17.1 Regra geral

Uma tarefa já atribuída não poderá ser transferida ou compartilhada sem:

- aceite do responsável atual; ou
- decisão da autoridade da missão.

### 17.2 Oferta de ajuda

Quando um participante concluir sua parte ou possuir disponibilidade, a IA poderá sugerir:

> “Você pode oferecer ajuda a esta tarefa.”

A oferta não modifica a responsabilidade até ser aceita.

### 17.3 Aceite do responsável

O responsável poderá:

- aceitar colaboração;
- transferir integralmente, quando permitido;
- compartilhar uma parte;
- recusar;
- pedir outro tipo de apoio.

### 17.4 Decisão administrativa

Em missão atribuída, a autoridade poderá redistribuir tarefas quando necessário.

A decisão deverá ser explícita e auditável.

### 17.5 Preservação histórica

A transferência deverá registrar:

- responsável anterior;
- novo responsável;
- motivo ou contexto;
- autor da decisão;
- momento;
- estado da tarefa;
- trabalho já realizado.

---

## 18. Teamwork

### 18.1 Finalidade

O Teamwork deverá tornar visível a contribuição coordenada sem apagar responsabilidades individuais.

### 18.2 Visão compartilhada

Participantes autorizados deverão poder consultar:

- objetivo coletivo;
- progresso;
- tarefas;
- responsáveis;
- dependências;
- bloqueios;
- marcos;
- decisões;
- conversas;
- notas;
- referências.

### 18.3 Limites de visibilidade

Participar de uma missão não concede acesso automático a todos os dados vinculados.

Cada referência deverá respeitar as permissões normais do usuário.

### 18.4 Coordenação

O sistema poderá destacar:

- tarefas que bloqueiam outras;
- necessidade de decisão;
- sobrecarga aparente;
- capacidade disponível;
- risco de prazo;
- oportunidade de ajuda.

### 18.5 Colaboração não coercitiva

Fora da autoridade formal, o sistema deverá apresentar colaboração como convite, não como imposição.

---

## 19. Progresso

### 19.1 Natureza

O progresso deverá refletir o avanço em direção ao objetivo, não apenas a quantidade bruta de tarefas concluídas.

### 19.2 Composição

O progresso poderá considerar:

- tarefas concluídas;
- peso ou relevância;
- marcos;
- dependências;
- processos relacionados;
- critérios de resultado;
- bloqueios;
- prazo.

### 19.3 Progresso quantitativo e qualitativo

Uma missão poderá apresentar:

- percentual estimado;
- marcos atingidos;
- estado narrativo;
- riscos;
- condições pendentes.

### 19.4 Evitar falsa precisão

Quando o progresso não puder ser calculado objetivamente, o sistema deverá apresentar estimativa ou estado descritivo, sem inventar percentual preciso.

### 19.5 Progresso individual

A visualização de contribuição individual deverá ser usada para coordenação e assistência, não para exposição depreciativa.

---

## 20. Métricas, dignidade e julgamento pessoal

### 20.1 Processo antes da pessoa

A comunicação deverá priorizar:

- risco;
- atraso;
- carga;
- dependência;
- impacto;
- necessidade de apoio.

### 20.2 Proibições

O Mheibos não deverá:

- criar ranking público depreciativo;
- rotular alguém como improdutivo;
- usar métricas isoladas como julgamento de caráter;
- comparar colegas de forma humilhante;
- expor dificuldades pessoais sem necessidade;
- converter estimativas em avaliação formal automática.

### 20.3 Exemplos adequados

> “A tarefa de aprovação bloqueia três entregas e precisa de decisão até 15h.”

> “A carga atual de Ana excede a capacidade estimada para o prazo. Há duas tarefas que podem receber apoio.”

### 20.4 Exemplos inadequados

> “Ana é a pessoa menos produtiva da equipe.”

> “Carlos está atrapalhando o grupo.”

### 20.5 Contexto gerencial

Gerentes autorizados poderão consultar responsabilidades e resultados necessários à coordenação, mas a IA deverá continuar apresentando fatos, contexto e incerteza.

---

## 21. Workspace persistente

### 21.1 Conteúdo

O workspace da missão deverá reunir:

- objetivo;
- plano;
- participantes;
- tarefas;
- progresso;
- prazos;
- dependências;
- histórico;
- conversas;
- notas;
- decisões;
- referências;
- contexto de interface necessário à retomada.

### 21.2 Persistência

Fechar a aplicação, trocar de módulo ou pausar a missão não deverá apagar o workspace.

### 21.3 Retomada

Ao retomar, o sistema deverá poder reconstruir:

- visão focada;
- posição lógica de trabalho;
- tarefas prioritárias;
- atualizações ocorridas;
- mensagens não vistas;
- bloqueios atuais;
- próximos passos.

### 21.4 Separação entre estado oficial e estado visual

O workspace poderá preservar filtros, agrupamentos e seleções úteis, mas esses dados não deverão ser confundidos com regras globais ou estado oficial da operação.

### 21.5 Arquivamento

Missões concluídas ou canceladas poderão ser arquivadas, preservando histórico e referências autorizadas.

---

## 22. Chat da missão

### 22.1 Finalidade

O chat deverá concentrar comunicação diretamente relacionada ao objetivo.

### 22.2 Estrutura

Cada mensagem deverá preservar, conforme aplicável:

- autor;
- momento;
- conteúdo;
- resposta a outra mensagem;
- referência a tarefa, decisão ou entidade;
- edição ou remoção lógica;
- visibilidade.

### 22.3 Chat não substitui decisão formal

Uma decisão importante discutida no chat deverá poder ser promovida a registro de decisão ou nota consolidada.

### 22.4 Chat não concede permissão

Uma referência compartilhada no chat não poderá revelar conteúdo que o destinatário não possa acessar.

### 22.5 Mensagens da IA

A IA poderá participar para:

- resumir;
- esclarecer contexto;
- apontar dependências;
- propor plano;
- identificar decisão pendente;
- preparar atualização.

Ela deverá ser claramente identificada e não deverá se passar por participante humano.

---

## 23. Notas da missão

### 23.1 Separação do chat

Notas não serão apenas mensagens fixadas.

Elas representarão conteúdo consolidado e localizável.

### 23.2 Tipos possíveis

Uma nota poderá representar:

- resumo;
- decisão;
- orientação;
- risco;
- hipótese;
- informação externa;
- checklist;
- referência;
- aprendizado temporário.

### 23.3 Autoria e edição

Notas deverão preservar autoria, momento e histórico de alterações relevantes.

### 23.4 Permissões

A criação, edição e visibilidade das notas deverão respeitar permissões da missão e dos dados referenciados.

### 23.5 Conhecimento oficial

Uma nota da missão não se torna automaticamente conhecimento oficial permanente da empresa.

A promoção para a base de conhecimento pertence à RFC-0011 e à governança correspondente.

---

## 24. Decisões da missão

### 24.1 Registro explícito

Decisões relevantes deverão poder ser registradas fora do fluxo informal do chat.

### 24.2 Conteúdo mínimo

Uma decisão deverá conter:

- descrição;
- contexto;
- responsável ou aprovador;
- momento;
- impacto;
- referências;
- tarefas afetadas.

### 24.3 Alteração de decisão

Uma decisão substituída não deverá ser apagada. Uma nova decisão deverá referenciar a anterior.

### 24.4 Autoridade

Registrar uma decisão no workspace não concede autoridade para alterar dados ou políticas fora das permissões normais.

---

## 25. Pausa e retomada

### 25.1 Pausa voluntária

Em missões voluntárias, o usuário ou líder autorizado poderá pausar o trabalho.

### 25.2 Pausa administrativa

Missões atribuídas poderão ser pausadas pela autoridade responsável ou conforme regras definidas.

### 25.3 Efeitos

Pausar não deverá:

- apagar tarefas;
- encerrar responsabilidades;
- concluir pendências;
- remover prazos silenciosamente;
- esconder riscos críticos.

### 25.4 Retomada

A retomada deverá apresentar:

- tempo de pausa;
- mudanças ocorridas;
- tarefas vencidas;
- novos bloqueios;
- mensagens e decisões;
- plano atualizado, quando aplicável.

---

## 26. Bloqueios e pedidos de ajuda

### 26.1 Registro de bloqueio

O participante poderá registrar que uma tarefa ou missão está bloqueada.

### 26.2 Conteúdo

O bloqueio deverá indicar:

- objeto afetado;
- motivo;
- dependência;
- impacto;
- ajuda necessária;
- urgência.

### 26.3 Pedido de ajuda

Pedir ajuda não transfere automaticamente a tarefa.

O pedido poderá gerar:

- convite a colaborador;
- sugestão da IA;
- escalonamento à autoridade;
- revisão do prazo;
- redistribuição autorizada.

### 26.4 Proteção humana

O sistema não deverá tratar pedido de ajuda como fracasso ou infração por padrão.

---

## 27. Atuação da IA

### 27.1 Capacidades

A IA poderá:

- sugerir criação de missão;
- preparar objetivo e plano;
- decompor trabalho;
- sugerir tarefas;
- identificar dependências;
- resumir progresso;
- detectar bloqueios;
- sugerir distribuição;
- recomendar oferta de ajuda;
- preparar atualização coletiva;
- resumir chat;
- extrair notas propostas;
- apontar decisões pendentes;
- sugerir revisão do plano.

### 27.2 Limites

A IA não poderá:

- impor missão coletiva espontânea;
- adicionar participantes sem consentimento ou autoridade;
- remover participantes por conta própria;
- transferir tarefa sem aceite ou decisão formal;
- criar obrigação oculta;
- encerrar missão atribuída;
- alterar permissões;
- expor dados privados;
- transformar métricas em julgamento pessoal;
- declarar conclusão oficial sem validação.

### 27.3 Explicabilidade

Sugestões relevantes deverão indicar:

- motivo;
- fatos utilizados;
- impacto esperado;
- participantes afetados;
- necessidade de aceite;
- incertezas.

### 27.4 Assistência contextual

A IA deverá adaptar sua atuação conforme:

- papel do usuário;
- estado da missão;
- tarefas sob responsabilidade;
- permissões;
- urgência;
- progresso;
- bloqueios.

---

## 28. Permissões e segurança

### 28.1 Herança das permissões

A missão não cria um espaço fora das regras da plataforma.

Todo acesso deverá respeitar a RFC-0007.

### 28.2 Ações protegidas

Poderão exigir permissão específica:

- criar missão administrativa;
- atribuir participante;
- remover participante;
- alterar autoridade;
- redistribuir tarefa sem aceite;
- cancelar missão atribuída;
- visualizar dados restritos;
- exportar conteúdo;
- promover nota a conhecimento oficial.

### 28.3 Ações sensíveis

Ações classificadas como sensíveis deverão exigir reautenticação e auditoria conforme política.

### 28.4 Menor exposição

O workspace deverá mostrar somente o conteúdo necessário e autorizado a cada participante.

Dois participantes da mesma missão poderão visualizar conjuntos diferentes de informações.

---

## 29. Eventos e auditoria

### 29.1 Eventos relevantes

Deverão gerar eventos, conforme aplicável:

- missão criada;
- proposta aceita ou recusada;
- missão atribuída;
- participante convidado;
- convite aceito ou recusado;
- participante removido;
- saída voluntária;
- tarefa criada;
- tarefa atribuída;
- transferência realizada;
- tarefa concluída;
- missão pausada ou retomada;
- missão concluída ou cancelada;
- decisão registrada;
- nota relevante alterada;
- autoridade modificada.

### 29.2 Preservação histórica

Alterações não deverão reescrever silenciosamente:

- participantes anteriores;
- responsáveis anteriores;
- tarefas concluídas;
- mensagens;
- decisões;
- planos substituídos;
- motivos de cancelamento.

### 29.3 Auditoria e conversa

Nem toda mensagem de chat precisa ser evento de domínio, mas sua autoria e cronologia deverão ser preservadas conforme a política de dados.

### 29.4 Origem da ação

Eventos deverão distinguir:

- ação humana;
- ação administrativa;
- sugestão da IA aceita;
- consequência automática autorizada.

---

## 30. Operação offline

### 30.1 Regra da primeira versão

Missões globais existentes não deverão ser alteradas offline, salvo futura decisão normativa específica.

### 30.2 Consulta

O Cliente poderá apresentar a última visão sincronizada autorizada, indicando que pode estar desatualizada.

### 30.3 Interface focada local

A visualização local da missão poderá ser restaurada a partir do cache, sem representar atualização global.

### 30.4 Ações locais

Rascunhos de notas ou mensagens poderão ser preservados localmente quando a implementação permitir, mas não deverão aparecer como publicados antes da confirmação da Central.

### 30.5 Evolução futura

Uma ampliação do suporte offline para missões exigirá regras próprias de conflito, autoria, ordenação e sincronização.

---

## 31. Notificações e continuidade

### 31.1 Relação com RFC-0012

Lembretes, escalonamentos, cadência de notificações e briefing diário pertencem à RFC-0012.

### 31.2 Gatilhos possíveis

Uma missão poderá produzir condições para notificação, como:

- convite recebido;
- atribuição;
- prazo próximo;
- tarefa desbloqueada;
- bloqueio declarado;
- pedido de ajuda;
- decisão pendente;
- mudança relevante;
- conclusão de dependência.

### 31.3 Evitar ruído

O Teamwork não deverá gerar uma notificação para cada pequena mudança quando um resumo contextual for suficiente.

---

## 32. Conclusão e encerramento

### 32.1 Critério de conclusão

A missão deverá possuir critério identificável para determinar se o objetivo foi alcançado.

### 32.2 Validação

A conclusão poderá depender de:

- confirmação do responsável;
- aceite do líder;
- aprovação da autoridade;
- conclusão de tarefas obrigatórias;
- resultado de processo relacionado;
- evidência exigida.

### 32.3 Conteúdo do encerramento

Ao concluir, o sistema deverá poder registrar:

- resultado alcançado;
- tarefas concluídas;
- tarefas dispensadas;
- pendências remanescentes;
- decisões finais;
- responsáveis;
- prazo real;
- referências;
- resumo.

### 32.4 Pendências remanescentes

Encerrar a missão não deverá apagar obrigações ainda abertas.

Elas deverão ser:

- concluídas;
- canceladas com autoridade;
- transferidas;
- transformadas em pendências;
- incorporadas a outro processo ou missão.

### 32.5 Cancelamento

O cancelamento deverá registrar:

- motivo;
- autoridade;
- impacto;
- destino das tarefas;
- pendências resultantes.

---

## 33. Arquivamento e consulta histórica

### 33.1 Arquivamento

Missões concluídas ou canceladas poderão ser removidas da visão principal e mantidas em arquivo.

### 33.2 Consulta

Usuários autorizados deverão poder consultar:

- objetivo;
- participantes;
- plano;
- tarefas;
- progresso histórico;
- conversas;
- notas;
- decisões;
- resultado.

### 33.3 Reutilização

Uma missão antiga poderá servir de referência ou modelo para nova missão.

A nova missão deverá possuir identidade própria e não reabrir silenciosamente o histórico anterior.

---

## 34. Fluxos principais

### 34.1 Missão individual sugerida pela IA

```text
IA detecta objetivo relevante
        ↓
Prepara proposta de missão
        ↓
Usuário revisa objetivo, plano e tarefas
        ↓
Usuário aceita, edita ou rejeita
        ↓
Missão é criada
        ↓
Interface focada é montada
        ↓
Usuário executa, pausa e retoma
        ↓
Resultado é validado e registrado
```

### 34.2 Missão coletiva espontânea

```text
Usuário cria missão coletiva
        ↓
Convida participantes
        ↓
Cada participante aceita ou recusa
        ↓
Teamwork é ativado
        ↓
Plano e tarefas são acordados
        ↓
Colaboração e progresso são acompanhados
        ↓
Participantes podem sair voluntariamente
        ↓
Objetivo é concluído ou missão é cancelada
```

### 34.3 Missão coletiva atribuída

```text
Gerente ou administrador cria missão
        ↓
Define objetivo, autoridade e participantes
        ↓
Participantes são informados
        ↓
Usuários podem registrar impedimentos ou pedir revisão
        ↓
Autoridade confirma ou ajusta o plano
        ↓
Teamwork acompanha tarefas e dependências
        ↓
Redistribuições são autorizadas
        ↓
Autoridade valida conclusão ou cancelamento
```

### 34.4 Oferta de ajuda

```text
Participante conclui sua tarefa
        ↓
IA identifica tarefa que precisa de apoio
        ↓
Sugere oferta de ajuda
        ↓
Participante oferece ajuda
        ↓
Responsável aceita, ajusta ou recusa
        ↓
Colaboração é registrada sem apagar responsabilidade
```

---

## 35. Requisitos de qualidade

### 35.1 Clareza

O usuário deverá compreender:

- objetivo;
- responsabilidade;
- estado;
- próximos passos;
- autoridade;
- impacto de sair, transferir ou concluir.

### 35.2 Continuidade

A missão deverá sobreviver ao fechamento da interface e permitir retomada consistente.

### 35.3 Baixo ruído

O workspace deverá consolidar informações sem produzir excesso de mensagens e notificações.

### 35.4 Rastreabilidade

Mudanças relevantes de participação, responsabilidade, plano e decisão deverão ser rastreáveis.

### 35.5 Consentimento

Colaboração espontânea deverá depender de aceite real, não de interface manipulativa.

### 35.6 Segurança

Missões não deverão criar atalhos para permissões ou exposição de dados.

### 35.7 Dignidade

Métricas deverão apoiar coordenação e solução, não humilhação ou julgamento pessoal.

### 35.8 Substituibilidade cognitiva

A lógica persistente da missão não deverá depender de um modelo específico de IA.

---

## 36. Riscos arquiteturais

A implementação deverá evitar:

- transformar qualquer tarefa em missão;
- duplicar Processos e Etapas dentro do workspace;
- criar participação coletiva sem consentimento ou autoridade;
- permitir saída silenciosa de missão atribuída;
- permitir transferência de tarefa sem aceite ou decisão formal;
- usar percentual de progresso sem base confiável;
- criar ranking público de produtividade;
- expor dados restritos pelo chat;
- tratar conversa como decisão oficial;
- promover nota a conhecimento permanente automaticamente;
- apagar histórico ao remover participante;
- confundir pausa com cancelamento;
- concluir missão deixando pendências invisíveis;
- permitir que a IA se torne autoridade da missão;
- transformar líder em administrador implícito;
- sobrecarregar o usuário com notificações de cada mudança.

---

## 37. Relação com os demais RFCs

| RFC | Responsabilidade relacionada |
|---|---|
| RFC-0000 | Propósito e participação ativa do Mheibos |
| RFC-0001 | Autonomia humana, dignidade e decisões conscientes |
| RFC-0002 | Processos, objetivos, fluxos e responsabilidades operacionais |
| RFC-0003 | Central, Clientes e componentes da plataforma |
| RFC-0004 | Sugestões, planos, proatividade e limites cognitivos da IA |
| RFC-0005 | Entidades Missão, Participação, Tarefa, Conversa e Nota |
| RFC-0006 | Eventos, histórico, autoria e auditoria |
| RFC-0007 | Identidade, permissões, autoridade e ações sensíveis |
| RFC-0008 | Limites da operação offline |
| RFC-0009 | Interface focada, pausa e retomada visual |
| RFC-0011 | Conhecimento, memória e promoção de notas |
| RFC-0012 | Lembretes, notificações e escalonamentos |
| RFC-0015 | Indicadores e análises de progresso |
| RFC-0016 | Governança e proteção humana da IA |

---

## 38. Consequências da decisão

### 38.1 Benefícios

- objetivos temporários ganham continuidade;
- colaboração deixa de depender de conversas dispersas;
- responsabilidades e dependências ficam visíveis;
- a IA pode apoiar planejamento sem impor relações;
- missões podem ser pausadas e retomadas;
- chat, notas e decisões permanecem contextualizados;
- progresso pode ser acompanhado sem apagar a responsabilidade individual;
- a gestão pode atribuir trabalho formalmente;
- participantes conservam canais de ajuda e revisão;
- conhecimento temporário não se mistura automaticamente com conhecimento oficial.

### 38.2 Custos

- exige modelo persistente próprio;
- aumenta a quantidade de estados e relações;
- requer controle fino de permissões;
- exige cuidado para não duplicar processos;
- requer histórico de participação e transferência;
- chat e notas aumentam necessidades de armazenamento e consulta;
- progresso qualitativo pode ser difícil de calcular;
- notificações precisam ser consolidadas para evitar ruído.

### 38.3 Limitações

- a primeira versão não oferecerá colaboração offline completa;
- não haverá edição colaborativa de documentos;
- a IA não poderá resolver conflitos humanos por autoridade própria;
- o progresso não será sempre representável por percentual;
- missões não substituirão ferramentas externas em todos os tipos de projeto.

---

## 39. Critérios de conformidade

Uma implementação estará em conformidade com esta RFC somente se:

1. toda missão possuir objetivo temporário e critério de conclusão;
2. missões preservarem plano, tarefas, progresso, contexto e histórico;
3. missões coletivas espontâneas exigirem aceite dos participantes;
4. missões atribuídas identificarem autoridade formal;
5. participantes puderem sair livremente de missões espontâneas;
6. participantes não puderem abandonar unilateralmente missões atribuídas;
7. usuários de missões atribuídas puderem justificar, pedir ajuda ou solicitar revisão;
8. a IA não puder impor colaboração entre colegas;
9. a transferência de tarefa exigir aceite do responsável ou decisão da autoridade;
10. ofertas de ajuda não alterarem responsabilidade automaticamente;
11. o Teamwork apresentar objetivo, tarefas, dependências, responsáveis e progresso;
12. sugestões de distribuição respeitarem carga, habilidade, disponibilidade, permissões e consentimento;
13. métricas não produzirem rankings depreciativos ou rótulos pessoais;
14. cada missão funcionar como workspace persistente;
15. pausa e retomada preservarem contexto;
16. chat e notas existirem como entidades distintas;
17. decisões relevantes poderem ser registradas explicitamente;
18. referências a Pedidos, Processos e Etapas não criarem duplicação contraditória;
19. permissões normais continuarem válidas dentro da missão;
20. ações relevantes gerarem eventos e histórico;
21. conclusão ou cancelamento tratarem pendências remanescentes explicitamente;
22. a IA não possuir autoridade própria para atribuir, remover ou encerrar obrigações.

---

## 40. Decisões adiadas

As seguintes decisões serão tomadas na implementação ou em documentos posteriores:

- layout definitivo do workspace;
- tecnologia do chat;
- política de retenção e busca de mensagens;
- edição de mensagens;
- menções e reações;
- anexos no chat;
- limites máximos de participantes;
- algoritmo de progresso percentual;
- catálogo inicial de papéis;
- modelos reutilizáveis de missão;
- regras de recorrência;
- integração com calendário;
- suporte offline ampliado;
- sincronização de rascunhos;
- mecanismos de busca dentro da missão;
- exportação e impressão;
- indicadores gerenciais específicos;
- critérios automáticos de arquivamento;
- política de anonimização ou retenção legal.

Essas decisões deverão respeitar as invariantes desta RFC.

---

## 41. Declaração normativa

O Mheibos utilizará Missões para representar objetivos operacionais temporários que necessitem de continuidade, organização, acompanhamento ou colaboração.

Cada Missão será um workspace persistente que reunirá objetivo, plano, tarefas, prazos, participantes, dependências, progresso, contexto, histórico, conversas, notas, decisões e referências relacionadas.

O Teamwork somente será ativado por concordância dos participantes ou por autoridade formal. A IA poderá sugerir organização, distribuição e ajuda, mas não poderá impor colaboração, transferir tarefas silenciosamente, criar obrigações ocultas ou substituir a autoridade humana.

Missões espontâneas permitirão saída voluntária. Missões atribuídas dependerão da autoridade responsável para retirada de participantes ou encerramento da obrigação, preservado o direito de justificar, pedir ajuda e solicitar revisão.

A comunicação do Mheibos deverá descrever fatos, riscos, carga, atraso, dependências e impacto sem transformar métricas em julgamento pessoal, ranking depreciativo ou exposição humilhante.

Conversas e notas permanecerão vinculadas à missão, mas serão entidades distintas. O chat preservará comunicação cronológica; notas preservarão conteúdo consolidado. Nenhum conteúdo será promovido automaticamente a conhecimento oficial sem o processo de governança correspondente.

A Missão organizará o trabalho sem substituir Pedidos, Processos, Etapas, Pendências, permissões, eventos ou estados oficiais da plataforma.
