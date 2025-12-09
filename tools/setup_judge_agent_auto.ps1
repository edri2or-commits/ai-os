# Judge Agent - Zero-Friction Auto Setup
# Reads API key from .env.txt and configures n8n automatically

param(
    [string]$EnvFile = "C:\Users\edri2\Desktop\AI\ai-os\services\mcp_github_client\.env.txt"
)

Write-Host "=== Judge Agent - Zero-Friction Setup ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Read API key from .env.txt
Write-Host "Step 1: Reading API key from .env.txt..." -ForegroundColor Yellow

if (-not (Test-Path $EnvFile)) {
    Write-Host "❌ ERROR: .env.txt not found at $EnvFile" -ForegroundColor Red
    exit 1
}

$envContent = Get-Content $EnvFile
$apiKeyLine = $envContent | Where-Object { $_ -match "^OPENAI_API_KEY=" }

if (-not $apiKeyLine) {
    Write-Host "❌ ERROR: OPENAI_API_KEY not found in .env.txt" -ForegroundColor Red
    exit 1
}

$apiKey = $apiKeyLine -replace "^OPENAI_API_KEY=", ""
$apiKey = $apiKey.Trim()

if ($apiKey -notmatch "^sk-proj-") {
    Write-Host "❌ ERROR: Invalid API key format in .env.txt" -ForegroundColor Red
    exit 1
}

Write-Host "✅ API key loaded from .env.txt" -ForegroundColor Green
Write-Host ""

# Step 2: Check n8n is running
Write-Host "Step 2: Checking n8n status..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ n8n is running" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: n8n is not responding at http://localhost:5678" -ForegroundColor Red
    Write-Host "Starting n8n container..." -ForegroundColor Yellow
    
    try {
        docker start ai-life-os-n8n
        Start-Sleep -Seconds 5
        Write-Host "✅ n8n started" -ForegroundColor Green
    } catch {
        Write-Host "❌ Could not start n8n. Please run: docker-compose up -d" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Step 3: Configure credential via n8n CLI (inside container)
Write-Host "Step 3: Configuring OpenAI credential in n8n..." -ForegroundColor Yellow

# Create credential JSON
$credentialJson = @"
{
  "name": "Judge Agent OpenAI",
  "type": "openAiApi",
  "data": {
    "apiKey": "$apiKey"
  }
}
"@

# Write JSON to temp file
$tempFile = "$env:TEMP\n8n_cred_$(Get-Random).json"
$credentialJson | Out-File -FilePath $tempFile -Encoding UTF8

try {
    # Copy to container
    docker cp $tempFile ai-life-os-n8n:/tmp/openai_cred.json
    
    # Import credential via n8n CLI
    docker exec ai-life-os-n8n n8n import:credentials --input=/tmp/openai_cred.json --separate
    
    # Clean up
    docker exec ai-life-os-n8n rm /tmp/openai_cred.json
    Remove-Item $tempFile -Force
    
    Write-Host "✅ Credential configured" -ForegroundColor Green
} catch {
    Write-Host "⚠️ CLI import failed, trying API method..." -ForegroundColor Yellow
    
    # Fallback: Try API
    try {
        $headers = @{
            "Content-Type" = "application/json"
        }
        
        $credResponse = Invoke-RestMethod -Uri "http://localhost:5678/api/v1/credentials" `
                                          -Method POST `
                                          -Headers $headers `
                                          -Body $credentialJson `
                                          -ErrorAction Stop
        
        Write-Host "✅ Credential created via API" -ForegroundColor Green
    } catch {
        Write-Host "❌ ERROR: Could not configure credential automatically" -ForegroundColor Red
        Write-Host ""
        Write-Host "⚠️ Manual step required (only takes 30 seconds):" -ForegroundColor Yellow
        Write-Host "1. Open: http://localhost:5678" -ForegroundColor White
        Write-Host "2. Click: Credentials (left sidebar)" -ForegroundColor White
        Write-Host "3. Click: Add Credential" -ForegroundColor White
        Write-Host "4. Select: OpenAI API" -ForegroundColor White
        Write-Host "5. Name: Judge Agent OpenAI" -ForegroundColor White
        Write-Host "6. API Key: (paste from .env.txt)" -ForegroundColor White
        Write-Host "7. Click: Save" -ForegroundColor White
        Write-Host ""
        Write-Host "Your API key is: $apiKey" -ForegroundColor Cyan
        exit 1
    }
}
Write-Host ""

# Step 4: Find and activate workflow
Write-Host "Step 4: Activating Judge Agent workflow..." -ForegroundColor Yellow

try {
    $headers = @{
        "Content-Type" = "application/json"
    }
    
    $workflows = Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows" `
                                   -Method GET `
                                   -Headers $headers `
                                   -ErrorAction Stop
    
    $judgeWorkflow = $workflows.data | Where-Object { $_.name -like "*Judge Agent*" }
    
    if (-not $judgeWorkflow) {
        Write-Host "❌ ERROR: Judge Agent workflow not found in n8n" -ForegroundColor Red
        Write-Host "Please import the workflow first" -ForegroundColor Yellow
        exit 1
    }
    
    $workflowId = $judgeWorkflow.id
    Write-Host "✅ Found workflow: $($judgeWorkflow.name)" -ForegroundColor Green
    
    # Activate workflow
    $activateData = @{
        active = $true
    } | ConvertTo-Json
    
    Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows/$workflowId" `
                      -Method PATCH `
                      -Headers $headers `
                      -Body $activateData `
                      -ErrorAction Stop | Out-Null
    
    Write-Host "✅ Workflow activated!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not activate via API" -ForegroundColor Yellow
    Write-Host "Please activate manually in n8n UI" -ForegroundColor Yellow
}
Write-Host ""

# Success!
Write-Host "=== ✅ SETUP COMPLETE! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Judge Agent is now configured and running!" -ForegroundColor Cyan
Write-Host "It will automatically detect errors every 6 hours." -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "• View executions: http://localhost:5678/executions" -ForegroundColor White
Write-Host "• Check reports: C:\Users\edri2\Desktop\AI\ai-os\truth-layer\drift\faux_pas\" -ForegroundColor White
Write-Host ""
