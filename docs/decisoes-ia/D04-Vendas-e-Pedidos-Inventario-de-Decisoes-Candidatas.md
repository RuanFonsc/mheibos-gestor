# MHEIBOS INTELLIGENT OPERATING SYSTEM

# D04 — Vendas e Pedidos
## Inventário de Decisões Cognitivas Candidatas ao Catálogo de Decisões Autônomas

**Status:** Consolidado para etapa posterior de classificação  
**Domínio:** D04 — Vendas e Pedidos  
**Natureza:** Inventário de decisões candidatas — não constitui, por si só, autorização autônoma final  
**Base normativa relacionada:** RFCs oficiais de operação, atendimento, pedidos, conhecimento/aprendizado e governança; D01 — Interface e UX; D03 — Atendimento e CRM; Plano-Modelo de Decisões Autônomas da IA

---

## 1. Objetivo

Este documento consolida as oito decisões levantadas para o **Domínio 04 — Vendas e Pedidos** durante a construção do futuro Catálogo de Decisões Autônomas da IA do Mheibos.

O domínio trata principalmente da fronteira entre:

- flexibilidade comercial humana;
- atendimento autônomo da IA;
- excepcionalidades comerciais;
- alternativas permitidas;
- preço e prazo;
- recomendações comerciais;
- uso do histórico do cliente;
- fechamento de pedidos;
- divergências identificadas após o fechamento.

As decisões aqui registradas são **candidatas cognitivas**. Ainda deverão passar pelas etapas posteriores previstas no Plano-Modelo antes de constituírem autoridade autônoma final da IA.

---

# 2. Princípios consolidados do domínio

## 2.1 Flexibilidade comercial humana não é automaticamente transferida à IA

Na operação real de uma gráfica, situações aparentemente incomuns podem ser perfeitamente legítimas.

Humanos treinados conseguem exercer flexibilidade em casos como:

- quantidades incomuns;
- combinações específicas de produto;
- acabamentos;
- condições particulares;
- necessidades específicas de clientes;
- exceções avaliadas conscientemente.

A IA poderá perceber que algo está fora do padrão e chamar a atenção do humano, mas não deverá concluir que o comportamento incomum está errado apenas porque é incomum.

Princípio:

> **O humano pode exercer flexibilidade comercial dentro de sua autoridade; a IA não adquire essa discricionariedade por observação ou aprendizado.**

---

## 2.2 Atendimento autônomo opera dentro de parâmetros definidos

Quando a IA estiver autorizada a atender clientes autonomamente, deverá seguir os parâmetros comerciais válidos do Mheibos.

Isso inclui, conforme aplicável:

- valores;
- prazos;
- produtos;
- quantidades possíveis;
- condições;
- regras de fechamento;
- demais parâmetros comerciais oficiais.

Situações extraordinárias que exijam decisão fora desses parâmetros deverão ser encaminhadas para avaliação humana.

---

## 2.3 A IA pode vender, mas não negociar preço ou prazo

A IA poderá:

- explicar condições;
- apresentar produtos;
- recomendar alternativas;
- encontrar soluções autorizadas;
- conduzir o atendimento;
- tentar concluir a venda.

Mas:

> **A IA não possui autoridade para negociar preço nem prazo.**

Quando o cliente realmente exigir uma negociação nesses elementos, a decisão deverá ser encaminhada para atendimento humano.

---

## 2.4 Autonomia não pode virar teimosia

A IA deve tentar resolver o atendimento dentro das regras e alternativas disponíveis.

Entretanto:

> **Tentar resolver autonomamente não significa resistir ao atendimento humano.**

A IA deverá perceber quando:

- o cliente não deseja continuar discutindo alternativas;
- o cliente pede atendimento humano;
- a conversa começa a gerar atrito;
- a solução depende efetivamente de uma excepcionalidade;
- continuar insistindo prejudicaria a experiência.

Não deverá existir uma regra artificial como “oferecer obrigatoriamente três alternativas antes de transferir”.

O contexto da conversa deverá ser considerado.

---

## 2.5 Recorrência de exceção não cria autorização

Se muitos clientes solicitarem repetidamente uma condição fora do padrão, isso poderá ser uma evidência relevante para o Mheibos Aprendizado.

Porém:

> **Recorrência de pedidos por uma exceção não transforma a exceção em autorização.**

Se 200 clientes solicitarem prazo menor que o definido, a IA não poderá concluir autonomamente que agora possui autoridade para prometer esse prazo.

A recorrência poderá alimentar análise, aprendizado e eventual proposta de revisão dos parâmetros. Até que uma mudança autorizada ocorra, os parâmetros vigentes permanecem válidos.

