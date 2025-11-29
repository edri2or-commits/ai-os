# End-to-End Slice to PR Demo - Runbook V1

**Version:** 1.0  
**Date:** 2025-11-28  
**Demo Slice:** SLICE_BOOTSTRAP_VALIDATOR_V1  
**Phase:** 2.3 (INFRA_ONLY)

---

## 🎯 Purpose

This runbook demonstrates the **complete end-to-end flow** of publishing a completed slice as a GitHub Pull Request using the Slice → PR Pipeline.

**Flow:**
```
Completed Slice (SLICE_BOOTSTRAP_VALIDATOR_V1)
    ↓
publish_slice_as_pr.py (create PR Intent)
    ↓
PR_INTENTS.jsonl (outbox)
    ↓
pr_worker.py (process intent)
    ↓
mcp_github_client (create PR on GitHub)
    ↓
GitHub PR (ready for review)
```

---

## 📋 Prerequisites

Before starting, ensure you have:

### 1. Repository State

✅ **On correct branch:**
```bash
cd C:\Users\edri2\Desktop\AI\ai-os
git status
# Should show: On branch main
```

✅ **No uncommitted changes** (optional but recommended):
```bash
git status
# Should show: nothing to commit, working tree clean
```

### 2. Services Running

✅ **mcp_github_client service** (required for pr_worker.py):
```bash
# Start service (in separate terminal/tab):
cd services/mcp_github_client
python -m uvicorn main:app --port 8081

# Verify it's running:
curl http://localhost:8081/health
# Should return: {"status": "healthy"}
```

**Alternative (if mcp_github_client not running):**
- Demo will work through Step 3 (creating intent)
- Step 4 (pr_worker.py) will fail with connection error
- Intent status will be "failed" with error_type: "connection_error"
- This is **expected behavior** when service is down

### 3. Python Environment

✅ **Python 3.8+** with required packages:
```bash
python --version
# Should be 3.8 or higher

# Verify scripts are executable
ls -lh scripts/publish_slice_as_pr.py
ls -lh scripts/pr_worker.py
```

---

## 🔄 Step-by-Step Flow

### Step 1: Verify Slice Exists

**Goal:** Confirm SLICE_BOOTSTRAP_VALIDATOR_V1 is complete and documented.

**Commands:**

```bash
# 1a. Check slice doc exists
cat docs/slices/SLICE_BOOTSTRAP_VALIDATOR_V1.md | head -20

# 1b. Find SLICE_COMPLETE event in timeline
grep "SLICE_BOOTSTRAP_VALIDATOR_V1" docs/system_state/timeline/EVENT_TIMELINE.jsonl | grep "SLICE_COMPLETE"

# 1c. Verify files exist
ls -lh scripts/validate_bootstrap_response.py
ls -lh test/bootstrap_responses/good_handshake.txt
ls -lh test/bootstrap_responses/bad_handshake.txt
ls -lh docs/slices/SLICE_BOOTSTRAP_VALIDATOR_V1.md
```

**Expected Output:**

```
# 1a - Slice doc header
# SLICE_BOOTSTRAP_VALIDATOR_V1

**Date:** 2025-11-28  
**Phase:** 2.3 (INFRA_ONLY)  
**Status:** ✅ COMPLETE  
...

# 1b - SLICE_COMPLETE event (JSON)
{"timestamp": "2025-11-28T01:30:00Z", "event_type": "SLICE_COMPLETE", ...}

# 1c - All files exist
-rwxr-xr-x 1 user group 11234 Nov 28 01:30 scripts/validate_bootstrap_response.py
-rw-r--r-- 1 user group   812 Nov 28 01:30 test/bootstrap_responses/good_handshake.txt
...
```

**Verify:**
- ✅ Slice doc shows Status: ✅ COMPLETE
- ✅ SLICE_COMPLETE event found with files_created
- ✅ All 4 files exist on disk

---

