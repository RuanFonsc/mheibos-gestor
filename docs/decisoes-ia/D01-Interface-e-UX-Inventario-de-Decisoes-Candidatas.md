# MHEIBOS INTELLIGENT OPERATING SYSTEM

# D01 — Interface e UX
## Inventário de Decisões Cognitivas Candidatas ao Catálogo de Decisões Autônomas

**Status:** Consolidado para etapa posterior de classificação  
**Domínio:** D01 — Interface e UX  
**Natureza:** Inventário de decisões candidatas — não constitui, por si só, autorização autônoma final  
**Base normativa relacionada:** RFC-0009 — Interface Viva e Intervenções; RFC-0010 — Missões e Teamwork; Plano-Modelo de Decisões Autônomas da IA

---

## 1. Objetivo

Este documento consolida as decisões levantadas para o **Domínio 01 — Interface e UX** durante a construção do futuro Catálogo de Decisões Autônomas da IA do Mheibos.

As decisões aqui registradas representam **capacidades cognitivas candidatas**. Sua presença neste documento não significa, isoladamente, que a IA esteja definitivamente autorizada a executá-las de forma autônoma em produção.

Na etapa posterior do plano, cada candidata deverá ser submetida a:

- eliminação de automações puramente determinísticas;
- identificação de proibições normativas;
- agrupamento de ações simples;
- classificação de importância, risco, reversibilidade, alcance, confiança e necessidade de confirmação;
- testes de cenários extremos;
- revisão contra as RFCs e princípios oficiais;
- publicação no Catálogo de Decisões Autônomas.

---

## 2. Direção consolidada do domínio

O Domínio 01 estabelece uma Interface Viva na qual a IA pode possuir ampla liberdade para **adaptar temporariamente a experiência do usuário**, desde que permaneça dentro das capacidades autorizadas do Mheibos.

A autonomia visual não equivale a autoridade operacional.

A IA poderá reorganizar, destacar, priorizar, expandir, recolher, compor visualizações, apresentar controles contextuais e administrar sua própria presença na interface. Entretanto, alterações persistentes, ações protegidas, criação de obrigações e mudanças estruturais continuam submetidas às autoridades e confirmações correspondentes.

Princípios que emergiram do domínio:

1. **A atenção do usuário é um recurso que deve ser administrado.**
2. **A Interface Viva deve usar a menor interrupção eficaz.**
3. **A IA pode ajudar sem necessariamente falar.**
4. **Painel lateral e Interface Viva são complementares e podem atuar simultaneamente.**
5. **Levar a informação ao usuário é preferível a levar o usuário até a informação.**
6. **A IA pode aprender a incomodar menos, mas não pode aprender a proteger menos.**
7. **A escolha deliberada do usuário prevalece sobre adaptações visuais comuns da IA.**
8. **Interface inteligente não significa interface permanentemente em movimento.**
9. **Adaptação temporária pode ser autônoma; persistência exige tratamento próprio.**
10. **A IA não altera autonomamente a arquitetura permanente da interface.**

---

# 3. Decisões candidatas consolidadas

## D01-01 — Reorganização contextual temporária

A IA poderá decidir dinamicamente como reorganizar temporariamente a interface conforme contexto, objetivo e situação do usuário.

A reorganização poderá modificar a apresentação, mas não deverá alterar silenciosamente dados, permissões, regras ou decisões persistentes.

---

## D01-02 — Seleção cognitiva de destaques

A IA poderá decidir **o que merece destaque**.

A intensidade e a forma da intervenção deverão utilizar como base os mecanismos de segurança, criticidade, alertas e intervenção já existentes no Mheibos, em vez de depender de regras visuais arbitrárias criadas pelo modelo.

A decisão deverá considerar também a carga visual e cognitiva existente. Um elemento individualmente relevante não justifica necessariamente adicionar mais uma intervenção quando a tela já estiver sobrecarregada.

---

## D01-03 — Priorização e ordenação contextual

A IA poderá reordenar automaticamente listas, filas, cards e outros elementos quando identificar cognitivamente uma organização mais útil para o contexto atual.

Essa ordenação é uma adaptação de apresentação e deverá permanecer reversível.

---

## D01-04 — Abertura contextual do painel lateral da IA

A IA poderá abrir automaticamente elementos auxiliares e não disruptivos.

Para comunicação em telas nas quais alertas sobrepostos possam prejudicar a atividade principal — como formulários — deverá existir um **painel lateral expansível da IA**.

