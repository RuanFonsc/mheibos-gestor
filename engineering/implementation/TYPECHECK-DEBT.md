# Dívida de tipagem do legado

**Data da descoberta:** 10/08/2026  
**Verificador:** mypy 1.20.2  
**Estado:** `CLOSED`

## Evidência

Após as correções incrementais de formulários, datas, projeções, CRM, payloads de sincronização, ferramentas de validação, visões de Catálogo e Financeiro, a dívida foi zerada. O mypy completo passou em 235 arquivos.

## Agrupamento atual

| Área | Diagnósticos | Natureza predominante |
|---|---:|---|
| `tools/` | 0 | variáveis sem anotação e valores opcionais (corrigido) |
| `apps/financeiro/` | 0 | agregações e listas sem tipos explícitos (corrigido) |
| `apps/catalogo/` | 0 | comandos, QuerySets e atributos legados (corrigido) |
| `apps/pedidos/` | 5 | atributos legados/projeções e parâmetros opcionais |
| `apps/vendas/` | 0 | QuerySet/lista e projeções (corrigido) |
| `apps/arquivos/` | 0 | respostas monkey-patched, uniões opcionais e migration loader (corrigido) |
| `apps/sincronizacao/` | 0 | payloads de testes tipados como `object` (corrigido neste ciclo) |
| `apps/missoes/` | 0 | campo de formulário Django sem tipo reconhecido (corrigido neste ciclo) |
| `apps/operacao/` | 0 | atributo legado de projeção em teste (corrigido) |
| `apps/` (migração) | 1 | assinatura de `MigrationLoader` |

## Política histórica

- Não mascarar esses erros com exclusões globais no `mypy.ini`.
- Corrigir por pacote quando o próximo ciclo tocar a área, começando por contratos oficiais e atributos realmente existentes.
- Reexecutar o mypy completo após cada grupo; manter o mypy de escopo como gate obrigatório para cada ciclo novo.
- Nenhum erro desta lista altera o fato de que o produto deve funcionar com a IA desligada.
