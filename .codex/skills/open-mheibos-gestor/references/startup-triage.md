# Mheibos Gestor Startup Triage

Use this reference when the user asks what went wrong while starting the Gestor or how to make startup faster.

## Problems Observed On 2026-08-01

1. Startup required several manual checks: Git state, skill freshness, port availability, migrations, process start, HTTP validation, and LAN IP discovery.
2. The server had no database issue; `manage.py migrate` reported no migrations to apply.
3. Port `8001` was free before start and later listened on `0.0.0.0:8001`.
4. The first hidden `Start-Process` command produced no useful console summary, so validation had to be done by HTTP and port inspection.
5. `.codex/runlogs/` already contained many old logs and stale PID files, which made it harder to identify the fresh process quickly.
6. The HTTP validation succeeded with `200 OK` after redirecting from `/` to `/login/`.
7. A `Broken pipe` appeared after the validation request. Treat it as harmless when the page returns successfully; it can happen when the client closes a connection early.

## Resolution Stages

Stage 1: Fast detection

- Check `http://127.0.0.1:8001/` first.
- If it returns any valid Django response, do not start a second server.
- Report the existing PID from `Get-NetTCPConnection`.

Stage 2: Clean startup

- Confirm `.venv\Scripts\python.exe` exists.
- Check port `8001`.
- If occupied and HTTP does not respond, report the owning PID and stop unless the user asked for restart.
- Run migrations before starting only when the server is not already online.

Stage 3: Reliable background process

- Start Django with `DJANGO_DEBUG=True`, `DJANGO_ALLOWED_HOSTS=*`, and `PYTHONUNBUFFERED=1`.
- Redirect stdout/stderr to timestamp-free current logs: `django-8001.out.log` and `django-8001.err.log`.
- Write the started PID to `.codex/runlogs/django-8001.pid`.

Stage 4: Validation

- Wait briefly for startup.
- Validate `http://127.0.0.1:8001/`.
- Get active non-loopback IPv4 addresses and prefer Ethernet or Wi-Fi.
- Report local URL, LAN URL, PID, and log paths.

Stage 5: Cleanup when needed

- Do not delete logs by default.
- If logs become noisy, summarize latest logs with `Get-Content -Tail` and optionally rotate old files only after user approval.
- Keep `.codex/runlogs/` ignored and out of Git.
