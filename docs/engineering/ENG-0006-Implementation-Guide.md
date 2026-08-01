# ENG-0006 — Implementation Guide

**Status:** COMPLETED_WITH_GAPS  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Responsabilidade exclusiva:** ordenar a implementação incremental da arquitetura oficial sobre o Mheibos Gestor atual.  
**Dependências:** RFCs, Diagnóstico, ENG-0004 e ENG-0005.

---

## 1. Princípio de sequenciamento

A implementação deve reduzir risco e retrabalho respeitando dependências normativas. Não começar por IA, Interface Viva ou sincronização geral quando Domínio, autorização, eventos e dados oficiais ainda não existem.

Cada fase entrega fatias utilizáveis, testadas e compatíveis. A ordem não autoriza reescrita total.

## 2. Baseline atual

O Gestor atual possui Django 5, templates server-side, PostgreSQL/SQLite configurável e Electron. Funcionalidades relevantes já existem em Clientes, Pedidos, Catálogo, Financeiro, Vendas, Aprendizado e Migração.

Débitos principais:

- Pedido concentra orçamento, venda, produção, financeiro e entrega;
- estados são alterados por múltiplos caminhos;
- regras estão em Views, Services e Forms;
- Vendas duplica Pedidos;
- não há Processo/Etapa formais;
- eventos, evidências e auditoria são incompletos;
- fontes de verdade competem;
- histórico e autorização são parciais.

## 3. Fase 0 — proteção do legado

Antes de modelar:

- inventariar models, migrations e dados;
- mapear caminhos que alteram Pedido/status;
- identificar cálculos financeiros e duplicações;
- registrar baseline de testes e fixtures;
- criar backups/restauração verificáveis no ambiente de migração;
- mapear identificadores legados;
- impedir novas regras em Views/templates.

Saída: mapa de mudança e suíte de caracterização do comportamento legítimo.

## 4. Fase 1 — fundações de aplicação

Introduzir fronteiras sem mudar comportamento:

- casos de uso explícitos para operações críticas;
- serviços de domínio sem dependência visual;
- adaptadores de persistência/integração;
- contratos estáveis;
- padrão transacional;
- origem/ator/contexto em comandos.

Migrar um caminho por vez; manter compatibilidade delegando o caminho antigo ao novo caso de uso.

## 5. Fase 2 — identidade e autorização

Consolidar:

- identidade própria do Mheibos;
- perfil principal e exceções;
- sessões;
- autorização fora da interface;
- ações sensíveis;
- identidades técnicas;
- bloqueios de edição.

Priorizar operações de cancelamento, alteração financeira, entrega com saldo, usuários e exclusões.

## 6. Fase 3 — eventos, evidências e auditoria

Criar infraestrutura mínima para mudanças relevantes:

- evento com identidade e correlação;
- autoria humana/sistema/IA/integração;
- auditoria aditiva;
- evidência referenciada;
- outbox/fila ou mecanismo equivalente conforme decisão técnica;
- idempotência;
- observabilidade separada.

Instrumentar casos de uso migrados antes de ampliar cobertura.

## 7. Fase 4 — modelo comercial estável

Preservar Pedido como centro comercial/financeiro:

- identidade e número visível;
- autoria comercial;
- itens com snapshot histórico;
- pagamentos separados;
- saldo derivado de fonte identificável;
- cancelamento auditável;
- estados comercial, financeiro e entrega independentes.

Não usar esta fase para representar execução operacional por novo status.

## 8. Fase 5 — Processo, Fluxo e Etapa

Introduzir:

- Modelo de Fluxo versionável;
- Processo como instância;
- Fluxo Instanciado preservado;
- Etapas, dependências e critérios de conclusão;
- responsabilidades e histórico;
- estados operacionais próprios;
- evidências de transição.

Vincular Processos a Pedido/Item sem mover responsabilidades financeiras. Migrar primeiro um fluxo piloto de baixo risco e observável.

## 9. Fase 6 — projeções e interface integrada

Projetar estado atual a partir de fontes oficiais. Adaptar telas existentes para consumir casos de uso e projeções.

