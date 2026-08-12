# MHEIBOS INTELLIGENT OPERATING SYSTEM

# D03 — Atendimento e CRM
## Inventário de Decisões Cognitivas Candidatas ao Catálogo de Decisões Autônomas

**Status:** Consolidado para etapa posterior de classificação  
**Domínio:** D03 — Atendimento e CRM  
**Natureza:** Inventário de decisões candidatas — não constitui, por si só, autorização autônoma final  
**Base normativa relacionada:** RFC-0011 — Conhecimento, Memória e Aprendizado; regras de Atendimento/CRM; D01 — Interface e UX; Plano-Modelo de Decisões Autônomas da IA

---

## 1. Objetivo

Este documento consolida as oito decisões levantadas para o **Domínio 03 — Atendimento e CRM** durante a construção do futuro Catálogo de Decisões Autônomas da IA do Mheibos.

O domínio trata da atuação cognitiva da IA durante o atendimento, do uso contextual das informações do CRM, do aprendizado a partir dos atendentes humanos, da detecção de divergências entre conversa e operação e da fronteira entre **assistência ao atendente humano** e **atendimento autônomo ao cliente**.

As decisões registradas aqui são candidatas. Ainda deverão passar pelas etapas posteriores do Plano-Modelo antes de constituírem autoridade autônoma final.

---

# 2. Princípios consolidados do domínio

## 2.1 O Mheibos aprende com os humanos

No atendimento, funcionários humanos já treinados podem inicialmente possuir competência prática superior à IA.

Por isso, o Mheibos deve partir de uma postura de aprendizado:

> **O objetivo inicial da IA no atendimento não é presumir que sabe atender melhor que os humanos, mas aprender com a competência prática existente na empresa.**

O nível e a qualidade das intervenções da IA devem acompanhar a maturidade do **Mheibos Aprendizado**.

Isso não significa que uma instalação pouco madura deva permanecer passiva. Toda ajuda válida continua sendo útil, mas a especificidade e a autonomia da assistência devem ser coerentes com o conhecimento efetivamente disponível.

---

## 2.2 Aprender não significa imitar

Humanos são adaptáveis, autênticos e flexíveis, mas também:

- cometem erros;
- pulam etapas;
- escrevem incorretamente;
- improvisam;
- utilizam gírias;
- utilizam figurinhas;
- adotam atalhos;
- podem desenvolver hábitos operacionais ruins.

Alguns desses comportamentos podem ser adequados em determinados contextos; outros não.

Portanto:

> **O Mheibos aprende com humanos por avaliação, não por imitação.**

Frequência de comportamento não equivale a boa prática.

O Mheibos Aprendizado deverá possuir critérios capazes de distinguir práticas adequadas de práticas ruins antes de promover padrões observados.

---

## 2.3 O aprendizado nunca autoriza violar o Mheibos

Se humanos pularem deliberadamente etapas, ignorarem procedimentos ou contornarem proteções, isso poderá ser observado e analisado.

Pode inclusive revelar:

- atrito no processo;
- problema de interface;
- procedimento inadequado;
- treinamento insuficiente;
- falha operacional recorrente.

Mas:

> **O Mheibos não poderá aprender a violar suas próprias regras apenas porque humanos fazem isso.**

Comportamento observado não supera processos, permissões, bloqueios, políticas e demais normas oficiais.

---

## 2.4 Maturidade não equivale a autoridade

Uma IA pode atingir alta competência no atendimento e ainda assim não possuir autorização para responder clientes.

Princípio:

> **Maturidade suficiente torna a IA apta ao atendimento autônomo; não a autoriza. A autorização continua sendo humana.**

---

# 3. Decisões candidatas consolidadas

## D03-01 — Intervenção cognitiva durante atendimento humano

Enquanto um funcionário humano estiver atendendo um cliente, a IA poderá acompanhar o contexto e decidir cognitivamente quando existe benefício suficiente para oferecer assistência.

Ela poderá:

