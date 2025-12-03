# Git Hooks - Auto-Sync Infrastructure

## Pre-commit Hook: SYSTEM_BOOK.md Auto-Sync

**Purpose:** Automatically sync SYSTEM_BOOK.md from 01-active-context.md before every commit.

**Result:** Zero drift, zero maintenance. SYSTEM_BOOK.md is ALWAYS up-to-date.

---

## Installation (Windows)

### One-time Setup

```powershell
# From repo root
cd C:\Users\edri2\Desktop\AI\ai-os

# Copy hook to .git/hooks/
copy tools\hooks\pre-commit .git\hooks\pre-commit
```

### Verification

```bash
# Make any commit
git commit -m "test: Check pre-commit hook"

# Expected output:
# [Pre-commit] Syncing SYSTEM_BOOK.md...
# [INFO] Extracted from 01-active-context.md: ...
# [SUCCESS] SYSTEM_BOOK.md updated ...
# [Pre-commit] SYSTEM_BOOK.md synced and staged ✓
```

---

## How It Works

### Trigger
Every `git commit` command runs `.git/hooks/pre-commit` automatically.

### Execution Flow

1. **Navigate:** `cd $(git rev-parse --show-toplevel)` (find repo root)
2. **Sync:** `python tools/sync_system_book.py` (update SYSTEM_BOOK.md)
3. **Stage:** `git add SYSTEM_BOOK.md` (include in current commit)
4. **Commit:** Proceeds normally with updated SYSTEM_BOOK.md

### Error Handling

If `sync_system_book.py` fails:
- Hook exits with code 1 (blocks commit)
- Shows error message
- Suggests: Fix error OR `git commit --no-verify` to skip

---

## Research Support

**Version Control Integration (xcubelabs.com, June 27, 2024):**
> "Utilise version control systems such as Git to track changes made to documentation over time"

**CI/CD Automation (github.com/resources, October 15, 2025):**
> "GitHub Actions, a CI/CD platform that automates the build, test, and deployment pipelines"

**Documentation as Code (devops.com, January 5, 2024):**
> "CI/CD pipeline can automatically build and deploy the updated documentation"

**Industry Practice:**
- GitHub: Docs as Code + Actions
- Vercel: Dynamic llms.txt generation
- Anthropic: Auto-generated docs via Mintlify

---

## Maintenance

### Update Hook
If `tools/sync_system_book.py` changes:
```bash
# Re-copy hook (no changes needed to hook itself)
copy tools\hooks\pre-commit .git\hooks\pre-commit
```

### Disable Hook (temporary)
```bash
# Skip for one commit
git commit --no-verify -m "..."

# Remove hook entirely
rm .git\hooks\pre-commit
```

### Re-enable Hook
```bash
copy tools\hooks\pre-commit .git\hooks\pre-commit
```

---

## Files

- `tools/hooks/pre-commit` - Source of truth (version controlled)
- `.git/hooks/pre-commit` - Active hook (local, not in Git)
- `tools/sync_system_book.py` - Sync logic (called by hook)

---

## Benefits

**Zero Drift:**
- SYSTEM_BOOK.md CANNOT be out of sync
- Every commit includes latest state

**Zero Maintenance:**
- No manual "remember to sync" step
- Automation runs invisibly

**Professional:**
- Industry standard (Git hooks + CI/CD)
- Research-backed design

**Safety:**
- Hook blocks commit if sync fails
- `--no-verify` escape hatch available

---

**Created:** 2025-12-04  
**Research:** xcubelabs (2024), GitHub (2025), DevOps.com (2024)
