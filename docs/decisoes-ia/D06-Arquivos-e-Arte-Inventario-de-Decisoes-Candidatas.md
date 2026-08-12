# MHEIBOS INTELLIGENT OPERATING SYSTEM

# D06 — Arquivos e Arte
## Inventário de Decisões Cognitivas Candidatas ao Catálogo de Decisões Autônomas

**Status:** Consolidado para etapa posterior de classificação  
**Domínio:** D06 — Arquivos e Arte  
**Natureza:** Inventário de decisões candidatas — não constitui, por si só, autorização autônoma final

---

## 1. Objetivo

Este documento consolida as oito decisões do **Domínio 06 — Arquivos e Arte** para o futuro Catálogo de Decisões Autônomas da IA do Mheibos.

O domínio estabelece uma fronteira deliberadamente restritiva: o Mheibos poderá administrar e compreender o **contexto operacional dos arquivos**, mas não deverá interpretar visualmente a arte nem assumir responsabilidades que pertencem ao designer ou ao usuário responsável.

> **O Mheibos administra o contexto operacional dos arquivos, mas não analisa a arte.**

---

## 2. Delimitações transversais

### 2.1 Sem análise visual da arte

Fica descartada, neste domínio, a utilização da IA para analisar cognitivamente o conteúdo visual dos arquivos de arte.

O Mheibos não deverá usar a IA para:

- interpretar visualmente arquivos `.cdr`;
- avaliar estética ou composição;
- procurar elementos gráficos cortados;
- avaliar margens visuais;
- interpretar temas pela imagem;
- comparar visualmente artes;
- determinar pela aparência qual arquivo pertence a determinado pedido;
- substituir a análise do designer.

Não se pressupõe pipeline de visão computacional ou renderização de arquivos para avaliação pela IA.

### 2.2 Validações objetivas permanecem determinísticas

Condições que o sistema consiga verificar objetivamente deverão permanecer na lógica determinística do Mheibos.

> **Se uma condição de arquivos pode ser determinada objetivamente pelo estado do sistema ou do processo, ela pertence à lógica determinística do Mheibos, não ao catálogo cognitivo da IA.**

---

# 3. Decisões consolidadas

## D06-01 — Alerta sobre possível incompatibilidade contextual de vínculo

Quando existirem evidências estruturadas suficientes para indicar uma possível incompatibilidade entre o vínculo registrado e o contexto do pedido, a IA poderá chamar a atenção do usuário.

Ela poderá apresentar a inconsistência percebida, explicar quais informações estruturadas motivaram a suspeita e perguntar se o vínculo está correto.

A IA não poderá autonomamente:

- desvincular;
- substituir;
- mover;
- renomear;
- determinar visualmente que outra arte é a correta.

A intervenção é de **alerta e conferência humana**, não de correção autônoma.

---

## D06-02 — Confirmação humana para criação ou restauração de vínculo

Quando um vínculo estiver ausente, perdido ou precisar ser restaurado, qualquer associação efetiva entre um arquivo e um pedido dependerá de confirmação humana.

A IA não deverá assumir que determinado arquivo é correto apenas com base em inferência probabilística.

Caso informações estruturadas já existentes permitam apontar um candidato contextual, isso poderá ser apresentado como auxílio, mas a decisão efetiva de vínculo permanece humana.

Esta decisão deve ser interpretada em conjunto com a D06-05:

> **A IA não analisa o conteúdo dos arquivos para determinar qual arte é a correta.**

---

## D06-03 — Sem inferência cognitiva sobre o conjunto ou conteúdo das artes

O Mheibos não deverá criar uma camada cognitiva dedicada a inferir se o conjunto de arquivos de um pedido está artística ou semanticamente correto.

Nesse aspecto, deverão prevalecer:

- regras determinísticas;
- vínculos registrados;
- estados do processo;
- propriedades objetivas;
- conferência humana.

A IA não deverá tentar concluir, por exemplo, que existem “arquivos demais” por expectativa cognitiva, que uma arte parece pertencer a outro contexto por análise visual ou que uma arte está visualmente incorreta.

---

## D06-04 — Pendências objetivas pertencem aos mecanismos determinísticos

Quando o Mheibos já possuir informação objetiva suficiente para determinar que existe uma pendência de arquivo, a IA não deverá criar uma previsão cognitiva redundante.

```text
Etapa do processo
        ↓
Arquivo deveria estar vinculado
        ↓
Vínculo não existe
        ↓
Regra determinística do Mheibos
        ↓
Alerta / bloqueio / tratamento aplicável
```

A IA poderá auxiliar posteriormente quando houver motivo, conforme a D06-06.

---

## D06-05 — Determinação do arquivo correto permanece humana

Quando o arquivo esperado estiver ausente, inacessível, perdido ou com vínculo inválido, a IA não deverá investigar arquivos candidatos para decidir qual deles é a arte correta.

Depois que os mecanismos determinísticos de busca, varredura ou recuperação previstos pelo Mheibos não resolverem a situação, a análise deverá ser realizada pelo usuário.

A IA poderá ajudar a alertar sobre:

- ausência do arquivo correto;
- vínculo quebrado;
- pendência;
- necessidade de intervenção.

Mas não deverá:

- analisar visualmente arquivos candidatos;
- ranquear artes pela aparência;
- escolher qual arte pertence ao pedido;
- restaurar autonomamente o vínculo;
- substituir a conferência humana.

> **O Mheibos gerencia a existência, vínculo e integridade operacional dos arquivos; não interpreta a arte para decidir qual arquivo está correto.**

---

