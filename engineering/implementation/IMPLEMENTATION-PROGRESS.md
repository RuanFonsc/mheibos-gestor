# Progresso da Implementação Integral

**Estado geral:** IN_PROGRESS  
**Fase atual:** Fase 8 — operação offline restrita e sincronização  
**Ciclo atual:** IMP-008 — comandos offline e reconciliação segura  
**Último ciclo concluído:** IMP-007A — Gateway opcional de IA e adaptador Gemini  
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

IMP-008C.2b — inicializar no banco local somente a identidade protegida da Estação e habilitar login offline com política/permissão registrada.

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

### IMP-007A — COMPLETED_WITH_GAPS

- **Capacidade:** Gateway de IA substituível, adaptador oficial Google Gemini e resumo operacional assistido, somente leitura e acionado pelo usuário.
- **Ordem excepcional:** fundação antecipada por decisão humana explícita em 01/08/2026; arquitetura cognitiva completa, analytics e governança permanecem nos ciclos proprietários e RFCs futuras.
- **Não bloqueio:** desligamento, chave ausente, provider incompatível, falha externa ou resposta vazia retornam fallback determinístico e não alteram Pedido, Processo ou Pendência.
- **Minimização:** somente identificador técnico e estados operacionais entram no contexto; cliente, telefones, valores, observações e arquivos não são enviados.
- **Autoridade:** texto gerado é sugestão não persistida; não valida, autoriza ou executa operações. A tentativa registra metadados sem prompt, resposta ou segredo.
- **Provider:** SDK oficial `google-genai`, configuração exclusivamente por ambiente, modelo estável configurável e default `gemini-3.6-flash`.
- **Testes:** 44 aprovados no conjunto; 6 cobrem fallback, falha, sucesso simulado, POST, auditoria auxiliar e imutabilidade operacional. Django check, migrations e mypy aprovados; Ruff do escopo de produto aprovado.
- **Quality Gates:** Fonte Normativa PASS; Arquitetura PASS; Domínio PASS; Eventos e Auditoria PASS_WITH_GAP; Segurança PASS; IA indisponível PASS; Testes PASS.
- **Lacunas não bloqueantes:** validação online requer uma nova chave rotacionada; políticas amplas de conhecimento, retenção, custo, quotas e governança aguardam os ciclos/RFCs proprietários.
- **Teste humano:** com IA desligada, gerar resumo e confirmar fallback; depois de configurar chave nova, habilitar Gemini, gerar resumo e confirmar que nenhum estado se altera.

### IMP-008A — COMPLETED

- **Capacidade:** primeiro corte executável do modo offline restrito, com criação local de Pedido, identidade técnica, código visível permanente, sequência por Estação/origem, pacote coerente e fila durável.
- **Separação:** a mesma base de código pode executar como `central` ou `client_offline`, mas cada papel usa persistência própria; uma tabela da Central não foi tratada como armazenamento local.
- **Atomicidade:** no papel local, formulário, Pedido, itens, evento causal com UUID estável, reserva da sequência e unidade de sincronização confirmam ou revertem juntos.
- **Segurança:** nenhuma pessoa existente recebe código offline por inferência; código de origem é único e explícito. Modo local bloqueia mutações de registros globais e logout com pendências.
- **Integridade:** payload e checksum ficam imutáveis; falhas preservam conteúdo, tentativas e motivo visível.
- **Central:** incorporação valida esquema, checksum e autoria permanente; reenvio da mesma chave devolve confirmação existente sem duplicar Pedido, Cliente, itens ou eventos.
- **Interface:** banner persistente identifica o modo restrito e painel `/sincronizacao/` apresenta fila, origem, estado, tentativas e falha.
- **Testes:** 14 testes específicos aprovados: atomicidade, rollback, sequência, imutabilidade, corrupção, autoria, idempotência, formulário real, bloqueio global e logout.
- **Fora desta fatia:** transporte autenticado, provisionamento de Estação, cache de identidade/credencial, detecção de queda, comutação Electron, retentativa automática e confirmação cliente-servidor entram em IMP-008B/8C.
- **Classificação:** `adicionar`; campos em Pedido/Operador são aditivos, sem backfill especulativo.

### IMP-008B — COMPLETED

- **Capacidade:** Estação autorizada com UUID e segredo verificado por hash, mais endpoint HTTP central para incorporação do pacote offline.
- **Autenticação:** a Central persiste somente o hash; o segredo é retornado uma vez no provisionamento e nunca aparece em evento ou resposta posterior.
- **Vinculação:** UUID do envelope deve coincidir com a Estação autenticada; um segredo válido não autoriza falsificar outra origem.
- **Contrato:** endpoint aceita somente no papel `central`, limita pacote, valida JSON, esquema, checksum, autoria e unidade completa antes da transação.
- **Confirmação:** primeira incorporação responde `INCORPORADO`; reenvio responde `JA_INCORPORADO` apontando o mesmo Pedido global, sem efeitos duplicados.
- **Segurança:** endpoint técnico não depende de sessão web, mas permanece fechado por credencial de Estação; segredo inválido não persiste dados.
- **Testes:** 8 cenários de serviço/transporte aprovados, incluindo segredo em hash, recusa, Estação divergente e confirmação idempotente.
- **Fora desta fatia:** armazenamento protegido do segredo no Windows, provisionamento administrativo visível, transporte cliente e retentativa automática entram em IMP-008C.

