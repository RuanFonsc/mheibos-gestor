# Decisões da Implementação

## DEC-IMP-012 — Segredos locais sob proteção do sistema operacional

- **Decisão:** credenciais persistentes do Cliente usam `safeStorage` do Electron/Windows; JSON local contém somente Base64 do conteúdo cifrado.
- **Falha segura:** se o cofre do sistema não estiver disponível, o setup não persiste a configuração e explica a falha.
- **Abrangência:** segredo da Estação e senha PostgreSQL existente seguem o mesmo contrato; nenhuma compatibilidade mantém nova gravação em texto.
- **Provisionamento:** administrador reautenticado cria Estação na Central; o segredo é revelado uma vez e a Central conserva apenas hash verificável.
- **Migração:** campos legados legíveis são aceitos apenas em memória para conversão imediata e removidos ao regravar.
- **Limite:** segredo decifrado pode existir somente em memória durante a execução/autenticação do processo local; não entra em logs, eventos, argumentos de linha de comando ou documentação.
- **Situação:** definitiva para armazenamento; rotação e revogação visual entram após o primeiro fluxo conectado.

## DEC-IMP-011 — Transporte central autenticado por Estação

- **Decisão:** a incorporação HTTP usa UUID público da Estação e segredo Bearer de alta entropia, persistido na Central somente por hash do Django.
- **Motivo:** sessão web do usuário não é prova suficiente da origem técnica offline; Estação e autoria humana precisam permanecer identidades separadas.
- **Limite:** o segredo não será colocado no `.env` definitivo do Cliente. IMP-008C deve usar armazenamento protegido do sistema operacional antes de habilitar envio real.
- **Validação:** Estação ativa, correspondência com envelope, checksum, schema, código permanente da autoria e idempotência são verificados antes de persistir.
- **Resposta:** confirmação expõe somente código, ID global e UUID offline; não devolve payload ou segredo.
- **Situação:** definitiva para a fronteira central; rotação, expiração e interface de provisionamento serão ampliadas sem alterar o envelope causal.

## DEC-IMP-010 — Um backend executável em papéis separados, sem banco compartilhado offline

- **Decisão:** reutilizar casos de uso e schema do backend nos papéis `central` e `client_offline`, mantendo processos e bancos fisicamente separados por execução.
- **Motivo:** o Electron já empacota o backend; iniciar um serviço local reduz duplicação de regras sem transformar indisponibilidade da Central em indisponibilidade do Cliente.
- **Proibição preservada:** o Cliente nunca acessa diretamente o banco central e não considera uma tabela central como fila local.
- **Identidade:** Pedido local usa UUID próprio; código visível combina código permanente da pessoa e sequência durável da Estação. PK de banco local não participa da identidade entre nós.
- **Fila:** unidade causal é imutável; apenas estado de envio, tentativas e falhas evoluem. Nenhuma remoção comum é permitida.
- **Incorporação:** a Central aceita unidade completa em transação, preserva autoria/origem e reconhece reenvios pela chave idempotente.
- **Compatibilidade:** `MHEIBOS_RUNTIME_ROLE=central` é o default e não altera o funcionamento existente.
- **Situação:** definitiva para a fronteira; SQLite local, transporte e política exata de retentativa permanecem decisões técnicas das próximas fatias.

## DEC-IMP-009 — Fundação cognitiva antecipada, opcional e sem autoridade

- **Decisão humana:** em 01/08/2026, foi autorizada a entrada antecipada de IA por API, com retomada posterior do IMP-008.
- **Interpretação:** antecipar somente Gateway substituível, adaptador e um uso assistivo de leitura; não declarar concluídas a arquitetura cognitiva, analytics ou governança dependentes das RFCs 0015/0016 futuras.
- **Fontes preservadas:** RFC-0003 §10.9; RFC-0004; RFC-0006; RFC-0011. Nenhuma RFC foi alterada silenciosamente.
- **Provider:** Gemini fica atrás do Gateway; modelo e provider são configuração, não regra de domínio.
- **Falha segura:** IA desligada, sem chave ou indisponível produz fallback determinístico; processos oficiais continuam sem degradação de autoridade.
- **Dados:** o primeiro uso envia apenas ID técnico e projeção de estados; exclui dados pessoais, financeiros, texto livre e arquivos.
- **Autoridade:** resultado não persiste fatos, não autoriza transições e não substitui decisão humana ou regra determinística.
- **Segredo:** chave somente em variável de ambiente; nunca em código, documentação, teste, evento ou log.
- **Situação:** definitiva para a fronteira e regra de não bloqueio; capacidades cognitivas ampliadas permanecem futuras.

