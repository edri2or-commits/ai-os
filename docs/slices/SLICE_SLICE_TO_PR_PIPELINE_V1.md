# SLICE_SLICE_TO_PR_PIPELINE_V1

**Date:** 2025-11-28  
**Phase:** 2.3 (INFRA_ONLY)  
**Status:** ✅ COMPLETE  
**Type:** Pipeline & Automation (Infrastructure)

---

## 🎯 Goal

Close a critical infrastructure gap: **Turn completed slices into structured GitHub PRs** using PR_CONTRACT_V1, eliminating manual `git commit/push` workflows.

**Before This Slice:**
- Manual `git commit` + `git push` for every slice
- Inconsistent PR formats and descriptions
- No automation for slice → PR conversion
- Manual file tracking and content assembly
- Each slice PR creation was bespoke

**After This Slice:**
- **Single command:** `publish_slice_as_pr.py --slice-name SLICE_X`
- Automatic PR Intent creation from slice metadata
- Consistent PR format (overview, changes, features, docs link)
- Integration with PR_CONTRACT_V1 (async, traceable, fault-tolerant)
- Slices are first-class citizens with standardized publishing

---

## 📁 Files Created/Modified

### Created (3 files)

1. **`docs/protocols/SLICE_TO_PR_PIPELINE_V1.md`** (~650 lines)
   - **THE** pipeline protocol specification
   - Inputs: slice name, slice doc, timeline event
   - Outputs: PR Intent, timeline event
   - Mapping: slice metadata → PR spec
   - Execution flow (5 steps)
   - Testing guide
   - Usage patterns
   - V2+ enhancements

2. **`scripts/publish_slice_as_pr.py`** (~480 lines)
   - CLI tool for creating PR Intents from slices
   - **Args:**
     - `--slice-name` (required): Slice to publish
     - `--dry-run`: Preview without saving
     - `--title`: Override PR title
     - `--base-branch`: Target branch (default: main)
   - **Flow:**
     1. Validate slice doc exists + SLICE_COMPLETE event
     2. Extract metadata (description, files, features)
     3. Read file contents from disk
     4. Build PR spec (title, description, files array)
     5. Create intent + log event
   - **Output:** PR Intent in PR_INTENTS.jsonl

3. **`docs/slices/SLICE_SLICE_TO_PR_PIPELINE_V1.md`** (this file)
   - Slice documentation

### Modified (0 files)

No existing files modified in V1.

---

## 🔄 How It Works

### Pipeline Architecture

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

### 5-Step Execution Flow

**Step 1: Validate**
- Check slice doc exists: `docs/slices/<SLICE_NAME>.md`
- Find SLICE_COMPLETE event in timeline
- Verify files exist on disk

**Step 2: Extract Metadata**
- Parse slice doc (Goal section, files lists)
- Load SLICE_COMPLETE event (description, files, features)
- Merge metadata (event takes precedence)

**Step 3: Read File Contents**
- For each file in files_created/modified:
  - Read full content from disk
  - Calculate size
- Build files[] array with operation (create/update)

**Step 4: Build PR Spec**
- **Title:** `<SLICE_NAME> - <Brief description>`
- **Description:**
  ```markdown
  ## Overview
  <Summary>
  
  ## Changes
  **Created:** ...
  **Modified:** ...
  
  ## Key Features
  - feature1
  - feature2
  
  ## Documentation
  See: docs/slices/<SLICE_NAME>.md
  
  ## Phase
  Phase 2.3 (INFRA_ONLY)
  ```
- **Files:** Array with path, content, operation

**Step 5: Create Intent**
- Generate intent_id: `slice-<SLICE_NAME>-<timestamp>-<random>`
- Set status: "pending"
- Append to PR_INTENTS.jsonl
- Log SLICE_PR_INTENT_CREATED event

---

## 🧪 Usage Examples

### Example 1: Basic Usage

**Publish a completed slice:**

