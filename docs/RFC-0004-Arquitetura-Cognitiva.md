# MHEIBOS INTELLIGENT OPERATING SYSTEM

# RFC-0004 — Arquitetura Cognitiva

**Status:** Draft para aprovação  
**Versão:** 0.1  
**Data:** 30/07/2026  
**Dependências:** RFC-0000, RFC-0001, RFC-0002, RFC-0003  
**Fonte normativa:** Inventário Oficial de Decisões Arquiteturais — INV-107 a INV-118

---

## 1. Resumo

Esta RFC define a Arquitetura Cognitiva do Mheibos: o papel da Inteligência Artificial dentro da operação, a forma como ela interpreta o estado da empresa, produz recomendações, antecipa riscos, gera planos de ação, explica suas conclusões e preserva a autoridade humana.

O Mheibos possuirá uma única identidade cognitiva para toda a empresa. Essa identidade adaptará seu comportamento conforme o usuário, suas permissões, responsabilidades e contexto, sem se transformar em IAs independentes por estação ou por funcionário.

A IA não será fonte oficial de dados, regras ou estados. Ela interpretará informações fornecidas pelo próprio sistema, enquanto motores determinísticos, evidências e políticas oficiais continuarão responsáveis por validar permissões, estados e transições.

A função cognitiva do Mheibos será participar ativamente da operação: detectar problemas, formular hipóteses, propor prioridades, gerar planos de ação, acompanhar resultados e explicar por que determinada recomendação foi apresentada. Alterações persistentes continuarão dependentes de autorização humana e dos mecanismos formais do sistema.

---

## 2. Objetivo

Esta RFC responde às seguintes perguntas:

- o que significa existir um único Mheibos para toda a empresa;
- quais responsabilidades pertencem à IA;
- quais decisões nunca pertencem ao modelo de linguagem;
- como o sistema transforma dados operacionais em recomendações;
- como a IA atua de forma proativa sem retirar a autonomia humana;
- como problemas pontuais geram planos de ação;
- como problemas recorrentes geram propostas de melhoria contínua;
- como riscos futuros são antecipados;
- como recomendações relevantes devem ser explicadas;
- como o sistema controla profundidade, contexto e custo de investigação;
- como análises preservam dignidade e privacidade internas.

Esta RFC não define o modelo de linguagem específico, a interface visual das intervenções, o armazenamento da memória, as regras de governança do conhecimento, o modelo de eventos ou os mecanismos técnicos de autorização. Esses assuntos pertencem a RFCs próprios.

---

## 3. Decisões fundamentais

A Arquitetura Cognitiva adota as seguintes decisões:

1. Existe uma única identidade cognitiva denominada Mheibos para toda a empresa.
2. A IA interpreta a realidade operacional, mas não é fonte oficial do estado.
3. Dados, evidências, permissões e regras determinísticas limitam qualquer conclusão ou ação cognitiva.
4. Alterações persistentes começam como sugestões, propostas ou planos sujeitos à decisão humana.
5. O Mheibos detecta problemas e produz planos de ação para auxiliar o responsável original.
6. Informar a gestão não transfere automaticamente a responsabilidade operacional.
7. Problemas recorrentes podem gerar hipóteses de causa raiz e propostas de melhoria permanente.
8. A IA atua como planejadora operacional diária e pode antecipar prioridades antes de solicitação explícita.
9. Previsões de risco podem gerar planos preventivos, mas não execução persistente automática.
10. Recomendações estratégicas podem ser muito fortes, mas não obrigam o gestor a aceitar ou justificar sua decisão.
11. Toda recomendação relevante deve ser explicável.
12. A IA responde primeiro com o contexto disponível e aprofunda investigações somente quando necessário e autorizado.
13. Análises devem priorizar processos e causas, preservando dignidade e privacidade das pessoas.

---

## 4. Escopo

### 4.1 Incluído

Esta RFC especifica:

- identidade cognitiva única;
- interpretação contextual;
- separação entre cognição e autoridade determinística;
- ciclo cognitivo de observação, interpretação, recomendação e acompanhamento;
- detecção de anomalias e gargalos;
- formulação de hipóteses;
- geração de planos de ação;
- planejamento operacional proativo;
- previsão de riscos;
- recomendações operacionais e estratégicas;
- explicabilidade;
- níveis de confiança e incerteza comunicada;
- aprofundamento progressivo de investigações;
- limites humanos, sociais e de privacidade.

### 4.2 Fora do escopo

Não fazem parte desta RFC:

