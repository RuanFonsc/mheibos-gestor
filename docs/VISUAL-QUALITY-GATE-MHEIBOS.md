# VISUAL QUALITY GATE DO MHEIBOS

**Projeto:** Mheibos Intelligent Operating System  
**Status:** Normativo  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Objetivo:** Definir critérios verificáveis para aprovar ou reprovar qualquer alteração visual no Mheibos

---

## 1. Regra geral

Nenhuma criação, refatoração ou correção de interface pode ser marcada como `COMPLETED` enquanto existir um gate visual obrigatório reprovado.

Testes funcionais, lint, type checking, Django checks e ausência de exceções não substituem os gates deste documento.

Uma interface é considerada aprovada apenas quando:

- funciona;
- respeita a arquitetura;
- respeita o padrão global de interface;
- permanece legível e operacional nos cenários obrigatórios;
- não apresenta regressões geométricas;
- possui evidências reproduzíveis.

---

## 2. Resultados possíveis

### `PASS`

Todos os gates críticos e aplicáveis foram aprovados.

### `PASS_WITH_DOCUMENTED_VARIANCE`

Existe uma variação consciente, justificada, aprovada e documentada que não compromete uso, arquitetura, acessibilidade ou consistência global.

### `FAIL`

Existe pelo menos uma falha visual, estrutural, de contenção, responsividade, acessibilidade ou evidência.

### `BLOCKED`

A validação não pôde ser executada por ausência de ambiente, dados, acesso, baseline, decisão normativa ou ferramenta necessária.

`BLOCKED` nunca equivale a aprovação.

---

## 3. Matriz obrigatória de execução

Toda tela afetada deve ser testada, quando aplicável, em:

| Cenário | Obrigatório |
|---|---|
| 1366 × 768, zoom 100% | sim |
| 1440 × 900, zoom 100% | sim |
| 1536 × 864, zoom 100% | sim |
| 1920 × 1080, zoom 100% | sim |
| 1366 × 768, zoom 125% | sim |
| sidebar expandida | sim |
| sidebar compacta | se existir |
| conteúdo normal | sim |
| conteúdo extremo | sim |
| estado vazio | sim |
| estado de erro | sim |
| estado de carregamento | se assíncrono |
| usuário com permissão reduzida | se aplicável |
| IA desligada | quando houver função cognitiva |
| Central indisponível/offline | quando aplicável |

---

# GATE V01 — Fonte normativa

Verificar:

- [ ] A RFC proprietária da funcionalidade foi identificada.
- [ ] A RFC-0009 foi consultada quando houver intervenção, adaptação ou condução visual.
- [ ] O padrão global de interface foi aplicado.
- [ ] O catálogo de componentes foi consultado.
- [ ] Nenhuma decisão visual estrutural foi inventada sem registro.

**Falha automática:** implementar a tela apenas a partir do template atual ou de uma referência externa.

---

# GATE V02 — Execução em ambiente real

Verificar:

- [ ] A aplicação foi iniciada.
- [ ] A tela foi aberta pelo fluxo real.
- [ ] Autenticação e permissões foram respeitadas.
- [ ] O agente inspecionou o DOM e os estilos computados quando aplicável.
- [ ] A validação não se limitou à leitura estática do código.

**Falha automática:** concluir sem abrir a interface real.

---

# GATE V03 — Design tokens

Verificar:

- [ ] Espaçamentos usam a escala oficial.
- [ ] Tamanhos de fonte usam a escala oficial.
- [ ] Alturas de controles estão nas faixas permitidas.
- [ ] Cores usam tokens aprovados.
- [ ] Raios e elevações usam valores oficiais.
- [ ] Não existem valores mágicos recorrentes.
- [ ] Não existem estilos inline não justificados.

**Falha automática:** novo valor arbitrário para corrigir apenas uma tela sem atualizar o sistema.

---

# GATE V04 — Componentes compartilhados

Verificar:

- [ ] Componentes existentes foram reutilizados.
- [ ] Variantes novas foram documentadas.
- [ ] Não existe duplicação visual entre templates.
- [ ] A tela não criou botão, input, card, badge ou modal próprio sem necessidade.
- [ ] Estados dos componentes permanecem consistentes.

**Falha automática:** duas implementações equivalentes com dimensões ou comportamento diferentes.

---

# GATE V05 — Densidade e proporção

Verificar:

- [ ] Inputs e botões não estão excessivamente altos.
- [ ] Cards não possuem padding ou min-height decorativo.
- [ ] Cabeçalho não ocupa área desproporcional.
- [ ] Espaço vazio possui função clara.
- [ ] A tela usa adequadamente a área disponível.
- [ ] Conteúdo denso permanece legível.
- [ ] Elementos não crescem apenas porque existe espaço.

