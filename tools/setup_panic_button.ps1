# Setup Panic Button Hotkey
# Creates desktop shortcut with Ctrl+Alt+P binding

$PanicScript = "C:\Users\edri2\Desktop\AI\ai-os\tools\panic_button.ps1"
$ShortcutPath = "$env:USERPROFILE\Desktop\PANIC_BUTTON.lnk"

Write-Host "Setting up Panic Button hotkey..." -ForegroundColor Cyan

# Create Windows shortcut
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$PanicScript`""
$Shortcut.WorkingDirectory = "C:\Users\edri2\Desktop\AI\ai-os"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,132" # Warning icon
$Shortcut.Description = "Emergency: Pause all automation and save state"
$Shortcut.Hotkey = "CTRL+ALT+P"
$Shortcut.Save()

Write-Host ""
Write-Host "[OK] Panic Button installed!" -ForegroundColor Green
Write-Host ""
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host "  - Press Ctrl+Alt+P anywhere to activate"
Write-Host "  - Or double-click 'PANIC_BUTTON.lnk' on Desktop"
Write-Host ""
Write-Host "What it does:" -ForegroundColor Yellow
Write-Host "  1. Pauses all Docker containers (n8n)"
Write-Host "  2. Creates Git WIP commit"
Write-Host "  3. Dumps system state to panic/"
Write-Host "  4. Archives recent logs"
Write-Host ""
Write-Host "Testing hotkey registration..."
Start-Sleep -Seconds 1

# Verify shortcut exists
if (Test-Path $ShortcutPath) {
    Write-Host "[OK] Shortcut created: $ShortcutPath" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to create shortcut" -ForegroundColor Red
}

Write-Host ""
Write-Host "NOTE: Windows hotkeys may require:" -ForegroundColor Cyan
Write-Host "  - Explorer restart (to activate hotkey)"
Write-Host "  - Or use Desktop shortcut directly"
Write-Host ""
Write-Host "To test: Run panic_button.ps1 -Test"
