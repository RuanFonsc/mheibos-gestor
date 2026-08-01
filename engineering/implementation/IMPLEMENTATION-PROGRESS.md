# Progresso da Implementação Integral

**Estado geral:** IN_PROGRESS  
**Fase atual:** Fase 5 — Processo, Fluxo e Etapa piloto  
**Ciclo atual:** IMP-005 — Processo, Fluxo e Etapa piloto  
**Último ciclo concluído:** IMP-004 — estados independentes do Pedido  
**Data:** 01/08/2026

## Contrato do ciclo IMP-003

- **Objetivo:** introduzir evento operacional imutável e instrumentar os casos de uso já migrados.
- **Resultado atual:** transição de status produz `PedidoStatusAlterado` com versão, autoria, origem, alvo, correlação e valores anterior/posterior na mesma transação.
- **Fontes:** RFC-0006 §§5–13 e 18; INV-024 a INV-029; ENG-0006 §6.
- **Migração:** nova tabela aditiva; nenhum histórico antigo é inventado.
- **Critério do ciclo:** ampliar para criação de Pedido e autenticação, validar consulta de auditoria e concluir gates.
- **Fora desta fatia:** fila assíncrona, eventos offline e evidências de arquivo.

## Contrato concluído do ciclo IMP-002

- **Objetivo:** tornar credenciais não legíveis e sessões independentes do nome mutável do operador.
- **Resultado observável:** login web e launcher usam o mesmo contrato; senhas novas são hash; senha legada válida é atualizada no primeiro uso; renomear operador não perde a sessão.
- **Legado substituído:** comparação/gravação direta de senha e sessão identificada somente por `operador_nome`.
- **Fontes:** RFC-0005 §§6–8; RFC-0007 §§5–7; INV-030 a INV-036; ENG-0006 §5.
- **Áreas:** OperadorGestor, autenticação, formulários, views web/API, middleware, permissões, preferências e testes.
- **Migração:** atualização gradual e irreversível somente após senha legada ser comprovada; sessões antigas são promovidas ao identificador técnico quando lidas.
- **Critério:** nenhum caminho mapeado grava senha nova em texto; login e troca usam contrato central; sessão usa `operador_id`; testes e gates aprovados.
- **Fora do ciclo:** catálogo granular de permissões, reautenticação auditada como evento, bloqueio de edição e sessão offline.

## Contrato concluído do ciclo IMP-001

- **Objetivo:** centralizar a mudança de status do Pedido em caso de uso transacional e auditável.
- **Resultado observável:** mudanças individuais, em massa e rejeições da Produção preservam as permissões atuais e sempre registram histórico com autoria.
- **Legado substituído:** atribuição direta de `Pedido.status` nas views.
- **Fontes:** RFC-0002; RFC-0005; RFC-0006; RFC-0007; ENG-0006, fases 1–3.
- **Áreas:** Pedidos, operador existente, histórico, views, migration e testes.
- **Migração:** vínculo opcional do histórico com `OperadorGestor`, sem inferir autoria de registros antigos.
- **Critério:** todos os três fluxos delegam ao caso de uso; alterações negadas não persistem; alteração aceita registra histórico; gates aprovados.
- **Fora do ciclo:** identidade oficial completa, evento genérico/outbox, decomposição de estados e Processo/Etapa.

## Próximo ciclo recomendado

IMP-005 — introduzir Processo, Fluxo instanciado e Etapa em um fluxo piloto de baixo risco.

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

### IMP-002 — COMPLETED

- **Capacidade:** credenciais protegidas pelo hasher do Django e sessão vinculada ao ID técnico do operador.
- **Substituído:** comparações/gravações diretas de senha nos logins, launcher, formulários e trocas de senha; sessão dependente apenas do nome.
- **Migração:** senha legada é convertida somente após prova correta; sessão legada por nome é promovida ao ser lida.
- **Testes:** 17 aprovados, incluindo sete cenários específicos de credencial e sessão; migrations sem divergências; Django check, Ruff, mypy e Skill aprovados.
- **Quality Gates:** Fonte Normativa PASS; Arquitetura PASS; Domínio PASS; Eventos e Auditoria NOT_APPLICABLE — infraestrutura entra no IMP-003; Segurança PASS; Testes PASS.
- **Limitação:** catálogo granular de permissões, reautenticação como evento e bloqueio de edição permanecem em ciclos posteriores da mesma fase arquitetural.
- **Teste humano:** entrar pelo Gestor e launcher; trocar a senha; sair e entrar com a nova; renomear o próprio perfil e continuar navegando. Senha antiga ou incorreta deve ser recusada.
- **Commit:** commit atômico do próprio ciclo; hash registrado na retomada seguinte.

### IMP-003 — COMPLETED

- **Capacidade:** evento operacional imutável com autoria, origem, alvo, versão, correlação, antes/depois, resultado e chave de idempotência.
- **Integração:** status, login aceito/recusado e criação de Pedido nos canais Gestor e Vendas.
- **Interface:** consulta administrativa em `/auditoria/`; usuário comum é recusado no servidor.
- **Migração:** tabela aditiva; nenhum fato legado foi inferido.
- **Testes:** 21 aprovados; incluem imutabilidade, idempotência, rollback, canais de criação e autorização da consulta.
- **Quality Gates:** Fonte Normativa PASS; Arquitetura PASS; Domínio PASS; Eventos e Auditoria PASS; Segurança PASS; Testes PASS.
- **Limitações:** eventos offline, evidências e processamento secundário entram nos ciclos proprietários; transporte permanece substituível.
- **Teste humano:** entrar como administrador, alterar um status, criar pedidos pelo Gestor e Vendas e abrir Auditoria; tentar `/auditoria/` como usuário comum e confirmar a recusa.
- **Commit:** commit atômico do próprio ciclo; hash registrado na retomada seguinte.

### IMP-004 — COMPLETED_WITH_GAPS

- **Capacidade:** estado comercial e de entrega registrados separadamente; estado financeiro derivado deterministicamente de total e pagamentos confirmados.
- **Compatibilidade:** `Pedido.status` permanece como projeção operacional legada somente até Processo/Etapa no IMP-005.
- **Migração:** backfill aditivo preserva cancelados, prontos e entregues; entrega antiga só é concluída comercialmente quando a quitação é comprovável.
- **Segurança:** entrega nova com saldo aberto é recusada; a exceção superior aguarda reautenticação, motivo, auditoria e Pendência.
- **Interface:** detalhe e assistência de entrega exibem dimensões independentes.
- **Testes:** 25 aprovados, incluindo derivação financeira, entrega paga, recusa com saldo e migração real de dados legados; Django check, Ruff e mypy aprovados.
- **Quality Gates:** Fonte Normativa PASS; Arquitetura PASS; Domínio PASS; Eventos e Auditoria PASS; Segurança PASS; Migração PASS; Testes PASS.
- **Teste humano:** abrir pedidos em estados cancelado, pronto, entregue, quitado e parcial; confirmar os rótulos separados e a recusa de entrega com saldo.
- **Lacuna não bloqueante:** fluxo autorizado de entrega com saldo será implementado junto às permissões e Pendências proprietárias.
- **Commit:** commit atômico do próprio ciclo; hash registrado na retomada seguinte.