### IMP-008C.1 — COMPLETED

- **Capacidade:** provisionamento administrativo visível da Estação e persistência protegida das credenciais do Cliente Electron.
- **Reautenticação:** somente administrador autenticado e com senha atual comprovada cria Estação; erro ou nome repetido não cria credencial.
- **Exposição única:** segredo de alta entropia aparece somente na resposta de criação. Banco e evento guardam nome, UUID, estado e hash, nunca o segredo.
- **Windows:** Electron usa `safeStorage`; sem proteção disponível, recusa salvar em vez de rebaixar para texto legível.
- **Migração:** configuração antiga com senha PostgreSQL ou segredo legível é regravada protegida na próxima abertura; os campos legíveis são removidos do JSON.
- **Setup remoto:** Cliente exige UUID e segredo provisionados antes de abrir; a configuração persistida contém somente conteúdo cifrado pelo sistema operacional.
- **Testes:** 21 testes Django do módulo, mais teste Node isolado que prova ausência dos dois segredos no JSON, recuperação autorizada e recusa sem cofre disponível.
- **Fora desta fatia:** última identidade validada, cache autorizado, login offline e envio automático permanecem em IMP-008C.2/8D.

### IMP-008C.2a — COMPLETED

- **Capacidade:** capturar a candidata de login somente em memória, confirmar a identidade pela sessão central e guardar credencial + snapshot no cofre do Windows.
- **Sem hash exportado:** a Central devolve apenas nome, papel, código de origem e permissões da própria sessão; senha e hash nunca aparecem no endpoint.
- **Dupla prova:** snapshot exige sessão humana válida e segredo da Estação injetado pelo processo principal do Electron; o renderer não lê o segredo persistido.
- **Confirmação:** o cache só substitui a identidade anterior quando o nome confirmado pela Central coincide com a candidata que acabou de autenticar.
- **Falha segura:** login recusado, endpoint indisponível, nome divergente ou falha de cache preservam a última identidade válida e não encerram a operação online.
- **Persistência:** senha digitada fica em memória até a confirmação e então integra o JSON de identidade cifrado por `safeStorage`; nunca é escrita legível.
- **Testes:** endpoint prova ausência de senha/hash e recusa segredo de Estação incorreto; teste Node prova que a credencial offline não aparece no JSON persistido.
- **Fora desta fatia:** materializar a identidade no banco SQLite local e autenticar offline pertencem a IMP-008C.2b.

### IMP-008C.2b — COMPLETED

- **Capacidade:** comando interno materializa no SQLite novo a última identidade validada, permitindo que o autenticador existente compare a senha localmente depois da indisponibilidade da Central.
- **Canal do segredo:** o JSON de identidade é recebido somente pela entrada padrão do subprocesso; senha ou hash não integram argumentos, ambiente, saída ou protocolo central.
- **Isolamento:** execução é recusada fora do papel `client_offline` e quando o identificador da Estação não coincide com a configuração local.
- **Menor privilégio:** papel e permissões precisam ser coerentes; um snapshot adulterado não pode promover permissões contraditórias.
- **Preservação:** banco com outra identidade é recusado integralmente, sem excluir, desativar ou sobrescrever operadores existentes.
- **Credencial local:** a senha é transformada pelo hasher oficial antes da persistência; texto legível permanece apenas na memória necessária ao bootstrap.
- **Testes:** 5 testes específicos e 72 no conjunto completo aprovados; Django check e verificação de migrações sem alterações aprovados.
- **Fora desta fatia:** executar migrações/bootstrap no ciclo do Electron, iniciar o backend SQLite e comutar a janela para ele pertencem à próxima fatia.

### IMP-008C.3 — COMPLETED_WITH_GAPS

- **Capacidade:** no início do Cliente Electron, indisponibilidade da Central aciona preparação do SQLite, bootstrap da identidade validada, backend `client_offline` e abertura do login local.
- **Separação:** a URL da Central permanece o destino online; o backend offline usa `127.0.0.1:8766` por padrão e banco `mheibos_offline`, sem compartilhar persistência com a Central.
- **Empacotado e desenvolvimento:** o executável empacotado executa sua migração interna; em desenvolvimento, o Electron executa `migrate --noinput` antes do bootstrap.
- **Segredo:** o snapshot é decriptado somente em memória e enviado ao comando pela entrada padrão; o processo de bootstrap ignora saída e nunca recebe senha em argumentos ou ambiente.
- **Falha segura:** sem identidade válida da própria Estação, ou se migração/bootstrap falhar, o Cliente não cria operador improvisado e informa que o modo offline ainda não está disponível.
- **Limite:** a captura de login só atualiza o cache quando a janela está efetivamente conectada à Central; autenticação local não tenta revalidar ou sobrescrever o snapshot central.
- **Testes:** helper Node valida configuração e vínculo da Estação; sintaxe do processo principal e preload aprovada; cofre aprovado; 72 testes Django, check e migrações aprovados.
- **Lacuna de validação:** `COMPLETED_WITH_GAPS` até smoke humano do instalador Windows confirmar queda real, abertura em `8766` e login local.
- **Fora desta fatia:** detectar retorno da Central, enviar a fila, persistir confirmações e comutar de volta pertencem a IMP-008D.