- escolha do LLM;
- quantidade de parâmetros do modelo;
- hardware de inferência;
- prompt definitivo do sistema;
- técnicas específicas de RAG, embeddings ou banco vetorial;
- estrutura física da memória curta ou longa;
- aprovação de ensinamentos e promoção de conhecimento oficial;
- controle visual detalhado da interface;
- notificações, pop-ups e escalonamento de pendências;
- definição de Missões e Teamwork;
- formato de eventos, evidências e auditoria;
- perfis, permissões e ações sensíveis;
- simulações financeiras e estratégicas detalhadas;
- integração direta com WhatsApp ou outros canais.

Esses temas poderão ser utilizados pela Arquitetura Cognitiva por meio de contratos, mas serão especificados em seus RFCs proprietários.

---

## 5. Identidade cognitiva única

### 5.1 Um único Mheibos

A empresa não possuirá uma IA independente por computador, setor ou usuário.

Todos os usuários interagirão com uma única entidade cognitiva: o Mheibos.

Essa identidade deverá preservar coerência de comportamento, princípios e linguagem em toda a instalação, ainda que suas respostas e seu alcance variem conforme o contexto de cada interação.

### 5.2 Adaptação por contexto

O Mheibos deverá adaptar sua atuação considerando, no mínimo:

- identidade do usuário;
- perfil e permissões;
- responsabilidades atribuídas;
- módulo, processo ou missão atual;
- estado operacional observado;
- histórico relevante autorizado;
- momento e urgência;
- impacto da situação;
- nível de detalhe adequado ao usuário.

A adaptação não cria uma nova personalidade cognitiva. Ela representa apenas uma visão contextual e autorizada da mesma entidade.

### 5.3 Coerência institucional

O Mheibos deverá manter os mesmos princípios fundamentais para todos os usuários.

Ele não poderá recomendar a um usuário uma prática que considere inválida para outro apenas por conveniência, salvo quando diferenças de permissão, responsabilidade ou contexto justificarem comportamentos diferentes.

### 5.4 Isolamento de contexto

A identidade cognitiva única não autoriza exposição indiscriminada de informações.

O Mheibos deverá utilizar somente dados que o usuário atual possa acessar ou que sejam estritamente necessários a uma função autorizada do sistema.

Conhecer uma informação na instalação não significa poder revelá-la em qualquer conversa.

---

## 6. Fonte da verdade e autoridade cognitiva

### 6.1 A IA não é fonte oficial

O modelo de linguagem não poderá declarar como verdadeiro um estado operacional apenas porque o inferiu ou porque apareceu em uma conversa anterior.

Sempre que a resposta depender do estado real da empresa, o Mheibos deverá consultar os dados, eventos, evidências e serviços oficiais disponíveis.

### 6.2 Separação de responsabilidades

A arquitetura deverá manter a seguinte separação:

```text
Dados, eventos e evidências
          ↓
Motores determinísticos e políticas
          ↓
Estado operacional validado
          ↓
Camada de contexto cognitivo
          ↓
IA interpreta, explica e propõe
          ↓
Mheibos valida a resposta e as ações
          ↓
Usuário decide ou executa
```

### 6.3 Autoridade dos motores determinísticos

Pertencem aos componentes determinísticos, e não à IA:

- autenticação;
- autorização;
- validação de permissões;
- regras obrigatórias;
- transições oficiais de estado;
- cálculos financeiros oficiais;
- bloqueios;
- consistência dos dados;
- classificação formal de ações sensíveis;
- persistência e auditoria.

### 6.4 Responsabilidades da IA

Pertencem à camada cognitiva:

- interpretar contexto;
- resumir situações;
- identificar relações relevantes;
- formular hipóteses;
- explicar riscos;
- sugerir prioridades;
- propor planos;
- preparar alternativas;
- estimar impactos quando houver base suficiente;
- comunicar incertezas;
- acompanhar o resultado de recomendações aprovadas.

### 6.5 Validação de saídas

Resultados do modelo deverão ser tratados como propostas estruturadas, não como comandos confiáveis por natureza.

Antes de qualquer uso operacional, o Mheibos deverá verificar:

- compatibilidade com permissões;
- existência dos objetos citados;
- consistência com o estado atual;
- validade das ações propostas;
- presença de campos obrigatórios;
- conflito com regras ou políticas;
- necessidade de confirmação humana.

---

## 7. Ciclo cognitivo operacional

A atuação cognitiva do Mheibos seguirá um ciclo geral:

