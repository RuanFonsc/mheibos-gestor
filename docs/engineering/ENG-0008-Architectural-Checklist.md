# ENG-0008 — Architectural Checklist

**Status:** COMPLETED_WITH_GAPS  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Responsabilidade exclusiva:** fornecer checklist obrigatório e repetível de conformidade arquitetural.  
**Dependências:** ENG-0000 a ENG-0007.

---

## 1. Uso

Marcar cada item como `PASS`, `FAIL`, `N/A — justificativa` ou `DECISAO_HUMANA_NECESSARIA`. Qualquer falha crítica impede conclusão.

## 2. Fonte normativa — crítico

- [ ] Manifesto e Princípios consultados.
- [ ] RFC proprietária identificada.
- [ ] RFCs relacionadas consultadas.
- [ ] Inventário considerado.
- [ ] Diagnóstico usado somente para o estado atual.
- [ ] Status/versão das fontes registrados.
- [ ] Nenhuma regra foi inventada.
- [ ] Conflitos e lacunas estão explícitos.

## 3. Responsabilidade e escopo

- [ ] Objetivo e critérios de aceitação definidos.
- [ ] Classificação da mudança registrada.
- [ ] Responsabilidade pertence ao componente/documento correto.
- [ ] Não há duplicação com módulo ou ENG existente.
- [ ] Arquitetura futura e implementação atual estão separadas.
- [ ] Decisões adiadas não foram fechadas silenciosamente.

## 4. Domínio — crítico

- [ ] Pedido e Processo permanecem distintos.
- [ ] Fluxo, Etapa, Estado, Evento e Evidência não foram confundidos.
- [ ] Estados comerciais, operacionais, financeiros e entrega são distinguíveis.
- [ ] Regras estão no domínio/caso de uso.
- [ ] Interface não possui autoridade.
- [ ] Critérios de transição e conclusão são determinísticos.
- [ ] Responsabilidade, autoria e execução são rastreáveis.

## 5. Plataforma

- [ ] Central preserva autoridade global.
- [ ] Cliente não acessa banco central diretamente.
- [ ] Estado local/cache não substitui estado global.
- [ ] Aplicação principal continua integrada.
- [ ] Aplicações especializadas usam contratos da Central.
- [ ] Falha de IA/integração não derruba função essencial.
- [ ] Fronteiras Domínio/Aplicação/Infraestrutura/Interface estão explícitas.

## 6. Dados

- [ ] Identidades técnicas são estáveis e não reutilizadas.
- [ ] Snapshots históricos não são reescritos por cadastro atual.
- [ ] Pagamentos e autoria são preservados.
- [ ] Exclusão relevante é lógica/explicitamente encerrada.
- [ ] Migration e backfill são idempotentes.
- [ ] Contagens, somas e referências foram reconciliadas.
- [ ] Compatibilidade possui fonte oficial e remoção.
- [ ] Rollback/compensação foi definido.

## 7. Eventos e auditoria — crítico

- [ ] Alterações relevantes geram evento.
- [ ] Evento possui autoria, origem, momento, alvo e mudança.
- [ ] Correlação/causalidade é preservada.
- [ ] Auditoria é aditiva e protegida.
- [ ] Ação mediada pela IA distingue sugestão, autorização e execução.
- [ ] Reprocessamento é idempotente.
- [ ] Falha secundária não apaga evento principal.
- [ ] Log técnico não substitui auditoria.

## 8. Segurança — crítico

- [ ] Autorização ocorre antes da persistência.
- [ ] Permissão não depende de botão oculto.
- [ ] Ação, recurso, registro, responsabilidade, contexto e alcance são avaliados.
- [ ] Ações sensíveis têm proteção, motivo e auditoria.
- [ ] IA herda permissões do usuário.
- [ ] Integrações usam identidades técnicas.
- [ ] Offline não amplia privilégio.
- [ ] Segredos/dados sensíveis não são expostos.

## 9. Offline e sincronização

