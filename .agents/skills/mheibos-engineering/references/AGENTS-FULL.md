# AGENTS.md — Constituição Operacional dos Agentes de Engenharia do Mheibos

**Projeto:** Mheibos Intelligent Operating System  
**Status:** Regra operacional inicial para Codex e agentes de engenharia  
**Escopo:** Todo o repositório, salvo quando um `AGENTS.md` mais específico existir em um subdiretório  
**Idioma oficial da documentação de arquitetura e engenharia:** Português do Brasil  
**Autoridade:** Subordinado ao Manifesto, aos Princípios Fundamentais, às RFCs e ao Inventário Oficial de Decisões Arquiteturais

---

## 1. Finalidade deste arquivo

Este arquivo define como qualquer agente de engenharia — incluindo Codex, agentes auxiliares, automações de revisão e futuros colaboradores — deve trabalhar no repositório do Mheibos.

Ele não define o funcionamento do produto. O funcionamento do produto pertence às RFCs.

Este arquivo define:

- como localizar a fonte correta;
- como interpretar a arquitetura;
- como planejar uma alteração;
- como implementar sem contrariar os RFCs;
- como testar;
- como documentar;
- como revisar;
- quando avançar;
- quando interromper;
- como executar trabalhos longos em loop;
- como produzir a série de documentos ENG.

O objetivo não é tornar o agente obediente a um prompt estático. O objetivo é tornar o desenvolvimento rastreável, verificável, repetível e subordinado à arquitetura oficial.

---

## 2. Regra fundamental

> O código atual demonstra o que existe.  
> As RFCs definem o que deve existir.  
> O diagnóstico explica a distância entre os dois.  
> Os documentos ENG definem como realizar a transição.  
> Nenhum agente pode inverter essa hierarquia.

Quando a implementação atual e uma RFC divergirem:

1. não trate o código atual como especificação;
2. não altere silenciosamente a RFC;
3. identifique a divergência;
4. determine se a tarefa é correção, migração, compatibilidade temporária ou decisão ainda ausente;
5. implemente segundo a fonte normativa aplicável;
6. preserve compatibilidade apenas quando ela for necessária e conscientemente planejada.

---

## 3. Hierarquia oficial das fontes

Toda decisão deve respeitar a seguinte ordem de autoridade:

1. **RFC-0000 — Manifesto do Projeto**
2. **RFC-0001 — Os 20 Princípios Fundamentais**
3. **RFCs normativas aprovadas ou adotadas como base do desenvolvimento**
4. **Inventário Oficial de Decisões Arquiteturais**
5. **Regras oficiais do projeto e contexto oficial**
6. **Documentos ENG**
7. **ADRs técnicos aprovados, quando existirem**
8. **Diagnósticos da implementação**
9. **Relatórios de funcionalidades**
10. **Código existente**
11. **Testes existentes**
12. **Comentários, nomes, convenções legadas e inferências**

Observações:

- Um diagnóstico descreve o sistema atual; ele não cria arquitetura futura.
- Um relatório funcional pode estar incompleto ou desatualizado.
- Um teste legado pode cristalizar comportamento incompatível com uma RFC.
- Comentários e nomes do código não são autoridade normativa.
- Um documento ENG nunca pode contrariar uma RFC.
- Quando duas RFCs parecerem divergir, não escolha silenciosamente uma delas. Registre o conflito.

---

## 4. Fontes obrigatórias conhecidas

Antes de iniciar trabalhos relevantes, localizar e considerar os documentos correspondentes no repositório.

### 4.1 Fundamentos

- `RFC-0000-Manifesto-do-Projeto.md`
- `RFC-0001-Os-20-Principios-Fundamentais-do-Mheibos.md`
- `RFC-0002-modelo-operacional.md`
- `MHEIBOS_PROJECT_CONTEXT.md`
- `MHEIBOS_PROJECT_RULES.md` ou variante equivalente existente

### 4.2 Arquitetura

- `RFC-0003-Arquitetura-Tecnica-da-Plataforma.md`
- `RFC-0004-Arquitetura-Cognitiva.md`
- `RFC-0005-Modelo-de-Dados.md`
- `RFC-0006-Eventos-Evidencias-e-Auditoria.md`
- `RFC-0007-Identidade-Permissoes-e-Seguranca.md`
- `RFC-0008-Operacao-Offline-e-Sincronizacao.md`
- `RFC-0009-Interface-Viva-e-Intervencoes.md`
- `RFC-0010-Missoes-e-Teamwork.md`
- `RFC-0011-Conhecimento-Memoria-e-Aprendizado.md`
- `RFC-0012-Modelo-Operacional-do-Mheibos.md`
- `RFC-0013-Modelo-Comercial-e-Financeiro.md`
- `RFC-0014-Arquivos-e-Integracoes.md`

