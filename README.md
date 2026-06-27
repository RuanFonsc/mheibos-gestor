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

## Electron

O Electron foi configurado como launcher leve. Ele abre o Django local em janela desktop, sem travar o desenvolvimento do sistema. Nesta fase ele nao substitui o Python, o Django nem o banco; ele encapsula a experiencia em uma janela de app.

Instale as dependencias uma vez:

```powershell
npm install
```

Abrir o Mheibos Gestor:

```powershell
npm run electron:gestor
```

Abrir o Mheibos Producao:

```powershell
npm run electron:producao
```

Tambem existem atalhos locais:

```powershell
.\abrir_mheibos_gestor.bat
.\abrir_mheibos_producao.bat
```

Para gerar instaladores no futuro:

```powershell
npm run dist:gestor
npm run dist:producao
```

Os instaladores ficam em `release/`, que nao entra no Git.

Variaveis uteis para instalacao/atalhos:

- `MHEIBOS_PROJECT_ROOT`: pasta onde esta o `manage.py`, caso o launcher seja aberto fora do repositorio.
- `MHEIBOS_BASE_URL`: endereco de um servidor Mheibos ja aberto, por exemplo `http://127.0.0.1:8765`.

O empacotamento realmente standalone, com Python/runtime/servico local junto, deve ser tratado como uma etapa propria quando o nucleo estiver estavel.

## Codex

Este projeto guarda uma copia da skill de trabalho em `.codex/skills/mheibos-gestor-senior`.
Ao abrir o projeto em outro computador, instale ou copie essa skill para `C:\Users\ruan_\.codex\skills` antes de pedir analises amplas ou alteracoes importantes.
