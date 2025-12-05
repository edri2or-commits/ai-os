# Restore Sleep - Revert to Normal Power Settings
# Use this when you want to re-enable normal sleep behavior

Write-Host "Restoring Normal Windows Power Settings..." -ForegroundColor Cyan

# Get current power scheme GUID
$currentScheme = (powercfg /getactivescheme).Split()[3]
Write-Host "Active Power Scheme: $currentScheme" -ForegroundColor Yellow

# Restore sleep after 30 minutes when plugged in
Write-Host "`n[1/5] Enabling sleep after 30 minutes (AC power)..." -ForegroundColor Green
powercfg /change standby-timeout-ac 30

# Restore monitor timeout after 15 minutes
Write-Host "[2/5] Enabling monitor timeout after 15 minutes..." -ForegroundColor Green
powercfg /change monitor-timeout-ac 15

# Re-enable hibernate
Write-Host "[3/5] Enabling hibernate..." -ForegroundColor Green
powercfg /hibernate on

# Re-enable hybrid sleep
Write-Host "[4/5] Enabling hybrid sleep..." -ForegroundColor Green
powercfg /setacvalueindex $currentScheme SUB_SLEEP HYBRIDSLEEP 1

# Restore hard disk timeout (20 minutes)
Write-Host "[5/5] Enabling hard disk timeout after 20 minutes..." -ForegroundColor Green
powercfg /change disk-timeout-ac 20

# Apply changes
powercfg /setactive $currentScheme

Write-Host "`n✅ Normal power settings restored!" -ForegroundColor Green
Write-Host "`nCurrent settings:" -ForegroundColor Cyan
powercfg /query $currentScheme SUB_SLEEP

Write-Host "`n💡 Your computer will now sleep normally after inactivity." -ForegroundColor Yellow
