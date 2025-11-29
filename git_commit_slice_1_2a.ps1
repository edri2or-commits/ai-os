Set-Location "C:\Users\edri2\Desktop\AI\ai-os"
$gitPath = "C:\Program Files\Git\bin\git.exe"

Write-Host "=== Git Add ===" -ForegroundColor Cyan
& $gitPath add -A

Write-Host "`n=== Git Status ===" -ForegroundColor Cyan
& $gitPath status --short

Write-Host "`n=== Git Commit ===" -ForegroundColor Cyan
& $gitPath commit -F COMMIT_MSG_SLICE_1_2a.txt

Write-Host "`n=== Verify Commit ===" -ForegroundColor Cyan
& $gitPath log --oneline -1
& $gitPath show --stat HEAD
