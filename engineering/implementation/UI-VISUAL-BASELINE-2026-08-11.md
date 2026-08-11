# Baseline visual global — 11/08/2026

## Referência oficial

A página **Clientes** é a referência visual de superfície do Mheibos Gestor: shell escuro, acentos ciano/azul, bordas finas, cantos arredondados, sombras discretas, painéis com gradiente sutil e espaçamento compacto, porém respirável.

## Regra de implementação

Novas telas devem reutilizar os tokens e componentes visuais de `templates/base.html`. Não devem criar uma segunda linguagem visual com cores, raios, sombras ou espaçamentos incompatíveis. Exceções locais precisam ser justificadas por comportamento, não por preferência estética.

Tokens compartilhados adicionados:

- `--border-accent` para bordas de destaque;
- `--panel-gradient` para heróis e painéis de destaque;
- `--card-radius` e `--card-shadow` para cartões;
- `.page-hero`, `.chart-card` e `.subtle-panel` para composições recorrentes.

## Aplicação atual

- Dashboard oficial: cabeçalho e meta individual usam o mesmo painel de destaque da referência; gráficos permanecem determinísticos.
- Clientes: o hero passou a consumir os tokens globais.
- Dashboard Financeiro: cartões de gráficos passaram a consumir os tokens globais.
- Demais páginas que usam `.card`, `.glass`, botões e shell base recebem a mesma fundação automaticamente.

## Validação

`manage.py check`, 12 testes de Analytics e `git diff --check` foram aprovados. O servidor local de demonstração está disponível em `http://127.0.0.1:8002/`.
