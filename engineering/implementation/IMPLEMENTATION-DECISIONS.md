# Decisões da Implementação

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