### Step 2: Dry Run - Preview PR Intent

**Goal:** Preview what PR Intent will be created **without** modifying any files.

**Command:**

```bash
python scripts/publish_slice_as_pr.py \
  --slice-name SLICE_BOOTSTRAP_VALIDATOR_V1 \
  --dry-run
```

**Expected Output:**

```
======================================================================
  Slice to PR Pipeline - Creating PR Intent
======================================================================

[1/5] Validating slice: SLICE_BOOTSTRAP_VALIDATOR_V1
  ✓ Slice doc found: docs/slices/SLICE_BOOTSTRAP_VALIDATOR_V1.md
  ✓ SLICE_COMPLETE event found in timeline
  ✓ Files exist on disk: 4 files

[2/5] Extracting metadata
  Slice description: Bootstrap handshake validator - automated validation tool for CHAT_BOOTSTRAP_PROTOCOL_V1 compliance
  Files created: 4
  Files modified: 0

[3/5] Reading file contents
  Reading: scripts/validate_bootstrap_response.py (11.2 KB)
  Reading: test/bootstrap_responses/good_handshake.txt (0.8 KB)
  Reading: test/bootstrap_responses/bad_handshake.txt (0.3 KB)
  Reading: docs/slices/SLICE_BOOTSTRAP_VALIDATOR_V1.md (18.5 KB)
  Total content size: 30.8 KB

[4/5] Building PR spec
  Title: SLICE_BOOTSTRAP_VALIDATOR_V1 - Bootstrap handshake validator
  Description: 16 lines
  Files: 4 entries

[5/5] DRY RUN - Not saving intent

Would create intent:
{
  "intent_id": "slice-SLICE_BOOTSTRAP_VALIDATOR_V1-1732757400-abc123",
  "created_at": "2025-11-28T02:10:00Z",
  "created_by": "slice_to_pr_pipeline_v1",
  "status": "pending",
  "pr_spec": {
    "title": "SLICE_BOOTSTRAP_VALIDATOR_V1 - Bootstrap handshake validator",
    "description": "## Overview\n\nBootstrap handshake validator...",
    ...
  }
}...

======================================================================
DRY RUN COMPLETE
======================================================================

Intent ID: slice-SLICE_BOOTSTRAP_VALIDATOR_V1-1732757400-abc123
Slice: SLICE_BOOTSTRAP_VALIDATOR_V1
Files: 4
PR Title: SLICE_BOOTSTRAP_VALIDATOR_V1 - Bootstrap handshake validator
```

**Verify:**
- ✅ Shows "[5/5] DRY RUN - Not saving intent"
- ✅ Total content size ~30.8 KB
- ✅ 4 files listed
- ✅ PR title looks correct

**Important:**
- No files were modified
- No intent created yet
- This is just a preview

---

### Step 3: Create PR Intent

**Goal:** Actually create the PR Intent in the outbox.

**Command:**

```bash
python scripts/publish_slice_as_pr.py \
  --slice-name SLICE_BOOTSTRAP_VALIDATOR_V1
```

**Expected Output:**

