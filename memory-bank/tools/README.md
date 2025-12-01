# Memory Bank Tools

Validation and maintenance tools for the Life Graph entities.

## Validator

### What It Does

Validates YAML frontmatter in Markdown files against JSON schemas to ensure:
- Required fields are present
- Field types are correct (string, boolean, enum, etc.)
- Values match allowed options (e.g., `status` must be one of: inbox, next, waiting, scheduled, completed)
- ID formats are correct (e.g., `task-{slug}`, `proj-{YYYY}-{slug}`)

### Why It Matters (ADHD Context)

The validator prevents:
- **Data corruption** from AI hallucinations (wrong field names, invalid values)
- **Broken queries** (if `energy_profile` has a typo, energy-matched task selection fails)
- **Cognitive load** from manually checking every field

### Quick Start

**Validate a single file:**
```bash
python memory-bank/tools/validate_entity.py memory-bank/10_Projects/proj-2025-website.md
```

**Validate multiple files:**
```bash
python memory-bank/tools/validate_entity.py memory-bank/10_Projects/*.md
```

**Validate templates (recommended after editing):**
```bash
python memory-bank/tools/validate_entity.py memory-bank/TEMPLATES/*.md
```

### Output Format

**✅ Success (clear, one-line):**
```
✅ Valid: task → task-example.md
```

**❌ Error (numbered list of issues):**
```
❌ Invalid: task → task-broken.md
   Errors found:
   1. Field 'dopamine_level': 'super-high' is not one of ['high', 'medium', 'low']
   2. Field 'energy_profile': [] is too short (minimum 1 item)
```

### Requirements

**Python 3.7+** with `jsonschema` and `pyyaml`:
```bash
pip install jsonschema pyyaml
```

### Schemas

JSON schemas are in `tools/schemas/`:
- `area.schema.json` - Life domains (Health, Career, etc.)
- `project.schema.json` - Finite goals with deadlines
- `task.schema.json` - Atomic work units
- `context.schema.json` - Constraints (where/how work can be done)
- `identity.schema.json` - Roles/modes (Writer, Developer, Parent)
- `log.schema.json` - Time-stamped notes, observations, journal entries

Each schema enforces:
- Required fields (e.g., `type`, `id`, `title`)
- Field types and formats
- Enum values (e.g., `status`, `energy_profile`)
- ID patterns (e.g., `task-[a-z0-9-]+`)

### Integration Ideas (Not Implemented Yet)

**Pre-commit Hook:**
Automatically validate changed files before git commit:
```bash
# .git/hooks/pre-commit
python memory-bank/tools/validate_entity.py $(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')
```

**n8n Workflow:**
Validate entities before writing to git in automated captures.

**CI/CD:**
Run validator on all entities in GitHub Actions on every push.

---

## Observer

### What It Does

**Read-only drift detection system** that scans the Memory Bank and identifies 5 types of drift without modifying files:

1. **Git HEAD Drift** - `last_commit` in system state doesn't match actual git HEAD
2. **Schema Violations** - Entities with invalid/deprecated fields (reuses validator logic)
3. **Orphaned Entities** - Tasks/Projects without parent references
4. **Broken Links** - References to non-existent entities
5. **Stale Timestamps** - Future dates or >6 months old

### Why It Matters (ADHD Context)

The Observer provides:
- **Early warning system** - catch issues before they cascade
- **Zero activation energy** - automated checks, no manual audits
- **Confidence** - know your Memory Bank is healthy without constant worry
- **Foundation for Reconciler** - drift detection → automated fixes

### Quick Start

**Scan entire Memory Bank:**
```bash
python memory-bank/tools/observer.py
```

**Output:**
- Console report (ADHD-friendly: colorful, concise, actionable)
- Markdown report: `docs/system_state/drift/observer-report-YYYYMMDD-HHMMSS.md`
- JSON report: `docs/system_state/drift/observer-report-YYYYMMDD-HHMMSS.json`

### Output Format

