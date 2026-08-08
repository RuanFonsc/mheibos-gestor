param(
    [int]$Port = 8001,
    [string]$ProjectRoot,
    [switch]$Restart,
    [switch]$SkipMigrate
)

$ErrorActionPreference = "Stop"

function Resolve-ProjectRoot {
    param([string]$RequestedRoot)

    if ($RequestedRoot) {
        $resolved = Resolve-Path -LiteralPath $RequestedRoot
        return $resolved.Path
    }

    if (Test-Path -LiteralPath (Join-Path (Get-Location) "manage.py")) {
        return (Get-Location).Path
    }

    $candidate = $PSScriptRoot
    while ($candidate) {
        if (Test-Path -LiteralPath (Join-Path $candidate "manage.py")) {
            return $candidate
        }
        $parent = Split-Path -Parent $candidate
        if ($parent -eq $candidate) {
            break
        }
        $candidate = $parent
    }

    throw "Project root not found. Run this script from the Mheibos Gestor repository or pass -ProjectRoot."
}

function Test-HttpReady {
    param([string]$Url)

    try {
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5 -MaximumRedirection 5
        return [pscustomobject]@{ Ready = $true; StatusCode = $response.StatusCode; Length = $response.Content.Length }
    }
    catch {
        return [pscustomobject]@{ Ready = $false; StatusCode = $null; Length = 0; Error = $_.Exception.Message }
    }
}

function Get-PortOwner {
    param([int]$Port)

    Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
        Where-Object { $_.State -eq "Listen" } |
        Select-Object -First 1
}

function Get-LanAddress {
    $addresses = Get-NetIPAddress -AddressFamily IPv4 |
        Where-Object { $_.IPAddress -notlike "127.*" -and $_.PrefixOrigin -ne "WellKnown" } |
        Sort-Object @{ Expression = { if ($_.InterfaceAlias -match "Ethernet|Wi-Fi|Wifi") { 0 } else { 1 } } }, InterfaceAlias

    return $addresses | Select-Object -First 1
}

$root = Resolve-ProjectRoot -RequestedRoot $ProjectRoot
$localUrl = "http://127.0.0.1:$Port/"
$python = Join-Path $root ".venv\Scripts\python.exe"
$logDir = Join-Path $root ".codex\runlogs"
$outLog = Join-Path $logDir "django-$Port.out.log"
$errLog = Join-Path $logDir "django-$Port.err.log"
$pidFile = Join-Path $logDir "django-$Port.pid"

if (-not (Test-Path -LiteralPath $python)) {
    throw "Project virtualenv Python not found at $python"
}

New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$ready = Test-HttpReady -Url $localUrl
$owner = Get-PortOwner -Port $Port

if ($ready.Ready -and -not $Restart) {
    $lan = Get-LanAddress
    [pscustomobject]@{
        Status = "already-running"
        LocalUrl = $localUrl
        LanUrl = if ($lan) { "http://$($lan.IPAddress):$Port/" } else { $null }
        Pid = if ($owner) { $owner.OwningProcess } else { $null }
        HttpStatus = $ready.StatusCode
        OutLog = $outLog
        ErrLog = $errLog
    } | Format-List
    exit 0
}

if ($owner -and -not $Restart) {
    throw "Port $Port is already occupied by PID $($owner.OwningProcess), but $localUrl did not respond. Use -Restart only if you intend to replace it."
}

if ($Restart -and $owner) {
    Stop-Process -Id $owner.OwningProcess -Force
    Start-Sleep -Seconds 2
}

if (-not $SkipMigrate) {
    Push-Location $root
    try {
        $env:DJANGO_DEBUG = "True"
        $env:DJANGO_ALLOWED_HOSTS = "*"
        & $python manage.py migrate
    }
    finally {
        Pop-Location
    }
}

$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "*"
$env:PYTHONUNBUFFERED = "1"

$process = Start-Process -FilePath $python `
    -ArgumentList @("manage.py", "runserver", "0.0.0.0:$Port", "--noreload") `
    -WorkingDirectory $root `
    -WindowStyle Hidden `
    -RedirectStandardOutput $outLog `
    -RedirectStandardError $errLog `
    -PassThru

Set-Content -LiteralPath $pidFile -Value $process.Id

$deadline = (Get-Date).AddSeconds(20)
do {
    Start-Sleep -Milliseconds 700
    $ready = Test-HttpReady -Url $localUrl
} until ($ready.Ready -or (Get-Date) -gt $deadline)

if (-not $ready.Ready) {
    $tail = if (Test-Path -LiteralPath $errLog) { Get-Content -LiteralPath $errLog -Tail 20 } else { @() }
    throw "Server process PID $($process.Id) started but HTTP validation failed. Error log tail: $($tail -join ' | ')"
}

$lan = Get-LanAddress
[pscustomobject]@{
    Status = "started"
    LocalUrl = $localUrl
    LanUrl = if ($lan) { "http://$($lan.IPAddress):$Port/" } else { $null }
    Pid = $process.Id
    HttpStatus = $ready.StatusCode
    OutLog = $outLog
    ErrLog = $errLog
    PidFile = $pidFile
} | Format-List
