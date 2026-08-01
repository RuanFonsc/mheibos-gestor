# MHEIBOS INTELLIGENT OPERATING SYSTEM

# RFC-0013 --- Modelo Comercial e Financeiro

**Status:** Draft para aprovação\
**Versão:** 0.1\
**Data:** 31/07/2026\
**Dependências:** RFC-0000 a RFC-0012

------------------------------------------------------------------------

# 1. Resumo

Esta RFC define o modelo comercial e financeiro do Mheibos,
estabelecendo as regras para pedidos, orçamentos, pagamentos, alterações
de valores, descontos, cancelamentos, inadimplência, metas comerciais e
princípios de segurança financeira.

O objetivo é garantir que toda movimentação comercial seja rastreável,
auditável e consistente, priorizando sempre a integridade dos dados
acima da agilidade operacional.

------------------------------------------------------------------------

# 2. Decisões Fundamentais

1.  O RFC-0013 concentra todas as regras comerciais e financeiras da
    plataforma.
2.  Todo pedido nasce imediatamente como rascunho e evolui por estados.
3.  O orçamento é convertido no próprio pedido, preservando sua
    identidade.
4.  O registro recebe UUID desde o nascimento, mas a numeração comercial
    somente após a confirmação do pedido.
5.  Pedidos podem ser alterados durante todo o ciclo de vida, com
    auditoria completa.
6.  O histórico é baseado em deltas, permitindo reconstrução de qualquer
    versão.
7.  Alterações financeiras preservam pagamentos existentes e exigem
    autorizações quando aplicável.
8.  Acréscimos após pagamento confirmado geram nova pendência;
    devoluções e estornos dependem de autorização gerencial.
9.  Todo desconto exige autorização de gerente.
10. Todo aumento de preço exige autorização de gerente.
11. Remoção de itens é permitida apenas antes da confirmação/início da
    produção.
12. Cancelamentos nunca apagam pedidos e sempre exigem autorização
    gerencial.
13. A produção inicia imediatamente após a confirmação do pedido.
14. A política de entrada é configurável pela empresa; exceções exigem
    gerente.
15. O Mheibos registra pagamentos informados pelo usuário, sem
    conciliação bancária.
16. Comprovantes são opcionais, porém fortemente recomendados quando
    aplicável.
17. A IA orienta o correto preenchimento das informações financeiras.
18. Inadimplência gera alertas progressivos e pode exigir autorização de
    gerente para novas vendas.
19. A meta comercial é contabilizada no primeiro pagamento confirmado.
20. A meta é contabilizada integralmente nesse primeiro pagamento.
21. Cada pedido possui um único vendedor responsável.
22. Reabertura de pedido finalizado exige gerente e justificativa.
23. Nenhum pedido pode ser excluído fisicamente.
24. A numeração comercial nunca é reutilizada.
25. Cadastro de clientes é independente da criação de pedidos.
26. O sistema sugere clientes existentes e atualiza automaticamente
    novos dados informados.
27. Possíveis clientes duplicados somente podem ser unificados mediante
    autorização de gerente.
28. O histórico comercial é exibido somente mediante solicitação do
    usuário, com análise cognitiva da IA.
29. A IA permanece passiva durante o preenchimento, atuando como
    copiloto apenas quando solicitada ou em exceções previstas.
30. A IA sugere geração de documentos, mas nunca os gera automaticamente
    sem confirmação.
31. Um pedido somente é concluído quando estiver entregue e totalmente
    quitado.
32. Em qualquer conflito, prevalecem segurança, rastreabilidade e
    auditoria.

------------------------------------------------------------------------

# 3. Princípio Arquitetural

O Mheibos registra a realidade operacional informada pelos usuários e
preserva integralmente sua rastreabilidade. A IA atua como assistente e
copiloto, jamais como autoridade comercial ou financeira.

Toda operação relevante deve ser auditável, reversível quando permitido
e vinculada à identidade do responsável.

------------------------------------------------------------------------

# 4. Critérios de Conformidade

Uma implementação somente estará conforme esta RFC se:

-   nunca excluir pedidos fisicamente;
-   preservar histórico integral;
-   impedir descontos sem gerente;
-   impedir aumentos de preço sem gerente;
-   registrar todas as alterações financeiras;
-   preservar UUID e numeração comercial;
-   manter autoria comercial única;
-   impedir reutilização da numeração;
-   respeitar o modelo de permissões;
-   priorizar segurança sobre conveniência.

------------------------------------------------------------------------

**Fim da RFC-0013**
