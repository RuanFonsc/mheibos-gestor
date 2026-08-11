# Dívida de tipagem do legado

**Data da descoberta:** 10/08/2026  
**Verificador:** mypy 1.20.2  
**Estado:** `OPEN — legado, não bloqueia os ciclos novos`

## Evidência

Após as correções incrementais de formulários, datas, projeções, CRM, payloads de sincronização, ferramentas de validação, visões de Catálogo e Financeiro, a dívida foi reduzida para 8 diagnósticos em 5 arquivos. O escopo dos ciclos recentes permanece verde: Analytics e Aprendizado (8 arquivos) passam sem erros.

## Agrupamento atual

| Área | Diagnósticos | Natureza predominante |
|---|---:|---|
| `tools/` | 0 | variáveis sem anotação e valores opcionais (corrigido neste ciclo) |
| `apps/financeiro/` | 0 | agregações e listas sem tipos explícitos (corrigido neste ciclo) |
| `apps/catalogo/` | 1 | comando de integridade textual com tipo genérico |
| `apps/pedidos/` | 5 | atributos legados/projeções e parâmetros opcionais |
| `apps/vendas/` | 0 | QuerySet/lista e projeções (corrigido neste ciclo) |
| `apps/arquivos/` | 6 | respostas monkey-patched, uniões opcionais e migration loader |
| `apps/sincronizacao/` | 0 | payloads de testes tipados como `object` (corrigido neste ciclo) |
| `apps/missoes/` | 0 | campo de formulário Django sem tipo reconhecido (corrigido neste ciclo) |
| `apps/operacao/` | 1 | atributo legado de projeção em teste |
| `apps/` (migração) | 1 | assinatura de `MigrationLoader` |

## Política

- Não mascarar esses erros com exclusões globais no `mypy.ini`.
- Corrigir por pacote quando o próximo ciclo tocar a área, começando por contratos oficiais e atributos realmente existentes.
- Reexecutar o mypy completo após cada grupo; manter o mypy de escopo como gate obrigatório para cada ciclo novo.
- Nenhum erro desta lista altera o fato de que o produto deve funcionar com a IA desligada.