**Console (example):**
```
🔍 Observer Report - 2025-12-01 10:30:00

📊 Summary:
   ✅ No drift detected: Git HEAD, Stale Timestamps
   ⚠️  5 orphaned entities
   ⚠️  2 broken links

📋 Details:

⚠️  Orphaned Entities (5):
   1. task-20251120-005 (no parent_project_id)
      → memory-bank/10_Projects/unknown/tasks/task-20251120-005.md
   ...

⚠️  Broken Links (2):
   1. project-20251201-001 references area-nonexistent-999
      → memory-bank/10_Projects/website-redesign/project.md
   ...

💡 Next Steps:
   - Review orphaned entities: should they be linked or archived?
   - Fix broken links: update or remove invalid references
   - Run Reconciler to generate Change Requests (CRs)
```

### Integration

**Scheduled Runs (Future: Slice 2.3b):**
- n8n workflow or Windows Task Scheduler
- Run every 15-30 minutes
- Alert on new drift detected

**With Reconciler (Future: Slice 2.4e):**
- Observer generates drift reports
- Reconciler reads reports → generates Change Requests (CRs)
- User approves CRs → Reconciler applies fixes

### Requirements

**Python 3.7+** with `jsonschema`, `pyyaml`, `GitPython`:
```bash
pip install -r memory-bank/tools/requirements.txt
```

---

## Reconciler

### What It Does

**Automated drift remediation system** that fixes issues detected by the Observer using a Change Request (CR) workflow:

1. **Observer detects drift** → generates drift report
2. **Reconciler reads report** → generates Change Request (CR) files
3. **User reviews CRs** → approves or rejects with reason
4. **Reconciler applies approved CRs** → updates entities, commits to git

### Why It Matters (ADHD Context)

The Reconciler provides:
- **Proactive system maintenance** - fixes drift automatically (with approval)
- **Safety** - all changes reversible via git, HITL approval for risky operations
- **Audit trail** - every change documented (who, what, when, why)
- **Low friction** - system fixes itself, you just approve/reject

### Status

**Phase 2 - Under Development:**
- ✅ Slice 2.4a: Design & CR format (complete)
- 🔲 Slice 2.4b: Minimal implementation (git HEAD drift + stale timestamps)
- 🔲 Slice 2.4c: CR approval CLI (list, show, approve, reject)
- 🔲 Slice 2.4d: Expand drift coverage (orphaned entities, broken links)
- 🔲 Slice 2.4e: Observer+Reconciler integration (scheduled runs)

### Architecture

See full design: [`docs/RECONCILER_DESIGN.md`](../docs/RECONCILER_DESIGN.md)

**Key Concepts:**

- **Change Request (CR)** - Structured proposal to fix drift
- **HITL Approval** - Human reviews CRs before application
- **Safety Invariants** - All changes git-reversible, risky changes require approval
- **Audit Trail** - Full lifecycle tracking (proposed → approved → applied)

**CR Lifecycle:**
```
Observer (drift detection)
   ↓
Reconciler (generate CR)
   ↓
User (review + approve/reject)
   ↓
Reconciler (apply approved CR + git commit)
```

### Future Quick Start (After Slice 2.4b)

**Generate CRs from drift report:**
```bash
python memory-bank/tools/reconciler.py generate
```

**List pending CRs:**
```bash
python memory-bank/tools/reconciler.py list
```

**Review specific CR:**
```bash
python memory-bank/tools/reconciler.py show CR-20251201-003
```

**Approve CR:**
```bash
python memory-bank/tools/reconciler.py approve CR-20251201-003
```

**Reject CR:**
```bash
python memory-bank/tools/reconciler.py reject CR-20251201-003 --reason "Should archive instead"
```

### Safety Features

- **INV-CR-001:** All entity modifications go through CR system (audit trail)
- **INV-CR-002:** HIGH risk CRs require explicit approval (never auto-applied)
- **INV-CR-003:** Every CR is git-reversible (`git revert` always works)
- **INV-CR-004:** CRs are derived state (not tracked in git, regenerable)
- **INV-CR-005:** CR application is atomic (all-or-nothing, no partial state)

---

## Future Tools (Roadmap)

- **Migration script** - Update existing files to canonical field names
- **Template generator** - Interactive CLI for creating new entities
- **Query helpers** - Common Life Graph queries (e.g., "What can I do now?")

---

**See also:** [`docs/LIFE_GRAPH_SCHEMA.md`](../docs/LIFE_GRAPH_SCHEMA.md) for complete schema documentation.
