---
type: side_architect_snapshot
schema_version: 1.0
last_updated: 2025-12-06T16:30:00Z
bridge_purpose:
  - onboard_side_architect_assistants_quickly_and_safely
  - explain_current_state_and_priorities_of_ai_life_os
  - remind_assistants_they_never_execute_tools_or_edit_files
current_phase: "Phase 2 – Architectural Alignment & Governance"
current_slice:
  id: "Documentation Consolidation"
  name: "Single Source of Truth (TOOLS_INVENTORY + WRITE_LOCATIONS + AI_LIFE_OS_STORY)"
  status: "completed"
progress_pct: 78
---

# Side Architect Bridge – System Snapshot

**Purpose:** Quick state overview for side architect assistant  
**Update Frequency:** After major slices or milestones  
**Read Time:** ~2 minutes

---

## 0. Purpose & Context

### Why This AI Life OS Exists

**For the user (Or):**
- 🧠 **ADHD + External Brain** – Working memory deficits and object permanence issues mean "if it's not visible, it doesn't exist." The Life Graph externalizes state so nothing gets forgotten.
- 🎯 **Reduce Cognitive Load** – Decision fatigue is real with ADHD. The system handles orchestration, validation, and drift detection automatically.
- ♻️ **Git as Infinite Undo** – ADHD brains hate irreversible mistakes. Git provides a safety net where every change is reversible.
- 📊 **Life Graph > "Everything in My Head"** – Externalized state (Projects, Tasks, Contexts, Identity) replaces mental juggling and prevents burnout.
- 🧠 Use Claude Desktop as the Head (reasoning, orchestration), external side-architect assistants (thinking partners), and automation layers (Hands: n8n) without losing control or creating split-brain scenarios.

### Why This Bridge Exists & Who "You" Are

**Two Layers:**
1. **Claude Desktop (Head)** – Has tools (MCP servers, filesystem, git), executes changes, validates, commits. This is the "executor."
2. **External Side-Architect Assistants (You)** – Thinking partners with NO tools. You read, think, propose specs, but never execute.

**Why the Bridge Exists:**
- ⚡ **Fast Onboarding** – 2-minute context load (bridge) vs 30+ minutes (re-reading research)
- 🔁 **Less Re-Explaining** – User doesn't repeat history every chat
- 🧭 **Alignment** – Keep assistants aligned with research, invariants, and ADHD constraints

**Who "You" Are (Side Architect):**
- 🧠 Help user think through architecture and design questions
- 📝 Write prompts and specs for Head (Claude Desktop) to execute
- 🔍 Research mode when Head needs external context
- ❌ **Never execute tools, modify files, or run git commands**

**Collaboration Flow:**
```
Side Architect (think/propose) → User (review/approve) → Head (Claude Desktop executes)
```

---

## 1. State Overview (Quick Scan)

**Core Invariants:**
- INV-001: Git repo as single Truth Layer (no state fragmentation)
- INV-002: All state changes via Nerves (MCP) or documented bridges
- INV-003: Heads are replaceable (Claude, ChatGPT, Gemini)
- INV-004: Nerves are stateless (MCP servers)
- INV-005: Heads are reactive, n8n (Hands) autonomous
- INV-006: Git as infinite undo

**Active Life Graph Entities:** 6/6 complete ✅
- **Structural:** Area, Context, Identity
- **State-based:** Project, Task, Log

**Technical Debt:**
- **TD-001:** Git MCP not configured → manual PowerShell bridge (documented workaround)

---

## 2. Files to Trust First (Truth Layer)

**Read in this order:**

