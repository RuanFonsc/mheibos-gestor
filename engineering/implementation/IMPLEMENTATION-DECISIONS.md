# Decisões da Implementação

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
