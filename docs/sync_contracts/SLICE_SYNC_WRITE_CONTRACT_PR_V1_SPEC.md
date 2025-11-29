# SLICE_SYNC_WRITE_CONTRACT_PR_V1 - Detailed Spec (UPDATED)

**Date:** 2025-11-27 (Updated after review)  
**Phase:** 2.3 (INFRA_ONLY)  
**Goal:** First Sync Write Contract - GitHub PR Creation  
**Pattern:** Transactional Outbox for asynchronous PR creation

---

## 🔍 Discovery Results

### Current State (Verified from Repo)

**1. mcp_github_client Service** ✅ Operational
- **Location:** `services/mcp_github_client/`
- **Port:** 8081 (from config.py)
- **Endpoint:** `POST /github/open-pr`

**What it does (verified from routes_github.py):**
1. Creates a new branch from `base_branch` (auto-generated name: `ai-os-pr-{timestamp}`)
2. Writes all files from `files[]` to the new branch
3. Creates a PR from new branch to `base_branch`
4. (Optional) Uses AI to refine PR description

**Request Parameters:**
```python
{
  "title": str,               # PR title
  "description": str,         # PR description/body
  "files": [FileChange],      # List of file changes
  "base_branch": str,         # Default: "main"
  "use_ai_generation": bool   # Default: false
}

FileChange:
{
  "path": str,                # File path (e.g., "docs/example.md")
  "content": str,             # FULL file content
  "operation": str            # "create"|"update"|"delete"
}
```

**Response Structure (SUCCESS):**
```python
{
  "ok": True,
  "pr_number": 123,                              # int
  "pr_url": "https://github.com/.../pull/123",   # string
  "branch_name": "ai-os-pr-20251127-230010",     # string (auto-generated)
  "message": "Pull Request created successfully"
}
```

**Response Structure (FAILURE):**
```python
{
  "ok": False,
  "error_type": "branch_creation_failed" | "file_update_failed" | "pr_creation_failed",
  "message": "Failed to create branch: ..."
}
```

**2. Existing Script:** `scripts/open_pr_for_branch.py`
- Works with pre-existing pushed branches
- Uses PyGithub library directly
- **Not used in this slice** - we're using mcp_github_client HTTP API

**3. Current Events in TIMELINE:**
- Found one example: `PR_OPENED_SLICE_GOVERNANCE_TRUTH_BOOTSTRAP_V1`
- No standardized PR intent/contract events yet

**4. No Outbox Infrastructure:**
- `docs/system_state/outbox/` does not exist
- Will be created in this slice

---

## 🎯 Objectives

### V1 Scope (This Slice)

1. **Create Intent Layer (Transactional Outbox)**
   - JSONL file for PR creation intents
   - Each intent = full specification for one PR
   - Intents persist until successfully executed

2. **Create Worker/Executor**
   - Python script `scripts/pr_worker.py`
   - Polls outbox, executes pending intents
   - Marks intents as processed (completed/failed)

3. **Standardize Events**
   - `PR_INTENT_CREATED`
   - `PR_INTENT_PROCESSING`
   - `PR_CREATED` (success)
   - `PR_CREATION_FAILED` (failure)

4. **Testing**
   - Manual intent creation
   - Execution end-to-end
   - Failure handling

### Not in V1 Scope

❌ **Automatic intent creation** - Only manual/scripted for now  
❌ **Retry logic** - Failed intents stay failed (manual re-process)  
❌ **Multiple workers** - Single worker instance  
❌ **Scheduled polling** - Manual execution only  
❌ **Intent expiration** - No TTL  
❌ **Live automations** - Still INFRA_ONLY  
❌ **Idempotency guarantees** - At-least-once, duplicates possible

---

## 📐 Architecture Design