```
======================================================================
  Slice to PR Pipeline - Creating PR Intent
======================================================================

[1/5] Validating slice: SLICE_BOOTSTRAP_VALIDATOR_V1
  ✓ Slice doc found: docs/slices/SLICE_BOOTSTRAP_VALIDATOR_V1.md
  ✓ SLICE_COMPLETE event found in timeline
  ✓ Files exist on disk: 4 files

[2/5] Extracting metadata
  Slice description: Bootstrap handshake validator - automated validation tool for CHAT_BOOTSTRAP_PROTOCOL_V1 compliance
  Files created: 4
  Files modified: 0

[3/5] Reading file contents
  Reading: scripts/validate_bootstrap_response.py (11.2 KB)
  Reading: test/bootstrap_responses/good_handshake.txt (0.8 KB)
  Reading: test/bootstrap_responses/bad_handshake.txt (0.3 KB)
  Reading: docs/slices/SLICE_BOOTSTRAP_VALIDATOR_V1.md (18.5 KB)
  Total content size: 30.8 KB

[4/5] Building PR spec
  Title: SLICE_BOOTSTRAP_VALIDATOR_V1 - Bootstrap handshake validator
  Description: 16 lines
  Files: 4 entries

[5/5] Creating PR Intent
  Intent ID: slice-SLICE_BOOTSTRAP_VALIDATOR_V1-1732757400-abc123
  Saved to: docs/system_state/outbox/PR_INTENTS.jsonl
  Logged event: SLICE_PR_INTENT_CREATED

======================================================================
✅ PR Intent Created Successfully
======================================================================

Intent ID: slice-SLICE_BOOTSTRAP_VALIDATOR_V1-1732757400-abc123
Slice: SLICE_BOOTSTRAP_VALIDATOR_V1
Files: 4
PR Title: SLICE_BOOTSTRAP_VALIDATOR_V1 - Bootstrap handshake validator

Next step: Run pr_worker.py to create the PR on GitHub
```

**Verify Intent Created:**

```bash
# Check intent was added to outbox
tail -1 docs/system_state/outbox/PR_INTENTS.jsonl | jq '{intent_id, status, pr_title: .pr_spec.title}'

# Expected:
{
  "intent_id": "slice-SLICE_BOOTSTRAP_VALIDATOR_V1-1732757400-abc123",
  "status": "pending",
  "pr_title": "SLICE_BOOTSTRAP_VALIDATOR_V1 - Bootstrap handshake validator"
}

# Check event was logged
tail -1 docs/system_state/timeline/EVENT_TIMELINE.jsonl | jq '{event_type, payload}'

# Expected:
{
  "event_type": "SLICE_PR_INTENT_CREATED",
  "payload": {
    "slice_name": "SLICE_BOOTSTRAP_VALIDATOR_V1",
    "intent_id": "slice-SLICE_BOOTSTRAP_VALIDATOR_V1-1732757400-abc123",
    "files_count": 4,
    ...
  }
}
```

**Verify:**
- ✅ Intent appended to `PR_INTENTS.jsonl`
- ✅ Intent status is `"pending"`
- ✅ Event appended to `EVENT_TIMELINE.jsonl`
- ✅ Event type is `SLICE_PR_INTENT_CREATED`

---

### Step 4: Process Intent (Create PR)

**Goal:** Run the worker to process pending intents and create PR on GitHub.

**Command:**

```bash
python scripts/pr_worker.py
```

**Expected Output (Success Case):**

```
======================================================================
  AI-OS PR Worker - Sync Write Contract
======================================================================

[1/3] Loading intents from: docs/system_state/outbox/PR_INTENTS.jsonl
  Total intents: 1
  Pending intents: 1

[2/3] Processing 1 pending intent(s)...

[INFO] Processing intent: slice-SLICE_BOOTSTRAP_VALIDATOR_V1-1732757400-abc123
  Title: SLICE_BOOTSTRAP_VALIDATOR_V1 - Bootstrap handshake validator
  Calling mcp_github_client at http://localhost:8081/github/open-pr...
  [SUCCESS] PR created: #42
  URL: https://github.com/edri2or-commits/ai-os/pull/42
  Branch: ai-os-pr-20251128-021030

======================================================================
[3/3] Summary
======================================================================
  Completed: 1
  Failed: 0
  Total processed: 1

[SUCCESS] PRs created successfully!
Check GitHub: https://github.com/edri2or-commits/ai-os/pulls
```

**Expected Output (Failure Case - Service Down):**