### 4.3 Consolidação e estado atual

- `INVENTARIO-OFICIAL-DE-DECISOES-ARQUITETURAIS-DO-MHEIBOS.md`
- `Diagnostico-Arquitetura-e-Fluxos-Atuais-Mheibos-Gestor.md`
- `RELATORIO-ATUAL-DE-FUNCIONALIDADES-DO-MHEIBOS-GESTOR.md`
- `ENG-0000-Programa-de-Engenharia-e-Governanca-Documental-do-Mheibos.md`

Os nomes físicos podem conter sufixos de versão, espaços ou parênteses. O agente deve localizar o arquivo real e não assumir cegamente o nome canônico.

---

## 5. Vocabulário obrigatório

O agente deve preservar rigorosamente a terminologia do projeto.

### 5.1 Termos que não podem ser confundidos

- **Cliente comercial:** pessoa ou organização que compra da empresa usuária do Mheibos.
- **Cliente Mheibos:** aplicação instalada em uma estação e subordinada à Central.
- **Fornecedor terceirizado:** empresa externa que presta impressão, fabricação ou outro serviço.
- **Usuário:** pessoa autenticada no Mheibos.
- **Estação:** computador autorizado a executar um Cliente Mheibos.
- **Central:** autoridade global da instalação.
- **Pedido:** centro comercial e financeiro.
- **Processo:** centro da execução operacional.
- **Modelo de fluxo:** definição reutilizável.
- **Fluxo instanciado:** caminho oficial de uma ocorrência.
- **Etapa:** unidade identificável de trabalho.
- **Estado:** condição atual de uma entidade ou dimensão.
- **Evento:** fato estruturado ocorrido.
- **Evidência:** elemento verificável que sustenta fato, estado ou decisão.
- **Pendência:** obrigação não encerrada que exige acompanhamento e decisão consciente.
- **Intervenção:** comunicação ativa que busca reconhecimento, decisão ou ação.
- **Missão:** workspace persistente orientado a objetivo temporário.
- **IA / camada cognitiva:** interpreta, explica, recomenda e planeja; não substitui autoridade determinística.
- **Arquivo oficial de arte:** arquivo formalmente selecionado para produção.
- **Anexo:** arquivo relacionado, mas não necessariamente oficial para produção.

### 5.2 Regra de nomes

Quando houver risco de ambiguidade, escrever o termo completo.

Evitar usar isoladamente:

- “cliente”, quando puder significar cliente comercial ou Cliente Mheibos;
- “status”, quando a realidade exigir estado comercial, operacional, financeiro, de entrega ou de etapa;
- “usuário”, quando o papel específico for autor comercial, responsável atual, executor, aprovador ou supervisor;
- “arquivo”, quando for necessário distinguir arquivo oficial, referência, anexo ou evidência.

---

## 6. Invariantes arquiteturais permanentes

Nenhuma implementação pode violar as regras abaixo.

### 6.1 Operação e domínio

1. O Mheibos é uma memória operacional ativa.
2. O sistema deve reduzir carga cognitiva e preservar a atenção humana.
3. O Pedido não substitui o Processo.
4. Um único campo de status não pode representar toda a realidade.
5. Estados comerciais, operacionais, financeiros e de entrega devem permanecer distinguíveis.
6. Processos devem possuir objetivos, fluxo, etapas, responsabilidades e critérios de conclusão.
7. Etapas obrigatórias não podem depender apenas de lembrança humana ou sugestão da IA.
8. Toda pendência relevante deve terminar em decisão consciente.
9. A aplicação deve representar a operação real, não impor fronteiras artificiais entre setores ou softwares.
10. Vendas, arte, produção, terceirização, entrega e financeiro são visões e responsabilidades sobre a mesma realidade compartilhada.

### 6.2 Plataforma

1. A versão inicial é desktop e local.
2. Existe uma Central e múltiplos Clientes Mheibos.
3. A Central é a autoridade global.
4. O Cliente não acessa diretamente o banco central.
5. A interface não contém autoridade de negócio.
6. Serviços, domínio, aplicação, infraestrutura e apresentação devem possuir fronteiras explícitas.
7. A aplicação principal é integrada.
8. Aplicações especializadas futuras devem consumir os mesmos contratos da Central.
9. Falha da IA não pode impedir funções determinísticas essenciais.
10. Falha de uma integração não pode derrubar o sistema inteiro.

### 6.3 IA

