---
type: side_architect_snapshot
schema_version: 1.0
last_updated: 2025-12-01T22:30:00Z
bridge_purpose:
  - onboard_side_architect_assistants_quickly_and_safely
  - explain_current_state_and_priorities_of_ai_life_os
  - remind_assistants_they_never_execute_tools_or_edit_files
current_phase: "Phase 2 – Core Infrastructure"
current_slice:
  id: "2.4b"
  name: "Reconciler Implementation (CR Management)"
  status: "completed"
progress_pct: 30
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

1. **`memory-bank/project-brief.md`** – Vision, TL;DR, Requirements (5 min)
2. **`memory-bank/01-active-context.md`** – Current phase, recent work, next steps (3 min)
3. **`memory-bank/02-progress.md`** – Chronological log (skim as needed)
4. **`docs/ARCHITECTURE_METAPHOR.md`** – Head/Hands/Truth/Nerves model (canonical architecture reference)
5. **`memory-bank/docs/LIFE_GRAPH_SCHEMA.md`** – 6 entities, ADHD metadata (10 min)
6. **`claude-project/system_mapping/migration_plan.md`** – Phases, slices, timeline (5 min)

**Quick Reference:**
- **Playbook:** `claude-project/ai-life-os-claude-project-playbook.md`
- **Research Digest:** `memory-bank/docs/side-architect-research-digest.md` (you are here!)

---

## 3. Recent Slices (Last 3)

**2025-12-01 – Slice 2.4b: Reconciler Implementation (CR Management)**
- CR lifecycle management: generate/list/show/approve/reject
- LOW risk drift types only (git_head_drift, stale_timestamp)
- Zero entity modifications (only CR file management)
- CLI with 5 commands, JSON Schema validation
- Foundation for apply logic (Slice 2.4c)
- Duration: ~1.5 hours

**2025-12-01 – Slice 2.4a: Reconciler Design & CR Format**
- CR architecture: YAML schema, Observer→CR mapping, HITL workflow
- 5 safety invariants (INV-CR-001 to INV-CR-005)
- Design only (no code yet), foundation for implementation in 2.4b
- Duration: ~60 min

**2025-12-01 – Slice 2.3a: Observer (Read-Only Drift Detection)**
- Built drift detection system: 5 drift types (Git, schema, orphans, broken links, stale timestamps)
- Read-only (never modifies files), generates Markdown + JSON reports
- Reuses validator logic (DRY), foundation for Reconciler
- Duration: ~2-3 hours

---

## 4. Current Work by Claude

**Current Slice:** Slice 2.4b (Reconciler CR Management) ✅ COMPLETE

**What Claude just finished:**
- Reconciler CR management system (tools/reconciler.py, 680 lines)
- Drift parsing (Markdown → DriftFinding objects)
- CR generation with auto-ID (CR-YYYYMMDD-NNN)
- List/show/approve/reject workflows (CR file updates only)
- Zero entity modifications (safe slice)
- Tools documentation (README.md)

**Next Options:**
- Reconciler Apply Logic (2.4c) - Entity modifications + git commits (MEDIUM risk)
- Scheduled Observer (2.3b) - n8n automation
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