- permanecer silenciosa;
- utilizar a Interface Viva;
- utilizar o painel lateral;
- combinar Interface Viva e painel lateral;
- decidir não intervir.

A decisão deverá considerar relevância, contexto, maturidade do aprendizado e custo da interrupção.

Essa capacidade **não autoriza a IA a assumir o atendimento ou enviar mensagens ao cliente**.

---

## D03-02 — Geração autônoma de resposta sugerida

Durante o atendimento humano, a IA poderá elaborar autonomamente uma **resposta completa sugerida**, utilizando:

- contexto da conversa;
- histórico autorizado;
- informações do CRM;
- conhecimento disponível;
- aprendizado validado;
- demais informações às quais o atendente possua acesso.

A resposta poderá aparecer pronta para revisão no painel lateral, inclusive acompanhada de informações ou ações contextuais.

Entretanto:

> **Gerar uma resposta não equivale a possuir autoridade para enviá-la.**

Enquanto o atendimento autônomo não estiver explicitamente autorizado, o envio ao cliente permanece uma ação humana.

---

## D03-03 — Curadoria cognitiva do contexto do CRM

A IA poderá recuperar, selecionar, resumir e apresentar autonomamente apenas as informações do CRM relevantes para o atendimento atual.

Ela deverá evitar despejar indiscriminadamente todo o histórico disponível.

Entre as informações potencialmente relevantes poderão estar:

- pedidos anteriores;
- histórico de relacionamento;
- pagamentos;
- ocorrências;
- conversas anteriores;
- dados cadastrais;
- preferências registradas;
- informações operacionais relacionadas.

A seleção deverá respeitar:

- permissões;
- necessidade contextual;
- autoridade;
- relevância;
- minimização de excesso informacional.

O objetivo é fornecer o **contexto suficiente para ajudar**, e não maximizar a quantidade de dados apresentados.

---

## D03-04 — Aprendizado avaliado a partir do atendimento humano

A IA poderá observar atendimentos humanos e identificar:

- padrões;
- estratégias;
- práticas;
- abordagens;
- formas de condução;
- respostas que parecem produzir bons resultados.

Essas observações poderão alimentar o Mheibos Aprendizado.

Entretanto, padrões observados **não se tornam automaticamente boas práticas, regras oficiais ou comportamento autorizado da IA**.

O fluxo conceitual deverá preservar distinções como:

```text
Comportamento observado
        ↓
Observação
        ↓
Análise
        ↓
Hipótese
        ↓
Avaliação de boa prática
        ↓
Conhecimento emergente
        ↓
Validação / promoção aplicável
        ↓
Conhecimento autorizado
```

### 3.4.1 Autenticidade humana

Elementos como:

- informalidade;
- gírias;
- figurinhas;
- estilo conversacional;
- formas naturais de interação;

não são automaticamente bons nem ruins.

Seu valor depende do contexto e dos critérios de boas práticas definidos para o Mheibos.

### 3.4.2 Práticas inadequadas

Erros ortográficos, comunicação inadequada, improvisações ruins, etapas deliberadamente ignoradas e contornos de segurança não deverão ser promovidos simplesmente porque aparecem com frequência.

---

## D03-05 — Identificação cognitiva de informações ausentes no atendimento

A IA poderá identificar informações relevantes que ainda não estejam presentes na conversa ou devidamente registradas no sistema.

Entretanto, ela não deverá presumir que toda informação ausente precisa ser perguntada ao cliente.

A fonte correta pode ser:

- o cliente;
- o atendente;
- o CRM;
- um pedido anterior;
- outro registro autorizado;
- informação operacional já conhecida pelo funcionário.

O Mheibos deverá, quando possível, recuperar informações já existentes antes de sugerir perguntas redundantes.

### 3.5.1 Informação que o atendente deve fornecer

Existem informações necessárias ao fechamento que podem não ter sido explicitamente fornecidas pelo cliente porque o próprio atendente já as conhece ou as determina durante o atendimento.

Exemplos:

- material;
- quantidade;
- tamanho;
- acabamento;
- data de entrega;
- valor total.

A ausência dessas informações na conversa não significa necessariamente que a IA deva perguntar ao cliente.

### 3.5.2 Resumo de fechamento

Quando o pedido estiver sendo fechado e informações relevantes ainda não estiverem claramente consolidadas na conversa, a IA poderá sugerir uma mensagem de fechamento contendo o orçamento completo.

Exemplo estrutural:

```text
Material: ...
Quantidade: ...
Tamanho: ...
Acabamento: ...
Data de entrega: ...
Valor total: ...
```

O objetivo é permitir que o atendente confira, complete e comunique claramente ao cliente o que está sendo acordado.

Essa mensagem também pode produzir uma confirmação conversacional estruturada do fechamento.

---

## D03-06 — Detecção e registro de divergências entre conversa e operação

A IA deverá ser capaz de identificar cognitivamente conflitos relevantes entre:

- conversa;
- CRM;
- orçamento;
- pedido;
- informações operacionais relacionadas.

Exemplo:

```text
Conversa:
Cliente solicitou 50 unidades.

Pedido:
Quantidade registrada: 40 unidades.
```

A IA deverá alertar claramente o usuário sobre a divergência e mostrar quais informações estão em conflito.

### 3.6.1 Sem correção silenciosa

A IA não deverá presumir automaticamente qual fonte está correta.

Ela não poderá corrigir silenciosamente o pedido apenas porque encontrou uma informação diferente na conversa.

### 3.6.2 Sem bloqueio cognitivo automático

A divergência detectada cognitivamente pela IA não cria, por si só, um bloqueio operacional.

O usuário poderá prosseguir quando nenhuma regra determinística do Mheibos impedir a ação.

### 3.6.3 Registro da divergência ignorada

Quando existir um conflito claro, a IA alertar o usuário e ele deliberadamente prosseguir mantendo a divergência, o ocorrido deverá ser registrado.

O registro deverá preservar, conforme aplicável:

- divergência identificada;
- informações conflitantes;
- origem das informações comparadas;
- momento da detecção;
- evidência de que o usuário foi alertado;
- identidade do usuário que prosseguiu;
- estado mantido após o alerta.

Esse registro não significa que a IA estava necessariamente correta.

Ele significa apenas:

> **A IA identificou uma divergência, informou o humano e o humano decidiu prosseguir.**

### 3.6.4 Prevalência das regras determinísticas

Se outra regra do Mheibos tornar determinada inconsistência intransponível, o bloqueio continua valendo.

A decisão cognitiva não substitui nem enfraquece proteções determinísticas.

---

## D03-07 — Aprendizado a partir de divergências e seus desfechos

Os registros de divergências poderão alimentar o Mheibos Aprendizado.

A IA poderá analisar recorrências para identificar hipóteses relacionadas a:

- falhas de atendimento;
- problemas de processo;
- problemas de interface;
- hábitos operacionais inadequados;
- treinamento;
- ambiguidades;
- erros de interpretação da própria IA;
- possíveis melhorias estruturais.

Esses padrões não poderão virar automaticamente regras ou boas práticas.

Princípio:

> **Frequência não transforma comportamento humano em boa prática.**

Se vários usuários ignorarem repetidamente determinado alerta, isso não prova que o alerta seja irrelevante.

Pode significar:

1. que a IA está interpretando a situação incorretamente;
2. que o alerta está mal formulado;
3. que o processo possui uma exceção ainda não compreendida;
4. que existe um erro humano recorrente;
5. que há um problema estrutural no fluxo.

O Mheibos deverá investigar antes de promover qualquer conclusão.

Fluxo esperado:

```text
Divergência
    ↓
Registro
    ↓
Recorrência / desfecho
    ↓
Análise
    ↓
Hipótese
    ↓
Validação
    ↓
Possível aprendizado
```

---

## D03-08 — Autoridade explícita para atendimento autônomo ao cliente