```bash
python scripts/publish_slice_as_pr.py --slice-name SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1
```

**Expected Output:**
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
  Reading: docs/system_state/timeline/EVENT_TIMELINE.jsonl (1.2 KB)
  Total content size: 29.8 KB

[4/5] Building PR spec
  Title: SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1 - Formal Chat Bootstrap Protocol
  Description: 15 lines
  Files: 5 entries

[5/5] Creating PR Intent
  Intent ID: slice-SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1-1732756800-a1b2c3
  Saved to: docs/system_state/outbox/PR_INTENTS.jsonl
  Logged event: SLICE_PR_INTENT_CREATED

======================================================================
✅ PR Intent Created Successfully
======================================================================

Intent ID: slice-SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1-1732756800-a1b2c3
Slice: SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1
Files: 5
PR Title: SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1 - Formal Chat Bootstrap Protocol

Next step: Run pr_worker.py to create the PR on GitHub
```

**Process the intent:**
```bash
python scripts/pr_worker.py
```

**Result:**
- PR created on GitHub
- Intent status → "completed"
- PR_CREATED event in timeline

---

### Example 2: Dry Run (Preview)

**Preview what will be created:**

```bash
python scripts/publish_slice_as_pr.py --slice-name SLICE_BOOTSTRAP_VALIDATOR_V1 --dry-run
```

**Expected Output:**
```
======================================================================
  Slice to PR Pipeline - Creating PR Intent
======================================================================

[1/5] Validating slice: SLICE_BOOTSTRAP_VALIDATOR_V1
  ✓ Slice doc found: docs/slices/SLICE_BOOTSTRAP_VALIDATOR_V1.md
  ✓ SLICE_COMPLETE event found in timeline
  ✓ Files exist on disk: 5 files

[2/5] Extracting metadata
  Slice description: Bootstrap handshake validator - automated validation tool
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
  Description: 12 lines
  Files: 4 entries

[5/5] DRY RUN - Not saving intent

Would create intent:
{
  "intent_id": "slice-SLICE_BOOTSTRAP_VALIDATOR_V1-1732757100-x9y2z1",
  "created_at": "2025-11-28T02:05:00Z",
  ...
}

======================================================================
DRY RUN COMPLETE
======================================================================

Intent ID: slice-SLICE_BOOTSTRAP_VALIDATOR_V1-1732757100-x9y2z1
Slice: SLICE_BOOTSTRAP_VALIDATOR_V1
Files: 4
PR Title: SLICE_BOOTSTRAP_VALIDATOR_V1 - Bootstrap handshake validator
```

**Note:** No files modified, no events logged.

---

### Example 3: Custom Title

**Override auto-generated title:**

```bash
python scripts/publish_slice_as_pr.py \
  --slice-name SLICE_EXPERIMENTAL_V1 \
  --title "🧪 Experimental Feature - Initial Prototype"
```

---

### Example 4: Different Branch

**Target a feature branch:**

```bash
python scripts/publish_slice_as_pr.py \
  --slice-name SLICE_X_V1 \
  --base-branch feature/new-contracts