```text
Observar
   ↓
Selecionar contexto
   ↓
Interpretar
   ↓
Detectar situação relevante
   ↓
Explicar
   ↓
Sugerir ou planejar
   ↓
Obter decisão humana quando necessária
   ↓
Acompanhar o resultado
   ↓
Reavaliar
```

### 7.1 Observar

A camada cognitiva recebe estados, eventos, evidências, indicadores e solicitações já selecionados pelos componentes do Mheibos.

Ela não deverá explorar livremente toda a instalação sem motivo definido.

### 7.2 Selecionar contexto

O sistema deverá reunir somente as informações necessárias à questão atual, respeitando permissões, relevância e custo computacional.

### 7.3 Interpretar

A IA relaciona fatos, identifica bloqueios, compara o estado atual com objetivos e procura anomalias ou riscos.

### 7.4 Explicar

Antes de recomendar uma ação relevante, o Mheibos deverá ser capaz de apresentar o problema de forma compreensível.

### 7.5 Sugerir ou planejar

A saída cognitiva poderá assumir diferentes formas:

- resposta informativa;
- alerta;
- recomendação;
- plano de ação;
- hipótese de causa raiz;
- proposta de melhoria;
- previsão de risco;
- preparação de uma missão;
- solicitação de decisão.

### 7.6 Acompanhar

Quando uma sugestão for aceita e produzir uma intervenção ou mudança, o Mheibos deverá acompanhar o resultado por meio dos indicadores e estados disponíveis.

---

## 8. Princípio da sugestão antes da imposição

### 8.1 Regra geral

A camada cognitiva deverá começar alterações reais como sugestões.

Isso inclui:

- mudanças de processo;
- reorganizações permanentes;
- alteração de prioridades oficiais;
- mudança de responsável;
- envio de mensagens;
- criação de tarefas persistentes;
- aplicação de novos procedimentos;
- alteração de dados;
- execução de planos.

### 8.2 Conteúdo mínimo da sugestão

Uma sugestão relevante deverá indicar, quando aplicável:

- o que foi identificado;
- o que a IA propõe;
- por que propõe;
- quais registros serão afetados;
- qual resultado espera;
- quais riscos existem;
- se a ação poderá ser desfeita;
- qual decisão humana é necessária.

### 8.3 Ações sem persistência

Ações cognitivas que apenas organizem a apresentação temporária, preparem contexto ou destaquem informações poderão ser tratadas pela RFC-0009.

Esta RFC não autoriza a IA a converter uma reorganização visual em mudança oficial de dados.

### 8.4 Configurações futuras de autonomia

Empresas poderão futuramente configurar categorias de autonomia, mas nenhuma configuração poderá eliminar:

- os limites de permissão;
- a autoridade das regras determinísticas;
- a auditoria;
- a supervisão humana sobre decisões críticas;
- os princípios fundamentais do projeto.

---

## 9. Detecção de problemas

### 9.1 Situações detectáveis

O Mheibos poderá identificar, entre outras:

- acúmulo de pedidos em uma etapa;
- prazos em risco;
- bloqueios recorrentes;
- pendências sem ação;
- dependências que impedem múltiplos processos;
- aumento anormal de retrabalho;
- divergências entre capacidade e demanda;
- concentração excessiva de tarefas;
- sequência operacional ineficiente;
- padrão de falhas repetidas;
- risco de não cumprimento de objetivo.

### 9.2 Evidência mínima

A IA não deverá apresentar uma suspeita como fato confirmado.

Cada detecção deverá distinguir:

- fatos observados;
- relações calculadas;
- hipótese interpretativa;
- grau de confiança;
- dados ausentes;
- condições que podem alterar a conclusão.

### 9.3 Foco no processo

A descrição inicial de um problema deverá priorizar:

- etapa afetada;
- volume;
- tempo;
- impacto;
- dependências;
- risco ao objetivo.

A identificação nominal de pessoas deverá ocorrer somente quando autorizada e necessária para assistência, atribuição ou gestão.

---

## 10. Planos de ação operacionais

### 10.1 Finalidade

Ao detectar um problema operacional relevante, o Mheibos poderá produzir um plano de ação para auxiliar o responsável a recuperar a operação.

O plano não deve servir como punição ou substituição imediata do usuário.

### 10.2 Estrutura mínima

Um plano de ação deverá poder conter:

- problema identificado;
- objetivo de recuperação;
- fatos e indicadores utilizados;
- tarefas propostas;
- ordem ou prioridade;
- prazos sugeridos;
- responsável atual;
- dependências;
- critérios de conclusão;
- resultado esperado;
- pontos de revisão;
- riscos e incertezas.

### 10.3 Ajuda antes de substituição