1. **`memory-bank/AI_LIFE_OS_STORY.md`** – Single canonical narrative (30s → 30min layers) ⭐ START HERE
2. **`memory-bank/01-active-context.md`** – Current phase, recent work, next steps (ground truth)
3. **`memory-bank/TOOLS_INVENTORY.md`** – Complete list of MCP servers, APIs, services, tools, capabilities
4. **`memory-bank/WRITE_LOCATIONS.md`** – Protocol 1 guidance (where to update what)
5. **`memory-bank/02-progress.md`** – Chronological log (skim as needed)
6. **`memory-bank/docs/ARCHITECTURE_REFERENCE.md`** – Hexagonal + MAPE-K (canonical architecture)
7. **`memory-bank/docs/CANONICAL_TERMINOLOGY.md`** – Official terms (MANDATORY - no deprecated terms)
8. **`memory-bank/docs/LIFE_GRAPH_SCHEMA.md`** – 6 entities, ADHD metadata (10 min)

**Quick Reference:**
- **Playbook:** `claude-project/ai-life-os-claude-project-playbook.md`
- **Research Digest:** `memory-bank/docs/side-architect-research-digest.md` (you are here!)
- **Entry Point:** `memory-bank/START_HERE.md` (navigation hub)

---

## 3. Recent Slices (Last 4)

**2025-12-06 – Documentation Consolidation: Single Source of Truth**
- **Created:** TOOLS_INVENTORY.md (436 lines) - Complete capability map
- **Created:** WRITE_LOCATIONS.md (445 lines) - Protocol 1 guidance
- **Created:** AI_LIFE_OS_STORY.md (640 lines) - Canonical narrative (30s → 30min)
- **Deleted:** Manifesto v1, project-brief, SYSTEM_BOOK (superseded)
- **Updated:** START_HERE.md (complete rewrite, fixed broken links)
- **Impact:** Zero duplicates, zero contradictions, 5-min onboarding (was 90 min)

**2025-12-06 – Slice H3: Telegram Approval Bot (TESTED & OPERATIONAL)**
- Async HITL via Telegram (@SALAMTAKBOT)
- File-based workflow: CR → Telegram → Approval → Database
- End-to-end verified: CR detected (5s), user approved, DB updated
- Status: PRODUCTION READY (ready for H4 VPS deployment)

**2025-12-05 – Judge Agent V2 + Langfuse V3 Integration**
- Langfuse V3 deployed (6 services: web, worker, postgres, clickhouse, redis, minio)
- Judge V2 reads traces from Langfuse instead of JSONL
- Visual debugging at http://localhost:3000
- Foundation for self-learning loop complete

**2025-12-02 – Slice 2.6: Observer System (CLI drift detection)**
- Python script: `tools/observer.py` (320 lines) with CLI interface
- Git-based drift detection: compare working tree to HEAD for truth-layer YAML files
- Generates structured drift reports in `truth-layer/drift/*.yaml` (git-ignored)
- Exit codes: 0 (clean), 1 (drift detected), 2 (error)
- Read-only operations, foundation for Observer→Reconciler integration
- Documentation: `docs/OBSERVER_DESIGN.md` (300 lines)
- Duration: ~2 hours

**2025-12-01 – Slice 2.4c: Reconciler Apply Logic**
- Apply command with 5 Git Safety Rules (targeted staging, working tree check, one commit per CR)
- `--dry-run` and `--limit` flags for safe execution
- Apply log tracking (timestamp | cr_id | status | commit_hash | files)
- Atomic operations with rollback on failure
- HITL protocol: Plan → Approve → Execute → Report
- Duration: ~3 hours (includes TD-002 resolution)

**2025-12-01 – Slice 2.4b: Reconciler Implementation (CR Management)**
- CR lifecycle management: generate/list/show/approve/reject
- LOW risk drift types only (git_head_drift, stale_timestamp)
- Zero entity modifications (only CR file management)
- CLI with 5 commands, JSON Schema validation
- Foundation for apply logic (Slice 2.4c)
- Duration: ~1.5 hours

**2025-12-01 – Slice 2.3a: Observer (Read-Only Drift Detection)**
- Built drift detection system: 5 drift types (Git, schema, orphans, broken links, stale timestamps)
- Read-only (never modifies files), generates Markdown + JSON reports
- Reuses validator logic (DRY), foundation for Reconciler
- Duration: ~2-3 hours

---

## 4. Current Work by Claude

**Current Slice:** Slice 2.6 (Observer System) ✅ COMPLETE

