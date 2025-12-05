# Judge Agent - Auto Setup Script
# This script configures OpenAI API key in n8n and activates Judge Agent workflow

Write-Host "=== Judge Agent - Auto Setup ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Get API key from user
Write-Host "Step 1: API Key Input" -ForegroundColor Yellow
Write-Host "Please paste your OpenAI API key (sk-proj-...):" -ForegroundColor White
$apiKey = Read-Host -AsSecureString
$apiKeyPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey))

if ($apiKeyPlain -notmatch "^sk-proj-") {
    Write-Host "ERROR: Invalid API key format. Should start with 'sk-proj-'" -ForegroundColor Red
    exit 1
}

Write-Host "✅ API key received" -ForegroundColor Green
Write-Host ""

# Step 2: Check n8n is running
Write-Host "Step 2: Checking n8n status..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ n8n is running" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: n8n is not responding at http://localhost:5678" -ForegroundColor Red
    Write-Host "Please start n8n first: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Step 3: Create OpenAI credential in n8n
Write-Host "Step 3: Creating OpenAI credential in n8n..." -ForegroundColor Yellow

$credentialData = @{
    name = "Judge Agent OpenAI"
    type = "openAiApi"
    data = @{
        apiKey = $apiKeyPlain
    }
} | ConvertTo-Json -Depth 10

try {
    $headers = @{
        "Content-Type" = "application/json"
    }
    
    # Note: n8n API requires authentication. 
    # If you have N8N_API_KEY set, we'll use it. Otherwise, we'll try without auth (local only).
    if ($env:N8N_API_KEY) {
        $headers["X-N8N-API-KEY"] = $env:N8N_API_KEY
    }
    
    $credResponse = Invoke-RestMethod -Uri "http://localhost:5678/api/v1/credentials" `
                                      -Method POST `
                                      -Headers $headers `
                                      -Body $credentialData `
                                      -ErrorAction Stop
    
    $credentialId = $credResponse.id
    Write-Host "✅ Credential created (ID: $credentialId)" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Failed to create credential" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "⚠️ Manual fallback required:" -ForegroundColor Yellow
    Write-Host "1. Open http://localhost:5678" -ForegroundColor White
    Write-Host "2. Go to Credentials → Add Credential → OpenAI API" -ForegroundColor White
    Write-Host "3. Paste your API key and save as 'Judge Agent OpenAI'" -ForegroundColor White
    exit 1
}
Write-Host ""

# Step 4: Find Judge Agent workflow
Write-Host "Step 4: Finding Judge Agent workflow..." -ForegroundColor Yellow
try {
    $workflows = Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows" `
                                   -Method GET `
                                   -Headers $headers `
                                   -ErrorAction Stop
    
    $judgeWorkflow = $workflows | Where-Object { $_.name -like "*Judge Agent*" }
    
    if (-not $judgeWorkflow) {
        Write-Host "❌ ERROR: Judge Agent workflow not found" -ForegroundColor Red
        Write-Host "Please import the workflow first" -ForegroundColor Yellow
        exit 1
    }
    
    $workflowId = $judgeWorkflow.id
    Write-Host "✅ Found workflow: $($judgeWorkflow.name) (ID: $workflowId)" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Failed to list workflows" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 5: Activate workflow
Write-Host "Step 5: Activating workflow..." -ForegroundColor Yellow
try {
    $activateData = @{
        active = $true
    } | ConvertTo-Json
    
    $activateResponse = Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows/$workflowId" `
                                          -Method PATCH `
                                          -Headers $headers `
                                          -Body $activateData `
                                          -ErrorAction Stop
    
    Write-Host "✅ Workflow activated!" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Failed to activate workflow" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 6: Test execution
Write-Host "Step 6: Testing execution..." -ForegroundColor Yellow
Write-Host "⚠️ Note: First execution may take 10-20 seconds" -ForegroundColor Yellow
try {
    $testResponse = Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows/$workflowId/activate" `
                                      -Method POST `
                                      -Headers $headers `
                                      -ErrorAction Stop
    
    Write-Host "✅ Test execution started" -ForegroundColor Green
    Write-Host "Check n8n UI for results: http://localhost:5678" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️ Could not trigger test (this is optional)" -ForegroundColor Yellow
}
Write-Host ""

# Success!
Write-Host "=== ✅ SUCCESS! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Judge Agent is now running automatically every 6 hours!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Check execution: http://localhost:5678/workflow/$workflowId" -ForegroundColor White
Write-Host "2. View FauxPas reports: C:\Users\edri2\Desktop\AI\ai-os\truth-layer\drift\faux_pas\" -ForegroundColor White
Write-Host ""

# Clean up sensitive data
$apiKeyPlain = $null
[System.GC]::Collect()