### IMP-008D.1 — COMPLETED

- **Capacidade:** ciclo durável da unidade local antes e depois do transporte: seleção ordenada, marcação prévia da tentativa, confirmação central validada, retentativa com backoff e recusa permanente visível.
- **Crash safety:** `PREPARANDO` e `ENVIANDO` voltam a ser elegíveis; queda após a requisição não perde a unidade e a idempotência central torna o reenvio seguro.
- **Confirmação:** somente `INCORPORADO` ou `JA_INCORPORADO`, com o mesmo identificador offline e Pedido global positivo, encerram a unidade.
- **Persistência:** código da confirmação, identificador global e instante de incorporação ficam gravados localmente; o payload causal continua imutável.
- **Falhas:** indisponibilidade agenda backoff exponencial limitado; recusas permanentes ficam em `REQUER_ATENCAO` e não entram em repetição infinita.
- **Auditoria:** confirmação local gera `PedidoOfflineConfirmado` na mesma transação, com chave idempotente e sem segredo de Estação.
- **Testes:** 10 cenários da fila cobrem preparação, confirmação, entidade divergente, backoff, recusa permanente, imutabilidade e rollback; migration explícita aprovada.
- **Fora desta fatia:** cliente HTTP autenticado e acionamento periódico pelo Electron pertencem a IMP-008D.2.

### IMP-008D.2 — COMPLETED

- **Capacidade:** comando restrito ao Cliente offline envia envelopes elegíveis ao endpoint central, classifica a resposta e aplica a confirmação ou retentativa durável de IMP-008D.1.
- **Autenticação:** UUID e segredo da Estação seguem em cabeçalhos; o segredo vem do cofre do Windows, não integra envelope, banco, saída do comando ou auditoria.
- **Destino:** somente URL HTTP/HTTPS válida é aceita; redirecionamentos são bloqueados para impedir encaminhamento da credencial a outro host.
- **Limites:** timeout de rede e resposta máxima de 2 MB evitam bloqueio indefinido e consumo sem limite; lote aceita de 1 a 100 unidades.
- **Classificação:** 2xx ainda exige confirmação semântica válida; 4xx fica em atenção humana; indisponibilidade/5xx recebe backoff; falhas globais de credencial ou contrato interrompem o lote.
- **Agendamento:** durante o modo offline, o processo principal dispara imediatamente e a cada 30 segundos, sem sobrepor execuções; o timer é encerrado junto com o aplicativo.
- **Interface:** painel local mostra Pedido central e código de confirmação, e não oferece provisionamento de Estações no papel offline.
- **Testes:** 7 testes de transporte/comando e 10 de fila aprovados; cobrem cabeçalhos, URL, bloqueio de redirect, confirmação, indisponibilidade, credencial recusada e isolamento de papel.
- **Fora desta fatia:** smoke com duas instâncias reais e comutação de volta à Central pertencem a IMP-008D.3.

### IMP-008D.3 — COMPLETED_WITH_GAPS

- **Capacidade:** após cada ciclo de envio, o Cliente verifica disponibilidade da Central e consulta o backend local para provar que todas as unidades estão `INCORPORADA`.
- **Autoridade:** o Electron não conta registros nem decide pela interface; o comando `verificar_retorno_online` recusa execução fora de `client_offline` e bloqueia qualquer estado não confirmado.
- **Dupla verificação:** ao aceitar a transição, a janela é desabilitada e fila/Central são verificadas novamente antes de encerrar o backend local.
- **Experiência segura:** continuar offline é a opção padrão; a pessoa é alertada sobre formulários não salvos. Recusar a troca mantém o modo e não repete o aviso durante a sessão.
- **Preservação:** SQLite não é apagado nem reescrito; permanece como evidência local. A janela volta ao login da Central e a sessão online é restabelecida pelo canal normal.
- **Eficiência do empacotado:** migrações automáticas agora executam somente na partida do servidor; comandos periódicos não repetem migrações. A preparação offline executa `migrate --noinput` explicitamente uma vez.
- **Testes:** 10 testes de transporte/retorno aprovados, incluindo bloqueio com pendência, liberação após confirmação e isolamento do papel Central; sintaxe Python e Electron aprovada.
- **Lacuna de validação:** `COMPLETED_WITH_GAPS` até smoke humano do instalador confirmar Central desligada, Pedido local, religamento, incorporação e retorno online.
- **Estado de IMP-008:** `COMPLETED_WITH_GAPS`; nenhuma lacuna técnica impede avançar ao próximo item do backlog.

### IMP-009A — COMPLETED