## D06-06 — Assistência cognitiva somente após insuficiência do alerta normal

Quando uma pendência de arquivo for detectada deterministicamente, o próprio alerta normal do Mheibos deverá ser o primeiro mecanismo de orientação.

Se o alerta já informa o problema e orienta sua resolução, a IA não deverá duplicar imediatamente a mesma informação pelo painel lateral.

A IA poderá intervir adicionalmente quando o usuário:

- ignorar o alerta;
- não responder adequadamente;
- demonstrar dificuldade;
- continuar sem tratar a pendência quando aplicável.

Nesse momento, a IA poderá chamar novamente a atenção e contextualizar a importância da pendência, mas continuará sem escolher o arquivo correto, analisar a arte, resolver o vínculo pelo usuário ou mover arquivos.

> **Alerta estrutural primeiro; assistência cognitiva adicional somente quando houver motivo.**

---

## D06-07 — Assistência antes de escalada gerencial por omissões recorrentes

Problemas recorrentes relacionados a arquivos não deverão ser tratados primariamente como mecanismo de fiscalização do usuário.

A prioridade da IA será **ajudar o usuário a cumprir corretamente o fluxo**.

### Estágio 1 — Ocorrência normal

O próprio Mheibos apresenta os alertas determinísticos aplicáveis. A IA não precisa duplicar a intervenção.

### Estágio 2 — Alerta ignorado ou dificuldade

A IA poderá intervir para chamar atenção e ajudar o usuário a fazer o correto.

### Estágio 3 — Reincidência

A IA poderá intensificar a assistência contextual, buscando reduzir a repetição do problema.

A reincidência isoladamente não deverá ser tratada imediatamente como motivo para escalar o usuário.

### Estágio 4 — Omissões claras e persistentes

Quando houver evidências suficientes de que o usuário repetidamente deixa de cumprir uma obrigação apesar dos alertas, orientações e assistência, a IA poderá escalar a situação para a gerência.

Essa escalada deverá ser apresentada como **problema operacional persistente que não está sendo resolvido pela assistência normal**, e não como mecanismo punitivo ou de vigilância.

> **A finalidade primária é corrigir o problema, não vigiar o funcionário. Escalar para a gerência é uma medida posterior diante de omissões claras e recorrentes.**

Não deverá existir necessariamente uma regra simplista como `3 erros = avisar gerente`. O contexto importa.

---

## D06-08 — Proibição de movimentação autônoma de arquivos de arte

A IA nunca poderá mover autonomamente arquivos de arte.

Isso permanece válido mesmo quando:

- o diretório correto pareça evidente;
- a IA possua confiança elevada;
- a movimentação pareça reversível;
- o arquivo tenha sido criado pelo próprio Mheibos;
- a organização atual pareça inadequada.

Operações físicas de movimentação deverão seguir exclusivamente os mecanismos, fluxos, permissões e autorizações oficiais do Mheibos.

A IA poderá alertar sobre uma situação relevante, mas não reorganizará diretórios por conta própria.

---

# 4. Hierarquia de tratamento

```text
Problema objetivo
      ↓
Regra determinística
      ↓
Alerta normal do Mheibos
      ↓
Usuário resolve?
   ┌──┴──┐
  sim   não
   │     │
 fim    IA pode ajudar
             ↓
      problema persiste?
          ┌──┴──┐
         não   sim
          │     │
         fim  assistência adicional
                    ↓
             omissão clara e persistente?
                 ┌──┴──┐
                não   sim
                 │     │
              ajuda   possível escalada
                      à gerência
```

A IA não deverá competir com os próprios mecanismos de alerta do sistema.

---

# 5. Fronteiras de autoridade

A IA do D06 pode:

- chamar atenção;
- contextualizar;
- explicar;
- ajudar após alertas ignorados;
- identificar possível incompatibilidade contextual com base em informações estruturadas;
- escalar omissões claras e persistentes quando a assistência normal falhar.

A IA do D06 não pode:

- analisar visualmente a arte;
- avaliar estética;
- escolher qual arte é correta;
- substituir a conferência do designer;
- mover arquivos autonomamente;
- renomear arquivos;
- corrigir vínculos autonomamente;
- criar inferências desnecessárias quando uma regra determinística já resolve a situação.

---

# 6. Estado deste documento

O D06 está **encerrado como inventário inicial de decisões candidatas**, contendo exatamente oito decisões consolidadas:

1. **D06-01** — Alerta sobre possível incompatibilidade contextual de vínculo;
2. **D06-02** — Confirmação humana para criação ou restauração de vínculo;
3. **D06-03** — Ausência de inferência cognitiva sobre o conjunto ou conteúdo das artes;
4. **D06-04** — Pendências objetivas de arquivos pertencem aos mecanismos determinísticos;
5. **D06-05** — Determinação do arquivo correto permanece humana;
6. **D06-06** — Assistência cognitiva somente após insuficiência do alerta normal;
7. **D06-07** — Assistência prioritária antes de escalada gerencial por omissões recorrentes;
8. **D06-08** — Proibição de movimentação autônoma de arquivos de arte.

Fica registrada a delimitação transversal:

> **O Mheibos administra o contexto operacional dos arquivos, mas não analisa a arte.**

O próximo tratamento previsto pelo Plano-Modelo deverá verificar sobreposições normativas, separar cognição de automação determinística, identificar proibições, classificar risco/alcance/reversibilidade, aplicar regras de confiança, definir confirmação e auditoria, testar cenários extremos e somente então promover decisões aprovadas ao Catálogo de Decisões Autônomas.
