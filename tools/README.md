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

**Purpose:** CLI tool for detecting drift in truth-layer YAML files by comparing working tree to last git commit.

**Version:** 0.1.0 (Slice 2.6)  
**Location:** `tools/observer.py`  
**Status:** ✅ Operational

### What Observer Does

Observer detects drift in **truth-layer YAML files only**:
- Compares current files to last git commit (HEAD)
- Identifies: modified, added, or deleted YAML files
- Generates structured drift reports
- Exit codes: 0 (clean), 1 (drift), 2 (error)

**Scope:**
- ✅ Scans: `truth-layer/*.yaml` files only
- ❌ Does NOT scan: `docs/`, `governance/`, `claude-project/`
- ❌ Does NOT detect: schema violations, orphaned entities, broken links (future work)

### Usage

**Basic usage:**
```bash
python tools/observer.py

# Output (if clean):
# [OK] No drift detected (5 files scanned)

# Output (if drift):
# [!] Drift detected (2 files)
# Report: truth-layer/drift/2025-12-02-143000-drift.yaml
```

**Verbose mode:**
```bash
python tools/observer.py --verbose

# Output:
# [Observer] Repository root: C:\Users\...\ai-os
# [Observer] Found 5 YAML files in truth-layer
# [Observer] Detecting drift...
# [Observer]   MODIFIED: truth-layer/projects/PR-001.yaml
# [Observer]   ADDED: truth-layer/tasks/T-042.yaml
# [Observer] Report generated: truth-layer/drift/2025-12-02-143000-drift.yaml
#
# [!] Drift detected (2 files)
# Report: truth-layer/drift/2025-12-02-143000-drift.yaml
```

### Drift Report Format

**Location:** `truth-layer/drift/YYYY-MM-DD-HHMMSS-drift.yaml` (git-ignored)

**Example report:**
```yaml
metadata:
  detected_at: "2025-12-02T14:30:00Z"
  observer_version: "0.1.0"
  files_scanned: 5
  files_with_drift: 2

drift:
  - path: "truth-layer/projects/PR-001-ai-life-os.yaml"
    type: "modified"
    diff: |
      diff --git a/truth-layer/projects/PR-001-ai-life-os.yaml ...
      -status: active
      +status: completed
  
  - path: "truth-layer/tasks/T-042-new-task.yaml"
    type: "added"
    diff: null  # New file, no previous version
```

**Drift types:**
- **modified** - File changed since last commit (includes full git diff)
- **added** - New file not yet committed (diff: null)
- **deleted** - File removed from working tree (diff: null)

### Integration with Reconciler

Observer generates drift reports → Reconciler consumes them → generates Change Requests:

```bash
# Step 1: Detect drift
python tools/observer.py
# Output: Report: truth-layer/drift/2025-12-02-143000-drift.yaml

# Step 2: Generate CR from drift report (future - Reconciler integration)
python tools/reconciler.py generate truth-layer/drift/2025-12-02-143000-drift.yaml
# Output: CR-20251202-001 created

# Step 3: Review and apply CR
python tools/reconciler.py show CR-20251202-001
python tools/reconciler.py approve CR-20251202-001
python tools/reconciler.py apply --dry-run
python tools/reconciler.py apply
```

### Key Features

✅ **Read-Only** - Never modifies files (safe to run anytime)  
✅ **Git-Based** - Uses standard git diff (reliable, no custom logic)  
✅ **Focused** - truth-layer only (simple, fast)  
✅ **Exit Codes** - 0/1/2 for scripting/automation  
✅ **Windows Compatible** - Text-only output (no Unicode symbols)

### When to Run Observer

- **Before committing** - Check what you changed
- **After manual edits** - Verify no uncommitted drift
- **Before reconciliation** - Generate CRs for drift
- **Daily/weekly** - Manual health check

**Note:** Observer is **manual CLI only** (run when needed). Scheduled automation coming in Slice 2.6b (n8n integration).

### Safety & Performance

**Safety:**
- Read-only operations only
- No entity modifications
- No git commits
- Drift reports are transient (git-ignored)

**Performance:**
- Typical runtime: <1 second for 100 files
- Uses efficient Path.rglob() for file discovery
- Minimal subprocess calls (2 git commands)

### Documentation

- **Design Doc:** `docs/OBSERVER_DESIGN.md` (architecture, workflow, testing)
- **Integration:** Observer → Reconciler workflow documented in RECONCILER_DESIGN.md

### Dependencies

**Standard library only** - no additional Python packages required.

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

**Last Updated:** 2025-12-02  
**Version:** 1.2 (Slice 2.6 - Observer System operational)