O painel:

- funciona como superfície conversacional;
- pode ser aberto automaticamente pela IA quando ela precisar se comunicar;
- pode ser aberto ativamente pelo usuário por meio de um ícone flutuante;
- deve evitar que múltiplos alertas sejam sobrepostos ao conteúdo principal;
- não concede à IA autoridade adicional sobre a operação.

---

## D01-05 — Curadoria cognitiva do conteúdo do painel

A IA poderá decidir dinamicamente:

- o que apresentar no painel lateral;
- em qual ordem;
- o que priorizar;
- o que pode aguardar;
- o que não merece interromper o usuário naquele momento.

A decisão deverá considerar relevância, urgência, contexto e carga cognitiva.

Alertas obrigatórios e mecanismos críticos permanecem sujeitos às proteções próprias do Mheibos.

O painel poderá apresentar **botões e ações funcionais contextuais** junto às informações.

Exemplo:

> Cliente já cadastrado encontrado.  
> **[Usar dados deste cliente]** · **[Ver cliente]**

Esses controles acionam capacidades previamente autorizadas do Mheibos e não código arbitrário produzido pela IA.

---

## D01-06 — Escolha do momento da interrupção

A IA poderá decidir se deve:

- abrir o painel imediatamente;
- aguardar um momento mais oportuno;
- comunicar de outra forma;
- ou não interromper.

A decisão deverá considerar urgência, relevância, atividade atual e quantidade/intensidade de intervenções recentes.

Situações críticas ou obrigatórias continuam submetidas às políticas próprias do sistema.

---

## D01-07 — Adaptação ao comportamento individual

A IA poderá aprender padrões individuais de uso e adaptar automaticamente a apresentação futura, mesmo fora de uma Missão.

Essas adaptações deverão ser:

- de apresentação;
- reversíveis;
- compatíveis com as permissões;
- incapazes de esconder informações obrigatórias;
- incapazes de alterar regras de negócio.

---

## D01-08 — Densidade e nível de informação

A IA poderá decidir dinamicamente quais informações:

- mostrar;
- resumir;
- expandir;
- recolher.

A decisão dependerá do contexto e da necessidade atual.

Informações obrigatórias, críticas ou necessárias para uma decisão segura não poderão ser ocultadas. Informações recolhidas continuarão acessíveis.

---

## D01-09 — Antecipação da próxima ação provável

A IA poderá antecipar próximas ações prováveis e preparar a interface.

Isso poderá incluir:

- organizar componentes;
- posicionar informações;
- preparar filtros;
- expandir seções;
- disponibilizar ações contextuais.

Preparar a interface não equivale a executar uma alteração operacional persistente.

---

## D01-10 — Manutenção, restauração e reaproveitamento de adaptações

A IA poderá decidir quando:

- restaurar uma adaptação;
- mantê-la;
- reaproveitá-la enquanto o contexto continuar;
- utilizar seu resultado como evidência para futuras adaptações.

A transformação de uma adaptação temporária em preferência persistente é tratada separadamente.

---

## D01-11 — Coordenação de intervenções concorrentes

A IA poderá combinar, priorizar, adiar ou suprimir adaptações concorrentes para produzir uma intervenção única e coerente.

O objetivo é alcançar o efeito necessário com a menor disputa possível pela atenção do usuário.

A IA deverá considerar o conjunto das intervenções, e não apenas cada alerta isoladamente.

Intervenções obrigatórias e críticas permanecem protegidas.

---

## D01-12 — Escolha e composição dos meios de assistência

A IA poderá decidir dinamicamente qual mecanismo é mais adequado para ajudar.

Ela poderá utilizar:

- apenas a Interface Viva;
- apenas o painel lateral;
- ambos simultaneamente;
- ou nenhum deles.

Exemplo: o painel lateral pode explicar uma inconsistência enquanto a Interface Viva destaca simultaneamente o campo relacionado.

O painel lateral é uma superfície da IA, mas não representa a totalidade da Interface Viva.

---

## D01-13 — Assistência silenciosa

A IA poderá ajudar silenciosamente por meio da Interface Viva quando não houver necessidade de comunicação explícita.

Ela poderá reorganizar, preparar, destacar, expandir, recolher ou adaptar elementos sem transformar cada pequena assistência em mensagem ou notificação.

A escolha entre assistência silenciosa, painel lateral, combinação dos dois ou ausência de intervenção será contextual.