## DEC-IMP-008 — Pendência estrutural sem política temporal presumida

- **Decisão:** implementar a entidade Pendência e integrar bloqueios de Processo, mantendo scheduler, cadência, criticidade automática e escalonamento fora do código até aprovação da RFC-0012.
- **Motivo:** RFC-0005 e Inventário fecham estrutura e invariantes, enquanto RFC-0012 v0.0 proíbe inventar as escolhas temporais.
- **Fontes:** RFC-0005 §18; RFC-0009 §§10–14 e 30.8; INV-085 a INV-092; RFC-0012 v0.0.
- **Fluxo:** bloqueio cria uma Pendência idempotente; retomada/conclusão resolve; cancelamento autorizado encerra; eventos preservam autoria e forma.
- **Responsabilidade:** responsável da Etapa permanece responsável principal; destinatários adicionais não transferem automaticamente responsabilidade.
- **Interface:** lista textual não bloqueante, acessível pelo módulo normal; usuário comum vê apenas itens próprios/destinados, administrador vê o conjunto autorizado.
- **Situação:** definitiva para estrutura; política temporal é `DECISAO_HUMANA_NECESSARIA` registrada em Blockers.

## DEC-IMP-007 — Processo prevalece na projeção operacional

- **Decisão:** todas as interfaces consomem `ProjecaoPedido`; quando existe Processo formal, seu estado é oficial, e `Pedido.status` só serve de fallback marcado para legado.
- **Motivo:** elimina interpretações concorrentes sem apagar pedidos antigos nem exigir backfill especulativo.
- **Fontes:** RFC-0003 §§9 e 12.6; RFC-0005 §§3.1, 12 e 16; RFC-0009 §§5–7 e 30; ENG-0006 §9.
- **Abrangência:** lista e detalhe do Gestor, fila de Produção, Vendas, dashboard individual e relatório comercial.
- **Autorização:** a projeção é somente leitura e não amplia acesso; cada view preserva seu recorte e identidade atuais.
- **Compatibilidade:** pedidos sem Processo mostram a fonte `Compatibilidade legada`; a condição de remoção é a migração explícita dos fluxos proprietários.
- **Falhas:** nenhuma IA ou integração participa da projeção; ausência dessas camadas não afeta navegação nem operação.
- **Situação:** definitiva para precedência e contrato; formatos visuais poderão evoluir.

## DEC-IMP-006 — Piloto aditivo de Processo de Produção

- **Decisão:** instanciar um Processo nativo `PRODUCAO_PEDIDO`, com snapshot do Modelo de Fluxo versão 1 e Etapa `PRODUZIR`, nas novas transições para produção.
- **Motivo:** transforma uma operação real existente no primeiro corte observável de Processo/Etapa sem inferir processos históricos nem copiar responsabilidades financeiras do Pedido.
- **Fontes:** RFC-0002 §§Processo Operacional, Conceitos e Quebra de Fluxo; RFC-0005 §§12–16 e 27; RFC-0006 §§7, 11 e 13; ENG-0006 §8.
- **Migração:** schema exclusivamente aditivo e sem backfill; Pedidos antigos continuam legíveis e recebem Processo somente numa nova transição explícita.
- **Histórico:** Modelo de Fluxo usado torna-se imutável; nova definição exige nova versão, enquanto Processo preserva código e versão em snapshot.
- **Transições:** entrar em produção inicia; pronto conclui; rejeição bloqueia com motivo; retomada desbloqueia; cancelamento cancela; processo final não reabre pelo status legado.
- **Auditoria:** `ProcessoConfirmado`, `EtapaConcluida`, `ProcessoBloqueado`, `ProcessoDesbloqueado` e `ProcessoCancelado` compartilham a transação da mudança.
- **Compatibilidade:** `Pedido.status` ainda dispara o piloto até as projeções consumirem Processo/Etapa no IMP-006.
- **Situação:** piloto definitivo como fronteira; catálogo completo de fluxos, dependências e evidências entra em ciclos posteriores.

## DEC-IMP-005 — Estados registrados e derivados do Pedido

