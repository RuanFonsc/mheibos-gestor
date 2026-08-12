# MHEIBOS INTELLIGENT OPERATING SYSTEM

# D10 — Conhecimento, Memória e Aprendizado
## Inventário de Decisões Cognitivas Candidatas ao Catálogo de Decisões Autônomas

**Status:** Proposta consolidada para revisão e aprovação humana  
**Domínio:** D10 — Conhecimento, Memória e Aprendizado  
**Natureza:** Inventário de decisões candidatas; não altera nem substitui as RFCs oficiais  
**Base principal:** RFC-0011 — Conhecimento, Memória e Aprendizado; RFC-0004 — Arquitetura Cognitiva; decisões D01–D09 já consolidadas.

---

## 1. Objetivo

Este documento propõe, sem nova rodada de perguntas, as decisões do D10 necessárias para completar o inventário cognitivo do Mheibos.

A proposta segue as regras já estabelecidas na documentação oficial:

- conhecimento, memória, observação, hipótese e ensinamento possuem autoridades diferentes;
- a IA não é fonte oficial;
- persistência não equivale a verdade;
- ensinamentos não se tornam conhecimento oficial automaticamente;
- promoção para uso oficial por terceiros exige validação humana autorizada;
- aprendizado deve permanecer privado/local à empresa na primeira versão;
- o Mheibos aprende com acertos, erros, improvisações e uso do próprio produto sem transformar correlação em causalidade;
- permissões e escopos continuam valendo durante recuperação, aprendizado e memória.

Princípio central:

> **A IA pode descobrir, organizar, lembrar, relacionar e propor conhecimento; ela não pode transformar sozinha uma observação, hipótese, ensinamento ou padrão em verdade oficial.**

---

# 2. D10-01 — Recuperação autônoma do menor contexto suficiente

A IA poderá recuperar autonomamente conhecimento e memória aos quais o usuário e a tarefa atual tenham acesso, quando isso for necessário para compreender a situação ou produzir uma resposta adequada.

A recuperação deverá:

- respeitar permissões;
- respeitar escopo;
- considerar autoridade;
- considerar vigência;
- preferir o menor contexto suficiente;
- evitar investigação infinita;
- preservar a origem das informações relevantes.

A IA não precisa pedir autorização a cada consulta normal de contexto que já esteja dentro das permissões e da finalidade atual.

Investigações extraordinariamente amplas continuam sujeitas às regras de consentimento e governança previstas na documentação oficial.

> **Permissão para responder não significa permissão irrestrita para investigar tudo.**

---

# 3. D10-02 — Persistência seletiva de memória sem armazenar tudo

A IA poderá identificar conteúdos candidatos à memória de longo prazo quando houver utilidade futura clara, origem identificável e escopo apropriado.

Podem ser candidatos, conforme as regras oficiais:

- decisões relevantes;
- preferências duráveis autorizadas;
- contexto necessário à continuidade;
- aprendizados de missão;
- soluções úteis;
- problemas recorrentes;
- informações consolidadas de relacionamento;
- padrões operacionais ainda corretamente classificados.

A IA não deverá promover indiscriminadamente todo conteúdo de sessão para memória longa.

Não deverão ser persistidos automaticamente como memória durável:

- conversa casual;
- emoção momentânea;
- rascunho descartado;
- hipótese transitória;
- sugestão rejeitada;
- dado sensível sem finalidade;
- informação fora do escopo.

A persistência deverá manter a classificação epistêmica original.

> **Lembrar não significa declarar verdadeiro.**

---

# 4. D10-03 — Consolidação de ocorrências em padrões sem promoção automática

A IA poderá consolidar múltiplas ocorrências semelhantes em um padrão ou observação estruturada quando houver evidência suficiente para justificar a relação.

A consolidação deverá:

- preservar referências às evidências;
- registrar contexto;
- evitar generalização indevida;
- distinguir frequência de causalidade;
- manter o resultado como observação, padrão ou hipótese conforme o caso.

Um padrão detectado não se torna automaticamente:

- regra;
- procedimento;
- boa prática;
- conhecimento oficial;
- característica permanente de um usuário.

> **Repetição gera evidência para análise; não gera autoridade normativa.**

---

# 5. D10-04 — Formulação autônoma de hipóteses e detecção de conflitos

A IA poderá formular hipóteses a partir de fatos, memória, padrões e conhecimento recuperado.