1. A IA não é fonte oficial de dados.
2. A IA não autentica, autoriza, valida permissões nem decide transições obrigatórias.
3. A IA não acessa diretamente banco, widgets ou recursos internos.
4. Saídas do modelo são propostas estruturadas sujeitas à validação.
5. Mudanças persistentes começam como sugestão, salvo ação explicitamente autorizada por regra determinística.
6. A IA herda as permissões do usuário autenticado.
7. Recomendações relevantes devem ser explicáveis.
8. Hipóteses não podem ser apresentadas como fatos.
9. O conhecimento oficial permanece fora do modelo.
10. Trocar o modelo não pode apagar memória, regras, procedimentos ou conhecimento acumulado.

### 6.4 Eventos, evidências e auditoria

1. Toda alteração relevante deve produzir evento.
2. Auditoria relevante é imutável.
3. Exclusão comum significa desativação, cancelamento, arquivamento ou remoção lógica, não destruição silenciosa.
4. Eventos devem preservar autoria, origem, momento, contexto e mudança.
5. Operações mediadas pela IA devem distinguir proposta, autorização humana, validação e evento oficial.
6. Falhas secundárias não podem apagar o evento principal.
7. Reprocessamento deve ser idempotente.
8. Estado atual e histórico são representações distintas.

### 6.5 Segurança

1. Ocultar botão não equivale a negar permissão.
2. A autorização deve ser validada antes da persistência.
3. Cada usuário possui identidade própria do Mheibos.
4. Cada usuário possui um perfil principal, complementado por exceções explícitas.
5. Ações sensíveis exigem proteção, reautenticação e auditoria conforme a política.
6. A IA não possui privilégios ocultos.
7. Acesso deve considerar ação, recurso, registro, propriedade, responsabilidade, contexto e alcance.
8. Edição concorrente sensível deve ser controlada.

### 6.6 Offline

1. Offline é restrito e visível.
2. Estado local não substitui estado global.
3. Dados locais pendentes não podem ser descartados.
4. Reenvio não pode duplicar operações.
5. O Cliente não amplia privilégios offline.
6. Pedidos offline permanecem associados à estação de origem até incorporação.
7. Sincronização deve ser automática, visível, idempotente e recuperável.
8. Não implementar sincronização geral simplificada sem respeitar a RFC-0008.

### 6.7 Interface

1. A interface normal permanece utilizável sem chat.
2. A IA controla a interface apenas por comandos estruturados e autorizados.
3. Adaptação temporária não pode ser confundida com alteração persistente.
4. A intervenção deve usar a menor interrupção eficaz.
5. Intensidade deve ser proporcional a gravidade, urgência e confiança.
6. A interface deve explicar o que mudou, por que mudou e como restaurar.
7. Animação, cor ou brilho não podem ser a única forma de comunicar informação crítica.
8. Assistência não pode humilhar, diagnosticar ou rotular pessoas.

---

## 7. Regra específica sobre a aplicação integrada

A separação de Vendas e Produção em programas independentes não deve ser tratada como modelo operacional futuro.

A arquitetura desejada é:

- uma aplicação principal integrada;
- visualizações adaptadas por perfil, permissão, responsabilidade e contexto;
- mesma fonte de verdade;
- mesmos pedidos, processos, etapas e eventos;
- nenhuma transição dependente da abertura de outro software.

Uma experiência móvel futura pode existir como Cliente Mheibos especializado, mas:

- não cria um segundo sistema;
- não mantém estados paralelos;
- não possui fluxo próprio incompatível;
- não duplica regras da Central;
- não transforma dispositivo em fronteira de domínio.

---

## 8. Regra específica sobre fornecedores terceirizados

Não criar automação que interprete, correlacione ou acompanhe automaticamente mensagens de fornecedores terceirizados.

Para fornecedores:

- o usuário registra envio, retorno, prazo informado, correção, recebimento e demais ocorrências;
- o Mheibos pode organizar arquivos, especificações, responsáveis, datas e pendências;
- o Mheibos pode lembrar que falta uma ação ou retorno;
- o Mheibos não presume que exista API, portal, status ou confirmação padronizada;
- o Mheibos não correlaciona mensagens de WhatsApp de fornecedores com pedidos;
- o fluxo deve funcionar integralmente por registro humano explícito.

Não confundir essa regra com mensagens de clientes comerciais em canais integrados.

---

## 9. Regra específica sobre clientes comerciais

Quando um canal de atendimento ao cliente comercial estiver integrado e autorizado:

- o Mheibos pode observar mensagens;
- pode associar mensagens quando houver base confiável;
- pode sugerir interpretação;
- pode preparar ações;
- deve solicitar confirmação quando a interpretação alterar estado oficial, compromisso ou decisão relevante.