```
======================================================================
  AI-OS PR Worker - Sync Write Contract
======================================================================

[1/3] Loading intents from: docs/system_state/outbox/PR_INTENTS.jsonl
  Total intents: 1
  Pending intents: 1

[2/3] Processing 1 pending intent(s)...

[INFO] Processing intent: slice-SLICE_BOOTSTRAP_VALIDATOR_V1-1732757400-abc123
  Title: SLICE_BOOTSTRAP_VALIDATOR_V1 - Bootstrap handshake validator
  Calling mcp_github_client at http://localhost:8081/github/open-pr...
  [ERROR] Connection error: [Errno 111] Connection refused

======================================================================
[3/3] Summary
======================================================================
  Completed: 0
  Failed: 1
  Total processed: 1

[FAILURE] Some intents failed. Check PR_INTENTS.jsonl for details.
```

**Verify (Success Case):**

```bash
# Check intent status updated
cat docs/system_state/outbox/PR_INTENTS.jsonl | jq 'select(.intent_id | contains("SLICE_BOOTSTRAP_VALIDATOR_V1")) | {status, pr_number: .result.pr_number, pr_url: .result.pr_url}'

# Expected:
{
  "status": "completed",
  "pr_number": 42,
  "pr_url": "https://github.com/edri2or-commits/ai-os/pull/42"
}

# Check PR_CREATED event
grep "PR_CREATED" docs/system_state/timeline/EVENT_TIMELINE.jsonl | tail -1 | jq '{event_type, payload}'

# Expected:
{
  "event_type": "PR_CREATED",
  "payload": {
    "intent_id": "slice-SLICE_BOOTSTRAP_VALIDATOR_V1-1732757400-abc123",
    "pr_number": 42,
    "pr_url": "https://github.com/edri2or-commits/ai-os/pull/42",
    ...
  }
}
```

**Verify (Failure Case):**

```bash
# Check intent status shows failure
cat docs/system_state/outbox/PR_INTENTS.jsonl | jq 'select(.intent_id | contains("SLICE_BOOTSTRAP_VALIDATOR_V1")) | {status, error_type, error}'

# Expected:
{
  "status": "failed",
  "error_type": "connection_error",
  "error": "Connection refused: [Errno 111] Connection to http://localhost:8081 refused"
}

# Check PR_CREATION_FAILED event
grep "PR_CREATION_FAILED" docs/system_state/timeline/EVENT_TIMELINE.jsonl | tail -1 | jq '{event_type, payload}'
```

**Verify:**
- ✅ Success: Intent status → `"completed"`, PR number & URL populated
- ✅ Failure: Intent status → `"failed"`, error type & message populated
- ✅ Appropriate event logged (PR_CREATED or PR_CREATION_FAILED)

---

### Step 5: Inspect Results

**Goal:** Verify the complete flow worked end-to-end.

**Commands:**

```bash
# 5a. Check final intent state
cat docs/system_state/outbox/PR_INTENTS.jsonl | \
  jq 'select(.slice_name == "SLICE_BOOTSTRAP_VALIDATOR_V1" or .intent_id | contains("SLICE_BOOTSTRAP_VALIDATOR_V1"))' | \
  jq '{intent_id, status, pr_spec: {title: .pr_spec.title, files_count: (.pr_spec.files | length)}, result, error}'

# 5b. Check all events related to this slice PR
grep "SLICE_BOOTSTRAP_VALIDATOR_V1" docs/system_state/timeline/EVENT_TIMELINE.jsonl | \
  grep -E "(SLICE_PR_INTENT_CREATED|PR_INTENT_PROCESSING|PR_CREATED|PR_CREATION_FAILED)" | \
  jq '{timestamp, event_type, payload}'

# 5c. If successful, open PR in browser
# (Replace {PR_NUMBER} with actual number from result)
echo "Open: https://github.com/edri2or-commits/ai-os/pull/{PR_NUMBER}"
```

**Expected Output (Success):**

