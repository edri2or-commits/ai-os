# SESSION_INIT_CHECKLIST.md – Session Initialization

**Version:** 0.4  
**Created:** 2025-11-24  
**Last Updated:** 2025-11-26 (Block ROLE_MODEL_SIMPLIFICATION_V1)  
**Status:** ✅ Operational — Used during Phase 2 sessions  
**Purpose:** Standardize how all AI interfaces start a session in AI-OS

---

## Status Update

- This checklist is **operational but evolving**.  
- It serves as the **session-init protocol** for all interfaces (Claude, GPT, Chat1) in AI-OS.
- The five-phase structure is **recommended**, though some automation details remain in development.

---

## Minimal Operational Rules

- Use `edri2or-commits/ai-os` on branch `main` as the single source of truth (SSOT).
- Confirm your interface identity and available capabilities at session start.
- Verify repo sync state (if applicable) before planning or editing.
- Load core docs: **CONSTITUTION**, **SYSTEM_SNAPSHOT**, **AGENT_SYNC_OVERVIEW**, **CONTROL_PLANE_SPEC**.
- Do **not execute** changes without explicit approval from Or (unless pre-approved).

---

## Overview

This checklist defines the **minimum steps every interface should perform** at the start of a new session.

**Why this matters:**
- Ensures consistent starting point across all interfaces
- Prevents drift, stale state, and conflicting assumptions
- Provides clear context for the current session
- Maintains safety and transparency

---

## Scope

This checklist applies to **all AI interfaces**:

| Interface | Access Type | Notes |
|-----------|-------------|-------|
| Claude Desktop | Local MCP + Repo | Full filesystem and tool access |
| GPT (ChatGPT) | Custom Actions + Drive | Google Workspace, GitHub Actions (DRY RUN) |
| Chat1 Telegram | Bot + Gateway | Natural language interface, approval-based |
| Future interfaces | TBD | Same protocol applies |

**No role hierarchy.** Each interface uses what's available to it. Planning and execution happen based on capabilities, not fixed roles.

---

## Session Init Protocol

### Phase 1: Identify Interface & Capabilities

- [ ] **1.1** State which interface you are (e.g., "Claude Desktop", "GPT via ChatGPT")
- [ ] **1.2** Confirm your current capabilities:
  - What tools/MCP/APIs do you have access to?
  - What **can** you do in this session?
  - What **cannot** you do in this session?
- [ ] **1.3** Confirm Or is present or has delegated authority

---

### Phase 2: Sync to Source of Truth

**If you have repo access:**
- [ ] **2.1** Confirm the canonical repo:
  - Remote: `https://github.com/edri2or-commits/ai-os`
  - Local: `C:\\Users\\edri2\\Work\\AI-Projects\\ai-os-claude-workspace`
- [ ] **2.2** Check current branch (should be `main`)
- [ ] **2.3** Check sync status with remote
  - If behind: flag it, ask whether to pull
  - If ahead: flag it, do NOT push without approval
- [ ] **2.4** Note any untracked or uncommitted changes

**If you don't have repo access:**
- [ ] **2.1** Confirm you're working with the latest available context (Drive Snapshot, shared docs, etc.)
- [ ] **2.2** Flag if state seems stale and request refresh if needed

---

### Phase 3: Load State Layer

**Quick Sync (Recommended):**
1. **Read `AGENT_SYNC_OVERVIEW.md`** — Phase, Mode, recent work
2. **Check `SESSION_NOTE.md`** — Current session intent (if defined)
3. **Skim `INFRA_MAP.md`** — Infrastructure status (if relevant)

**Core Documents (if needed):**
- [ ] `docs/CONSTITUTION.md` — 9 foundational principles
- [ ] `docs/CONTROL_PLANE_SPEC.md` — Phase, Mode, constraints
- [ ] `docs/SYSTEM_SNAPSHOT.md` — Full system state
- [ ] `docs/system_state/AGENT_CAPABILITY_PROFILE.md` — Interface capabilities

**Additional Context (if task-specific):**
- `docs/DECISIONS_AI_OS.md` — Locked decisions
- `docs/system_state/registries/SERVICES_STATUS.json` — Service status
- `docs/system_state/timeline/EVENT_TIMELINE.jsonl` — Recent events

---

### Phase 4: Confirm Session Scope

- [ ] **4.1** What is the goal of this session?
  - Broad goal (e.g., "Phase 2 infrastructure work")
  - Specific task (e.g., "simplify role model")
