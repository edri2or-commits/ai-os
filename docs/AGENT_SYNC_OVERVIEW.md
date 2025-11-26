# AGENT_SYNC_OVERVIEW.md — סיכום מצב לסוכנים

**Purpose:** קובץ סינכרון מהיר לכל ממשק AI-OS בתחילת סשן.  
**Version:** 0.4  
**Last Updated:** 2025-11-26 (STATE_LAYER_BASELINE_V1 declared)

---

## 1. PHASE & MODE

| Property | Value |
|----------|-------|
| **Phase** | Phase 2 — Stabilizing the Hands |
| **Mode** | INFRA_ONLY |
| **Automations Enabled** | false |
| **Sandbox Only** | true |
| **Source** | `docs/CONTROL_PLANE_SPEC.md` (v0.3, 2025-11-25) |

**What this means:**
- Focus on infrastructure stability, not new features
- All automation is paused/disabled
- Direct writes allowed only with logging
- Human approval required for significant changes

---

## 2. CORE STATE SNAPSHOT

מצב המערכת נכון ל-2025-11-26:

- ✅ **GitHub integration operational** — Full R/W via MCP + GPT Actions
- ✅ **Google Workspace connected** — Gmail, Calendar, Drive, Docs working
- ✅ **Claude Desktop available** — Local access with full MCP
- ✅ **GPT (ChatGPT) available** — Custom Actions via ngrok tunnel
- 🟡 **Chat1 (Telegram)** — Code ready, not persistently deployed
- 📋 **n8n** — Planned, not configured yet

**Source:** `docs/SYSTEM_SNAPSHOT.md` (SNAP-2025-11-26-003)

---

## 3. INFRA SUMMARY

| Service | Status | Notes |
|---------|--------|-------|
| GitHub | ✅ up | MCP Client on port 8081 |
| Google Workspace | ✅ up | Client on port 8082, OAuth working |
| ngrok | ✅ up | ⚠️ URL changes on restart |
| Claude Desktop | ✅ up | Full MCP access |
| GPT Actions | ✅ up | Depends on ngrok |
| Chat1 | 🟡 partial | Not deployed persistently |
| n8n | 📋 planned | Not configured |

**Full details:** `docs/INFRA_MAP.md`  
**Service status JSON:** `docs/system_state/registries/SERVICES_STATUS.json`

---

## 4. ACTIVE PLANS

**Current active plans:**

| Plan | Status | Notes |
|------|--------|-------|
| State Layer Completion | ✅ Done | Block STATE_LAYER_COMPLETION_V1 |
| Role Model Simplification | ✅ Done | Block ROLE_MODEL_SIMPLIFICATION_V1 |
| System State JSON Refresh | ✅ Done | Block SYSTEM_STATE_JSON_REFRESH_V2 |
| n8n Integration | 📋 Planned | Waiting for Or's task definition |

**Note:** אין כרגע `active_plans/` folder — תכנון עתידי.

---

## 5. RECENT WORK / BLOCKS

עבודה אחרונה (נכון ל-2025-11-26):

1. **Block 5** (2025-11-25) — Added Drive Snapshot Layer documentation
2. **Block 4** (2025-11-25) — Generated first SYSTEM_SNAPSHOT_DRIVE
3. **Block 3** (2025-11-25) — Created AUTOMATIONS_REGISTRY, metadata sections
4. **Block STATE_LAYER_COMPLETION_V1** (2025-11-26) — Created missing State Layer files:
   - SESSION_NOTE.md
   - INFRA_MAP.md
   - AGENT_SYNC_OVERVIEW.md (this file)
   - AGENT_CAPABILITY_PROFILE.md
   - SERVICES_STATUS.json
   - EVENT_TIMELINE.jsonl
