# PADRÃO GLOBAL DE INTERFACE DO MHEIBOS

**Projeto:** Mheibos Intelligent Operating System  
**Status:** Normativo para toda a interface  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Escopo:** Mheibos Gestor e futuras aplicações subordinadas à mesma Central  
**Aplicação:** Todas as telas, componentes, estados, módulos, templates e intervenções visuais

---

## 1. Finalidade

Este documento define as regras globais necessárias para que toda a interface do Mheibos apresente a mesma disciplina visual, independentemente do módulo, desenvolvedor, agente, perfil ou fluxo.

Ele padroniza:

- densidade;
- proporção;
- espaçamento;
- alinhamento;
- tipografia;
- dimensões;
- contenção de texto;
- composição de páginas;
- formulários;
- tabelas;
- cards;
- botões;
- status;
- alertas;
- modais;
- responsividade;
- acessibilidade;
- estados da Interface Viva.

As regras deste documento são estruturais. A identidade visual definitiva — cores de marca, logotipo, ilustrações e expressão estética — poderá evoluir sem violar a geometria e a hierarquia aqui definidas.

---

## 2. Princípio visual central

> O Mheibos deve ser compacto, respirável, previsível e orientado ao trabalho.

O Mheibos não é uma landing page, uma apresentação institucional ou um painel meramente decorativo. É uma aplicação operacional usada por longos períodos, com alta densidade de decisões, registros e informações.

A interface deve priorizar:

1. leitura rápida;
2. ação inequívoca;
3. continuidade entre módulos;
4. baixo esforço de navegação;
5. redução de carga cognitiva;
6. uso eficiente da área disponível;
7. estabilidade geométrica;
8. ausência de surpresas visuais.

---

## 3. Regras fundamentais

1. Nenhuma tela cria sua própria escala visual.
2. Nenhum módulo possui botões, inputs, cards ou tabelas exclusivos sem necessidade comprovada.
3. Todo espaçamento deve usar tokens oficiais.
4. Todo tamanho de fonte deve usar a escala tipográfica oficial.
5. Toda cor deve vir de token semântico ou de marca aprovado.
6. Toda informação deve possuir hierarquia clara.
7. Toda linha, coluna e grupo deve estar alinhado a uma grade.
8. Todo texto deve possuir comportamento explícito de contenção.
9. Todo componente deve possuir estados completos.
10. Toda tela deve funcionar sem IA.
11. Nenhuma regra de negócio pode depender apenas de aparência.
12. Nenhuma ação persistente pode ser disfarçada de ajuste visual.
13. Fundos coloridos não devem ser usados como decoração de texto comum.
14. Cards não devem ser usados para fragmentar conteúdo sem necessidade.
15. Espaço vazio deve organizar, não desperdiçar área.
16. Densidade não significa aperto; respiro não significa gigantismo.
17. A interface deve permanecer coerente em 100% e 125% de zoom.
18. Overflow não planejado é defeito.
19. Corte silencioso de informação é defeito.
20. Uma tela funcional, mas visualmente inconsistente, não está concluída.

---

## 4. Escala de espaçamento

Usar exclusivamente a escala abaixo, salvo exceção documentada:

| Token | Valor | Uso principal |
|---|---:|---|
| `space-0` | 0 px | remoção explícita de espaço |
| `space-1` | 4 px | ajustes mínimos, ícone e texto |
| `space-2` | 8 px | elementos intimamente relacionados |
| `space-3` | 12 px | gap compacto entre controles |
| `space-4` | 16 px | padding padrão e separação comum |
| `space-5` | 20 px | seções internas mais abertas |
| `space-6` | 24 px | separação entre grupos principais |
| `space-8` | 32 px | separação entre seções de página |
| `space-10` | 40 px | uso excepcional em divisões amplas |
| `space-12` | 48 px | apenas áreas especiais e vazias |

### 4.1 Proibições