---

## D01-14 — Adaptação diante de provável dificuldade

A IA poderá identificar cognitivamente uma provável dificuldade durante a interação e adaptar a assistência.

Poderá, conforme o caso:

- simplificar a visualização;
- destacar o próximo passo;
- expandir informações úteis;
- preparar ações;
- usar o painel lateral;
- combinar painel e Interface Viva;
- iniciar orientação mais guiada.

A inferência deverá se limitar à dificuldade contextual da interação e não poderá produzir diagnóstico ou rótulo pessoal.

---

## D01-15 — Redução dinâmica da assistência

A IA poderá aumentar, reduzir, suspender e posteriormente retomar assistência contextual conforme:

- necessidade observada;
- domínio demonstrado da atividade;
- contexto;
- resposta do usuário.

O objetivo é oferecer **a menor assistência necessária para manter eficiência e segurança**.

Essa redução não se aplica a proteções, informações obrigatórias ou alertas críticos.

---

## D01-16 — Aprendizado a partir da reação às intervenções

A IA poderá aprender com a reação do usuário e adaptar futuramente:

- canal;
- intensidade;
- momento;
- formato da assistência.

Exemplo: poderá perceber que determinado usuário responde melhor a adaptações silenciosas do que à abertura frequente do painel lateral.

Esse aprendizado não poderá enfraquecer proteções obrigatórias ou críticas.

---

## D01-17 — Prevenção contextual de omissões e erros prováveis

A IA poderá intervir preventivamente antes da materialização de um erro quando houver **evidência contextual concreta** de que uma omissão, inconsistência ou erro provável está em formação e quando a antecipação trouxer benefício claro.

A mera possibilidade abstrata de erro não justifica intervenção.

Exemplo:

O campo **Tema** está no início do formulário e é obrigatório. O usuário passa por ele sem preencher e já alcança campos do final, como **Valor pago**. A IA pode usar a Interface Viva para chamar discretamente a atenção para o Tema.

A prevenção primária do Mheibos continua baseada na lógica dos fluxos, validações, processos e alertas coerentes. A IA complementa essas proteções; não deve criar uma camada de alertas preventivos indiscriminados.

---

## D01-18 — Reavaliação antes de repetir ou escalar uma intervenção

A IA não deverá escalar uma intervenção simplesmente porque o usuário não reagiu.

Antes de atuar novamente, deverá reavaliar a situação operacional.

Uma nova intervenção só deverá ocorrer quando:

- ainda houver benefício concreto;
- existir justificativa relevante;
- ou surgir uma nova condição.

Se validações, bloqueios ou etapas posteriores do próprio Mheibos já impedirem uma consequência problemática, não há motivo para a IA insistir.

**A IA não escala porque foi ignorada; intervém novamente porque a situação justifica uma nova intervenção.**

---

## D01-19 — Autocorreção da própria presença visual

A IA poderá reconhecer que uma adaptação deixou de ser útil ou passou a gerar atrito e poderá:

- reduzi-la;
- desfazê-la;
- substituí-la;
- adotar abordagem menos intrusiva;
- aprender com o resultado quando apropriado.

Essa capacidade não permite neutralizar alertas críticos.

Fechar painéis, restaurar a visualização ou demonstrar incômodo não poderá ensinar à IA que proteções críticas devem deixar de ser apresentadas.

**A IA pode aprender a incomodar menos; não pode aprender a proteger menos.**

---

## D01-20 — Composição dinâmica de visualizações contextuais

A IA poderá compor visualizações temporárias utilizando componentes e informações que o usuário já esteja autorizado a acessar.

Essas visualizações poderão reunir informações normalmente separadas em vários módulos quando isso facilitar a compreensão de uma situação.

A IA não poderá:

- criar código arbitrário;
- inventar componentes fora dos contratos permitidos;
- adquirir novas permissões;
- alterar dados apenas por causa da visualização.

---

## D01-21 — Proposição de Missão a partir de contexto complexo

A IA poderá concluir cognitivamente que uma situação deixou de ser adequada para uma simples visualização temporária e **propor a criação de uma Missão**.

A proposta poderá conter:

- objetivo;
- justificativa;
- contexto;
- plano inicial;
- tarefas;
- dependências;
- referências.

Entretanto:

> **A IA não pode criar, ativar nem iniciar uma Missão autonomamente.**

A criação e o início dependem da autorização do usuário ou da autoridade humana aplicável.

