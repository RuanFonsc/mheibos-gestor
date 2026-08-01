# ENG-0000 — Programa de Engenharia e Governança do Mheibos

**Status:** COMPLETED_WITH_GAPS  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Responsabilidade exclusiva:** estabelecer a autoridade, o ciclo, os estados, os controles e a rastreabilidade da Engenharia Oficial do Mheibos.  
**Não é responsabilidade deste documento:** criar arquitetura de produto, detalhar práticas de implementação, substituir RFCs ou definir regras de negócio.

---

## 1. Finalidade

Este documento institui a série ENG como o sistema oficial de transformação da arquitetura normativa do Mheibos em práticas verificáveis de engenharia.

As RFCs definem o produto que deve existir. O Inventário distribui decisões entre RFCs proprietárias. O Diagnóstico descreve a implementação atual. A série ENG governa como interpretar, planejar, implementar, migrar, testar, revisar e documentar a transição entre o estado atual e a arquitetura oficial.

Nenhum ENG possui autoridade para alterar Manifesto, Princípios, RFCs ou Inventário. Quando a base normativa for insuficiente ou conflitante, a Engenharia registra a lacuna e interrompe somente o trabalho afetado.

## 2. Fundamento filosófico

O programa preserva as finalidades permanentes do Mheibos:

- atuar como memória operacional da empresa;
- preservar a atenção humana;
- acompanhar processos e pendências sem substituir pessoas;
- tratar o próprio sistema, e não o modelo de IA, como fonte da verdade;
- manter decisões críticas sob supervisão humana;
- justificar intervenções por estados, eventos e evidências;
- usar tecnologia como instrumento, sem obsessão tecnológica;
- permitir evolução sem comprometer regras críticas.

Esses fundamentos derivam diretamente da RFC-0000 e da RFC-0001 e são critérios de interpretação de toda a série.

## 3. Autoridade documental

Toda decisão de engenharia deve aplicar a seguinte precedência:

1. RFC-0000 — Manifesto do Projeto;
2. RFC-0001 — Princípios Fundamentais;
3. RFCs normativas aplicáveis;
4. Inventário Oficial de Decisões Arquiteturais;
5. regras e contexto oficiais do projeto;
6. documentos ENG anteriores e aprovados;
7. ADRs técnicos aprovados;
8. diagnóstico da implementação;
9. relatório funcional;
10. código e testes existentes;
11. comentários, nomes legados e inferências.

Uma fonte inferior não revoga fonte superior. Código demonstra o que existe, não o que deve existir. Diagnóstico não cria arquitetura. ENG não cria regra de produto.

Quando fontes de mesma autoridade divergirem, registrar ambas, o escopo afetado e `DECISAO_HUMANA_NECESSARIA`. Não escolher silenciosamente.

## 4. Separação entre futuro e presente

Todo trabalho deve manter duas visões explícitas:

- **arquitetura normativa:** comportamento, fronteiras e invariantes que devem existir;
- **implementação atual:** capacidades, dados, débitos e restrições que existem hoje.

A diferença deve ser classificada como preservar, adaptar, refatorar, reprojetar, substituir, adicionar, descontinuar, compatibilidade temporária, correção normativa ou decisão pendente.

O Diagnóstico registra que o sistema atual concentra responsabilidades em Pedido, utiliza estados implícitos e mantém regras em Views, Services e Forms. Essa fotografia não autoriza perpetuar tais escolhas. A migração deverá introduzir Processo, Fluxo, Etapa, Evento, Evidência, Auditoria e estados independentes incrementalmente, preservando dados e continuidade.

## 5. Invariantes transversais

Toda engenharia do Mheibos deve preservar:

1. Pedido é o centro comercial e financeiro; Processo é o centro da execução operacional.
2. Um único status não representa estados comerciais, operacionais, financeiros, de entrega e de etapa.
3. Interface coleta intenção e apresenta estado, mas não possui autoridade de negócio.
4. Permissões, transições e validações oficiais são determinísticas.
5. IA interpreta, explica, recomenda e planeja; não autentica, autoriza nem se torna fonte da verdade.
6. Eventos relevantes e auditoria preservam autoria, origem, momento, contexto e mudança.
7. Histórico relevante não é destruído silenciosamente.
8. A Central mantém autoridade global; estado local e cache não a substituem.
9. A aplicação principal é integrada; Clientes Mheibos especializados usam contratos da mesma Central.
10. Cliente comercial, Cliente Mheibos, usuário, estação e fornecedor terceirizado são conceitos distintos.
11. Mensagens de fornecedores terceirizados não são automaticamente correlacionadas a pedidos; o registro é humano e explícito.
12. Compatibilidade temporária exige escopo, responsável, teste, rollback e condição de remoção.

