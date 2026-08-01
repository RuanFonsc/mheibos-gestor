# RFC-0002 — Modelo Operacional do Mheibos

**Status:** Aprovado  
**Versão:** 1.0  
**Dependências:** RFC-0000, RFC-0001

## Histórico e resolução de numeração

Esta versão consolida o draft 0.1 da RFC-0002 e o conteúdo operacional que havia sido publicado, por erro de numeração, como “RFC-0012 — Modelo Operacional do Mheibos”. A RFC-0012 fica reservada exclusivamente a Pendências, Lembretes e Escalonamento, conforme o Inventário Oficial.

## Objetivo

Definir o modelo operacional que governa os processos do Mheibos e os conceitos pelos quais o sistema compreende o trabalho por meio de processos, evidências e estados.

## Princípios

- As pessoas executam o trabalho; o Mheibos o compreende e orienta.
- Estados surgem de evidências e regras, não de cliques isolados.
- O sistema deve guiar em vez de punir; bloqueios são o último recurso.
- A IA é opcional, auxilia interpretação e explicação, mas nunca é fonte da verdade.
- O próprio Mheibos deve seguir seu modelo operacional.

## Processo Operacional

Processo Operacional é uma atividade organizada que altera o estado da empresa e possui objetivo, fluxo, responsáveis, estados e resultado esperado. Consultas e navegação não são processos. Os tipos de processo são nativos do sistema; usuários não criam novos tipos.

Grupos oficiais incluem Comercial e Pedidos; Produção; Entrega e Logística; Financeiro; CRM e Cadastros; Estoque, Materiais e Compras; Usuários e Organização Interna; e Correções, Retrabalho, Cancelamentos e Exceções.

Processos podem iniciar processos filhos autônomos, permanentemente vinculados à origem.

## Conceitos operacionais

- **Objetivo:** resultado que justifica a existência do processo.
- **Fluxo:** sequência esperada de evolução.
- **Estado Operacional:** situação atual conhecida.
- **Evidência Operacional:** fato objetivo observado, como arquivo criado, PDF exportado, resposta recebida ou pagamento confirmado.
- **Observação Passiva:** percepção por sistema interno, Desktop Agent, integrações ou passagem do tempo.
- **Motor de Evidências:** interpreta evidências e propõe transições.
- **Motor de Regras:** valida transições, permissões e bloqueios e é a autoridade determinística.

## Prazos, alertas e responsabilidade

Nem todo processo possui prazo. Quando existir, ele representa compromisso; apenas gerentes e administradores podem alterá-lo, sempre com auditoria. Atrasos não podem ser mascarados por extensão automática.

A prioridade de exibição dos alertas é dinâmica, sem alterar a prioridade do processo. Usuários comuns não descartam alertas críticos; uma decisão gerencial de ignorá-los deve ser registrada.

A responsabilidade é registrada por etapa. Quando um gerente autoriza uma exceção, assume a responsabilidade pela decisão.

## Quebra de fluxo

Usuários comuns não pulam etapas. Exceções críticas exigem autenticação gerencial, inclusive remota quando prevista. A autorização deve registrar se a etapa foi dispensada definitivamente ou adiada para regularização. Processos bloqueados continuam bloqueados até resolução explícita.

## IA desligada primeiro

Na fase atual não será instalado modelo de IA local nem integração com IA por API. Toda função operacional, persistência, regra, evidência, auditoria e interface essencial deve funcionar integralmente com a IA desligada.

A futura camada cognitiva poderá interpretar contexto, explicar situações e sugerir ações por uma interface substituível. Ela não poderá alterar diretamente estados oficiais, executar decisões gerenciais ou financeiras, nem se tornar dependência para o funcionamento determinístico.

## Encerramento

O fechamento valida pendências, consolida indicadores, atualiza métricas e registra auditoria. Alimentar memória cognitiva é opcional e somente ocorrerá quando essa capacidade futura estiver habilitada.

Estados finais possíveis incluem Concluído, Cancelado, Inviabilizado, Abandonado e Substituído. Todo encerramento preserva histórico, evidências e responsáveis.

## Limites

Detalhes técnicos pertencem às RFCs de arquitetura. Cadência, scheduler, notificações, lembretes e escalonamento pertencem exclusivamente à RFC-0012.
