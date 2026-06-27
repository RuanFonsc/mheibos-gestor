$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    py -3 -m venv .venv
}

.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt pyinstaller

if (Test-Path "dist\backend") {
    Remove-Item -LiteralPath "dist\backend" -Recurse -Force
}
New-Item -ItemType Directory -Force -Path "dist\backend" | Out-Null

.\.venv\Scripts\pyinstaller.exe --noconfirm mheibos-backend.spec

Move-Item -LiteralPath "dist\mheibos-backend" -Destination "dist\backend\mheibos-backend"

Write-Host "Backend pronto em dist\backend\mheibos-backend"