## 6. Organização oficial da série

| Ordem | Documento | Responsabilidade exclusiva | Dependência |
|---:|---|---|---|
| 0000 | Programa de Engenharia e Governança | governar a série | Manifesto, Princípios, RFCs |
| 0001 | Manifesto de Engenharia | filosofia da prática de engenharia | ENG-0000 |
| 0002 | Constituição Operacional dos Agentes | obrigações executáveis dos agentes | ENG-0000/0001 |
| 0003 | Skill Oficial do Codex | workflow reutilizável e descoberta | ENG-0000/0002 |
| 0004 | Development Protocol | processo obrigatório de mudança | ENG-0000/0003 |
| 0005 | Architecture Guide | interpretação e roteamento das RFCs | RFCs/Inventário |
| 0006 | Implementation Guide | ordem de implementação | RFCs/Diagnóstico |
| 0007 | Migration Strategy | transição segura do Gestor atual | Diagnóstico/RFCs |
| 0008 | Architectural Checklist | checklist de conformidade | ENG anteriores |
| 0009 | Code Review Guide | revisão técnica uniforme | ENG-0004/0008 |
| 0010 | Glossário Oficial | vocabulário canônico | todas as RFCs |

Cada responsabilidade possui um único documento proprietário. Outros ENGs podem referenciá-la, sem duplicar sua especificação.

## 7. Ciclo controlado de produção

Para cada ENG, executar sequencialmente:

1. descobrir todas as fontes;
2. confirmar o próximo documento permitido;
3. identificar responsabilidade exclusiva e dependências;
4. extrair decisões normativas;
5. construir sumário;
6. produzir a primeira versão;
7. revisar contra RFCs relacionadas;
8. revisar terminologia;
9. revisar duplicações e fronteiras;
10. executar os doze Quality Gates;
11. corrigir inconsistências;
12. produzir relatório de validação;
13. atualizar `engineering/ENG-PROGRESS.json`;
14. somente então avançar.

Nunca manter dois ENGs em produção simultânea. Uma interrupção deve retomar o primeiro documento não concluído ou bloqueado.

## 8. Estados e transições

Estados operacionais permitidos:

- `PENDING`: ainda não iniciado;
- `IN_PROGRESS`: único documento atualmente em produção;
- `COMPLETED`: todos os gates aprovados e nenhuma lacuna normativa relevante;
- `COMPLETED_WITH_GAPS`: gates críticos aprovados e lacunas explicitamente documentadas;
- `BLOCKED`: gate crítico reprovado ou decisão normativa indispensável ausente.

Conclusão exige validação explícita. Progresso nunca é promovido automaticamente por geração de texto. O histórico deve registrar data, estado anterior, novo estado, documento produzido, pendências, conflitos e nota de validação.

## 9. Quality Gates

Os gates oficiais são cumulativos:

1. Fonte Normativa;
2. Arquitetura;
3. Domínio;
4. Dados;
5. Eventos e Auditoria;
6. Segurança;
7. Inteligência Artificial;
8. UX;
9. Código;
10. Testes;
11. Documentação;
12. Revisão Final.

Fonte Normativa, Arquitetura, Domínio, Eventos/Auditoria, Segurança e Testes são críticos. Para documentos sem código, o Gate 10 valida estrutura, referências, consistência, scripts documentais e cenários aplicáveis; não se declara teste de produto inexistente.

## 10. Política de lacunas e conflitos

Uma lacuna deve registrar:

- identificador;
- documento afetado;
- fontes consultadas;
- descrição precisa;
- alternativas conhecidas, sem seleção;
- impacto;
- decisão humana necessária;
- condição para desbloqueio.

Um conflito deve registrar as duas fontes, níveis de autoridade, trechos ou decisões afetadas e por que não pode ser resolvido por precedência. Nenhum documento pode esconder lacuna para obter estado de conclusão.

## 11. Governança de mudanças

Alterações em ENG seguem revisão deliberada:

- preservar histórico pelo Git;
- atualizar versão, data e rastreabilidade;
- reexecutar gates afetados;
- revisar documentos dependentes;
- não sobrescrever documento concluído sem registrar motivo;
- não alterar fonte normativa para adequá-la à implementação.

Mudança técnica que introduza decisão arquitetural não coberta deve gerar proposta de RFC/ADR para decisão humana, não uma regra silenciosa dentro do ENG.

## 12. Persistência e recuperação

`engineering/ENG-PROGRESS.json` é o estado operacional do loop. Os próprios documentos são os artefatos oficiais; Git preserva versões e autoria técnica.