```
┌──────────────────────────────────────────────────────────┐
│              Intent Layer (Outbox)                       │
│  docs/system_state/outbox/PR_INTENTS.jsonl               │
│                                                          │
│  Each line = one intent (JSONL format):                  │
│  {                                                       │
│    "intent_id": "pr-intent-{timestamp}-{random}",        │
│    "created_at": "2025-11-27T23:00:00Z",                 │
│    "created_by": "infra-operator",                       │
│    "status": "pending",  // or processing/completed/failed │
│    "pr_spec": {                                          │
│      "title": "SLICE_EXAMPLE - Description",            │
│      "description": "Full PR body...",                   │
│      "files": [                                          │
│        {                                                 │
│          "path": "docs/EXAMPLE.md",                      │
│          "content": "# Example\n\nFull content...",      │
│          "operation": "create"                           │
│        }                                                 │
│      ],                                                  │
│      "base_branch": "main",                              │
│      "use_ai_generation": false                          │
│    },                                                    │
│    "trace_id": "pr-intent-{timestamp}-{random}",         │
│    "result": null,  // Filled after success              │
│    "error": null,   // Filled after failure              │
│    "processed_at": null                                  │
│  }                                                       │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│           Worker/Executor (scripts/pr_worker.py)         │
│                                                          │
│  FLOW:                                                   │
│  1. Read PR_INTENTS.jsonl into memory                    │
│  2. Filter: status == "pending"                          │
│  3. For each pending intent:                             │
│     a. Set status = "processing"                         │
│     b. Write back to file                                │
│     c. Log PR_INTENT_PROCESSING event                    │
│     d. POST http://localhost:8081/github/open-pr         │
│        Body: intent.pr_spec                              │
│     e. If ok==True:                                      │
│        - Set result = {pr_number, pr_url, branch_name}   │
│        - Set status = "completed"                        │
│        - Set processed_at = now()                        │
│        - Write back to file                              │
│        - Log PR_CREATED event                            │
│     f. Else:                                             │
│        - Set error = response.message                    │
│        - Set error_type = response.error_type            │
│        - Set status = "failed"                           │
│        - Set processed_at = now()                        │
│        - Write back to file                              │
│        - Log PR_CREATION_FAILED event                    │
│  4. Print summary: X completed, Y failed                 │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│       mcp_github_client Service (port 8081)              │
│       POST /github/open-pr                               │
│                                                          │
│       What it does:                                      │
│       1. Creates branch (auto-named: ai-os-pr-{timestamp}) │
│       2. Commits all files to branch                     │
│       3. Opens PR to base_branch                         │
│                                                          │
│       Returns: pr_number, pr_url, branch_name            │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│              EVENT_TIMELINE.jsonl                        │
│                                                          │
│  PR_INTENT_CREATED → PR_INTENT_PROCESSING →              │
│  PR_CREATED | PR_CREATION_FAILED                         │
└──────────────────────────────────────────────────────────┘
```

---

## 🔧 Implementation Details

### 1. Intent Schema (PR_INTENTS.jsonl)

**File Location:** `docs/system_state/outbox/PR_INTENTS.jsonl`

**Format:** JSONL (one JSON object per line)

**Intent Structure:**
```json
{
  "intent_id": "pr-intent-1732748400-x7k9m2",
  "created_at": "2025-11-27T23:00:00.000Z",
  "created_by": "infra-operator",
  "status": "pending",
  "pr_spec": {
    "title": "SLICE_EXAMPLE_V1 - Add new feature",
    "description": "This PR adds...\n\n## Changes\n- Added EXAMPLE.md\n- Updated config",
    "files": [
      {
        "path": "docs/EXAMPLE.md",
        "content": "# Example\n\nFull file content here...\n\nMore lines...",
        "operation": "create"
      },
      {
        "path": "config/settings.json",
        "content": "{\"key\": \"value\"}",
        "operation": "update"
      }
    ],
    "base_branch": "main",
    "use_ai_generation": false
  },
  "trace_id": "pr-intent-1732748400-x7k9m2",
  "result": null,
  "error": null,
  "error_type": null,
  "processed_at": null
}
```

**After Successful Processing:**
```json
{
  "intent_id": "pr-intent-1732748400-x7k9m2",
  "status": "completed",
  "result": {
    "pr_number": 22,
    "pr_url": "https://github.com/edri2or-commits/ai-os/pull/22",
    "branch_name": "ai-os-pr-20251127-230010"
  },
  "processed_at": "2025-11-27T23:00:15.000Z",
  ...
}
```

**After Failed Processing:**
```json
{
  "intent_id": "pr-intent-1732748400-x7k9m2",
  "status": "failed",
  "error": "Failed to create branch: Branch already exists",
  "error_type": "branch_creation_failed",
  "processed_at": "2025-11-27T23:00:15.000Z",
  ...
}
```

**Status Values:**
- `pending` - Not yet processed by worker
- `processing` - Currently being executed (locks against concurrent processing)
- `completed` - Successfully created PR
- `failed` - Execution failed (see error field)

