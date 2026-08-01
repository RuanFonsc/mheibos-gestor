# MHEIBOS INTELLIGENT OPERATING SYSTEM

# RFC-0011 — Conhecimento, Memória e Aprendizado

**Status:** Draft para aprovação  
**Versão:** 0.1  
**Data:** 30/07/2026  
**Dependências:** RFC-0000, RFC-0001, RFC-0002, RFC-0003, RFC-0004, RFC-0005, RFC-0006, RFC-0007, RFC-0008, RFC-0009, RFC-0010  
**Fonte normativa:** Inventário Oficial de Decisões Arquiteturais — INV-073 a INV-084

---

## 1. Resumo

Esta RFC define como o Mheibos organiza, recupera, preserva, valida e evolui seu conhecimento.

O conhecimento do Mheibos não ficará armazenado dentro do modelo de linguagem. Informações sobre o produto, a empresa, a operação, os procedimentos, os clientes, os processos, as decisões e os aprendizados deverão existir em componentes próprios da plataforma, independentes do modelo utilizado. A substituição do modelo de IA não poderá apagar a inteligência acumulada pela instalação.

A base de conhecimento será organizada em camadas. Na primeira versão, deverão existir, no mínimo:

- conhecimento universal do Mheibos;
- conhecimento institucional da empresa;
- conhecimento operacional;
- memória de longo prazo;
- memória de curto prazo;
- contexto atual da interação.

Essas camadas permanecerão separadas por finalidade, autoridade, privacidade, validade e ciclo de vida, mas poderão ser consultadas em conjunto quando a situação exigir relações entre diferentes fontes.

O modelo de linguagem não poderá percorrer indiscriminadamente toda a memória da empresa. O próprio Mheibos controlará a recuperação de contexto, selecionando fontes relevantes, aplicando permissões, priorizando relações próximas, limitando profundidade, registrando a origem das informações e interrompendo a investigação quando houver contexto suficiente.

A primeira versão não utilizará um grafo geral de conhecimento como pilar cognitivo. O sistema partirá das relações determinísticas já existentes no domínio — como pertencimento, responsabilidade, dependência, bloqueio, autoria, sequência, estado e vínculo entre entidades — e somente ampliará a busca quando houver necessidade clara.

A memória de curto prazo será responsável pela continuidade imediata de sessões, conversas, telas, missões e trabalho diário. A memória de longo prazo consolidará conhecimento estável, histórico relevante, relacionamento com clientes, padrões operacionais, aprendizados aprovados e evolução organizacional.

O aprendizado inicial será privado e local à empresa. Acertos, erros, improvisações e padrões de uso poderão originar observações, hipóteses, recomendações ou propostas de melhoria. Nenhum ensinamento novo fornecido por um usuário será promovido automaticamente a conhecimento oficial. Ele deverá passar por avaliação preliminar e validação humana apropriada.

Práticas úteis poderão permanecer como procedimentos emergentes ou recomendações sem se tornarem regras obrigatórias. Futuramente, boas práticas aprovadas entre instalações poderão compor uma biblioteca optativa, jamais uma atualização automática imposta a todas as empresas.

---

## 2. Objetivo

Esta RFC responde às seguintes perguntas:

- onde o conhecimento do Mheibos deve existir;
- como impedir que o conhecimento fique preso a um modelo de linguagem;
- quais camadas de conhecimento e memória a plataforma deverá distinguir;
- como diferentes camadas poderão ser consultadas em conjunto;
- quem controla a recuperação do contexto enviado à IA;
- quais critérios deverão limitar profundidade, escopo e duração de uma investigação;
- por que a primeira versão não terá um grafo geral de conhecimento como fundamento;
- quando uma investigação ampla exige consentimento do usuário;
- como memória de curto prazo e memória de longo prazo se diferenciam;
- como conhecimento oficial se diferencia de observação, hipótese, recomendação e ensinamento pendente;
- como o Mheibos aprende com acertos, erros e improvisações;
- como o sistema aprende sobre a própria interface e o próprio produto;
- como um ensinamento humano entra em validação;
- como práticas emergentes podem ser úteis sem se tornarem obrigatórias;
- como o aprendizado permanece privado à empresa na primeira versão;
- como uma futura biblioteca global de boas práticas deverá funcionar;
- como permissões, auditoria, explicabilidade e governança se aplicam à memória.

Esta RFC não define o modelo de linguagem concreto, a tecnologia definitiva de busca semântica, o banco vetorial, o esquema físico de armazenamento, os prompts finais, a interface visual de administração do conhecimento ou a política completa de governança da IA. Essas escolhas pertencem à implementação ou a RFCs especializados, mas deverão respeitar as invariantes aqui estabelecidas.

---

## 3. Decisões fundamentais

A arquitetura de Conhecimento, Memória e Aprendizado adota as seguintes decisões:

1. O Mheibos possuirá uma base de conhecimento própria e externa ao modelo de linguagem.
2. Trocar o modelo de IA não poderá eliminar conhecimento, memória, procedimentos ou histórico acumulado.
3. Conhecimento será separado em camadas com finalidades, autoridades e ciclos de vida diferentes.
4. As camadas poderão ser consultadas em conjunto quando a questão exigir relações entre elas.
5. O Mheibos, e não o modelo, controlará a recuperação de contexto.
6. A recuperação deverá respeitar identidade, permissões, relevância, proximidade operacional, custo e critérios de parada.
7. O modelo não poderá explorar livremente todas as fontes da instalação.
8. Relações determinísticas do domínio serão a base inicial da recuperação.
9. Não haverá um grafo geral de conhecimento como pilar obrigatório da primeira versão.
10. Investigações amplas, lentas ou de maior custo deverão ser explicadas e dependerão de consentimento quando não forem necessárias à resposta imediata.
11. Memória de curto prazo e memória de longo prazo serão separadas.
12. A memória curta sustentará continuidade imediata e contexto transitório.
13. A memória longa consolidará conhecimento estável, histórico relevante e evolução organizacional.
14. O aprendizado da primeira versão permanecerá privado e local à empresa.
15. Acertos poderão reforçar recomendações e práticas úteis.
16. Erros poderão alimentar prevenção, assistência e melhoria.
17. Improvisações bem-sucedidas poderão ser registradas como soluções emergentes.
18. O Mheibos poderá aprender sobre o uso e as fricções do próprio produto.
19. Observação de uso não autoriza diagnóstico pessoal, vigilância indiscriminada ou julgamento depreciativo.
20. Conhecimento ensinado por usuários não se tornará oficial automaticamente.
21. Todo ensinamento deverá possuir origem, autor, contexto, estado de validação e histórico.
22. A IA poderá realizar avaliação preliminar de coerência, conflito, risco e evidência.
23. A promoção a conhecimento oficial para outros usuários dependerá de validação humana autorizada.
24. Procedimentos emergentes poderão ser sugeridos sem se tornarem obrigatórios.
25. Procedimentos oficiais não deverão impedir métodos alternativos autorizados que alcancem o resultado esperado.
26. Boas práticas globais futuras formarão uma biblioteca optativa, não uma imposição automática.
27. Toda resposta relevante deverá preservar a diferença entre fato, memória, inferência, hipótese, ensinamento e regra oficial.
28. Conhecimento sensível continuará subordinado a permissões e escopos de acesso.
29. Mudanças de estado de conhecimento relevante deverão ser rastreáveis e auditáveis.

