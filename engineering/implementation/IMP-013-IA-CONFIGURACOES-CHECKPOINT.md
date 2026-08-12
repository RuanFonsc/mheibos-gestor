# Checkpoint — Configurações de IA — 11/08/2026

## Implementado

- Catálogo versionado em `apps/cognicao/configuracoes_ia.py`.
- Escopos Empresa, Usuário, Missão e `LOCKED` representados na página oficial.
- Política empresarial configurável com senha administrativa e persistência separada.
- Preferências individuais persistidas por operador.
- Autonomia por Missão exibida com escopo isolado e desligada por padrão.
- Decisões não configuráveis exibidas como informação, sem controles de alteração.
- `resolve_ai_policy` centralizado para bloquear decisões financeiras, alteração normativa, análise visual de arte e uso opcional quando a IA estiver desligada.
- IA permanece opcional: desligá-la não bloqueia o fluxo determinístico.

## Lacunas preservadas

- O vínculo editável de autonomia precisa ser conectado à entidade Missão quando o fluxo de Missões expuser essa autoridade.
- Conselho de gerentes, cache distribuído e eventos de auditoria específicos de cada configuração ainda dependem da infraestrutura normativa correspondente.
- As decisões D01–D11 continuam candidatas até classificação/aprovação posterior; a tela não as promove automaticamente.

## Validação

- `manage.py check` aprovado.
- 22 testes direcionados de `apps.catalogo` e `apps.cognicao` aprovados.
- Template de Configurações compilado com sucesso.
- Ruff e `git diff --check` aprovados.