Quando a interação ocorrer presencialmente ou por canal não observado:

- o usuário registra a ocorrência;
- a origem deve ser preservada;
- o evento oficial resultante pode ser o mesmo, ainda que a evidência e o canal sejam diferentes.

---

## 10. Classificação obrigatória de mudanças

Antes de implementar, classificar a alteração como uma ou mais categorias:

- **Preservar:** a capacidade atual atende ao modelo futuro.
- **Adaptar:** a função permanece com alterações localizadas.
- **Refatorar:** o conceito permanece, mas a estrutura técnica precisa mudar.
- **Reprojetar:** o modelo operacional atual é insuficiente.
- **Substituir:** a implementação conflita com a arquitetura.
- **Adicionar:** a capacidade não existe.
- **Descontinuar:** a capacidade deixa de ter papel legítimo.
- **Compatibilidade temporária:** ponte conscientemente limitada para migração.
- **Correção normativa:** código atual contradiz uma fonte oficial.
- **Decisão pendente:** fonte insuficiente para implementar corretamente.

Registrar a classificação no plano da tarefa ou no relatório final.

---

## 11. Fluxo obrigatório para qualquer tarefa de engenharia

Nenhuma tarefa relevante deve começar diretamente pela edição de código.

### Etapa 1 — Entender a solicitação

Identificar:

- objetivo;
- comportamento esperado;
- usuários afetados;
- entidades afetadas;
- dados persistentes envolvidos;
- riscos;
- compatibilidade necessária;
- critérios de aceitação explícitos e implícitos.

### Etapa 2 — Descobrir fontes

Pesquisar:

- RFC proprietária do tema;
- RFCs dependentes;
- decisões do Inventário;
- diagnóstico atual;
- código relacionado;
- testes existentes;
- documentos ENG aplicáveis.

### Etapa 3 — Extrair restrições

Produzir internamente uma lista de:

- invariantes;
- proibições;
- permissões;
- estados;
- eventos;
- evidências;
- ações sensíveis;
- requisitos offline;
- requisitos de interface;
- requisitos de auditoria.

### Etapa 4 — Mapear a implementação atual

Localizar:

- modelos;
- views/controllers;
- forms/serializers;
- services/use cases;
- templates/componentes;
- tarefas assíncronas;
- integrações;
- migrações;
- testes;
- duplicações;
- fontes de verdade concorrentes.

### Etapa 5 — Comparar atual e futuro

Identificar:

- o que pode ser preservado;
- o que precisa de compatibilidade;
- o que deve ser removido;
- o que deve ser migrado;
- riscos de regressão;
- regras escondidas na interface;
- dados históricos que não podem ser perdidos.

### Etapa 6 — Planejar

Antes de editar, definir:

- escopo mínimo coerente;
- arquivos prováveis;
- migrações;
- sequência de implementação;
- estratégia de testes;
- rollback;
- feature flags, quando necessárias;
- atualização documental.

### Etapa 7 — Implementar em fatias verificáveis

Preferir:

- alterações pequenas e completas;
- domínio antes da interface;
- casos de uso explícitos;
- contratos estáveis;
- testes próximos da regra;
- migrações reversíveis quando possível;
- compatibilidade temporária claramente marcada.

Evitar:

- reescrita total sem necessidade;
- abstrações especulativas;
- duplicação para “resolver rápido”;
- regra de negócio em template, widget, view ou JavaScript;
- acesso direto da interface ao banco;
- uso de IA como remendo para regra ausente.

### Etapa 8 — Validar

Executar:

- testes unitários;
- testes de domínio;
- testes de integração;
- testes de autorização;
- testes de migração;
- testes de eventos e auditoria;
- testes de falha, quando aplicável;
- lint, type checking e verificações do projeto;
- inspeção de diferenças.

### Etapa 9 — Revisar conformidade

Aplicar todos os quality gates deste arquivo.

### Etapa 10 — Documentar

Atualizar:

- código e comentários estritamente necessários;
- testes;
- documentação técnica afetada;
- ADR, quando houver decisão técnica relevante;
- plano de migração;
- relatório de lacunas;
- progresso de loops longos.

---

## 12. Regra “domínio antes da interface”

Quando uma funcionalidade envolve regra operacional:

1. definir ou localizar a entidade;
2. definir ou localizar o caso de uso;
3. aplicar regra determinística;
4. gerar evento;
5. persistir;
6. expor contrato;
7. somente então criar ou alterar a interface.

A interface pode:

- coletar intenção;
- validar formato básico;
- apresentar estado;
- oferecer ações autorizadas;
- exibir erros e explicações.

A interface não pode:

- decidir transição oficial;
- calcular permissão final;
- persistir diretamente;
- inventar estado;
- ocultar inconsistência;
- duplicar regra do domínio.

---

## 13. Regra “IA depois da verdade operacional”

Não implementar automação cognitiva antes de existir uma fonte determinística confiável para o fato analisado.

Exemplos:

- não pedir à IA para decidir se uma etapa está concluída quando não existe Etapa persistida;
- não pedir à IA para inferir saldo quando o financeiro não possui fonte única;
- não pedir à IA para lembrar algo que não foi representado como pendência ou obrigação;
- não pedir à IA para corrigir passagem de fluxo que deveria ser validada pelo domínio;
- não pedir à IA para reconciliar fornecedores terceirizados por mensagens.

A IA pode enriquecer, explicar, sugerir e priorizar. Ela não substitui modelagem.

---

## 14. Política de compatibilidade e migração

A transição do Gestor atual para o novo núcleo deve ser progressiva quando isso reduzir risco.

Regras:

1. preservar dados históricos;
2. não converter silenciosamente status antigo em fatos que não podem ser comprovados;
3. registrar suposições de migração;
4. permitir reconciliação;
5. preferir projeções temporárias a duas fontes permanentes de verdade;
6. limitar o período de dupla escrita;
7. marcar todo adaptador legado;
8. criar plano explícito de remoção;
9. não manter aplicações antigas como autoridade paralela;
10. não considerar uma migração concluída enquanto o fluxo novo depender do módulo antigo para avançar.

Quando possível:

- novos pedidos usam o novo modelo;
- pedidos antigos permanecem legíveis;
- adaptação de leitura traduz legado;
- escrita nova ocorre apenas no núcleo futuro;
- status legado torna-se projeção ou compatibilidade temporária;
- módulos antigos são desativados por etapas.

---

## 15. Política de testes

### 15.1 Regras gerais

Toda alteração de comportamento precisa de teste proporcional ao risco.

Não considerar “funciona na interface” como evidência suficiente.

### 15.2 Testes mínimos por categoria

#### Domínio

- transições válidas;
- transições inválidas;
- obrigatoriedade;
- condições;
- dependências;
- cálculo de estado;
- invariantes;
- reabertura, dispensa e cancelamento.

#### Segurança

- acesso permitido;
- acesso negado;
- escopo próprio;
- escopo de equipe;
- escopo global;
- ação sensível;
- reautenticação;
- justificativa;
- auditoria.

#### Eventos

- evento produzido;
- autoria;
- valor anterior e posterior;
- correlação;
- idempotência;
- falha secundária;
- exclusão lógica.

#### Dados

- migração;
- reversão quando viável;
- preservação histórica;
- unicidade;
- referências;
- não reutilização de identidade.

#### Offline

- persistência local;
- reconexão;
- repetição;
- duplicação;
- falha parcial;
- retomada;
- isolamento por estação.

#### IA

- contexto autorizado;
- resultado estruturado;
- validação;
- negação por permissão;
- indisponibilidade do modelo;
- resposta inválida;
- sugestão não persistida sem confirmação.

#### Interface

- acessibilidade;
- estado carregando;
- vazio;
- erro;
- permissão negada;
- conectividade;
- restauração;
- adaptação temporária;
- confirmação persistente.

### 15.3 Testes de caracterização

Antes de refatorar comportamento legado importante:

- criar testes que demonstrem o comportamento atual;
- separar comportamento desejado de defeito legado;
- não preservar bug apenas porque foi caracterizado;
- marcar claramente testes que serão substituídos pela regra normativa.

---

## 16. Quality gates obrigatórios

Uma tarefa somente pode ser considerada concluída quando todos os gates aplicáveis forem aprovados.

### Gate A — Fonte

- A RFC proprietária foi identificada.
- RFCs relacionadas foram consultadas.
- O Inventário foi considerado.
- O diagnóstico foi usado apenas como descrição do atual.
- Nenhuma regra foi inventada.

### Gate B — Domínio

- Pedido e Processo não foram confundidos.
- Estados independentes foram preservados.
- Regras não foram colocadas apenas na interface.
- Responsabilidades e papéis estão explícitos.
- Etapas obrigatórias possuem validação determinística.

### Gate C — Dados

- Identidades são estáveis.
- Relações importantes são explícitas.
- Histórico não é destruído.
- Exclusões são lógicas quando aplicável.
- Migrações preservam rastreabilidade.

### Gate D — Eventos e auditoria

- Alterações relevantes geram eventos.
- Autoria e origem são preservadas.
- Ações mediadas pela IA distinguem proposta e autorização.
- Valores anteriores e posteriores são registrados quando necessários.
- Reprocessamento é seguro.