- **Capacidade:** `ArquivoOficialArte` representa múltiplos vínculos físicos por Pedido, guardando caminho, nome, extensão, proveniência, estados e campos técnicos sem persistir binário.
- **Identidade:** Pedido, caminho e nome tornam-se imutáveis no primeiro vínculo; exclusão física/lógica silenciosa é recusada e o futuro encerramento usa estado próprio.
- **Autorização:** somente pessoa autorizada a editar o Pedido vincula arquivo; modo offline não exibe o fluxo e o middleware continua bloqueando a mutação global.
- **Auditoria:** vínculo e evento `ArquivoOficialArteVinculado` confirmam na mesma transação; falha do evento reverte o vínculo.
- **Compatibilidade:** caminhos de `Pedido.caminho_arquivo_corel` recebem backfill `LEGADO/NAO_VERIFICADO`, sem autoria inventada. O campo permanece somente como leitura/entrada temporária; novos vínculos são gravados na entidade oficial.
- **Dono da compatibilidade:** app `pedidos`; remoção após todos os consumidores lerem `arquivos_oficiais_arte`, nenhum caminho legado ficar sem vínculo e a migração ser validada em cópia de produção.
- **Tema:** alteração é recusada após primeiro pagamento ou primeiro arquivo oficial, cobrindo sinais determinísticos já disponíveis; início formal da Etapa de Arte será incorporado quando a fatia de criação automática ligar Processo/Etapa ao arquivo.
- **Interface:** detalhe do Pedido lista arquivos, integridade e proveniência e permite vincular outro arquivo existente, deixando explícito que o banco guarda apenas referência.
- **Testes:** 7 cenários de domínio/interface e 1 teste de migration cobrem múltiplos vínculos, ausência de binário, idempotência, imutabilidade, exclusão, rollback, caminho inválido, tema e autorização.
- **Fora desta fatia:** nome/diretório automáticos, programa gráfico, verificação física, aceite consciente de alerta, anexos, arte de referência, pesquisa, backup e revisão anual pertencem a IMP-009B em diante.

### IMP-009B — COMPLETED

- **Capacidade:** cada vínculo oficial pode ser verificado contra o sistema de arquivos; existência, acesso, nome e tamanho conhecido atualizam o estado sem copiar o conteúdo para o banco.
- **Alerta explicável:** ausência, inacessibilidade ou divergência de nome produzem códigos e mensagens persistentes; nova verificação substitui a evidência anterior e exige novo reconhecimento quando ainda houver problema.
- **Aceite consciente:** o comando explícito `Eu entendi` registra pessoa, data, discrepâncias e evento `AlertaArquivoOficialReconhecido`; ele não corrige nem esconde o alerta.
- **Autorização:** somente pessoa autorizada a editar o Pedido verifica ou reconhece; verificação física fica indisponível no modo offline restrito.
- **Auditoria:** verificação e reconhecimento são transacionais e geram eventos próprios com estado anterior e posterior.
- **Testes:** 3 cenários novos cobrem arquivo íntegro, arquivo ausente, persistência do alerta, interface, reconhecimento e auditoria; suíte completa com 97 testes aprovada.
- **Fora desta fatia:** dimensões, proporção e resolução dependem de leitores técnicos por formato; criação automática depende das preferências normativas de programa, extensão e raiz física.

### IMP-009C — COMPLETED

- **Capacidade:** o upload legado `ArtePedido` passa a representar explicitamente a arte de referência visual usada na Ordem de Produção, separada do arquivo oficial e sem sincronização automática.
- **Ciclo de vida:** remover encerra apenas o vínculo; o registro, hash, nome, tamanho e arquivo físico permanecem preservados. Consultas operacionais usam `Pedido.artes_ativas`, enquanto o histórico continua disponível.
- **Integridade histórica:** `Pedido` passa a ser protegido contra exclusão enquanto qualquer vínculo de referência existir, inclusive encerrado.
- **Autoria e auditoria:** inclusão e desvinculação passam por serviços transacionais e geram `ArteReferenciaVinculada` e `ArteReferenciaDesvinculada`; falha de auditoria reverte o registro e remove somente a cópia órfã que ainda não chegou a constituir vínculo.
- **Migração:** vínculos legados recebem autoria e hash novos nulos, sem inferência; permanecem ativos até ação humana explícita.
- **Compatibilidade temporária:** o nome físico `ArtePedido` é mantido para evitar migração destrutiva; dono `apps/pedidos`, remoção após consumidores, importador legado e dados históricos migrarem para nome de domínio próprio.
- **Interface:** criação, edição, detalhe e listas passam a chamar o conteúdo de “arte de referência” e explicam que ele não substitui o arquivo oficial.
- **Testes:** 5 cenários novos cobrem autoria/hash/evento, autorização no serviço, preservação física e histórica, proteção do Pedido, rollback de auditoria e rota administrativa de desvinculação; baseline completo aprovado com 102 testes.
- **Fora desta fatia:** anexos gerais e sua decisão de duplicidade são entidade e fluxo separados; não foram fundidos à referência visual.

### IMP-009D — COMPLETED

