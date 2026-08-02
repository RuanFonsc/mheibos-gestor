# Bloqueios da Implementação

Nenhum bloqueio global ativo.

## Lacunas futuras conhecidas

- RFC-0012 está reservada, mas precisa de elaboração antes de políticas detalhadas de pendências e escalonamento.
- RFC-0015 e RFC-0016 serão adicionadas posteriormente.
- Essas lacunas não bloqueiam ciclos independentes. A antecipação humana de IMP-007A autoriza somente Gateway, adaptador e leitura assistiva; não antecipa regras pertencentes às RFCs futuras.
- A exceção de entrega com saldo exige um ciclo futuro de reautenticação superior, motivo, evento e Pendência; até lá, a entrega é recusada com segurança e não bloqueia os demais fluxos.
- A chave Gemini divulgada na conversa deve ser revogada e rotacionada. A validação online aguarda uma nova chave configurada localmente; desenvolvimento, testes e operação sem IA continuam liberados.

## DECISAO_HUMANA_NECESSARIA — Política temporal da RFC-0012

- **Parte afetada:** scheduler, cadência/repetição, limiares de criticidade, briefing diário e escalonamento automático.
- **Fontes consultadas:** RFC-0012 v0.0; RFC-0005 §18; RFC-0009 §§11–14, 23–24 e 30.8; INV-085 a INV-092.
- **Lacuna:** as fontes exigem essas capacidades, mas reservam os valores, gatilhos e regras concretas para uma futura versão aprovada da RFC-0012.
- **Alternativas não escolhidas:** política fixa global; política configurável por empresa; cadência por tipo de Pendência; somente ações manuais sem scheduler.
- **Pergunta futura:** quais gatilhos, intervalos, níveis e destinatários deverão compor a primeira política temporal oficial?
- **Impacto atual:** Pendência, autoria, responsável, destinatários, vínculo e encerramento funcionam; nenhuma regra temporal foi inventada. IMP-008 e demais ciclos independentes podem avançar.
