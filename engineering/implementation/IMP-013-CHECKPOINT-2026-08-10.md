# Checkpoint IMP-013 — Governança da IA

**Data:** 10/08/2026  
**Estado:** `PENDING`  
**Fonte:** RFC-0016 Draft 0.1  
**Dependências:** IMP-002, IMP-003, IMP-011  

## Ponto de partida

- A RFC-0016 foi preservada em `docs/RFC-0016-Governanca-da-IA-Autonomia-e-Autoridade-Humana.md`.
- O impacto foi registrado em `engineering/implementation/IMP-013-IMPACT-ASSESSMENT.md`.
- IMP-012 funciona com IA desligada e não delega autoridade a nenhum modelo.
- A camada de conhecimento e memória continua independente da IA.

## Decisões que já vinculam o próximo ciclo

- Automações determinísticas e IA cognitiva permanecem fronteiras distintas.
- Ausência de autoridade humana nunca concede autoridade extraordinária à IA.
- Ações autônomas futuras deverão ser reversíveis, planejadas, explicáveis e auditáveis.
- Confiança insuficiente deve converter execução autônoma em proposta humana.
- Feedback não altera políticas ou permissões automaticamente.

## Bloqueio normativo explícito

A RFC-0016 exige o documento futuro **Modelo de Decisões Autônomas da IA**, que deverá definir o catálogo de ações, limites, confiança mínima, autoridades, janelas de execução, reversão e recuperação. Até esse documento existir e a RFC ser aprovada, não será implementada autonomia nem serão inventados contratos equivalentes.

## Gates de entrada

- [ ] RFC-0016 aprovada como fonte normativa.
- [ ] Modelo de Decisões Autônomas da IA recebido e versionado.
- [ ] Catálogo de ações e limites revisado contra RFC-0000 a RFC-0016.
- [ ] Contratos de autoridade, reversão e auditoria definidos.
- [ ] Testes determinísticos e de IA desligada preservados.

O funcionamento operacional atual não depende desses gates; eles condicionam somente a futura autonomia cognitiva.