### Gate E — Segurança

- A autorização não depende da interface.
- Permissões são verificadas no caso de uso ou Central.
- A IA respeita o usuário autenticado.
- Ações sensíveis são protegidas.
- Dados não autorizados não são expostos em mensagens de erro, logs ou contexto cognitivo.

### Gate F — IA

- A IA não virou fonte da verdade.
- O modelo não acessa diretamente banco ou interface.
- Saídas são estruturadas e validadas.
- A função continua degradando de forma segura sem modelo.
- Explicabilidade e incerteza foram consideradas.

### Gate G — Offline

- Nenhuma autoridade global foi movida para o Cliente.
- Dados locais pendentes não são perdidos.
- Repetição não duplica.
- Estado offline é visível.
- O escopo respeita a RFC-0008.

### Gate H — UX

- A alteração reduz ou não aumenta injustificadamente carga cognitiva.
- O usuário não precisa abrir outro software para registrar uma etapa que pode executar no contexto atual.
- A interface comunica estado, próxima ação e bloqueios.
- Erros são acionáveis.
- Funções principais continuam acessíveis sem chat.

### Gate I — Testes

- Testes relevantes foram adicionados ou atualizados.
- Testes passam.
- Lint e verificações passam.
- Migrações foram testadas.
- Falhas previsíveis foram consideradas.

### Gate J — Documentação

- A documentação afetada foi atualizada.
- Não existe nova decisão arquitetural escondida no código.
- Compatibilidade temporária possui plano de remoção.
- Lacunas foram registradas.

---

## 17. Proibições explícitas

O agente não pode:

1. alterar RFC para acomodar código sem solicitação e decisão formal;
2. inventar regra de negócio para concluir uma tarefa;
3. criar entidade de domínio importante sem rastreabilidade normativa;
4. usar um único `status` para representar múltiplas dimensões;
5. colocar autorização apenas na interface;
6. acessar diretamente o banco central a partir do Cliente;
7. permitir que o modelo execute SQL, código ou clique arbitrário;
8. persistir sugestão da IA como fato sem validação;
9. apagar histórico para “corrigir” inconsistência;
10. manter duas fontes permanentes de verdade;
11. duplicar núcleo de negócio em aplicações especializadas;
12. usar mensagens de fornecedores terceirizados como automação de processo;
13. transformar exceção da empresa piloto em regra universal sem fonte;
14. generalizar antes de compreender a operação real;
15. introduzir abstração apenas para parecer arquiteturalmente sofisticado;
16. refatorar arquivos não relacionados sem justificativa;
17. ignorar testes falhando;
18. declarar concluído trabalho parcialmente validado;
19. esconder lacunas;
20. seguir em loop infinito após falha repetida.

---

## 18. Estados de parada obrigatórios

O agente deve interromper a parte afetada e registrar o motivo quando ocorrer:

### 18.1 Ausência de fonte

A implementação exige regra que não está definida.

Ação:

- registrar a lacuna;
- indicar documentos consultados;
- descrever opções sem escolher;
- marcar como `DECISAO_HUMANA_NECESSARIA`.

### 18.2 Conflito normativo

Duas fontes de mesma ou próxima autoridade parecem incompatíveis.

Ação:

- citar as duas;
- explicar o conflito;
- não reconciliar silenciosamente;
- marcar como `CONFLITO_NORMATIVO`.

### 18.3 Risco de perda

A mudança pode apagar, corromper ou tornar inacessíveis dados.

Ação:

- interromper;
- produzir plano de backup, migração e rollback;
- marcar como `RISCO_DE_DADOS`.

### 18.4 Validação impossível

Não existem ambiente, dependência ou dados necessários para testar.

Ação:

- concluir somente o que for demonstrável;
- listar validações não executadas;
- marcar como `VALIDACAO_PENDENTE`.

### 18.5 Escopo explosivo

A tarefa exige reescrever áreas não previstas.

Ação:

- dividir em fases;
- propor fatia mínima;
- não realizar expansão silenciosa;
- marcar como `REPLANEJAMENTO_NECESSARIO`.

### 18.6 Repetição sem progresso

O mesmo erro ocorre após três tentativas materialmente diferentes.

Ação:

- parar o loop;
- preservar logs;
- resumir hipóteses testadas;
- marcar como `BLOQUEADO_APOS_TENTATIVAS`.

---

## 19. Formato obrigatório do relatório de tarefa

Ao concluir trabalho relevante, informar:

### 19.1 Resumo

- objetivo;
- resultado;
- classificação da mudança.

### 19.2 Fontes

