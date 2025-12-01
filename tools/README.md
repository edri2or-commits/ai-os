# Tools Directory

Development and validation tools for AI Life OS.

---

## 🔍 Entity Validator

**Purpose:** Validates Life Graph entity files (Area, Project, Task, Context, Identity, Log) against the canonical schema.

**Location:** `tools/validate_entity.py`

### Installation

Run the setup script once to install validator + git hooks:

```bash
bash tools/setup_hooks.sh
```

This will:
- Install validator to `tools/validate_entity.py`
- Install pre-commit hook to `.git/hooks/pre-commit`
- Enable automatic validation on every commit

### Usage

**Validate a single file:**
```bash
python tools/validate_entity.py memory-bank/10_Projects/proj-2025-website.md
```

**Validate a directory (recursive):**
```bash
python tools/validate_entity.py memory-bank/10_Projects/
python tools/validate_entity.py memory-bank/TEMPLATES/
```

**Validate staged files (used by git hook):**
```bash
python tools/validate_entity.py --staged
```

### Example Output

**Valid file:**
```
✅ VALID: proj-2025-website.md
```

**Invalid file:**
```
❌ INVALID: proj-2025-broken.md
  - Missing required field: 'energy_profile'
  - Deprecated field 'dopamine_reward' - use 'dopamine_level' instead
  - Invalid status: 'done' (valid: planning, active, blocked, completed, archived)
```

### Git Integration

After running `setup_hooks.sh`, the validator runs automatically on every commit:

```bash
$ git commit -m "Add new project"

🔍 Validating Life Graph entities...
❌ INVALID: proj-2025-new.md
  - Missing required field: 'energy_profile'

❌ Validation failed. Fix errors above and try again.
💡 Tip: To bypass validation (use carefully): git commit --no-verify
```

**To bypass validation** (emergency only):
```bash
git commit --no-verify -m "WIP: Incomplete entity"
```

---

## 📋 What the Validator Checks

### Required Fields

Each entity type has specific required fields:

- **Area:** `type`, `id`, `name`, `active`
- **Project:** `type`, `id`, `title`, `status`, `created`, `energy_profile`, `dopamine_level`
- **Task:** `type`, `id`, `title`, `status`, `created`, `energy_profile`, `contexts`
- **Context:** `type`, `context_name`
- **Identity:** `type`, `id`, `title`
- **Log:** `type`, `id`, `timestamp`

### Field Name Validation

Checks for deprecated field names and suggests canonical alternatives:

- ❌ `dopamine_reward` → ✅ `dopamine_level`
- ❌ `scheduled` (in Project) → ✅ `do_date`

### Enum Validation

Validates enum fields have valid values:

- **status:** `planning`, `active`, `blocked`, `completed`, `archived` (Project)
- **status:** `inbox`, `next`, `waiting`, `scheduled`, `completed` (Task)
- **energy_profile:** `high_focus`, `creative`, `admin`, `low_energy`
- **dopamine_level:** `high`, `medium`, `low`, `negative`

### ID Format Validation

Checks ID follows naming convention:

- Area: `area-{slug}` (e.g., `area-health`)
- Project: `proj-{YYYY}-{slug}` (e.g., `proj-2025-website`)
- Task: `task-{slug}` (e.g., `task-homepage-copy`)
- Identity: `role-{slug}` (e.g., `role-writer`)
- Log: `log-YYYY-MM-DD-HHMM` (e.g., `log-2025-12-01-1430`)

---

## 👁️ Observer (Drift Detection)

**Purpose:** Read-only drift detection system. Compares Truth Layer (files) with actual system state and reports discrepancies.

**Location:** `tools/observer.py`

### What Observer Checks

Observer detects **5 types of drift:**

1. **Git Drift** - HEAD commit doesn't match `last_commit` in SYSTEM_STATE_COMPACT.json
2. **Schema Violations** - Entity files that fail validator checks
3. **Orphaned Entities** - Tasks/Projects without parent Area
4. **Broken Links** - References to non-existent entities (e.g., `project: proj-does-not-exist`)
5. **Stale Timestamps** - Future dates or old active entities (>6 months) without updates

### Usage

**Run Observer:**
```bash
python tools/observer.py
```

**Output:**
```
🔍 Running Observer...

   [1/5] Checking Git drift...
   [2/5] Validating entities (reusing validator)...
   [3/5] Checking orphaned entities...
   [4/5] Checking broken links...
   [5/5] Checking stale timestamps...

📝 Generating reports...

============================================================
🔍 Observer Report (2025-12-01 14:30:15)
============================================================

⚠️  3 issues found:

   ❌ Git Drift: 1
   ❌ Schema Violations: 1
   ⚠️  Orphaned Entities: 1

📊 Drift Score: 3 issues detected
📝 Full report: docs/system_state/drift/DRIFT_REPORT.md
📄 JSON report: docs/system_state/drift/DRIFT_LATEST.json
============================================================
```

