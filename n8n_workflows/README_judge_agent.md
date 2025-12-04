# Judge Agent Workflow - Usage Guide

## Overview
The Judge Agent is part of the Continuous Learning Protocol (CLP-001) Slow Loop. It automatically scans EVENT_TIMELINE.jsonl every 6 hours and identifies "Faux Pas" (procedural errors worth learning from).

## Components Created
- ✅ `prompts/judge_agent_prompt.md` (151 lines) - Judge Agent system prompt with 4 Faux Pas taxonomy
- ✅ `n8n_workflows/judge_agent.json` (160 lines) - n8n workflow for automated error detection
- ✅ `truth-layer/drift/faux_pas/` - Directory for FauxPas reports

## Prerequisites
1. **n8n running** - `docker ps` should show `n8n-production` container
2. **OpenAI API Key** - Required for GPT-5.1 Judge calls
3. **EVENT_TIMELINE.jsonl exists** - Created by Observer (runs every 15 min)

## Installation Steps

### Step 1: Set OpenAI API Key in n8n
1. Open n8n: http://localhost:5678
2. Go to **Settings** → **Environment Variables**
3. Add: `OPENAI_API_KEY = sk-proj-...` (your key)
4. Restart n8n container:
   ```powershell
   docker restart n8n-production
   ```

### Step 2: Import Judge Agent Workflow
1. In n8n, click **+ Workflow** (top right)
2. Click **...** (three dots menu) → **Import from File**
3. Select: `C:\Users\edri2\Desktop\AI\ai-os\n8n_workflows\judge_agent.json`
4. Workflow will open with 5 nodes:
   - Schedule Trigger (every 6 hours)
   - Read Timeline Events (last 6 hours)
   - Prepare Judge Prompt (load prompt template)
   - Call GPT-5.1 Judge (analyze events)
   - Write FauxPas Report (save to truth-layer/)

### Step 3: Test Manually (Before Activating)
**DO NOT activate yet!** Test first:

1. **Force an error** (to have something for Judge to detect):
   ```powershell
   # Option A: Manually add an error event to timeline
   $errorEvent = @{
     ts_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
     type = "ERROR"
     payload = @{
       error_type = "capability_amnesia"
       description = "Test error: System used regex for CSV instead of Python tool"
       severity = "high"
     }
   } | ConvertTo-Json -Compress
   
   Add-Content -Path "C:\Users\edri2\Desktop\AI\ai-os\truth-layer\timeline\EVENT_TIMELINE.jsonl" -Value $errorEvent
   ```

2. **Manual Test Run** (in n8n):
   - Click **Execute Workflow** button (play icon)
   - Watch nodes turn green
   - Check console output for errors

3. **Verify Output**:
   ```powershell
   # Check if FauxPas report was created
   Get-ChildItem "C:\Users\edri2\Desktop\AI\ai-os\truth-layer\drift\faux_pas\"
   
   # View the report
   Get-Content "C:\Users\edri2\Desktop\AI\ai-os\truth-layer\drift\faux_pas\FP-*.json" | ConvertFrom-Json | ConvertTo-Json -Depth 10
   ```

4. **Expected Output** (if error was detected):
   ```json
   {
     "report_id": "FP-2025-12-04-14",
     "analyzed_at_utc": "2025-12-04T14:00:00Z",
     "time_window": {
       "start": "2025-12-04T08:00:00Z",
       "end": "2025-12-04T14:00:00Z"
     },
     "events_analyzed": 15,
     "faux_pas_detected": [
       {
         "fp_id": "FP-2025-12-04-001",
         "type": "capability_amnesia",
         "severity": "high",
         "timestamp": "2025-12-04T12:30:00Z",
         "description": "Test error detected",
         "recommended_lho": {
           "trigger_pattern": "task contains 'CSV'",
           "correction_strategy": "Use Python CSV tool",
           "priority": "high"
         }
       }
     ],
     "summary": {
       "capability_amnesia": 1,
       "constraint_blindness": 0,
       "loop_paralysis": 0,
       "hallucinated_affordances": 0
     }
   }
   ```

### Step 4: Activate (After Successful Test)
1. In n8n workflow editor, toggle **Active** switch (top right)
2. Judge Agent will now run automatically every 6 hours
3. Monitor: http://localhost:5678/executions

## How It Works

### 1. Schedule Trigger (Every 6 Hours)
- Triggers at: 00:00, 06:00, 12:00, 18:00 UTC
- Configurable: Edit node → Change "hoursInterval"