**Falha automática:** gigantismo visual, margens verticais excessivas ou necessidade de rolagem causada principalmente por espaçamento exagerado.

---

# GATE V06 — Grade e alinhamento

Verificar:

- [ ] Bordas principais estão alinhadas.
- [ ] Cards da mesma linha seguem uma grade coerente.
- [ ] Labels e campos equivalentes alinham-se.
- [ ] Ações equivalentes ocupam posição previsível.
- [ ] Ícones estão centralizados e padronizados.
- [ ] Números e valores estão alinhados corretamente.
- [ ] Não existem deslocamentos causados por margens individuais.

**Tolerância sugerida:** deslocamentos superiores a 2 px entre elementos que deveriam compartilhar eixo exigem correção ou justificativa.

---

# GATE V07 — Hierarquia visual

Verificar:

- [ ] O título da página é inequívoco.
- [ ] A ação primária é identificável.
- [ ] Ações secundárias não competem com a primária.
- [ ] Títulos de seção não competem com o título da página.
- [ ] Metadados possuem menor ênfase.
- [ ] A ordem visual corresponde à ordem operacional.
- [ ] A tela não usa excesso de níveis tipográficos.

**Falha automática:** múltiplos elementos competindo como ação ou título principal.

---

# GATE V08 — Contenção de texto

Executar com conteúdo normal e extremo.

Verificar:

- [ ] Nenhum texto sai de seu container.
- [ ] Nenhum texto importante é cortado silenciosamente.
- [ ] Truncamentos possuem acesso ao conteúdo completo.
- [ ] Botões não quebram em duas linhas.
- [ ] Badges não deformam o layout.
- [ ] Palavras longas não quebram a página.
- [ ] Mensagens de erro permanecem completas.
- [ ] Números e códigos preservam legibilidade.
- [ ] Labels extensos não colidem com controles.

**Falha automática:** `scrollWidth > clientWidth` ou `scrollHeight > clientHeight` em componente não autorizado.

---

# GATE V09 — Overflow e limites do viewport

Verificar automaticamente e manualmente:

- [ ] Não existe overflow horizontal acidental na página.
- [ ] Nenhum componente essencial fica fora do viewport.
- [ ] Modais cabem na área disponível.
- [ ] Drawers preservam acesso às ações.
- [ ] Tabelas usam estratégia responsiva documentada.
- [ ] Tooltips e popovers permanecem visíveis.
- [ ] Menus não são cortados por containers.
- [ ] Elementos fixos não cobrem conteúdo.

**Falha automática:** ocultar overflow para esconder a regressão.

---

# GATE V10 — Responsividade desktop

Verificar em todas as resoluções oficiais:

- [ ] Layout reorganiza-se sem perda funcional.
- [ ] A ação primária continua acessível.
- [ ] Filtros permanecem utilizáveis.
- [ ] Tabela ou lista preserva estratégia definida.
- [ ] Sidebar não comprime conteúdo de forma destrutiva.
- [ ] Cabeçalho não quebra de forma incoerente.
- [ ] Nenhum texto importante desaparece sem alternativa.

**Falha automática:** tela utilizável apenas em 1920 × 1080.

---

# GATE V11 — Zoom e escala

Verificar em 100% e 125%:

- [ ] Não há sobreposição.
- [ ] Não há perda de ações.
- [ ] Não há corte de texto.
- [ ] Foco e navegação continuam visíveis.
- [ ] Modais permanecem operacionais.
- [ ] A grade não colapsa indevidamente.

**Falha automática:** perda de função em 125% de zoom.

---

# GATE V12 — Estados da interface

Verificar, conforme aplicável:

- [ ] padrão;
- [ ] hover;
- [ ] foco;
- [ ] ativo;
- [ ] selecionado;
- [ ] desabilitado;
- [ ] carregando;
- [ ] vazio;
- [ ] erro;
- [ ] sucesso;
- [ ] offline;
- [ ] sem permissão;
- [ ] IA indisponível;
- [ ] intervenção ativa.

**Falha automática:** estado importante sem representação visual ou que provoque salto de layout desnecessário.

---

# GATE V13 — Formulários

Verificar:

- [ ] Labels estão vinculados aos campos.
- [ ] Campos curtos não ocupam largura excessiva.
- [ ] Grupos possuem espaçamento consistente.
- [ ] Erros aparecem próximos ao campo.
- [ ] Entrada não é perdida após falha.
- [ ] Ações de salvar e cancelar são previsíveis.
- [ ] Tabulação segue ordem lógica.
- [ ] Campos obrigatórios são identificáveis sem depender apenas de cor.
- [ ] Mensagens não deslocam a tela de forma abrupta.

