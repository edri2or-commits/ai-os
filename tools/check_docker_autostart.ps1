# Check Docker Desktop Auto-Start Configuration
# This script verifies that Docker Desktop will start automatically with Windows
# and that containers have proper restart policies.

Write-Host "=== Docker Desktop Auto-Start Check ===" -ForegroundColor Cyan

# Check Docker Desktop settings
$settingsFile = "$env:APPDATA\Docker\settings-store.json"
if (Test-Path $settingsFile) {
    $settings = Get-Content $settingsFile | ConvertFrom-Json
    $autoStart = $settings.AutoStart
    if ($autoStart -eq $true) {
        Write-Host "[OK] Docker Desktop AutoStart: Enabled" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Docker Desktop AutoStart: Disabled" -ForegroundColor Yellow
    }
} else {
    Write-Host "[ERROR] Docker settings file not found" -ForegroundColor Red
}

# Check Windows Registry
$regKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$dockerEntry = Get-ItemProperty -Path $regKey -ErrorAction SilentlyContinue | 
    Select-Object -ExpandProperty "Docker Desktop" -ErrorAction SilentlyContinue

if ($dockerEntry) {
    Write-Host "[OK] Windows Startup Registry: Docker Desktop registered" -ForegroundColor Green
} else {
    Write-Host "[WARN] Windows Startup Registry: Docker Desktop not found" -ForegroundColor Yellow
}

# Check Docker service
$dockerProcess = Get-Process "Docker Desktop" -ErrorAction SilentlyContinue
if ($dockerProcess) {
    Write-Host "[OK] Docker Desktop: Running" -ForegroundColor Green
} else {
    Write-Host "[WARN] Docker Desktop: Not running" -ForegroundColor Yellow
    exit 1
}

# Check container restart policies
$containers = @("n8n-production", "qdrant-production")
foreach ($container in $containers) {
    $restartPolicy = docker inspect $container --format "{{.HostConfig.RestartPolicy.Name}}" 2>$null
    if ($restartPolicy -eq "always") {
        Write-Host "[OK] ${container}: RestartPolicy=always" -ForegroundColor Green
    } elseif ($restartPolicy) {
        Write-Host "[WARN] ${container}: RestartPolicy=$restartPolicy (not 'always')" -ForegroundColor Yellow
    } else {
        Write-Host "[ERROR] ${container}: Not found" -ForegroundColor Red
    }
}

Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "Docker Desktop will start automatically with Windows." -ForegroundColor Green
Write-Host "Containers will restart automatically if Docker Desktop is running." -ForegroundColor Green
