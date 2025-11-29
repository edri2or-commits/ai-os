<!--
MAINTENANCE RULE: Update QUICK STATUS after EVERY completed slice
(phase %, recent work, next options change frequently)
-->

---
**QUICK STATUS:** AI Life OS Migration | Phase 1: Cleanup (~30% done) | Just finished: Archive tools/ (Slice 1.2b) | Next: Remove duplicates OR fix drift
---

<!--
PROTOCOL: How to use Memory Bank files in this project

AT START OF ANY NEW CHAT:
1. Read these files:
   - memory-bank/project-brief.md (project overview)
   - memory-bank/01-active-context.md (THIS FILE - where we are now)

2. Summarize for user:
   - What this project is (1-2 sentences from project-brief.md)
   - Which Phase/Slice we are in (from Current Focus below)
   - What changed recently (from Recent Changes below)
   - What you propose as next 1-3 slices (from Next Steps below)

3. THEN start working on requested slice

AT END OF ANY MEANINGFUL SLICE:
1. Update THIS FILE (01-active-context.md):
   - Update "Current Focus" with new Phase/Slice
   - Move completed slice from "Next Steps" to "Recent Changes"
   - Add new candidates to "Next Steps" from migration_plan.md

2. Append to 02-progress.md:
   - Format: "- YYYY-MM-DD – Slice X.Y: Brief description"

3. Keep both files SHORT and SCANNABLE (ADHD-friendly)

GROUNDING:
- This pattern follows Memory Bank research family
- Truth Layer principle: Files are memory, not chat history
- ADHD principle: Quick context load, minimal cognitive overhead
-->

# Current Focus

**Phase:** Phase 1 – Investigation & Foundation Cleanup  
**Status:** ~30% complete (3/10 slices done)  
**Active Work:** Just completed Slice 1.2b (Archive tools/)  

**What we're doing:**
- Cleaning up legacy/unclear components (ai_core/, tools/)
- Removing duplicates (EVENT_TIMELINE, research folders)
- Fixing critical drift (Git HEAD mismatch)
- Establishing clean baseline for Phase 2

**Pattern:**
- Small slices (30-45 min each)
- Archive > delete (safety-first)
- Git-backed reversibility
- Update all mapping docs after each slice

---

# Recent Changes

**2025-11-29 – Slice 1.2b: Archive tools/**
- Moved `tools/` → `archive/one-time/tools/`
- Reason: One-time repo initialization utilities, no active usage
- Components: repo_bootstrap_agent.py, repo_introspection_agent.py, repo_reader_base.py, system_init.py, TOOLS_INVENTORY.md
- Impact: Zero (no imports, no references)
- Commit: 869ad5ce
- Docs updated: INVESTIGATION_RESULTS.md, migration_plan.md, current_vs_target_matrix.md, current_state_map.md

**2025-11-29 – Slice 1.2a: Archive ai_core/**
- Moved `ai_core/` → `archive/legacy/ai_core/`
- Reason: Legacy pre-MCP orchestration layer
- Components: action_executor.py, agent_gateway.py, gpt_orchestrator.py, intent_router.py, ssot_writer.py
- Impact: Demo/test scripts broken (expected, not operational)
- Commit: 0e6614fe
- Docs updated: INVESTIGATION_RESULTS.md, migration_plan.md, current_vs_target_matrix.md, current_state_map.md

**2025-11-29 – Slice 1.1a: Legacy Component Investigation**
- Static analysis of ai_core/, tools/, scripts/, root scripts
- Method: Import analysis, code inspection, git history
- Result: docs/INVESTIGATION_RESULTS.md (comprehensive findings)
- Confidence: High for ai_core/tools/, Medium for scripts/

**2025-11-29 – Phase 0: System Mapping (Complete)**
- Created 4 professional mapping docs:
  - current_state_map.md (90+ elements mapped)
  - target_architecture_summary.md (7 core principles)
  - current_vs_target_matrix.md (action plan per element)
  - migration_plan.md (4 phases, 16 slices)

---

# Next Steps

**Immediate Candidates (from migration_plan.md):**

**Option A: Slice 1.2c – Remove EVENT_TIMELINE duplicate (15-20 min)**
- Action: `git rm EVENT_TIMELINE.jsonl` (root duplicate)
- Keep: `docs/system_state/timeline/EVENT_TIMELINE.jsonl`
- Risk: Very low (verified duplicate)
- Benefit: Quick cleanup win

**Option B: Slice 1.2d – Remove research duplicates (30-45 min)**
- Actions:
  - `git rm -r "claude project/Knowl/"`
  - `git rm -r "claude project/מחסן מחקרים/"`
  - `git rm -r "maby relevant/" "mcp/" "מחקרי ארכיטקטורה/"`
- Risk: Low (duplicates confirmed)
- Benefit: Cleaner repo structure

**Option C: Slice 1.3 – Fix Critical Drift (15-30 min)**
- Problem: Truth Layer reports `last_commit: 43b308a`, actual HEAD is `869ad5ce`
- Action: Run reconciler to update Truth Layer
- Risk: Low (just reconciler execution)
- Benefit: Fix split-brain condition (high value)

**Strategic Note:**
- Consider doing 1.2c + 1.2d back-to-back (finish all cleanup)
- Then 1.3 (drift fix) before Phase 2
- Or jump to Phase 2 if cleanup fatigue

**User Preference:**
- ADHD-aware: prefer momentum + quick wins
- Safety-first: always reversible changes
- Documentation: keep mapping docs updated

---

**Last Updated:** 2025-11-29 (after Slice 1.2b)  
**Next Update:** After next completed slice