- **Capacidade:** `AnexoPedido` mantém uma lista única de arquivos anexados, separada de arte oficial e arte de referência, guardando arquivo físico fora do banco e somente referência/metadados no registro.
- **Conteúdo opaco:** o serviço não tenta interpretar, descriptografar, solicitar senha, renderizar ou extrair significado; calcula apenas SHA-256 técnico para integridade e duplicidade.
- **Duplicidade:** conteúdo já conhecido é recusado por padrão com explicação; uma nova cópia só é vinculada quando a pessoa marca explicitamente a decisão de manter duplicados, registrada no evento.
- **Ciclo de vida:** administrador remove apenas o vínculo; arquivo físico, metadados, autoria e histórico permanecem. O `Pedido` é protegido contra exclusão enquanto o histórico do anexo existir.
- **Autorização e auditoria:** autor do Pedido ou administrador adiciona; somente administrador desvincula; regras vivem no serviço. Inclusão e desvinculação geram eventos transacionais, e falha de auditoria elimina apenas a cópia órfã ainda não vinculada.
- **Acesso:** anexos usam armazenamento privado sem URL pública; download sempre passa por endpoint que revalida a autorização do Pedido e força `Content-Disposition: attachment`.
- **Interface:** detalhe do Pedido lista anexos, permite seleção múltipla e apresenta a decisão explícita para duplicidades; informa que o Mheibos não interpreta conteúdo.
- **Testes:** 6 cenários cobrem opacidade, metadados, ausência de URL pública, duplicidade com decisão humana, autorização e download forçado, preservação física/histórica, proteção do Pedido, rollback e interface; baseline completo aprovado com 108 testes.
- **Fora desta fatia:** Ctrl+V binário genérico depende de contrato seguro do navegador/Electron; seleção múltipla e drag-and-drop nativo do campo já funcionam sem criar interpretação de conteúdo.

### IMP-009E — COMPLETED

- **Capacidade:** a lista integrada de Pedidos localiza artes por número do Pedido, cliente, telefones, produto, tema, descrição, nome/caminho/extensão do arquivo, referência visual e metadados técnicos.
- **Metadados:** propriedades técnicas e discrepâncias JSON são convertidas apenas para consulta textual; tamanho, largura, altura e resolução recebem comparação numérica quando o termo é um número.
- **Escopo operacional:** arquivos oficiais encerrados e referências desvinculadas não participam da busca nem dos nomes exibidos; o histórico permanece preservado em suas entidades.
- **Interface:** o campo existente foi ampliado, sem criar tela paralela, e cada cartão mostra os nomes dos arquivos oficiais ativos que justificam o resultado.
- **Leitura:** pesquisa não altera estado e não gera evento de domínio, em conformidade com a regra de auditoria para consultas comuns.
- **Testes:** 2 cenários percorrem os dez critérios de busca, metadados JSON e numéricos, evidência visual e exclusão de vínculo encerrado; baseline completo aprovado com 110 testes.
- **Fora desta fatia:** indexação dedicada e ranking só serão introduzidos mediante evidência de volume/desempenho; a consulta atual preserva semântica idêntica em SQLite e PostgreSQL.

### IMP-009F — COMPLETED

- **Capacidade:** a verificação física extrai automaticamente largura, altura, proporção reduzida, formato, modo de cor, quantidade de quadros e DPI quando disponíveis em raster BMP/GIF/JFIF/JPEG/PNG/TIFF/WEBP.
- **Limite seguro:** Pillow já era dependência oficial; o extrator abre somente extensões explicitamente suportadas e captura arquivo inválido, inacessível ou excessivo sem derrubar o fluxo.
- **Discrepância:** arquivo que se declara raster mas não permite leitura técnica recebe `PROPRIEDADES_TECNICAS_INDISPONIVEIS`, explicação e o mesmo aceite consciente auditado do monitoramento.
- **Compatibilidade:** CDR, AI, SVG e demais formatos não geram falso alerta; metadados existentes são preservados e a leitura raster registra apenas que não é aplicável.
- **Persistência e auditoria:** a fotografia técnica participa da mesma transação e do evento `ArquivoOficialArteVerificado`, junto de integridade, tamanho e discrepâncias.
- **Interface:** detalhe do Pedido exibe dimensões, proporção, DPI e formato; formatos não suportados recebem explicação não bloqueante.
- **Testes:** 3 cenários novos cobrem raster real 1600×900/300 DPI, conteúdo raster inválido e preservação de metadados especializados em CDR; baseline completo aprovado com 113 testes.
- **Fora desta fatia:** leitura nativa de CDR/AI/SVG exige extratores próprios e será adicionada apenas com dependência segura e contrato determinístico.

### IMP-009G — COMPLETED