- [ ] Capacidade offline está explicitamente permitida.
- [ ] Modo offline é visível e restrito.
- [ ] Operações pendentes não são descartadas.
- [ ] IDs/origem/estação são estáveis.
- [ ] Reenvio não duplica.
- [ ] Conflitos são detectados e apresentados.
- [ ] Incorporação global depende da Central.
- [ ] Recuperação após falha está testada.

## 10. IA e conhecimento

- [ ] IA não é fonte da verdade.
- [ ] IA não autoriza nem valida regra obrigatória.
- [ ] Gateway controla contexto e recursos.
- [ ] Saída é estruturada e validada.
- [ ] Recomendação é explicável.
- [ ] Hipótese e fato são distinguidos.
- [ ] Conhecimento permanece fora do modelo.
- [ ] Ensinamento não vira oficial sem validação humana.
- [ ] Investigação ampla opcional pede consentimento.

## 11. Interface e UX

- [ ] Fluxo normal funciona sem chat.
- [ ] Interface acompanha operação real.
- [ ] Intervenção usa menor interrupção eficaz.
- [ ] Mudança visual explica motivo e restauração.
- [ ] Informação crítica não depende somente de cor/animação.
- [ ] Adaptação temporária não vira regra persistente.
- [ ] Dignidade e privacidade são preservadas.
- [ ] Carga cognitiva foi reduzida ou justificada.

## 12. Integrações e arquivos

- [ ] Adaptadores isolam dependência externa.
- [ ] Arquivo físico e referência são distintos.
- [ ] Remover vínculo não apaga arquivo.
- [ ] Indisponibilidade física preserva histórico.
- [ ] Cliente comercial e fornecedor terceirizado não são confundidos.
- [ ] Mensagem de fornecedor não é correlacionada automaticamente.
- [ ] Envio assistido ao cliente exige autoridade/confirmação aplicável.

## 13. Missões e colaboração

- [ ] Missão possui objetivo, participantes, plano e conclusão.
- [ ] Tarefa referencia Processo/Etapa sem duplicar.
- [ ] Teamwork possui aceite ou autoridade formal.
- [ ] Responsabilidade não é transferida silenciosamente.
- [ ] Conversa e Nota são distintas.
- [ ] Métricas não humilham nem diagnosticam.

## 14. Código e testes — crítico para implementação

- [ ] Código segue padrões existentes legítimos.
- [ ] Não há duplicação evitável ou dependência circular nova.
- [ ] Transações/concorrência foram analisadas.
- [ ] Testes de domínio passam.
- [ ] Autorização permitida/negada foi testada.
- [ ] Migration/backfill foi testado.
- [ ] Eventos/auditoria foram testados.
- [ ] Falhas e idempotência foram testadas.
- [ ] `manage.py check` passa.
- [ ] Testes focados e suíte aplicável passam.
- [ ] Gaps de lint/type checking foram declarados.

## 15. Documentação e entrega

- [ ] Documentação afetada foi atualizada.
- [ ] RFC não foi alterada silenciosamente.
- [ ] ADR existe quando escolha técnica relevante exige.
- [ ] Progresso de loop foi atualizado.
- [ ] Diff foi inspecionado.
- [ ] Relatório final contém comandos/resultados.
- [ ] Ações manuais e rollback estão claros.

## 16. Regra de decisão

- `COMPLETED`: todos os itens aplicáveis e gates aprovados.
- `COMPLETED_WITH_GAPS`: críticos aprovados; gaps não bloqueantes explícitos.
- `BLOCKED`: qualquer crítico falha ou decisão normativa indispensável falta.

## 17. Lacunas conhecidas

Aplicar sempre o registro central do ENG-0000: RFC-0015/0016 ausentes, drafts e elaboração normativa pendente da RFC-0012. Aplicar GAP-ENG-0004-001 enquanto lint/type checking não estiverem configurados.

## 18. Relatório de validação

O checklist cobre cumulativamente os doze gates do `ENG-QUALITY-GATES.md`, preserva responsabilidade exclusiva e não adiciona regra de produto.

**Resultado:** `COMPLETED_WITH_GAPS`, devido às lacunas herdadas.
