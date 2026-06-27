$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw "npm nao encontrado no PATH. Instale Node.js LTS antes de gerar os instaladores."
}

npm install
npm run build:backend
npm run dist:suite
npm run dist:gestor
npm run dist:producao

Write-Host "Instaladores gerados em release\suite, release\gestor e release\producao"