- **Capacidade:** administrador encerra individualmente um vínculo oficial durante a revisão, sem apagar ou mover o arquivo físico e sem alterar sua identidade.
- **Persistência:** estado `ENCERRADO`, autoria, instante, observação e declaração opcional de backup prévio ficam no vínculo; nome, caminho, integridade, dimensões, DPI e propriedades técnicas permanecem intactos.
- **Autorização e consciência:** a regra administrativa vive no serviço; a interface exige digitar `ENCERRAR` e não transforma backup opcional em requisito obrigatório.
- **Auditoria:** `VinculoArquivoOficialEncerrado` registra estado anterior/posterior e as garantias de preservação na mesma transação; repetição é idempotente e falha do evento reverte o encerramento.
- **Projeção:** vínculo encerrado continua visível como histórico no detalhe, sem ação de abrir ou verificar e fora da pesquisa operacional.
- **Cancelamento:** cancelar o Pedido foi validado separadamente e não altera estado, caminho ou nome do arquivo oficial.
- **Testes:** 5 cenários novos cobrem preservação física real, identidade/metadados, autorização, idempotência, rollback, confirmação/interface e cancelamento; baseline completo aprovado com 118 testes.
- **Fora desta fatia:** arquivamento em lote e “manter anos ativos” exigem definir normativamente qual data atribui o vínculo a um período; nenhum ano foi inferido silenciosamente.

### IMP-009 — COMPLETED_WITH_GAPS

- **Resultado consolidado:** IMP-009A–G entregam a fronteira oficial de vínculos, monitoramento, referência visual, anexos opacos, pesquisa, metadados raster e encerramento administrativo preservador.
- **Auditoria de fontes:** RFC-0014, Inventário Oficial, diagnóstico, relatório funcional, mapa de migração, implementação Electron e preferências existentes foram comparados antes do encerramento do ciclo.
- **DECISAO_HUMANA_NECESSARIA — criação física:** faltam raiz oficial, origem da data de Ano/Mês/Dia, programas/extensões admitidos e contrato determinístico para criar um arquivo vazio com as configurações padrão do software.
- **DECISAO_HUMANA_NECESSARIA — backup:** faltam mecanismo por provedor, credenciais, destino, retenção e critério verificável de sucesso; nenhuma cópia foi presumida pela simples presença de pasta sincronizada.
- **DECISAO_HUMANA_NECESSARIA — revisão anual:** falta definir qual data atribui cada vínculo ao período e a semântica de arquivar ou manter um ano ativo.
- **Extratores especializados:** CDR/AI/SVG continuam não bloqueantes conforme “quando possível”; sua ampliação exige dependência segura e contrato determinístico, sem impedir formatos não suportados.
- **Continuidade:** as lacunas são isoladas, não invalidam as capacidades entregues e não bloqueiam IMP-010; o ciclo segue como `COMPLETED_WITH_GAPS`.

### IMP-010A — COMPLETED

- **Capacidade:** uma pessoa com identidade ativa cria missão individual voluntária com título, objetivo temporário, critério de conclusão, resultado esperado opcional, origem, responsável e estado planejado.
- **Workspace persistente:** lista e detalhe recompõem o contexto após troca de tela ou reinício; a missão é entidade própria e não copia Pedido, Processo, Etapa ou Pendência.
- **Autoridade e exposição:** criador e responsável são a própria pessoa; usuário comum vê somente suas missões e administrador mantém supervisão. Identidade temporária não cria missão.
- **Offline:** consulta permanece disponível conforme a última base local autorizada; criação é bloqueada pelo contrato global de mutações offline.
- **Auditoria:** `MissaoCriada` participa da mesma transação; falha do evento reverte a missão.
- **Testes:** 5 cenários cobrem contrato mínimo, identidade, persistência, auditoria/rollback, privacidade, interface e isolamento offline.
- **Fora desta fatia:** missão atribuída, participantes, aceite, tarefas, referências, transições, chat, notas e decisões serão adicionados em fatias próprias.

### IMP-010B — COMPLETED

- **Capacidade:** missão individual planejada pode ser iniciada, pausada, retomada, bloqueada e concluída por serviços transacionais com transições explícitas.
- **Autoridade:** somente o responsável altera a missão voluntária; visibilidade administrativa não concede poder implícito sobre o workspace de outra pessoa.
- **Pausa e retomada:** instante e tempo acumulado de pausa são persistidos; atualização de retomada e duração entram no evento sem apagar contexto.
- **Bloqueio:** motivo, dependência, impacto, ajuda necessária e urgência são obrigatórios; a retomada limpa a fotografia atual, enquanto o evento preserva o histórico.
- **Conclusão:** exige resultado alcançado e confirmação do responsável. Obrigação remanescente não pode ser enterrada em texto livre; até existir destino formal, a missão permanece aberta.
- **Auditoria e falha segura:** início, pausa, retomada, bloqueio e conclusão bloqueiam concorrentemente o registro e geram eventos na mesma transação; repetição do mesmo comando não duplica evento e falha de auditoria reverte o estado.
- **Offline:** consulta continua permitida, mas todas as transições globais permanecem bloqueadas no Cliente offline.
- **Testes:** 7 cenários novos cobrem ciclo completo, contexto de bloqueio, autoridade, transição inválida, obrigação remanescente, idempotência, concorrência transacional, rollback, interface e offline; baseline completo aprovado com 130 testes.
- **Fora desta fatia:** `EM_REVISAO` depende de participante/aprovador ou autoridade identificável; tarefas, referências e destinação formal de pendências entram nos próximos ciclos.

### IMP-010C — COMPLETED

