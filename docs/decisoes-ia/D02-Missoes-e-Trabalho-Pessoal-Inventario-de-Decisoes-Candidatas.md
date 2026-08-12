# MHEIBOS INTELLIGENT OPERATING SYSTEM

# D02 — Missões e Trabalho Pessoal
## Inventário de Decisões Cognitivas Candidatas ao Catálogo de Decisões Autônomas

**Status:** Consolidado para etapa posterior de classificação  
**Domínio:** D02 — Missões e Trabalho Pessoal  
**Natureza:** Inventário de decisões candidatas — não constitui, por si só, autorização autônoma final  
**Base normativa relacionada:** RFC-0010 — Missões e Teamwork; D01 — Interface e UX; Plano-Modelo de Decisões Autônomas da IA

---

## 1. Objetivo

Este documento consolida as oito decisões levantadas para o **Domínio 02 — Missões e Trabalho Pessoal** durante a construção do futuro Catálogo de Decisões Autônomas da IA do Mheibos.

O D02 trata principalmente da relação entre:

- identificação da necessidade de uma Missão;
- formulação de propostas de Missão;
- decomposição do objetivo em trabalho executável;
- autonomia configurável individualmente por Missão;
- repriorização e replanejamento;
- lembretes e acompanhamento;
- assistência diante de problemas detectados pelos mecanismos normais do Mheibos;
- conclusão;
- redefinição do objetivo.

As decisões aqui registradas são **candidatas cognitivas**. Elas ainda deverão passar pelas etapas posteriores previstas no Plano-Modelo antes de constituírem autoridade autônoma final da IA.

---

# 2. Princípios consolidados do domínio

O levantamento do D02 produziu uma distinção central:

> **O humano define e confirma o propósito; a IA pode receber autonomia para administrar os meios para alcançá-lo.**

A autonomia de uma Missão:

1. é configurada **individualmente por Missão**;
2. não é uma preferência global;
3. não é automaticamente herdada por outras Missões;
4. permite autonomia sobre a gestão interna da Missão quando concedida;
5. não aumenta permissões fora da Missão;
6. não atravessa barreiras de segurança, autenticação ou autoridade do restante do Mheibos;
7. não autoriza a IA a redefinir unilateralmente o objetivo;
8. não autoriza a IA a encerrar definitivamente a Missão sem confirmação humana.

Outro princípio consolidado:

> **Autonomia da Missão elimina confirmações de gestão interna; não elimina as proteções do Mheibos.**

---

# 3. Decisões candidatas consolidadas

## D02-01 — Identificação e proposição de uma Missão

A IA poderá identificar cognitivamente que determinada situação merece ser tratada como uma Missão.

Ela poderá formular uma proposta contendo, quando útil:

- justificativa;
- objetivo;
- contexto inicial;
- informações relacionadas.

A decisão cognitiva de **propor** a Missão poderá partir autonomamente da IA.

Entretanto:

> **A IA não poderá criar, ativar ou iniciar a Missão sem autorização humana aplicável.**

A proposta não equivale à criação da obrigação.

---

## D02-02 — Decomposição da Missão como proposta de plano

Depois que o usuário autorizar a criação da Missão, a IA poderá decompor cognitivamente seu objetivo em:

- tarefas;
- subtarefas;
- dependências;
- ordem sugerida de execução;
- estrutura inicial de trabalho.

Essa decomposição será inicialmente uma **proposta de plano**.

As tarefas deverão ser aprovadas pelo usuário antes de integrarem efetivamente o plano inicial da Missão.

Princípio:

> **Autorizar o objetivo da Missão não significa autorizar antecipadamente qualquer plano que a IA venha a formular.**

Depois que o plano for aprovado, poderão valer as regras de autonomia específicas daquela Missão.

---

## D02-03 — Autonomia configurável individualmente por Missão

Cada Missão poderá possuir sua própria configuração de autonomia da IA.

Exemplo:

```text
Missão 1
Autonomia da IA: ATIVADA

Missão 2
Autonomia da IA: DESATIVADA
```

A autorização concedida à Missão 1 não produz qualquer autorização para a Missão 2, para Missões futuras ou para o restante do Mheibos.

Quando a autonomia estiver habilitada naquela Missão específica, a IA poderá administrar autonomamente sua organização e condução interna, incluindo, conforme aplicável:

- criar tarefas;
- remover tarefas;
- alterar tarefas;
- repriorizar;
- reorganizar dependências;
- reorganizar sequência;
- replanejar;
- ajustar acompanhamento;
- ajustar lembretes;
- adaptar a organização interna conforme o contexto evoluir.

Essas alterações não precisarão de confirmação individual a cada mudança enquanto estiverem dentro da autorização concedida àquela Missão.

### 3.1 Limite da autorização

A configuração de autonomia da Missão **não poderá ferir as demais ressalvas, permissões e barreiras de segurança do programa**.

Ela não poderá ser utilizada para:

- adquirir novas permissões;
- ignorar autenticações;
- ultrapassar autoridade do usuário;
- executar ações proibidas;
- neutralizar proteções permanentes;
- modificar regras oficiais;
- obter autoridade sobre outras Missões;
- adquirir autoridade geral sobre o Mheibos.

