# MHEIBOS INTELLIGENT OPERATING SYSTEM

# D09 — Interface Viva e Intervenções
## Inventário de Decisões Cognitivas Candidatas ao Catálogo de Decisões Autônomas

**Status:** Consolidado para etapa posterior de classificação  
**Domínio:** D09 — Interface Viva e Intervenções  
**Natureza:** Inventário de decisões candidatas — não constitui, por si só, autorização autônoma final  
**Base normativa relacionada:** RFC-0009 — Interface Viva e Intervenções; arquitetura cognitiva; governança da IA; decisões anteriores sobre personalização individual, painel lateral e reversibilidade.

---

## 1. Objetivo

Este documento consolida as oito decisões do **Domínio 09 — Interface Viva e Intervenções** para o futuro Catálogo de Decisões Autônomas da IA do Mheibos.

O domínio trata de quando e como a IA pode:

- intervir preventivamente;
- interromper o usuário;
- inferir objetivos a partir da navegação;
- criar facilitações individuais;
- avaliar suas próprias adaptações;
- reverter adaptações;
- aprender sem transformar a interface em experimento permanente;
- respeitar rejeições do usuário;
- preservar reversibilidade.

A Interface Viva deve aumentar eficiência e reduzir erros sem produzir uma interface instável, invasiva ou excessivamente opinativa.

---

# 2. Decisão anterior já coberta — adaptação comportamental da interface

Durante a discussão do D09 foi inicialmente levantada a possibilidade de a IA identificar dificuldades recorrentes de uso e adaptar autonomamente aspectos permitidos da interface individual.

Essa autoridade **já estava prevista na documentação e nas decisões anteriores da Interface Viva**.

Inclui, dentro das limitações já estabelecidas:

- destacar informações;
- reorganizar elementos permitidos;
- criar botões flutuantes;
- facilitar acesso a ações;
- adaptar a apresentação conforme comportamento e necessidade do usuário.

Essa decisão anterior não deverá ser duplicada como nova autorização independente.

O D09 detalha casos específicos e limites dessa autoridade.

---

# 3. Decisões consolidadas

## D09-01 — Intervenção preventiva diante de provável erro não determinístico

A IA não deverá criar alertas simplesmente porque considera que o humano **pode** estar prestes a errar.

Quando uma ação for válida segundo as regras determinísticas do sistema, uma intervenção preventiva baseada apenas em interpretação cognitiva exigirá:

> **confiança igual ou superior a 95% de que existe uma inconsistência real entre a ação e o contexto ou objetivo identificado.**

Quando esse limiar for atingido, a IA poderá:

- chamar a atenção;
- explicar concretamente a inconsistência percebida;
- apresentar as evidências relevantes;
- perguntar ao usuário se aquilo está correto.

A confiança cognitiva, por si só, **não autoriza bloqueio**.

Bloqueios continuam pertencendo às regras determinísticas e demais mecanismos oficiais do Mheibos.

A finalidade desta restrição é impedir que a IA produza uma sucessão de alertas baseados em suspeitas sobre possíveis erros humanos.

---

## D09-02 — Interrupção proativa somente com alta confiança e relevância temporal

A IA poderá interromper proativamente o usuário para apresentar uma informação descoberta durante sua atividade somente quando duas condições forem satisfeitas simultaneamente:

1. a IA possuir **mais de 95% de confiança** na informação ou conclusão que motiva a intervenção;
2. a informação for **materialmente relevante para a ação atual**, de modo que apresentá-la antes da conclusão produza benefício claro.

Portanto:

- confiança alta sem urgência/relevância temporal não basta;
- relevância alta com confiança insuficiente não basta.

Se a informação puder esperar, ela poderá permanecer no painel lateral ou ser apresentada em momento mais apropriado.

> **Alta confiança não basta para interromper. É necessária também relevância temporal suficiente.**

---

## D09-03 — Confirmação leve de intenção pelo painel lateral

Quando o comportamento do usuário sugerir que ele está procurando uma informação, funcionalidade ou tentando alcançar determinado objetivo, a IA poderá formular uma hipótese sobre essa intenção.

Nesse caso, não é necessário exigir confiança superior a 95% para qualquer aproximação.

A IA poderá perguntar de forma pouco intrusiva pelo **painel lateral**, por exemplo:

> “Você está tentando localizar o histórico deste cliente? Posso mostrar aqui.”

A IA não deverá apresentar a hipótese como certeza.

Se o usuário confirmar, ela poderá:

- apresentar a informação no próprio painel lateral;
- oferecer a ação necessária;
- auxiliar o usuário naquele objetivo.

Quando o painel lateral for suficiente, a IA deverá evitar mudar o usuário de tela desnecessariamente.

