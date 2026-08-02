# Análise de impacto — RFC-0015

**Data:** 02/08/2026  
**Estado da fonte:** APROVADA  
**SHA-256 da origem recebida:** `58192A7B3A21176B0C7BEAC3C57CEE4EBD0BB1F6A05FD2B9C6E407DBBC07BC9C`

## Responsabilidade exclusiva

A RFC-0015 governa a camada gerencial formada por Dashboard, Analytics e Simulação. Ela não redefine Pedido, Processo, Etapa, Pendência, Missão, Conhecimento, autorização ou auditoria: consome esses contratos e projeta seus dados conforme as RFCs proprietárias.

## Invariantes extraídos

- Dashboard mostra o presente e abre na visão individual.
- Analytics explica presente e passado com evidências, confiança e separação entre fato, correlação, inferência e hipótese.
- Simulação projeta o futuro somente com dados internos suficientes e autorização válida.
- Simulação salva tem validade dinâmica; execução real não nasce diretamente dela, mas pode ser promovida a Missão.
- A IA apoia análise e adaptação, sem substituir dados oficiais, autorização ou decisão humana.
- A ausência de IA não bloqueia o Dashboard, métricas determinísticas, relatórios, evidências ou simulações matemáticas autorizadas.

## Estado atual e classificação

| Área atual | Classificação | Impacto |
|---|---|---|
| `apps/financeiro` como Dashboard principal | reprojetar | A tela atual é predominantemente financeira e não cumpre o centro de comando individual e modular. |
| Dashboard separado do antigo Mheibos Vendas | descontinuar | A duplicação contraria a aplicação integrada e a convergência já decidida. |
| Dados de metas, CRM e relatórios existentes | adaptar | Podem alimentar widgets, mas não definir sozinhos a arquitetura do Dashboard. |
| Widget flutuante e preferências atuais | compatibilidade temporária | Reaproveitar apenas contratos úteis; sobreposição Windows não é o Dashboard oficial web. |
| Fila de atenção e intervenções | adaptar | Deve consumir Pendências, criticidade e Etapas sem recalcular autoridade na interface. |
| Analytics explicável e evidências | adicionar | Requer entidades/contratos próprios para análise, evidência, confiança, previsão e resultado. |
| Simulação salva e comparação | adicionar | Requer domínio próprio, autorização, validade e promoção auditada para Missão. |
| Análise por IA e Modo Inteligente | adicionar na fase final de IA | Preparar contratos e fallback; não tornar o Dashboard dependente do modelo. |

## Dependências e sequência

1. Concluir IMP-009 para não deixar regras críticas de arte pela metade.
2. Concluir IMP-010, pois a RFC-0015 promove cenários para Missão e exibe Missões no Dashboard.
3. Implementar IMP-011, pois previsão, decisão e resultado alimentam Conhecimento e Aprendizado.
4. Executar IMP-012 em fatias: domínio/evidências; Dashboard determinístico; Analytics determinístico; Simulação; integração com Missões; interface; pontos cognitivos desligáveis.
5. Integrar análise cognitiva, linguagem natural e reorganização automática somente após a RFC-0016 e na fase final de IA.

## Conclusão

A RFC-0015 muda substancialmente o futuro Dashboard, mas não justifica interromper a IMP-009. Implementar agora uma reforma visual completa criaria retrabalho porque Missões e Conhecimento ainda são dependências incompletas. A ação correta agora é oficializar a RFC, atualizar o backlog e preservar a sequência normativa.