- não usar valores arbitrários como 13, 18, 22, 27, 30 ou 38 px;
- não somar margens verticais redundantes entre componentes;
- não aplicar padding vertical grande para “dar importância” a conteúdo comum;
- não criar espaços acima e abaixo de títulos sem relação com a grade;
- não usar margem para corrigir componente estruturalmente errado.

### 4.2 Regra de proximidade

- elementos do mesmo grupo: 4–12 px;
- grupos dentro da mesma seção: 16–24 px;
- seções distintas: 24–32 px;
- mudanças de contexto: 32–40 px, somente quando necessário.

---

## 5. Densidade e dimensões

### 5.1 Alturas padrão

| Elemento | Compacto | Padrão | Máximo comum |
|---|---:|---:|---:|
| Input / select | 32 px | 36 px | 40 px |
| Botão | 30 px | 36 px | 40 px |
| Botão principal destacado | — | 38 px | 42 px |
| Linha de tabela | 36 px | 40 px | 44 px |
| Aba | 32 px | 36 px | 40 px |
| Item de menu | 34 px | 38 px | 42 px |
| Toolbar | 40 px | 44 px | 48 px |
| Cabeçalho de página | 52 px | 60 px | 68 px |
| Badge | 20 px | 24 px | 28 px |

Valores superiores exigem justificativa de acessibilidade ou função específica.

### 5.2 Larguras recomendadas

- sidebar expandida: 216–248 px;
- sidebar compacta: 56–72 px;
- painel lateral: 320–440 px;
- modal pequeno: 400–520 px;
- modal médio: 560–720 px;
- modal grande: 800–1040 px, respeitando viewport;
- conteúdo principal: ocupa área disponível, com largura máxima somente quando a leitura exigir;
- formulários longos: preferir colunas e agrupamentos, não campos gigantes de largura total.

### 5.3 Regra contra gigantismo

Um elemento não deve crescer apenas porque existe espaço disponível.

- inputs curtos devem ter largura compatível com o conteúdo;
- botões devem ter largura pelo texto, salvo ações em layout móvel;
- cards de métrica devem ser compactos;
- títulos não devem consumir altura desproporcional;
- seções não devem receber min-height decorativo;
- áreas vazias não devem virar blocos altos sem função.

---

## 6. Tipografia

### 6.1 Escala oficial

| Papel | Tamanho | Peso sugerido | Uso |
|---|---:|---:|---|
| `display` | 28–32 px | 600–700 | uso excepcional |
| `page-title` | 20–24 px | 600–700 | título da tela |
| `section-title` | 16–18 px | 600 | seção principal |
| `component-title` | 14–16 px | 600 | card, painel, tabela |
| `body` | 13–15 px | 400–500 | texto comum |
| `label` | 12–14 px | 500–600 | rótulo de campo |
| `small` | 11–13 px | 400–500 | apoio e metadado |
| `micro` | 10–11 px | 500–600 | uso restrito |

### 6.2 Regras

- uma tela comum não deve usar mais de quatro níveis tipográficos simultâneos;
- texto de corpo abaixo de 13 px exige justificativa;
- título de card não deve competir com título da página;
- peso 700 deve ser reservado para destaques reais;
- maiúsculas completas devem ser raras e usadas apenas em micro-rótulos;
- não usar cor de fundo para dar hierarquia a texto comum;
- não reduzir fonte para encaixar conteúdo que deveria quebrar, truncar ou reorganizar.

### 6.3 Comprimento de linha

- textos de leitura contínua: aproximadamente 55–80 caracteres por linha;
- descrições curtas em cards: até 2–3 linhas;
- conteúdo operacional deve priorizar leitura escaneável;
- blocos longos devem ser divididos por subtítulos, listas ou revelação progressiva.

---

## 7. Grade e alinhamento

### 7.1 Grade base

Toda página deve alinhar seus principais limites a uma grade de 4 px, usando os tokens de espaçamento.

### 7.2 Alinhamentos obrigatórios

