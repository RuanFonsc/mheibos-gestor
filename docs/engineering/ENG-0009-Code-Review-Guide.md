# ENG-0009 — Code Review Guide

**Status:** COMPLETED_WITH_GAPS  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Responsabilidade exclusiva:** padronizar revisão de código, migrations, testes e contratos do Mheibos.  
**Dependências:** ENG-0004 e ENG-0008.

---

## 1. Objetivo da revisão

Encontrar defeitos concretos que afetem correção, arquitetura, segurança, dados, operação, manutenção ou experiência. Revisão não é preferência estilística nem oportunidade de redesenhar escopo sem evidência.

## 2. Preparação

Revisor deve:

- ler solicitação e critérios;
- identificar fontes normativas;
- conferir classificação/plano;
- inspecionar status e diff;
- separar mudanças do autor de alterações preexistentes;
- localizar testes e migrations;
- aplicar ENG-0008.

## 3. Ordem de inspeção

1. invariantes normativas;
2. dados/migrations;
3. autorização e ações sensíveis;
4. domínio/casos de uso;
5. eventos/auditoria;
6. contratos/integrações;
7. concorrência/idempotência;
8. interface/UX;
9. IA;
10. testes;
11. documentação e rollout.

Essa ordem prioriza riscos irreversíveis.

## 4. Severidade

- **P0 — Crítico:** perda/corrupção ampla, segredo exposto, autorização crítica contornável, sistema indisponível.
- **P1 — Alto:** regra normativa violada, dado financeiro incorreto, migration destrutiva, privilégio indevido, fluxo principal quebrado.
- **P2 — Médio:** comportamento incorreto em caso válido, auditoria incompleta, falha recuperável, regressão relevante.
- **P3 — Baixo:** problema localizado com impacto real limitado.

Não elevar preferência, hipótese ou melhoria opcional a defeito.

## 5. Forma de um finding

Um finding deve conter:

- título com severidade;
- arquivo e intervalo mínimo;
- cenário de reprodução;
- comportamento atual;
- comportamento esperado;
- impacto;
- fonte normativa ou evidência técnica;
- correção orientativa sem exigir reescrita desnecessária.

Comentário deve ser autossuficiente e verificável.

## 6. Domínio e aplicação

Verificar:

- regra duplicada em View/Form/template;
- transição sem Processo/Etapa;
- status genérico sobrecarregado;
- caso de uso bypassado;
- autoria/responsabilidade sobrescrita;
- validação somente no cliente;
- cálculo oficial duplicado;
- operação parcial sem transação/compensação.

## 7. Dados e migrations

Inspecionar arquivo de migration, não apenas model.

Buscar:

- coluna obrigatória sem backfill;
- default que inventa histórico;
- remoção antes de migrar leitores;
- conversão ambígua;
- perda de precisão monetária;
- ID reutilizado;
- constraint incompatível com dados existentes;
- operação não idempotente;
- rollback impossível sem registro;
- dual-write divergente.

Exigir evidência por contagens, consultas, testes ou plano.

## 8. Segurança

Verificar autorização no servidor/caso de uso, inclusive acesso direto a URL/API. Testar permitido e negado.

Buscar:

- botão oculto como única proteção;
- objeto acessado sem escopo;
- ação sensível sem reautenticação/motivo;
- IA ou webhook com privilégio implícito;
- sessão/offline ampliando autoridade;
- segredo em código/log;
- auditoria sem ator/origem.

## 9. Eventos e auditoria

Confirmar que o evento ocorre na mesma unidade lógica do fato principal ou possui mecanismo confiável de entrega. Falha secundária não pode apagar o principal.

Buscar evento duplicado, ausência de correlação, reprocessamento não idempotente, correção destrutiva de auditoria e log textual usado como histórico de negócio.

## 10. Offline e concorrência

Revisar:

- origem/estação;
- versão/conflito;
- idempotency key;
- retry;
- ordenação;
- bloqueio com expiração;
- operações concorrentes;
- transação e isolamento;
- estado local apresentado como global.

## 11. IA

Reprovar:

- modelo decidindo permissão/transição;
- prompt como única regra;
- acesso direto a banco/widget;
- saída persistida sem schema/validação;
- contexto sem permissão;
- hipótese apresentada como fato;
- conhecimento apenas no modelo;
- indisponibilidade bloqueando função essencial.

## 12. Interface

Revisar fluxo completo, não somente aparência:

- ação chama contrato correto;
- feedback de sucesso/erro;
- loading/duplo envio;
- acessibilidade;
- estado vazio;
- responsividade desktop;
- informação crítica por múltiplos canais;
- restauração de adaptação;
- consistência sem chat.

## 13. Integrações

Verificar timeouts, retry, idempotência, assinatura/autenticação, isolamento de falha e preservação de payload necessário à auditoria.

Fornecedor terceirizado não recebe automação de correlação de mensagens. Remoção de referência não apaga arquivo externo.

## 14. Testes

Teste deve falhar sem a correção e cobrir risco, não implementação incidental.

Exigir conforme aplicável:

- happy path;
- autorização negada;
- limite/erro;
- migration com dado legado;
- evento/auditoria;
- idempotência;
- integração indisponível;
- IA indisponível/saída inválida;
- regressão.

Teste legado incompatível com RFC deve ser corrigido junto à regra, com rastreabilidade.

## 15. Performance e operabilidade

Investigar somente com caminho plausível:

- N+1 em listas;
- consulta sem índice crítico;
- carga síncrona pesada;
- fila sem limite;
- log sensível/ruidoso;
- falha sem diagnóstico;
- build/implantação incompatível.

## 16. Decisão da revisão

- **Approve:** nenhum finding bloqueante e gates aplicáveis passam.
- **Request changes:** existe P0/P1/P2 que viola critério ou risco.
- **Comment:** dúvida/melhoria não bloqueante.
- **Blocked:** fonte ou decisão normativa indispensável ausente.

Revisor não resolve conflito de RFC por opinião.

## 17. Evidências de encerramento

Antes de aprovar:

- findings respondidos/corrigidos;
- testes executados;
- migrations verificadas;
- diff final inspecionado;
- documentação atualizada;
- gaps declarados;
- ENG-0008 preenchido;
- rollout/rollback claros.

## 18. Lacunas

Enquanto lint/type checking não existirem, revisão manual não pode ser descrita como substituto equivalente. Drafts e RFCs ausentes continuam limitando aprovação de mudanças normativas afetadas.

## 19. Relatório de validação

| Gate | Resultado |
|---|---|
| Fonte Normativa | APROVADO COM LACUNAS |
| Arquitetura | APROVADO |
| Domínio | APROVADO |
| Dados | APROVADO |
| Eventos/Auditoria | APROVADO |
| Segurança | APROVADO |
| IA | APROVADO |
| UX | APROVADO |
| Código | APROVADO |
| Testes | APROVADO COM GAP-ENG-0004-001 |
| Documentação | APROVADO |
| Revisão Final | APROVADO COM LACUNAS |

**Resultado:** `COMPLETED_WITH_GAPS`.