O primeiro objetivo do plano será permitir que o responsável original solucione a situação.

Informar gerente ou administrador não altera automaticamente:

- autoria;
- responsabilidade;
- propriedade da tarefa;
- permissão;
- avaliação de desempenho.

### 10.4 Visibilidade da gestão

Quando o impacto justificar supervisão, a gestão poderá receber:

- descrição do problema;
- gravidade;
- plano sugerido;
- responsável;
- evolução;
- risco de não conclusão;
- necessidade de apoio.

A forma de notificação e escalonamento pertence à RFC-0012.

### 10.5 Aprovação e aplicação

A criação cognitiva do plano não equivale à criação automática de tarefas oficiais.

A persistência do plano, sua transformação em Missão ou a alteração de responsabilidades seguirá os RFCs de Interface, Missões, Permissões e Auditoria.

---

## 11. Melhoria contínua e causa raiz

### 11.1 Problema recorrente

Quando o mesmo tipo de problema ocorrer repetidamente, o Mheibos não deverá limitar-se a tratar cada ocorrência de forma isolada.

Ele poderá iniciar uma análise de melhoria contínua.

### 11.2 Hipótese de causa raiz

A IA poderá formular uma hipótese de causa raiz, desde que apresente claramente:

- padrão observado;
- período analisado;
- ocorrências consideradas;
- fatores correlacionados;
- explicações alternativas;
- limitações da análise;
- confiança estimada.

Correlação não deverá ser apresentada como causalidade comprovada.

### 11.3 Proposta de melhoria

A proposta poderá conter:

- mudança sugerida;
- processo afetado;
- benefício esperado;
- riscos;
- custo operacional;
- indicadores de acompanhamento;
- período de teste;
- condição de reversão.

A promoção de uma proposta a procedimento oficial pertence à governança definida no RFC-0016.

### 11.4 Verificação de resultado

Após uma melhoria aprovada, o Mheibos deverá poder comparar o período anterior e posterior, informando:

- se o problema diminuiu;
- em que proporção;
- quais efeitos colaterais surgiram;
- se o resultado é conclusivo;
- se a mudança deve continuar, ser ajustada ou revertida.

### 11.5 Ciclo de melhoria

```text
Detectar recorrência
        ↓
Formular hipótese
        ↓
Propor melhoria
        ↓
Aprovação humana
        ↓
Aplicação pelos componentes oficiais
        ↓
Medir resultados
        ↓
Explicar o efeito
        ↓
Manter, ajustar ou reverter
```

---

## 12. Planejamento operacional proativo

### 12.1 Atuação antes da solicitação

O Mheibos poderá analisar a operação antes de um pedido explícito do usuário e apresentar prioridades relevantes.

Essa atuação materializa o princípio de que o sistema participa da operação e não espera que o usuário descubra sozinho o que merece atenção.

### 12.2 Planejamento personalizado

O planejamento deverá variar conforme:

- perfil;
- permissões;
- responsabilidades;
- objetivos ativos;
- pendências próprias;
- processos sob supervisão;
- prazos do período;
- criticidade;
- contexto temporal.

Exemplos:

- um Designer/Vendedor recebe artes, aprovações, atendimentos e metas próprias;
- um responsável financeiro recebe saldos, vencimentos e cobranças;
- um gerente recebe gargalos, riscos coletivos e capacidade operacional;
- um administrador recebe visão ampla da instalação e decisões estratégicas.

### 12.3 Saída do planejamento

O planejamento poderá apresentar:

- prioridades sugeridas;
- justificativa da ordem;
- riscos do dia;
- processos bloqueados;
- pendências herdadas;
- missões pausadas;
- preparação de um ambiente de trabalho;
- ações recomendadas.

A apresentação visual e o briefing de início do dia pertencem às RFCs 0009 e 0012.

### 12.4 Não substituição da agenda humana

O plano proativo é uma recomendação operacional.

O usuário ou gestor autorizado poderá alterar a ordem, adiar, rejeitar ou iniciar outro objetivo, salvo obrigações formais já definidas por regras externas à IA.

---

## 13. Previsão de riscos

### 13.1 Capacidade preventiva

O Mheibos poderá estimar riscos futuros com base em estados, prazos, capacidade, histórico e dependências.

Exemplos:

- probabilidade de atraso;
- fila prestes a ultrapassar capacidade;
- processo que bloqueará várias entregas;
- pendência financeira próxima de escalonamento;
- missão com ritmo insuficiente;
- concentração de demanda em determinado período.

### 13.2 Natureza da previsão

Toda previsão deverá ser apresentada como estimativa, não como certeza.

