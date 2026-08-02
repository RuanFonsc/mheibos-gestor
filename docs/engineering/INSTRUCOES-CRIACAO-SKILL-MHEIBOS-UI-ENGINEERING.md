# INSTRUÇÕES PARA CRIAÇÃO DA SKILL `mheibos-ui-engineering`

**Projeto:** Mheibos Intelligent Operating System  
**Status:** Documento de implantação da skill  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Escopo:** Codex, agentes de engenharia e automações responsáveis por criar, revisar ou refatorar a interface do Mheibos  
**Autoridade:** Subordinado ao Manifesto, aos Princípios Fundamentais, às RFCs, ao Inventário Oficial, ao `AGENTS.md`, ao padrão global de interface e ao Visual Quality Gate

---

## 1. Finalidade

Este documento instrui a criação de uma skill especializada denominada **`mheibos-ui-engineering`**.

A skill deverá transformar o trabalho de interface do Codex em um processo de engenharia visual repetível, mensurável e verificável. Seu objetivo não é apenas produzir telas consideradas “bonitas”. Seu objetivo é impedir inconsistências geométricas, componentes arbitrários, excesso de tamanho, vazamentos de texto, desalinhamentos, espaçamentos irregulares, fundos decorativos sem função e regressões visuais entre módulos.

A skill deverá ser utilizada sempre que uma tarefa envolver:

- criação de nova tela;
- redesenho de tela existente;
- criação ou alteração de componentes visuais;
- mudança de layout, tipografia, espaçamento, densidade ou responsividade;
- criação de dashboard, formulário, tabela, modal, drawer ou painel lateral;
- implantação da Interface Viva;
- correção de overflow, truncamento, corte, sobreposição ou desalinhamento;
- revisão visual de uma entrega;
- migração de templates para o design system oficial;
- comparação com screenshots, protótipos ou referências visuais.

---

## 2. Resultado esperado

Depois de instalada, a skill deverá obrigar o agente a seguir este fluxo:

```text
Ler fontes normativas
        ↓
Inspecionar a interface real
        ↓
Identificar o fluxo e os estados
        ↓
Mapear componentes existentes
        ↓
Aplicar tokens e padrões oficiais
        ↓
Implementar a menor fatia coerente
        ↓
Executar testes funcionais
        ↓
Executar validação visual automatizada
        ↓
Capturar evidências em screenshots
        ↓
Corrigir até aprovação
        ↓
Registrar resultado e limitações
```

Nenhuma tela deverá ser considerada concluída apenas porque renderiza, passa nos testes de backend ou não apresenta exceções no navegador.

---

## 3. Relação entre Skill, `AGENTS.md` e documentos normativos

A skill não substitui o `AGENTS.md`.

A divisão de responsabilidades deverá ser:

- **`AGENTS.md`:** constituição geral de engenharia do repositório;
- **RFCs:** comportamento e arquitetura obrigatórios do produto;
- **Padrão Global de Interface:** regras visuais e geométricas aplicáveis ao programa inteiro;
- **Visual Quality Gate:** critérios objetivos para aprovar ou reprovar uma implementação visual;
- **Skill `mheibos-ui-engineering`:** método operacional que conduz o agente por essas fontes e executa o trabalho.

Em caso de conflito, a hierarquia definida no `AGENTS.md` permanece soberana.

---

## 4. Estrutura recomendada da skill

Criar uma pasta de skill com estrutura equivalente a:

```text
mheibos-ui-engineering/
├── SKILL.md
├── references/
│   ├── UI-STANDARDS-MHEIBOS.md
│   ├── VISUAL-QUALITY-GATE-MHEIBOS.md
│   ├── RFC-0009-Interface-Viva-e-Intervencoes.md
│   ├── UI-COMPONENT-CATALOG.md
│   ├── UI-SCREEN-INVENTORY.md
│   └── UI-REFERENCE-GALLERY.md
├── scripts/
│   ├── run_visual_audit.py
│   ├── detect_overflow.js
│   ├── capture_screenshots.js
│   ├── compare_screenshots.py
│   └── validate_design_tokens.py
└── assets/
    ├── reference-screens/
    ├── baselines/
    └── test-data/
```

A estrutura poderá ser adaptada às convenções atuais do Codex, desde que preserve:

1. um `SKILL.md` principal;
2. referências normativas separadas;
3. scripts reutilizáveis;
4. baselines visuais versionados;
5. dados de teste adequados para validar conteúdo curto, longo, vazio e extremo.

---

## 5. Conteúdo obrigatório do `SKILL.md`