### Reports Generated

**Markdown Report** (`docs/system_state/drift/DRIFT_REPORT.md`):
- Human-readable summary
- Detailed findings by drift type
- Next steps & remediation guidance
- ADHD-friendly formatting (headings, bullets, short sections)

**JSON Report** (`docs/system_state/drift/DRIFT_LATEST.json`):
- Machine-readable format
- Full drift_items array with details
- Statistics by drift type
- Timestamp of generation

### Example Drift Types

**Git Drift:**
```
❌ Git HEAD mismatch
  - actual: 9f2bed6
  - expected: 6473aa3
```

**Schema Violation:**
```
❌ Schema violation in memory-bank/10_Projects/proj-broken.md
  - Missing required field: 'energy_profile'
  - Deprecated field 'dopamine_reward' - use 'dopamine_level'
```

**Orphaned Entity:**
```
⚠️  Orphaned task: task-homepage-copy (no project or area)
  - file: memory-bank/00_Inbox/task-homepage-copy.md
```

**Broken Link:**
```
❌ Broken link in task-review: project 'proj-website' not found
  - file: memory-bank/10_Projects/task-review.md
  - broken_ref: proj-website
```

**Stale Timestamp:**
```
ℹ️  Old active entity without updated field: proj-2024-old (created 2024-05-15)
  - file: memory-bank/10_Projects/proj-2024-old.md
  - status: active
```

### Key Features

✅ **Read-Only** - Never modifies files (safe to run anytime)  
✅ **Reuses Validator** - Same schema logic as pre-commit hook  
✅ **Dual Reports** - Markdown (human) + JSON (machine)  
✅ **Clear Console** - ADHD-friendly progress indicators  
✅ **Foundation** - Prepares for Reconciler (Slice 2.4)

### When to Run Observer

- **Before major work** - Check system health
- **After manual edits** - Verify no drift introduced
- **Weekly check** - Catch accumulated drift
- **Before reconciliation** - Identify what needs fixing

**Note:** Observer is **manual only** (run when you want). Scheduled/automated runs coming in future slice (2.3b).

---

## 🔧 Reconciler (Change Request Management)

**Purpose:** Change Request (CR) lifecycle management. Generates CRs from Observer drift reports, enables approval/rejection workflows.

**Status:** ✅ **CR Management Operational** (Slice 2.4b) - Apply logic coming in Slice 2.4c

**Location:** `tools/reconciler.py`

### Architecture Overview

The **Reconciler** is the **write side** of the drift detection + remediation loop:

```
Observer (Read) → Drift Reports → Reconciler (Write) → Change Requests → HITL Approval → Applied Changes
```

### Change Requests (CRs)

A **Change Request (CR)** is a YAML file proposing a specific modification to fix drift:

**Location:** `docs/system_state/change_requests/CR-YYYYMMDD-NNN.cr.yaml`

**Example CR:**
```yaml
cr_id: "CR-20251201-001"
timestamp: "2025-12-01T10:30:00Z"
status: "proposed"  # proposed → approved → applied

drift_type: "stale_timestamp"
affected_entity:
  type: "task"
  id: "task-20251128-001"
  path: "memory-bank/.../task-20251128-001.md"

proposed_changes:
  field: "updated_at"
  current_value: "2025-11-28T14:00:00Z"
  proposed_value: "2025-12-01T10:30:00Z"
  operation: "update"

risk_level: "low"
requires_approval: true
```

### CR Lifecycle

1. **Observer detects drift** → generates CR file
2. **User reviews CR** (manual or via CLI)
3. **User approves/rejects:**
   - Approve: `reconciler approve CR-20251201-001`
   - Reject: `reconciler reject CR-20251201-001 --reason "Not needed"`
4. **Reconciler applies** approved CR:
   - Updates entity file
   - Git commits with CR reference
   - Updates CR status to "applied"

### Observer → CR Mapping

| Drift Type | CR Action | Risk Level | Auto-Approvable? |
|------------|-----------|------------|-----------------|
| **git_head_drift** | Update `last_commit` metadata | LOW | Future: YES |
| **stale_timestamp** | Update `updated_at` to current time | LOW | Future: YES |
| **orphaned_entity** | Add parent OR move to archive | MEDIUM | NO (human decision) |
| **broken_link** | Remove invalid link | MEDIUM | NO (may indicate deeper issue) |
| **schema_violation** | Fix field (rename/add/remove) | MEDIUM-HIGH | NO (validator should catch) |