Quanto menor a confiança na hipótese, menor deverá ser a propensão da IA a perguntar, evitando transformar o painel lateral em uma sequência de palpites.

---

## D09-04 — Criação de facilitações individuais a partir de padrões legítimos

Quando a IA identificar um padrão legítimo e repetitivo de uso, poderá criar autonomamente facilitações individuais e reversíveis de interface.

Exemplos:

- botão flutuante;
- atalho contextual;
- acesso direto;
- outra facilitação permitida pela Interface Viva.

Essas adaptações não poderão:

- pular etapas;
- contornar permissões;
- esconder informações obrigatórias;
- alterar processos;
- modificar regras de negócio;
- alterar a autoridade do usuário.

O usuário deverá continuar podendo retornar à visualização padrão.

Esta decisão constitui uma aplicação explícita da autoridade de adaptação comportamental já prevista anteriormente para a Interface Viva.

---

## D09-05 — Reversão de adaptação malsucedida com limite de estabilidade

Quando a IA realizar legitimamente uma adaptação individual e posteriormente existirem evidências suficientes de que ela piorou a experiência, a IA poderá reverter autonomamente a própria adaptação.

Poderá retornar:

- ao estado anterior;
- à visualização padrão;
- a outro estado estável previamente válido, quando aplicável.

Entretanto, a reversão deverá **encerrar aquele ciclo adaptativo**.

O fluxo esperado é:

```text
observar
   ↓
adaptar
   ↓
avaliar
   ↓
manter OU reverter
   ↓
estabilizar
```

A IA não poderá ficar:

```text
adaptando
   ↓
revertendo
   ↓
adaptando novamente
   ↓
revertendo novamente
   ↓
...
```

para a mesma necessidade e contexto.

Uma nova adaptação equivalente somente poderá ocorrer diante de:

- mudança relevante de contexto; ou
- nova evidência suficientemente diferente.

> **A Interface Viva pode aprender com uma adaptação ruim e desfazê-la, mas não pode transformar a interface em um experimento permanente.**

---

## D09-06 — Proibição de experimentação autônoma da interface

A Interface Viva não poderá alterar a interface apenas para:

- experimentar;
- executar teste A/B;
- coletar evidências;
- observar reação;
- descobrir se uma hipótese de design funciona.

Toda adaptação deverá possuir **justificativa operacional anterior**, baseada em necessidade, objetivo ou padrão já identificado.

O usuário não deverá ser transformado em objeto permanente de experimentação da Interface Viva.

> **A Interface Viva aprende com adaptações justificadas; não cria adaptações apenas para aprender.**

---

## D09-07 — Ausência de uso não equivale a rejeição

Quando uma adaptação individual tiver sido criada legitimamente e não estiver causando prejuízo, o simples fato de o usuário ainda não utilizá-la não constitui evidência suficiente para removê-la.

O usuário pode:

- ainda não ter precisado da função;
- não ter tido oportunidade de utilizá-la;
- não ter percebido a facilitação;
- utilizá-la apenas em situações pouco frequentes.

Portanto:

> **Não usar não significa rejeitar.**

Uma adaptação poderá permanecer disponível enquanto:

- não estiver causando prejuízo;
- não estiver atrapalhando a interface;
- não tiver sido explicitamente recusada pelo usuário.

Baixo uso isoladamente não deverá iniciar um novo ciclo de substituição por outras adaptações.

> **Inutilidade aparente não é prejuízo.**

Se houver evidência de prejuízo, aplica-se a D09-05.

Se houver rejeição explícita, aplica-se a D09-08.

---

## D09-08 — Rejeição persistente e reversível de adaptações

Quando o usuário explicitamente:

- remover;
- recusar;
- desativar;
- pedir para não utilizar

uma adaptação criada pela Interface Viva, essa rejeição deverá tornar-se uma **preferência individual persistente**.

A IA não deverá reapresentar autonomamente:

- a mesma adaptação;
- uma adaptação funcionalmente equivalente criada apenas para contornar a recusa;

no mesmo contexto.

Entretanto:

> **A própria ação de reverter também precisa ser reversível.**

A rejeição não cria uma proibição eterna e imutável.

O usuário deverá poder posteriormente:

- mudar de ideia;
- restaurar a adaptação;
- permitir novamente aquele tipo de intervenção;
- desfazer sua própria rejeição.

A IA não poderá interpretar essa reversibilidade como autorização para insistir.

Depois da rejeição:

> **Quem reabre aquela possibilidade é o usuário.**

Fluxo:

```text
IA adapta
   ↓
usuário pode reverter
   ↓
IA respeita
   ↓
usuário pode reverter a própria reversão
```