### 2. Read Timeline Events
- Opens: `truth-layer/timeline/EVENT_TIMELINE.jsonl`
- Filters: Events from last 6 hours only
- Output: JSON array of events

### 3. Prepare Judge Prompt
- Loads: `prompts/judge_agent_prompt.md`
- Appends: Events JSON
- Output: Full prompt for GPT-5.1

### 4. Call GPT-5.1 Judge
- Model: `gpt-5.1` (adaptive reasoning model)
- Temperature: 0.2 (low for consistency)
- Response Format: JSON object (structured output)
- Cost: ~$0.01-0.02 per analysis (cheaper than GPT-4o)

### 5. Write FauxPas Report
- Filename: `FP-YYYY-MM-DDTHH-MM-SS.json`
- Location: `truth-layer/drift/faux_pas/`
- Contains: Full analysis + recommended LHOs

## 4 Faux Pas Types (What Judge Looks For)

| Type | Name | Example |
|------|------|---------|
| I | **Capability Amnesia** | Used regex for CSV instead of Python tool (despite past failures) |
| II | **Constraint Blindness** | Modified file without updating documentation (violated rule) |
| III | **Loop Paralysis** | Tried same import 5 times without variation (stuck in retry loop) |
| IV | **Hallucinated Affordances** | Called tool with non-existent parameter (invented capability) |

## Monitoring

### Check Judge Status
```powershell
# n8n executions
docker logs n8n-production --tail 50

# Recent FauxPas reports
Get-ChildItem "C:\Users\edri2\Desktop\AI\ai-os\truth-layer\drift\faux_pas\" | Sort-Object LastWriteTime -Descending | Select-Object -First 5

# Count errors by type
$reports = Get-ChildItem "C:\Users\edri2\Desktop\AI\ai-os\truth-layer\drift\faux_pas\*.json"
$reports | ForEach-Object {
  $report = Get-Content $_.FullName | ConvertFrom-Json
  $report.summary
}
```

### n8n Dashboard
- URL: http://localhost:5678/executions
- Filter: "Judge Agent" workflow
- View: Execution history, success/failure rates, timing

## Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution:** Environment variable not set in n8n
```powershell
# Check Docker env vars
docker inspect n8n-production | Select-String "OPENAI_API_KEY"

# If missing, add to docker-compose.yml and restart
```

### Issue: "Cannot read EVENT_TIMELINE.jsonl"
**Solution:** Observer not running or timeline file missing
```powershell
# Check if Observer task exists
schtasks /Query /TN "\AI-OS\Observer-Drift-Detection"

# Manually create timeline if needed
New-Item -ItemType Directory -Path "C:\Users\edri2\Desktop\AI\ai-os\truth-layer\timeline" -Force
New-Item -ItemType File -Path "C:\Users\edri2\Desktop\AI\ai-os\truth-layer\timeline\EVENT_TIMELINE.jsonl" -Force
```

### Issue: "No events in last 6 hours"
**Normal:** If Observer hasn't detected drift, timeline might be empty
**Solution:** Force an error (see Step 3) or wait for Observer to run

### Issue: "GPT-5.1 returns empty faux_pas_detected"
**Normal:** Judge didn't find any learnable patterns (good!)
**Expected:** Most runs should be empty (system is learning over time)

## Next Steps

After Judge Agent is operational:
1. ✅ **Slice 2.5.4:** Teacher Agent (converts FauxPas → LHOs)
2. ✅ **Slice 2.5.5:** Librarian Agent (indexes LHOs in Qdrant)
3. ✅ **Slice 2.5.6:** Context Manager (injects LHOs into Fast Loop)

The Judge Agent is the **observer** of the Slow Loop. It detects, but doesn't fix. That's Teacher's job!

## Cost Estimate
- **Per Run:** ~$0.01-0.02 (GPT-5.1 analysis, 50% cheaper than GPT-4o)
- **Per Day:** 4 runs × $0.015 = ~$0.06/day
- **Per Month:** ~$1.80/month
- **Note:** Only charges when events exist (empty timeline = free run)

## Files Modified
- Created: `prompts/judge_agent_prompt.md`
- Created: `n8n_workflows/judge_agent.json`
- Created: `truth-layer/drift/faux_pas/` (directory)
- Modified: None (all additive)

---

**Status:** Ready for testing (NOT ACTIVATED YET)
**Next Action:** Follow Step 3 (Test Manually)