O arquivo principal deverá conter, no mínimo, as seções abaixo.

### 5.1 Nome e descrição

Usar nome inequívoco:

```yaml
name: mheibos-ui-engineering
description: >
  Use esta skill para criar, redesenhar, revisar ou validar qualquer interface
  do Mheibos. Ela aplica o design system, controla densidade e espaçamento,
  exige componentes reutilizáveis, valida overflow e responsividade,
  executa testes visuais e impede conclusão sem evidências em screenshots.
```

A descrição deverá deixar claro quando a skill deve ser carregada. O Codex utiliza nome e descrição para decidir relevância antes de carregar o conteúdo completo da skill.

### 5.2 Fontes obrigatórias

A skill deverá mandar localizar e consultar, conforme aplicável:

- `AGENTS.md`;
- RFC-0003 — Arquitetura Técnica;
- RFC-0007 — Identidade, Permissões e Segurança;
- RFC-0008 — Operação Offline e Sincronização;
- RFC-0009 — Interface Viva e Intervenções;
- RFC-0010 — Missões e Teamwork;
- RFC-0012 — Modelo Operacional;
- padrão global de interface;
- catálogo de componentes;
- Visual Quality Gate;
- inventário de telas;
- screenshots e baselines aprovados.

### 5.3 Princípios não negociáveis

O `SKILL.md` deverá declarar explicitamente:

1. Interface não contém autoridade de negócio.
2. A interface normal permanece utilizável sem IA.
3. A IA só influencia a interface por comandos estruturados e autorizados.
4. A densidade padrão é operacional e compacta, não promocional.
5. Espaçamentos e dimensões devem usar tokens oficiais.
6. Componentes existentes devem ser reutilizados antes da criação de variantes.
7. Texto deve possuir comportamento explícito de quebra, truncamento ou expansão.
8. Cor de fundo deve ter função semântica ou estrutural justificável.
9. Nenhuma tela pode ser aprovada sem validação em resoluções oficiais.
10. Nenhuma tela pode ser concluída sem screenshots de evidência.
11. O agente deve testar estados extremos, não apenas o caso ideal.
12. A implementação deve continuar funcional com a IA indisponível.

### 5.4 Procedimento obrigatório

O procedimento deverá ser dividido em etapas bloqueantes.

#### Etapa A — Descoberta

- localizar as fontes normativas;
- executar a aplicação real;
- abrir a tela atual no navegador ou ambiente desktop;
- identificar fluxo, perfis, permissões e estados;
- listar componentes já existentes;
- identificar duplicações e CSS local arbitrário;
- registrar problemas observados com evidências.

#### Etapa B — Contrato visual

Antes de codificar, registrar:

- finalidade da tela;
- ações primárias e secundárias;
- hierarquia de informação;
- grade utilizada;
- largura máxima e comportamento de expansão;
- componentes reutilizados;
- estados obrigatórios;
- estratégia para textos longos;
- comportamento em resoluções mínimas;
- elementos que podem receber intervenção da IA;
- alterações persistentes que exigem confirmação.

#### Etapa C — Implementação

- aplicar tokens oficiais;
- usar componentes compartilhados;
- manter regras de negócio fora do template;
- evitar estilos inline;
- evitar valores mágicos;
- evitar duplicação de CSS;
- preservar semântica HTML;
- implementar acessibilidade mínima;
- não introduzir bibliotecas sem necessidade comprovada;
- produzir alteração pequena, coerente e revisável.

#### Etapa D — Validação funcional

- executar testes existentes;
- testar permissões e estados relevantes;
- testar com IA desligada;
- testar estados de carregamento, vazio, erro e sucesso;
- testar conteúdo realista e conteúdo extremo;
- verificar ausência de regressão entre Gestor, Vendas e Produção.

#### Etapa E — Validação visual

- executar o Visual Quality Gate;
- capturar screenshots nas resoluções oficiais;
- executar detector de overflow;
- validar zoom de 100% e 125%;
- verificar modais, drawers, menus e tooltips;
- comparar com baseline quando disponível;
- corrigir até todos os gates críticos passarem.

#### Etapa F — Encerramento

Produzir relatório contendo:

- tela ou componente alterado;
- fontes normativas usadas;
- tokens e componentes aplicados;
- resoluções testadas;
- estados testados;
- screenshots gerados;
- gates aprovados;
- regressões corrigidas;
- limitações restantes;
- commit correspondente.

---

## 6. Regras de comportamento do agente

A skill deverá proibir o agente de:

- interpretar “moderno” como “grande”;
- aumentar padding para mascarar falta de hierarquia;
- criar cards para todo agrupamento de texto;
- aplicar fundo colorido a rótulos comuns;
- usar badges como decoração;
- criar componentes quase idênticos em telas diferentes;
- alterar identidade visual sem autorização;
- copiar literalmente a identidade de uma referência externa;
- substituir tabela por cards sem justificativa operacional;
- esconder dados importantes para obter uma tela visualmente limpa;
- reduzir fonte para corrigir overflow sem revisar o layout;
- usar `overflow: hidden` para esconder defeitos;
- cortar texto sem tooltip ou acesso ao conteúdo completo;
- considerar apenas a resolução do computador do desenvolvedor;
- concluir a tarefa sem abrir a aplicação real;
- concluir a tarefa sem evidências visuais;
- mover regras de negócio para templates, JavaScript ou CSS;
- introduzir nova biblioteca de UI antes de auditar as existentes;
- reconstruir o programa inteiro quando uma correção localizada for suficiente.

---

## 7. Design system como dependência obrigatória

Antes do redesenho integral, a skill deverá exigir a existência de:

- tokens de espaçamento;
- tokens de tipografia;
- tokens de dimensões;
- tokens de raio;
- tokens de cor semântica;
- tokens de elevação;
- tokens de movimento;
- componentes fundamentais;
- estados de componentes;
- regras de conteúdo;
- catálogo de ícones;
- padrões de página;
- padrões de formulário;
- padrões de tabela;
- padrões de intervenção.

Quando algum desses elementos ainda não existir, a skill deverá:

1. impedir que cada tela invente sua própria solução;
2. criar a menor definição global necessária;
3. documentar a decisão;
4. testar a definição em uma tela-piloto;
5. só depois aplicá-la em larga escala.

---

## 8. Tela-piloto obrigatória

Antes de migrar o programa inteiro, selecionar uma tela-piloto representativa.

A tela-piloto ideal deve conter:

- navegação principal;
- cabeçalho de página;
- indicadores ou resumo;
- tabela ou lista;
- formulário ou filtros;
- ações primárias e secundárias;
- status;
- estado vazio;
- estado de erro;
- conteúdo longo;
- pelo menos uma intervenção contextual.

Candidatas recomendadas:

- detalhe do Pedido;
- criação de Pedido;
- dashboard operacional.

A escala visual somente poderá ser congelada depois de a tela-piloto ser aprovada em densidade, proporção, legibilidade, hierarquia e comportamento responsivo.

---

## 9. Integração com Playwright e navegador real

A skill deverá usar navegador real sempre que a interface for baseada em HTML, templates server-side ou aplicação Electron que exponha conteúdo web.

O fluxo deverá incluir:

- inicialização do servidor;
- autenticação com usuário de teste;
- navegação pelo fluxo real;
- preenchimento de dados;
- captura de screenshots;
- inspeção de dimensões computadas;
- detecção de overflow;
- validação em múltiplos viewports;
- repetição após correções.

O agente não deve confiar apenas na leitura estática de HTML e CSS.

---

## 10. Scripts recomendados

### 10.1 `detect_overflow.js`

Deverá detectar, no mínimo:

- elementos com `scrollWidth > clientWidth` não autorizados;
- elementos com `scrollHeight > clientHeight` não autorizados;
- conteúdo saindo do viewport;
- sobreposição entre caixas relevantes;
- botões ou inputs abaixo da altura mínima;
- texto invisível por corte;
- modais maiores que a área disponível;
- tabela sem estratégia de responsividade.

### 10.2 `capture_screenshots.js`

Deverá capturar:

- página completa;
- viewport visível;
- componentes críticos;
- estados abertos de modal, drawer e menu;
- versões nas resoluções oficiais;
- versões com conteúdo normal e extremo.

### 10.3 `validate_design_tokens.py`

Deverá procurar:

- valores de espaçamento fora da escala;
- tamanhos de fonte não autorizados;
- cores hexadecimais fora dos tokens;
- raios arbitrários;
- alturas excessivas;
- estilos inline proibidos;
- duplicações de regras visuais.

### 10.4 `compare_screenshots.py`

Deverá apoiar comparação de baseline sem transformar qualquer diferença de pixel em falha automática.

A comparação deve distinguir:

- diferença esperada de conteúdo;
- diferença causada por antialiasing;
- regressão estrutural;
- mudança não autorizada de geometria;
- desaparecimento de elemento;
- deslocamento relevante;
- overflow ou corte.

---

