# Observer System Design

**Version:** 1.0  
**Status:** Operational  
**Last Updated:** 2025-12-02

---

## Overview

The Observer System is a **read-only drift detection tool** that monitors uncommitted changes in the Truth Layer (YAML files). It compares the current working tree state to the last git commit (HEAD) and generates structured drift reports.

**Purpose:** Enable proactive drift detection before changes accumulate and become difficult to track.

**Scope:** Phase 2 - Core Infrastructure (Slice 2.6)

---

## Architecture

### Components

1. **Observer CLI** (`tools/observer.py`)
   - Python script (~290 lines)
   - Git integration for diff detection
   - YAML report generation
   
2. **Drift Reports Directory** (`truth-layer/drift/`)
   - Stores timestamped drift reports
   - Git-ignored (transient state)
   
3. **Observer Design Doc** (`docs/OBSERVER_DESIGN.md`)
   - This file
   - Architecture and usage documentation

### Data Flow

```
┌─────────────────┐
│  User runs CLI  │
└────────┬────────┘
         │
         v
┌─────────────────────────────────┐
│ Observer.detect_drift()         │
│ - Run: git diff HEAD --name...  │
│ - Parse changed files           │
│ - Get diffs for modified files  │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Observer.generate_report()      │
│ - Create drift/YYYY-MM-DD...    │
│ - Write YAML report             │
└────────┬────────────────────────┘
         │
         v
┌─────────────────┐
│ Report to user  │
│ Exit code: 0/1  │
└─────────────────┘
```

---

## Usage

### Basic Usage

```bash
# Check for drift
python tools/observer.py

# Output (no drift):
✅ No drift detected. Truth layer is clean.

# Output (drift found):
⚠️  Drift detected in 3 file(s).
📄 Report generated: truth-layer/drift/2025-12-02-143000-drift.yaml

Files with drift:
  - truth-layer/projects/PR-001-ai-life-os.yaml (modified)
  - truth-layer/tasks/T-042-new-task.yaml (added)
  - truth-layer/contexts/CTX-003-old.yaml (deleted)
```

### Verbose Mode

```bash
# Enable detailed logging
python tools/observer.py --verbose

# Output:
[Observer] Starting drift detection...
[Observer] Running git diff to detect changes...
[Observer] Found 2 changed files
[Observer] Processing truth-layer/projects/PR-001.yaml (type: modified)
[Observer] Generating report: truth-layer/drift/2025-12-02-143000-drift.yaml
...
```

### Exit Codes

- **0:** No drift detected (clean working tree)
- **1:** Drift detected (report generated)
- **2:** Error (not in git repo, invalid YAML, etc.)

---

## Drift Report Format

### Structure

```yaml
metadata:
  detected_at: "2025-12-02T14:30:00Z"
  observer_version: "0.1.0"
  files_scanned: 12
  files_with_drift: 3

drift:
  - path: "truth-layer/projects/PR-001-ai-life-os.yaml"
    type: "modified"
    diff: |
      --- a/truth-layer/projects/PR-001-ai-life-os.yaml
      +++ b/truth-layer/projects/PR-001-ai-life-os.yaml
      @@ -5,7 +5,7 @@
      -status: active
      +status: completed
  
  - path: "truth-layer/tasks/T-042-new-task.yaml"
    type: "added"
    diff: null  # New file, no previous version
  
  - path: "truth-layer/contexts/CTX-003-old-context.yaml"
    type: "deleted"
    diff: null  # File deleted
```

### Fields

**Metadata:**
- `detected_at`: UTC timestamp (ISO 8601 format)
- `observer_version`: Observer script version
- `files_scanned`: Total YAML files in truth-layer
- `files_with_drift`: Number of changed files

**Drift Array:**
- `path`: Relative path to changed file
- `type`: Change type (added/modified/deleted/renamed)
- `diff`: Git diff output (null for added/deleted files)

---

## Integration with Reconciler

The Observer generates drift reports that can be consumed by the Reconciler:

### Workflow

