# Judge Agent Auto-Fix Script
Write-Host "Judge Agent Auto-Fix Starting..." -ForegroundColor Cyan

# Export current workflow
Write-Host "Exporting workflow..." -ForegroundColor Yellow
docker exec n8n-production n8n export:workflow --id=judge-agent-v1 --output=/tmp/judge_current.json

# The simplest fix: Just toggle the workflow off and on in the database
# This forces n8n to re-validate all node configurations

Write-Host "Deactivating workflow..." -ForegroundColor Yellow
docker exec n8n-production n8n update:workflow --id=judge-agent-v1 --active=false

Write-Host "Waiting 2 seconds..." -ForegroundColor Gray
Start-Sleep -Seconds 2

Write-Host "Reactivating workflow..." -ForegroundColor Yellow  
docker exec n8n-production n8n update:workflow --id=judge-agent-v1 --active=true

Write-Host "Done! Judge Agent should now be active." -ForegroundColor Green
Write-Host "If it still fails, the HTTP node needs manual JSON body fix in UI." -ForegroundColor Yellow