- **Capacidade:** missão coletiva espontânea cria liderança explícita e convites sem impor obrigação; convidado pode aceitar, recusar, pedir informações ou sugerir ajuste de participação.
- **Consentimento:** aceite constitui participação e torna a missão planejada; recusa encerra somente aquele convite, não gera punição e permite convite futuro com novo histórico.
- **Papéis:** liderança, participante, observador autorizado e aprovador são vínculos explícitos; acumulação futura não será inferida por cargo global.
- **Saída voluntária:** participante aceito pode sair após confirmação consciente e motivo; contribuições e vínculo histórico permanecem. Líder precisa transferir liderança antes de sair.
- **Visibilidade:** convite pendente e participação aceita dão acesso ao workspace da missão; recusa ou saída encerram a projeção corrente sem apagar o registro. Nenhum vínculo concede acesso automático a dados externos restritos.
- **Encerramento:** convites pendentes impedem conclusão; missão concluída, cancelada ou arquivada não recebe convites, respostas ou saídas tardias.
- **Auditoria e concorrência:** criação, convite, manifestação, aceite, recusa e saída são transacionais, bloqueiam registros concorrentes e geram eventos; falha de evento reverte missão e participações.
- **Migração:** missões existentes recebem tipo `INDIVIDUAL_VOLUNTARIA`; nenhuma autoridade ou participação histórica é inventada.
- **Offline:** criação coletiva e todas as mutações de participação permanecem bloqueadas no Cliente offline.
- **Testes:** 10 cenários novos cobrem criação, consentimento, manifestação, recusa/reconvite, autoridade, idempotência, saída, visibilidade, encerramento, rollback, interface e offline.
- **Fora desta fatia:** missão atribuída exige tarefas iniciais, prazo e impacto; será implementada junto do modelo de tarefas e da matriz de autoridade administrativa.

### IMP-006B — COMPLETED

- **Convergência:** Mheibos Vendas deixa de ser uma superfície oficial; Gestor de Pedidos concentra a entrada comercial e Produção permanece uma visão especializada por função e Etapa.
- **Fluxo operacional:** Produção e Entrega aparecem como perspectivas contínuas do mesmo Pedido; a tela intermediária inicialmente rotulada como Expedição teve sua responsabilidade corrigida para Preparação de arte no IMP-006C.
- **Projeção oficial:** Lista e Detalhe usam a mesma projeção de Processo/Etapa; o detalhe agora carrega explicitamente `projetar_pedido()` e possui teste de regressão.
- **Funcionamento offline:** a fundação visual e as telas piloto permanecem utilizáveis quando bibliotecas visuais externas não carregam; IA não é requisito para qualquer ação operacional.
- **Validação visual:** 20 combinações de quatro telas por cinco resoluções/escalas foram aprovadas sem overflow, incluindo 125%, estado vazio e conteúdo extremo.
- **Rastreabilidade:** relatório completo em `engineering/implementation/IMP-006B-VISUAL-VALIDATION.md`.

### IMP-006C — COMPLETED_WITH_GAPS

- **Regra:** sem arte de referência ativa, o Pedido não avança para Produção ou estados posteriores.
- **Assistência atual:** fila de Preparação de arte, contador, notificação periódica determinística e ação direta para anexar arte.
- **Convergência funcional da interface (02/08/2026):** Preparação de arte e Assistência de Impressão permanecem funções distintas; ambas expõem o fluxo contínuo para a Produção especializada e Entrega. As filas agora comunicam prazo, responsável ou referência operacional, evidências, bloqueio, próxima ação e motivo calculado do alerta quando houver item aplicável.
- **Ações e segurança visual:** ações em massa desabilitadas explicam a seleção necessária; Entrega torna visível que saldo aberto exige autorização superior registrada, sem criar silenciosamente o mecanismo normativo ainda ausente.
- **Consistência:** rotas individual, em massa e de compatibilidade usam o mesmo caso de uso; o botão global “Abrir a Produção” foi removido.
- **Testes e visual:** 38 testes direcionados e 10 combinações visuais aprovados.
- **Lacuna:** Pendência formal, scheduler, cadência e escalonamento dependem da RFC-0012 completa; não bloqueiam a trava nem a fila atuais.

### IMP-009H — COMPLETED

- **Capacidade:** criação física vazia pela interface, nome oficial numerado, estrutura compartilhada por usuário/ano/mês/dia, escolha de programa/formato e vínculo auditado sem binário no banco.
- **Preferências:** Perfil recebe programa de arte padrão; Perfil da Empresa recebe raiz compartilhada e retenção de cópias locais; gestão de usuários é apresentada apenas na área Usuários.
- **Validação parcial:** testes direcionados de arquivos oficiais aprovam criação vazia, numeração, exigência de raiz, vínculos, integridade e auditoria.
- **Validação:** lint, type checking, Django check, migração e 150 testes aprovados; detalhe, Perfil e Usuários validados em navegador real nas cinco combinações oficiais, sem overflow horizontal. Evidências em `IMP-009H-VISUAL-VALIDATION.md`.
- **Estado:** COMPLETED para a fatia de criação; as capacidades seguintes permanecem separadas e rastreadas abaixo.
- **Próximas fatias:** estado agregado da arte, monitoramento de inatividade, confirmação de conclusão, restauração crítica, autorização gerencial, transferência e sincronização offline conforme DEC-IMP-033.