- títulos de seções alinhados aos conteúdos abaixo;
- cabeçalhos de cards alinhados entre cards da mesma linha;
- botões de mesma função com altura idêntica;
- labels e campos consistentes dentro do mesmo formulário;
- números em tabelas alinhados à direita;
- textos e nomes alinhados à esquerda;
- ações de linha posicionadas em coluna previsível;
- ícones centralizados em caixas de tamanho padronizado;
- bordas e divisores alinhados ao conteúdo, não ao acaso.

### 7.3 Proibições

- centralização de texto operacional sem motivo;
- alinhamentos diferentes entre componentes equivalentes;
- cards com alturas arbitrárias em uma mesma linha;
- ícones de tamanhos diferentes para ações equivalentes;
- botões deslocados por margens individuais;
- uso de `position: absolute` para montar estrutura básica.

---

## 8. Estrutura de página

Toda página comum deve ser composta, quando aplicável, por:

1. navegação global;
2. cabeçalho da página;
3. contexto ou breadcrumb discreto;
4. ação primária clara;
5. ações secundárias agrupadas;
6. filtros ou toolbar;
7. conteúdo principal;
8. feedback e estados;
9. ações persistentes ou paginação.

### 8.1 Cabeçalho de página

Deve conter apenas o necessário:

- título;
- descrição curta opcional;
- contexto relevante;
- ação primária;
- ações secundárias em menu quando numerosas.

Não deve conter:

- múltiplos cards decorativos;
- textos longos;
- alertas permanentes comuns;
- badges sem função;
- margens verticais excessivas.

### 8.2 Conteúdo principal

- priorizar uma coluna principal clara;
- usar duas colunas quando houver relação real entre conteúdo primário e secundário;
- evitar mosaicos de cards sem ordem de leitura;
- preservar alinhamento entre seções;
- não fazer cada módulo adotar estrutura diferente.

---

## 9. Componentes obrigatórios

A interface deverá possuir catálogo compartilhado, no mínimo, para:

- `Button`;
- `IconButton`;
- `Input`;
- `SearchInput`;
- `Select`;
- `Textarea`;
- `Checkbox`;
- `Radio`;
- `Switch`;
- `FieldGroup`;
- `FormSection`;
- `Card`;
- `MetricCard`;
- `DataTable`;
- `DataList`;
- `StatusBadge`;
- `Alert`;
- `Toast`;
- `Tooltip`;
- `Popover`;
- `Modal`;
- `Drawer`;
- `Tabs`;
- `PageHeader`;
- `Toolbar`;
- `Pagination`;
- `EmptyState`;
- `ErrorState`;
- `LoadingState`;
- `Skeleton`;
- `ConfirmAction`;
- `InterventionPanel`;
- `GuidedHighlight`.

### 9.1 Regra de reutilização

Antes de criar um novo componente, o agente deve responder:

1. Existe componente equivalente?
2. Uma variante documentada resolve?
3. A diferença é de conteúdo ou de estrutura?
4. A criação reduzirá ou aumentará fragmentação?
5. O componente será usado novamente?

---

## 10. Botões e ações

### 10.1 Hierarquia

- uma ação primária por contexto visual;
- ações secundárias com menor ênfase;
- ações terciárias em estilo discreto;
- ações destrutivas visualmente distinguíveis, sem dominar a tela;
- excesso de ações deve ir para menu contextual.

### 10.2 Regras

- texto curto e orientado a verbo;
- ícone não substitui texto em ação ambígua;
- botão não deve quebrar em duas linhas;
- largura não deve crescer excessivamente;
- ícone e texto com gap de 8 px;
- loading não deve alterar bruscamente a largura;
- ação desabilitada deve explicar motivo quando relevante;
- ação sensível deve obedecer confirmação e reautenticação normativas.

### 10.3 Proibições

- múltiplos botões primários lado a lado;
- botões coloridos para ações comuns sem hierarquia;
- botões gigantes em desktop;
- texto de parágrafo dentro de botão;
- ícone isolado sem tooltip quando o significado não for universal.

