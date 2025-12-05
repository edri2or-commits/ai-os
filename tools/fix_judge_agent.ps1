#!/usr/bin/env pwsh
# Judge Agent Auto-Fix Script
# This script fixes the Judge Agent workflow configuration

Write-Host "🔧 Judge Agent Auto-Fix Starting..." -ForegroundColor Cyan

# Step 1: Export current workflow
Write-Host "`n📤 Exporting current workflow..." -ForegroundColor Yellow
$exportResult = docker exec n8n-production n8n export:workflow --id=judge-agent-v1 --output=/tmp/judge_export.json 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Export failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Exported" -ForegroundColor Green

# Step 2: Copy from container
Write-Host "`n📥 Copying workflow file..." -ForegroundColor Yellow
docker cp n8n-production:/tmp/judge_export.json "$env:TEMP\judge_export.json" | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Copy failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Copied" -ForegroundColor Green

# Step 3: Read and fix JSON
Write-Host "`n🔧 Fixing workflow configuration..." -ForegroundColor Yellow
$workflow = Get-Content "$env:TEMP\judge_export.json" -Raw | ConvertFrom-Json

# Find the HTTP Request node
$httpNode = $workflow.nodes | Where-Object { $_.name -like "*GPT*" -or $_.type -eq "n8n-nodes-base.httpRequest" }

if ($httpNode) {
    Write-Host "   Found HTTP node: $($httpNode.name)" -ForegroundColor Gray
    
    # Fix the body parameters to use JSON mode
    $httpNode.parameters.specifyBody = "json"
    $httpNode.parameters.jsonBody = '={
  "model": "gpt-4o",
  "messages": [{"role": "user", "content": $json.prompt}],
  "temperature": 0.2,
  "response_format": {"type": "json_object"}
}'
    
    # Remove old body parameters if exist
    if ($httpNode.parameters.bodyParameters) {
        $httpNode.parameters.PSObject.Properties.Remove('bodyParameters')
    }
    
    Write-Host "✅ Fixed body configuration" -ForegroundColor Green
} else {
    Write-Host "⚠️  HTTP node not found - workflow may have different structure" -ForegroundColor Yellow
}

# Step 4: Save fixed workflow
Write-Host "`n💾 Saving fixed workflow..." -ForegroundColor Yellow
$workflow | ConvertTo-Json -Depth 20 | Set-Content "$env:TEMP\judge_fixed.json" -Encoding UTF8
Write-Host "✅ Saved" -ForegroundColor Green

# Step 5: Copy back to container
Write-Host "`n📤 Uploading fixed workflow..." -ForegroundColor Yellow
docker cp "$env:TEMP\judge_fixed.json" n8n-production:/tmp/judge_fixed.json | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Upload failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Uploaded" -ForegroundColor Green

# Step 6: Delete old workflow
Write-Host "`n🗑️  Removing old workflow..." -ForegroundColor Yellow
docker exec n8n-production sh -c "rm -f /home/node/.n8n/database.sqlite-wal /home/node/.n8n/database.sqlite-shm" 2>&1 | Out-Null
Write-Host "✅ Cleaned" -ForegroundColor Green

# Step 7: Import fixed workflow  
Write-Host "`n📥 Importing fixed workflow..." -ForegroundColor Yellow
docker exec n8n-production n8n import:workflow --separate --input=/tmp/judge_fixed.json 2>&1 | Out-Null
Write-Host "✅ Imported" -ForegroundColor Green

# Step 8: Activate workflow
Write-Host "`n⚡ Activating workflow..." -ForegroundColor Yellow
$activateResult = docker exec n8n-production n8n update:workflow --id=judge-agent-v1 --active=true 2>&1
if ($activateResult -like "*Error*") {
    Write-Host "⚠️  Activation may need manual toggle in UI" -ForegroundColor Yellow
} else {
    Write-Host "✅ Activated" -ForegroundColor Green
}

Write-Host "`n🎉 Judge Agent Auto-Fix Complete!" -ForegroundColor Green
Write-Host "   Next execution: In 6 hours" -ForegroundColor Gray
Write-Host "   Check: http://localhost:5678" -ForegroundColor Gray