Princípio:

> **Autonomia da Missão significa autonomia para administrar aquela Missão, não autoridade irrestrita sobre o sistema.**

---

## D02-04 — Replanejamento diante de fatos novos

Durante a execução de uma Missão poderão surgir fatos que tornem o plano original inadequado.

Exemplos:

- uma tarefa torna-se impossível;
- surge uma dependência inesperada;
- uma solução melhor é identificada;
- determinada tarefa perde a necessidade;
- uma sequência deixa de ser eficiente;
- novas informações modificam a melhor forma de alcançar o objetivo.

### Missão com autonomia habilitada

A IA poderá replanejar autonomamente a Missão, incluindo alterações em:

- tarefas;
- sequência;
- prioridades;
- dependências;
- organização interna.

### Missão sem autonomia habilitada

A IA poderá:

1. analisar a necessidade de mudança;
2. preparar um novo plano;
3. explicar a justificativa;
4. solicitar aprovação do usuário.

As demais barreiras do Mheibos permanecem válidas em ambos os casos.

---

## D02-05 — Lembretes e acompanhamento cognitivo

A IA poderá decidir cognitivamente **quando e como lembrar ou chamar a atenção do usuário para uma Missão**.

Essa decisão poderá considerar:

- prazo;
- importância;
- progresso;
- dependências;
- contexto atual;
- comportamento recente;
- custo da interrupção.

Essa assistência poderá ocorrer mesmo quando a Missão não possuir autonomia habilitada, porque **lembrar não equivale a modificar o plano**.

A atuação deverá respeitar os princípios definidos no D01 sobre:

- carga cognitiva;
- menor interrupção eficaz;
- escolha do momento adequado;
- uso do painel lateral;
- uso da Interface Viva;
- prevenção de excesso de notificações;
- decisão consciente de não intervir.

A IA não deverá transformar acompanhamento em insistência indiscriminada.

---

## D02-06 — Assistência cognitiva diante de problemas detectados pelo Mheibos

O Mheibos já possui mecanismos estruturais para detectar e alertar sobre situações relacionadas a:

- tarefas;
- etapas;
- processos;
- bloqueios;
- prazos;
- atrasos;
- outras condições operacionais relevantes.

A IA **não deverá criar um sistema paralelo de alertas** para substituir ou duplicar esses mecanismos.

Quando o próprio Mheibos detectar um problema relacionado à Missão, a IA poderá:

- analisar a situação;
- explicar o problema;
- identificar possíveis causas;
- sugerir alternativas;
- propor soluções;
- propor replanejamento.

### Missão com autonomia habilitada

A IA poderá executar autonomamente as mudanças **internas da Missão** necessárias à solução, desde que estejam dentro da autorização concedida e respeitem todas as demais barreiras do Mheibos.

### Missão sem autonomia habilitada

A IA poderá formular a solução ou o replanejamento e submetê-lo à aprovação correspondente.

Princípio:

> **O Mheibos detecta e protege; a IA interpreta e ajuda a resolver.**

---

## D02-07 — Conclusão da Missão exige confirmação humana

A IA poderá avaliar cognitivamente se:

- as tarefas foram concluídas;
- os critérios de conclusão parecem satisfeitos;
- o objetivo aparenta ter sido alcançado;
- existem pendências relevantes antes do encerramento.

Ela poderá reunir o resultado e **propor o encerramento da Missão**.

Entretanto:

> **O fechamento definitivo da Missão sempre exige confirmação humana.**

Essa regra permanece válida inclusive quando a Missão possuir autonomia habilitada.

A autonomia permite que a IA administre o caminho até o objetivo, mas não declare unilateralmente que o propósito humano foi definitivamente cumprido.

---

## D02-08 — Redefinição do objetivo exige autorização humana

Durante a execução, a IA poderá identificar que o objetivo original deixou de ser o mais adequado ou que um objetivo diferente produziria resultado melhor.

Ela poderá:

- identificar a necessidade;
- explicar a descoberta;
- justificar a mudança;
- formular um novo objetivo;
- propor a alteração ao usuário.

Entretanto:

> **A IA não poderá redefinir unilateralmente o objetivo da Missão.**

A alteração do objetivo sempre exigirá autorização humana, inclusive quando a Missão possuir autonomia habilitada.

A autonomia concedida serve para administrar **como alcançar o objetivo aprovado**, não para decidir unilateralmente **qual deve ser o propósito da Missão**.

---

# 4. Modelo conceitual de autonomia por Missão

A configuração deverá ser entendida conceitualmente da seguinte forma:

```text
                     MISSÃO
                       │
              Objetivo autorizado
                       │
             Plano inicial aprovado
                       │
          ┌────────────┴────────────┐
          │                         │
 Autonomia DESATIVADA       Autonomia ATIVADA
          │                         │
 IA analisa e propõe        IA administra os meios
 mudanças internas          autonomamente
          │                         │
 aprovação humana           sem confirmação a cada
 para alterar plano         mudança interna
          │                         │
          └────────────┬────────────┘
                       │
              Limites permanentes
                 do Mheibos
                       │
         ┌─────────────┴─────────────┐
         │                           │
 Objetivo não muda sozinho     Encerramento não ocorre
                               sozinho
```

