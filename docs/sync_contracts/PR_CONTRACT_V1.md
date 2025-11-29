# PR Creation Contract V1

**Contract Type:** Sync Write Contract  
**Operation:** Create Pull Request on GitHub  
**Pattern:** Transactional Outbox  
**Phase:** 2.3 (INFRA_ONLY)

---

## 🎯 Purpose

This contract defines how AI-OS creates Pull Requests on GitHub in an asynchronous, traceable manner using the Transactional Outbox pattern.

**Key Benefits:**
- **Asynchronous:** Intent creation decoupled from execution
- **Traceable:** Complete audit trail via events
- **Fault-tolerant:** Failed intents don't block others
- **Retryable:** Manual retry by resetting status

---

## 📐 Contract Architecture

```
Intent Creation
    ↓
Outbox (PR_INTENTS.jsonl)
    ↓
Worker (pr_worker.py)
    ↓
Service (mcp_github_client:8081)
    ↓
Events (EVENT_TIMELINE.jsonl)
```

---

## 📋 Intent Schema

### Intent Structure

```json
{
  "intent_id": "pr-intent-{timestamp}-{random}",
  "created_at": "2025-11-27T23:00:00.000Z",
  "created_by": "create_pr_intent" | "infra-operator" | "script-name",
  "status": "pending" | "processing" | "completed" | "failed",
  "pr_spec": {
    "title": "SLICE_NAME - Short description",
    "description": "Full PR body in markdown...",
    "files": [
      {
        "path": "docs/EXAMPLE.md",
        "content": "# Full file content here...",
        "operation": "create" | "update"
      }
    ],
    "base_branch": "main",
    "use_ai_generation": false
  },
  "trace_id": "pr-intent-{timestamp}-{random}",
  "result": {
    "pr_number": 22,
    "pr_url": "https://github.com/edri2or-commits/ai-os/pull/22",
    "branch_name": "ai-os-pr-20251127-230010"
  },
  "error": "Error message if failed",
  "error_type": "connection_error" | "github_api_error" | "unexpected_error",
  "processed_at": "2025-11-27T23:00:15.000Z"
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `intent_id` | string | Yes | Unique identifier (auto-generated) |
| `created_at` | string (ISO 8601) | Yes | When intent was created |
| `created_by` | string | Yes | Who/what created the intent |
| `status` | enum | Yes | Current status (see Status Lifecycle) |
| `pr_spec` | object | Yes | PR specification (see below) |
| `trace_id` | string | Yes | For observability (same as intent_id in V1) |
| `result` | object | No | PR creation result (if completed) |
| `error` | string | No | Error message (if failed) |
| `error_type` | string | No | Error classification (if failed) |
| `processed_at` | string (ISO 8601) | No | When intent was processed |

### PR Spec Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | PR title (visible on GitHub) |
| `description` | string | Yes | PR body/description (markdown) |
| `files` | array[FileChange] | Yes | Files to include in PR |
| `base_branch` | string | No | Target branch (default: "main") |
| `use_ai_generation` | boolean | No | Use AI to refine description (default: false) |

### FileChange Structure

```json
{
  "path": "docs/EXAMPLE.md",
  "content": "# Full file content\n\nMust include complete file content...",
  "operation": "create"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `path` | string | Yes | File path in repository |
| `content` | string | Yes | **Full** file content |
| `operation` | enum | Yes | "create" or "update" |

---

## 🔄 Status Lifecycle

```
pending
  ↓
processing  (worker picked up intent)
  ↓
completed   (PR created successfully)
  OR
failed      (error occurred)
```

**Status Transitions:**
- `pending` → Worker hasn't processed yet
- `processing` → Worker is currently executing
- `completed` → PR created successfully, see `result`
- `failed` → Execution failed, see `error` and `error_type`

**Manual Retry:**
To retry a failed intent, manually edit PR_INTENTS.jsonl and change `status` back to `"pending"`.

---

## 📊 Events

### PR_INTENT_CREATED

Logged when intent is created.

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

### PR_INTENT_PROCESSING

Logged when worker starts processing.

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

### PR_CREATED

Logged when PR created successfully.

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

### PR_CREATION_FAILED

Logged when PR creation fails.

```json
{
  "timestamp": "2025-11-27T23:00:10.000Z",
  "event_type": "PR_CREATION_FAILED",
  "source": "pr_worker",
  "payload": {
    "intent_id": "pr-intent-1732748400-x7k9m2",
    "pr_title": "SLICE_EXAMPLE_V1",
    "error_type": "connection_error",
    "error": "Connection refused: [Errno 111]"
  }
}
```

---

## 🔐 Contract Guarantees

### What This Contract Guarantees

✅ **At-least-once execution:** Every pending intent will be processed at least once  
✅ **Audit trail:** All intents and events permanently logged  
✅ **Status visibility:** Intent status always reflects current state  
✅ **Failure isolation:** One intent failure doesn't block others  
✅ **No data loss:** Failed intents remain for manual intervention  

### What This Contract Does NOT Guarantee (V1)

❌ **Exactly-once execution:** Worker crash may cause retry  
❌ **Idempotency:** Duplicate PRs possible (GitHub will reject)  
❌ **Immediate processing:** Manual execution only  
❌ **Automatic retry:** Failed intents require manual intervention  

---

## 🛠️ Usage

### Creating an Intent

**Option 1: Helper Script (Recommended)**

```bash
# Create content file
cat > example_content.md << 'EOF'
# Example Document

This is example content for the PR.
EOF

# Create description
cat > pr_description.txt << 'EOF'
This PR adds example documentation.

## Changes
- Added docs/EXAMPLE.md

## Testing
- Manual review
EOF

# Create intent
python scripts/create_pr_intent.py \
  --title "Add example documentation" \
  --description-file pr_description.txt \
  --file docs/EXAMPLE.md:example_content.md \
  --operation create
```

**Option 2: Manual JSON**

```bash
# Append to PR_INTENTS.jsonl
cat >> docs/system_state/outbox/PR_INTENTS.jsonl << 'EOF'
{"intent_id": "pr-intent-manual-001", "created_at": "2025-11-27T23:00:00Z", "created_by": "manual", "status": "pending", "pr_spec": {"title": "Test PR", "description": "Test", "files": [{"path": "test.txt", "content": "test content", "operation": "create"}], "base_branch": "main", "use_ai_generation": false}, "trace_id": "pr-intent-manual-001", "result": null, "error": null, "error_type": null, "processed_at": null}
EOF
```

### Processing Intents

```bash
# Prerequisites: mcp_github_client running on port 8081
cd services/mcp_github_client
python -m uvicorn main:app --port 8081 &

# Run worker
python scripts/pr_worker.py
```

**Expected Output:**
```
======================================================================
  AI-OS PR Worker - Sync Write Contract
======================================================================

[1/3] Loading intents from: docs/system_state/outbox/PR_INTENTS.jsonl
  Total intents: 1
  Pending intents: 1

[2/3] Processing 1 pending intent(s)...

[INFO] Processing intent: pr-intent-manual-001
  Title: Test PR
  Calling mcp_github_client...
  [SUCCESS] PR created: #22
  URL: https://github.com/edri2or-commits/ai-os/pull/22

======================================================================
[3/3] Summary
======================================================================
  Completed: 1
  Failed: 0
  Total processed: 1

[SUCCESS] PRs created successfully!
Check GitHub: https://github.com/edri2or-commits/ai-os/pulls
```

---

## 🧪 Testing

### Test 1: Success Path

```bash
# Create test intent
python scripts/create_pr_intent.py \
  --title "Test - Success path" \
  --description "Test successful PR creation" \
  --file test/success.txt:test_content.txt

# Run worker
python scripts/pr_worker.py

# Verify
cat docs/system_state/outbox/PR_INTENTS.jsonl | jq '.status'
# Should show: "completed"

grep "PR_CREATED" docs/system_state/timeline/EVENT_TIMELINE.jsonl | tail -1
```

### Test 2: Failure Path

```bash
# Stop mcp_github_client
pkill -f "uvicorn.*8081"

# Create test intent
python scripts/create_pr_intent.py \
  --title "Test - Failure path" \
  --description "Test failed PR creation" \
  --file test/failure.txt:test_content.txt

# Run worker (will fail)
python scripts/pr_worker.py

# Verify
cat docs/system_state/outbox/PR_INTENTS.jsonl | jq 'select(.status=="failed") | .error'

grep "PR_CREATION_FAILED" docs/system_state/timeline/EVENT_TIMELINE.jsonl | tail -1
```

---

## 📝 Error Types

| Error Type | Description | Cause |
|------------|-------------|-------|
| `connection_error` | Cannot reach mcp_github_client | Service down, network issue |
| `branch_creation_failed` | Cannot create Git branch | Branch already exists, permissions |
| `file_update_failed` | Cannot write file to branch | Invalid path, encoding issue |
| `pr_creation_failed` | Cannot create PR on GitHub | API error, permissions |
| `unexpected_error` | Unknown error | Bug in worker, malformed intent |

---

## 🔮 Future Enhancements (V2+)

1. **Retry Logic:**
   - Automatic retry with exponential backoff
   - Max retry count

2. **Scheduled Execution:**
   - Cron trigger for pr_worker.py
   - n8n workflow integration

3. **HTTP API:**
   - `POST /sync/pr/create` - Create intent
   - `POST /sync/pr/process` - Process intents
   - `GET /sync/pr/status/{intent_id}` - Check status

4. **Enhanced Idempotency:**
   - Deduplication based on title/files hash
   - GitHub API idempotency keys

5. **Batch Operations:**
   - Process multiple intents in parallel
   - Rate limit handling

---

**Contract Version:** 1.0  
**Last Updated:** 2025-11-27  
**Status:** ✅ Production (INFRA_ONLY)