Após falha ou interrupção:

1. validar o JSON;
2. localizar o único `IN_PROGRESS`;
3. conferir se o arquivo existe e não está vazio;
4. reexecutar gates antes de continuar;
5. retomar sem avançar automaticamente.

## 13. Revisão cruzada da série

Ao finalizar ou bloquear formalmente todos os documentos:

- comparar todos os ENGs com todas as RFCs;
- verificar responsabilidade exclusiva;
- verificar terminologia e referências;
- verificar lacunas e conflitos;
- atualizar índice e mapa de dependências;
- produzir relatório final;
- confirmar que nenhum ENG criou arquitetura ou regra de negócio.

## 14. Lacunas normativas registradas

### GAP-ENG-0000-001 — RFCs previstas e ausentes

O Inventário atribui INV-119 a INV-124 à RFC-0016 e INV-125 a INV-127 à RFC-0015. Não existem arquivos RFC-0015 ou RFC-0016 no conjunto atual.

**Impacto:** analytics/simulação e governança/segurança da IA não podem receber especificação de engenharia definitiva.  
**Decisão:** `DECISAO_HUMANA_NECESSARIA` sobre produção ou retirada formal dessas RFCs do mapa.  
**Alternativas não escolhidas:** produzir as RFCs; revisar explicitamente o Inventário; manter os temas bloqueados.

### GAP-ENG-0000-002 — Status das RFCs

RFC-0002 está aprovada; RFC-0003 a RFC-0011 e RFC-0013 continuam como Draft para aprovação. RFC-0012 está reservada, aguardando elaboração; RFC-0000, RFC-0001 e RFC-0014 possuem estado oficial/aprovado explícito.

**Impacto:** a série pode documentar rastreabilidade e processo, mas não deve declarar encerradas decisões dependentes de aprovação.  
**Decisão:** `DECISAO_HUMANA_NECESSARIA` para adoção/aprovação ou revisão.

### GAP-ENG-0000-003 — Elaboração da RFC-0012

A ambiguidade de numeração foi resolvida: o Modelo Operacional foi consolidado na RFC-0002, e a RFC-0012 foi reservada a Pendências, Lembretes e Escalonamento. Sua elaboração normativa detalhada ainda é necessária antes da implementação desse domínio.

**Impacto:** roteamento documental ambíguo para pendências e modelo operacional.  
**Decisão:** `DECISAO_HUMANA_NECESSARIA`; este ENG não renomeia nem altera RFC.

## 15. Rastreabilidade

Fontes consultadas:

- RFC-0000 e RFC-0001;
- RFC-0002 a RFC-0014 existentes;
- Inventário Oficial de Decisões Arquiteturais;
- Diagnóstico da Arquitetura e dos Fluxos Atuais;
- Relatório Atual de Funcionalidades;
- `AGENTS.md`;
- `ENG-SERIES-PLAN.md`;
- `ENG-QUALITY-GATES.md`;
- regras e contexto oficiais do projeto.

## 16. Relatório de validação

| Gate | Resultado | Evidência |
|---|---|---|
| 01 Fonte Normativa | APROVADO COM LACUNAS | fontes listadas; gaps 001/002 e conflito 001 |
| 02 Arquitetura | APROVADO | não cria arquitetura; consolida invariantes existentes |
| 03 Domínio | APROVADO | preserva fronteiras e responsabilidade documental |
| 04 Dados | NÃO APLICÁVEL AO ARTEFATO | nenhuma migração ou dado de produto alterado |
| 05 Eventos/Auditoria | APROVADO | exige rastreabilidade e histórico de progresso |
| 06 Segurança | APROVADO | preserva autorização determinística e supervisão humana |
| 07 IA | APROVADO | IA não é autoridade nem fonte da verdade |
| 08 UX | APROVADO | programa preserva atenção e carga cognitiva |
| 09 Código | NÃO APLICÁVEL AO ARTEFATO | somente documentação |
| 10 Testes | APROVADO | estrutura, referências, numeração e progresso validáveis por script |
| 11 Documentação | APROVADO | responsabilidade, fontes, gaps e validação registrados |
| 12 Revisão Final | APROVADO COM LACUNAS | nenhuma lacuna foi ocultada |

**Resultado final:** `COMPLETED_WITH_GAPS`.

## 17. Declaração final

A Engenharia Oficial do Mheibos permanece subordinada à arquitetura oficial e à atenção humana. Seu papel é tornar a evolução rastreável, verificável e segura. Nenhum ganho de velocidade justifica inventar regra, apagar histórico, confundir implementação com norma ou transferir decisão crítica para a IA.