---

# GATE V14 — Tabelas e listas

Verificar:

- [ ] Cabeçalho e colunas alinham-se.
- [ ] Linhas mantêm altura permitida.
- [ ] Valores numéricos estão à direita.
- [ ] Ações ocupam coluna estável.
- [ ] Seleção, hover e foco são visíveis.
- [ ] Conteúdo longo possui estratégia.
- [ ] Paginação ou virtualização funciona quando necessária.
- [ ] Estado vazio mantém contexto e próxima ação.
- [ ] A tabela não foi substituída por cards sem justificativa.

---

# GATE V15 — Cor e semântica

Verificar:

- [ ] Cor de fundo possui função semântica ou estrutural.
- [ ] Texto comum não foi transformado em pílula decorativa.
- [ ] Status equivalentes usam a mesma semântica.
- [ ] Contraste é suficiente.
- [ ] Significado não depende apenas de cor.
- [ ] Ações destrutivas não dominam a tela.
- [ ] Não existe excesso de cores competindo por atenção.

**Falha automática:** fundo colorido sem função identificável.

---

# GATE V16 — Ícones

Verificar:

- [ ] Família e estilo são consistentes.
- [ ] Tamanhos seguem catálogo.
- [ ] Ícones ambíguos possuem rótulo ou tooltip.
- [ ] Ações críticas não dependem apenas de ícone.
- [ ] Alinhamento óptico foi revisado.
- [ ] Não existem ícones meramente decorativos em excesso.

---

# GATE V17 — Modais, drawers e menus

Verificar:

- [ ] Cabem no viewport mínimo.
- [ ] Conteúdo longo possui scroll interno.
- [ ] Cabeçalho e ações permanecem acessíveis.
- [ ] Foco é movido e restaurado corretamente.
- [ ] Fechamento respeita criticidade.
- [ ] Não há empilhamento indevido.
- [ ] Menu não é cortado.
- [ ] A dimensão corresponde à complexidade.

---

# GATE V18 — Interface Viva

Quando houver intervenção:

- [ ] A IA não manipula diretamente widgets.
- [ ] O comando visual é estruturado e autorizado.
- [ ] A adaptação temporária é reversível.
- [ ] A intensidade é proporcional à criticidade.
- [ ] A intervenção não altera dados silenciosamente.
- [ ] A informação não depende apenas de animação ou cor.
- [ ] O usuário entende o que mudou e por quê.
- [ ] A interface normal continua disponível conforme as regras.
- [ ] O estado é removido ou atualizado quando deixa de ser relevante.

---

# GATE V19 — Acessibilidade

Verificar:

- [ ] Navegação por teclado nos fluxos principais.
- [ ] Foco visível.
- [ ] Ordem de tabulação coerente.
- [ ] Labels e nomes acessíveis.
- [ ] Contraste adequado.
- [ ] Feedback não depende apenas de cor.
- [ ] Área interativa suficiente.
- [ ] Suporte a redução de movimento.
- [ ] Tooltip e popover acessíveis.
- [ ] Zoom de 125% sem perda funcional.

---

# GATE V20 — Consistência transversal

Comparar a alteração com telas equivalentes em Gestor, Vendas, Produção e demais módulos.

Verificar:

- [ ] Mesma entidade apresenta o mesmo resumo oficial.
- [ ] Mesma ação possui mesmo componente e hierarquia.
- [ ] Mesmo estado possui mesma linguagem visual.
- [ ] Não existem leituras divergentes do domínio.
- [ ] Nenhuma regra foi movida para template.
- [ ] A alteração não criou uma linguagem visual exclusiva de um módulo.

---

# GATE V21 — Regressão visual

Verificar:

- [ ] Baseline anterior foi comparada quando disponível.
- [ ] Mudanças esperadas foram identificadas.
- [ ] Deslocamentos não planejados foram corrigidos.
- [ ] Elementos não desapareceram.
- [ ] Geometria principal permanece coerente.
- [ ] A comparação não ignora diferenças estruturais sob alegação de antialiasing.

Diferença visual intencional deve ser registrada no relatório.

---

# GATE V22 — Evidências

A entrega deve conter:

- [ ] screenshot de página completa em 1366 × 768;
- [ ] screenshot em 1920 × 1080;
- [ ] screenshot em 125% de zoom;
- [ ] screenshot com conteúdo extremo;
- [ ] screenshot de estado vazio;
- [ ] screenshot de erro, quando aplicável;
- [ ] screenshot de modal/drawer aberto, quando aplicável;
- [ ] relatório do detector de overflow;
- [ ] lista de resoluções e estados testados;
- [ ] resultado dos testes funcionais;
- [ ] commit correspondente.