```json
// 5a - Intent state
{
  "intent_id": "slice-SLICE_BOOTSTRAP_VALIDATOR_V1-1732757400-abc123",
  "status": "completed",
  "pr_spec": {
    "title": "SLICE_BOOTSTRAP_VALIDATOR_V1 - Bootstrap handshake validator",
    "files_count": 4
  },
  "result": {
    "pr_number": 42,
    "pr_url": "https://github.com/edri2or-commits/ai-os/pull/42",
    "branch_name": "ai-os-pr-20251128-021030"
  },
  "error": null
}

// 5b - Events
{
  "timestamp": "2025-11-28T02:10:00Z",
  "event_type": "SLICE_PR_INTENT_CREATED",
  "payload": {"slice_name": "SLICE_BOOTSTRAP_VALIDATOR_V1", ...}
}
{
  "timestamp": "2025-11-28T02:10:30Z",
  "event_type": "PR_INTENT_PROCESSING",
  "payload": {"intent_id": "slice-SLICE_BOOTSTRAP_VALIDATOR_V1-...", ...}
}
{
  "timestamp": "2025-11-28T02:10:35Z",
  "event_type": "PR_CREATED",
  "payload": {"pr_number": 42, "pr_url": "...", ...}
}
```

**Verify (Success):**
- ✅ Intent status: `"completed"`
- ✅ PR number populated (e.g., 42)
- ✅ PR URL valid GitHub link
- ✅ Branch created on GitHub
- ✅ All events logged in timeline

**Verify (Failure):**
- ✅ Intent status: `"failed"`
- ✅ error_type: `"connection_error"` (or other error type)
- ✅ error message explains what went wrong
- ✅ PR_CREATION_FAILED event logged

---

## ⚠️ Failure Modes & Debugging

### Failure Mode 1: mcp_github_client Down

**Symptom:**
```
[ERROR] Connection error: [Errno 111] Connection refused
```

**Cause:**
- `mcp_github_client` service not running on port 8081

**Solution:**
```bash
# Start service in separate terminal
cd services/mcp_github_client
python -m uvicorn main:app --port 8081

# Retry pr_worker.py
python scripts/pr_worker.py
```

**Or: Manual Retry**
```bash
# Reset intent status to "pending"
# Edit PR_INTENTS.jsonl manually:
# Change "status": "failed" → "status": "pending"

# Then run worker again
python scripts/pr_worker.py
```

---

### Failure Mode 2: Slice Not Found

**Symptom:**
```
[ERROR] Slice doc not found: docs/slices/SLICE_X.md
```

**Cause:**
- Typo in slice name
- Slice doc doesn't exist

**Solution:**
```bash
# List available slices
ls docs/slices/

# Use correct slice name (exact match, case-sensitive)
python scripts/publish_slice_as_pr.py --slice-name SLICE_CORRECT_NAME_V1
```

---

### Failure Mode 3: SLICE_COMPLETE Event Missing

**Symptom:**
```
[WARNING] SLICE_COMPLETE event not found in timeline
Will use slice doc only
```

**Cause:**
- Slice completed but SLICE_COMPLETE event not logged
- Event malformed or name mismatch

**Impact:**
- Non-critical: Script continues using slice doc metadata
- May have less accurate file list

**Solution:**
- Script will work, but metadata may be incomplete
- Consider adding SLICE_COMPLETE event manually if needed

---

### Failure Mode 4: Duplicate PR

**Symptom:**
```
[ERROR] Branch already exists: ai-os-pr-20251128-021030
```

**Cause:**
- Running pr_worker.py twice on same intent
- GitHub rejects duplicate branch names

**Solution:**
```bash
# Check if PR already exists on GitHub
# Visit: https://github.com/edri2or-commits/ai-os/pulls

# If PR exists: Intent succeeded, no action needed
# If PR doesn't exist: Delete branch and retry
git push origin --delete ai-os-pr-20251128-021030
```

---

### Debugging Checklist

When something goes wrong:

1. **Check Intent Status:**
   ```bash
   tail -5 docs/system_state/outbox/PR_INTENTS.jsonl | jq '{intent_id, status, error}'
   ```