O Mheibos deverá distinguir formalmente dois regimes de atendimento.

# Regime 1 — Atendimento autônomo DESATIVADO

Enquanto a autorização de atendimento autônomo estiver desativada, a IA poderá:

- observar;
- aprender;
- analisar;
- recuperar contexto;
- detectar conflitos;
- sugerir respostas;
- auxiliar o atendente;
- preparar informações;
- preparar ações.

Mas:

> **A IA NUNCA poderá responder ou enviar mensagens diretamente ao cliente.**

Essa proibição independe de:

- nível de confiança;
- simplicidade da mensagem;
- maturidade do modelo;
- quantidade de aprendizado;
- certeza aparente da resposta.

Sem autorização explícita, não existe autoridade de envio.

# Regime 2 — Atendimento autônomo ATIVADO

O Mheibos Aprendizado prevê que, após atingir nível suficiente de aprendizado e maturidade, a IA possa tornar-se apta a atender clientes autonomamente como um **chatbot integrado ao sistema**.

Entretanto, a maturidade não ativa essa capacidade automaticamente.

A ativação deverá ocorrer:

1. explicitamente nas configurações;
2. por uma ação humana;
3. mediante autenticação por **senha de gerente**.

Somente depois dessa autorização a IA poderá responder diretamente aos clientes dentro das regras aplicáveis.

### 3.8.1 Maturidade e permissão são condições diferentes

```text
Mheibos Aprendizado
        ↓
Maturidade suficiente?
        │
   não ─┴─ sim
             │
             ↓
      IA está APTA
             │
             ↓
 Atendimento autônomo
 está autorizado nas configurações?
        │
   não ─┴─ sim
    │         │
    ↓         ↓
PROIBIDO   PERMITIDO
responder  responder
cliente    dentro das regras
```

Portanto:

> **Maturidade suficiente torna o Mheibos apto ao atendimento autônomo; não o autoriza.**

### 3.8.2 Barreiras continuam válidas

A ativação do atendimento autônomo não remove:

- permissões;
- políticas;
- processos;
- proteções;
- limites de conhecimento;
- regras de segurança;
- auditoria;
- regras de confiança;
- demais restrições oficiais do Mheibos.

A autorização concede a capacidade de responder diretamente ao cliente dentro do regime previsto. Ela não concede autoridade irrestrita sobre o restante do sistema.

---

# 4. Modelo conceitual de evolução do atendimento

O D03 estabelece uma progressão conceitual:

```text
        MHEIBOS COM POUCO APRENDIZADO
                     │
                     ↓
              observa humanos
                     │
                     ↓
             recupera contexto
                     │
                     ↓
              oferece ajuda
                     │
                     ↓
           sugere respostas
                     │
                     ↓
       aprende práticas avaliadas
                     │
                     ↓
       valida conhecimento útil
                     │
                     ↓
        aumenta sua competência
                     │
                     ↓
      maturidade suficiente para
       atendimento autônomo
                     │
                     ↓
         AINDA NÃO AUTORIZADO
                     │
                     ↓
      gerente ativa nas configurações
       com autenticação por senha
                     │
                     ↓
       ATENDIMENTO AUTÔNOMO
```

A progressão de competência não implica progressão automática de autoridade.

---

# 5. Relação entre humano e IA no aprendizado

O atendente humano possui duas funções simultâneas no estágio assistido:

1. **executa o atendimento real**;
2. **produz evidências de prática para o aprendizado do Mheibos**.

A IA, por sua vez:

1. observa;
2. recupera contexto;
3. auxilia;
4. compara;
5. identifica padrões;
6. gera hipóteses;
7. aprende apenas após avaliação adequada.

O modelo não deverá assumir:

```text
humano fez X
    ↓
X é correto
    ↓
IA deve fazer X
```

O modelo correto é:

```text
humano fez X
    ↓
X produziu evidência
    ↓
Mheibos avalia contexto e resultado
    ↓
X é boa prática?
    ↓
validação aplicável
    ↓
possível aprendizado
```

