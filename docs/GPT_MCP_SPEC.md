# GPT_MCP_SPEC.md – Future GPT + MCP Execution Model (v0)

**Version:** 0.1 (Draft)  
**Created:** 2025-11-24  
**Status:** 🚧 In Design – Not Yet Implemented  
**Purpose:** Define how GPT will gain MCP-based execution capabilities alongside Claude Desktop

---

## Overview

This document specifies the **target architecture** for giving GPT direct MCP access to:
- GitHub (read/write to `ai-os` repo)
- Google Workspace (Drive, Docs, Sheets, Calendar)
- Potentially other services in the future

**Current State:**
- GPT is ARCHITECT ONLY — no direct execution
- All execution goes through Claude Desktop (local) or Or (manual)

**Target State:**
- GPT gains MCP "hands" for specific, well-defined tasks
- Claude Desktop remains the local execution agent
- Clear division of labor between the two

---

## Goals

1. **Enable GPT to directly update SSOT documents** (with approval flow)
2. **Enable GPT to create PRs and branches** on `ai-os`
3. **Enable GPT to read/write Google Docs/Sheets** for system dashboards
4. **Maintain safety** — no uncontrolled execution
5. **Maintain auditability** — all GPT actions are logged and traceable
6. **Preserve human-in-the-loop** for sensitive operations

---

## Proposed Architecture

### High-Level Flow

```
┌─────────────┐      ┌─────────────────┐      ┌─────────────────┐
│     Or      │ ───> │   GPT + MCP     │ ───> │  GitHub / Google│
│   (Human)   │      │   (Architect +  │      │   (Remote)      │
│             │      │    Executor)    │      │                 │
└─────────────┘      └─────────────────┘      └─────────────────┘
       │                                              │
       │              ┌─────────────────┐             │
       └───────────── │ Claude Desktop  │ ◄───────────┘
                      │  (Local Exec)   │
                      └─────────────────┘
```

### Component Responsibilities

| Component | Role | MCP Access | Scope |
|-----------|------|------------|-------|
| **Or (Human)** | Owner, approver, decision-maker | N/A | Everything |
| **GPT + MCP** | Architect + remote executor | GitHub, Google | Docs, PRs, dashboards |
| **Claude Desktop** | Local executor + analyst | Full local MCP | Filesystem, Windows, local Git |

---

## MCP Connections for GPT

### 1. GitHub MCP

**Purpose:** Allow GPT to read and write to `edri2or-commits/ai-os`

**Capabilities:**
- ✅ Read files from any branch
- ✅ Create new branches
- ✅ Create/update files (with commit)
- ✅ Create Pull Requests
- ✅ Read PR comments and reviews
- ⚠️ Merge PRs (requires approval flag)
- ❌ Delete branches (restricted)
- ❌ Force push (restricted)

**Scope Restrictions:**
- ONLY `edri2or-commits/ai-os` repo
- ONLY `docs/`, `agents/`, `workflows/`, `policies/`, `tools/` directories
- NO access to `services/` code without explicit approval
- NO access to `.env`, secrets, or sensitive configs

**Approval Model:**
- Read operations: auto-approved
- Write to `docs/`: auto-approved (logged)
- Write to other dirs: requires Or's approval
- PR creation: auto-approved (PR itself is the review gate)
- PR merge: requires Or's approval

---

### 2. Google Workspace MCP

**Purpose:** Allow GPT to manage system-related Google Docs, Sheets, and Drive files

**Capabilities:**
- ✅ Read Google Docs
- ✅ Read Google Sheets
- ✅ Read Google Drive (list, search)
- ✅ Write/update Google Docs (specific files only)
- ✅ Write/update Google Sheets (specific files only)
- ✅ Read Google Calendar
- ⚠️ Create Calendar events (requires approval)
- ❌ Delete files (restricted)
- ❌ Access to personal/private files (restricted)

**Scope Restrictions:**
- ONLY files/folders explicitly tagged as "AI-OS System"
- ONLY the `edri2or@gmail.com` account
- NO access to personal emails (Gmail read restricted to system-related)
- NO access to files outside designated AI-OS folders

**Approval Model:**
- Read operations: auto-approved
- Write to designated system files: auto-approved (logged)
- Write to other files: requires Or's approval
- File creation: requires Or's approval
- File deletion: BLOCKED (must go through Or manually)

---

## Division of Labor: GPT vs Claude Desktop

### GPT + MCP is BETTER for:

| Task | Why GPT? |
|------|----------|
| Updating SSOT docs (`SYSTEM_SNAPSHOT.md`, etc.) | GPT is the architect; should own doc updates |
| Creating PRs for doc changes | Can do atomic commits without local clone sync |
| Managing Google Sheets dashboards | Direct API access, no local dependency |
| Cross-referencing multiple docs | Can read and synthesize across repo |
| Scheduled/triggered updates | Can run without Or being actively present |
| Structured refactors (move/rename docs) | GitHub API handles this cleanly |