---

## 4. Escopo

### 4.1 Incluído

Esta RFC especifica:

- base de conhecimento própria;
- independência em relação ao modelo de linguagem;
- camadas de conhecimento;
- categorias de memória;
- contexto cognitivo;
- recuperação controlada;
- seleção de fontes;
- relações operacionais próximas;
- critérios de aprofundamento e parada;
- consentimento para investigação ampla;
- memória curta;
- memória longa;
- conhecimento universal do produto;
- conhecimento institucional da empresa;
- conhecimento operacional;
- observações e padrões;
- aprendizado com acertos, erros e improvisações;
- aprendizado sobre o próprio produto;
- ensinamentos fornecidos por usuários;
- avaliação preliminar;
- fila de validação;
- promoção, rejeição, revisão e substituição de conhecimento;
- procedimentos emergentes;
- procedimentos oficiais;
- biblioteca futura de boas práticas;
- permissões, privacidade e auditoria aplicadas ao conhecimento;
- requisitos de qualidade e critérios de conformidade.

### 4.2 Fora do escopo

Não são definidos aqui:

- modelo de linguagem definitivo;
- quantidade de parâmetros;
- mecanismo concreto de embeddings;
- banco vetorial definitivo;
- algoritmo de ranking final;
- tecnologia física da busca;
- estrutura SQL definitiva;
- política legal completa de retenção;
- anonimização global entre empresas;
- marketplace de conhecimento;
- compartilhamento automático entre instalações;
- interface visual final de curadoria;
- workflow completo de aprovação estratégica da IA;
- política final de propriedade intelectual;
- telemetria externa do produto;
- mecanismo completo de atualização em nuvem;
- definição detalhada dos briefings, lembretes e escalonamentos;
- avaliação formal de desempenho de funcionários.

A ausência dessas definições não autoriza implementações incompatíveis com esta RFC.

---

## 5. Conceitos fundamentais

### 5.1 Conhecimento

Conhecimento é uma informação estruturada, interpretável e reutilizável pelo Mheibos para explicar, orientar, validar, recomendar ou contextualizar uma operação.

Um conteúdo somente deverá ser tratado como conhecimento oficial quando possuir autoridade, origem e validade suficientes para o uso pretendido.

### 5.2 Informação

Informação é um dado ou conteúdo disponível, mas que não possui necessariamente validação, estabilidade ou generalidade suficiente para ser utilizado como conhecimento oficial.

### 5.3 Memória

Memória é a capacidade de preservar contexto, acontecimentos, relações, preferências autorizadas e aprendizados para uso posterior.

A memória não deverá ser tratada como uma única coleção indiferenciada.

### 5.4 Contexto

Contexto é o conjunto selecionado de informações necessárias para compreender uma interação, decisão, objeto, missão, processo ou situação atual.

Contexto é construído para um objetivo específico e poderá ser temporário.

### 5.5 Fonte

Fonte é a origem identificável de uma informação ou conhecimento.

Exemplos:

- RFC oficial;
- política da empresa;
- procedimento aprovado;
- evento de domínio;
- registro de cliente;
- histórico de pedido;
- nota validada;
- usuário autor do ensinamento;
- integração externa identificada;
- análise produzida pela IA.

### 5.6 Autoridade

Autoridade indica o grau em que uma fonte pode definir ou sustentar uma conclusão.

Uma política aprovada possui autoridade diferente de uma sugestão, uma conversa, uma hipótese ou uma observação de uso.

### 5.7 Conhecimento oficial

Conhecimento oficial é conteúdo validado e autorizado para orientar outros usuários, respostas, procedimentos ou decisões dentro de seu escopo.

### 5.8 Conhecimento emergente

Conhecimento emergente é uma prática, solução, padrão ou interpretação útil ainda não promovida a procedimento ou conhecimento oficial.

### 5.9 Ensinamento

Ensinamento é um conteúdo explicitamente fornecido por um usuário com intenção de ensinar algo ao Mheibos.

O ensinamento poderá estar correto, incompleto, local, contraditório, desatualizado ou arriscado. Por isso, não será oficial por natureza.

### 5.10 Observação

Observação é um fato ou padrão registrado pelo sistema sem que sua causa ou generalidade esteja confirmada.

### 5.11 Hipótese

Hipótese é uma explicação possível ainda não comprovada.

### 5.12 Procedimento

Procedimento é uma orientação sobre como executar determinado trabalho.

Ele poderá ser:

- emergente;
- recomendado;
- oficial;
- substituído;
- desativado.

### 5.13 Recuperação de contexto

Recuperação de contexto é o processo de localizar, selecionar, ordenar e fornecer ao componente cognitivo as informações relevantes para uma questão específica.

### 5.14 Promoção

Promoção é a mudança controlada de um conteúdo para um nível superior de autoridade ou reutilização.

Exemplo:

```text
Ensinamento pendente
        ↓ validação
Conhecimento aprovado
        ↓ governança
Procedimento oficial
```

---

## 6. Base própria de conhecimento

### 6.1 Regra fundamental

O conhecimento do Mheibos deverá existir fora do modelo de linguagem.

O modelo poderá interpretar, resumir e relacionar conteúdos, mas não será o repositório oficial da inteligência da empresa.

### 6.2 Motivos

Essa separação permite:

- trocar o modelo sem perda de conhecimento;
- corrigir conteúdos sem retreinar o modelo;
- aplicar permissões e escopos;
- identificar fontes;
- preservar versões;
- auditar alterações;
- distinguir conteúdo oficial de inferência;
- manter conhecimento local à empresa;
- combinar regras determinísticas e cognição;
- reduzir dependência de fornecedor.

### 6.3 Conteúdos preservados fora do modelo

Deverão permanecer em componentes próprios, conforme aplicável:

- RFCs;
- princípios e políticas;
- documentação do produto;
- procedimentos;
- cadastros e estados operacionais;
- eventos e evidências;
- decisões;
- histórico de clientes;
- aprendizados aprovados;
- memória de missões;
- padrões identificados;
- notas validadas;
- preferências autorizadas;
- vocabulário da empresa;
- regras e exceções.

### 6.4 Modelo como dependência substituível

O modelo de linguagem deverá ser acessado pelo Gateway de IA definido na RFC-0003.

Nenhum conteúdo oficial poderá existir somente em pesos do modelo, no histórico interno de uma sessão de inferência ou em um prompt não versionado.

### 6.5 Reconstituição

A plataforma deverá ser capaz de reconstruir contexto cognitivo a partir de suas fontes próprias após:

- reinicialização;
- troca do modelo;
- atualização do modelo;
- encerramento de sessão;
- falha do serviço cognitivo;
- migração futura de infraestrutura.

---

## 7. Camadas de conhecimento

### 7.1 Princípio de separação

Conhecimentos com autoridades, escopos e ciclos de vida diferentes não deverão ser misturados em uma única coleção sem distinção.

### 7.2 Conhecimento universal do Mheibos

Representa aquilo que pertence ao produto e aos princípios gerais da plataforma.

Exemplos:

- Manifesto;
- Princípios Fundamentais;
- comportamento esperado da IA;
- arquitetura oficial;
- semântica das entidades;
- funcionamento dos módulos;
- documentação de uso;
- limites permanentes do sistema.

