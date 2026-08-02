# IMP-006C — Arte como pré-requisito da Produção

Data: 2026-08-02

Estado: COMPLETED_WITH_GAPS

## Decisão implementada

Pedido sem arte de referência ativa permanece em `AGUARDANDO_ARTE` e não pode avançar para `LIBERADO_PRODUCAO`, `EM_PRODUCAO`, `PRONTO` ou `ENTREGUE`.

A regra está no caso de uso de transição, não no template. Rotas individual, em massa e a antiga rota de Assistência usam o mesmo caso de uso auditável. A criação direta como pronto também é recusada quando nenhum arquivo de arte acompanha o Pedido.

## Continuidade e assistência disponíveis agora

- Status explícito `AGUARDANDO_ARTE`.
- Fila “Preparação de arte” independente de categoria de produto.
- Contador persistente e acesso direto para adicionar arte.
- Notificação determinística periódica já existente, agora contabilizando todo Pedido aguardando arte.
- Bloqueio de domínio que impede avanço acidental.
- Histórico e evento normais quando a transição válida acontece.

Nada depende de IA.

## Limites normativos

A entidade `Pendencia` atual exige um `Processo` formal e hoje cobre bloqueios de Processo de Produção. Criar uma Pendência de pré-produção sem antes definir o Processo/Etapa correspondente inventaria arquitetura.

Permanecem para a versão completa da RFC-0012 e para o fechamento do IMP-007:

- cadência normativa de lembretes;
- scheduler e continuidade diária;
- destinatários adicionais;
- escalonamento, criticidade e prazos automáticos;
- criação/encerramento de Pendência formal para a Etapa de arte.

A IA futura poderá priorizar, resumir e sugerir intervenções, mas nunca será responsável pelo bloqueio ou pela continuidade básica.

## Validação

- 38 testes direcionados: PASS.
- suíte integral: 144 testes em 156,875 s, PASS.
- matriz visual de Lista e Preparação de arte: 10/10 combinações sem overflow.
- conteúdo real sem arte e sem categoria: PASS.
- zoom 125%: PASS.
- IA desligada: PASS por construção determinística.

Evidências locais: `C:\Users\Ruan\Documents\Mheibos Gestor\visual-evidence\IMP-006C`.
