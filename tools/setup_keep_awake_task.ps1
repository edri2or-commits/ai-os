# Setup Smart Keep-Awake Task Scheduler
# Configures Windows Task Scheduler to run Smart Keep-Awake on startup

Write-Host "Setting up Smart Keep-Awake Task..." -ForegroundColor Cyan

$taskName = "AI-OS\Smart Keep-Awake"
$scriptPath = "C:\Users\edri2\Desktop\AI\ai-os\tools\smart_keep_awake.ps1"

# Check if script exists
if (-not (Test-Path $scriptPath)) {
    Write-Error "Script not found: $scriptPath"
    exit 1
}

# Remove existing task if exists
$existingTask = Get-ScheduledTask -TaskName "Smart Keep-Awake" -TaskPath "\AI-OS\" -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName "Smart Keep-Awake" -TaskPath "\AI-OS\" -Confirm:$false
}

# Create task action
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""

# Create task trigger (at startup)
$trigger = New-ScheduledTaskTrigger -AtStartup

# Create task settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable:$false `
    -ExecutionTimeLimit (New-TimeSpan -Days 365)

# Create task principal (run as current user, highest privileges)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

# Register task
Register-ScheduledTask `
    -TaskName "Smart Keep-Awake" `
    -TaskPath "\AI-OS\" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Prevents Windows sleep when Docker automation is running" | Out-Null

Write-Host "✅ Task created successfully!" -ForegroundColor Green
Write-Host "`nTask Details:" -ForegroundColor Cyan
Write-Host "  Name: $taskName" -ForegroundColor Gray
Write-Host "  Trigger: At Windows startup" -ForegroundColor Gray
Write-Host "  Action: Run smart_keep_awake.ps1 (hidden window)" -ForegroundColor Gray
Write-Host "  Behavior: Prevents sleep only when Docker containers are running" -ForegroundColor Gray

Write-Host "`n💡 To start now (without reboot):" -ForegroundColor Yellow
Write-Host "   Start-ScheduledTask -TaskPath '\AI-OS\' -TaskName 'Smart Keep-Awake'" -ForegroundColor White

Write-Host "`n💡 To stop:" -ForegroundColor Yellow
Write-Host "   Stop-ScheduledTask -TaskPath '\AI-OS\' -TaskName 'Smart Keep-Awake'" -ForegroundColor White

Write-Host "`n⚠️  Note: This task will run automatically on every Windows startup." -ForegroundColor Cyan
