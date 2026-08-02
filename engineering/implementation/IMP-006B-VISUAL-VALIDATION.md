# Relatório de Validação Visual — IMP-006B

Data: 2026-08-02

Estado: COMPLETED

## Escopo validado

- Gestor de Pedidos como entrada comercial única, sem navegação para Mheibos Vendas.
- Produção como visão especializada, acessível pelo papel/função e pela etapa do Pedido.
- A tela então chamada Expedição e a Entrega como partes visíveis do Fluxo do Pedido. A responsabilidade real da primeira foi corrigida para Preparação de arte no IMP-006C.
- Detalhe do Pedido expondo a projeção oficial de Processo e Etapa.
- Operação integral sem IA; assistência cognitiva permanece opcional e não bloqueante.

## Casos de conteúdo

- estado vazio;
- dois Pedidos realistas;
- cliente, tema e item com texto longo;
- Processo formal `PRODUCAO_PEDIDO v1` em andamento;
- ausência de categoria, arte e pedidos prontos para entrega.

Os dados foram criados apenas na cópia isolada `C:\Users\Ruan\Documents\Mheibos Gestor\manual-test-data\mheibos_manual.sqlite3`.

## Matriz visual

Lista, Detalhe, a tela então chamada Expedição e Entrega foram verificadas em 1366 × 768, 1440 × 900, 1536 × 864 e 1920 × 1080 a 100%, além de 1366 × 768 a 125% (viewport CSS 1093 × 614 e fator 1,25). A errata semântica está registrada no IMP-006C.

Resultado final: 20 de 20 combinações sem overflow detectado. A evidência local está em `C:\Users\Ruan\Documents\Mheibos Gestor\visual-evidence\IMP-006B\final-*`; a correção específica de 125% está em `final-list-125-fix`.

## Revisão humana

- Hierarquia, contraste, leitura e densidade: PASS.
- Ações principais e estados vazios: PASS.
- Conteúdo extremo e quebra de layout: PASS após correção da grade em 125%.
- Coerência entre Lista e Detalhe: PASS após carregar `projetar_pedido()` no detalhe.
- Dependência de CDN: a fundação e as quatro telas piloto continuam legíveis e operáveis sem Tailwind/Lucide/Chart.js; ícones são complementares.
- Tokens nos quatro templates afetados: PASS no validador automático.

## Gates técnicos

- `manage.py check`: PASS.
- teste direcionado da projeção no detalhe: PASS.
- lint dos arquivos de produto e da Skill de UI alterados: PASS.
- type checking no escopo oficial configurado (8 arquivos): PASS.
- suíte integral: 141 testes em 156,302 s, PASS.

A varredura de lint de todo o repositório também identificou dívida anterior em scripts compactados da Skill `mheibos-engineering`. Ela não foi introduzida nem ampliada pelo IMP-006B e permanece fora do escopo desta fatia; os arquivos alterados passaram separadamente.

## Compatibilidade preservada

As rotas legadas de Vendas não são apresentadas como produto ou navegação. Sua remoção física não foi feita nesta fatia para não quebrar integrações históricas sem migração; permanecem apenas como fronteira temporária de compatibilidade, sem duplicar a interface oficial.

## Conflitos e decisões humanas

Nenhum conflito normativo ou `DECISAO_HUMANA_NECESSARIA` foi identificado para esta fatia.
