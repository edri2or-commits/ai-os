# Judge Agent V2 - Langfuse Integration Setup

## Overview

Judge V2 reads traces from **Langfuse** instead of raw JSONL files.

**Benefits:**
- ✅ Visual debugging (timeline, spans, costs)
- ✅ Structured data (traces, spans, generations)
- ✅ Full context (input/output of every action)
- ✅ Cost tracking (automatic token counting)
- ✅ Professional observability (OpenTelemetry standard)

---

## Architecture

```
Claude Action → langfuse_logger.py → Langfuse API → PostgreSQL
                                            ↓
Judge Agent (n8n) ← Langfuse API (GET /traces)
       ↓
FauxPas Reports (JSON)
```

---

## Prerequisites

1. ✅ Langfuse V3 running (docker-compose up)
2. ✅ Langfuse SDK installed (`pip install langfuse`)
3. ✅ n8n running with OpenAI API key

---

## Setup Steps

### Step 1: Get Langfuse API Keys

1. Open Langfuse Dashboard: http://localhost:3000
2. **Create Account:**
   - Email: or@localhost.com (or any email)
   - Password: [choose secure password]
3. **Create Project:**
   - Name: "AI Life OS"
   - Click "Create Project"
4. **Copy API Keys:**
   - Go to **Settings** → **API Keys**
   - Copy:
     - **Public Key:** `pk-lf-xxxxxxxx`
     - **Secret Key:** `sk-lf-xxxxxxxx` (click "Show")

---

### Step 2: Configure Environment Variables

Add Langfuse keys to **n8n .env file**:

```bash
# File: infra/n8n/.env

# Existing keys...
OPENAI_API_KEY=sk-proj-...

# Add Langfuse keys:
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxx
LANGFUSE_HOST=http://host.docker.internal:3000
```

**Restart n8n:**

```powershell
cd C:\Users\edri2\Desktop\AI\ai-os\infra\n8n
docker-compose restart
```

---

### Step 3: Test Langfuse Logger

Run test script to verify connection:

```powershell
cd C:\Users\edri2\Desktop\AI\ai-os

# Set keys (temporary - this session only)
$env:LANGFUSE_PUBLIC_KEY = "pk-lf-YOUR_KEY"
$env:LANGFUSE_SECRET_KEY = "sk-lf-YOUR_KEY"
$env:LANGFUSE_HOST = "http://localhost:3000"

# Run test
python tools/langfuse_logger.py
```

**Expected output:**
```
Testing Langfuse Logger...
✅ Logged test action: trace-abc123
✅ Logged tool call: trace-def456
✅ Logged conversation: trace-ghi789

🎉 All tests passed! Check Langfuse dashboard: http://localhost:3000
```

**Verify in Dashboard:**
- Go to http://localhost:3000/traces
- You should see 3 test traces

---

### Step 4: Import Judge V2 Workflow to n8n

**Option A: Via n8n UI (Recommended)**

1. Open n8n: http://localhost:5678
2. Click **"Workflows"** → **"Import from File"**
3. Select: `C:\Users\edri2\Desktop\AI\ai-os\n8n_workflows\judge_agent_v2_langfuse.json`
4. Click **"Import"**
5. **Activate Workflow:**
   - Click toggle switch (top right)
   - Status should show "Active" ✅

**Option B: Via CLI**

```powershell
docker exec ai_os_n8n n8n import:workflow --input=/workspace/n8n_workflows/judge_agent_v2_langfuse.json
```

---

### Step 5: Test Judge V2

**Manual Test:**

1. Open n8n workflow: "Judge Agent V2 - Langfuse Integration"
2. Click **"Execute Workflow"** (top right)
3. Wait 10-15 seconds
4. **Check Results:**
   - Node outputs should show traces fetched
   - FauxPas report written to: `truth-layer/drift/faux_pas/FP-YYYY-MM-DD...json`

**Expected Behavior:**

```json
{
  "summary": "Analyzed 3 traces from last 6 hours. No faux pas detected.",
  "faux_pas_detected": [],
  "traces_analyzed": 3
}
```

---

## Usage

### Logging Claude Actions (Protocol 1)

**From Python scripts:**

```python
from tools.langfuse_logger import log_action, log_tool_call

# Log a file edit
log_action(
    action_type="file_edit",
    details={"file": "test.py", "lines_changed": 5},
    status="success"
)

# Log a tool call
log_tool_call(
    tool_name="git_commit",
    tool_args={"message": "feat: add feature X"},
    tool_result={"commit_hash": "abc1234"},
    duration_ms=120.5
)
```

**From Claude Desktop (future):**

Will require MCP server wrapper to intercept tool calls.

---

### Viewing Traces in Langfuse

**Dashboard:** http://localhost:3000

**Key Views:**

1. **Traces:** Timeline of all actions
   - Filter by tags: `claude_action`, `tool_call`, `conversation`
   - Click trace → see full details (input/output, duration, cost)

2. **Sessions:** Group related actions
   - One chat = one session
   - See full flow of work

3. **Users:** Filter by user
   - Currently: just "or"

4. **Scores:** Quality ratings
   - Judge can add scores to traces
   - Track improvement over time

---

## Differences from V1 (JSONL)

| Feature | V1 (JSONL) | V2 (Langfuse) |
|---------|-----------|---------------|
| Storage | Plain text file | PostgreSQL + ClickHouse |
| Querying | Manual file parsing | REST API |
| Visualization | None | Timeline, graphs, filters |
| Context | Raw events only | Full traces (input/output/spans) |
| Cost tracking | Manual | Automatic |
| Retention | Forever (until deleted) | Configurable (30/60/90 days) |
| Search | Text search | Semantic search + filters |

---

## Troubleshooting

### Issue: "Failed to connect to Langfuse"

**Cause:** API keys not set or Langfuse not running

**Fix:**
1. Check Langfuse is up: `docker ps | grep langfuse`
2. Verify keys in `.env`
3. Restart n8n: `docker-compose restart`

---

### Issue: "No traces found (last 6hr)"

**Cause:** No actions logged yet

**Fix:**
1. Run test: `python tools/langfuse_logger.py`
2. Verify traces appear in dashboard
3. Run Judge workflow again

---

### Issue: "GPT-4o API key invalid"

**Cause:** OpenAI API key missing or expired

**Fix:**
1. Check `infra/n8n/.env` has `OPENAI_API_KEY=sk-proj-...`
2. Test key: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $KEY"`

---

## Next Steps (Slice 2.5.6)

After Judge V2 is operational:

1. **Teacher Agent:** Convert errors → LHOs (Life Handling Objects)
2. **Librarian Agent:** Index LHOs in Qdrant
3. **Context Manager:** Inject LHOs before tasks

---

## Cost Analysis

**Langfuse:** $0/month (self-hosted)

**Judge V2:**
- GPT-4o: $0.015/run × 4 runs/day = $1.80/month
- (Down from GPT-5.1 $3.60/month)

**Storage:**
- Langfuse DB: ~100MB/month (traces)
- Negligible on local disk

**Total:** ~$2/month (vs infrastructure-only JSONL)

---

## Status

- ✅ Langfuse V3 operational
- ✅ Logger script created (`langfuse_logger.py`)
- ✅ Judge V2 workflow created (`judge_agent_v2_langfuse.json`)
- ⏳ **Pending:** Get API keys from Langfuse dashboard
- ⏳ **Pending:** Import workflow to n8n
- ⏳ **Pending:** First test run

---

**Last Updated:** 2025-12-05  
**Author:** AI Life OS (Claude + Or)  
**Version:** 2.0 (Langfuse Integration)