```

---

## 📊 Generated PR Intent Structure

### Example Intent (SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1)

```json
{
  "intent_id": "slice-SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1-1732756800-a1b2c3",
  "created_at": "2025-11-28T02:00:00Z",
  "created_by": "slice_to_pr_pipeline_v1",
  "status": "pending",
  "pr_spec": {
    "title": "SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1 - Formal Chat Bootstrap Protocol",
    "description": "## Overview\n\nFormal Chat Bootstrap Protocol for consistent session initialization\n\n## Changes\n\n**Created:**\n- `docs/protocols/CHAT_BOOTSTRAP_PROTOCOL_V1.md`\n- `docs/protocols/CHAT_BOOTSTRAP_PROMPT_TEMPLATE_V1.md`\n- `docs/session/SESSION_MANIFEST_TEMPLATE_V1.json`\n- `docs/slices/SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1.md`\n\n**Modified:**\n- `docs/system_state/timeline/EVENT_TIMELINE.jsonl`\n\n## Key Features\n\n- 5-step bootstrap flow\n- ACK_CONTEXT_LOADED handshake format\n- Truth Sources (COMPACT, GOVERNANCE, TIMELINE)\n- Session manifest template\n- Bootstrap prompt template\n\n## Documentation\n\nSee full details: `docs/slices/SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1.md`\n\n## Phase\n\nPhase 2.3 (INFRA_ONLY)\n",
    "files": [
      {
        "path": "docs/protocols/CHAT_BOOTSTRAP_PROTOCOL_V1.md",
        "content": "# CHAT_BOOTSTRAP_PROTOCOL_V1\n\n**Version:** 1.0...",
        "operation": "create"
      },
      {
        "path": "docs/protocols/CHAT_BOOTSTRAP_PROMPT_TEMPLATE_V1.md",
        "content": "# Chat Bootstrap Prompt Template V1...",
        "operation": "create"
      },
      {
        "path": "docs/session/SESSION_MANIFEST_TEMPLATE_V1.json",
        "content": "{\n  \"schema_version\": \"SESSION_MANIFEST_V1\"...",
        "operation": "create"
      },
      {
        "path": "docs/slices/SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1.md",
        "content": "# SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1...",
        "operation": "create"
      },
      {
        "path": "docs/system_state/timeline/EVENT_TIMELINE.jsonl",
        "content": "{\"timestamp\": \"2025-11-27T...",
        "operation": "update"
      }
    ],
    "base_branch": "main",
    "use_ai_generation": false
  },
  "trace_id": "slice-SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1-1732756800-a1b2c3",
  "result": null,
  "error": null,
  "error_type": null,
  "processed_at": null
}
```

---

## 📋 Generated Timeline Event

### SLICE_PR_INTENT_CREATED

```json
{
  "timestamp": "2025-11-28T02:00:00Z",
  "event_type": "SLICE_PR_INTENT_CREATED",
  "source": "slice_to_pr_pipeline_v1",
  "payload": {
    "slice_name": "SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1",
    "intent_id": "slice-SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1-1732756800-a1b2c3",
    "files_count": 5,
    "pr_title": "SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1 - Formal Chat Bootstrap Protocol"
  }
}
```

---

## ⚠️ Known Limitations (V1)

### What V1 Does:

✅ **Reads slice metadata** from slice doc + timeline  
✅ **Reads file contents** from disk  
✅ **Creates PR Intent** following PR_CONTRACT_V1  
✅ **Logs event** to timeline  
✅ **Dry run mode** for preview  

### What V1 Does NOT Do:

❌ **Auto-execute worker** - Must manually run `pr_worker.py`  
❌ **Generate diffs** - Sends full files, not diffs  
❌ **Detect create vs update perfectly** - Best-effort heuristic  
❌ **Filter large files** - Includes all files regardless of size  
❌ **Validate file syntax** - No pre-flight checks  
❌ **Batch multiple slices** - One slice at a time  
❌ **n8n integration** - No workflow automation  

---

## 🔮 Future Enhancements (V2+)

### V2 - Automation

1. **Auto-Execute Worker:**
   ```bash
   python scripts/publish_slice_as_pr.py --slice-name SLICE_X --execute
   # Creates intent AND runs pr_worker automatically
   ```

2. **n8n Workflow:**
   - Trigger: SLICE_COMPLETE event detected
   - Actions: Create intent → run worker → notify
   - Workflow: `SLICE_TO_PR_WORKFLOW_V1`

### V3 - Enhanced Metadata

3. **Diff Generation:**
   - For `update` operations, include git diff in PR description
   - Show what changed vs previous version

4. **Smart Operation Detection:**
   - Use git history to accurately determine create vs update
   - Check if file exists in git history

5. **File Filtering:**
   - `--exclude` patterns for large/binary files
   - `--max-size` to skip files over threshold
   - Auto-skip generated files (e.g., `__pycache__`)

### V4 - Advanced Features

6. **Batch Processing:**
   ```bash
   python scripts/publish_slice_as_pr.py --multiple SLICE_A SLICE_B SLICE_C
   # Create intents for multiple slices
   ```

7. **PR Templates:**
   - Customizable description templates
   - Different templates for different slice types
   - `--template` argument

8. **Validation:**
   - Pre-flight checks (files exist, valid syntax)
   - Lint integration
   - Test execution before PR creation

---

## 🎓 Usage Patterns

### Pattern 1: Standard Workflow

```bash
# 1. Complete slice implementation
# 2. Update slice doc with files, summary
# 3. Add SLICE_COMPLETE event to timeline