## 11. Dados visuais de teste

A skill deverá manter fixtures ou factories para:

1. conteúdo curto;
2. conteúdo médio realista;
3. nomes e descrições muito longos;
4. números monetários grandes;
5. campos vazios;
6. muitos registros;
7. poucos registros;
8. texto com palavras sem espaços;
9. mensagens de erro extensas;
10. múltiplos status;
11. permissões reduzidas;
12. tela com IA indisponível;
13. tela offline, quando aplicável;
14. zoom de 125%;
15. viewport mínimo suportado.

---

## 12. Critérios de conclusão da skill

A criação da skill somente estará concluída quando:

- [ ] `SKILL.md` existir e descrever claramente quando deve ser usado;
- [ ] as referências normativas estiverem vinculadas;
- [ ] o padrão global de interface estiver disponível;
- [ ] o Visual Quality Gate estiver disponível;
- [ ] os scripts principais puderem ser executados;
- [ ] existir pelo menos uma tela-piloto validada;
- [ ] existirem screenshots baseline aprovadas;
- [ ] o detector de overflow encontrar falhas propositalmente introduzidas;
- [ ] o validador de tokens reprovar valores arbitrários;
- [ ] o fluxo completo funcionar sem depender de interpretação manual do agente;
- [ ] o `AGENTS.md` indicar quando a skill é obrigatória;
- [ ] a documentação ensinar como atualizar a skill sem quebrar baselines.

---

## 13. Trecho recomendado para adicionar ao `AGENTS.md`

```md
## Skill obrigatória para interface

Toda tarefa que crie, altere, redesenhe ou revise interface deve carregar e seguir
`mheibos-ui-engineering`.

A tarefa não poderá ser marcada como concluída enquanto o Visual Quality Gate
estiver reprovado ou enquanto não existirem screenshots das resoluções e estados
obrigatórios.

Testes funcionais aprovados não substituem validação visual.
```

---

## 14. Prompt recomendado para criação da skill no Codex

```text
Crie e instale no projeto uma skill denominada `mheibos-ui-engineering`.

Antes de escrever a skill, leia integralmente:
- AGENTS.md;
- RFC-0003;
- RFC-0007;
- RFC-0008;
- RFC-0009;
- RFC-0010;
- o padrão global de interface do Mheibos;
- o Visual Quality Gate do Mheibos;
- o diagnóstico da interface atual.

A skill deve ser especializada em engenharia visual de aplicação desktop
operacional baseada na stack real do repositório. Ela não deve introduzir uma
nova arquitetura de frontend sem necessidade normativa.

Implemente:
1. SKILL.md com descrição de ativação clara e procedimento bloqueante;
2. references/ com vínculos para as fontes oficiais;
3. scripts para captura de screenshots, detecção de overflow, validação de
   tokens e comparação de baselines;
4. matriz de viewports e estados obrigatórios;
5. fixtures de conteúdo normal e extremo;
6. relatório de instalação e teste da skill.

A skill deve impedir conclusão de tarefas de UI sem:
- aplicação executada em navegador real;
- testes funcionais aprovados;
- Visual Quality Gate aprovado;
- screenshots de evidência;
- validação de textos longos;
- validação em 1366x768, 1440x900, 1536x864 e 1920x1080;
- zoom de 100% e 125%;
- ausência de overflow não planejado.

Não redesenhe o programa inteiro nesta tarefa. Use uma tela-piloto para provar
que a skill, os scripts e os gates funcionam. Faça commit atômico e publique o
resultado somente depois de todos os gates passarem.
```

---

## 15. Referências externas de implementação

A documentação oficial do Codex descreve skills como pacotes reutilizáveis de instruções, referências e scripts, carregados por relevância. Ela também recomenda o uso de screenshots e navegador real, com Playwright, para implementar e revisar interfaces responsivas.

Referências:

- OpenAI Developers — Build skills: `https://developers.openai.com/codex/build-skills`
- OpenAI Developers — Build responsive front-end designs: `https://developers.openai.com/codex/use-cases/frontend-designs`
- OpenAI Developers — Custom instructions with AGENTS.md: `https://developers.openai.com/codex/agent-configuration/agents-md`

---

## 16. Resultado normativo

A skill `mheibos-ui-engineering` deverá transformar qualidade visual em uma condição verificável de engenharia.

Ela não poderá prometer “perfeição” subjetiva. Deverá garantir disciplina suficiente para que inconsistências de tamanho, espaçamento, alinhamento, contenção e hierarquia sejam detectadas antes de uma implementação ser aceita.