---

## 2.6 Cognição adiciona proteção; não remove proteção

A IA poderá realizar análises semânticas e cognitivas adicionais sobre pedidos.

Entretanto:

> **A cognição pode adicionar proteção ao fluxo; nunca remover proteção do fluxo.**

Confiança alta da IA não autoriza:

- pular etapas;
- ignorar validações;
- dispensar confirmações obrigatórias;
- contornar processos;
- flexibilizar bloqueios.

---

# 3. Decisões candidatas consolidadas

## D04-01 — Análise cognitiva de excepcionalidades comerciais

Durante um atendimento humano, a IA poderá analisar cognitivamente o pedido e identificar situações incomuns, aparentemente inconsistentes ou fora do padrão.

Exemplos conceituais:

- quantidade incomum;
- combinação pouco frequente;
- acabamento atípico;
- condição comercial diferente do padrão;
- prazo incomum;
- informação que mereça conferência.

Quando não houver violação de regra determinística, a IA deverá limitar sua intervenção a **chamar a atenção do usuário e perguntar se a situação está correta**.

Exemplo:

```text
Esta condição está diferente do padrão observado.
Está correto?

[Sim] [Revisar]
```

A IA não deverá:

- alterar o pedido autonomamente;
- bloquear a ação apenas pela excepcionalidade cognitiva;
- presumir que o humano está errado;
- transformar padrão estatístico em regra comercial.

A flexibilidade humana pode ser legítima.

### 3.1.1 Diferença no atendimento autônomo

Quando a própria IA estiver atendendo o cliente autonomamente, ela não poderá utilizar a flexibilidade humana observada como autorização para improvisar condições extraordinárias.

Deverá seguir um padrão rígido de fechamento dentro dos parâmetros comerciais definidos.

Qualquer excepcionalidade que realmente exija sair desses parâmetros deverá receber avaliação humana.

---

## D04-02 — Encaminhamento de excepcionalidade comercial para atendimento humano

Quando estiver atendendo autonomamente e o cliente solicitar algo fora das condições comerciais que a IA está autorizada a oferecer, a IA deverá inicialmente tentar conduzir o atendimento dentro dos padrões oficiais existentes.

Ela poderá:

- explicar a condição vigente;
- apresentar as opções permitidas;
- buscar alternativas autorizadas;
- tentar concluir a venda sem criar uma exceção.

Exemplo conceitual:

```text
Cliente solicita prazo inferior ao autorizado.
        ↓
IA verifica opções permitidas.
        ↓
Existe alternativa dentro das regras?
   ┌────┴────┐
  sim       não
   │          │
oferece    excepcionalidade
opção      necessária
   │          │
   ↓          ↓
continua   encaminha para
venda      atendimento humano
```

Quando a solução depender realmente de uma exceção que a IA não possui autoridade para conceder, o atendimento deverá ser encaminhado ao humano.

A IA poderá apresentar ao atendente:

- contexto;
- solicitação do cliente;
- alternativas já tentadas;
- análise;
- possível solução;
- eventual proposta de exceção.

A decisão sobre a excepcionalidade permanece humana.

### 3.2.1 Recorrência

A repetição de solicitações semelhantes não cria autorização autônoma.

Demandas recorrentes podem alimentar o Mheibos Aprendizado e subsidiar revisão humana futura, mas não alteram silenciosamente as condições vigentes.

---

## D04-03 — Escolha autônoma de alternativas comerciais autorizadas

Quando a necessidade original do cliente não puder ser atendida exatamente como solicitada, mas existirem alternativas válidas dentro das regras comerciais, a IA poderá raciocinar autonomamente sobre essas opções.

Ela poderá oferecer alternativas envolvendo, conforme aplicável:

- produtos;
- configurações;
- quantidades permitidas;
- acabamentos;
- opções de execução;
- condições já autorizadas.

O objetivo é tentar resolver a necessidade e concluir a venda **sem ultrapassar os parâmetros comerciais existentes**.

A IA deverá encaminhar para atendimento humano quando a necessidade continuar dependendo de excepcionalidade.

### 3.3.1 Limite de insistência

A tentativa de encontrar alternativas não poderá se transformar em resistência à transferência.

A IA deverá considerar a reação do cliente e evitar:

- insistência excessiva;
- repetição de alternativas já recusadas;
- prolongamento desnecessário;
- atrito;
- tentativa de impedir acesso ao humano.

Princípio:

> **A IA deve tentar resolver autonomamente dentro das regras, mas não transformar autonomia em teimosia.**

