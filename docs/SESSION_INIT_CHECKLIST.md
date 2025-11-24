# SESSION_INIT_CHECKLIST.md – Agent Session Initialization (v0)

**Version:** 0.1 (Draft)  
**Created:** 2025-11-24  
**Status:** 🚧 In Design – Not Yet Binding  
**Purpose:** Standardize how all agents start a session in the AI-OS

---

## Overview

This checklist defines the **minimum steps every agent must perform** at the start of a new session (conversation, task, or workflow run).

**Why this matters:**
- Ensures all agents start from the same source of truth
- Prevents drift, stale state, and conflicting assumptions
- Makes handoffs between agents (Claude ↔ GPT) predictable
- Reduces "I don't know where things are" friction

---

## Scope

This checklist applies to:

| Agent | Applies? | Notes |
|-------|----------|-------|
| Claude Desktop | ✅ Yes | Primary executor, local access |
| GPT (Architect) | ✅ Yes | Planner, no MCP yet |
| GPT + MCP (future) | ✅ Yes | When MCP access is established |
| Any future agent | ✅ Yes | Default onboarding path |

---

## Session Init Checklist (v0)

### Phase 1: Confirm Identity & Role

- [ ] **1.1** State which agent you are (e.g., "Claude Desktop", "GPT Architect")
- [ ] **1.2** Confirm your current capabilities and limitations
  - What tools/MCP do you have access to?
  - What can you NOT do in this session?
- [ ] **1.3** Confirm the human owner (Or) is present or has delegated

---

### Phase 2: Sync to Source of Truth

- [ ] **2.1** Confirm the canonical repo:
  - Remote: `https://github.com/edri2or-commits/ai-os`
  - Local (if applicable): `C:\Users\edri2\Desktop\AI\ai-os`
- [ ] **2.2** Check current branch (should be `main` unless told otherwise)
- [ ] **2.3** Check sync status with remote
  - If behind: flag it, ask whether to pull
  - If ahead: flag it, do NOT push without approval
- [ ] **2.4** Note any untracked or uncommitted changes

---

### Phase 3: Load Critical Context

- [ ] **3.1** Read (or confirm awareness of) these core documents:
  - `docs/CONSTITUTION.md` — 9 foundational rules
  - `docs/SYSTEM_SNAPSHOT.md` — current system state
  - `docs/DECISIONS_AI_OS.md` — locked decisions
  - `policies/SECURITY_SECRETS_POLICY.md` — security rules
- [ ] **3.2** Check for any recent changes to the above (git log)
- [ ] **3.3** If a specific task is given, check for relevant:
  - `workflows/` documents
  - `agents/` specs
  - `tools/` inventory

---

### Phase 4: Confirm Session Scope

- [ ] **4.1** What is the goal of this session?
  - Broad (e.g., "route recalculation phase")
  - Specific (e.g., "update SYSTEM_SNAPSHOT.md")
- [ ] **4.2** What is IN scope?
- [ ] **4.3** What is OUT of scope?
- [ ] **4.4** What approvals are needed before execution?

---

### Phase 5: Declare Readiness

- [ ] **5.1** Summarize:
  - "I am [agent], on branch [X], synced to [commit], ready to [task]"
- [ ] **5.2** Flag any blockers or uncertainties
- [ ] **5.3** Wait for human confirmation before proceeding (unless pre-approved)

---

## Example: Claude Desktop Session Start

```
SESSION INIT – Claude Desktop

1. Identity: Claude Desktop (local executor + system analyst)
2. Capabilities: Full MCP (GitHub, Filesystem, Windows, Google read-only)
3. Limitations: Cannot push to remote without approval

4. Repo: C:\Users\edri2\Desktop\AI\ai-os
5. Branch: main
6. Sync: Up to date with origin/main (commit 9ac3e7d)
7. Untracked files: 4 (noted, not touching)

8. Context loaded:
   - CONSTITUTION.md ✓
   - SYSTEM_SNAPSHOT.md ✓
   - DECISIONS_AI_OS.md ✓
   - SECURITY_SECRETS_POLICY.md ✓

9. Session scope: Route recalculation phase
   - IN: mapping, analysis, design proposals
   - OUT: personal life topics, life automations

10. Ready for instructions.
```

---

## Example: GPT Architect Session Start

```
SESSION INIT – GPT Architect

1. Identity: GPT (system architect, planner)
2. Capabilities: Can read docs (via Or), can design, can plan
3. Limitations: NO MCP access, cannot execute, cannot directly read repo

4. Repo: https://github.com/edri2or-commits/ai-os (remote only)
5. Branch: main (as reported by Claude/Or)
6. Sync: Relying on Claude's report

7. Context loaded:
   - Or shared CONSTITUTION.md ✓
   - Or shared SYSTEM_SNAPSHOT.md ✓
   - Other docs as needed via Or

8. Session scope: Route recalculation phase
   - IN: architecture design, policy proposals, spec writing
   - OUT: direct execution, file changes

9. Ready to collaborate via Or.
```

---

## Open Questions (To Be Resolved)

1. **Auto-sync policy:** Should agents auto-pull main at session start, or always ask?
2. **Context caching:** How much context should be re-read vs. assumed from prior sessions?
3. **Handoff protocol:** When Claude hands off to GPT (or vice versa), what must be communicated?
4. **Session logging:** Should session init be logged somewhere (e.g., `logs/session_init.md`)?
5. **Failure mode:** What if an agent cannot complete init (e.g., repo unreachable)?

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2025-11-24 | Claude Desktop | Initial draft created during route recalculation |

---

**Next Steps:**
- [ ] Review with Or and GPT
- [ ] Refine based on feedback
- [ ] Promote to v1.0 when stable
- [ ] Integrate into agent onboarding docs