---

## D01-22 — Interface Viva orientada por Missão

Depois que uma Missão estiver devidamente autorizada e iniciada, a IA poderá adaptar autonomamente a Interface Viva conforme:

- objetivo;
- tarefa atual;
- progresso;
- prioridades;
- dependências;
- mudanças de contexto.

Essa autonomia visual não concede autoridade adicional para alterar responsabilidades, tarefas oficiais ou outras decisões persistentes da Missão.

---

## D01-23 — Mudança cognitiva de foco

A IA poderá decidir mudar o foco da Interface Viva quando surgir uma situação suficientemente mais importante.

A decisão deverá considerar:

- criticidade;
- urgência;
- impacto;
- atividade atual;
- custo cognitivo da interrupção;
- possibilidade de esperar.

Algo ser mais importante não significa automaticamente que deva interromper o usuário naquele instante.

A IA poderá preparar a informação, sinalizá-la, utilizar o painel ou aguardar momento melhor.

---

## D01-24 — Preservação e restauração de contexto

Quando uma interrupção realmente exigir mudança temporária de foco, a IA poderá preservar e posteriormente restaurar automaticamente:

- tela;
- posição;
- filtros;
- registro selecionado;
- seções abertas;
- organização contextual;
- demais elementos necessários à continuidade.

Se durante a interrupção o usuário assumir conscientemente outro objetivo, a IA não deverá disputar o controle tentando forçar o retorno.

---

## D01-25 — Gestão contextual do espaço da interface

A IA poderá adaptar dinamicamente:

- tamanho;
- expansão;
- densidade;
- protagonismo dos componentes contextuais;
- espaço ocupado pelo painel lateral.

A decisão deverá considerar atividade atual, quantidade de informação, relevância e necessidade de preservar a área principal de trabalho.

A liberdade permanece dentro dos componentes e limites do design system. A IA escolhe uma composição autorizada; não inventa layouts arbitrários.

---

## D01-26 — Adaptação ao estado momentâneo da interação

A IA poderá inferir o estado momentâneo da interação e adaptar:

- densidade informacional;
- assistência;
- frequência de intervenções;
- comportamento da Interface Viva.

Exemplos conceituais:

- execução intensa → menos interrupções opcionais;
- análise → mais contexto disponível;
- provável dificuldade → assistência maior;
- fluidez → interferência menor.

Essa inferência descreve o contexto momentâneo da interação e não poderá ser convertida em diagnóstico, rótulo ou julgamento permanente sobre a pessoa.

---

## D01-27 — Prevalência da escolha visual deliberada do usuário

Quando o usuário deliberadamente contrariar uma adaptação comum da IA — por exemplo, mudar uma ordenação, recolher uma seção ou restaurar a visualização padrão — sua escolha prevalecerá naquele contexto.

A IA poderá:

- interpretar a reação;
- adaptar sua atuação;
- aprender com ela.

Mas não deverá ficar desfazendo repetidamente a escolha consciente do usuário.

A exceção são proteções, informações obrigatórias e intervenções críticas independentes da preferência visual.

---

## D01-28 — Confirmação de objetivos inferidos pela navegação

A IA poderá inferir uma possível intenção a partir da navegação e do comportamento contextual, mas **não deverá assumir essa hipótese como objetivo declarado**.

Quando uma intenção inferida for relevante para orientar uma nova linha de assistência, deverá confirmá-la com o usuário.

Exemplo:

> Parece que você está tentando entender a situação financeira deste cliente. Quer que eu organize essas informações?

**[Sim, organizar]** · **[Não]**

A restrição não impede adaptações baseadas em contexto já conhecido. Ela impede que a IA deduza um novo objetivo e passe a agir como se o usuário o tivesse declarado.

---

## D01-29 — Atalhos e botões contextuais temporários

A IA poderá criar e posicionar temporariamente:

- atalhos contextuais;
- botões funcionais;
- botões flutuantes.

Esses elementos deverão representar exclusivamente capacidades já existentes e autorizadas do Mheibos.

A IA poderá decidir:

- quando apresentá-los;
- onde posicioná-los dentro dos espaços permitidos;
- quando removê-los.

Ela deverá evitar acumular controles flutuantes e gerar poluição visual.

A IA cria um **ponto de acesso contextual**, não uma nova capacidade do sistema.

---

## D01-30 — Trazer informação ao usuário antes de mudar de tela

