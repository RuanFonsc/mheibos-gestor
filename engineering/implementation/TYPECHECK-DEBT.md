# Dívida de tipagem do legado

**Data da descoberta:** 10/08/2026  
**Verificador:** mypy 1.20.2  
**Estado:** `OPEN — legado, não bloqueia os ciclos novos`

## Evidência

Após as correções incrementais de formulários e datas, a dívida foi reduzida para 39 diagnósticos em 14 arquivos. O escopo dos ciclos recentes permanece verde: Analytics e Aprendizado (8 arquivos) passam sem erros.

## Agrupamento atual

| Área | Diagnósticos | Natureza predominante |
|---|---:|---|
| `tools/` | 4 | variáveis sem anotação e valores opcionais |
| `apps/financeiro/` | 13 | CRM, agregações e listas sem tipos explícitos |
| `apps/catalogo/` | 5 | comandos, QuerySets e atributos legados |
| `apps/pedidos/` | 5 | atributos legados/projeções e parâmetros opcionais |
| `apps/vendas/` | 3 | parâmetros opcionais, QuerySet/lista e projeções |
| `apps/arquivos/` | 5 | respostas monkey-patched e uniões opcionais |
| `apps/sincronizacao/` | 2 | payloads de testes tipados como `object` |
| `apps/missoes/` | 0 | campo de formulário Django sem tipo reconhecido (corrigido neste ciclo) |
| `apps/operacao/` | 1 | atributo legado de projeção em teste |
| `apps/` (migração) | 1 | assinatura de `MigrationLoader` |

## Política

- Não mascarar esses erros com exclusões globais no `mypy.ini`.
- Corrigir por pacote quando o próximo ciclo tocar a área, começando por contratos oficiais e atributos realmente existentes.
- Reexecutar o mypy completo após cada grupo; manter o mypy de escopo como gate obrigatório para cada ciclo novo.
- Nenhum erro desta lista altera o fato de que o produto deve funcionar com a IA desligada.