Ela deverá incluir:

- horizonte temporal;
- fatores utilizados;
- nível de confiança;
- cenários alternativos;
- eventos que podem invalidá-la.

### 13.3 Plano preventivo

Uma previsão de risco poderá gerar proposta contendo:

- prioridades;
- tarefas;
- prazos;
- responsáveis sugeridos;
- impacto esperado;
- condição de revisão.

A IA não poderá persistir essas alterações sem o fluxo de aprovação correspondente.

### 13.4 Atualização contínua

Previsões deverão ser recalculadas quando surgirem evidências relevantes.

O sistema deverá evitar manter alertas desatualizados depois que o risco tiver sido resolvido ou substancialmente alterado.

---

## 14. Recomendações operacionais e estratégicas

### 14.1 Recomendação operacional

Relaciona-se a ações de curto prazo dentro de processos existentes.

Exemplos:

- priorizar determinados pedidos;
- resolver um bloqueio;
- revisar uma etapa;
- iniciar um plano de recuperação.

### 14.2 Recomendação estratégica

Relaciona-se a decisões de maior alcance, como:

- capacidade;
- contratação;
- preços;
- alteração permanente de processo;
- redistribuição estrutural de recursos;
- mudança de política.

A análise detalhada de cenários pertence à RFC-0015.

### 14.3 Recomendação muito forte

Quando dados e impacto justificarem, o Mheibos poderá apresentar uma recomendação estratégica de forma enfática.

Ela deverá:

- destacar a gravidade;
- explicar o risco;
- mostrar as evidências;
- apresentar alternativas;
- indicar a recomendação principal;
- informar confiança e incertezas.

### 14.4 Limite de autoridade

Mesmo com alta confiança, a IA não poderá exigir que um gestor:

- aceite a recomendação;
- justifique formalmente sua rejeição;
- delegue sua decisão ao modelo;
- execute uma mudança estratégica automaticamente.

A decisão estratégica permanece humana.

---

## 15. Explicabilidade

### 15.1 Obrigatoriedade

Toda recomendação relevante deverá poder ser explicada em linguagem adequada ao usuário.

A explicação não poderá ser substituída por afirmações como:

- “a IA decidiu”;
- “o algoritmo detectou”;
- “o sistema sabe que é melhor”.

### 15.2 Conteúdo da explicação

Quando aplicável, a explicação deverá apresentar:

- pergunta ou objetivo analisado;
- fatos utilizados;
- período considerado;
- relações identificadas;
- regras determinísticas relevantes;
- impacto de não agir;
- alternativas avaliadas;
- recomendação final;
- nível de confiança;
- incertezas;
- dados ausentes;
- simulação utilizada.

### 15.3 Níveis de detalhe

A explicação poderá ser progressiva:

1. resumo objetivo;
2. principais motivos;
3. evidências e relações;
4. análise detalhada;
5. investigação ampliada, quando autorizada.

### 15.4 Rastreabilidade

A explicabilidade cognitiva deverá apontar para dados e registros oficiais, quando disponíveis.

Ela não substitui a auditoria técnica ou operacional definida na RFC-0006.

### 15.5 Honestidade epistêmica

O Mheibos deverá distinguir explicitamente:

- fato confirmado;
- regra oficial;
- cálculo;
- inferência;
- hipótese;
- previsão;
- opinião ou recomendação.

---

## 16. Resposta rápida e investigação progressiva

### 16.1 Responder com o contexto disponível

A IA deverá primeiro utilizar o contexto já disponível e suficiente para produzir uma resposta útil.

Ela não deverá iniciar buscas amplas, lentas ou dispendiosas quando uma resposta confiável puder ser dada com dados próximos.

### 16.2 Relações operacionais próximas

A seleção inicial deverá priorizar:

- objeto atual;
- processo relacionado;
- estado;
- responsável;
- dependências diretas;
- eventos recentes;
- regras aplicáveis;
- objetivo do usuário.

### 16.3 Critérios de aprofundamento

Uma investigação mais ampla poderá ser necessária quando:

- houver contradição entre fontes;
- faltarem dados essenciais;
- a decisão tiver alto impacto;
- a causa não estiver nas relações próximas;
- o usuário solicitar maior profundidade;
- a confiança inicial for insuficiente.

### 16.4 Consentimento para investigação ampliada

Quando a investigação adicional puder consumir tempo ou recursos significativos, o Mheibos deverá:

1. apresentar o que já encontrou;
2. explicar a limitação atual;
3. informar o que pretende investigar;
4. solicitar autorização do usuário.

