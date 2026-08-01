# ENG-0007 — Migration Strategy

**Status:** COMPLETED_WITH_GAPS  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Responsabilidade exclusiva:** governar a migração incremental de dados e comportamento do Gestor atual para a arquitetura oficial.  
**Dependências:** Diagnóstico, RFCs, ENG-0006.

---

## 1. Objetivo

Preservar continuidade, dados, identidade e história enquanto responsabilidades hoje concentradas em Pedido, Views e aplicativos separados migram para domínio, casos de uso, Processos, Eventos e contratos oficiais.

Migração não é reescrita. É uma sequência observável de estados compatíveis, com critério de remoção.

## 2. Princípios

- legado é referência do presente, não norma futura;
- dados oficiais não são descartados;
- IDs existentes são preservados ou mapeados;
- pagamentos e autoria nunca são recalculados silenciosamente;
- estado antigo permanece interpretável;
- caminho novo recebe tráfego gradualmente;
- rollback é planejado antes do corte;
- compatibilidade tem proprietário e fim;
- nenhum backfill depende de IA.

## 3. Inventário de origem

Para cada capacidade, registrar:

- models/tabelas/campos;
- constraints e índices;
- migrations;
- caminhos de escrita;
- cálculos e sinais;
- Views, Forms e Services com regras;
- APIs e Electron;
- dados importados/identificadores legados;
- testes;
- volumes, nulos, duplicatas e valores inválidos;
- arquivos físicos/referências;
- integrações.

## 4. Mapa conceitual inicial

| Legado | Destino normativo | Tratamento |
|---|---|---|
| Pedido sobrecarregado | Pedido + Processo(s) + estados independentes | decomposição progressiva |
| status único | estados comercial/operacional/financeiro/entrega/Etapa | tradução versionada |
| histórico de status | eventos/auditoria/evidências quando legítimo | preservar origem e limitações |
| Vendas/Produção separadas | visões da aplicação integrada | convergir contratos |
| regras em Views/Forms | domínio/casos de uso | strangler por operação |
| pagamentos agregados | registros de Pagamento e saldo derivado | reconciliar sem destruir |
| artes binárias/caminhos | Referências de Arquivo contextuais | preservar vínculo e físico |
| importador legado | origem/mapeamento persistente | manter rastreabilidade |
| conversas de aprendizado | conhecimento pendente com proveniência | não promover automaticamente |

O mapa é orientação; cada migração exige análise dos campos reais.

## 5. Estratégia Strangler

Para cada operação:

1. caracterizar o caminho legado;
2. criar contrato de aplicação;
3. delegar caminho antigo ao contrato;
4. introduzir modelo novo;
5. dual-read somente se fonte oficial estiver definida;
6. evitar dual-write sem reconciliação;
7. migrar consumidores;
8. observar;
9. remover caminho antigo.

Dual-write é temporário, idempotente, monitorado e possui compensação. Nunca manter duas verdades sem autoridade definida.

## 6. Migração de dados

### Preparação

- backup verificável;
- migration reversível quando possível;
- tabela/mapeamento de IDs;
- dry-run;
- consultas de baseline;
- janela e responsáveis.

### Backfill

- executar em lotes;
- usar chave de idempotência;
- preservar timestamps/origem;
- registrar rejeições;
- não adivinhar valores ausentes;
- marcar `DECISAO_HUMANA_NECESSARIA` quando tradução for ambígua.

### Verificação

- contagens por entidade/estado;
- somas financeiras;
- amostras e extremos;
- referências órfãs;
- duplicatas;
- invariantes;
- reconciliação com legado;
- teste de restauração.

## 7. Pedido e Processo

Não converter cada status diretamente em Processo/Etapa sem confirmar semântica e evidência. Um Pedido pode originar múltiplos Processos; um Processo pode existir independentemente.

Estratégia:

- manter Pedido como registro comercial;
- criar Processo somente quando houver objetivo/fluxo identificável;
- preservar status legado como dado de origem durante transição;
- derivar mapeamento explícito por versão;
- não reescrever histórico como se eventos novos tivessem ocorrido;
- identificar registros que exigem classificação humana.

## 8. Financeiro

Antes de corte:

- reconciliar total, pagamentos, estornos e saldo;
- distinguir valor importado de pagamento confirmado;
- preservar lançamento financeiro vinculado;
- impedir duplicação ao reprocessar;
- testar cancelamento e entrega com saldo;
- manter autoria e datas originais.

Diferença financeira não é corrigida por arredondamento silencioso.

## 9. Eventos e auditoria retroativa

Eventos futuros começam no novo pipeline. Histórico legado pode ser representado como evento importado somente quando origem e grau de confiança forem explícitos.

Não fabricar autoria, momento ou evidência. Quando houver apenas status final, registrar snapshot/importação, não uma sequência fictícia.

## 10. Arquivos

Preservar caminho, nome, entidade, origem e disponibilidade. Validar existência sem apagar referência ausente. Não mover ou excluir arquivo físico como efeito colateral de migração de vínculo, salvo plano específico.

## 11. Compatibilidade temporária

Cada ponte registra:

- ID;
- motivo;
- dono;
- fonte oficial durante coexistência;
- leitores/escritores;
- métrica de divergência;
- prazo ou condição;
- rollback;
- remoção;
- testes.

Compatibilidade sem condição de retirada reprova o Gate 04.

## 12. Cutover

Critérios:

- backfill completo ou gaps aceitos;
- reconciliação aprovada;
- testes e migrations aprovados;
- observabilidade;
- suporte preparado;
- rollback testado;
- nenhuma escrita não mapeada;
- decisão humana para exceções.

Após corte, monitorar erros, filas, divergências, permissões e indicadores financeiros. Rollback não pode descartar operações novas.

## 13. Desativação

Antes de remover modelo/campo/caminho:

- confirmar nenhum leitor/escritor;
- preservar exportação/histórico;
- remover flags e compatibilidade;
- atualizar testes/documentação;
- migration separada de destruição;
- obter autorização quando houver dado histórico.

## 14. Ondas recomendadas

1. caracterização e contratos;
2. identidade/autorização;
3. eventos/auditoria;
4. comercial/financeiro;
5. Processo/Etapa piloto;
6. projeções e interfaces;
7. integrações/arquivos;
8. offline;
9. missões/conhecimento;
10. cognição avançada após fontes oficiais.

## 15. Runbook mínimo

Para cada onda:

- escopo e responsáveis;
- pré-condições;
- backup;
- comandos;
- duração estimada;
- checks antes/depois;
- critérios de abortar;
- rollback;
- comunicação;
- relatório.

## 16. Lacunas

- mapeamentos físicos exigem inspeção de schema e dados reais por onda;
- políticas de retenção/anonimização estão adiadas;
- RFC-0012 reservada e ainda não elaborada afeta migração de pendências;
- RFC-0015/0016 ausentes bloqueiam migrações desses temas;
- drafts exigem adoção antes de decisões irreversíveis.

## 17. Relatório de validação

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
| Código | APROVADO — estratégia incremental |
| Testes | APROVADO — reconciliação/rollback obrigatórios |
| Documentação | APROVADO |
| Revisão Final | APROVADO COM LACUNAS |

**Resultado:** `COMPLETED_WITH_GAPS`.