Também poderá identificar:

- conflito entre fontes;
- conhecimento possivelmente desatualizado;
- ensinamento incompatível com regra oficial;
- divergência entre memória e estado atual;
- duplicação;
- lacuna de informação;
- necessidade de validação adicional.

A IA deverá explicitar, conforme aplicável:

- fatos;
- inferências;
- hipótese;
- fontes;
- autoridade das fontes;
- confiança;
- incerteza;
- conflito encontrado.

A IA não poderá resolver um conflito de autoridade simplesmente escolhendo a versão que considere mais plausível quando a hierarquia normativa ou validação humana for necessária.

> **A IA pode descobrir o conflito; a autoridade aplicável decide o que prevalece quando a documentação não resolver deterministicamente.**

---

# 6. D10-05 — Avaliação preliminar de ensinamentos e candidatos a conhecimento

A IA poderá analisar autonomamente ensinamentos fornecidos por usuários e outros conteúdos candidatos à promoção.

A avaliação poderá examinar:

- clareza;
- completude;
- coerência;
- evidências;
- duplicação;
- conteúdo semelhante;
- conflito com conhecimento oficial;
- conflito com princípios;
- risco operacional;
- risco financeiro;
- risco de segurança;
- escopo;
- generalização indevida;
- necessidade de especialista.

A IA poderá classificar o candidato como, por exemplo:

- aparentemente coerente;
- incompleto;
- duplicado;
- conflitante;
- potencialmente arriscado;
- específico demais;
- candidato a recomendação;
- candidato a procedimento;
- necessitando informação adicional.

Essa classificação serve para **organizar a validação humana**.

> **Avaliação preliminar da IA nunca equivale a aprovação.**

---

# 7. D10-06 — Proibição absoluta de promoção autônoma a conhecimento oficial

A IA não poderá promover autonomamente observações, hipóteses, improvisações, ensinamentos, padrões ou recomendações para **conhecimento oficial destinado a orientar outros usuários**.

Isso permanece válido mesmo quando:

- o padrão se repete muitas vezes;
- o resultado observado parece positivo;
- a confiança da IA supera 95%;
- vários usuários fazem a mesma coisa;
- não houve reclamações;
- o conteúdo está sendo usado há muito tempo;
- a IA considera a prática claramente superior.

Conhecimento destinado a uso oficial por terceiros deverá passar pela validação humana autorizada prevista na RFC-0011.

Tempo decorrido, repetição e ausência de revisão não constituem aprovação silenciosa.

> **A IA pode propor promoção; somente a autoridade humana aplicável pode oficializar.**

Esta regra não impede persistência privada ou operacional em estados não oficiais quando a RFC permitir.

---

# 8. D10-07 — Aprendizado com humanos sem copiar práticas ruins nem autoridade

A IA poderá aprender com:

- acertos;
- erros;
- improvisações;
- decisões humanas;
- resultados posteriores;
- uso da interface;
- formas de recuperação de problemas;
- boas soluções emergentes.

Entretanto, comportamento humano observado não deverá ser copiado automaticamente.

O Mheibos deverá avaliar a prática diante de:

- regras obrigatórias;
- segurança;
- processo;
- qualidade;
- resultado;
- contexto;
- boas práticas;
- evidências.

Especialmente no atendimento, o fato de humanos:

- pularem etapas;
- cometerem erros;
- escreverem incorretamente;
- improvisarem;
- utilizarem práticas inadequadas;

não autoriza a IA a aprender essas práticas como comportamento desejável.

Uma improvisação poderá ser útil e candidata a recomendação, mas deverá preservar o contexto e passar pela governança compatível com seu impacto.

> **O Mheibos aprende com humanos; não imita humanos indiscriminadamente.**

E:

> **Aprender com a decisão de alguém não transfere para a IA a autoridade daquela pessoa.**

---

# 9. D10-08 — Aprendizado orientado primeiro à assistência e melhoria

Quando o aprendizado detectar erros recorrentes, dificuldades, fricções ou padrões problemáticos, sua finalidade primária deverá ser:

1. ajudar o usuário a fazer o correto;
2. prevenir repetição;
3. melhorar orientação;
4. melhorar interface ou processo quando aplicável;
5. gerar hipótese de causa raiz;
6. sugerir treinamento ou melhoria quando necessário.

