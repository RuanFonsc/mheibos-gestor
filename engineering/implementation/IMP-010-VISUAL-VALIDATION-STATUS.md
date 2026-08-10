# IMP-010 — Status da validação visual

**Estado:** `BLOCKED`  
**Data:** 10/08/2026

A validação visual real ainda não foi aprovada. O servidor de teste foi iniciado, mas a base usada pelo processo web não possuía `django_session`, impedindo renderizar `/missoes/` no navegador.

## Evidência disponível

- `manage.py check`: PASS;
- testes de interface do workspace: PASS;
- testes do app `apps.missoes`: PASS;
- renderização real no navegador: não validada por erro de inicialização da base.

## Condição para desbloqueio

Executar o servidor com uma base SQLite persistente e migrada no mesmo processo/configuração, abrir `/missoes/` e `/missoes/<uuid>/`, verificar visualmente tarefas, notas, chat, ações e ausência de overflow nas resoluções oficiais. Só então alterar este documento para `PASS`.
