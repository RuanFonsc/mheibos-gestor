# VISUAL QUALITY GATE REPORT

**Ciclo:** IMP-009H  
**Telas:** detalhe do Pedido, Perfil, Perfil da Empresa e Usuários  
**Data:** 02/08/2026

## Contrato visual

- Finalidade: criar ou vincular arte oficial sem abrir outra tela e tornar preferências descobríveis.
- Ação primária: `Criar arquivo oficial`; ação secundária: `Vincular oficialmente`.
- Densidade: seletor e ação em uma linha no desktop; lista completa permanece no detalhe, sem expandir cartões da fila.
- Estados inspecionados: sem arquivo oficial, preferência padrão, área de usuários separada, IA disponível ou desligada sem impacto operacional.
- Conteúdo longo: caminho usa quebra controlada no detalhe; nome permanece identificável; seletor mantém rótulos completos.

## Fontes normativas

- RFC-0000, RFC-0001, RFC-0006, RFC-0007, RFC-0008, RFC-0009 e RFC-0014.
- `docs/UI-STANDARDS-MHEIBOS.md`.
- `docs/VISUAL-QUALITY-GATE-MHEIBOS.md`.
- DEC-IMP-032 e DEC-IMP-033.

## Viewports testados

- 1366x768 @ 100%: PASS, `scrollWidth = clientWidth = 1366`.
- 1440x900 @ 100%: PASS, `scrollWidth = clientWidth = 1440`.
- 1536x864 @ 100%: PASS, `scrollWidth = clientWidth = 1536`.
- 1920x1080 @ 100%: PASS, `scrollWidth = clientWidth = 1920`.
- 1366x768 @ 125%: PASS, sem overflow horizontal e com ações acessíveis por rolagem vertical.

## Automação e gates

- Lint: PASS.
- Type checking: PASS.
- Django check/migrations: PASS.
- Testes: PASS, 150 testes.
- Overflow horizontal: PASS em todas as resoluções.
- IA desligada: PASS por contrato; nenhuma ação nova chama gateway cognitivo.
- V01, V02, V03, V05, V06, V08, V09, V10, V11, V12, V13, V18 e V20: PASS para a fatia.
- V22: PASS com evidências abaixo.
- V23: não aplicável; a fatia reutiliza o design system já aprovado e não o altera.

## Evidências

- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009H/pedido-2-1366x768.png`
- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009H/pedido-2-1920x1080.png`
- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009H/pedido-2-1366x768-zoom125.png`
- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009H/configuracoes-perfil-1366x768.png`
- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009H/configuracoes-usuarios-1366x768.png`

## Resultado

**PASS** para IMP-009H. Alertas temporais, conclusão agregada, restauração crítica, exceção gerencial e sincronização de cópias permanecem explicitamente nas próximas fatias da DEC-IMP-033; não são simulados nesta interface.