**Falha automática:** relatório textual sem evidência visual.

---

# GATE V23 — Revisão humana da tela-piloto

Aplicável ao estabelecimento ou alteração relevante do design system.

Verificar:

- [ ] Densidade foi aprovada.
- [ ] Proporções foram aprovadas.
- [ ] Sidebar e shell foram aprovados.
- [ ] Escala tipográfica foi aprovada.
- [ ] Inputs, botões e cards foram aprovados.
- [ ] Tabela ou lista foi aprovada.
- [ ] Tratamento de conteúdo longo foi aprovado.
- [ ] A identidade do Mheibos foi preservada.

Sem aprovação da tela-piloto, não migrar o programa inteiro.

---

## 4. Gates críticos

Os gates abaixo nunca podem ser ignorados:

- V01 — Fonte normativa;
- V02 — Execução em ambiente real;
- V03 — Design tokens;
- V05 — Densidade e proporção;
- V06 — Grade e alinhamento;
- V08 — Contenção de texto;
- V09 — Overflow e limites do viewport;
- V10 — Responsividade desktop;
- V11 — Zoom e escala;
- V18 — Interface Viva, quando aplicável;
- V20 — Consistência transversal;
- V22 — Evidências.

Qualquer falha crítica mantém o trabalho em `FAIL` ou `BLOCKED`.

---

## 5. Falhas impeditivas típicas

A presença de qualquer item abaixo reprova a entrega:

- texto saindo do card, campo, botão, tabela ou modal;
- texto importante cortado sem acesso alternativo;
- botão ou input desproporcionalmente grande;
- margens verticais excessivas;
- cards altos sem conteúdo correspondente;
- fundo colorido decorativo em texto comum;
- desalinhamento visível entre elementos equivalentes;
- overflow horizontal da página inteira;
- modal maior que o viewport;
- ação primária fora da área visível;
- tela quebrada em 1366 × 768;
- perda funcional em zoom de 125%;
- interface diferente entre módulos equivalentes;
- status oficial substituído por leitura legada;
- CSS local duplicando componente global;
- ausência de estado vazio ou erro;
- conclusão sem screenshots;
- uso de `overflow: hidden` para ocultar defeito;
- regra de negócio implementada no template;
- dependência obrigatória da IA para função normal.

---

## 6. Relatório obrigatório

Toda execução do gate deve gerar relatório equivalente a:

```text
VISUAL QUALITY GATE REPORT

Ciclo: IMP-XXX
Tela/componente: ...
Commit: ...
Data: ...

Fontes normativas:
- ...

Viewports testados:
- 1366x768 @ 100%
- 1440x900 @ 100%
- 1536x864 @ 100%
- 1920x1080 @ 100%
- 1366x768 @ 125%

Estados testados:
- normal
- conteúdo extremo
- vazio
- erro
- ...

Automação:
- overflow: PASS/FAIL
- tokens: PASS/FAIL
- screenshots: PASS/FAIL
- regressão: PASS/FAIL

Gates:
- V01 PASS
- V02 PASS
- ...

Variâncias aprovadas:
- nenhuma / descrição

Evidências:
- caminho/screenshot-1.png
- caminho/screenshot-2.png

Resultado final: PASS / PASS_WITH_DOCUMENTED_VARIANCE / FAIL / BLOCKED
```

---

## 7. Integração com os Quality Gates gerais

Este documento complementa o `ENG-QUALITY-GATES.md`.

Para tarefas de interface:

- o GATE 08 — UX somente pode ser aprovado depois deste Visual Quality Gate;
- o GATE 10 — Testes deve incluir testes visuais aplicáveis;
- o GATE 11 — Documentação deve incluir screenshots e relatório;
- o GATE 12 — Revisão Final deve confirmar ausência de falhas visuais críticas.

---

## 8. Regra de encerramento

Uma tarefa de interface somente pode ser encerrada como `COMPLETED` quando:

1. todos os gates gerais aplicáveis estiverem aprovados;
2. todos os gates visuais críticos estiverem aprovados;
3. as evidências estiverem anexadas;
4. variações intencionais estiverem documentadas;
5. o commit estiver coerente com as screenshots apresentadas.

A ausência de uma ferramenta de validação não autoriza aprovação manual superficial. Nesse caso, o resultado deve permanecer `BLOCKED` até que a validação equivalente possa ser realizada.
