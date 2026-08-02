# VISUAL QUALITY GATE REPORT

**Ciclo:** IMP-009J  
**Telas:** detalhe do Pedido e Preparação de Arte  
**Data:** 02/08/2026

## Contrato visual

- Finalidade: impedir que uma arte iniciada e não concluída seja esquecida.
- Ação primária: concluir a arte; ações secundárias: continuar trabalhando, lembrar em 30 minutos e, quando permitido, adiar para amanhã.
- Prazo crítico: retirar o adiamento e oferecer ajuda urgente sem esconder o motivo.
- Descoberta: manter o alerta tanto no Pedido quanto na fila operacional e na notificação global.
- Conteúdo: preservar nome, responsável, número do alerta, criticidade e explicação de que a conclusão é humana.
- IA: não participa da detecção, autorização, prazo, persistência nem das respostas.

## Estados validados

- primeiro alerta fora do prazo crítico;
- segundo alerta com adiamento ainda permitido;
- terceiro alerta sem adiamento;
- prazo crítico com ajuda urgente e adiamento bloqueado;
- alerta respondido com lembrete de 30 minutos;
- fila com alerta e pedido aguardando arte simultaneamente;
- IA desligada e operação normal.

## Viewports

- 1366x768 @ 100%: PASS, sem overflow horizontal.
- 1440x900 @ 100%: PASS, sem overflow horizontal.
- 1536x864 @ 100%: PASS, sem overflow horizontal.
- 1920x1080 @ 100%: PASS, sem overflow horizontal.
- 1366x768 @ 125%: PASS, ações acessíveis por rolagem vertical e sem overflow horizontal.

## Automação e gates

- Lint e type checking: PASS.
- Django check e migration check: PASS.
- Tokens visuais: PASS.
- Testes focados: PASS, 59 testes.
- V01, V02, V03, V05, V06, V08, V09, V10, V11, V18, V20 e V22: PASS.
- V23: não aplicável; componentes e design system aprovados foram reutilizados.

## Evidências

- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009J/alerta-1366x768.png`
- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009J/alerta-1440x900.png`
- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009J/alerta-1536x864.png`
- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009J/alerta-1920x1080.png`
- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009J/alerta-1366x768-zoom125.png`
- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009J/alerta-prazo-critico-1920x1080.png`
- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009J/fila-preparacao-1920x1080.png`

## Resultado

**PASS** para IMP-009J. Transferência gerencial de responsabilidade pertence à IMP-009L; restauração de arquivo ausente e exceção por ação pertencem à IMP-009K.