- RFCs consultadas;
- decisões do Inventário;
- diagnóstico consultado;
- documentos ENG aplicados.

### 19.3 Implementação

- componentes alterados;
- decisões técnicas;
- compatibilidade;
- migrações.

### 19.4 Validação

- testes executados;
- verificações;
- resultados;
- validações não executadas.

### 19.5 Riscos e pendências

- riscos remanescentes;
- compatibilidade temporária;
- remoções futuras;
- decisões humanas necessárias.

Não escrever relatórios promocionais. Ser preciso e verificável.

---

## 20. Padrões para documentos ENG

Documentos ENG definem engenharia, não produto.

Eles podem definir:

- processo de desenvolvimento;
- critérios de qualidade;
- organização de código;
- revisão;
- migração;
- testes;
- documentação;
- atuação do Codex;
- governança técnica.

Eles não podem definir:

- novos estados de negócio;
- novas permissões de produto;
- novos fluxos operacionais;
- novos poderes da IA;
- novos comportamentos de usuários;
- novas regras comerciais;
- exceções não presentes nas fontes.

Quando um ENG encontrar lacuna arquitetural, deve criar uma seção de “decisão necessária”, não preencher a lacuna.

---

## 21. Plano inicial da série ENG

A série inicial deve conter:

- **ENG-0000 — Programa de Engenharia e Governança Documental**
- **ENG-0001 — Manifesto de Engenharia**
- **ENG-0002 — Constituição do Desenvolvimento / AGENTS.md**
- **ENG-0003 — Skill Oficial do Codex**
- **ENG-0004 — Protocolo Oficial de Desenvolvimento**
- **ENG-0005 — Guia de Arquitetura**
- **ENG-0006 — Guia de Implementação**
- **ENG-0007 — Estratégia Oficial de Migração**
- **ENG-0008 — Checklist Arquitetural**
- **ENG-0009 — Guia Oficial de Revisão**
- **ENG-0010 — Glossário Oficial**

O plano pode ser refinado pelo próprio trabalho documental, mas:

- não renumerar silenciosamente;
- não duplicar responsabilidades;
- não criar documento apenas para aumentar volume;
- registrar qualquer alteração do plano.

---

## 22. Loop mestre para produção da série ENG

Quando o usuário ordenar a produção completa da série, executar o seguinte ciclo.

### 22.1 Inicialização

1. localizar todas as fontes oficiais;
2. verificar arquivos existentes;
3. criar ou carregar:
   - `engineering/ENG-SERIES-PLAN.md`;
   - `engineering/ENG-PROGRESS.json`;
   - `engineering/ENG-QUALITY-GATES.md`;
   - `engineering/ENG-CONFLICT-REPORT.md`;
   - `engineering/ENG-GLOSSARY-WORKING.md`;
4. registrar hashes ou datas das fontes, quando útil;
5. não sobrescrever documento oficial sem preservar versão ou diff.

### 22.2 Ciclo por documento

Para cada ENG pendente:

1. identificar responsabilidade exclusiva;
2. listar fontes normativas;
3. extrair requisitos;
4. montar sumário;
5. verificar sobreposição com ENGs anteriores;
6. redigir primeira versão;
7. executar revisão normativa;
8. executar revisão de terminologia;
9. executar revisão de duplicação;
10. executar revisão de aplicabilidade ao Codex;
11. corrigir;
12. executar quality gates;
13. marcar resultado:
    - `CONCLUIDO`;
    - `CONCLUIDO_COM_LACUNAS`;
    - `BLOQUEADO`;
14. atualizar `ENG-PROGRESS.json`;
15. avançar apenas se não houver conflito impeditivo.

### 22.3 Revisão cruzada final

Após produzir todos os documentos:

1. verificar contradições entre ENGs;
2. verificar contradições com RFCs;
3. verificar duplicações;
4. verificar termos;
5. verificar referências;
6. verificar se cada obrigação possui documento proprietário;
7. atualizar índice;
8. gerar mapa de dependências;
9. gerar relatório de lacunas;
10. gerar relatório final de conformidade.

### 22.4 Critério de parada do loop

O loop termina quando:

- todos os documentos estão concluídos; ou
- todos os documentos restantes estão formalmente bloqueados.

Nunca continuar inventando conteúdo apenas para marcar progresso.

---

## 23. Estrutura mínima do arquivo de progresso

Exemplo:

```json
{
  "series": "ENG",
  "version": 1,
  "current_document": "ENG-0003",
  "status": "IN_PROGRESS",
  "completed": [
    "ENG-0000",
    "ENG-0001",
    "ENG-0002"
  ],
  "completed_with_gaps": [],
  "blocked": [],
  "source_snapshot": {
    "manifesto": "present",
    "principles": "present",
    "inventory": "present",
    "diagnostic": "present"
  },
  "last_quality_gate": "passed",
  "last_updated": "ISO-8601"
}
```