Quando informações existentes em outros módulos, registros ou telas forem necessárias ao objetivo atual, a IA deverá preferir recuperá-las e apresentá-las no painel lateral, preservando a tela e o contexto atuais.

A Interface Viva poderá complementar essa apresentação.

A navegação para outra tela deverá ser reservada aos casos em que:

- a própria atividade precise ser executada naquela interface;
- ou o conteúdo/ação não possa ser representado adequadamente no contexto atual.

Princípio:

> **Levar a informação ao usuário é preferível a levar o usuário até a informação.**

---

## D01-31 — Ações contextuais pelo painel lateral

O painel lateral poderá permitir a execução de ações contextuais autorizadas sem retirar o usuário da tela atual, sempre que tecnicamente possível.

Continuam valendo:

- permissões;
- confirmações;
- autenticações;
- proteções;
- regras da operação original.

O painel não aumenta a autoridade da IA. Ele leva capacidades existentes até o contexto atual.

---

## D01-32 — Preenchimento assistido mediante autorização

Quando a IA identificar informações confiáveis que poderiam preencher campos do formulário, ela poderá preparar o preenchimento, mas **não deverá inseri-las silenciosamente**.

Antes da alteração, deverá utilizar o painel lateral para informar claramente quais dados serão preenchidos e oferecer uma ação funcional.

Exemplo:

> Encontrei este cliente no cadastro. Posso preencher:
>
> **Nome:** João Silva  
> **Telefone:** (...)  
> **E-mail:** (...)  
> **Endereço:** (...)
>
> **[Preencher informações]**

O preenchimento somente ocorre após ação do usuário.

Informações incertas ou conflitantes deverão ser explicitadas antes da confirmação.

---

## D01-33 — Proposição de persistência de uma adaptação

Quando uma adaptação temporária recorrente demonstrar utilidade, a IA poderá identificar que vale a pena transformá-la em preferência persistente.

Entretanto, deverá **propor a mudança ao usuário**.

Somente após autorização ela poderá tornar-se preferência permanente.

Princípio:

> **Autonomia ampla para adaptação temporária; consentimento humano para transformar a adaptação em configuração persistente.**

---

## D01-34 — Decisão consciente de não intervir

A IA poderá concluir que a interface atual já é suficientemente adequada e decidir **não modificar absolutamente nada**.

A ausência de intervenção é uma decisão válida quando o benefício esperado não justificar:

- custo de atenção;
- interrupção;
- mudança visual;
- risco de sobrecarga.

O modo inteligente não significa uma interface permanentemente em movimento.

---

## D01-35 — Proposição de mudanças estruturais de UX

Quando a IA identificar problemas recorrentes na estrutura permanente da interface, poderá:

- identificar o problema;
- correlacionar ocorrências;
- reunir evidências;
- explicar o impacto;
- propor uma melhoria estrutural.

Entretanto:

> **A IA não poderá alterar autonomamente o design permanente ou a arquitetura estrutural da interface do Mheibos.**

A Interface Viva pode ser dinâmica, contextual e reversível. A evolução estrutural do produto permanece submetida à governança humana e ao processo de desenvolvimento.

---

# 4. Painel lateral cognitivo da IA

O levantamento do D01 consolidou um componente importante que deverá ser tratado formalmente na arquitetura de interface.

## 4.1 Natureza

O painel lateral é a superfície conversacional e contextual própria da IA dentro do Cliente Mheibos.

Ele não substitui a Interface Viva.

A relação conceitual é:

```text
                 Assistência da IA
                       │
          ┌────────────┴────────────┐
          │                         │
   Interface Viva             Painel lateral
          │                         │
 organização visual          conversa/contexto
 destaques                   explicações
 filtros                     informações externas
 foco                        ações funcionais
 visualizações               confirmações
 botões contextuais          preenchimento assistido
          │                         │
          └────────────┬────────────┘
                       │
              Podem atuar juntos
```

## 4.2 Abertura

O painel poderá ser:

- aberto automaticamente pela IA quando houver justificativa;
- aberto voluntariamente pelo usuário por ícone flutuante;
- mantido fechado quando a Interface Viva for suficiente;
- utilizado simultaneamente com outras adaptações.

## 4.3 Funções

O painel poderá:

- conversar com o usuário;
- explicar situações;
- apresentar informações de outros módulos;
- resumir contexto;
- oferecer botões funcionais;
- oferecer atalhos;
- solicitar confirmações;
- apresentar propostas;
- preparar preenchimentos;
- permitir ações contextuais autorizadas.