---

## D04-04 — Proibição de negociação autônoma de preço e prazo

A IA não poderá negociar preço nem prazo.

Mesmo durante atendimento autônomo, deverá trabalhar com as condições comerciais válidas disponibilizadas pelo Mheibos.

Ela poderá:

- apresentar o preço;
- apresentar o prazo;
- explicar as condições;
- apresentar alternativas autorizadas;
- procurar outra solução permitida.

Ela não poderá autonomamente:

- conceder desconto;
- inventar desconto;
- decidir uma margem de negociação;
- reduzir preço para fechar venda;
- prometer antecipação extraordinária;
- reduzir prazo por negociação;
- criar condição especial de preço ou prazo.

Quando o cliente desejar efetivamente negociar preço ou prazo e a solução depender dessa negociação, o caso deverá ser encaminhado para atendimento humano.

Princípio:

> **A IA pode vender; quem negocia preço e prazo é o humano.**

---

## D04-05 — Recomendações comerciais contextualmente justificadas

A IA poderá recomendar autonomamente produtos, serviços, adicionais ou alternativas quando houver **justificativa contextual real** relacionada à necessidade do cliente.

A recomendação poderá ocorrer tanto como assistência ao atendente quanto durante atendimento autônomo devidamente autorizado.

A IA não deverá:

- transformar todo atendimento em tentativa obrigatória de upsell;
- recomendar itens sem fundamento contextual;
- insistir depois de ausência clara de interesse;
- alterar preço ou prazo para viabilizar a recomendação;
- inventar condições comerciais.

O objetivo é ajudar o cliente a encontrar uma solução adequada, e não maximizar indiscriminadamente o valor de cada venda.

---

## D04-06 — Uso do histórico do cliente para oportunidades comerciais

A IA poderá utilizar o histórico autorizado do cliente como evidência para identificar oportunidades comerciais contextualmente relevantes.

Exemplos possíveis:

- compras recorrentes;
- produtos normalmente adquiridos em conjunto;
- necessidades relacionadas ao atendimento atual;
- repetição periódica de determinado pedido;
- informações históricas que indiquem uma solução potencialmente útil.

A IA poderá apresentar essas oportunidades ao cliente, inclusive durante atendimento autônomo autorizado.

A utilização do histórico deverá respeitar:

- permissões;
- relevância;
- contexto;
- ausência de insistência;
- demais regras de conhecimento e privacidade do Mheibos.

O histórico não concede autoridade para negociar preço ou prazo.

---

## D04-07 — Avaliação cognitiva complementar antes do fechamento

Antes do fechamento, a IA poderá avaliar cognitivamente se o pedido parece coerente e suficientemente preparado.

Essa análise poderá identificar problemas adicionais que não sejam capturados por validações tradicionais.

Entretanto, o fechamento deverá obedecer integralmente ao **fluxo determinístico do Mheibos**.

A IA não poderá utilizar sua confiança para:

- dispensar etapas;
- ignorar validações;
- remover bloqueios;
- pular conferências obrigatórias;
- flexibilizar requisitos;
- substituir processos oficiais.

No atendimento autônomo, a IA deverá seguir os padrões de fechamento definidos pelo sistema.

Princípio:

> **A cognição pode identificar algo que o fluxo não percebeu; não pode decidir que uma proteção do fluxo deixou de ser necessária.**

---

## D04-08 — Divergência identificada após o fechamento

Depois que um pedido tiver sido fechado, a IA poderá identificar uma possível divergência entre:

- o que foi comunicado ao cliente;
- o que foi prometido;
- a conversa;
- o orçamento;
- o pedido efetivamente registrado;
- prazo oficial;
- condição comercial;
- demais informações relacionadas.

Quando isso ocorrer, a IA deverá:

1. identificar claramente a divergência;
2. preservar as evidências relevantes;
3. alertar o humano responsável;
4. apresentar o contexto necessário à avaliação.

A IA não poderá autonomamente:

- alterar o pedido para fazê-lo corresponder à conversa;
- decidir qual versão é correta;
- criar nova condição;
- renegociar preço;
- renegociar prazo;
- comunicar ao cliente uma correção extraordinária antes da avaliação humana.

Essa restrição permanece válida inclusive quando o atendimento autônomo estiver habilitado.

Princípio:

> **Autonomia para conversar com clientes não concede autoridade para resolver excepcionalidades comerciais pós-fechamento.**

---

# 4. Dois regimes de flexibilidade comercial

O D04 estabelece uma diferença estrutural entre atendimento humano e atendimento autônomo.

## 4.1 Atendimento humano

