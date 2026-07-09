# Codex Project Instructions

Before working on this repository, check whether the project skill is installed:

- Project copy: `.codex/skills/mheibos-gestor-senior`
- Local install target on Windows: `$env:USERPROFILE\.codex\skills\mheibos-gestor-senior`

Derive the local target from the current Windows user instead of hardcoding a user profile:

```powershell
$projectSkill = ".\.codex\skills\mheibos-gestor-senior"
$localSkill = Join-Path $env:USERPROFILE ".codex\skills\mheibos-gestor-senior"
```

If the local skill is missing or older than the project copy, copy/install it to `$localSkill` before doing broad analysis. Use the skill's rules for token economy, intent translation, Git-first workflow, and senior technical intervention.

When the user uses approximate technical language, translate it into the likely product/workflow intent before searching literal terms.

## Quick server startup

When the user asks to "subir o servidor", use this path before broader discovery:

1. Start with the project skill rule:
   ```powershell
   git status --short --branch
   git diff --stat
   ```
2. Check whether port `8001` is free:
   ```powershell
   Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue
   ```
3. Apply/check migrations with the project virtualenv:
   ```powershell
   $env:DJANGO_DEBUG='True'
   $env:DJANGO_ALLOWED_HOSTS='*'
   .\.venv\Scripts\python.exe manage.py migrate
   ```
4. Start the LAN server on port `8001`:
   ```powershell
   $env:DJANGO_DEBUG='True'
   $env:DJANGO_ALLOWED_HOSTS='*'
   $env:PYTHONUNBUFFERED='1'
   .\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8001 --noreload
   ```
   If the user needs the shell back, start it hidden with `Start-Process`, redirect logs under `.codex/runlogs/`, and keep `.codex/runlogs/` out of Git.
5. Validate before reporting success:
   ```powershell
   Invoke-WebRequest -Uri 'http://127.0.0.1:8001/' -UseBasicParsing -TimeoutSec 10
   Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '127.*' -and $_.PrefixOrigin -ne 'WellKnown' }
   ```

Report the local URL `http://127.0.0.1:8001/` and the LAN URL using the active Ethernet/Wi-Fi IPv4, usually `http://IP_DO_SERVIDOR:8001/`.