## 4.4 Proteção contra sobrecarga

O painel não deverá se transformar em uma fila indiscriminada de tudo que a IA percebe.

A IA deverá decidir:

- o que merece aparecer;
- o que pode esperar;
- o que pode ser resolvido silenciosamente;
- o que perdeu relevância;
- quando abrir;
- quando permanecer fechado.

---

# 5. Limites consolidados

Independentemente da classificação autônoma futura, o D01 identificou os seguintes limites:

### 5.1 Sem código arbitrário

A IA não controla diretamente widgets, coordenadas ou código da interface.

Toda ação deve passar pelos contratos e componentes autorizados do Mheibos.

### 5.2 Sem autoridade nova

Uma superfície contextual não concede permissão operacional que o usuário ou a IA não possuam.

### 5.3 Sem enfraquecimento de segurança

Personalização, aprendizado e redução de assistência não podem neutralizar:

- alertas críticos;
- informações obrigatórias;
- bloqueios;
- validações;
- proteções permanentes.

### 5.4 Sem disputa de controle

Em adaptações comuns, a escolha deliberada do usuário prevalece.

### 5.5 Sem persistência silenciosa

Adaptações temporárias úteis podem originar propostas de preferência, mas não devem tornar-se permanentes silenciosamente.

### 5.6 Sem criação autônoma de Missão

A IA pode propor e preparar uma Missão, mas não criá-la, ativá-la ou iniciá-la sem autorização humana aplicável.

### 5.7 Sem redesign autônomo do produto

Problemas estruturais podem ser identificados e documentados pela IA, mas mudanças permanentes na arquitetura visual dependem do processo humano de evolução do Mheibos.

---

# 6. Tratamento da atenção e da carga cognitiva

O D01 estabelece que **atenção é um recurso operacional limitado**.

A IA deverá considerar o custo de uma intervenção antes de realizá-la.

Isso implica:

- evitar alertas redundantes;
- evitar múltiplos destaques concorrentes;
- evitar abertura excessiva do painel;
- evitar botões flutuantes acumulados;
- preferir intervenções coordenadas;
- utilizar assistência silenciosa quando suficiente;
- não repetir uma intervenção apenas porque foi ignorada;
- reduzir ajuda opcional quando ela deixar de ser necessária;
- preservar o foco quando uma informação puder ser trazida ao contexto atual;
- decidir não intervir quando essa for a melhor escolha.

---

# 7. Relação com segurança e fluxo determinístico

A autonomia cognitiva da Interface Viva não substitui a arquitetura determinística do Mheibos.

Fluxos, validações, processos, bloqueios e alertas continuam sendo a principal camada de garantia da integridade operacional.

A IA poderá antecipar problemas e melhorar a experiência, mas não deverá criar um segundo sistema paralelo de validação baseado em notificações cognitivas.

Exemplo:

```text
Usuário esquece o campo Tema
            │
            ├── IA percebe indício contextual
            │      ↓
            │  destaca Tema preventivamente
            │
            └── usuário ainda ignora
                   ↓
          validação determinística
                   ↓
        pedido não pode ser salvo
```

A IA ajuda antes do erro. O sistema continua garantindo que o erro não se consolide.

---

# 8. Estado deste documento

O D01 está **encerrado como inventário inicial de decisões candidatas**.

O próximo tratamento previsto pelo Plano-Modelo deverá revisar estas candidatas para:

1. detectar sobreposições remanescentes;
2. separar decisão cognitiva de comportamento determinístico;
3. identificar proibições normativas;
4. agrupar ações simples quando apropriado;
5. classificar risco, importância, alcance, reversibilidade e confiança;
6. definir condições de autonomia, confirmação e auditoria;
7. testar cenários extremos;
8. confrontar o resultado com as RFCs oficiais;
9. somente então promover decisões aprovadas ao Catálogo de Decisões Autônomas.

---

## 9. Nota de consolidação

Durante o levantamento, uma formulação originalmente numerada como D01-33 foi considerada redundante por já estar coberta pelas decisões sobre restauração e autocorreção de adaptações. Ela foi descartada e substituída pela atual **D01-33 — Proposição de persistência de uma adaptação**.

Assim, a numeração final permanece de **D01-01 a D01-35**, sem manter a candidata redundante como decisão normativa independente.