---

# 5. O que a autonomia da Missão pode abranger

Quando habilitada, a gestão autônoma poderá abranger, conforme a implementação e a classificação posterior do catálogo:

- criação de tarefas internas;
- remoção de tarefas internas;
- alteração de tarefas;
- reorganização;
- repriorização;
- dependências;
- sequência de execução;
- replanejamento;
- acompanhamento;
- organização de lembretes;
- resposta interna a mudanças de contexto;
- ajustes necessários para continuar perseguindo o objetivo aprovado.

Essas capacidades continuam subordinadas às normas externas aplicáveis.

---

# 6. O que a autonomia da Missão não concede

A autorização individual de uma Missão não concede automaticamente à IA poder para:

- alterar o objetivo sem autorização;
- encerrar definitivamente a Missão sem confirmação;
- criar outra Missão sem autorização;
- atribuir autoridade que o usuário não possui;
- ignorar permissões;
- ignorar autenticações;
- ultrapassar políticas obrigatórias;
- neutralizar alertas ou bloqueios;
- modificar processos oficiais;
- executar ações externas protegidas apenas porque beneficiariam a Missão;
- modificar outras Missões;
- transformar a autorização local em preferência global;
- alterar normas oficiais do Mheibos.

---

# 7. Relação entre propósito e meios

O D02 estabelece três momentos distintos.

## 7.1 Propósito

O objetivo é humano.

A IA pode sugerir:

- que uma Missão seja criada;
- qual poderia ser seu objetivo;
- que o objetivo existente seja revisto.

Mas a definição ou alteração do propósito depende de autorização humana.

## 7.2 Meios

Depois que objetivo e plano inicial forem aprovados, o usuário poderá conceder autonomia àquela Missão.

Nesse caso, a IA poderá administrar os meios necessários para perseguir o objetivo dentro das barreiras existentes.

## 7.3 Conclusão

Mesmo que a IA tenha administrado autonomamente toda a execução, a declaração definitiva de que a Missão cumpriu seu propósito retorna ao humano.

Conceitualmente:

```text
HUMANO
  │
  ├── autoriza a Missão
  ├── aprova objetivo
  ├── aprova plano inicial
  └── escolhe autonomia daquela Missão
              │
              ▼
             IA
              │
       administra os meios
       se estiver autorizada
              │
              ▼
      propõe conclusão
              │
              ▼
           HUMANO
              │
       confirma encerramento
```

---

# 8. Relação com o sistema de alertas

O D02 não cria uma nova arquitetura de detecção de problemas.

Alertas e condições objetivas continuam pertencendo aos mecanismos estruturais do Mheibos.

A IA atua principalmente na camada de:

```text
Condição operacional
        ↓
Mheibos detecta
        ↓
Alerta / bloqueio / estado
        ↓
IA interpreta o contexto
        ↓
Explica / propõe solução
        ↓
Missão autônoma?
   ┌────┴────┐
  não       sim
   │          │
propõe     ajusta internamente
mudança    quando permitido
```

Isso evita duplicação de notificações e mantém a cognição separada das garantias determinísticas do sistema.

---

# 9. Relação com o D01 — Interface e UX

A comunicação e assistência relacionadas às Missões deverão reutilizar as decisões do D01.

Isso inclui:

- painel lateral da IA;
- Interface Viva;
- escolha cognitiva do momento da intervenção;
- assistência silenciosa;
- administração da carga cognitiva;
- coordenação de intervenções;
- preservação de contexto;
- decisão de não intervir;
- preferência por levar informação ao usuário em vez de deslocá-lo desnecessariamente.

Uma Missão autônoma não autoriza a IA a ignorar os limites de experiência e atenção definidos no D01.

---

# 10. Estado deste documento

O D02 está **encerrado como inventário inicial de decisões candidatas**, contendo exatamente oito decisões consolidadas:

1. D02-01 — Identificação e proposição de uma Missão;
2. D02-02 — Decomposição da Missão como proposta de plano;
3. D02-03 — Autonomia configurável individualmente por Missão;
4. D02-04 — Replanejamento diante de fatos novos;
5. D02-05 — Lembretes e acompanhamento cognitivo;
6. D02-06 — Assistência cognitiva diante de problemas detectados pelo Mheibos;
7. D02-07 — Conclusão da Missão exige confirmação humana;
8. D02-08 — Redefinição do objetivo exige autorização humana.

O próximo tratamento previsto pelo Plano-Modelo deverá:

1. verificar sobreposições com decisões já normatizadas;
2. separar decisões cognitivas de comportamentos determinísticos;
3. identificar proibições;
4. classificar importância, risco, alcance e reversibilidade;
5. aplicar as regras de confiança;
6. definir requisitos de confirmação e auditoria;
7. testar cenários extremos;
8. revisar contra as RFCs oficiais;
9. somente então promover as decisões aprovadas ao Catálogo de Decisões Autônomas.
