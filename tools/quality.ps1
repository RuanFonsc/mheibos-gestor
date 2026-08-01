$ErrorActionPreference = "Stop"

$python = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    $python = "python"
}

& $python -m ruff check apps config manage.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $python -m mypy
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $python manage.py check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $python manage.py test --noinput
exit $LASTEXITCODE