**File Management:**
- **V1 Approach:** Update-in-place
  - Read entire file into memory
  - Update intent object
  - Write back entire file
  - Simple, works for small number of intents
- **Future:** Append-only with compaction

---

### 2. Worker Script (scripts/pr_worker.py)

**Purpose:** Process pending PR intents

**Execution:** Manual (for V1)
```bash
python scripts/pr_worker.py
```

**Detailed Flow:**

```python
#!/usr/bin/env python3
"""
PR Worker - Processes pending PR intents

Reads PR_INTENTS.jsonl, executes pending intents via mcp_github_client,
updates status, and logs events to EVENT_TIMELINE.jsonl.
"""

import json
import httpx
from datetime import datetime
from pathlib import Path

INTENTS_FILE = Path("docs/system_state/outbox/PR_INTENTS.jsonl")
TIMELINE_FILE = Path("docs/system_state/timeline/EVENT_TIMELINE.jsonl")
MCP_GITHUB_URL = "http://localhost:8081/github/open-pr"

def main():
    # 1. Load intents
    intents = load_intents(INTENTS_FILE)
    
    # 2. Filter pending
    pending = [i for i in intents if i.get("status") == "pending"]
    
    print(f"[INFO] Found {len(pending)} pending intent(s)")
    
    # 3. Process each
    completed_count = 0
    failed_count = 0
    
    for intent in pending:
        intent_id = intent["intent_id"]
        print(f"\n[INFO] Processing intent: {intent_id}")
        
        # 3a. Mark as processing
        intent["status"] = "processing"
        save_intents(INTENTS_FILE, intents)
        log_event("PR_INTENT_PROCESSING", {"intent_id": intent_id, "pr_title": intent["pr_spec"]["title"]})
        
        # 3d. Call API
        try:
            response = httpx.post(
                MCP_GITHUB_URL,
                json=intent["pr_spec"],
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            
            # 3e. Success path
            if result.get("ok"):
                intent["status"] = "completed"
                intent["result"] = {
                    "pr_number": result["pr_number"],
                    "pr_url": result["pr_url"],
                    "branch_name": result["branch_name"]
                }
                intent["processed_at"] = datetime.utcnow().isoformat() + "Z"
                save_intents(INTENTS_FILE, intents)
                log_event("PR_CREATED", {
                    "intent_id": intent_id,
                    "pr_number": result["pr_number"],
                    "pr_url": result["pr_url"],
                    "pr_title": intent["pr_spec"]["title"]
                })
                print(f"[SUCCESS] PR created: #{result['pr_number']}")
                completed_count += 1
            
            # 3f. Failure path (ok=False)
            else:
                intent["status"] = "failed"
                intent["error"] = result.get("message", "Unknown error")
                intent["error_type"] = result.get("error_type", "unknown")
                intent["processed_at"] = datetime.utcnow().isoformat() + "Z"
                save_intents(INTENTS_FILE, intents)
                log_event("PR_CREATION_FAILED", {
                    "intent_id": intent_id,
                    "error": intent["error"],
                    "error_type": intent["error_type"],
                    "pr_title": intent["pr_spec"]["title"]
                })
                print(f"[ERROR] Failed: {intent['error']}")
                failed_count += 1
        
        except Exception as e:
            # 3f. Exception path
            intent["status"] = "failed"
            intent["error"] = str(e)
            intent["error_type"] = "connection_error"
            intent["processed_at"] = datetime.utcnow().isoformat() + "Z"
            save_intents(INTENTS_FILE, intents)
            log_event("PR_CREATION_FAILED", {
                "intent_id": intent_id,
                "error": str(e),
                "error_type": "connection_error",
                "pr_title": intent["pr_spec"]["title"]
            })
            print(f"[ERROR] Exception: {e}")
            failed_count += 1
    
    # 4. Summary
    print(f"\n[SUMMARY] {completed_count} completed, {failed_count} failed")

def load_intents(path):
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def save_intents(path, intents):
    with open(path, 'w', encoding='utf-8') as f:
        for intent in intents:
            f.write(json.dumps(intent, ensure_ascii=False) + '\n')

def log_event(event_type, payload):
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "source": "pr_worker",
        "payload": payload
    }
    with open(TIMELINE_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(event, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    main()
```

