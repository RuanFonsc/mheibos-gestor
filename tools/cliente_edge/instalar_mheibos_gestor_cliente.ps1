param(
    [string]$ServerUrl = "http://192.168.100.174:8001/"
)

$ErrorActionPreference = "Stop"

if (-not $ServerUrl.StartsWith("http://") -and -not $ServerUrl.StartsWith("https://")) {
    $ServerUrl = "http://$ServerUrl"
}
$ServerUrl = $ServerUrl.TrimEnd("/") + "/"

$edgeCandidates = @(
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
) | Where-Object { $_ -and (Test-Path $_) }

if (-not $edgeCandidates) {
    throw "Microsoft Edge nao foi encontrado neste computador."
}

$edgePath = $edgeCandidates[0]
$installDir = Join-Path $env:LOCALAPPDATA "MheibosGestorCliente"
$profileDir = Join-Path $installDir "EdgeProfile"
$startMenuDir = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Mheibos Gestor"
$desktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "Mheibos Gestor.lnk"
$startMenuShortcut = Join-Path $startMenuDir "Mheibos Gestor.lnk"
$launcherBat = Join-Path $installDir "Abrir Mheibos Gestor.bat"

New-Item -ItemType Directory -Force -Path $installDir, $profileDir, $startMenuDir | Out-Null

@"
@echo off
start "" "$edgePath" --app="$ServerUrl" --user-data-dir="$profileDir" --no-first-run
"@ | Set-Content -LiteralPath $launcherBat -Encoding ASCII

$shell = New-Object -ComObject WScript.Shell
foreach ($shortcutPath in @($desktopShortcut, $startMenuShortcut)) {
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $edgePath
    $shortcut.Arguments = "--app=`"$ServerUrl`" --user-data-dir=`"$profileDir`" --no-first-run"
    $shortcut.WorkingDirectory = $installDir
    $shortcut.IconLocation = "$edgePath,0"
    $shortcut.Description = "Mheibos Gestor"
    $shortcut.Save()
}

Write-Host ""
Write-Host "Mheibos Gestor instalado para este usuario do Windows."
Write-Host "Endereco configurado: $ServerUrl"
Write-Host "Atalhos criados na Area de Trabalho e no Menu Iniciar."
Write-Host ""
Write-Host "Importante: o servidor central precisa estar ligado e acessivel na rede."