Esse conhecimento deverá ser versionado como parte do produto.

### 7.3 Conhecimento institucional da empresa

Representa aquilo que é próprio da organização atendida.

Exemplos:

- setores;
- políticas internas;
- procedimentos aprovados;
- horários;
- fornecedores;
- categorias de serviço;
- critérios internos;
- vocabulário;
- regras comerciais;
- orientações de atendimento;
- exceções autorizadas.

### 7.4 Conhecimento operacional

Representa a realidade dinâmica do trabalho.

Exemplos:

- pedidos;
- processos;
- estados;
- etapas;
- prazos;
- bloqueios;
- pendências;
- responsabilidades;
- missões;
- carga;
- eventos recentes;
- evidências;
- decisões em andamento.

Conhecimento operacional poderá mudar rapidamente e deverá consultar fontes oficiais atualizadas.

### 7.5 Memória de relacionamento

Representa histórico contextual de clientes, interações, preferências autorizadas, compromissos, ocorrências e continuidade de atendimento.

Ela não substitui cadastros e eventos oficiais.

### 7.6 Memória individual autorizada

Representa preferências, continuidade, objetivos, padrões de interface e contexto útil de um usuário específico.

Seu uso deverá respeitar privacidade, permissões e finalidade.

### 7.7 Memória da missão

Representa objetivo, plano, tarefas, notas, decisões, conversa e progresso necessários à continuidade de uma Missão.

### 7.8 Contexto da conversa

Representa as mensagens, objetos e objetivos relevantes à interação atual.

Ele deverá ser temporário, limitado e separado da memória oficial.

### 7.9 Consulta combinável

A separação em camadas não deverá impedir uma resposta que precise relacionar, por exemplo:

- regra universal do produto;
- política da empresa;
- estado atual de um pedido;
- histórico do cliente;
- responsabilidade do usuário;
- contexto da conversa.

A combinação deverá ser controlada e justificável.

---

## 8. Autoridade e precedência

### 8.1 Necessidade de hierarquia

Quando fontes divergirem, o sistema deverá identificar qual possui autoridade para a questão atual.

### 8.2 Ordem conceitual

Sem substituir regras específicas de domínio, a precedência deverá considerar:

1. princípios permanentes e políticas normativas aplicáveis;
2. regras determinísticas oficiais;
3. estado operacional validado;
4. procedimentos oficiais vigentes;
5. decisões formalmente registradas;
6. conhecimento institucional aprovado;
7. conhecimento emergente validado para recomendação;
8. observações e padrões;
9. ensinamentos pendentes;
10. hipóteses e inferências da IA.

### 8.3 Escopo antes da autoridade abstrata

Uma fonte superior fora do escopo não deverá substituir uma fonte específica válida.

Exemplo:

> Um procedimento geral não elimina uma exceção formal aprovada para determinado tipo de pedido.

### 8.4 Conflitos

Quando houver conflito material, o Mheibos deverá:

- identificar as fontes;
- informar a divergência;
- evitar escolher silenciosamente;
- aplicar a regra oficial quando houver;
- solicitar decisão humana quando necessário;
- registrar a resolução relevante.

### 8.5 Conteúdo desatualizado

Conhecimento com vigência encerrada não deverá ser apresentado como regra atual.

Ele poderá permanecer consultável como histórico.

---

## 9. Estrutura conceitual de um item de conhecimento

Um item persistente de conhecimento deverá permitir representar, conforme aplicável:

### 9.1 Identidade

- identificador técnico;
- tipo;
- camada;
- organização;
- versão.

### 9.2 Conteúdo

- título;
- descrição;
- conteúdo estruturado ou referência;
- palavras e entidades relacionadas;
- idioma;
- formato.

### 9.3 Origem

- autor humano;
- componente produtor;
- documento de origem;
- eventos relacionados;
- data de criação;
- contexto em que surgiu.

### 9.4 Autoridade

- oficial;
- aprovado;
- recomendado;
- emergente;
- pendente;
- rejeitado;
- histórico;
- invalidado.

### 9.5 Escopo

- global do produto;
- organização;
- setor;
- função;
- processo;
- categoria de pedido;
- cliente;
- missão;
- usuário;
- situação específica.

### 9.6 Validade

- vigência inicial;
- vigência final;
- condição de aplicação;
- versão substituta;
- motivo de desativação.

### 9.7 Segurança

- classificação de sensibilidade;
- permissões necessárias;
- restrições de divulgação;
- origem privada ou compartilhada.

### 9.8 Validação

- estado;
- avaliador;
- data;
- justificativa;
- conflitos identificados;
- riscos;
- evidências;
- decisão final.

### 9.9 Uso

- consultas relevantes;
- recomendações apoiadas;
- feedback recebido;
- resultados observados;
- necessidade de revisão.

A estrutura física poderá variar, mas essas dimensões não deverão ser perdidas quando forem necessárias à governança.

---

## 10. Recuperação controlada de contexto

### 10.1 Autoridade do Mheibos

O Mheibos controlará quais informações serão fornecidas ao modelo.

O modelo não receberá acesso irrestrito ao banco, aos arquivos, às memórias ou às integrações.

### 10.2 Fluxo geral

```text
Pergunta, evento ou objetivo
           ↓
Identificação do usuário e do escopo
           ↓
Definição da necessidade de contexto
           ↓
Seleção de fontes autorizadas
           ↓
Recuperação de relações próximas
           ↓
Avaliação de suficiência
           ↓
Montagem do pacote de contexto
           ↓
Gateway de IA
           ↓
Resposta estruturada
           ↓
Validação e explicação pelo Mheibos
```

### 10.3 Seleção por finalidade

A recuperação deverá começar pela pergunta operacional concreta.

O sistema não deverá coletar contexto apenas porque ele existe.

### 10.4 Menor contexto suficiente

O objetivo será fornecer o menor conjunto de informações que permita uma resposta confiável.

Isso reduz:

- exposição indevida;
- latência;
- custo computacional;
- confusão;
- contradições;
- alucinação;
- sobrecarga do modelo.

### 10.5 Resultados estruturados

O componente de recuperação deverá identificar, quando possível:

- fonte;
- entidade;
- relação;
- autoridade;
- momento;
- validade;
- permissão;
- motivo de inclusão.

### 10.6 Separação entre busca e resposta

Encontrar conteúdo não significa que ele seja verdadeiro, vigente ou autorizado.

A resposta deverá considerar autoridade e contexto antes de utilizar o resultado.

---

## 11. Relações operacionais próximas

### 11.1 Ponto de partida

A primeira busca deverá partir do objeto, usuário, processo, missão ou situação atual.

### 11.2 Relações prioritárias

O sistema deverá priorizar relações determinísticas como:

- Pedido → Cliente;
- Pedido → Itens;
- Pedido → Processos;
- Processo → Etapas;
- Etapa → Responsável;
- Etapa → Dependências;
- Processo → Bloqueios;
- Pedido → Pagamentos;
- Pedido → Arquivos;
- Missão → Tarefas;
- Missão → Participantes;
- Pendência → Responsável;
- Evento → Entidade afetada;
- Evidência → Evento ou estado;
- Usuário → Perfil e permissões;
- Cliente → histórico autorizado.

### 11.3 Vantagem

Essas relações já possuem significado operacional definido e reduzem a necessidade de inferência livre.

