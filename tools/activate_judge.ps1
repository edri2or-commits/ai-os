# Quick activation script
$apiKey = "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"

Write-Host "=== Activating Judge Agent ===" -ForegroundColor Cyan

try {
    $headers = @{"Content-Type" = "application/json"}
    
    # Get workflows
    $workflows = Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows" -Method GET -Headers $headers -ErrorAction Stop
    
    # Find Judge Agent
    $judgeWorkflow = $workflows.data | Where-Object { $_.name -like "*Judge Agent*" }
    
    if ($judgeWorkflow) {
        $workflowId = $judgeWorkflow.id
        Write-Host "Found workflow: $($judgeWorkflow.name)" -ForegroundColor Green
        Write-Host "Workflow ID: $workflowId" -ForegroundColor Cyan
        
        # Activate
        $body = @{ active = $true } | ConvertTo-Json
        Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows/$workflowId" -Method PATCH -Headers $headers -Body $body -ErrorAction Stop | Out-Null
        
        Write-Host ""
        Write-Host "SUCCESS! Workflow is now active!" -ForegroundColor Green
        Write-Host "Judge Agent will run automatically every 6 hours." -ForegroundColor Cyan
    } else {
        Write-Host "ERROR: Judge Agent workflow not found" -ForegroundColor Red
        Write-Host "Please import the workflow first or check the name" -ForegroundColor Yellow
    }
} catch {
    Write-Host "ERROR: Could not activate workflow" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Manual activation needed (30 seconds):" -ForegroundColor Yellow
    Write-Host "1. Open http://localhost:5678" -ForegroundColor White
    Write-Host "2. Click Workflows" -ForegroundColor White
    Write-Host "3. Find 'Judge Agent'" -ForegroundColor White
    Write-Host "4. Toggle Active switch" -ForegroundColor White
}