- **Decisão:** persistir estado comercial e estado de entrega; derivar o estado financeiro do total e dos pagamentos confirmados.
- **Motivo:** mantém as dimensões independentes sem criar uma segunda fonte da verdade financeira.
- **Fontes:** RFC-0005 §§10, 16, 17 e 26; RFC-0013 §2; INV-096 a INV-099; ENG-0006 §7.
- **Compatibilidade:** `Pedido.status` permanece temporariamente como projeção operacional legada até Processo/Etapa no IMP-005.
- **Migração:** cancelado, pronto e entregue são mapeados; entregue somente vira comercialmente concluído quando os pagamentos comprovam quitação.
- **Segurança:** entrega com saldo é recusada até existir autorização superior com reautenticação, motivo, auditoria e pendência.
- **Reversibilidade:** campos são aditivos; o backfill não altera nem exclui o status legado.
- **Situação:** definitiva para a separação; vocabulário poderá ser ampliado somente por fonte normativa.

## DEC-IMP-004 — Evento aditivo na mesma transação do caso de uso

- **Decisão:** persistir o evento oficial na mesma transação da mudança primária; consequências secundárias serão desacopladas posteriormente.
- **Motivo:** impede estado alterado sem auditoria e entrega valor funcional antes de escolher barramento ou outbox.
- **Fontes:** RFC-0006 §§6, 13, 17, 18 e 23.
- **Alternativas rejeitadas:** log técnico; sinal Django implícito; infraestrutura assíncrona sem consumidor.
- **Impacto:** falha ao registrar o evento reverte a transição.
- **Migração:** tabela exclusivamente aditiva; não converter histórico antigo por inferência.
- **Reversibilidade:** migration reversível enquanto não houver consumidores externos.
- **Situação:** definitiva para atomicidade; transporte secundário permanece substituível.

## DEC-IMP-002 — Migração oportunista de senhas legadas

- **Decisão:** senhas novas usam o hasher do Django; credenciais antigas em texto são aceitas uma única vez e convertidas somente após validação correta.
- **Motivo:** remove texto legível sem exigir conhecimento da senha original e sem bloquear usuários existentes.
- **Fontes:** RFC-0007 §§5.2, 6.1–6.4; INV-030; ENG-0007.
- **Alternativas rejeitadas:** manter texto até migração manual; invalidar todas as senhas; tentar hash em migration sem distinguir valores já protegidos.
- **Impacto funcional:** login permanece compatível; senha inválida nunca provoca conversão.
- **Migração:** gradual, sem inferência e sem reversão para texto legível.
- **Reversibilidade:** código reversível; hashes produzidos não devem ser revertidos.
- **Situação:** definitiva. Compatibilidade com texto legado será removida quando auditoria confirmar ausência desses valores.

## DEC-IMP-003 — Sessão usa identificador técnico

- **Decisão:** `operador_id` é a identidade da sessão; `operador_nome` permanece somente como compatibilidade e apresentação.
- **Motivo:** nome pode mudar e não é identidade estável.
- **Fontes:** RFC-0005 §§6.1, 6.3, 8.1 e 8.3; RFC-0007 §§5.1 e 5.6.
- **Alternativas rejeitadas:** continuar por nome; introduzir imediatamente um segundo modelo de usuário paralelo.
- **Impacto funcional:** renomear usuário não encerra a sessão.
- **Migração:** sessões antigas são promovidas ao serem resolvidas.
- **Reversibilidade:** compatibilidade por nome permite rollback temporário.
- **Situação:** definitiva para identidade técnica; remoção da chave legada será feita após estabilização.

## DEC-IMP-001 — Primeiro corte pelo fluxo de mudança de status

- **Decisão:** migrar primeiro mudanças de status para um caso de uso transacional, preservando a interface atual.
- **Motivo:** é uma operação crítica, duplicada e atualmente nem sempre auditada; cria fronteira utilizável para autorização e eventos posteriores.
- **Fontes:** ENG-0006 §§3–6; RFC-0006 §§5–9; RFC-0007.
- **Alternativas rejeitadas:** criar infraestrutura genérica de eventos sem consumidor; redesenhar telas antes do domínio.
- **Impacto funcional:** mesma ação visível, agora com regra única e histórico.
- **Migração:** novo vínculo opcional de autoria; históricos antigos permanecem sem autoria inferida.
- **Reversibilidade:** migration reversível; views podem ser restauradas pelo Git.
- **Situação:** definitiva para a fronteira do caso de uso; histórico atual é compatibilidade temporária até o evento oficial.