---

## 11. Formulários

### 11.1 Organização

- agrupar campos por significado, não por conveniência visual;
- preferir formulários em 1–3 colunas conforme conteúdo;
- campos longos ocupam mais largura; campos curtos não;
- labels sempre vinculados aos controles;
- ajuda deve aparecer somente quando necessária;
- erros devem ficar próximos do campo;
- ações de formulário devem permanecer previsíveis.

### 11.2 Espaçamento

- label para campo: 4–8 px;
- campo para mensagem de ajuda/erro: 4–8 px;
- entre campos do mesmo grupo: 12–16 px;
- entre grupos: 20–24 px;
- entre seções: 24–32 px.

### 11.3 Validação

- não depender apenas de cor;
- preservar layout quando mensagens surgirem;
- evitar saltos grandes da página;
- mostrar erro específico e acionável;
- não apagar entrada após falha;
- não usar placeholders como substituto de label.

---

## 12. Tabelas e listas operacionais

### 12.1 Uso

Tabelas são preferidas quando o usuário precisa:

- comparar registros;
- ordenar;
- filtrar;
- observar padrões;
- executar ações repetitivas;
- ler valores alinhados.

Cards não devem substituir tabelas apenas por estética.

### 12.2 Regras

- cabeçalho visível e compacto;
- linha de 36–44 px por padrão;
- colunas numéricas à direita;
- datas e códigos sem quebra;
- ações alinhadas em coluna fixa;
- truncamento somente com acesso ao conteúdo completo;
- seleção visual inequívoca;
- estados de hover e foco;
- paginação ou virtualização quando necessário;
- comportamento documentado em viewport estreito.

### 12.3 Responsividade

A estratégia deverá ser escolhida explicitamente:

- priorização e ocultação de colunas;
- rolagem horizontal autorizada;
- visualização de detalhes;
- transformação controlada em lista;
- largura mínima por coluna.

Rolagem horizontal em tabela pode ser válida; overflow acidental na página inteira não.

---

## 13. Cards

### 13.1 Quando usar

- agrupamento autônomo de conteúdo;
- resumo de métrica;
- painel secundário;
- entidade com ações próprias;
- divisão clara de contexto.

### 13.2 Quando não usar

- cada parágrafo;
- cada rótulo;
- cada campo de formulário;
- cada linha de lista;
- simples separação que um divisor resolveria;
- tentativa de deixar a tela “moderna”.

### 13.3 Dimensões

- padding padrão: 16 px;
- padding amplo: 20 px, somente quando necessário;
- gap entre cards: 12–16 px;
- raio: 8–12 px;
- cabeçalho compacto;
- altura determinada pelo conteúdo, sem min-height decorativo.

---

## 14. Cor, fundos e elevação

### 14.1 Funções permitidas para cor de fundo

- status;
- alerta;
- seleção;
- feedback;
- criticidade;
- agrupamento estrutural legítimo;
- área interativa;
- mudança temporária de contexto;
- intervenção da Interface Viva.

### 14.2 Funções não permitidas

- decorar subtítulos;
- envolver textos comuns;
- criar “pílulas” sem semântica;
- compensar falta de espaçamento;
- diferenciar cada bloco arbitrariamente;
- usar muitas cores para sugerir variedade.

### 14.3 Elevação

- borda e contraste devem ser preferidos a sombras intensas;
- sombras reservadas para sobreposição real: modal, popover, menu, drawer;
- cards comuns devem ter elevação discreta ou nenhuma;
- não empilhar sombras e bordas pesadas.

---

## 15. Ícones

- usar uma única família principal;
- tamanhos preferidos: 14, 16, 18, 20 e 24 px;
- caixa de ícone padronizada;
- alinhamento óptico revisado;
- ícones não devem substituir rótulos ambíguos;
- evitar mistura de estilos preenchido, outline e duotone sem regra;
- ícones decorativos devem ser raros;
- ações críticas não devem depender apenas de ícone.