```bash
# 1. Detect drift
python tools/observer.py
# Output: Report generated: truth-layer/drift/2025-12-02-143000-drift.yaml

# 2. Generate Change Request (CR)
python tools/reconciler.py generate truth-layer/drift/2025-12-02-143000-drift.yaml
# Output: CR-20251202-001 created

# 3. Review CR
python tools/reconciler.py show CR-20251202-001

# 4. Approve CR
python tools/reconciler.py approve CR-20251202-001

# 5. Preview apply
python tools/reconciler.py apply --dry-run

# 6. Execute apply
python tools/reconciler.py apply
```

---

## Safety & Constraints

### Safety Features

✅ **Read-Only Operations**
- Observer NEVER modifies files
- Only uses git read commands (diff, rev-parse)
- Zero risk of data loss

✅ **Transient Reports**
- Drift reports stored in git-ignored directory
- Not committed to repository
- Can be safely deleted at any time

✅ **Error Handling**
- Graceful failure if not in git repo
- Clear error messages for debugging
- Exit codes indicate success/failure

### Constraints

❌ **Does NOT:**
- Modify Truth Layer files
- Auto-generate Change Requests (that's Reconciler's job)
- Commit changes to git
- Require network access
- Depend on external services

✅ **DOES:**
- Detect uncommitted changes
- Generate structured reports
- Provide clear exit codes
- Support verbose logging

---

## Future Enhancements (Post-Phase 2)

### Slice 2.3: Scheduled Observer (n8n Integration)

**Goal:** Automated drift detection every 15 minutes

**Architecture:**
```
┌─────────────┐
│ n8n Workflow │ (cron: */15 * * * *)
│ - Schedule   │
└──────┬───────┘
       │
       v
┌──────────────────────────────┐
│ Execute: python observer.py  │
│ - Capture exit code          │
│ - Parse output               │
└──────┬───────────────────────┘
       │
       v
┌──────────────────────────────┐
│ If drift detected (exit=1):  │
│ - Send notification          │
│ - (Optional) Auto-generate CR│
└──────────────────────────────┘
```

**Benefits:**
- Proactive drift alerts
- No manual checking required
- Continuous monitoring

**Risks:**
- n8n configuration complexity
- Notification fatigue if too frequent
- Resource usage (lightweight, minimal)

**Status:** Future work (Phase 2, Slice 2.3)

---

## Research Alignment

**Family:** Safety/Governance (08.md), Memory/RAG (12.md)

**Principles:**
1. **Git as SSOT:** Observer respects git as Single Source of Truth
2. **Read-Only Safety:** No destructive operations
3. **Drift Detection:** Core to split-brain prevention
4. **HITL Protocol:** Human reviews drift, not automatic remediation

**Invariants:**
- INV-001 (Git as Core): Observer queries git exclusively
- INV-CR-001 (Read-Only Observer): Observer never modifies entities
- Architecture: Observer = "Nerves" (sensory input)

---

## Troubleshooting

### Issue: "Not in a git repository"

**Symptom:**
```
❌ Error: Not in a git repository
```

**Cause:** Script not run from within git repo

**Fix:**
```bash
cd C:\Users\edri2\Desktop\AI\ai-os
python tools/observer.py
```

---

### Issue: No drift reports generated

**Symptom:** Exit code 1 but no file created

**Cause:** Permission error writing to `truth-layer/drift/`

**Fix:**
```bash
# Check directory exists and is writable
ls -la truth-layer/drift/

# Create if missing
mkdir -p truth-layer/drift
```

---

### Issue: "Git diff failed"

**Symptom:**
```
❌ Error: Git diff failed: <stderr message>
```

**Cause:** Git command error (invalid ref, corrupt repo)

**Fix:**
```bash
# Verify git status
git status

# Check HEAD is valid
git rev-parse HEAD

# Repair if needed
git fsck
```

---

## Changelog

### v0.1.0 (2025-12-02)

**Initial Release:**
- CLI with --verbose flag
- Git-based drift detection (diff HEAD)
- YAML report generation
- Exit codes (0/1/2)
- Support for added/modified/deleted/renamed files
- Diff content for modified files
- Read-only, safe operations

---

**Document Status:** Complete  
**Next:** Slice 2.3 (Scheduled Observer with n8n integration)
