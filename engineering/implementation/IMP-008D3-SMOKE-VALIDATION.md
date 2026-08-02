# IMP-008D.3 — Validação real entre duas instâncias

**Data:** 02/08/2026  
**Estado:** PASS_WITH_GAP  
**Escopo:** ciclo Django/HTTP entre Central e Cliente offline com persistências independentes

## Ambiente isolado

- Base Central SQLite exclusiva.
- Base Cliente SQLite exclusiva.
- Servidor HTTP Central temporário em porta livre local.
- Credencial de Estação efêmera, mantida fora do relatório.
- Nenhum acesso ou alteração ao banco de testes manuais do usuário.

## Resultados

1. O Cliente criou um Pedido local e uma unidade durável de sincronização.
2. `verificar_retorno_online` recusou o retorno enquanto existia uma unidade pendente.
3. `enviar_fila_offline` transmitiu o envelope por HTTP real e recebeu uma confirmação válida.
4. Após a persistência da confirmação, `verificar_retorno_online` respondeu `RETORNO_SEGURO`.
5. O mesmo envelope foi transmitido novamente e a Central respondeu `JA_INCORPORADO`.
6. A Central terminou com exatamente um Pedido offline e uma incorporação, provando ausência de duplicação.

## Rastreabilidade

- Executor reproduzível: `tools/smoke_offline_two_instances.py`.
- Evidência local preservada: `C:\Users\Ruan\Documents\Mheibos Gestor\smoke-offline\IMP-008D3-2026-08-02\result.json`.
- Bases isoladas preservadas ao lado do relatório para inspeção posterior.

## Lacuna remanescente

O repositório não contém instalador `.exe` ou `.msi`. Portanto, continuam pendentes apenas os aspectos que exigem interação humana com o pacote Electron no Windows: `safeStorage`, troca visual para o backend local em `127.0.0.1:8766` e retorno visual à Central. Essa lacuna não invalida o ciclo Django/HTTP nem bloqueia os IMPs seguintes.
