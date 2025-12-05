# Disable Sleep - AI Life OS Configuration
# Prevents Windows from sleeping while automation is running

Write-Host "Configuring Windows Power Settings for 24/7 Operation..." -ForegroundColor Cyan

# Get current power scheme GUID
$currentScheme = (powercfg /getactivescheme).Split()[3]
Write-Host "Active Power Scheme: $currentScheme" -ForegroundColor Yellow

# Disable sleep when plugged in (AC)
Write-Host "`n[1/5] Disabling sleep (AC power)..." -ForegroundColor Green
powercfg /change standby-timeout-ac 0

# Disable monitor timeout when plugged in
Write-Host "[2/5] Disabling monitor timeout (AC power)..." -ForegroundColor Green
powercfg /change monitor-timeout-ac 0

# Disable hibernate
Write-Host "[3/5] Disabling hibernate..." -ForegroundColor Green
powercfg /hibernate off

# Disable hybrid sleep
Write-Host "[4/5] Disabling hybrid sleep..." -ForegroundColor Green
powercfg /setacvalueindex $currentScheme SUB_SLEEP HYBRIDSLEEP 0

# Disable hard disk timeout
Write-Host "[5/5] Disabling hard disk timeout..." -ForegroundColor Green
powercfg /change disk-timeout-ac 0

# Apply changes
powercfg /setactive $currentScheme

Write-Host "`n✅ Power settings configured for 24/7 operation!" -ForegroundColor Green
Write-Host "`nCurrent settings:" -ForegroundColor Cyan
powercfg /query $currentScheme SUB_SLEEP

Write-Host "`n⚠️  Note: Screen will stay on. Consider using 'monitor-timeout-ac 10' if needed." -ForegroundColor Yellow