### 11.4 Expansão gradual

A busca poderá avançar para relações mais distantes somente quando:

- o contexto próximo for insuficiente;
- houver contradição;
- o impacto justificar;
- a causa provável estiver fora do objeto atual;
- o usuário solicitar maior profundidade;
- uma política exigir verificação adicional.

---

## 12. Ausência de grafo geral como pilar inicial

### 12.1 Decisão

A primeira versão não dependerá de um grafo geral de conhecimento aberto à exploração livre pela IA.

### 12.2 O que esta decisão não significa

Ela não proíbe:

- relações explícitas entre entidades;
- índices de busca;
- referências cruzadas;
- mapas limitados de dependência;
- estruturas de grafo em componentes específicos;
- futura adoção de tecnologias de grafo.

### 12.3 O que esta decisão impede

Ela impede que o funcionamento básico dependa de:

- modelar toda a empresa como uma rede sem fronteiras;
- permitir navegação indefinida pelo modelo;
- inferir relações não validadas como se fossem fatos;
- adicionar complexidade antes de haver necessidade comprovada;
- criar uma segunda fonte de verdade paralela ao domínio.

### 12.4 Fundamento da primeira versão

A base inicial será formada por:

- entidades oficiais;
- relações determinísticas;
- eventos;
- evidências;
- documentos e procedimentos versionados;
- índices de recuperação;
- metadados de autoridade e escopo.

### 12.5 Evolução futura

Uma estrutura de grafo poderá ser adotada futuramente para problemas específicos, desde que:

- não substitua a fonte oficial;
- possua relações rastreáveis;
- respeite permissões;
- demonstre benefício real;
- tenha limites de exploração;
- não torne a arquitetura dependente de inferências opacas.

---

## 13. Critérios de profundidade e parada

### 13.1 Profundidade limitada

Toda recuperação deverá possuir limite explícito ou implícito de profundidade.

### 13.2 Critérios de suficiência

O contexto poderá ser considerado suficiente quando:

- a pergunta estiver respondida por fontes oficiais;
- as relações principais estiverem cobertas;
- não houver conflito material;
- o nível de confiança for adequado ao impacto;
- novas fontes não alterarem materialmente a conclusão.

### 13.3 Critérios de parada

A busca deverá terminar quando:

- houver resposta suficiente;
- a permissão limitar novas fontes;
- a profundidade autorizada for atingida;
- o custo superar o benefício;
- apenas uma pessoa puder fornecer o dado ausente;
- as fontes adicionais forem repetitivas;
- a conclusão depender de decisão humana, e não de mais busca.

### 13.4 Evitar investigação infinita

O sistema não deverá continuar procurando apenas para aparentar maior inteligência.

### 13.5 Informação de insuficiência

Quando não houver base suficiente, o Mheibos deverá declarar:

- o que encontrou;
- o que falta;
- por que isso limita a conclusão;
- qual próxima fonte ou ação poderia resolver a incerteza.

---

## 14. Investigações amplas e consentimento

### 14.1 Regra

Uma investigação ampla não deverá começar automaticamente quando a resposta inicial puder ser útil sem ela.

### 14.2 Quando pedir consentimento

O Mheibos deverá solicitar autorização quando a investigação puder:

- demorar perceptivelmente;
- consumir recursos relevantes;
- consultar grande volume de histórico;
- cruzar múltiplos setores;
- acessar fontes adicionais sensíveis;
- ampliar significativamente o escopo original;
- produzir análise estratégica extensa.

### 14.3 Conteúdo da solicitação

Antes de aprofundar, o sistema deverá apresentar:

- resposta ou achado inicial;
- limitação atual;
- fontes adicionais pretendidas;
- benefício esperado;
- escopo da investigação;
- eventual impacto de tempo ou recursos.

### 14.4 Consentimento não amplia permissão

Autorizar uma investigação não concede acesso a informações que o usuário não poderia consultar.

### 14.5 Investigações obrigatórias

Uma regra de segurança ou validação poderá exigir consulta adicional sem consentimento opcional quando a operação não puder ser concluída com segurança sem essa verificação.

Nesse caso, o sistema deverá explicar que a consulta é necessária à ação solicitada.

---

## 15. Montagem do pacote de contexto

### 15.1 Finalidade

O pacote de contexto é a representação controlada das informações fornecidas ao modelo para uma tarefa específica.

### 15.2 Conteúdo possível

Ele poderá incluir:

- identidade e permissões relevantes;
- objetivo atual;
- entidades principais;
- fatos oficiais;
- estados;
- eventos recentes;
- evidências;
- procedimentos aplicáveis;
- histórico necessário;
- conhecimento institucional;
- contexto da conversa;
- instruções de saída estruturada.

### 15.3 Conteúdo excluído

O pacote não deverá incluir:

- informações sem relação com a finalidade;
- dados fora da permissão;
- segredos desnecessários;
- memória privada de terceiros;
- histórico integral quando um resumo verificável for suficiente;
- conteúdo rejeitado como se fosse oficial;
- hipóteses sem identificação de incerteza.

### 15.4 Referências

Sempre que possível, o contexto deverá preservar referências que permitam ao Mheibos verificar a resposta.

### 15.5 Atualidade

Dados operacionais deverão ser obtidos das fontes atuais antes de respostas que dependam do estado presente.

### 15.6 Versionamento

Procedimentos, políticas e conhecimento universal deverão indicar versão ou vigência quando isso afetar a resposta.

---

## 16. Memória de curto prazo

### 16.1 Papel

A memória de curto prazo sustenta a continuidade imediata do trabalho.

### 16.2 Conteúdo

Ela poderá preservar:

- contexto da sessão;
- conversa atual;
- objetos abertos;
- tela e módulo atuais;
- filtros temporários;
- missão ativa;
- rascunhos;
- decisões ainda não concluídas;
- ações recentes;
- preferências temporárias;
- objetivo do período;
- intervenção em andamento.

### 16.3 Características

A memória curta deverá ser:

- limitada;
- orientada ao objetivo;
- atualizável;
- descartável quando deixar de ser útil;
- separada de conhecimento oficial;
- protegida por sessão e usuário;
- capaz de sobreviver a interrupções quando a continuidade exigir.

### 16.4 Encerramento de sessão

Encerrar a sessão não deverá promover automaticamente todo o contexto temporário à memória longa.

O sistema deverá selecionar o que merece persistência.

### 16.5 Missões

Contexto necessário à retomada de Missão poderá ser persistido além da sessão, mas continuará pertencendo à memória da Missão, e não a uma memória geral irrestrita.

### 16.6 Conversa

A conversa atual poderá ser resumida para continuidade, desde que o resumo preserve decisões, dúvidas e objetos relevantes sem substituir o histórico oficial.

---

## 17. Memória de longo prazo

### 17.1 Papel

A memória de longo prazo preserva aquilo que deverá continuar útil após sessões, dias ou mudanças de contexto.

### 17.2 Conteúdo possível

Ela poderá incluir:

- conhecimento aprovado;
- histórico de relacionamento com clientes;
- padrões operacionais validados;
- procedimentos;
- decisões relevantes;
- aprendizados de missões;
- preferências autorizadas e duráveis;
- evolução de processos;
- problemas recorrentes;
- soluções emergentes;
- histórico institucional;
- comportamento agregado do produto;
- resultados de melhorias.

