# Mheibos Gestor

Sistema de gestao da Mheibos, em Django, para substituir e evoluir o sistema Desktop/PyQt legado.

## Escopo inicial

- CRM de clientes.
- Gestor de pedidos e producao.
- Itens de pedido normalizados.
- Artes salvas em arquivos, nao em Base64 no banco.
- Pagamentos e lancamentos financeiros integrados.
- Relatorios mensais/anuais equivalentes a planilha Solides.

## Primeiros comandos

```powershell
cd C:\Users\ruan_\Documents\GESTOR\mheibos-gestor
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py preparar_financeiro
.\.venv\Scripts\python.exe manage.py importar_legado --dry-run
.\.venv\Scripts\python.exe manage.py importar_legado
```

Antes de aplicar `migrate`, ajuste as credenciais em `.env` com base em `.env.example`.

## Codex

Este projeto guarda uma copia da skill de trabalho em `.codex/skills/mheibos-gestor-senior`.
Ao abrir o projeto em outro computador, instale ou copie essa skill para `C:\Users\ruan_\.codex\skills` antes de pedir analises amplas ou alteracoes importantes.