### Claude Desktop is BETTER for:

| Task | Why Claude? |
|------|-------------|
| Local filesystem operations | Only Claude has Windows MCP |
| Running Python scripts | Local Python environment |
| Interactive debugging | Real-time local feedback |
| Reading/writing local-only files (`.env`, etc.) | Not in repo, local access required |
| Desktop automation (UI, apps) | Windows MCP only |
| Quick prototyping | Faster iteration locally |
| Handling path issues (`C:\Users` vs `C:\משתמשים`) | Local context required |

### Shared / Handoff Tasks:

| Task | Primary | Backup | Handoff Trigger |
|------|---------|--------|-----------------|
| Reading repo state | Either | Either | Whoever is in session |
| Proposing architecture changes | GPT | Claude | GPT proposes, Claude can refine |
| Executing approved changes | GPT (remote) | Claude (local) | Depends on change type |
| Verifying changes | Claude | GPT | Local verification preferred |

---

## Safety & Approval Model

### Approval Levels

| Level | Description | Examples |
|-------|-------------|----------|
| **L0: Auto** | No approval needed, logged | Read files, read calendar |
| **L1: Logged** | Auto-approved but logged for audit | Write to `docs/`, create branch |
| **L2: Review** | Requires Or's review before merge | PR merge, write to `agents/` |
| **L3: Explicit** | Requires Or's explicit approval | Delete anything, write to `services/` |
| **L4: Blocked** | Cannot be done via MCP | Force push, delete repo, access secrets |

### Audit Log

All GPT+MCP actions should be logged to:
- GitHub commit messages (for repo changes)
- A dedicated `logs/gpt_mcp_actions.md` or Google Sheet
- With timestamp, action type, target, and result

**Log Entry Format:**
```
[2025-11-24 19:00:00] GPT-MCP | ACTION: update_file | TARGET: docs/SYSTEM_SNAPSHOT.md | RESULT: success | COMMIT: abc1234
```

---

## Implementation Phases

### Phase 0: Current (No MCP)
- GPT is architect only
- All execution via Claude or Or
- ✅ We are here

### Phase 1: GitHub Read-Only
- GPT gets GitHub MCP with READ-ONLY access
- Can read files, branches, PRs
- Cannot write or create
- **Goal:** Validate connection stability

### Phase 2: GitHub Write (Docs Only)
- GPT can write to `docs/` directory
- Can create branches and PRs
- Cannot merge without approval
- **Goal:** Enable SSOT updates

### Phase 3: GitHub Write (Extended)
- GPT can write to `agents/`, `workflows/`, `policies/`, `tools/`
- Still cannot touch `services/` without L3 approval
- **Goal:** Full doc/design management

### Phase 4: Google Workspace
- GPT gets Google MCP
- Can read/write designated system files
- Can manage dashboards and indexes
- **Goal:** Unified system visibility

### Phase 5: Automation Hooks
- GPT can be triggered by external events (webhooks, schedules)
- Can run predefined workflows without Or present
- Strict guardrails on what auto-runs can do
- **Goal:** Reduce manual overhead

---

## Open Questions

1. **Authentication:** How will GPT's MCP auth be managed? (OAuth, PAT, service account?)
2. **Rate Limits:** What are the API limits and how do we handle them?
3. **Rollback:** If GPT makes a bad commit, what's the rollback process?
4. **Conflict Resolution:** If GPT and Claude both try to update the same file, who wins?
5. **Session State:** How does GPT maintain context across sessions without local memory?
6. **Monitoring:** How do we monitor GPT+MCP health and catch failures?
7. **Fallback:** If GPT+MCP is unavailable, how do we gracefully degrade to Claude-only?

---

## Dependencies

Before implementing GPT+MCP, we need:

- [ ] Stable `ai-os` repo structure (System Map complete)
- [ ] Clear folder permissions model
- [ ] Audit logging infrastructure
- [ ] MCP server/client setup for GPT (technical implementation)
- [ ] OAuth or PAT management for GitHub
- [ ] Google service account or OAuth for Google Workspace
- [ ] Testing environment (sandbox branch or test repo)

---

## Related Documents

- `docs/SESSION_INIT_CHECKLIST.md` — Agent session startup
- `docs/CONSTITUTION.md` — Foundational rules (human-in-the-loop)
- `docs/DECISIONS_AI_OS.md` — Locked decisions (DRY RUN policy)
- `policies/SECURITY_SECRETS_POLICY.md` — Secret handling
- `agents/AGENTS_INVENTORY.md` — Agent roles

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2025-11-24 | Claude Desktop | Initial draft created during route recalculation |

---

**Next Steps:**
- [ ] Review with Or and GPT
- [ ] Resolve open questions
- [ ] Define Phase 1 implementation plan
- [ ] Set up test environment
- [ ] Promote to v1.0 when ready for implementation