### 17.3 Critérios de persistência

Um conteúdo deverá ser promovido à memória longa quando possuir utilidade futura clara, origem identificável e escopo apropriado.

### 17.4 Não acumulação indiscriminada

A memória longa não deverá armazenar tudo para sempre sem distinção.

Deverá existir tratamento para:

- validade;
- revisão;
- consolidação;
- substituição;
- arquivamento;
- expiração;
- restrição de uso.

### 17.5 Memória longa não é verdade automática

Conteúdo persistente poderá permanecer como observação, hipótese, histórico ou recomendação.

Persistência não equivale a autoridade oficial.

---

## 18. Transição entre memória curta e longa

### 18.1 Promoção seletiva

Ao final de uma sessão, missão, processo ou período relevante, o Mheibos poderá identificar conteúdos candidatos à memória longa.

### 18.2 Exemplos de candidatos

- decisão importante;
- preferência recorrente autorizada;
- solução útil;
- erro repetido;
- informação consolidada de cliente;
- aprendizado de uma missão;
- alteração de procedimento;
- contexto necessário à continuidade.

### 18.3 Conteúdos que não devem ser promovidos automaticamente

- conversa casual;
- emoção momentânea;
- hipótese não confirmada;
- dado sensível sem finalidade;
- rascunho descartado;
- informação de terceiros fora do escopo;
- sugestão rejeitada;
- inferência transitória.

### 18.4 Consolidação

Múltiplas ocorrências semelhantes poderão ser consolidadas em um padrão, mantendo referência aos fatos que o sustentam.

### 18.5 Correção

A memória longa deverá permitir correção por novo registro ou revisão explícita, sem apagar silenciosamente a origem anterior.

---

## 19. Aprendizado privado e local

### 19.1 Regra da primeira versão

Todo aprendizado produzido na instalação inicial permanecerá local à empresa.

### 19.2 Ausência de compartilhamento automático

O sistema não enviará automaticamente para outras empresas:

- conversas;
- procedimentos;
- dados operacionais;
- padrões de clientes;
- erros;
- métricas;
- ensinamentos;
- memórias individuais;
- documentos internos.

### 19.3 Benefícios

A decisão reduz:

- risco de exposição;
- complexidade jurídica;
- dependência de nuvem;
- necessidade de anonimização precoce;
- confusão entre práticas de empresas diferentes.

### 19.4 Aprendizado do produto

Mesmo observações sobre o próprio Mheibos permanecerão locais na primeira versão, salvo exportação ou compartilhamento explicitamente autorizado em mecanismo futuro.

### 19.5 Evolução global

Uma camada global e anônima poderá existir futuramente, mas exigirá RFC ou revisão específica sobre:

- consentimento;
- anonimização;
- segurança;
- propriedade;
- curadoria;
- qualidade;
- revogação;
- isolamento entre empresas;
- auditoria;
- aplicação optativa.

---

## 20. Aprendizado com acertos

### 20.1 Identificação

O sistema poderá identificar práticas associadas a resultados positivos.

### 20.2 Cuidado com causalidade

Um resultado positivo não prova automaticamente que uma prática foi sua causa.

O Mheibos deverá distinguir:

- ocorrência;
- correlação;
- hipótese de contribuição;
- prática validada.

### 20.3 Uso inicial

Uma prática bem-sucedida poderá alimentar:

- recomendação;
- exemplo;
- sugestão de procedimento;
- comparação antes e depois;
- candidato a melhoria.

### 20.4 Repetição e evidência

Quanto maior o impacto ou a generalização pretendida, maior deverá ser a exigência de repetição, evidência e validação.

### 20.5 Não imposição

Uma prática útil não deverá tornar-se obrigatória apenas porque funcionou uma vez.

---

## 21. Aprendizado com erros

### 21.1 Finalidade

Erros deverão servir à prevenção, assistência e melhoria, e não à humilhação.

### 21.2 Conteúdo aprendido

O Mheibos poderá aprender:

- condição em que o erro ocorre;
- etapa afetada;
- consequência;
- sinais prévios;
- forma de recuperação;
- orientação preventiva;
- necessidade de treinamento;
- possível fricção da interface.

### 21.3 Processo antes da pessoa

O conhecimento deverá descrever o padrão operacional antes de atribuir julgamento pessoal.

### 21.4 Erro individual e padrão sistêmico

Uma ocorrência isolada não deverá ser generalizada como característica permanente de um usuário.

### 21.5 Resultado

O aprendizado poderá gerar:

- alerta contextual;
- ajuda progressiva;
- revisão de procedimento;
- melhoria de interface;
- proposta de treinamento;
- hipótese de causa raiz.

A aplicação dessas consequências dependerá dos RFCs proprietários.

---

## 22. Aprendizado com improvisações

### 22.1 Conceito

Improvisação é uma forma não prevista de alcançar o resultado esperado.

### 22.2 Avaliação

Uma improvisação poderá ser classificada como:

- inadequada;
- arriscada;
- neutra;
- útil apenas no contexto;
- solução emergente;
- candidata a boa prática.

### 22.3 Preservação da autonomia

O Mheibos não deverá rejeitar automaticamente um método diferente do procedimento recomendado quando:

- o usuário possuir autorização;
- o resultado for válido;
- não houver violação de segurança;
- não houver conflito com regra obrigatória.

### 22.4 Promoção

Uma improvisação útil poderá tornar-se recomendação, mas somente mediante avaliação e governança compatíveis com seu impacto.

### 22.5 Registro de contexto

A utilidade deverá ser relacionada às condições em que ocorreu para evitar generalização indevida.

---

## 23. Aprendizado sobre o próprio produto

### 23.1 Capacidade

O Mheibos poderá observar como sua interface e seus fluxos são utilizados para identificar oportunidades de melhoria do próprio sistema.

### 23.2 Sinais observáveis

Poderão ser analisados, de forma autorizada e proporcional:

- campos frequentemente corrigidos;
- telas abandonadas;
- sequências repetitivas;
- etapas confusas;
- funções pouco encontradas;
- atalhos frequentes;
- excesso de cliques;
- erros de navegação;
- intervenções dispensadas;
- filtros recorrentes;
- módulos pouco utilizados;
- pontos de demora;
- solicitações repetidas de ajuda.

### 23.3 Saídas possíveis

O aprendizado poderá produzir:

- adaptação temporária individual;
- sugestão de atalho;
- melhoria de tutorial;
- recomendação de layout;
- revisão de campo;
- proposta de automação;
- issue de produto;
- análise de fricção.

### 23.4 Limites

A observação não poderá:

- diagnosticar condição psicológica;
- criar rótulo pessoal;
- vigiar conteúdo fora da finalidade;
- medir produtividade por movimentos superficiais;
- expor usuários publicamente;
- alterar permissões;
- impor mudança persistente sem aprovação.

### 23.5 Produto e empresa

Uma melhoria observada localmente poderá ser útil ao produto geral, mas não sairá da instalação sem mecanismo futuro autorizado.

---

## 24. Ensinamentos fornecidos por usuários

### 24.1 Entrada explícita

O usuário poderá ensinar ao Mheibos informações, procedimentos, exceções, orientações e conhecimentos dentro de seu contexto.

### 24.2 Registro inicial

Todo ensinamento deverá registrar:

- autor;
- momento;
- conteúdo;
- contexto;
- escopo pretendido;
- entidades relacionadas;
- motivo;
- fonte ou evidência, quando disponível;
- estado de validação.

### 24.3 Estado inicial

O ensinamento deverá começar como conteúdo pendente, não oficial.

### 24.4 Uso pelo próprio autor

A implementação poderá permitir que um ensinamento pendente seja lembrado ao próprio autor dentro de escopo privado, desde que seja claramente identificado como não aprovado e não produza autoridade oficial.

### 24.5 Uso por terceiros

O conteúdo não deverá orientar outros usuários como conhecimento oficial antes da validação apropriada.

### 24.6 Permissão para ensinar

Registrar uma observação pessoal poderá ser amplamente permitido. Propor conhecimento institucional ou procedimento oficial deverá respeitar permissões específicas.

---

## 25. Avaliação preliminar pela IA

### 25.1 Finalidade

Antes da validação humana, a IA poderá realizar uma análise preliminar para organizar a decisão.

### 25.2 Critérios

A avaliação poderá examinar:

- clareza;
- completude;
- coerência interna;
- conflito com conhecimento oficial;
- conflito com princípios;
- risco operacional;
- risco financeiro;
- risco de segurança;
- escopo;
- generalização indevida;
- evidências fornecidas;
- duplicação;
- conteúdo semelhante existente;
- necessidade de especialista.

### 25.3 Resultado

A IA poderá classificar o ensinamento como:

- aparentemente coerente;
- incompleto;
- duplicado;
- conflitante;
- potencialmente arriscado;
- específico demais;
- candidato a recomendação;
- candidato a procedimento;
- necessita informação adicional.

### 25.4 Limite

A avaliação da IA não equivale a aprovação.

### 25.5 Explicação

A avaliação deverá apresentar motivos e fontes de conflito quando houver.

---

## 26. Validação humana

### 26.1 Obrigatoriedade

Conhecimento que será utilizado oficialmente por outros usuários deverá ser validado por pessoa autorizada.

### 26.2 Validador

O validador poderá ser:

- gerente;
- administrador;
- responsável pelo domínio;
- curador designado;
- autoridade definida pela empresa.

### 26.3 Decisões possíveis

O validador poderá:

- aprovar;
- aprovar com edição;
- limitar o escopo;
- solicitar evidências;
- devolver ao autor;
- manter como recomendação emergente;
- rejeitar;
- arquivar;
- encaminhar a autoridade superior.

### 26.4 Conteúdo da decisão

A validação deverá registrar:

- decisão;
- autor;
- data;
- justificativa;
- escopo;
- vigência;
- alterações realizadas;
- conflitos resolvidos;
- estado resultante.

### 26.5 Ausência de aprovação silenciosa

Tempo decorrido, uso repetido ou falta de revisão não deverão promover automaticamente o ensinamento.

---

## 27. Estados do conhecimento

Um item de conhecimento deverá suportar estados equivalentes a:

- rascunho;
- pendente de avaliação;
- aguardando informação;
- em validação;
- aprovado;
- recomendado;
- emergente;
- oficial;
- restrito;
- rejeitado;
- substituído;
- desativado;
- arquivado;
- invalidado.

### 27.1 Rascunho

Conteúdo ainda não submetido.

### 27.2 Pendente de avaliação

Conteúdo enviado e aguardando análise preliminar.

### 27.3 Em validação

Conteúdo sob decisão de autoridade humana.

### 27.4 Aprovado

Conteúdo validado para o escopo definido.

### 27.5 Recomendado

Conteúdo que pode orientar, mas não obriga.

### 27.6 Oficial

Conteúdo que possui autoridade institucional dentro de seu escopo.

### 27.7 Emergente

Prática útil ainda em observação ou teste.

### 27.8 Rejeitado

Conteúdo não aprovado para uso pretendido, preservando o histórico da decisão.

### 27.9 Substituído

Conteúdo que possui versão posterior vigente.

### 27.10 Invalidado

Conteúdo que não deve mais ser utilizado por erro, risco ou perda de validade.

---

## 28. Procedimentos emergentes

### 28.1 Papel

Procedimentos emergentes preservam soluções úteis sem transformar observação inicial em regra obrigatória.

### 28.2 Apresentação

O Mheibos poderá apresentá-los como:

- alternativa conhecida;
- prática que funcionou em situação semelhante;
- recomendação experimental;
- solução adotada anteriormente;
- candidato a melhoria.

### 28.3 Transparência

A interface deverá informar que o procedimento:

- não é obrigatório;
- possui escopo conhecido;
- pode estar em avaliação;
- não substitui regra oficial;
- pode exigir confirmação.

### 28.4 Uso

Procedimentos emergentes poderão auxiliar respostas e dúvidas, desde que não sejam confundidos com obrigação institucional.

### 28.5 Promoção futura

A transformação em procedimento oficial dependerá da governança correspondente e deverá preservar versão, autor, evidências e decisão.

---

## 29. Procedimentos oficiais e flexibilidade

### 29.1 Orientação, não engessamento

Mesmo um procedimento oficial poderá orientar a forma preferida sem impedir toda alternativa.

### 29.2 Regra obrigatória e recomendação

O sistema deverá distinguir:

- regra obrigatória;
- etapa obrigatória;
- procedimento recomendado;
- boa prática;
- alternativa emergente.

### 29.3 Métodos alternativos

Um usuário autorizado poderá utilizar método diferente quando:

- alcançar o resultado exigido;
- preservar evidências necessárias;
- não violar segurança;
- não violar permissão;
- não contrariar regra obrigatória.

### 29.4 Melhoria de procedimento

Uso recorrente de alternativa bem-sucedida poderá originar proposta de revisão do procedimento oficial.

---

## 30. Biblioteca futura de boas práticas

### 30.1 Natureza

Uma futura camada global poderá oferecer boas práticas aprovadas como biblioteca optativa.

### 30.2 Não aplicação automática

Nenhuma prática global deverá ser aplicada automaticamente a uma empresa apenas porque foi útil em outra instalação.

### 30.3 Momento de escolha

A biblioteca poderá ser apresentada:

- durante implantação;
- em revisão de processo;
- em diagnóstico;
- quando problema semelhante for detectado;
- por solicitação de gestor.

### 30.4 Conteúdo mínimo

Uma prática global deverá informar:

- problema que busca resolver;
- contexto em que foi útil;
- requisitos;
- benefícios esperados;
- riscos;
- evidência disponível;
- possibilidade de adaptação;
- origem anonimizada ou institucional;
- versão.

### 30.5 Adaptação local

A empresa deverá poder:

- aceitar;
- rejeitar;
- adaptar;
- testar;
- limitar escopo;
- reverter.

### 30.6 Governança futura

O funcionamento dessa biblioteca exigirá documento específico antes da implementação global.

---

## 31. Privacidade e permissões

### 31.1 Regra geral

A identidade cognitiva única não autoriza acesso irrestrito ao conhecimento.

### 31.2 Aplicação de permissões

A recuperação deverá respeitar:

- identidade;
- perfil;
- exceções individuais;
- escopo;
- propriedade;
- responsabilidade;
- sensibilidade;
- finalidade.

### 31.3 Memórias privadas

Memória individual, notas pessoais e contexto privado não deverão ser revelados a terceiros sem autorização ou fundamento operacional explícito.

