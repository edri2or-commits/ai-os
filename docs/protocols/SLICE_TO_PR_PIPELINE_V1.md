# Slice to PR Pipeline Protocol V1

**Version:** 1.0  
**Date:** 2025-11-28  
**Phase:** 2.3 (INFRA_ONLY)  
**Status:** ✅ Active

---

## 🎯 Purpose

This protocol defines a **repeatable pipeline** for publishing completed slices as GitHub Pull Requests using the existing PR_CONTRACT_V1.

**Before This Protocol:**
- Manual `git commit` + `git push` for each slice
- Inconsistent PR formats
- No automation for slice → PR conversion
- Manual file tracking

**After This Protocol:**
- Single command: `publish_slice_as_pr.py --slice-name SLICE_X`
- Automatic PR Intent creation from slice metadata
- Consistent PR format (title, description, files)
- Integration with PR_CONTRACT_V1 (async, traceable, fault-tolerant)

---

## 📐 Architecture

```
Completed Slice
    ↓
Slice Doc (docs/slices/SLICE_*.md)
    +
Timeline Event (SLICE_COMPLETE)
    ↓
publish_slice_as_pr.py
    ↓
PR Intent (PR_INTENTS.jsonl)
    ↓
pr_worker.py
    ↓
mcp_github_client
    ↓
GitHub PR
```

---

## 📥 Inputs

### Required:

1. **Slice Name**
   - Format: `SLICE_<NAME>_V<N>`
   - Example: `SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1`

2. **Slice Doc**
   - Path: `docs/slices/<SLICE_NAME>.md`
   - Must contain:
     - Goal / summary
     - Files Created/Modified section

3. **Timeline Event**
   - `SLICE_COMPLETE` event in `EVENT_TIMELINE.jsonl`
   - Must contain:
     - `files_created` array
     - `files_modified` array (optional)
     - `description` (brief summary)

### Optional:

4. **Override Title**
   - Custom PR title (defaults to slice name)

5. **Override Description**
   - Custom PR description (defaults to auto-generated)

---

## 📤 Outputs

### 1. PR Intent

Created in: `docs/system_state/outbox/PR_INTENTS.jsonl`

**Structure:**
```json
{
  "intent_id": "slice-<SLICE_NAME>-<timestamp>-<random>",
  "created_at": "2025-11-28T02:00:00Z",
  "created_by": "slice_to_pr_pipeline_v1",
  "status": "pending",
  "pr_spec": {
    "title": "SLICE_<NAME>_V<N> - Brief description",
    "description": "## Overview\n\nSlice summary...\n\n## Changes\n\n- Created: ...\n- Modified: ...\n\n## Details\n\nSee: docs/slices/<SLICE_NAME>.md",
    "files": [
      {
        "path": "docs/slices/SLICE_NAME.md",
        "content": "<full file content>",
        "operation": "create"
      }
    ],
    "base_branch": "main",
    "use_ai_generation": false
  },
  "trace_id": "slice-<SLICE_NAME>-<timestamp>-<random>",
  "result": null,
  "error": null,
  "error_type": null,
  "processed_at": null
}
```

### 2. Timeline Event

Created in: `docs/system_state/timeline/EVENT_TIMELINE.jsonl`

**Event Type:** `SLICE_PR_INTENT_CREATED`

**Structure:**
```json
{
  "timestamp": "2025-11-28T02:00:00Z",
  "event_type": "SLICE_PR_INTENT_CREATED",
  "source": "slice_to_pr_pipeline_v1",
  "payload": {
    "slice_name": "SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1",
    "intent_id": "slice-SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1-1732756800-a1b2c3",
    "files_count": 6,
    "pr_title": "SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1 - Formal Chat Bootstrap Protocol"
  }
}
```

---

## 🗺️ Mapping: Slice → PR Spec

### Title

**Default Format:**
```
<SLICE_NAME> - <Brief Description>
```

**Example:**
```
SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1 - Formal Chat Bootstrap Protocol
```

**Source:**
- Extract brief description from:
  - Slice doc "Goal" section (first line)
  - OR SLICE_COMPLETE event `description` field

### Description

**Default Format:**
```markdown
## Overview

<Summary from slice doc's "Goal" section>

## Changes

**Created:**
- path1
- path2

**Modified:**
- path3

## Key Features

- feature1
- feature2

## Documentation

See full details: `docs/slices/<SLICE_NAME>.md`

## Phase

Phase 2.3 (INFRA_ONLY)
```

**Source:**
- Goal: Slice doc "Goal" section
- Files: SLICE_COMPLETE event `files_created` / `files_modified`
- Features: SLICE_COMPLETE event `key_features` or slice doc highlights

### Files Array

**For Each File:**

1. **Get Path:**
   - From `files_created` or `files_modified` in SLICE_COMPLETE event
   - OR from "Files Created/Modified" section in slice doc