# 4. Create PR intent
python scripts/publish_slice_as_pr.py --slice-name SLICE_X_V1

# 5. Process intent (create PR on GitHub)
python scripts/pr_worker.py

# 6. PR now available for review on GitHub
```

### Pattern 2: Preview Before Publishing

```bash
# 1. Dry run to preview
python scripts/publish_slice_as_pr.py --slice-name SLICE_X_V1 --dry-run

# 2. Review output
# 3. If looks good, publish for real
python scripts/publish_slice_as_pr.py --slice-name SLICE_X_V1

# 4. Process
python scripts/pr_worker.py
```

### Pattern 3: Immediate Publishing (V2)

```bash
# Future: Single command end-to-end
python scripts/publish_slice_as_pr.py --slice-name SLICE_X_V1 --execute
# Creates intent AND opens PR in one step
```

---

## 🔗 Relationship to Other Slices

This slice builds on and integrates with:

1. **SLICE_SYNC_WRITE_CONTRACT_PR_V1:**
   - Uses PR_CONTRACT_V1 for async PR creation
   - Leverages PR Intent + Worker pattern
   - Follows same outbox architecture

2. **SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1:**
   - **First use case:** Can publish bootstrap protocol as PR
   - Example slice with complete metadata

3. **SLICE_BOOTSTRAP_VALIDATOR_V1:**
   - **Second use case:** Can publish validator slice as PR
   - Another example with full documentation

---

## 📚 Related Documentation

- **Protocol:** `docs/protocols/SLICE_TO_PR_PIPELINE_V1.md`
- **PR Contract:** `docs/sync_contracts/PR_CONTRACT_V1.md`
- **Worker:** `scripts/pr_worker.py`
- **Intent Creator:** `scripts/create_pr_intent.py`
- **Slice Docs:** `docs/slices/SLICE_*.md`

---

## ✅ Success Criteria

Pipeline is successful when:

✅ **Single command creates PR Intent** from slice metadata  
✅ **All slice files included** with full content  
✅ **PR description clear** (overview, changes, features)  
✅ **Intent follows PR_CONTRACT_V1** exactly  
✅ **Timeline event logged** for traceability  
✅ **Worker can process intent** → create PR  
✅ **No git commands** (contract-based only)  
✅ **Dry run mode works** (preview without modifying)  

---

## 🎯 Strategic Impact

**Pattern Established:**
- First pipeline for automated slice publishing
- Template for future slice workflows
- Slices are now first-class with standardized PR creation

**Before This Slice:**
- Manual git workflow for every slice
- Inconsistent PR descriptions
- No automation
- High friction

**After This Slice:**
- One command: `publish_slice_as_pr.py`
- Consistent PR format
- Integration with PR_CONTRACT_V1
- Low friction, repeatable

**Next Steps:**
- Use this pipeline for all future slices
- Enhance with V2 features (auto-execute, n8n, diff generation)
- Extend pattern to other content types (protocols, docs, etc.)

---

**Slice Completed:** 2025-11-28  
**Next Slice:** TBD (possibly Email Contract or Task Contract)  
**Status:** ✅ COMPLETE  
**Pattern Established:** Slice → PR Pipeline using PR_CONTRACT_V1