### 31.4 Conhecimento administrativo

Políticas de segurança, auditoria sensível e decisões administrativas poderão exigir permissões superiores.

### 31.5 Resumo sem exposição

Quando possível, o sistema deverá responder com conclusão agregada sem revelar conteúdo privado desnecessário.

### 31.6 IA subordinada

O modelo receberá apenas o conteúdo autorizado para a sessão atual.

---

## 32. Auditoria e rastreabilidade

### 32.1 Ações auditáveis

Deverão produzir eventos relevantes, conforme a RFC-0006:

- criação de conhecimento oficial;
- submissão de ensinamento;
- aprovação;
- rejeição;
- alteração de escopo;
- mudança de autoridade;
- substituição;
- invalidação;
- promoção de procedimento;
- alteração de política de recuperação;
- exportação sensível;
- compartilhamento futuro entre instalações.

### 32.2 Histórico

O histórico deverá permitir responder:

- quem ensinou;
- quem avaliou;
- quem aprovou;
- qual era a versão anterior;
- por que mudou;
- quais fontes sustentaram a decisão;
- onde o conhecimento foi utilizado;
- qual escopo possuía.

### 32.3 Correção

Correções deverão criar nova versão ou evento, preservando a versão anterior.

### 32.4 Uso da IA

Quando uma recomendação relevante depender de conhecimento recuperado, o sistema deverá ser capaz de indicar as fontes utilizadas.

---

## 33. Explicabilidade do conhecimento

### 33.1 Identificação da natureza

O Mheibos deverá distinguir em suas respostas:

- fato oficial;
- estado atual;
- procedimento vigente;
- histórico;
- memória;
- ensinamento pendente;
- padrão observado;
- hipótese;
- recomendação;
- previsão.

### 33.2 Fontes

Respostas relevantes deverão permitir acesso às fontes, quando autorizado.

### 33.3 Conflitos

Fontes conflitantes deverão ser apresentadas como conflito, não combinadas em uma falsa certeza.

### 33.4 Confiança

A confiança deverá considerar autoridade, atualidade, consistência, evidência e abrangência.

### 33.5 Ausência de fonte

Quando uma resposta depender apenas de inferência, isso deverá ser declarado.

---

## 34. Atualização, revisão e esquecimento controlado

### 34.1 Conhecimento evolui

Conhecimentos poderão tornar-se desatualizados, incorretos ou inadequados.

### 34.2 Revisão

A plataforma deverá permitir revisão por:

- data;
- mudança de política;
- conflito;
- resultado negativo;
- atualização do produto;
- solicitação humana;
- substituição de procedimento.

### 34.3 Esquecimento controlado

Esquecer não deverá significar apagar silenciosamente o passado quando houver relevância histórica.

O conteúdo poderá ser:

- desativado para uso atual;
- arquivado;
- anonimizado por política futura;
- substituído;
- invalidado;
- removido de índices ativos.

### 34.4 Preferências individuais

O usuário deverá poder revisar preferências e memórias individuais persistentes quando a interface futura oferecer essa capacidade.

### 34.5 Retenção

Políticas concretas de retenção serão definidas posteriormente, respeitando auditoria, privacidade e finalidade.

---

## 35. Falhas e degradação

### 35.1 Falha da recuperação semântica

A indisponibilidade de um índice semântico não deverá apagar o conhecimento oficial nem impedir consultas determinísticas essenciais.

### 35.2 Falha do modelo

A base de conhecimento continuará preservada se o modelo estiver indisponível.

### 35.3 Contexto insuficiente

O sistema deverá responder com limitação explícita, não inventar conhecimento.

### 35.4 Fonte indisponível

Quando uma referência externa ou arquivo não puder ser acessado, o Mheibos deverá indicar a indisponibilidade e preservar o vínculo histórico.

### 35.5 Recuperação parcial

O sistema poderá fornecer resposta parcial quando identificar claramente o que foi e o que não foi consultado.

### 35.6 Modo offline

Sem a Central, recursos de conhecimento e IA poderão ficar limitados conforme RFC-0008. O Cliente não deverá tratar cache local como base oficial atualizada.

---

## 36. Requisitos de qualidade

### 36.1 Independência cognitiva

O conhecimento não poderá depender de um modelo específico.

### 36.2 Relevância

A recuperação deverá priorizar conteúdo relacionado à finalidade atual.

### 36.3 Precisão

Fontes oficiais e estados atuais deverão prevalecer sobre memória vaga ou inferência.

### 36.4 Atualidade

Conteúdo com vigência deverá ser verificado antes do uso.

### 36.5 Segurança

Nenhum mecanismo de memória poderá contornar permissões.

### 36.6 Rastreabilidade

Conhecimento relevante deverá possuir origem e histórico.

### 36.7 Baixo custo

A arquitetura deverá funcionar com infraestrutura compatível com a primeira versão local.

### 36.8 Latência controlada

A recuperação não deverá tornar interações comuns desnecessariamente lentas.

### 36.9 Honestidade

O sistema deverá declarar incerteza e insuficiência.

### 36.10 Não acumulação

Memória longa deverá ser consolidável e revisável.

### 36.11 Dignidade

Aprendizado com pessoas deverá apoiar melhoria sem criar vigilância ou julgamento pessoal indevido.

---

## 37. Riscos arquiteturais

A implementação deverá evitar:

- armazenar conhecimento apenas no prompt ou no modelo;
- misturar conhecimento oficial com conversa casual;
- permitir acesso direto do modelo ao banco;
- enviar contexto excessivo por padrão;
- ignorar permissões durante busca semântica;
- tratar conteúdo persistente como automaticamente verdadeiro;
- promover ensinamento sem validação;
- transformar uma ocorrência em regra geral;
- confundir correlação com causalidade;
- criar grafo geral complexo antes da necessidade;
- permitir exploração infinita de relações;
- ocultar fontes conflitantes;
- utilizar memória privada de terceiros fora do escopo;
- manter conhecimento desatualizado como vigente;
- apagar versões anteriores silenciosamente;
- acumular dados sem finalidade;
- criar perfis psicológicos de usuários;
- usar erros para punição ou ranking;
- impor boa prática global a empresas diferentes;
- tornar o sistema dependente de nuvem para aprender;
- permitir que a IA aprove seu próprio ensinamento;
- confundir procedimento recomendado com regra obrigatória;
- tratar cache offline como memória global atualizada;
- usar investigação ampla sem consentimento quando o aprofundamento for opcional.

---

## 38. Relação com os demais RFCs

| RFC | Responsabilidade relacionada |
|---|---|
| RFC-0000 | Mheibos como memória operacional ativa |
| RFC-0001 | Limites humanos, segurança, qualidade e autonomia |
| RFC-0002 | Processos, estados, procedimentos e resultados esperados |
| RFC-0003 | Base própria, Gateway de IA e independência do modelo |
| RFC-0004 | Seleção cognitiva, investigação progressiva e explicabilidade |
| RFC-0005 | Entidades, identidades, notas, referências e persistência |
| RFC-0006 | Eventos, evidências, versões e auditoria |
| RFC-0007 | Permissões, escopos e proteção de conhecimento sensível |
| RFC-0008 | Limitações de memória e IA durante operação offline |
| RFC-0009 | Personalização, assistência e aprendizado sobre a interface |
| RFC-0010 | Memória, chat, notas e aprendizado das Missões |
| RFC-0012 | Continuidade diária, briefing, notas e gatilhos de lembrança |
| RFC-0014 | Documentos, arquivos e fontes externas de conhecimento |
| RFC-0015 | Padrões, análises, cenários e avaliação de resultados |
| RFC-0016 | Governança, validação, confiança e proteção humana da IA |

