# VISUAL QUALITY GATE REPORT

**Ciclo:** IMP-009K  
**Telas:** detalhe do Pedido e Preparação de Arte  
**Data:** 02/08/2026

## Contrato visual

- Finalidade: tornar impossível ignorar a ausência de um arquivo oficial.
- Prioridade: crítica, acima do lembrete comum de inatividade.
- Ação primária: restaurar o arquivo no nome e caminho oficiais e vinculá-lo novamente pelo Mheibos.
- Exceção: autorização gerencial visível apenas como alternativa pontual para uma transição, sem encerrar o alerta.
- Conteúdo: número do Pedido, nome e caminho oficial, estado persistente, decisão em caso de conteúdo divergente e explicação da autorização excepcional.
- IA: não participa da detecção, bloqueio, restauração, autorização ou persistência.

## Estados validados

- arquivo ausente e alerta não dispensável;
- arquivo reaparecido ainda sem vinculação explícita;
- restauração com mesmo conteúdo;
- restauração divergente com decisão humana;
- transição bloqueada sem gerente;
- autorização pontual com gerente, senha e justificativa;
- fila crítica e notificação global prioritária;
- estado normal restaurado após o cenário visual.

## Viewports

- 1366x768 @ 100%: PASS, sem overflow horizontal.
- 1440x900 @ 100%: PASS, sem overflow horizontal.
- 1536x864 @ 100%: PASS, sem overflow horizontal.
- 1920x1080 @ 100%: PASS, sem overflow horizontal.
- 1366x768 @ 125% efetivo: PASS, ações acessíveis por rolagem vertical e sem overflow horizontal.

## Automação e gates

- Ruff: PASS.
- Mypy: PASS.
- Django check e migration check: PASS.
- Tokens visuais: PASS.
- Testes focados: PASS, 46 testes.
- Baseline completo: PASS, 167 testes.
- V01, V02, V03, V05, V06, V08, V09, V10, V11, V18, V20 e V22: PASS.
- V23: não aplicável; componentes e design system aprovados foram reutilizados.

## Evidências

- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009K/pedido-2-alerta-critico.jpg`
- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009K/fila-alerta-critico.jpg`

## Resultado

**PASS** para IMP-009K. O alerta artificial usado na validação foi removido do banco manual; o servidor local permaneceu disponível na porta 8002.