### 16.5 Critério de parada

A investigação deverá terminar quando:

- a pergunta estiver suficientemente respondida;
- novas fontes deixarem de alterar materialmente a conclusão;
- o limite autorizado tiver sido atingido;
- faltarem dados que somente uma pessoa possa fornecer;
- o custo superar o benefício esperado.

---

## 17. Dignidade, privacidade e proteção humana

### 17.1 Processo antes da pessoa

Ao comunicar um problema, o Mheibos deverá priorizar a descrição do processo, da carga e do impacto.

Exemplo adequado:

> “A etapa de criação acumula 18 pedidos e está acima da capacidade prevista.”

Exemplo inadequado para exposição geral:

> “João é o responsável pelo atraso da empresa.”

### 17.2 Identificação necessária

A identificação individual poderá ocorrer quando:

- o usuário está recebendo assistência sobre sua própria operação;
- um gerente autorizado precisa coordenar o trabalho;
- existe responsabilidade formal vinculada ao registro;
- uma investigação autorizada exige rastreabilidade;
- a segurança ou auditoria exige autoria.

### 17.3 Menor exposição possível

Mesmo quando a identificação for permitida, o sistema deverá revelar somente o necessário à finalidade da interação.

### 17.4 Proibição de julgamento pessoal

A IA não deverá:

- humilhar;
- acusar sem evidência;
- criar rankings públicos depreciativos;
- transformar estimativas em rótulos pessoais;
- diagnosticar características psicológicas ou médicas;
- utilizar informações privadas para constranger o usuário.

### 17.5 Linguagem orientada à solução

A comunicação deverá ser:

- respeitosa;
- objetiva;
- gentil;
- contextualizada;
- orientada a próximos passos;
- proporcional à gravidade.

A governança detalhada desses limites pertence à RFC-0016.

---

## 18. Contratos com os componentes da plataforma

### 18.1 Entrada cognitiva

A camada cognitiva deverá receber contexto estruturado, contendo somente campos autorizados e relevantes.

Uma entrada poderá conter:

- identidade contextual;
- objetivo;
- entidades relacionadas;
- estados validados;
- eventos relevantes;
- evidências;
- regras aplicáveis;
- histórico autorizado;
- indicadores;
- pergunta ou gatilho.

### 18.2 Saída cognitiva

A resposta do modelo deverá ser convertida em uma estrutura controlada, podendo incluir:

- tipo de resposta;
- resumo;
- fatos citados;
- hipótese;
- recomendação;
- confiança;
- incertezas;
- ações propostas;
- plano sugerido;
- necessidade de confirmação;
- necessidade de investigação adicional.

### 18.3 Proibição de acesso direto

O modelo de linguagem não deverá:

- consultar diretamente o banco;
- executar SQL;
- alterar estados;
- chamar componentes internos sem mediação;
- controlar diretamente a interface;
- enviar mensagens externas;
- decidir permissões;
- gravar conhecimento oficial.

Toda capacidade deverá ser mediada por ferramentas e serviços controlados pelo Mheibos.

### 18.4 Falha ou indisponibilidade

Quando a IA estiver indisponível:

- o estado oficial permanece válido;
- regras determinísticas continuam funcionando;
- módulos essenciais continuam utilizáveis;
- nenhuma operação já confirmada deverá depender de uma nova inferência para permanecer consistente;
- o usuário deverá ser informado de que recursos cognitivos estão temporariamente indisponíveis.

---

## 19. Modos de atuação cognitiva

A arquitetura deverá suportar, no mínimo, os seguintes modos conceituais:

### 19.1 Resposta sob demanda

O usuário faz uma pergunta ou solicita ajuda.

### 19.2 Assistência contextual

O sistema percebe uma oportunidade de ajuda relacionada ao trabalho atual.

### 19.3 Detecção proativa

O Mheibos identifica problema, risco ou bloqueio sem solicitação explícita.

### 19.4 Planejamento

A IA organiza prioridades, tarefas e prazos como proposta.

### 19.5 Acompanhamento

O sistema observa a evolução de um plano ou recomendação aceita.

### 19.6 Melhoria contínua

A IA analisa recorrências, formula hipóteses e mede mudanças aprovadas.

### 19.7 Explicação

O usuário ou gestor solicita os fundamentos de uma conclusão.

Esses modos poderão compartilhar o mesmo modelo, mas deverão possuir contratos e limites claros no Mheibos.

---

## 20. Requisitos de qualidade cognitiva

### 20.1 Correção factual

A IA deverá utilizar prioritariamente dados oficiais e declarar quando não houver evidência suficiente.