---

## 39. Consequências da decisão

### 39.1 Benefícios

- conhecimento sobrevive à troca do modelo;
- fontes oficiais permanecem identificáveis;
- permissões podem ser aplicadas à memória;
- contexto enviado à IA é menor e mais relevante;
- a plataforma pode operar com modelos menores;
- respostas tornam-se mais explicáveis;
- conhecimento institucional não se mistura com conversa transitória;
- acertos, erros e improvisações alimentam melhoria;
- procedimentos emergentes podem ser úteis sem engessar a empresa;
- ensinamentos humanos recebem governança;
- aprendizado permanece privado na primeira fase;
- a arquitetura pode evoluir para biblioteca global sem depender dela agora.

### 39.2 Custos

- exige armazenamento e indexação próprios;
- requer metadados de origem, autoridade e escopo;
- aumenta a complexidade de recuperação;
- exige workflow de validação;
- requer revisão e versionamento;
- precisa distinguir memória curta, longa e conhecimento oficial;
- exige cuidado com privacidade;
- depende de qualidade das relações e fontes do domínio;
- poderá demandar ferramentas futuras de curadoria.

### 39.3 Limitações

- a primeira versão não possuirá conhecimento global entre empresas;
- não haverá grafo geral como mecanismo cognitivo principal;
- investigação ampla poderá depender de consentimento;
- o aprendizado não será automaticamente correto;
- conhecimento informal dependerá de validação para uso oficial;
- o sistema poderá não identificar causalidade apenas com padrões;
- memória offline será limitada;
- a primeira implementação poderá utilizar mecanismos de busca simples antes de recursos semânticos avançados.

---

## 40. Critérios de conformidade

Uma implementação estará em conformidade com esta RFC somente se:

1. o conhecimento oficial existir fora do modelo de linguagem;
2. a troca do modelo não apagar memória ou procedimentos;
3. conhecimento universal, institucional, operacional e contexto atual forem distinguíveis;
4. memória curta e memória longa forem separadas;
5. a recuperação for controlada pelo Mheibos;
6. o modelo não possuir acesso irrestrito às fontes;
7. permissões forem aplicadas antes da montagem do contexto;
8. relações operacionais próximas forem priorizadas;
9. a busca possuir critérios de profundidade e parada;
10. investigações amplas opcionais dependerem de consentimento;
11. a primeira versão não depender de grafo geral de conhecimento;
12. fatos oficiais forem distinguidos de hipóteses e inferências;
13. conhecimento possuir origem e escopo identificáveis;
14. conteúdo desatualizado não for apresentado como vigente;
15. aprendizados permanecerem locais à empresa na primeira versão;
16. acertos não forem automaticamente tratados como causalidade comprovada;
17. erros alimentarem prevenção sem produzir julgamento pessoal;
18. improvisações úteis puderem ser registradas como emergentes;
19. observação do produto respeitar privacidade e dignidade;
20. ensinamentos de usuários começarem como pendentes;
21. a IA não puder aprovar sozinha conhecimento oficial;
22. conhecimento destinado a terceiros depender de validação humana autorizada;
23. estados de aprovação, rejeição, substituição e invalidação forem preservados;
24. procedimentos emergentes forem apresentados como não obrigatórios;
25. regras obrigatórias forem distinguíveis de recomendações;
26. versões anteriores relevantes não forem apagadas silenciosamente;
27. mudanças relevantes gerarem eventos e auditoria;
28. respostas relevantes puderem indicar fontes autorizadas;
29. memória privada não for revelada fora do escopo;
30. falha do modelo não destruir a base de conhecimento;
31. biblioteca global futura, se criada, permanecer optativa.

---

## 41. Decisões adiadas

As seguintes decisões serão tomadas na implementação ou em documentos posteriores:

- banco de dados definitivo da base de conhecimento;
- uso e tecnologia de banco vetorial;
- modelo de embeddings;
- estratégia de chunking;
- algoritmo de ranking;
- formato físico do pacote de contexto;
- limites numéricos de profundidade;
- tamanho máximo de memória curta;
- política de expiração de memória;
- interface de curadoria;
- catálogo inicial de tipos de conhecimento;
- workflow visual de aprovação;
- responsáveis padrão por cada domínio;
- política de revisão periódica;
- mecanismos de feedback sobre respostas;
- medição de utilidade de conhecimento;
- anonimização entre empresas;
- biblioteca global;
- exportação e importação de conhecimento;
- integração com documentação externa;
- suporte a múltiplos idiomas;
- mecanismos futuros de grafo especializado;
- retenção legal;
- direito de correção e exclusão de memória pessoal;
- sincronização ampliada de conhecimento offline.

Essas decisões deverão respeitar as invariantes desta RFC.

---

## 42. Declaração normativa

O Mheibos possuirá uma base própria de conhecimento, memória e aprendizado, externa ao modelo de linguagem e preservada como parte permanente da plataforma.

O conhecimento será separado em camadas com autoridades, escopos, finalidades e ciclos de vida distintos, incluindo conhecimento universal do produto, conhecimento institucional da empresa, conhecimento operacional, memória de longo prazo, memória de curto prazo e contexto atual. Essas camadas poderão ser combinadas quando a situação exigir, mas nunca serão misturadas sem identificação de origem, permissão e validade.

O próprio Mheibos controlará a recuperação de contexto. O modelo de linguagem não poderá explorar livremente bancos, arquivos, memórias ou relações. A recuperação partirá de relações operacionais determinísticas, utilizará o menor contexto suficiente, aplicará critérios de profundidade e parada e solicitará consentimento antes de investigações amplas opcionais.

A primeira versão não dependerá de um grafo geral de conhecimento. Entidades, relações oficiais, eventos, evidências, documentos versionados e índices controlados formarão a base inicial da inteligência recuperável.

A memória curta preservará continuidade imediata de sessões, conversas, interfaces, missões e trabalho diário. A memória longa consolidará conhecimento estável, histórico relevante, relacionamento, padrões, aprendizados e evolução organizacional. Nenhum conteúdo temporário será promovido automaticamente apenas por ter sido observado ou persistido.

O aprendizado inicial permanecerá privado à empresa. O Mheibos poderá aprender com acertos, erros, improvisações e padrões de uso do próprio produto, sempre distinguindo fatos, correlações, hipóteses e recomendações e preservando dignidade, privacidade e autonomia humana.

Ensinamentos fornecidos por usuários começarão como conteúdo pendente. A IA poderá avaliar coerência, conflito, risco e evidência, mas não poderá aprovar sozinha conhecimento oficial. A promoção para uso institucional ou por outros usuários dependerá de validação humana autorizada, com escopo, vigência, autoria e histórico preservados.

Práticas úteis poderão permanecer como procedimentos emergentes e recomendações sem se tornarem obrigatórias. Uma futura biblioteca global de boas práticas será optativa e dependerá de governança própria, sem aplicação automática sobre empresas com realidades diferentes.