---

# 4. Regra de confiança para intervenções

O D09 estabelece uma diferença importante entre tipos de intervenção.

## 4.1 Suspeita de erro

Para alertar preventivamente sobre uma ação válida que a IA considera provavelmente errada:

> **confiança ≥95%**

Abaixo disso, a IA não deverá perturbar o usuário com suspeitas preventivas de erro.

## 4.2 Interrupção por informação relevante

Para interromper proativamente:

> **confiança >95% + relevância temporal material**

Uma condição sem a outra não basta.

## 4.3 Hipótese leve de intenção

Para perguntar discretamente pelo painel lateral se o usuário está tentando atingir determinado objetivo, não é necessário o mesmo limiar rígido, pois a IA não afirma que sabe a intenção e não bloqueia/interrompe a ação.

Ainda assim, a frequência dessas perguntas deverá ser proporcional à qualidade da evidência para evitar palpites excessivos.

---

# 5. Princípio de estabilidade da Interface Viva

A Interface Viva deverá adaptar-se sem oscilar indefinidamente.

O comportamento desejado é:

```text
necessidade identificada
        ↓
adaptação justificada
        ↓
observação natural do efeito
        ↓
funcionou?
   ┌────┴────┐
  sim       não
   │         │
manter    reverter
             ↓
          estabilizar
```

A adaptação não deverá iniciar um ciclo permanente de testes.

---

# 6. Reversibilidade em múltiplos níveis

A reversibilidade deverá existir tanto para a ação da IA quanto para a ação humana de desfazê-la.

Isso significa:

1. a IA pode criar uma adaptação autorizada;
2. o usuário pode removê-la;
3. a IA respeita a remoção;
4. o usuário pode posteriormente desfazer sua própria remoção.

Assim, reversibilidade não significa que a IA pode insistir.

Significa que o **humano nunca fica preso permanentemente à decisão anterior de aceitar ou rejeitar uma personalização**.

---

# 7. O painel lateral como espaço preferencial para assistência cognitiva leve

Quando a IA puder ajudar sem alterar a navegação principal, o painel lateral deverá ser preferido.

Isso é especialmente importante quando:

- a IA está confirmando uma hipótese;
- o usuário parece procurar informação;
- a informação pode ser apresentada sem mudar de tela;
- a assistência não exige intervenção estrutural.

A Interface Viva não deverá movimentar o usuário entre telas quando a informação necessária puder ser oferecida adequadamente pelo painel lateral.

---

# 8. Separação entre adaptação e processo

A autoridade para adaptar a interface não concede autoridade para modificar a operação subjacente.

Uma adaptação visual ou funcional permitida não poderá:

- remover obrigação;
- eliminar etapa;
- contornar bloqueio;
- modificar regra de produção;
- alterar coleta obrigatória de dados;
- alterar permissão;
- reduzir requisito de segurança;
- mudar decisão normativa.

A Interface Viva adapta **como o usuário interage com o sistema**, não as obrigações fundamentais do sistema.

---

# 9. Estado deste documento

O D09 está **encerrado como inventário inicial de decisões candidatas**, contendo exatamente oito decisões consolidadas:

1. **D09-01** — Intervenção preventiva diante de provável erro não determinístico;
2. **D09-02** — Interrupção proativa somente com alta confiança e relevância temporal;
3. **D09-03** — Confirmação leve de intenção pelo painel lateral;
4. **D09-04** — Criação de facilitações individuais a partir de padrões legítimos;
5. **D09-05** — Reversão de adaptação malsucedida com limite de estabilidade;
6. **D09-06** — Proibição de experimentação autônoma da interface;
7. **D09-07** — Ausência de uso não equivale a rejeição;
8. **D09-08** — Rejeição persistente e reversível de adaptações.

Ficam registradas como diretrizes transversais:

> **A IA não deve criar alertas preventivos sobre possíveis erros humanos com base em suspeitas fracas.**

> **Interromper exige alta confiança e relevância temporal.**

> **A Interface Viva adapta para resolver necessidades identificadas, não para experimentar.**

> **A interface deve estabilizar após adaptação ou reversão.**

> **Não usar não significa rejeitar.**

> **A rejeição do usuário deve ser respeitada, mas a própria reversão continua reversível pelo usuário.**

Antes de eventual promoção ao Catálogo de Decisões Autônomas, estas decisões deverão passar pelas etapas posteriores do Plano-Modelo: verificação de sobreposições normativas, separação entre cognição e automação determinística, identificação de proibições, classificação de risco/alcance/reversibilidade, aplicação das regras de confiança, confirmação e auditoria, testes de cenários extremos e confronto com as RFCs oficiais.
