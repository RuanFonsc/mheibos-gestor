# Progresso da Implementação Integral

**Estado geral:** IN_PROGRESS  
**Fase atual:** Fase 8 — operação offline restrita e sincronização  
**Ciclo atual:** IMP-008 — comandos offline e reconciliação segura  
**Último ciclo concluído:** IMP-007 — Pendências estruturais determinísticas  
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

IMP-008 — introduzir comandos offline idempotentes, fila local e reconciliação no escopo autorizado.

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

### IMP-005 — COMPLETED_WITH_GAPS

- **Capacidade:** Modelo de Fluxo versionado, Processo UUID e Etapa UUID formalizam o piloto de Produção do Pedido.
- **Fluxo vertical:** entrada em produção instancia; pronto conclui; rejeição bloqueia com motivo; nova entrada retoma; cancelamento encerra.
- **Histórico:** fluxo instanciado preserva snapshot e impede edição silenciosa da versão usada.
- **Migração:** schema aditivo, sem inferir Processo para Pedido legado.
- **Eventos:** confirmação, conclusão, bloqueio, desbloqueio e cancelamento são auditáveis na mesma transação.
- **Interface:** detalhe do Pedido mostra Processo, versão, Etapa, estado, responsável e motivo de bloqueio.
- **Testes:** 32 aprovados, incluindo idempotência, imutabilidade, rollback e proibição de reabertura de Processo final pelo status legado; Django check, Ruff, mypy e migrations aprovados.
- **Quality Gates:** Fonte Normativa PASS; Arquitetura PASS; Domínio PASS; Eventos e Auditoria PASS; Segurança PASS; Migração PASS; Testes PASS.
- **Lacunas não bloqueantes:** catálogo amplo de modelos, várias Etapas/dependências, evidências formais e processos independentes entram nos ciclos proprietários.
- **Teste humano:** mover Pedido para produção, conferir Processo; rejeitar com motivo, retomar e marcar pronto; confirmar estados no detalhe e Auditoria.
- **Commit:** commit atômico do próprio ciclo; hash registrado na retomada seguinte.

### IMP-006 — COMPLETED_WITH_GAPS

- **Capacidade:** uma projeção somente leitura compõe estados comercial, financeiro, entrega e operacional do Pedido.
- **Precedência:** Processo formal é fonte operacional; `Pedido.status` aparece apenas como compatibilidade identificada quando não há Processo.
- **Integração:** Gestor, Vendas, dashboard, relatório e Produção usam o mesmo contrato de projeção.
- **Fila:** Produção seleciona Processo em andamento/bloqueado e Prontos seleciona Processo concluído; fallback legado continua disponível.
- **Segurança:** recortes e permissões de cada interface foram preservados; projeção não persiste nem autoriza ações.
- **Testes:** 34 aprovados, incluindo divergência intencional entre Processo e status legado nas três interfaces; Django check, Ruff, mypy e migrations aprovados.
- **Quality Gates:** Fonte Normativa PASS; Arquitetura PASS; Domínio PASS; Interface PASS; Segurança PASS; Testes PASS.
- **Lacunas não bloqueantes:** outras famílias de Processo ainda usarão fallback até serem formalizadas; Orquestrador de Interface completo pertence a ciclo posterior da RFC-0009.
- **Teste humano:** abrir o mesmo Pedido no Gestor, Vendas e Produção; comparar estado e fonte; concluir Processo com status legado divergente e confirmar a fila correta.
- **Commit:** commit atômico do próprio ciclo; hash registrado na retomada seguinte.

### IMP-007 — COMPLETED_WITH_GAPS

- **Capacidade:** Pendência UUID com origem explícita, responsável principal, vários destinatários, estado e forma de encerramento.
- **Fluxo vertical:** rejeição da Produção abre obrigação única; retomada/conclusão resolve; cancelamento autorizado encerra.
- **Responsabilidade:** a pessoa responsável pela Etapa continua principal; destinatários não duplicam a Pendência nem transferem responsabilidade.
- **Segurança:** usuário comum vê somente Pendências próprias/destinadas; administrador mantém visão global autorizada.
- **Interface:** módulo textual e não bloqueante, sem depender de IA, popup, scheduler ou manipulação visual automática.
- **Eventos:** criação e encerramento auditáveis na mesma transação; falha reverte a mudança operacional completa.
- **Testes:** 38 aprovados, incluindo criação, encerramento, acesso e rollback; Django check, Ruff, mypy e migrations aprovados.
- **Quality Gates:** Fonte Normativa PASS parcial; Arquitetura PASS; Domínio PASS; Eventos e Auditoria PASS; Segurança PASS; Migração PASS; Testes PASS.
- **Lacuna formal:** política temporal, briefing, repetição e escalonamento permanecem `DECISAO_HUMANA_NECESSARIA` até RFC-0012 completa.
- **Teste humano:** rejeitar Pedido em Produção, abrir Pendências, retomar Produção e conferir o item em Encerradas e na Auditoria.
- **Commit:** commit atômico do próprio ciclo; hash registrado na retomada seguinte.