### IMP-009I — COMPLETED

- **Estado agregado:** cada Pedido possui uma preparação de arte própria em `NÃO INICIADA`, `EM PREPARAÇÃO` ou `CONCLUÍDA`, com responsável, atividade e confirmação humana rastreáveis.
- **Conclusão humana:** existência, tamanho ou conteúdo nunca concluem a arte automaticamente. A pessoa autorizada confirma a conclusão do conjunto inteiro somente quando há arquivo oficial ativo, acessível e com o nome preservado.
- **Linha de base:** no instante da conclusão, o Mheibos registra tamanho e data técnica de modificação de todos os arquivos oficiais, inclusive quando ainda não houve verificação manual.
- **Proteção:** enquanto a arte estiver concluída, criar ou vincular outro arquivo oficial é recusado no serviço e não é oferecido pela interface.
- **Alteração posterior:** verificação física detecta mudança de conteúdo depois da conclusão, registra pessoa e instante e exige a escolha explícita entre manter o conjunto concluído ou voltar à preparação.
- **Auditoria:** conclusão e decisão posterior geram eventos transacionais; voltar à preparação remove a confirmação anterior sem apagar o histórico.
- **Teste real:** criação vazia, conclusão sem verificação prévia, alteração física, alerta persistente e retorno à preparação foram exercitados no Pedido #1. O teste revelou e corrigiu a ausência inicial da linha de base.
- **Validação:** lint, type checking, Django check, migration check, testes direcionados e gate visual aprovados; evidências em `IMP-009I-VISUAL-VALIDATION.md`.
- **Próxima fatia:** alerta por duas horas de inatividade, cadência, lembrete, adiamento condicionado e prazo crítico conforme DEC-IMP-033.

### IMP-009J — COMPLETED

- **Detecção determinística:** criar ou vincular arquivo oficial inicia monitoramento; modificação física reinicia o prazo. Após duas horas sem alteração e sem conclusão humana, o alerta torna-se ativo.
- **Respostas:** `Concluir arte`, `Ainda estou trabalhando` (duas horas), `Lembrar em 30 minutos` e `Deixar a arte para amanhã` são comandos explícitos e auditados.
- **Adiamento:** disponível apenas nos dois primeiros alertas, exige a senha do responsável e suprime o alerta até a próxima data local. O alerta volta automaticamente quando o novo dia começa se a arte continuar aberta.
- **Prazo crítico:** usa as regras configuradas da categoria e a data de entrega. Dentro do limite crítico, o adiamento desaparece e o responsável pode solicitar ajuda urgente.
- **Responsabilidade:** somente o responsável atual responde ao alerta; uma falha na auditoria reverte integralmente lembrete, adiamento ou pedido de ajuda.
- **Descoberta assistencial:** o alerta persistente aparece no detalhe do Pedido, na fila de Preparação de Arte e na notificação global periódica, sem depender de IA.
- **Validação real:** alerta normal, lembrete de 30 minutos, segundo alerta, prazo crítico, bloqueio de adiamento, ajuda urgente e fila integrada foram exercitados no banco e navegador locais.
- **Testes e visual:** 59 testes focados aprovados; lint, type checking, Django, migration check, tokens e matriz visual sem overflow aprovados. Evidências em `IMP-009J-VISUAL-VALIDATION.md`.
- **Próxima fatia:** ausência crítica do arquivo, restauração vinculada e exceção gerencial por ação conforme DEC-IMP-033.

### IMP-009K — COMPLETED

- **Ausência crítica:** a verificação física registra a falta de arquivo oficial como alerta crítico persistente. O alerta não oferece aceite, dispensa ou fechamento e continua ativo mesmo quando um arquivo reaparece no caminho.
- **Restauração explícita:** somente a ação `Vincular arquivo restaurado`, pela interface do Mheibos, encerra o alerta. Nome e caminho precisam coincidir exatamente com a identidade oficial; mover ou renomear é recusado.
- **Conteúdo divergente:** o Mheibos compara SHA-256 com a última evidência disponível. Se o conteúdo restaurado divergir, exige decisão humana entre manter o estado atual ou devolver o conjunto para preparação.
- **Exceção pontual:** continuar uma transição sem o arquivo exige gerente ou administrador ativo, senha própria e justificativa. A autorização pertence somente àquela ação, mantém solicitante e autorizador distintos e não remove o alerta crítico.
- **Assistencialização:** a ausência aparece no detalhe do Pedido, na fila de Preparação de Arte e com prioridade na notificação global, sem depender de IA.
- **Auditoria:** restauração e exceção gerencial geram eventos transacionais; a exceção integra a mesma transação da mudança de estado, impedindo autorização órfã quando a operação falha.
- **Validação:** migration check, Django check, lint, type checking, tokens visuais, 46 testes focados e baseline completo de 167 testes aprovados. Matriz visual oficial sem overflow; evidências em `IMP-009K-VISUAL-VALIDATION.md`.
- **Próxima fatia:** transferência gerencial de responsabilidade e continuidade da preparação conforme DEC-IMP-033.