---

# 6. Relação entre conversa e dados operacionais

A conversa com o cliente é uma fonte importante de evidência operacional, mas não é automaticamente a única fonte verdadeira.

O Mheibos poderá comparar semanticamente:

```text
CONVERSA
    │
    ├──────────┐
    │          │
    ↓          ↓
ORÇAMENTO    CRM
    │          │
    └────┬─────┘
         ↓
       PEDIDO
         │
         ↓
   OPERAÇÃO REAL
```

A IA deverá procurar inconsistências entre essas representações sem assumir silenciosamente qual delas prevalece.

Isso permite detectar situações difíceis de capturar apenas com validações tradicionais.

---

# 7. Registro de divergências como evidência

Uma divergência ignorada é relevante tanto para auditoria quanto para aprendizado.

Entretanto, seu significado deve permanecer preciso.

Ela prova que:

- duas informações aparentemente conflitantes existiam;
- a IA percebeu o conflito;
- o usuário foi alertado;
- o usuário prosseguiu.

Ela **não prova**, isoladamente:

- que o usuário errou;
- que a IA estava correta;
- que a conversa deveria prevalecer;
- que o pedido deveria prevalecer.

O desfecho posterior poderá produzir novas evidências.

---

# 8. Critérios de boas práticas de atendimento

O D03 identifica a necessidade de o Mheibos Aprendizado possuir critérios explícitos para avaliar boas práticas.

Esses critérios deverão impedir que o sistema confunda:

- popularidade com correção;
- frequência com qualidade;
- autenticidade com erro;
- informalidade com inadequação;
- flexibilidade com violação de processo;
- atalho humano com comportamento autorizado da IA.

A definição normativa completa desses critérios deverá permanecer alinhada aos documentos oficiais de conhecimento, aprendizado, atendimento e governança.

---

# 9. Relação com o D01 — Interface e UX

A assistência ao atendente deverá utilizar as superfícies definidas no D01.

Isso inclui:

- painel lateral da IA;
- Interface Viva;
- assistência silenciosa;
- escolha do momento da intervenção;
- menor interrupção eficaz;
- curadoria contextual;
- botões funcionais;
- preservação do contexto;
- prevenção de sobrecarga;
- decisão de não intervir.

O atendimento não deve transformar o painel em uma sequência contínua de sugestões.

A maturidade do aprendizado e a relevância da ajuda deverão influenciar o nível de intervenção.

---

# 10. Estado deste documento

O D03 está **encerrado como inventário inicial de decisões candidatas**, contendo exatamente oito decisões consolidadas:

1. **D03-01** — Intervenção cognitiva durante atendimento humano;
2. **D03-02** — Geração autônoma de resposta sugerida;
3. **D03-03** — Curadoria cognitiva do contexto do CRM;
4. **D03-04** — Aprendizado avaliado a partir do atendimento humano;
5. **D03-05** — Identificação cognitiva de informações ausentes no atendimento;
6. **D03-06** — Detecção e registro de divergências entre conversa e operação;
7. **D03-07** — Aprendizado a partir de divergências e seus desfechos;
8. **D03-08** — Autoridade explícita para atendimento autônomo ao cliente.

Uma formulação inicialmente considerada para a D03-05 — adaptação autônoma da personalidade/estilo da IA por cliente — foi descartada por redundância, pois a personalidade do Mheibos IA já é definida em outra camada normativa e não deve ser reinventada pelo Catálogo de Decisões Autônomas.

O próximo tratamento previsto pelo Plano-Modelo deverá:

1. verificar sobreposições com decisões já normatizadas;
2. separar cognição de automação determinística;
3. identificar proibições;
4. classificar importância, risco, alcance e reversibilidade;
5. aplicar regras de confiança;
6. definir requisitos de confirmação e auditoria;
7. testar cenários extremos;
8. confrontar o resultado com as RFCs oficiais;
9. somente então promover as decisões aprovadas ao Catálogo de Decisões Autônomas.