2. **Check Recent Events:**
   ```bash
   tail -10 docs/system_state/timeline/EVENT_TIMELINE.jsonl | jq '{timestamp, event_type, payload}'
   ```

3. **Check Service Health:**
   ```bash
   curl http://localhost:8081/health
   # Should return: {"status": "healthy"}
   ```

4. **Check Files Exist:**
   ```bash
   # From slice doc or SLICE_COMPLETE event
   ls -lh scripts/validate_bootstrap_response.py
   ls -lh test/bootstrap_responses/
   ```

5. **Check GitHub:**
   ```bash
   # Visit repo to see PRs and branches
   https://github.com/edri2or-commits/ai-os/pulls
   https://github.com/edri2or-commits/ai-os/branches
   ```

---

## 🔄 Cleanup & Re-Running

### Safe to Re-Run:

✅ **Step 1 (Verify):** Always safe, read-only  
✅ **Step 2 (Dry run):** Always safe, no side effects  
✅ **Step 3 (Create intent):** Creates new intent each time  
⚠️ **Step 4 (Process):** Only processes `"pending"` intents  

### Avoid Duplicate PRs:

**Option 1: Don't re-run Step 3**
- If intent already exists, skip to Step 4
- Worker will only process pending intents

**Option 2: Clean up old intent first**
```bash
# Manually edit PR_INTENTS.jsonl
# Remove the old intent line, or
# Change status to "completed" (will be skipped)
```

**Option 3: Use Different Slice**
```bash
# Demo with a different slice
python scripts/publish_slice_as_pr.py --slice-name SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1
```

---

## 📊 Success Checklist

After completing all steps, you should have:

✅ **In PR_INTENTS.jsonl:**
- New intent with status `"completed"` (or `"failed"`)
- Result populated with PR number and URL (if successful)

✅ **In EVENT_TIMELINE.jsonl:**
- `SLICE_PR_INTENT_CREATED` event
- `PR_INTENT_PROCESSING` event
- `PR_CREATED` event (or `PR_CREATION_FAILED`)

✅ **On GitHub:**
- New PR: https://github.com/edri2or-commits/ai-os/pull/{NUMBER}
- New branch: `ai-os-pr-{timestamp}`
- PR contains all 4 slice files
- PR description has overview, changes, features

✅ **Locally:**
- No uncommitted changes (optional)
- Outbox and timeline updated
- Ready for next slice

---

## 🎓 What You Learned

By completing this runbook, you:

1. ✅ Verified a completed slice has proper documentation
2. ✅ Created a PR Intent from slice metadata (automated)
3. ✅ Processed the intent through PR_CONTRACT_V1 (async)
4. ✅ Saw the full Slice → PR pipeline in action
5. ✅ Understood failure modes and how to debug

**Key Insight:**
- **Before:** Manual `git commit/push` for every slice (15+ commands)
- **After:** 2 commands (`publish_slice_as_pr.py` + `pr_worker.py`)
- **Result:** Consistent, traceable, automated slice publishing

---

## 🔗 Related Documentation

- **Pipeline Protocol:** `docs/protocols/SLICE_TO_PR_PIPELINE_V1.md`
- **PR Contract:** `docs/sync_contracts/PR_CONTRACT_V1.md`
- **Slice Docs:**
  - `docs/slices/SLICE_BOOTSTRAP_VALIDATOR_V1.md` (used in demo)
  - `docs/slices/SLICE_SLICE_TO_PR_PIPELINE_V1.md` (the pipeline itself)
- **Scripts:**
  - `scripts/publish_slice_as_pr.py`
  - `scripts/pr_worker.py`

---

**Runbook Version:** 1.0  
**Last Updated:** 2025-11-28  
**Status:** ✅ Complete  
**Tested With:** SLICE_BOOTSTRAP_VALIDATOR_V1