- [ ] **4.2** What is IN scope for this session?
- [ ] **4.3** What is OUT of scope?
- [ ] **4.4** What approvals are needed before execution?
- [ ] **4.5** Are there any safety constraints? (INFRA_ONLY, no remote push, etc.)

---

### Phase 5: Declare Readiness & Propose Next Steps

- [ ] **5.1** Summarize your understanding:
  - "I am [interface], with access to [capabilities]"
  - "Current Phase/Mode: [X]"
  - "Session goal: [Y]"
  - "Ready to [action]"
- [ ] **5.2** Propose 1-3 concrete Blocks/tasks you can help with
- [ ] **5.3** Flag any blockers or uncertainties
- [ ] **5.4** Wait for confirmation before proceeding (unless pre-approved)

---

## Drive Snapshot Awareness

For interfaces **without direct repo access** (like GPT Planning via ChatGPT):

- **`SYSTEM_SNAPSHOT_DRIVE`** is available as a Google Doc: [link](https://docs.google.com/document/d/1-ysIo2isMJpHjlYXsUgIBdkL4y21QPb-)
- This is a **view** of the repo state, not the source of truth
- Request a refresh if data seems stale
- When in doubt, ask Or to verify against repo

For interfaces **with repo access** (like Claude Desktop):
- Always read from `docs/SYSTEM_SNAPSHOT.md` in the repo
- Update Drive Snapshot only on explicit request from Or

---

## Batch Approved Session Mode

When Or explicitly approves a full session scope, the interface may proceed through all steps without re-asking for intermediate confirmations.

**Must still pause for:**
- Repository structural changes
- External connections
- System policy modifications

**At session end:**
- Summarize all performed actions
- Update State Layer (EVENT_TIMELINE, relevant docs)
- Wait for approval before any push or deployment

---

## Example Session Inits

### Claude Desktop

```
SESSION INIT – Claude Desktop

1. Interface: Claude Desktop
2. Capabilities: Full MCP (GitHub, Filesystem, Windows, Google read-only, Canva, Browser)
3. Limitations: No push without approval, no autonomous deployment

4. Repo: C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace
5. Branch: main
6. Sync: Up to date with origin/main

7. State loaded:
   - AGENT_SYNC_OVERVIEW.md ✓
   - SESSION_NOTE.md ✓ (goal: simplify role model)
   - CONTROL_PLANE_SPEC.md ✓ (Phase 2, INFRA_ONLY)

8. Session scope: Remove rigid role hierarchy, update docs
   - IN: AGENT_CAPABILITY_PROFILE, SESSION_INIT_CHECKLIST, State Layer
   - OUT: n8n, Docker, production deployments

9. Proposed blocks: Update AGENT_CAPABILITY_PROFILE (1), Update SESSION_INIT_CHECKLIST (2), Sync State Layer (3)

10. Ready for approval.
```

### GPT (ChatGPT)

```
SESSION INIT – GPT

1. Interface: GPT (ChatGPT with Custom Actions)
2. Capabilities: Google Workspace access, GitHub Actions (DRY RUN), Drive Snapshot access
3. Limitations: No MCP, no direct repo access, depends on ngrok tunnel

4. State: Using SYSTEM_SNAPSHOT_DRIVE (last refresh: 2025-11-25)
5. Context: Or shared AGENT_SYNC_OVERVIEW.md, SESSION_NOTE.md

6. Session scope: Collaborate on architecture design
   - IN: High-level planning, Spec writing, Analysis
   - OUT: Direct file execution

7. Ready to collaborate.
```

---

## Safety Constraints (Apply to All)

These constraints apply **regardless of interface**:

1. **No push without approval** — Never push to remote without Or's explicit approval
2. **INFRA_ONLY respect** — In Phase 2, no live automations on Or's life
3. **Human-Approved Writes** — All writes logged in EVENT_TIMELINE with clear commit messages
4. **No CONSTITUTION changes** — Only with Or's explicit approval
5. **Transparency** — Every change visible, explainable, logged

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 0.1 | 2025-11-24 | Claude Desktop | Initial draft |
| 0.2 | 2025-11-25 | Claude Desktop | Added Drive Snapshot Awareness |
| 0.3 | 2025-11-26 | Claude Desktop | Added Quick Sync via State Layer |
| 0.4 | 2025-11-26 | Claude Desktop | Simplified: removed role hierarchy, unified protocol for all interfaces |

**Note:** Operational protocol for all AI-OS interfaces.
