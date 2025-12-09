# Observer System Design

**Version:** 0.1.0  
**Status:** Operational  
**Type:** Read-Only Drift Detection CLI

---

## Overview

The Observer System detects drift in truth-layer YAML files by comparing the working tree state to the last git commit. It generates structured drift reports for human review and reconciliation.

**Key Principle:** Observer is **read-only** - it never modifies files, never commits changes, never generates Change Requests. It simply reports what changed.

---

## Architecture

### Components

```
tools/observer.py           # CLI script (Python)
truth-layer/drift/          # Drift reports directory (git-ignored)
truth-layer/drift/.gitignore # Exclude reports from git
```

### Data Flow

```
User runs: python tools/observer.py
    ↓
Observer scans: truth-layer/*.yaml
    ↓
Git diff: Compare working tree to HEAD
    ↓
If drift detected:
    → Generate report: truth-layer/drift/YYYY-MM-DD-HHMMSS-drift.yaml
    → Exit code: 1
Else:
    → Print "No drift"
    → Exit code: 0
```

---

## Usage

### Basic Usage

```bash
# Run drift detection
python tools/observer.py

# Output (if drift detected):
# ✗ Drift detected (2 files)
# Report: truth-layer/drift/2025-12-02-143000-drift.yaml

# Output (if clean):
# ✓ No drift detected (5 files scanned)
```

### Verbose Mode

```bash
# Enable detailed logging
python tools/observer.py --verbose

# Output:
# [Observer] Repository root: C:\Users\edri2\Desktop\AI\ai-os
# [Observer] Found 5 YAML files in truth-layer
# [Observer] Detecting drift...
# [Observer]   MODIFIED: truth-layer/projects/PR-001.yaml
# [Observer]   ADDED: truth-layer/tasks/T-042.yaml
# [Observer] Report generated: truth-layer/drift/2025-12-02-143000-drift.yaml
```

### Exit Codes

- `0` - No drift detected (clean state)
- `1` - Drift detected (report generated)
- `2` - Error (git not available, invalid repo, etc.)

---

## Drift Report Format

**File:** `truth-layer/drift/YYYY-MM-DD-HHMMSS-drift.yaml`

### Example Report

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
      --- a/truth-layer/projects/PR-001-ai-life-os.yaml
      +++ b/truth-layer/projects/PR-001-ai-life-os.yaml
      @@ -5,7 +5,7 @@
      -status: active
      +status: completed
  
  - path: "truth-layer/tasks/T-042-new-task.yaml"
    type: "added"
    diff: null  # New file, no previous version
```

### Drift Types

| Type | Description | Diff Included? |
|------|-------------|----------------|
| `modified` | File changed since last commit | Yes (full git diff) |
| `added` | New file not yet committed | No (null) |
| `deleted` | File removed from working tree | No (null) |

---

## Integration with Reconciler

Observer generates drift reports. Reconciler (Slice 2.4) consumes these reports to generate Change Requests (CRs).

### Workflow

```bash
# Step 1: Detect drift
python tools/observer.py
# Output: Report: truth-layer/drift/2025-12-02-143000-drift.yaml

# Step 2: Generate CR from drift report
python tools/reconciler.py generate truth-layer/drift/2025-12-02-143000-drift.yaml
# Output: CR-20251202-001 created

# Step 3: Review and apply CR
python tools/reconciler.py show CR-20251202-001
python tools/reconciler.py approve CR-20251202-001
python tools/reconciler.py apply --dry-run
python tools/reconciler.py apply
```

---

## Safety Design

### Read-Only Guarantees

1. **No File Modifications:** Observer never writes to truth-layer files
2. **No Git Operations:** Never stages, commits, or pushes changes
3. **No CR Generation:** Never creates Change Requests (that's Reconciler's job)

### Transient Reports

Drift reports are **git-ignored** (via `truth-layer/drift/.gitignore`):
- They are informational only
- Not tracked in git history
- Can be safely deleted after review
- Generated on-demand when needed

### Error Handling

Observer fails gracefully with clear error messages:

```bash
# If git not available:
✗ Observer error: Git repository not found or git not installed

# If not in repo root:
✗ Observer error: Git diff failed: fatal: not a git repository
```

---

## Implementation Details

### Git Integration

Observer uses `git diff HEAD --name-status` to detect changes:
- Efficient: Only reads git index, doesn't traverse entire filesystem
- Accurate: Compares working tree to last commit (HEAD)
- Standard: Uses native git commands, no custom logic

### Path Handling

Observer uses **relative paths from repo root**:
- `truth-layer/projects/PR-001.yaml` (correct)
- NOT `C:\Users\...\truth-layer\...` (absolute paths avoided)

This ensures:
- Cross-platform compatibility (Windows/Linux/macOS)
- Clean drift reports
- Easy integration with Reconciler

### Performance

Observer is optimized for speed:
- Uses `Path.rglob()` for efficient YAML file discovery
- Subprocess calls are minimal (2 git commands total)
- No YAML parsing (unnecessary for drift detection)
- Typical runtime: <1 second for 100 files

---

## Limitations & Future Work

### Current Limitations

1. **Truth-Layer Only:** Only scans `truth-layer/` directory
   - Does NOT scan `docs/`, `governance/`, `claude-project/`
   - This is by design (Slice 2.6 scope)

2. **No Scheduled Runs:** Must be run manually
   - No n8n integration yet (that's Slice 2.3, future work)

3. **No Auto-Reconciliation:** Reports must be processed manually
   - Observer → Reconciler → Apply is a manual workflow

### Future Enhancements (Out of Scope)

- **Slice 2.3 (Proactive Observer):** n8n workflow for scheduled drift detection
- **Phase 3:** Auto-generate CRs for LOW risk drift (HITL approval still required)
- **Expanded Scope:** Detect drift in `docs/` and `governance/` directories

---

## Testing

### Test Scenarios

**Test 1: Clean State (No Drift)**
```bash
# Ensure all changes committed
git status  # Should show "nothing to commit"

# Run Observer
python tools/observer.py

# Expected output:
# ✓ No drift detected (0 files scanned)
# Exit code: 0
```

**Test 2: Modified File (Drift Detected)**
```bash
# Modify a YAML file
echo "test: true" >> truth-layer/projects/PR-001.yaml

# Run Observer
python tools/observer.py

# Expected output:
# ✗ Drift detected (1 files)
# Report: truth-layer/drift/2025-12-02-HHMMSS-drift.yaml
# Exit code: 1

# Clean up
git restore truth-layer/projects/PR-001.yaml
```

**Test 3: New File (Drift Detected)**
```bash
# Create new YAML file
echo "id: test-001" > truth-layer/test.yaml

# Run Observer
python tools/observer.py

# Expected output:
# ✗ Drift detected (1 files)
# Report: truth-layer/drift/2025-12-02-HHMMSS-drift.yaml
# Exit code: 1

# Clean up
rm truth-layer/test.yaml
```

---

## Research Alignment

Observer implements principles from multiple research families:

1. **Safety/Governance (08.md):** Drift detection prevents split-brain states
2. **Memory/Truth Layer (12.md):** Git as Single Source of Truth
3. **Architecture (Head/Hands/Truth):** Observer = "Nerves" (sensory input)
4. **ADHD-aware (18.md):** Simple CLI, clear output, low friction

---

## Changelog

### v0.1.0 (2025-12-02)
- Initial implementation
- CLI with `--verbose` flag
- Git-based drift detection
- YAML report generation
- Exit codes (0/1/2)
- Documentation complete

---

**Last Updated:** 2025-12-02  
**Slice:** 2.6 (Observer System)  
**Status:** ✅ Complete