---

## 16. Status, badges e etiquetas

### 16.1 Status

Status deve comunicar condição real e possuir semântica consistente no sistema inteiro.

- mesmo estado, mesmo rótulo e aparência;
- não usar `Pedido.status` legado quando a projeção oficial for Processo/Etapa;
- estados comercial, operacional, financeiro e de entrega permanecem distinguíveis;
- não comprimir múltiplas dimensões em um único badge ambíguo.

### 16.2 Badges

- altura de 20–24 px;
- padding horizontal compacto;
- texto de 11–12 px;
- largura pelo conteúdo, com limite;
- sem múltiplos badges redundantes;
- sem cor decorativa não semântica.

---

## 17. Contenção e comportamento de texto

Todo componente deve definir uma das estratégias:

- quebra livre;
- quebra limitada a N linhas;
- truncamento com reticências;
- tooltip ou expansão;
- scroll interno;
- crescimento do container;
- largura fixa;
- conteúdo sem quebra.

### 17.1 Regras por conteúdo

| Conteúdo | Comportamento padrão |
|---|---|
| código de pedido | sem quebra |
| valor monetário | sem quebra, alinhado à direita |
| status | sem quebra dentro do badge |
| nome de cliente | 1 linha com truncamento e tooltip quando necessário |
| título de card | 1–2 linhas |
| descrição | 2–3 linhas ou expansão |
| observação | quebra livre controlada |
| mensagem de erro | quebra livre, sem corte |
| botão | sem quebra |
| breadcrumb | truncamento intermediário preservando item atual |

### 17.2 Proibições

- `overflow: hidden` sem estratégia de acesso ao conteúdo;
- altura fixa em texto variável;
- redução automática excessiva de fonte;
- corte de mensagem de erro;
- botão que cresce verticalmente por quebra de texto;
- palavra longa quebrando toda a página.

---

## 18. Modais, drawers e sobreposições

- devem caber no viewport com margem mínima de 24 px;
- conteúdo longo deve rolar internamente;
- cabeçalho e ações devem permanecer acessíveis;
- foco deve ser gerenciado;
- tecla Esc e fechamento devem respeitar criticidade;
- não usar modal para fluxo longo que merece página;
- não empilhar modais comuns;
- ações destrutivas devem mostrar objeto e impacto;
- tamanho deve corresponder à complexidade, não à importância percebida.

---

## 19. Estados obrigatórios

Todo componente assíncrono ou de dados deve prever:

- padrão;
- hover;
- foco;
- ativo;
- selecionado;
- desabilitado;
- carregando;
- vazio;
- erro;
- sucesso;
- offline quando aplicável;
- sem permissão;
- conteúdo parcial;
- IA indisponível quando aplicável.

Nenhum estado deve provocar salto geométrico desnecessário.

---

## 20. Interface Viva

A Interface Viva deve usar os mesmos componentes e tokens da interface normal.

### 20.1 Estados adicionais

Componentes relevantes devem poder receber:

- `suggested`;
- `guided`;
- `attention`;
- `warning`;
- `critical`;
- `resolved`.

### 20.2 Regras

- a IA não cria estilos arbitrários;
- destaque não altera permissão;
- adaptação temporária deve ser reversível;
- alteração persistente exige fluxo próprio;
- animações devem ser moderadas;
- informação não pode depender só de cor ou brilho;
- criticidade deve ser proporcional;
- interface normal permanece acessível conforme as RFCs.

---

## 21. Navegação

- localização atual sempre perceptível;
- sidebar estável;
- item ativo consistente;
- ícone e rótulo alinhados;
- grupos de menu claros;
- quantidade de níveis reduzida;
- ações globais separadas das ações do módulo;
- não esconder função essencial apenas no chat;
- breadcrumbs usados quando a profundidade justificar;
- retorno previsível ao contexto anterior.

---

## 22. Responsividade e resoluções suportadas

A interface desktop deverá ser validada em:

- 1366 × 768;
- 1440 × 900;
- 1536 × 864;
- 1920 × 1080.

Também deve ser testada em:

- zoom 100%;
- zoom 125%;
- sidebar expandida;
- sidebar compacta, quando existir;
- conteúdo mínimo;
- conteúdo extremo.

### 22.1 Regra de viewport mínimo

A interface deve permanecer operacional em 1366 × 768 sem:

- corte de ações essenciais;
- modal inacessível;
- página inteira com overflow horizontal acidental;
- cabeçalho ocupando área excessiva;
- botões ou filtros fora da tela sem mecanismo de acesso.

---

## 23. Acessibilidade mínima

- navegação por teclado nos fluxos principais;
- foco visível;
- contraste suficiente;
- label associado ao campo;
- feedback não dependente apenas de cor;
- áreas clicáveis adequadas;
- tooltip acessível;
- sem animações excessivas;
- suporte a redução de movimento;
- ordem de tabulação coerente;
- mensagens de erro identificáveis;
- conteúdo ampliável a 125% sem perda funcional.

---

## 24. CSS e implementação

### 24.1 Obrigatório

- tokens em fonte central;
- componentes reutilizáveis;
- classes semânticas;
- organização por camada;
- documentação de variantes;
- remoção de estilos mortos;
- testes de regressão visual;
- compatibilidade com a stack real.

### 24.2 Proibido

- estilos inline, salvo valor dinâmico estritamente necessário;
- cores hexadecimais espalhadas;
- valores mágicos repetidos;
- `!important` como solução comum;
- seletores excessivamente específicos;
- CSS copiado entre templates;
- regras de negócio em CSS ou JavaScript;
- dependência visual exclusiva de uma tela;
- `position: absolute` para layout estrutural;
- esconder overflow para aprovar gate.

---

## 25. Processo de criação de nova tela

1. identificar objetivo e fluxo;
2. mapear dados e permissões;
3. escolher padrão de página existente;
4. definir hierarquia de ações;
5. selecionar componentes do catálogo;
6. definir comportamento de texto;
7. aplicar tokens;
8. implementar estados obrigatórios;
9. testar conteúdo extremo;
10. executar Visual Quality Gate;
11. capturar screenshots;
12. revisar com baseline;
13. corrigir;
14. documentar variante nova, se houver;
15. somente então concluir.

---

## 26. Processo de refatoração do programa inteiro

A migração deve ocorrer por famílias de componentes e telas, não por alterações isoladas sem plano.

Ordem recomendada:

1. tokens;
2. tipografia;
3. botões e inputs;
4. navegação e shell;
5. cabeçalhos e toolbars;
6. cards e métricas;
7. tabelas e listas;
8. formulários;
9. modais e drawers;
10. feedback e estados;
11. Interface Viva;
12. telas-piloto;
13. migração por módulo;
14. remoção de CSS legado;
15. auditoria final transversal.

---

## 27. Critérios de conformidade

Uma interface está em conformidade somente quando:

- [ ] usa tokens oficiais;
- [ ] usa componentes compartilhados;
- [ ] respeita a densidade operacional;
- [ ] possui hierarquia clara;
- [ ] não contém fundo decorativo desnecessário;
- [ ] não possui overflow não planejado;
- [ ] textos longos estão tratados;
- [ ] funciona em viewports oficiais;
- [ ] funciona em 125% de zoom;
- [ ] possui estados obrigatórios;
- [ ] mantém regras fora da interface;
- [ ] continua funcional sem IA;
- [ ] passou no Visual Quality Gate;
- [ ] possui screenshots de evidência.

---

## 28. Resultado normativo

Este padrão deve ser aplicado ao programa inteiro.

Nenhum módulo poderá alegar identidade operacional própria para abandonar a escala, a grade, os componentes ou as regras de contenção. Diferenças entre módulos devem surgir do conteúdo, das permissões e do fluxo, não de uma reconstrução visual independente.