**What Claude just finished:**
- Observer CLI tool (tools/observer.py, 320 lines)
- Git-based drift detection for truth-layer YAML files
- Structured drift reports in `truth-layer/drift/*.yaml` (git-ignored)
- Exit codes: 0 (clean), 1 (drift), 2 (error)
- Read-only operations, foundation for Observer→Reconciler workflow
- Documentation (docs/OBSERVER_DESIGN.md, 300 lines)

**What's Operational Now:**
- ✅ Desktop Commander MCP (subprocess management, file ops, surgical editing)
- ✅ Observer CLI (drift detection, report generation)
- ✅ Validator (pre-commit hook, JSON Schema validation)
- ✅ Reconciler (CR management + apply logic with Git Safety Rules)
- ✅ Life Graph schema (6/6 entities complete)
- ✅ Narrative Layer (Manifesto + ADRs + Design Guide)

**Next Options:**
- Field Standardization (2.2b) - Clean up inconsistent field names in Life Graph
- Scheduled Observer (2.6b) - n8n automation for continuous drift detection
- Documentation Polish - Improve examples, add diagrams
- Side-Architect Refinement Track (SA-1...SA-5) - Improve side architect experience

---

## 5. Notes for Side Architect Assistant

**ADHD/Ergonomic Constraints:**
- Keep responses short, scannable (bullets > paragraphs)
- Avoid overwhelming options (2-3 max)
- Use visual markers (✅ ❌ ⚠️ 🔴)
- Low activation energy (Claude executes, user approves)
- Git rollback always available (safety net)

**Current Priorities (Phase 2 - 25% complete):**
1. ✅ Life Graph infrastructure (6/6 entities complete)
2. ✅ Validator + git hooks (automatic validation)
3. ✅ Observer (drift detection - read-only)
4. 🟡 Reconciler (auto-fix drift - next candidate)
5. 🟡 Circuit Breakers (safety layer)

**Tools Available:**
- **Validator:** `python tools/validate_entity.py <file|dir>`
- **Observer:** `python tools/observer.py` (manual run)
- **Reconciler:** `python tools/reconciler.py generate|list|show|approve|reject`
- **Git pre-commit hook:** Automatic validation on commit

**What Side Architects Do:**
- 🧠 Think through architecture and design questions
- 📝 Provide spec feedback and identify gaps
- 🔍 Research mode (when kernel needs external context)
- 🎯 Strategic guidance (phases, priorities, tradeoffs)

**What Side Architects Don't Do:**
- ❌ Execute changes (no file modifications, no git commits)
- ❌ Direct MCP/tool access (Head/Claude Desktop handles implementation)
- ❌ Approve slices (only user approves via HITL)

**Collaboration Pattern:**
- Side architect proposes → User reviews → Head (Claude Desktop) executes
- Side architect has full read access to Memory Bank + research corpus
- Use bridge + digest for quick context load (~10 min total)

**How to Revisit Past Work:**

When you need context about previous slices or decisions:

1. **Don't reconstruct from chat memory** – Chat history is unreliable and incomplete
2. **Ask the user to help you find it:**
   - Open `memory-bank/02-progress.md` (chronological log of all slices)
   - Search for a keyword (e.g., "Observer", "Reconciler", "validator", "bridge")
   - Paste the relevant slice entry into the chat
3. **For higher-level planning questions:**
   - Ask for the relevant section of `claude-project/system_mapping/migration_plan.md`
   - This has the 4-phase roadmap and strategic context

**Why this matters:** Side-architect assistants have no persistent memory. Asking the user to provide excerpts is faster and more accurate than trying to reconstruct history from conversation.

**Unusual Risks:****
- Context window overflow (mitigated by AP-001: surgical edits)
- Git MCP missing (workaround: manual PowerShell bridge, TD-001)
- TD-001 investigation: `@modelcontextprotocol/server-git` doesn't exist (404)

---

**Last Updated:** 2025-12-01T20:45:00Z  
**Next Update:** After next major slice (Reconciler 2.4 or scheduled Observer 2.3b)
