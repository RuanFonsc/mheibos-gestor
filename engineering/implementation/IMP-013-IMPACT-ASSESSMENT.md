# Impacto da RFC-0016 — Governança da IA

**Data:** 10/08/2026  
**Fonte:** RFC-0016-Governanca-da-IA-Autonomia-e-Autoridade-Humana.md  
**Estado da fonte:** Draft 0.1; recebido e preservado, ainda sujeito a aprovação.  
**Responsabilidade:** orientar o IMP-013 e a futura camada cognitiva; não autoriza executar autonomia de IA agora.

## Decisões que já vinculam a implementação

- IA cognitiva e automações determinísticas são fronteiras distintas.
- Desligar a IA não pode desligar segurança, integridade, auditoria, sincronização ou outras invariantes determinísticas.
- Nenhuma ação autônoma pode ser irreversível, iniciar sem planejamento ou ultrapassar permissões.
- Ausência de autoridade não concede autoridade extraordinária à IA; urgência aumenta intervenção, não autoridade.
- Confiança insuficiente converte uma ação elegível em proposta humana.
- Toda decisão autônoma futura deverá registrar contexto, evidências, política, confiança, planejamento, execução, resultado e recuperação.
- Reversão e restauração de autonomia são humanas; restauração exige o mesmo nível de autoridade da reversão.
- Feedback, frequência e aprendizado não alteram política ou permissões automaticamente.

## Impacto nos ciclos atuais

| Ciclo | Tratamento |
|---|---|
| IMP-011 | Conhecimento e memória permanecem independentes da IA; aprovação humana continua obrigatória. |
| IMP-012 | Analytics e simulação determinísticos podem criar evidências, análises e Missões, mas não são decisões autônomas da IA. |
| IMP-013 | Deve definir catálogo de ações autônomas, políticas, planejamento, reversão, escalonamento, janelas, recursos e auditoria permanente. |
| IMP-014 | Só poderá conectar modelos e autonomia depois dos contratos de governança; IA desligada continua sendo caminho válido. |

## Lacunas formais preservadas

A própria RFC determina um documento futuro obrigatório, o **Modelo de Decisões Autônomas da IA**, que deverá detalhar cada ação. Enquanto ele não existir e a RFC-0016 não estiver aprovada, nenhum agente deve inventar catálogo, confiança mínima, autoridade de reversão ou janela autônoma.

## Gate de continuidade

O Dashboard do IMP-012 pode prosseguir com dados oficiais e regras determinísticas. A RFC-0016 não bloqueia o funcionamento do Mheibos; ela impede apenas que uma integração cognitiva futura seja tratada como autoridade sem governança.