5. **Block ROLE_MODEL_SIMPLIFICATION_V1** (2025-11-26) — Simplified agent role model, removed rigid hierarchy
6. **Block SYSTEM_STATE_JSON_REFRESH_V2** (2025-11-26) — Created SYSTEM_STATE_COMPACT.json for external agents

---

## 6. OPEN QUESTIONS / DECISIONS

### Pending Decisions

| ID | Question | Owner | Priority |
|----|----------|-------|----------|
| Q1 | When to deploy Chat1 persistently? | Or | Medium |
| Q2 | n8n vs Make.com — which to use? | Or | Medium |
| Q3 | Cloud deployment timing (Cloud Run)? | Or | Low |
| Q4 | Auto-sync policy for Drive Snapshot? | Claude + Or | Low |

### Recent Decisions (Locked)

- **DEC-001**: MCP Orchestration = Legacy/Reference Only
- **DEC-002**: GitHub Executor API = Not Deployed
- **DEC-003**: GPT GitHub Agent = DRY RUN Only
- **DEC-004**: Human-Approved Writes Only (Constitutional Amendment)

**Full decisions log:** `docs/DECISIONS_AI_OS.md`

---

## 7. QUICK LINKS

| Document | Purpose |
|----------|---------|  
| `docs/system_state/SYSTEM_STATE_COMPACT.json` | **Single JSON source** for external agents |
| `docs/CONSTITUTION.md` | Core principles & rules |
| `docs/CONTROL_PLANE_SPEC.md` | Phase, mode, variables |
| `docs/SYSTEM_SNAPSHOT.md` | Full system state |
| `docs/SESSION_NOTE.md` | Current session intent |
| `docs/INFRA_MAP.md` | Infrastructure map |
| `docs/SESSION_INIT_CHECKLIST.md` | How to start a session |

---

## 8. STATE LAYER BASELINE

### 🎯 STATE_LAYER_BASELINE_V1

**Declared:** 2025-11-26  
**Declared By:** Or (via GPT Operator)  
**Phase:** Phase 2 – Stabilizing the Hands

**Scope Blocks:**
- `STATE_LAYER_COMPLETION_V1` — Created missing State Layer files
- `ROLE_MODEL_SIMPLIFICATION_V1` — Simplified agent role model
- `SYSTEM_STATE_JSON_REFRESH_V2` — Created compact JSON state

**Core Files:**
- `docs/SNAPSHOT_LAYER_DESIGN.md` — State Layer design document (704 lines)
- `docs/system_state/SYSTEM_STATE_COMPACT.json` — Single JSON source for external agents
- `docs/system_state/agents/AGENT_CAPABILITY_PROFILE.md` — Agent capabilities and limitations
- `docs/system_state/registries/SERVICES_STATUS.json` — Service status registry
- `docs/system_state/timeline/EVENT_TIMELINE.jsonl` — Chronological event log
- `docs/system_state/AUTOMATIONS_REGISTRY.jsonl` — Automation inventory

**Notes:**
- This set of files and blocks is considered the **baseline State Layer (V1)** for Phase 2.2–2.3
- All future infra and automation work must keep these files consistent and up to date
- The State Layer provides synchronized state across all AI interfaces (Claude, GPT, Chat1)
- Changes to State Layer structure require explicit approval and documentation

**Status:** ✅ Declared and Locked

---

## 📝 How to Use This Document

**For all AI interfaces (Claude, GPT, Chat1):**
1. Read this file at session start for quick sync
2. Check SESSION_NOTE.md for current session intent
3. Verify CONTROL_PLANE_SPEC.md for Phase/Mode constraints
4. Cross-reference with SYSTEM_SNAPSHOT.md or SYSTEM_SNAPSHOT_DRIVE for full details

**Important:**
- This is a **summary**, not the source of truth
- When in doubt, check the source documents listed in section 7
- Update this file after significant system changes

---

**Last Updated:** 2025-11-26  
**Updated By:** Claude Desktop (STATE_LAYER_BASELINE_V1 declaration)