**Error Handling:**
- `httpx.RequestError` → connection_error
- `response.ok == False` → GitHub API error
- Invalid JSON → parsing error (shouldn't happen if intents are valid)

---

### 3. Events (EVENT_TIMELINE.jsonl)

**New Event Types:**

**PR_INTENT_CREATED** (logged by create_pr_intent.py)
```json
{
  "timestamp": "2025-11-27T23:00:00.000Z",
  "event_type": "PR_INTENT_CREATED",
  "source": "create_pr_intent",
  "payload": {
    "intent_id": "pr-intent-1732748400-x7k9m2",
    "pr_title": "SLICE_EXAMPLE_V1",
    "created_by": "infra-operator",
    "files_count": 2
  }
}
```

**PR_INTENT_PROCESSING** (logged by pr_worker.py)
```json
{
  "timestamp": "2025-11-27T23:00:05.000Z",
  "event_type": "PR_INTENT_PROCESSING",
  "source": "pr_worker",
  "payload": {
    "intent_id": "pr-intent-1732748400-x7k9m2",
    "pr_title": "SLICE_EXAMPLE_V1"
  }
}
```

**PR_CREATED** (logged by pr_worker.py on success)
```json
{
  "timestamp": "2025-11-27T23:00:10.000Z",
  "event_type": "PR_CREATED",
  "source": "pr_worker",
  "payload": {
    "intent_id": "pr-intent-1732748400-x7k9m2",
    "pr_number": 22,
    "pr_url": "https://github.com/edri2or-commits/ai-os/pull/22",
    "branch_name": "ai-os-pr-20251127-230010",
    "pr_title": "SLICE_EXAMPLE_V1"
  }
}
```

**PR_CREATION_FAILED** (logged by pr_worker.py on failure)
```json
{
  "timestamp": "2025-11-27T23:00:10.000Z",
  "event_type": "PR_CREATION_FAILED",
  "source": "pr_worker",
  "payload": {
    "intent_id": "pr-intent-1732748400-x7k9m2",
    "pr_title": "SLICE_EXAMPLE_V1",
    "error_type": "github_api_error",
    "error": "Branch already exists"
  }
}
```

---

### 4. Helper Script (scripts/create_pr_intent.py)

**Purpose:** Create a PR intent easily from command line

**Usage:**
```bash
python scripts/create_pr_intent.py \
  --title "SLICE_EXAMPLE_V1 - Add feature" \
  --description-file pr_description.txt \
  --file docs/EXAMPLE.md:example_content.txt \
  --file config/settings.json:settings.json
```

**Arguments:**
- `--title` - PR title (required)
- `--description-file` - Path to file containing PR description
- `--file PATH:CONTENT_FILE` - File to include (can specify multiple times)
  - PATH = path in repo (e.g., `docs/EXAMPLE.md`)
  - CONTENT_FILE = local file with content
- `--operation` - Default operation for files (`create` or `update`, default: `create`)
- `--base-branch` - Base branch (default: `main`)

**Flow:**
1. Generate intent_id (`pr-intent-{timestamp}-{random}`)
2. Read description from file
3. Read content for each file
4. Create intent object
5. Append to PR_INTENTS.jsonl
6. Log PR_INTENT_CREATED event
7. Print intent_id and summary

---

## 📁 Files to Create/Modify

### Files to Create

1. **`docs/system_state/outbox/`** (NEW directory)
   - Outbox directory for all future write contracts

2. **`docs/system_state/outbox/PR_INTENTS.jsonl`** (NEW)
   - Intent storage file
   - Initially empty

3. **`scripts/pr_worker.py`** (NEW)
   - Worker that processes pending intents
   - ~150 lines of Python

4. **`scripts/create_pr_intent.py`** (NEW)
   - Helper to create intents easily
   - CLI interface
   - ~100 lines of Python

5. **`docs/sync_contracts/PR_CONTRACT_V1.md`** (NEW)
   - Contract documentation
   - Intent schema
   - Event types
   - Usage examples

6. **`docs/slices/SLICE_SYNC_WRITE_CONTRACT_PR_V1.md`** (NEW)
   - Slice documentation
   - Implementation notes
   - Testing results

### Files to Modify

7. **`docs/system_state/timeline/EVENT_TIMELINE.jsonl`** (APPEND)
   - New events as intents are created/processed

---

## 🧪 Testing & Validation

### Prerequisites
```bash
# Start mcp_github_client
cd services/mcp_github_client
python -m uvicorn main:app --port 8081

# Verify it's running
curl http://localhost:8081/health
```

### Test 1: Create Intent Manually

```bash
# Create outbox directory
mkdir -p docs/system_state/outbox

# Create test intent
cat > docs/system_state/outbox/PR_INTENTS.jsonl << 'EOF'
{"intent_id": "pr-intent-test-001", "created_at": "2025-11-27T23:00:00Z", "created_by": "manual-test", "status": "pending", "pr_spec": {"title": "Test PR - Manual Intent", "description": "This is a test PR created via manual intent.\n\n## Changes\n- Added test.txt", "files": [{"path": "test/test001.txt", "content": "Test content for PR intent test", "operation": "create"}], "base_branch": "main", "use_ai_generation": false}, "trace_id": "pr-intent-test-001", "result": null, "error": null, "error_type": null, "processed_at": null}
EOF

# Verify
cat docs/system_state/outbox/PR_INTENTS.jsonl | jq .
```

### Test 2: Run Worker (Success Path)

```bash
# Make sure mcp_github_client is running on port 8081

# Run worker
python scripts/pr_worker.py

# Expected output:
# [INFO] Found 1 pending intent(s)
# 
# [INFO] Processing intent: pr-intent-test-001
# [SUCCESS] PR created: #22
# 
# [SUMMARY] 1 completed, 0 failed

# Verify intent status changed
cat docs/system_state/outbox/PR_INTENTS.jsonl | jq .status
# Should show: "completed"

# Verify result
cat docs/system_state/outbox/PR_INTENTS.jsonl | jq .result
# Should show: {"pr_number": 22, "pr_url": "...", "branch_name": "..."}

# Verify events logged
grep "PR_INTENT\|PR_CREATED" docs/system_state/timeline/EVENT_TIMELINE.jsonl | tail -3
```

### Test 3: Failure Handling

```bash
# Stop mcp_github_client
# (Ctrl+C in the terminal running uvicorn)

# Create new intent
cat >> docs/system_state/outbox/PR_INTENTS.jsonl << 'EOF'
{"intent_id": "pr-intent-test-002", "created_at": "2025-11-27T23:05:00Z", "created_by": "failure-test", "status": "pending", "pr_spec": {"title": "Test Failure", "description": "Test", "files": [{"path": "test/test002.txt", "content": "test2", "operation": "create"}], "base_branch": "main", "use_ai_generation": false}, "trace_id": "pr-intent-test-002", "result": null, "error": null, "error_type": null, "processed_at": null}
EOF

# Run worker (should fail)
python scripts/pr_worker.py

# Expected output:
# [INFO] Found 1 pending intent(s)
# 
# [INFO] Processing intent: pr-intent-test-002
# [ERROR] Exception: Connection refused [Errno 111]
# 
# [SUMMARY] 0 completed, 1 failed

# Verify intent marked as failed
cat docs/system_state/outbox/PR_INTENTS.jsonl | grep "pr-intent-test-002" | jq .status
# Should show: "failed"

# Verify error
cat docs/system_state/outbox/PR_INTENTS.jsonl | grep "pr-intent-test-002" | jq .error
# Should show connection error

# Verify PR_CREATION_FAILED event
grep "PR_CREATION_FAILED" docs/system_state/timeline/EVENT_TIMELINE.jsonl | tail -1
```

### Test 4: Create Intent via Helper Script

```bash
# Create description file
cat > /tmp/test_pr_desc.txt << 'EOF'
This PR adds a test feature via helper script.

## Changes
- Added TEST.md file
- Demonstrates create_pr_intent.py usage

## Testing
- Manual test of intent creation
- Verifies helper script works
EOF

# Create content file
cat > /tmp/test_content.md << 'EOF'
# Test Document

This is a test document created via pr intent helper.

## Purpose
Demonstrate the Sync Write Contract PR creation flow.
EOF

# Use helper script
python scripts/create_pr_intent.py \
  --title "SLICE_TEST_HELPER_V1" \
  --description-file /tmp/test_pr_desc.txt \
  --file docs/TEST_HELPER.md:/tmp/test_content.md \
  --operation create

# Expected output:
# [INFO] Creating PR intent...
# [INFO] Intent ID: pr-intent-1732748500-abc123
# [INFO] PR Title: SLICE_TEST_HELPER_V1
# [INFO] Files: 1
# [SUCCESS] Intent created and logged
# 
# Next steps:
# 1. Review intent: docs/system_state/outbox/PR_INTENTS.jsonl
# 2. Run worker: python scripts/pr_worker.py

# Verify intent created
tail -1 docs/system_state/outbox/PR_INTENTS.jsonl | jq .

# Verify PR_INTENT_CREATED event
tail -1 docs/system_state/timeline/EVENT_TIMELINE.jsonl | jq .
```

---

## ✅ Success Criteria

### Must Have

- [ ] `docs/system_state/outbox/PR_INTENTS.jsonl` created
- [ ] Intent schema matches `/github/open-pr` API exactly
- [ ] `scripts/pr_worker.py` created and functional
- [ ] `scripts/create_pr_intent.py` created and functional
- [ ] Events logged: PR_INTENT_CREATED, PR_INTENT_PROCESSING, PR_CREATED, PR_CREATION_FAILED
- [ ] Manual test: intent created → processed → PR opened on GitHub
- [ ] Manual test: worker handles failures gracefully (service down)
- [ ] Documentation complete (contract + slice docs)

### Nice to Have (Future V1.1+)

- Retry logic with exponential backoff
- Intent expiration/TTL
- Scheduled worker execution (cron or n8n)
- Multiple file operations validation
- AI-generated PR descriptions (use_ai_generation=true)

---

## 📊 Contract Definition

**Contract Name:** `PR_CREATION_CONTRACT_V1`

**Intent Schema:** See section 1 above

**Guarantees (V1):**
1. **At-least-once execution:** Each pending intent processed at least once
2. **Audit trail:** All intents and events permanently logged
3. **Status visibility:** Intent status always reflects current state
4. **Failure isolation:** One intent failure doesn't stop others
5. **No data loss:** Failed intents remain in file for manual intervention

**Does NOT Guarantee (V1):**
- **Exactly-once execution:** If worker crashes mid-processing, might retry
- **Idempotency:** GitHub might reject duplicate PRs, but intent processes anyway
- **Immediate processing:** Manual execution only, no scheduling
- **Automatic retry:** Failed intents require manual re-run or status reset

**At-least-once Semantics:**
- Worker only processes `status == "pending"`
- Once status changes to `processing`/`completed`/`failed`, worker skips it
- To retry a failed intent: manually change `status` back to `pending`
- Duplicate PRs possible if GitHub API succeeds but response not recorded

---

## 🔮 Next Steps (Post-V1)

### Immediate Improvements (V1.1)

1. **Retry Logic:**
   ```python
   "retry_count": 0,
   "max_retries": 3,
   "retry_delay_seconds": 60
   ```

2. **HTTP Endpoint:** `POST /sync/pr/process` in OS Core or new service

3. **Batch Processing:** Process multiple intents more efficiently

### Phase 2.4+

1. **n8n Workflow:** `PR_SYNC_ORCHESTRATOR_V1`
   - Cron trigger: every 5 minutes
   - Check for pending intents
   - Call pr_worker or HTTP endpoint

2. **Intent Creation API:** HTTP endpoint to create intents programmatically

3. **Langfuse Integration:** Trace intent → execution → PR

---

## 🚨 Known Limitations & Assumptions

### Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Manual execution only | No real-time processing | Document clearly, future cron |
| No retry logic | Failed intents need manual intervention | Keep error messages clear |
| File-based storage | Limited scalability | Acceptable for INFRA_ONLY phase |
| No idempotency | Duplicate PRs possible | GitHub rejects duplicates anyway |
| Single worker | Can't run concurrently | Document constraint |

### Assumptions

1. **mcp_github_client is running** on port 8081
2. **GitHub API is available** (internet connection)
3. **PR_INTENTS.jsonl is valid JSON** (one object per line)
4. **File content is text-based** (not binary)
5. **Intent IDs are unique** (timestamp + random should guarantee this)

---

## 🎓 Lessons for Future Contracts

**What Works:**
- ✅ Intent-based pattern cleanly separates creation from execution
- ✅ JSONL format simple and human-readable
- ✅ Status field makes intent lifecycle clear
- ✅ Events provide complete audit trail

**For Next Contracts (Email, Calendar, Tasks):**
- Use same pattern: Intent Layer → Worker → Service → Events
- Keep intent schema simple in V1
- Start with manual execution, add automation later
- Always log events for observability

---

**Spec Updated:** 2025-11-27  
**Status:** Ready for Implementation ✅  
**Approved By:** Or (with 3 clarifications incorporated)