2. **Read Content:**
   - Read actual file from disk: `REPO_ROOT / path`
   - **CRITICAL:** Must include FULL file content (PR_CONTRACT_V1 requirement)

3. **Determine Operation:**
   - **Best-effort logic:**
     - If in `files_created` → `"create"`
     - If in `files_modified` → `"update"`
     - If uncertain → `"update"` (safer default)

**Example:**
```json
{
  "path": "docs/protocols/CHAT_BOOTSTRAP_PROTOCOL_V1.md",
  "content": "# CHAT_BOOTSTRAP_PROTOCOL_V1\n\n**Version:** 1.0...",
  "operation": "create"
}
```

### Base Branch

**Default:** `"main"`

Can be overridden with `--base-branch` CLI argument.

---

## 🔄 Execution Flow

### Step-by-Step Pipeline

```
1. Validate Inputs
   ├─ Slice doc exists?
   ├─ SLICE_COMPLETE event exists?
   └─ Files exist on disk?

2. Extract Metadata
   ├─ Read slice doc → parse Goal, files
   ├─ Read TIMELINE → find SLICE_COMPLETE event
   └─ Combine metadata

3. Read File Contents
   ├─ For each file in files_created/modified:
   ├─ Read from disk (full content)
   └─ Build files[] array

4. Build PR Spec
   ├─ Generate title (slice name + brief desc)
   ├─ Generate description (overview, changes, features)
   └─ Assemble pr_spec object

5. Create Intent
   ├─ Generate intent_id
   ├─ Set status: "pending"
   ├─ Append to PR_INTENTS.jsonl
   └─ Log SLICE_PR_INTENT_CREATED event

6. Output Summary
   └─ Print: intent_id, slice_name, files_count, pr_title
```

### Command:

```bash
python scripts/publish_slice_as_pr.py --slice-name SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1
```

### Expected Output:

```
======================================================================
  Slice to PR Pipeline - Creating PR Intent
======================================================================

[1/5] Validating slice: SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1
  ✓ Slice doc found: docs/slices/SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1.md
  ✓ SLICE_COMPLETE event found in timeline
  ✓ Files exist on disk: 6 files

[2/5] Extracting metadata
  Slice description: Formal Chat Bootstrap Protocol for consistent session initialization
  Files created: 5
  Files modified: 1

[3/5] Reading file contents
  Reading: docs/protocols/CHAT_BOOTSTRAP_PROTOCOL_V1.md (12.5 KB)
  Reading: docs/protocols/CHAT_BOOTSTRAP_PROMPT_TEMPLATE_V1.md (3.2 KB)
  Reading: docs/session/SESSION_MANIFEST_TEMPLATE_V1.json (4.8 KB)
  Reading: docs/slices/SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1.md (8.1 KB)
  Reading: docs/system_state/timeline/EVENT_TIMELINE.jsonl (1.2 KB, tail)
  Total content size: 29.8 KB

[4/5] Building PR spec
  Title: SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1 - Formal Chat Bootstrap Protocol
  Description: 15 lines
  Files: 6 entries

[5/5] Creating PR Intent
  Intent ID: slice-SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1-1732756800-a1b2c3
  Saved to: docs/system_state/outbox/PR_INTENTS.jsonl
  Logged event: SLICE_PR_INTENT_CREATED

======================================================================
✅ PR Intent Created Successfully
======================================================================

Intent ID: slice-SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1-1732756800-a1b2c3
Slice: SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1
Files: 6
PR Title: SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1 - Formal Chat Bootstrap Protocol

Next step: Run pr_worker.py to create the PR on GitHub
```

### Dry Run:

```bash
python scripts/publish_slice_as_pr.py --slice-name SLICE_X --dry-run
```

Shows what would be created **without** modifying outbox or timeline.

---

## 🔐 Constraints

### Hard Constraints:

✅ **No Direct Git:** Script does NOT run `git commit`, `git push`, or any git commands  
✅ **PR_CONTRACT_V1 Only:** All PRs go through existing PR Contract  
✅ **INFRA_ONLY:** Only touches code/docs in AI-OS repo (no real-world services)  
✅ **Full File Content:** Must include complete file content in `files[].content`  
✅ **Truth Protocol:** All metadata from slice doc + timeline, not memory  

### Soft Constraints:

⚠️ **Operation Best-Effort:** `create` vs `update` determined heuristically  
⚠️ **Manual Worker Execution:** V1 requires manual `pr_worker.py` run  
⚠️ **No Diff Generation:** Sends full files, not diffs  
⚠️ **Single Branch:** All PRs target `main` (or override)  

---

## 🧪 Testing

### Test 1: Existing Slice

**Pick a completed slice:**
```bash
python scripts/publish_slice_as_pr.py \
  --slice-name SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1 \
  --dry-run
```