O estado deve ser persistido após cada documento ou etapa longa.

---

## 24. Comando mestre recomendado

O usuário poderá iniciar o trabalho com uma instrução equivalente a:

> Execute o loop oficial de produção da série ENG definido no `AGENTS.md`.  
> Leia todas as fontes normativas, crie os arquivos de controle, produza cada documento pendente individualmente, valide-o contra as RFCs, atualize o progresso e continue até concluir ou bloquear formalmente todos os documentos.  
> Não invente arquitetura. Registre conflitos e decisões humanas necessárias.

Este comando não substitui as regras deste arquivo. Ele apenas inicia o ciclo.

---

## 25. Trabalho paralelo

Agentes paralelos podem ser usados somente quando as tarefas forem separáveis.

Usos aceitáveis:

- um agente extrai decisões de RFCs;
- outro verifica terminologia;
- outro revisa duplicações;
- outro inspeciona o código atual;
- outro executa testes.

Usos proibidos:

- dois agentes editando o mesmo documento sem coordenação;
- dois agentes implementando a mesma regra;
- agentes criando arquiteturas concorrentes;
- mesclar resultados contraditórios sem revisão;
- paralelizar etapas que dependem da mesma decisão humana.

Um agente coordenador deve manter a fonte de verdade do plano e do progresso.

---

## 26. Estratégia de commits

Quando o agente tiver autorização para alterar o repositório:

- fazer commits pequenos e coerentes;
- não misturar documentação, refatoração ampla e funcionalidade sem necessidade;
- usar mensagens que expliquem intenção;
- relacionar RFC ou ENG quando aplicável;
- não commitar arquivos temporários, segredos ou artefatos de ambiente;
- manter migrações junto da alteração que as exige;
- não reescrever histórico compartilhado sem autorização.

Formato recomendado:

```text
tipo(escopo): objetivo

Refs: RFC-000X, ENG-000Y
```

Exemplos de tipo:

- `feat`
- `fix`
- `refactor`
- `test`
- `docs`
- `migration`
- `chore`

---

## 27. Critério para ADRs

Criar ADR quando houver decisão técnica importante que:

- não esteja definida por RFC;
- tenha alternativas reais;
- afete múltiplos componentes;
- seja difícil de reverter;
- precise ser compreendida no futuro.

Exemplos:

- escolha de mecanismo de fila;
- formato de IDs;
- biblioteca de migração;
- estratégia concreta de event outbox;
- protocolo interno;
- mecanismo de cache.

ADR não pode alterar regra de produto.

---

## 28. Critério de simplicidade

O Mheibos é sofisticado na operação, mas a implementação deve evitar sofisticação gratuita.

Preferir:

- contratos explícitos;
- componentes substituíveis;
- estados claros;
- código legível;
- erros acionáveis;
- soluções testáveis;
- evolução incremental.

Evitar:

- frameworks introduzidos sem necessidade;
- microserviços prematuros;
- event sourcing completo apenas por moda;
- múltiplos modelos de IA sem benefício;
- grafos gerais como fundamento inicial;
- abstrações genéricas antes de existirem casos concretos;
- dependências de nuvem na primeira versão local.

---

## 29. Definição de pronto

Uma tarefa está pronta somente quando:

- o comportamento solicitado existe;
- as regras normativas foram respeitadas;
- a alteração está testada;
- falhas relevantes foram consideradas;
- segurança foi validada;
- eventos e auditoria foram avaliados;
- migração foi tratada;
- documentação foi atualizada;
- nenhuma pendência crítica foi escondida;
- o usuário recebe um relatório honesto.

“Código escrito” não significa “trabalho concluído”.

---

## 30. Declaração final

Todo agente que trabalhe no Mheibos deve agir como guardião da coerência entre visão, arquitetura, operação e código.

Velocidade é valiosa, mas não justifica:

- destruir rastreabilidade;
- criar fontes paralelas de verdade;
- deslocar regras para a interface;
- usar IA como remendo arquitetural;
- impor à empresa um fluxo artificial;
- perder dados;
- confundir conceitos;
- ocultar lacunas.

O melhor resultado não é o maior volume de código.

O melhor resultado é uma mudança pequena ou grande que:

- represente corretamente a realidade;
- respeite as RFCs;
- reduza carga cognitiva;
- preserve autoridade humana;
- seja testável;
- seja auditável;
- possa evoluir sem perder a memória do sistema.

---
