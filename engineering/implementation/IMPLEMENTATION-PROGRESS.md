# Progresso da Implementação Integral

**Estado geral:** IN_PROGRESS  
**Fase atual:** Fase 2 — identidade e autorização  
**Ciclo atual:** IMP-002 — identidade e autorização central para ações sensíveis  
**Último ciclo concluído:** IMP-001 — transição auditável de status do Pedido  
**Data:** 01/08/2026

## Contrato do ciclo IMP-001

- **Objetivo:** centralizar a mudança de status do Pedido em caso de uso transacional e auditável.
- **Resultado observável:** mudanças individuais, em massa e rejeições da Produção preservam as permissões atuais e sempre registram histórico com autoria.
- **Legado substituído:** atribuição direta de `Pedido.status` nas views.
- **Fontes:** RFC-0002; RFC-0005; RFC-0006; RFC-0007; ENG-0006, fases 1–3.
- **Áreas:** Pedidos, operador existente, histórico, views, migration e testes.
- **Migração:** vínculo opcional do histórico com `OperadorGestor`, sem inferir autoria de registros antigos.
- **Critério:** todos os três fluxos delegam ao caso de uso; alterações negadas não persistem; alteração aceita registra histórico; gates aprovados.
- **Fora do ciclo:** identidade oficial completa, evento genérico/outbox, decomposição de estados e Processo/Etapa.

## Próximo ciclo recomendado

IMP-002 — identidade e autorização central para ações sensíveis.

## Histórico resumido

### IMP-001 — COMPLETED

- **Capacidade:** caso de uso transacional único para transições de status.
- **Substituído:** escrita direta de status nos fluxos individual, em massa e rejeição da Produção.
- **Áreas:** `apps/pedidos/use_cases.py`, models, migration 0008, views e testes.
- **Testes:** 10 aprovados; migration criada do zero no banco de teste; Django check, Ruff e mypy aprovados.
- **Quality Gates:** Fonte Normativa PASS; Arquitetura PASS; Domínio PASS; Eventos e Auditoria PASS; Segurança PASS; Testes PASS.
- **Limitação:** `HistoricoStatusPedido` é compatibilidade temporária até o evento/auditoria genéricos de IMP-003.
- **Teste humano:** no detalhe do Pedido, alterar o status e confirmar a mensagem; em Pedidos, aplicar ação em massa; em Produção, rejeitar com motivo. Usuário alheio ao Pedido deve ter a alteração negada.
- **Commit:** commit atômico do próprio ciclo; consultar o `git log` (hash registrado na retomada seguinte).