### 20.2 Relevância

A resposta deverá concentrar-se no objetivo atual e evitar informações sem impacto operacional.

### 20.3 Proporcionalidade

A intensidade da recomendação deverá corresponder à gravidade, urgência e confiança.

### 20.4 Consistência

Recomendações semelhantes deverão seguir os mesmos princípios, salvo diferenças contextuais explicáveis.

### 20.5 Previsibilidade

O usuário deverá compreender o que a IA pode fazer, o que depende de confirmação e o que nunca fará sozinha.

### 20.6 Transparência

Incertezas, limitações e dados ausentes deverão ser comunicados.

### 20.7 Eficiência

A IA deverá evitar contexto excessivo, investigações desnecessárias e uso de recursos sem benefício proporcional.

### 20.8 Utilidade operacional

Uma recomendação deve conduzir a uma decisão, ação ou compreensão melhor. Texto longo sem consequência prática não constitui boa assistência.

### 20.9 Preservação humana

A arquitetura deverá ajudar pessoas a resolver problemas sem transformar a IA em instrumento de constrangimento, vigilância abusiva ou julgamento pessoal.

---

## 21. Falhas cognitivas previstas

### 21.1 Informação insuficiente

O Mheibos deverá reconhecer quando faltarem dados e solicitar somente a informação necessária.

### 21.2 Conflito entre fontes

O sistema deverá indicar a divergência e priorizar a fonte oficial definida pelos contratos da plataforma.

### 21.3 Baixa confiança

A IA deverá reduzir a força da recomendação, apresentar alternativas ou pedir investigação adicional.

### 21.4 Resposta inválida do modelo

Saídas malformadas, incompatíveis com permissões ou contraditórias com regras deverão ser rejeitadas pela camada de validação.

### 21.5 Recomendação desatualizada

Antes da execução, o sistema deverá verificar se o estado utilizado ainda é atual.

### 21.6 Ausência de resposta do modelo

A interface deverá degradar de forma compreensível, sem bloquear funções determinísticas essenciais.

### 21.7 Excesso de proatividade

A frequência e a intensidade das intervenções deverão ser controladas pelas políticas da RFC-0009, evitando que a assistência se torne ruído.

---

## 22. Relação com os demais RFCs

| RFC | Responsabilidade relacionada |
|---|---|
| RFC-0000 | Propósito do Mheibos como memória operacional ativa |
| RFC-0001 | Princípios permanentes, supervisão humana, fonte da verdade e explicabilidade |
| RFC-0002 | Processos, estados, evidências e realidade operacional interpretada pela IA |
| RFC-0003 | Central, Clientes, Gateway de IA e fronteiras técnicas |
| RFC-0005 | Entidades e dados usados no contexto cognitivo |
| RFC-0006 | Eventos, evidências, auditoria e rastreabilidade das ações |
| RFC-0007 | Identidade, permissões e limites herdados pela IA |
| RFC-0008 | Disponibilidade cognitiva e contexto durante operação offline |
| RFC-0009 | Apresentação visual, intervenções e controle da interface |
| RFC-0010 | Transformação de planos em Missões e Teamwork |
| RFC-0011 | Conhecimento, memória e recuperação de contexto |
| RFC-0012 | Briefing, pendências, notificações e escalonamento |
| RFC-0013 | Regras comerciais e financeiras interpretadas pela IA |
| RFC-0014 | Canais, arquivos e integrações usados como contexto ou ação mediada |
| RFC-0015 | Analytics e simulações que sustentam recomendações estratégicas |
| RFC-0016 | Ensino, aprovação, governança, confiança e segurança da IA |

Esta RFC define como o Mheibos pensa e recomenda. Os RFCs relacionados definem de onde vêm os dados, como as ações são autorizadas, como aparecem na interface e como são registradas.

---

## 23. Consequências da decisão

### 23.1 Benefícios

- identidade coerente em toda a empresa;
- assistência personalizada sem fragmentar o conhecimento;
- separação clara entre inteligência e fonte da verdade;
- participação proativa do sistema;
- ajuda operacional antes de substituição humana;
- melhoria contínua baseada em resultados;
- recomendações transparentes;
- redução de investigações desnecessárias;
- preservação da autoridade do usuário e do gestor;
- caminho para trocar o modelo sem redefinir o comportamento cognitivo.

### 23.2 Custos e limitações