**Verify:**
- ✓ Prints summary
- ✓ Shows title, description, files
- ✓ No files modified

**Run without dry-run:**
```bash
python scripts/publish_slice_as_pr.py \
  --slice-name SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1
```

**Verify:**
- ✓ Intent added to PR_INTENTS.jsonl
- ✓ Event added to EVENT_TIMELINE.jsonl
- ✓ Status: "pending"

**Process intent:**
```bash
python scripts/pr_worker.py
```

**Verify:**
- ✓ Intent status → "completed"
- ✓ PR created on GitHub
- ✓ PR_CREATED event in timeline

---

### Test 2: Missing Slice

```bash
python scripts/publish_slice_as_pr.py \
  --slice-name SLICE_NONEXISTENT_V1
```

**Expected:**
```
[ERROR] Slice doc not found: docs/slices/SLICE_NONEXISTENT_V1.md
```

---

### Test 3: Missing Files

**Create slice doc but files don't exist:**

**Expected:**
```
[ERROR] File not found: docs/missing.md
Cannot create PR intent with missing files.
```

---

## 📊 Events

### SLICE_PR_INTENT_CREATED

Logged when PR Intent is created for a slice.

```json
{
  "timestamp": "2025-11-28T02:00:00Z",
  "event_type": "SLICE_PR_INTENT_CREATED",
  "source": "slice_to_pr_pipeline_v1",
  "payload": {
    "slice_name": "SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1",
    "intent_id": "slice-SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1-1732756800-a1b2c3",
    "files_count": 6,
    "pr_title": "SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1 - Formal Chat Bootstrap Protocol"
  }
}
```

---

## 🔮 Future Enhancements (V2+)

### V2 - Automation

1. **Auto-Execution:**
   - `--execute` flag to automatically run pr_worker after creating intent
   - Single command: slice → PR (end-to-end)

2. **n8n Integration:**
   - Workflow: `SLICE_TO_PR_WORKFLOW_V1`
   - Trigger: SLICE_COMPLETE event detected
   - Actions: Create intent → run worker → notify

### V3 - Enhanced Metadata

3. **Diff Generation:**
   - For `update` operations, include git diff in PR description
   - Show what changed vs previous version

4. **Auto-Detection:**
   - Smart detection of create vs update
   - Use git history to determine operation

5. **File Filtering:**
   - `--exclude` patterns for large/binary files
   - Auto-skip generated files

### V4 - Advanced Features

6. **Batch Processing:**
   - `--multiple` to create intents for multiple slices
   - Bulk PR creation

7. **PR Templates:**
   - Customizable PR description templates
   - Different templates for different slice types

8. **Validation:**
   - Pre-flight checks (files exist, syntax valid, etc.)
   - Lint/test integration before creating intent

---

## 🎓 Usage Patterns

### Pattern 1: Standard Slice Publishing

```bash
# Complete slice implementation
# Update slice doc, timeline, files

# Create PR intent
python scripts/publish_slice_as_pr.py --slice-name SLICE_X_V1

# Process intent (create PR)
python scripts/pr_worker.py

# PR now on GitHub for review
```

### Pattern 2: Dry Run First

```bash
# Preview what will be created
python scripts/publish_slice_as_pr.py --slice-name SLICE_X_V1 --dry-run

# If looks good, create for real
python scripts/publish_slice_as_pr.py --slice-name SLICE_X_V1

# Process
python scripts/pr_worker.py
```

### Pattern 3: Custom Branch

```bash
# Target different branch
python scripts/publish_slice_as_pr.py \
  --slice-name SLICE_X_V1 \
  --base-branch develop

python scripts/pr_worker.py
```

### Pattern 4: Override Title

```bash
# Custom PR title
python scripts/publish_slice_as_pr.py \
  --slice-name SLICE_X_V1 \
  --title "Experimental Feature X - Initial Implementation"

python scripts/pr_worker.py
```

---

## 📚 Related Documentation

- **PR Contract:** `docs/sync_contracts/PR_CONTRACT_V1.md`
- **Worker:** `scripts/pr_worker.py`
- **Intent Creator:** `scripts/create_pr_intent.py`
- **Slice Docs:** `docs/slices/SLICE_*.md`
- **Timeline:** `docs/system_state/timeline/EVENT_TIMELINE.jsonl`

---

## ✅ Success Criteria

Pipeline is successful when:

✅ Single command creates PR Intent from slice metadata  
✅ All files included with full content  
✅ PR description clearly explains what changed  
✅ Intent follows PR_CONTRACT_V1 schema exactly  
✅ Timeline event logged for traceability  
✅ Worker can process intent → create PR  
✅ No git commands executed (contract-based only)  

---

**Protocol Version:** 1.0  
**Last Updated:** 2025-11-28  
**Status:** ✅ Active  
**Phase:** 2.3 (INFRA_ONLY)