### Safety Invariants

**INV-CR-001:** All entity modifications MUST go through CR system (audit trail)

**INV-CR-002:** HIGH risk CRs MUST require explicit approval

**INV-CR-003:** Every CR MUST be git-reversible (`git revert` always works)

**INV-CR-004:** CRs are derived state [PROPOSAL] - not tracked in git for now (may revisit)

**INV-CR-005:** CR application is atomic (update + commit + status, or rollback everything)

### Usage (Slice 2.4b - CR Management Only)

**Generate CRs from drift report:**
```bash
python tools/reconciler.py generate

# Or from specific report
python tools/reconciler.py generate --report docs/system_state/drift/drift-20251201.md
```

**List CRs:**
```bash
# List all CRs
python tools/reconciler.py list

# Filter by status
python tools/reconciler.py list --status proposed
python tools/reconciler.py list --status approved
python tools/reconciler.py list --status rejected
```

**Show specific CR:**
```bash
python tools/reconciler.py show CR-20251201-001
```

**Approve CR:**
```bash
python tools/reconciler.py approve CR-20251201-001

# With custom reviewer name
python tools/reconciler.py approve CR-20251201-001 --reviewed-by "edri2or"
```

**Reject CR:**
```bash
python tools/reconciler.py reject CR-20251201-001 --reason "Not needed"
```

**IMPORTANT - Slice 2.4b Scope:**
- ✅ Generate CRs from drift reports
- ✅ List/show CRs
- ✅ Approve/reject CRs (updates CR file only)
- ❌ **NO `apply` command yet** (coming in Slice 2.4c)
- ❌ NO entity modifications
- ❌ NO git commits from reconciler

### Example Workflow

```bash
# Step 1: Observer detects drift (generates report)
# (Observer tool not yet implemented - use sample report for now)

# Step 2: Generate CRs from drift report
python tools/reconciler.py generate
# Output: ✅ Generated CR-20251201-001 (git_head_drift)
#         ✅ Generated CR-20251201-002 (stale_timestamp)

# Step 3: Review proposed CRs
python tools/reconciler.py list --status proposed
# Output:
# CR ID               | Drift Type         | Risk  | Status
# --------------------|-------------------|-------|----------
# CR-20251201-001     | git_head_drift    | low   | proposed
# CR-20251201-002     | stale_timestamp   | low   | proposed

# Step 4: Show details
python tools/reconciler.py show CR-20251201-001
# Output: (full YAML content)

# Step 5: Approve or reject
python tools/reconciler.py approve CR-20251201-001
# Output: ✅ Approved CR-20251201-001

python tools/reconciler.py reject CR-20251201-002 --reason "Entity archived"
# Output: ❌ Rejected CR-20251201-002

# Step 6: Apply approved CRs (Slice 2.4c - not yet implemented)
# python tools/reconciler.py apply
```

### Dependencies

**Required Python packages:**
```bash
pip install pyyaml jsonschema --break-system-packages
```

*(Already in `tools/requirements.txt` if installed during validator setup)*

### Documentation

- **Design Doc:** `docs/RECONCILER_DESIGN.md` (architecture, workflow, safety)
- **CR Schema:** `docs/schemas/change_request.schema.json` (validation)
- **CR Template:** `memory-bank/TEMPLATES/change_request_template.yaml` (examples)

### Implementation Status

- **Slice 2.4a:** ✅ Design & CR format (complete)
- **Slice 2.4b:** ✅ CR management (generate/list/show/approve/reject)
- **Slice 2.4c:** ⏭ Apply logic (entity modifications + git commits)
- **Slice 2.4d:** ⏭ Expand drift coverage (orphaned entities, broken links)
- **Slice 2.4e:** ⏭ Observer+Reconciler integration

**Phase 2 Policy:** All CRs require manual approval (conservative, safe)

---

## 🚀 Future Tools

Planned additions to this directory:

- **Entity Creator** - CLI for creating new entities from templates
- **Graph Visualizer** - Visualize Life Graph relationships

---

## 📚 Documentation

- **Schema Reference:** `memory-bank/docs/LIFE_GRAPH_SCHEMA.md`
- **Templates:** `memory-bank/TEMPLATES/`
- **Playbook:** `claude-project/ai-life-os-claude-project-playbook.md`

---

**Last Updated:** 2025-12-01  
**Version:** 1.1 (Slice 2.4a - Reconciler design complete)
