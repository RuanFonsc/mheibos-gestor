# Mudanca de servidor - Mheibos Gestor

Checklist pratico para levar o sistema para outra maquina e manter o Codex trabalhando com o mesmo contexto.

## Codigo e contexto do agente

- Levar o repositorio completo, incluindo `AGENTS.md` e `.codex/skills/mheibos-gestor-senior`.
- Instalar a skill local copiando `.codex/skills/mheibos-gestor-senior` para `%USERPROFILE%\.codex\skills\mheibos-gestor-senior`.
- Conferir se o remoto Git esta acessivel: `git remote -v`.
- Nao versionar nem copiar como codigo: `.venv`, logs, backups, `media` e arquivos de ambiente com senhas.

## Ambiente do servidor

- Instalar Python compativel e dependencias de `requirements.txt`.
- Configurar PostgreSQL e restaurar/criar o banco usado pelo `.env`.
- Criar `.env` a partir de `.env.example` e ajustar `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
- Rodar: `.venv\Scripts\python.exe manage.py migrate`.
- Rodar: `.venv\Scripts\python.exe manage.py check`.

## Subir para a rede

- Usar `iniciar_mheibos_servidor_rede.bat`.
- O servidor deve abrir em `0.0.0.0:8001`.
- Nos clientes da rede, acessar `http://IP_DO_SERVIDOR:8001/`.

### Subida manual rapida

Use quando precisar subir pelo terminal sem procurar o comando:

```powershell
cd D:\mheibos-gestor
$env:DJANGO_DEBUG='True'
$env:DJANGO_ALLOWED_HOSTS='*'
$env:PYTHONUNBUFFERED='1'
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8001 --noreload
```

Antes de iniciar, confira se a porta esta livre:

```powershell
Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue
```

Depois valide:

```powershell
Invoke-WebRequest -Uri 'http://127.0.0.1:8001/' -UseBasicParsing -TimeoutSec 10
```

## Mheibos Aprendizado / WhatsApp

- Configurar o webhook da Evolution para `http://IP_DO_SERVIDOR:8001/webhook`.
- Teste rapido de saude: abrir `http://IP_DO_SERVIDOR:8001/webhook` e esperar `{"ok": true, "modulo": "Mheibos Aprendizado"}`.
- As conversas ficam em `apps.aprendizado` no banco e o JSON de treino e gerado em `exports/aprendizado/conversas_uteis.json`.