O aprendizado não deverá ser estruturado primariamente como mecanismo de vigilância, julgamento pessoal ou punição.

Uma ocorrência isolada não deverá se tornar característica permanente de uma pessoa.

Quando houver omissões claras, persistentes e operacionalmente relevantes, as regras de escalada já definidas nos outros domínios poderão ser aplicadas.

A IA poderá ainda aprender sobre o próprio produto a partir de sinais como:

- campos frequentemente corrigidos;
- sequências repetitivas;
- etapas confusas;
- funções difíceis de encontrar;
- excesso de cliques;
- erros de navegação;
- pedidos repetidos de ajuda.

Esse aprendizado poderá gerar propostas e adaptações apenas dentro das autoridades definidas pelos domínios proprietários, especialmente o D09.

> **Aprendizado identifica oportunidades; não concede automaticamente autoridade para aplicar a mudança.**

---

# 10. Hierarquia epistêmica obrigatória

O Mheibos deverá preservar diferenças explícitas entre categorias como:

```text
REGRA / CONHECIMENTO OFICIAL
            ↑
     validação autorizada
            ↑
RECOMENDAÇÃO / CONHECIMENTO EMERGENTE
            ↑
       avaliação
            ↑
PADRÃO / OBSERVAÇÃO / ENSINAMENTO
            ↑
       evidências
            ↑
FATOS E EVENTOS
```

Hipóteses e inferências da IA permanecem identificadas como tais e não atravessam essa hierarquia apenas por confiança estatística.

---

# 11. Autoridade, vigência e conflito

Ao recuperar ou utilizar conhecimento, a IA deverá considerar não apenas similaridade ou relevância semântica, mas também:

- autoridade;
- escopo;
- vigência;
- origem;
- validação;
- permissões;
- finalidade atual.

Conteúdo desatualizado não deverá ser apresentado como regra atual.

Conteúdo persistente não deverá prevalecer sobre fonte oficial atual apenas por estar na memória há mais tempo.

Quando uma informação nova corrigir uma anterior, a correção deverá preservar rastreabilidade e não apagar silenciosamente a origem histórica.

---

# 12. Privacidade e isolamento

O aprendizado inicial do Mheibos permanecerá privado e local à empresa.

Não haverá compartilhamento automático entre empresas de:

- conversas;
- procedimentos;
- dados operacionais;
- padrões;
- erros;
- métricas;
- ensinamentos;
- memórias;
- conhecimento institucional.

Qualquer aprendizado global futuro exigirá decisão normativa específica.

Memórias individuais, de missão, relacionamento e empresa deverão manter seus respectivos escopos.

---

# 13. Relação com os demais domínios

O D10 não concede novas autoridades operacionais aos demais domínios.

Exemplos:

- aprender uma prática financeira não autoriza decisão financeira;
- aprender um padrão de interface não autoriza experimentação ilimitada;
- aprender com arquivos não autoriza analisar arte;
- aprender com atendimento não autoriza responder clientes sem a permissão já exigida;
- aprender com missão não remove barreiras de segurança;
- aprender com operação offline não amplia a função da IA local.

> **Aprendizado melhora competência dentro da autoridade existente; não cria autoridade nova.**

---

# 14. Estado deste documento

O D10 é apresentado para **revisão e aprovação humana**, contendo oito decisões propostas:

1. **D10-01** — Recuperação autônoma do menor contexto suficiente;
2. **D10-02** — Persistência seletiva de memória sem armazenar tudo;
3. **D10-03** — Consolidação de ocorrências em padrões sem promoção automática;
4. **D10-04** — Formulação autônoma de hipóteses e detecção de conflitos;
5. **D10-05** — Avaliação preliminar de ensinamentos e candidatos a conhecimento;
6. **D10-06** — Proibição absoluta de promoção autônoma a conhecimento oficial;
7. **D10-07** — Aprendizado com humanos sem copiar práticas ruins nem autoridade;
8. **D10-08** — Aprendizado orientado primeiro à assistência e melhoria.

As decisões foram propostas conservadoramente a partir das regras já estabelecidas na RFC-0011, RFC-0004 e decisões D01–D09.

Nenhum trecho deste documento deverá ser interpretado como alteração automática das RFCs oficiais.

> **A IA pode aprender cada vez mais; sua autoridade continua sendo determinada pelo Mheibos.**
