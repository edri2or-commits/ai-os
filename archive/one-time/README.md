# One-Time Utilities Archive

**Purpose:** This directory contains one-time initialization utilities that were used during initial repo setup.

**Status:** ARCHIVED - No longer needed

**Reason:** These were one-time setup scripts that have already served their purpose. The repo structure they were meant to create already exists.

---

## Contents

### archive/one-time/tools/

**Archived:** 2025-11-29 (Slice 1.2b)  
**Reason:** One-time repo initialization utilities, no active usage  
**Superseded by:** Repo structure already exists, no ongoing initialization needed  

**Components:**
- `repo_bootstrap_agent.py` - Creates initial directory structure (core/, system/, agents/, workflows/)
  - Status: One-time setup, already executed
  - Note: Contains typos ("CHECT" instead of "CHECK"), never production-grade
- `repo_introspection_agent.py` - Repo analysis utility
  - Status: One-time analysis tool, no ongoing use
- `repo_reader_base.py` - Base class for repo reading
  - Status: Base class, no external imports found
- `system_init.py` - System initialization
  - Status: One-time initialization, already executed
- `TOOLS_INVENTORY.md` - Tools documentation
  - Status: Archive documentation

**Usage Pattern:**
```
One-time: Setup repo → tools/ scripts run → repo initialized → tools/ no longer needed
```

**Evidence for Archival (from Slice 1.1a investigation):**
- **ZERO** external imports found in entire codebase
- **ZERO** references in docs/ or README.md
- **ZERO** usage in active scripts or services
- Code quality issues (typos) suggest never production-grade
- Directory structure they create already exists

**Confidence:** **HIGH** (95%+) - These are clearly one-time utilities

**Documentation:**
- Investigation: `docs/INVESTIGATION_RESULTS.md` (Slice 1.1a)
- Migration: `claude-project/system_mapping/migration_plan.md` (Slice 1.2b)
- Analysis: `claude-project/system_mapping/current_vs_target_matrix.md`

**Rollback:**
```bash
# If needed (very unlikely):
git mv archive/one-time/tools tools/
# Or:
git revert <commit-hash>
```

---

## Why Archive Instead of Delete?

1. **Git History:** Preserve for historical understanding
2. **Safety:** Easy restoration if assumption was wrong
3. **Learning:** Understand initial repo setup decisions
4. **Documentation:** Context for migration decisions

---

## Maintenance

- **DO NOT** modify files in this directory
- **DO NOT** import from archived utilities
- **DO** refer to this archive for historical context
- **DO** consider removal after confirming stable migration (1-4 weeks)

---

## Comparison: archive/legacy/ vs archive/one-time/

**archive/legacy/** (ai_core/)
- Reason: Superseded by newer architecture (MCP servers)
- Pattern: Old system → New system replaced it

**archive/one-time/** (tools/)
- Reason: One-time initialization, job already done
- Pattern: Setup script → Setup complete → Script no longer needed

Both follow **archive > delete** safety principle.

---

**Last Updated:** 2025-11-29  
**Migration Phase:** Phase 1 (Investigation & Cleanup)  
**Slice:** 1.2b  
**Next Review:** 2025-12-06 (1 week monitoring period)