- necessidade de preparar contexto estruturado e confiável;
- validação obrigatória de toda saída do modelo;
- maior esforço para explicar recomendações;
- necessidade de métricas para acompanhar planos e melhorias;
- complexidade para controlar proatividade sem gerar ruído;
- dependência de RFCs complementares para ações, memória e governança;
- impossibilidade de tratar o modelo como executor livre da plataforma.

### 23.3 Riscos

- confundir hipótese com fato;
- permitir que o modelo se torne fonte de estado;
- produzir recomendações sem evidência suficiente;
- expor usuários desnecessariamente;
- sobrecarregar a pessoa com alertas e planos;
- criar planos impossíveis por ignorar capacidade real;
- manter recomendações desatualizadas;
- ocultar incerteza para parecer convincente;
- executar alterações persistentes sem confirmação;
- misturar cognição com regras determinísticas.

---

## 24. Critérios de conformidade

Uma implementação estará em conformidade com esta RFC somente se:

1. todos os usuários interagirem com uma identidade cognitiva coerente denominada Mheibos;
2. respostas forem limitadas pela identidade, permissões e contexto do usuário;
3. o modelo não for utilizado como fonte oficial de dados ou estados;
4. regras, permissões e transições críticas forem validadas por componentes determinísticos;
5. alterações persistentes propostas pela IA exigirem o fluxo de confirmação aplicável;
6. planos de ação priorizarem ajudar o responsável original;
7. informar a gestão não transferir automaticamente responsabilidade;
8. recorrências puderem gerar hipótese, proposta de melhoria e acompanhamento de resultado;
9. planejamento proativo for personalizado e apresentado como recomendação;
10. previsões forem identificadas como estimativas, com confiança e incertezas;
11. recomendações estratégicas não obrigarem o gestor a aceitar ou justificar a rejeição;
12. recomendações relevantes puderem explicar fatos, relações, impacto e limitações;
13. investigações amplas dependerem de necessidade e consentimento quando tiverem custo relevante;
14. análises priorizarem processos e limitarem exposição de pessoas;
15. saídas do modelo forem validadas antes de qualquer uso operacional;
16. a indisponibilidade da IA não invalidar o estado nem impedir as funções determinísticas essenciais.

---

## 25. Decisões adiadas

As seguintes decisões serão tomadas em RFCs posteriores ou na implementação:

- modelo de linguagem inicial;
- formato definitivo do contexto enviado ao modelo;
- esquema definitivo da resposta estruturada;
- cálculo técnico do nível de confiança;
- métricas concretas para detecção de anomalias;
- limiares de proatividade;
- frequência do planejamento diário;
- formato visual das explicações;
- duração e critérios de testes de melhoria;
- sistema de avaliação da qualidade das recomendações;
- mecanismo de cache de respostas;
- política de retenção de interações cognitivas;
- autonomia configurável por categoria de ação;
- ferramentas específicas disponíveis ao modelo.

Essas decisões deverão respeitar os limites desta RFC.

---

## 26. Declaração normativa

O Mheibos possuirá uma única identidade cognitiva para toda a empresa. Essa identidade interpretará o estado operacional, detectará problemas, antecipará riscos, explicará situações, sugerirá prioridades e produzirá planos de ação.

A IA nunca será fonte oficial da verdade, nunca substituirá motores determinísticos e nunca ultrapassará as permissões do usuário. Alterações persistentes serão apresentadas como propostas e dependerão dos fluxos humanos e sistêmicos de autorização.

A proatividade do Mheibos terá como finalidade preservar a atenção, ajudar o responsável a recuperar a operação e impedir que riscos relevantes permaneçam invisíveis. Recomendações importantes deverão ser explicáveis, proporcionais, honestas quanto à incerteza e respeitosas com a dignidade e a privacidade das pessoas.

---

## 27. Rastreabilidade com o Inventário Oficial

| Decisão | Seção principal desta RFC |
|---|---|
| INV-107 — único Mheibos para toda a empresa | 5 |
| INV-108 — IA interpreta; sistema mantém dados e regras oficiais | 6 e 18 |
| INV-109 — IA sugere antes de impor | 8 |
| INV-110 — detecção de problemas e planos de ação | 9 e 10 |
| INV-111 — ajuda antes de substituição | 10.3 e 10.4 |
| INV-112 — recorrência e melhoria contínua | 11 |
| INV-113 — planejamento operacional diário | 12 |
| INV-114 — previsão de risco e planos para aprovação | 13 |
| INV-115 — recomendações estratégicas muito fortes | 14 |
| INV-116 — explicabilidade | 15 |
| INV-117 — resposta cedo e aprofundamento sob demanda | 16 |
| INV-118 — dignidade e privacidade internas | 17 |