Convergir Vendas, Produção e Gestor como visões da mesma aplicação/realidade, preservando permissões e contexto. Não manter regras duplicadas por aplicativo.

## 10. Fase 7 — pendências e intervenções determinísticas

Representar obrigações persistentes, responsável principal, destinatários, prazo, criticidade e encerramento.

Implementar primeiro lembretes e escalonamentos determinísticos. Interface Viva pode apresentar intervenções somente após fatos, regras e autorização existirem.

O roteamento definitivo desta fase depende da resolução do elaboração normativa pendente da RFC-0012.

## 11. Fase 8 — offline restrito

Somente após comandos idempotentes, eventos, autorização e identidade estáveis:

- credencial offline protegida;
- cache autorizado;
- fila local;
- origem/estação;
- IDs estáveis;
- sincronização automática e visível;
- conflitos;
- recuperação.

Começar por capacidades expressamente permitidas pela RFC-0008. Não implementar sincronização genérica.

## 12. Fase 9 — arquivos e integrações

Migrar anexos para referências contextuais sem apagar arquivos. Encapsular Windows, CorelDRAW, PDFs, WhatsApp e webhooks.

Assistência a clientes comerciais exige contexto e confirmação. Fornecedores terceirizados permanecem em registro humano explícito.

## 13. Fase 10 — Missões e Teamwork

Implementar Missão persistente sobre identidades, autorização, eventos e referências existentes. Tarefas de missão podem referenciar Processos/Etapas; não duplicá-los.

Colaboração depende de aceite ou autoridade formal.

## 14. Fase 11 — conhecimento e cognição

Somente com fontes oficiais:

- camadas de conhecimento;
- proveniência e validação;
- memória curta/longa;
- recuperação controlada;
- Gateway de IA;
- sugestões estruturadas;
- explicabilidade;
- planos e acompanhamento.

IA não corrige lacuna de modelagem.

Analytics/simulação e governança avançada permanecem bloqueados onde dependam das RFC-0015/0016 ausentes.

## 15. Critério de passagem entre fases

Uma fase avança quando:

- fatia possui domínio e contrato;
- migration é segura;
- autorização está testada;
- eventos/auditoria aplicáveis existem;
- testes passam;
- compatibilidade possui remoção;
- observabilidade permite diagnóstico;
- documentação/gates são atualizados.

Fases podem coexistir em capacidades diferentes, mas uma capacidade não pula suas dependências.

## 16. Estratégia de rollout

Para cada fatia:

1. caracterizar comportamento atual;
2. criar novo caminho atrás de contrato/flag quando necessário;
3. migrar dados;
4. executar em paralelo somente com fonte oficial definida;
5. comparar resultados;
6. tornar novo caminho principal;
7. remover compatibilidade após evidência e decisão;
8. preservar rollback.

## 17. Matriz de risco

Prioridade máxima:

- perda/corrupção de pedidos e pagamentos;
- autorização indevida;
- entrega com saldo;
- duplicação offline;
- histórico apagado;
- regra duplicada em Vendas/Produção;
- IA com efeito persistente sem validação.

## 18. Lacunas

- fases de analytics/governança cognitiva avançada dependem das RFC-0015/0016;
- pendências dependem da resolução da RFC-0012;
- detalhes físicos adiados pelas RFCs exigirão ADRs, sem alterar invariantes;
- baseline real de testes deve ser executado em cada fatia, não inferido deste documento.

## 19. Relatório de validação

| Gate | Resultado |
|---|---|
| Fonte Normativa | APROVADO COM LACUNAS |
| Arquitetura | APROVADO |
| Domínio | APROVADO |
| Dados | APROVADO |
| Eventos/Auditoria | APROVADO |
| Segurança | APROVADO |
| IA | APROVADO |
| UX | APROVADO |
| Código | APROVADO — ordem incremental |
| Testes | APROVADO — passagem exige testes por fatia |
| Documentação | APROVADO |
| Revisão Final | APROVADO COM LACUNAS |

**Resultado:** `COMPLETED_WITH_GAPS`.