```text
Condições do pedido
       ↓
IA analisa
       ↓
Situação incomum?
   ┌───┴───┐
  não     sim
   │        │
segue    IA pergunta
normal   se está correto
            │
            ↓
       humano avalia
            │
            ↓
  flexibilidade conforme
  autoridade e regras
```

O humano poderá possuir discricionariedade legítima dentro das permissões do sistema.

## 4.2 Atendimento autônomo

```text
Necessidade do cliente
        ↓
Parâmetros comerciais autorizados
        ↓
IA encontra solução dentro deles?
   ┌────┴────┐
  sim       não
   │          │
oferece     tenta alternativa
solução     autorizada
              │
       ainda exige exceção?
          ┌───┴───┐
         não     sim
          │        │
       continua  humano
```

A IA possui flexibilidade cognitiva para encontrar soluções **dentro das regras**, mas não discricionariedade para criar exceções.

---

# 5. Preço e prazo como fronteiras de autoridade

Preço e prazo merecem tratamento explícito porque são elementos comerciais com impacto direto.

A IA poderá conhecer, explicar e utilizar os valores e prazos autorizados.

Mas não poderá decidir:

```text
"Vou reduzir o preço para fechar."

"Vou prometer um prazo menor porque o cliente insistiu."

"Esse cliente compra muito, então posso dar desconto."

"Vários clientes pediram isso, então vou começar a oferecer."
```

Essas decisões permanecem humanas enquanto envolverem negociação ou excepcionalidade.

---

# 6. Excepcionalidade não é erro

Uma condição fora do padrão não deverá ser automaticamente tratada como erro.

O D04 distingue:

```text
FORA DO PADRÃO
      │
      ├── pode ser flexibilidade humana legítima
      │
      ├── pode ser erro
      │
      └── pode ser excepcionalidade que exige decisão
```

Durante atendimento humano, a IA poderá chamar a atenção e perguntar se está correto.

Durante atendimento autônomo, a IA deverá permanecer dentro dos parâmetros autorizados e encaminhar aquilo que realmente exigir exceção.

---

# 7. Aprendizado a partir de demandas comerciais

Solicitações recorrentes poderão gerar evidências para aprendizado.

Exemplo:

```text
Muitos clientes solicitam prazo menor
            ↓
        observação
            ↓
       padrão recorrente
            ↓
      hipótese comercial
            ↓
 análise / eventual proposta
            ↓
 decisão humana sobre parâmetros
```

O fluxo proibido é:

```text
Muitos clientes solicitaram
            ↓
IA passa a conceder
automaticamente
```

O Mheibos poderá aprender sobre o mercado sem conceder à IA autoridade comercial que nunca foi autorizada.

---

# 8. Relação com D03 — Atendimento e CRM

O D04 depende das fronteiras estabelecidas no D03.

Enquanto o atendimento autônomo estiver desativado, a IA poderá auxiliar o vendedor, mas não responder diretamente ao cliente.

Quando o atendimento autônomo estiver explicitamente habilitado conforme as regras do D03, as decisões do D04 passam a definir parte importante do que a IA poderá ou não fazer durante a venda.

Portanto:

```text
D03
Autoridade para falar com cliente
        +
D04
Autoridade comercial dentro da conversa
```

Autorizar atendimento autônomo não equivale a autorizar negociação ou excepcionalidades.

---

# 9. Relação com D01 — Interface e UX

Durante vendas humanas, a IA poderá utilizar as capacidades do D01 para:

- chamar atenção para excepcionalidades;
- perguntar se algo está correto;
- mostrar divergências;
- apresentar informações no painel lateral;
- oferecer ações contextuais;
- evitar interrupções excessivas;
- preservar o foco do vendedor.

A análise cognitiva comercial deverá respeitar o princípio da menor interrupção eficaz.

---

# 10. Estado deste documento

O D04 está **encerrado como inventário inicial de decisões candidatas**, contendo exatamente oito decisões consolidadas:

1. **D04-01** — Análise cognitiva de excepcionalidades comerciais;
2. **D04-02** — Encaminhamento de excepcionalidade comercial para atendimento humano;
3. **D04-03** — Escolha autônoma de alternativas comerciais autorizadas;
4. **D04-04** — Proibição de negociação autônoma de preço e prazo;
5. **D04-05** — Recomendações comerciais contextualmente justificadas;
6. **D04-06** — Uso do histórico do cliente para oportunidades comerciais;
7. **D04-07** — Avaliação cognitiva complementar antes do fechamento;
8. **D04-08** — Divergência identificada após o fechamento.

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
