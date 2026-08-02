# VISUAL QUALITY GATE REPORT

**Ciclo:** IMP-009L  
**Tela:** detalhe do Pedido  
**Data:** 02/08/2026

## Contrato visual

- Finalidade: permitir ajuda urgente real sem perder autoria ou identidade do arquivo.
- Exposição: transferência aparece somente quando o alerta está ativo e o prazo da categoria é crítico.
- Ação: selecionar novo responsável, gerente autorizador e informar a senha do gerente.
- Consequência: responsabilidade muda imediatamente; pasta, criador e arquivos permanecem no lugar.
- Continuidade: o novo responsável recebe as ações de preparação sem assumir a autoria do Pedido ou dos arquivos.
- IA: não participa da criticidade, autorização, seleção ou mudança de responsabilidade.

## Estados validados

- alerta comum sem transferência;
- prazo crítico com solicitação de ajuda e transferência;
- senha gerencial inválida;
- transferência concluída e evento auditável;
- rollback quando a auditoria falha;
- novo responsável com acesso às ações da arte;
- dados manuais restaurados após o cenário visual.

## Viewports

- 1366x768 @ 100%: PASS, sem overflow horizontal.
- 1440x900 @ 100%: PASS, sem overflow horizontal.
- 1536x864 @ 100%: PASS, sem overflow horizontal.
- 1920x1080 @ 100%: PASS, sem overflow horizontal.
- 1366x768 @ 125% efetivo: PASS, com rolagem vertical e sem overflow horizontal.

## Automação e gates

- Ruff: PASS.
- Mypy: PASS.
- Django check e migration check: PASS.
- Tokens visuais: PASS.
- Testes focados: PASS, 37 testes.
- Baseline completo: PASS, 170 testes.
- V01, V02, V03, V05, V06, V08, V09, V10, V11, V18, V20 e V22: PASS.
- V23: não aplicável; componentes e design system existentes foram reutilizados.

## Evidência

- `C:/Users/Ruan/Documents/Mheibos Gestor/visual-evidence/IMP-009L/transferencia-gerencial.jpg`

## Resultado

**PASS** para IMP-009L. O cenário crítico artificial foi removido e o servidor local permaneceu disponível na porta 8002.
