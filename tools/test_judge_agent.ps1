# Test Judge Agent - Force Error & Verify Detection
# Purpose: Create a test error in EVENT_TIMELINE.jsonl and verify Judge Agent detects it

Write-Host "🧪 Judge Agent Test Script" -ForegroundColor Cyan
Write-Host "=" * 50

# Step 1: Create test error event
Write-Host "`n[1/4] Creating test error event..." -ForegroundColor Yellow

$testError = @{
    ts_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
    type = "ERROR"
    payload = @{
        error_type = "capability_amnesia"
        task = "Parse sales_data.csv"
        description = "System attempted to use regex for CSV parsing despite Python CSV tool availability"
        tool_used = "regex_parse"
        tool_result = "FAILED: Unescaped comma in quoted field"
        correct_tool = "python_csv"
        severity = "high"
        repeated = $true
        session_count = 2
    }
} | ConvertTo-Json -Compress

$timelineFile = "C:\Users\edri2\Desktop\AI\ai-os\truth-layer\timeline\EVENT_TIMELINE.jsonl"

if (-not (Test-Path $timelineFile)) {
    Write-Host "   Creating EVENT_TIMELINE.jsonl..." -ForegroundColor Gray
    New-Item -ItemType Directory -Path (Split-Path $timelineFile) -Force | Out-Null
    New-Item -ItemType File -Path $timelineFile -Force | Out-Null
}

Add-Content -Path $timelineFile -Value $testError
Write-Host "   ✅ Test error added to timeline" -ForegroundColor Green

# Step 2: Verify n8n is running
Write-Host "`n[2/4] Checking n8n status..." -ForegroundColor Yellow

$n8nRunning = docker ps --filter "name=n8n-production" --format "{{.Status}}" 2>$null
if ($n8nRunning -like "*Up*") {
    Write-Host "   ✅ n8n is running: $n8nRunning" -ForegroundColor Green
} else {
    Write-Host "   ❌ n8n is NOT running!" -ForegroundColor Red
    Write-Host "   Start it with: docker start n8n-production" -ForegroundColor Yellow
    exit 1
}

# Step 3: Instructions for manual test
Write-Host "`n[3/4] Manual Test Instructions:" -ForegroundColor Yellow
Write-Host "   1. Open n8n: " -NoNewline
Write-Host "http://localhost:5678" -ForegroundColor Cyan
Write-Host "   2. Navigate to 'Judge Agent' workflow"
Write-Host "   3. Click 'Execute Workflow' button (play icon)"
Write-Host "   4. Wait for all nodes to turn green"
Write-Host "   5. Check output: Should detect 1 capability_amnesia error"

Write-Host "`n   Press ENTER after you've executed the workflow..." -ForegroundColor Magenta
Read-Host

# Step 4: Verify report was created
Write-Host "`n[4/4] Verifying FauxPas report..." -ForegroundColor Yellow

$reportsDir = "C:\Users\edri2\Desktop\AI\ai-os\truth-layer\drift\faux_pas"
$latestReport = Get-ChildItem $reportsDir -Filter "FP-*.json" -ErrorAction SilentlyContinue | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 1

if ($latestReport) {
    Write-Host "   ✅ Report found: $($latestReport.Name)" -ForegroundColor Green
    
    $report = Get-Content $latestReport.FullName | ConvertFrom-Json
    
    Write-Host "`n📊 Report Summary:" -ForegroundColor Cyan
    Write-Host "   Report ID: $($report.report_id)"
    Write-Host "   Analyzed At: $($report.analyzed_at_utc)"
    Write-Host "   Events Analyzed: $($report.events_analyzed)"
    
    Write-Host "`n🔍 Errors Detected:" -ForegroundColor Cyan
    Write-Host "   Capability Amnesia: $($report.summary.capability_amnesia)"
    Write-Host "   Constraint Blindness: $($report.summary.constraint_blindness)"
    Write-Host "   Loop Paralysis: $($report.summary.loop_paralysis)"
    Write-Host "   Hallucinated Affordances: $($report.summary.hallucinated_affordances)"
    
    if ($report.faux_pas_detected.Count -gt 0) {
        Write-Host "`n✅ TEST PASSED: Judge Agent detected the test error!" -ForegroundColor Green
        Write-Host "`nDetected Errors:" -ForegroundColor Yellow
        foreach ($fp in $report.faux_pas_detected) {
            Write-Host "   - Type: $($fp.type)"
            Write-Host "     Severity: $($fp.severity)"
            Write-Host "     Description: $($fp.description)"
            if ($fp.recommended_lho) {
                Write-Host "     Recommended LHO: $($fp.recommended_lho.correction_strategy)"
            }
            Write-Host ""
        }
    } else {
        Write-Host "`n⚠️  Warning: No errors detected in report" -ForegroundColor Yellow
        Write-Host "   This might be normal if timeline had no recent events"
    }
    
    Write-Host "`n📄 Full Report:" -ForegroundColor Cyan
    Write-Host $latestReport.FullName -ForegroundColor Gray
    
} else {
    Write-Host "   ❌ No FauxPas report found!" -ForegroundColor Red
    Write-Host "   Expected location: $reportsDir" -ForegroundColor Yellow
    Write-Host "   Make sure you executed the workflow in n8n"
}

Write-Host "`n" + ("=" * 50)
Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. If test passed: Activate workflow in n8n (toggle 'Active' switch)"
Write-Host "   2. Monitor: http://localhost:5678/executions"
Write-Host "   3. Next Slice: Teacher Agent (converts FauxPas → LHOs)"
