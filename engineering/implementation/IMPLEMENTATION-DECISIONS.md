# Decisões da Implementação

## DEC-IMP-001 — Primeiro corte pelo fluxo de mudança de status

- **Decisão:** migrar primeiro mudanças de status para um caso de uso transacional, preservando a interface atual.
- **Motivo:** é uma operação crítica, duplicada e atualmente nem sempre auditada; cria fronteira utilizável para autorização e eventos posteriores.
- **Fontes:** ENG-0006 §§3–6; RFC-0006 §§5–9; RFC-0007.
- **Alternativas rejeitadas:** criar infraestrutura genérica de eventos sem consumidor; redesenhar telas antes do domínio.
- **Impacto funcional:** mesma ação visível, agora com regra única e histórico.
- **Migração:** novo vínculo opcional de autoria; históricos antigos permanecem sem autoria inferida.
- **Reversibilidade:** migration reversível; views podem ser restauradas pelo Git.
- **Situação:** definitiva para a fronteira do caso de uso; histórico atual é compatibilidade temporária até o evento oficial.
