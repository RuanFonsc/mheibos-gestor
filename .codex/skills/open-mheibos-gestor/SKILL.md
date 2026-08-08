---
name: open-mheibos-gestor
description: Start or open the Mheibos Gestor Django server quickly. Use when the user asks to "subir o gestor", "abrir o gestor", "iniciar o Gestor", get the local/LAN URL, diagnose startup friction, or make the repeated server startup flow faster for this repository.
---

# Open Mheibos Gestor

Use this skill for the fast, repeatable Mheibos Gestor startup path. Prefer the bundled script over retyping commands.

## Fast Path

From the repository root, run:

```powershell
.\.codex\skills\open-mheibos-gestor\scripts\start-gestor.ps1
```

The script:

1. Checks whether `http://127.0.0.1:8001/` already responds.
2. Checks whether port `8001` is occupied.
3. Runs migrations only when the server is not already online.
4. Starts Django hidden with logs in `.codex/runlogs/`.
5. Writes a fresh PID file.
6. Validates HTTP and reports local plus LAN URLs.

Use `-Restart` only when the user explicitly wants to restart the running server. Use `-SkipMigrate` only for a quick smoke start after migrations were already checked in the same session.

## Manual Fallback

If the script fails, use this focused sequence:

```powershell
git status --short --branch
git diff --stat
Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue
$env:DJANGO_DEBUG='True'
$env:DJANGO_ALLOWED_HOSTS='*'
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8001 --noreload
```

Then validate:

```powershell
Invoke-WebRequest -Uri 'http://127.0.0.1:8001/' -UseBasicParsing -TimeoutSec 10
Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '127.*' -and $_.PrefixOrigin -ne 'WellKnown' }
```

## Known Startup Friction

Read `references/startup-triage.md` when diagnosing why startup was slow, confusing, or unreliable.

Default report format:

- Local URL: `http://127.0.0.1:8001/`
- LAN URL: use the active Ethernet or Wi-Fi IPv4, usually `http://<ip>:8001/`
- Validation: HTTP status, PID, migration result, and any blocker.
