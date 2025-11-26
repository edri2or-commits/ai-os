# SYNC_AGENT_SESSION_TEMPLATE_V1

**Version:** 1.0  
**Created:** 2025-11-26  
**Author:** Claude Desktop (Block PHASE2_24_SYNC_AGENT_SESSION_TEMPLATE_V1)  
**Purpose:** Playbook for running manual Sync Agent sessions using the State Layer Blackboard

---

## 🎯 What is a Sync Agent Session?

A **Sync Agent Session** is a manual, structured review where Or, Claude Desktop, and/or GPT Operator work together to:
1. **Observe** what changed in the system since the last session
2. **Orient** to identify gaps, inconsistencies, and opportunities
3. **Decide** on proposed Blocks and tasks
4. **Act** by documenting proposals and (with Or's approval) executing them

**Key Principle:** The Sync Agent is **not autonomous**. It's a collaborative process with Human-in-the-Loop at every step.

---

## 📅 When to Run a Sync Session

### Triggers (Examples):

**Regular Schedule:**
- Start of a new work session (after 24+ hours since last session)
- End of day wrap-up (before closing the session)
- After completing a major Block

**Event-Driven:**
- After merging changes from remote (git pull)
- After deploying a new service
- When STATE_LAYER_BASELINE changes
- When gaps are suspected (e.g., "things feel out of sync")

**On-Demand:**
- Or asks: "What's the current state?"
- Or asks: "What should we work on next?"
- Before starting a new Phase or Mode transition

**Frequency Recommendation:** 
- Daily for active development (Phase 2.2-2.3)
- Weekly for maintenance mode (future phases)

---

## 📥 Session Inputs (Required Reading)

Before starting OODA, read these files in order:

### 1. **Quick Sync Files** (always read first):
- `docs/AGENT_SYNC_OVERVIEW.md` — Current Phase, Mode, Recent Work, Open Questions
- `docs/SESSION_NOTE.md` — Current session intent and constraints (if exists)

### 2. **State Layer Files** (for full context):
- `docs/system_state/SYSTEM_STATE_COMPACT.json` — Full system state (interfaces, services, gaps)
- `docs/TOOL_INTEGRATION_MAP.md` — Who accesses what and how

### 3. **Timeline** (for delta detection):
- `docs/system_state/timeline/EVENT_TIMELINE.jsonl` — Read **only new events** since last session
  - Identify last session timestamp (from previous `session_init` or `sync` event)
  - Filter: `timestamp > last_session_timestamp`

### 4. **Registries** (if reviewing specific areas):
- `docs/system_state/registries/SERVICES_STATUS.json` — Service statuses
- `docs/system_state/AUTOMATIONS_REGISTRY.jsonl` — Automation inventory

**Note:** Don't read everything every time. Focus on what's relevant to the current session intent.

---

## 🔄 OODA Loop on the Blackboard

### **O — Observe (תצפית)**

**Goal:** Understand what changed since last session.

**Questions to Answer:**
- What's the last session timestamp? (from EVENT_TIMELINE)
- What events happened since then?
  - Blocks completed?
  - Services changed status?
  - New automations added?
  - Errors logged?
  - Decisions made?
- What's the current Phase & Mode? (from AGENT_SYNC_OVERVIEW)
- Are there any critical issues flagged? (from SYSTEM_STATE_COMPACT)

**Output:** List of recent changes (events, service status updates, new files)

**Example Observation:**
```
Since last session (2025-11-26T12:52:00Z):
- EVT-2025-11-26-006: STATE_LAYER_BASELINE_V1 declared
- EVT-2025-11-26-007: TOOL_INTEGRATION_MAP_V1 created
- Phase: 2.2-2.3, Mode: INFRA_ONLY
- Critical Issue: ngrok URL instability (still unresolved)
```

---

### **O — Orient (התמצאות)**

**Goal:** Identify gaps, inconsistencies, and opportunities.

**Types of Issues to Look For:**

**Gaps (פערים):**
- Service status mismatch:
  - Service `up` in SERVICES_STATUS but `partial` in SYSTEM_STATE_COMPACT
  - Automation in AUTOMATIONS_REGISTRY but not in SERVICES_STATUS
- Missing documentation:
  - Service running but no entry in AUTOMATIONS_REGISTRY
  - Block completed but AGENT_SYNC_OVERVIEW not updated
- Open gaps in SYSTEM_STATE_COMPACT with no planned Blocks

**Inconsistencies (אי-עקביות):**
- Phase mismatch between CONTROL_PLANE_SPEC and AGENT_SYNC_OVERVIEW
- Last Updated timestamps > 48h old (stale documentation)
- Event logged but STATE_LAYER file not updated accordingly

**Opportunities (הזדמנויות):**
- Pending decisions in AGENT_SYNC_OVERVIEW that can be addressed
- Automation not verified recently (> 7 days)
- Critical issue with known solution path (e.g., ngrok → paid plan or cloud deployment)
- Ready-to-execute Blocks waiting for approval

**Tool-Specific Risks:**
- Access patterns unclear or untested (from TOOL_INTEGRATION_MAP)
- Service marked `error_auth` (like AUTO-GAS-001)
- Dependencies between services not documented

**Output:** Categorized list of findings

**Example Orientation:**
```
Gaps:
- GAP-001 (ngrok URL instability) still open, no Block proposed
- SERVICES_STATUS shows 14 services, SYSTEM_STATE_COMPACT lists 11 (mismatch)

Inconsistencies:
- AGENT_SYNC_OVERVIEW Last Updated: 2025-11-26T11:00 (stale, >5h)
- n8n status: "planned" in both files (consistent ✓)

Opportunities:
- AUTO-GAS-001 (Collector_Gmail_to_Records) needs decision: fix/migrate/disable
- Can create BLOCK_NGROK_STABILITY_PLAN to address GAP-001
```

---

### **D — Decide (החלטה)**

**Goal:** Propose Blocks and prioritize tasks.

**Block Proposal Format:**
```
BLOCK_ID: BLOCK_<SHORT_DESCRIPTIVE_NAME>
Priority: Critical | High | Medium | Low
Responsible: Claude Desktop | GPT Operator | Or
Estimated Time: <minutes/hours>
Dependencies: <list of other Blocks or prerequisites>
Rationale: <why is this Block necessary?>
Actions:
  - <concrete step 1>
  - <concrete step 2>
  - ...
```

**Prioritization Criteria:**
1. **Critical:** Blocks system functionality or violates safety constraints
2. **High:** Closes important gaps or prevents future issues
3. **Medium:** Improves documentation or developer experience
4. **Low:** Nice-to-have, can be deferred

**Task Classification:**
- **Quick wins:** < 30 minutes, can be done immediately
- **Blocks:** > 30 minutes, need planning and potentially multiple sessions
- **Decisions:** Require Or's input before proceeding

**Output:** List of proposed Blocks with priorities

**Example Decisions:**
```
Proposed Blocks:

BLOCK_AGENT_SYNC_OVERVIEW_REFRESH
Priority: High
Responsible: Claude Desktop
Time: 15 minutes
Dependencies: None
Rationale: AGENT_SYNC_OVERVIEW is stale (>5h), needs update with recent Blocks
Actions:
  - Update "Recent Work / Blocks" section
  - Update "Last Updated" timestamp
  - Add TOOL_INTEGRATION_MAP_V1 to Quick Links

BLOCK_NGROK_STABILITY_DECISION
Priority: High
Responsible: Or (decision) + GPT Operator (research)
Time: 1-2 hours
Dependencies: None
Rationale: GAP-001 critical issue blocking reliable GPT access
Actions:
  - GPT: Research ngrok paid plans vs cloud deployment (Google Cloud Run)
  - GPT: Write comparison doc with cost/complexity analysis
  - Or: Decide on solution approach
  - Log decision in CONTROL_PLANE_SPEC

BLOCK_AUTO_GAS_001_RESOLUTION
Priority: Medium
Responsible: Or (decision) + Claude Desktop (execution)
Time: 30-60 minutes
Dependencies: Or's decision
Rationale: Legacy Apps Script failing, needs explicit decision
Actions:
  - Or decides: fix OAuth / migrate to new arch / disable
  - If fix: Claude updates OAuth permissions in Apps Script
  - If migrate: Create BLOCK_GMAIL_COLLECTOR_MIGRATION
  - If disable: Update AUTOMATIONS_REGISTRY status to "disabled"
```

---

### **A — Act (פעולה)**

**Goal:** Execute approved tasks and log results.

**What "Act" Means in Sync Agent v0 (Manual):**
- **NOT:** Autonomous execution
- **IS:** Or approves → Agent executes → Results logged

**Execution Flow:**
1. **Present proposals** to Or (list of Blocks + quick wins)
2. **Or selects** what to execute now vs later
3. **Agent executes** selected tasks:
   - Claude Desktop: file edits, scripts, Git operations
   - GPT Operator: specs, research, Google Workspace operations
4. **Log to EVENT_TIMELINE** after each significant action
5. **Update State Layer** files as needed (AGENT_SYNC_OVERVIEW, SERVICES_STATUS, etc.)

**Quick Win Example:**
```
Or: "Yes, please refresh AGENT_SYNC_OVERVIEW"
Claude: [edits docs/AGENT_SYNC_OVERVIEW.md]
Claude: [logs EVT-2025-11-26-008 to EVENT_TIMELINE]
Claude: "Done. AGENT_SYNC_OVERVIEW updated with recent Blocks."
```

**Block Example:**
```
Or: "Start on BLOCK_NGROK_STABILITY_DECISION, ask GPT to research"
Claude: "I'll create a task for GPT Operator"
[Claude creates GitHub issue or Drive doc with research request]
GPT: [researches and writes comparison doc]
Or: [reviews and makes decision]
Claude: [logs decision to CONTROL_PLANE_SPEC + EVENT_TIMELINE]
```

---

## 📤 Session Outputs

At the end of a Sync Session, produce:

### 1. **Findings Summary**
```markdown
## Findings Since Last Session

**Last Session:** 2025-11-26T12:52:00Z (session_id: claude-desktop-20251126-1247)

**Events Since Then:**
- EVT-2025-11-26-006: STATE_LAYER_BASELINE_V1 declared
- EVT-2025-11-26-007: TOOL_INTEGRATION_MAP_V1 created

**Service Changes:**
- No service status changes

**Critical Issues:**
- GAP-001 (ngrok URL instability) still open
```

---

### 2. **Detected Gaps**
```markdown
## Detected Gaps

**Gaps:**
- GAP-001: ngrok URL instability (no Block proposed yet)
- SERVICES_STATUS vs SYSTEM_STATE_COMPACT mismatch (14 vs 11 services)

**Inconsistencies:**
- AGENT_SYNC_OVERVIEW stale (>5h since last update)

**Opportunities:**
- AUTO-GAS-001 needs decision (fix/migrate/disable)
- Can create BLOCK_NGROK_STABILITY_PLAN
```

---

### 3. **Proposed Blocks**
```markdown
## Proposed Blocks

### BLOCK_AGENT_SYNC_OVERVIEW_REFRESH
- **Priority:** High
- **Responsible:** Claude Desktop
- **Time:** 15 minutes
- **Actions:**
  - Update "Recent Work / Blocks" section
  - Update "Last Updated" timestamp
  - Add TOOL_INTEGRATION_MAP_V1 to Quick Links

### BLOCK_NGROK_STABILITY_DECISION
- **Priority:** High
- **Responsible:** Or + GPT Operator
- **Time:** 1-2 hours
- **Actions:**
  - Research ngrok paid vs cloud deployment
  - Write comparison doc
  - Or decides on approach
  - Log decision

[... more Blocks ...]
```

---

### 4. **Tool Risks & Open Questions**
```markdown
## Tool Risks & Open Questions

**Tool Risks:**
- **ngrok:** URL changes on restart → breaks GPT Actions (GAP-001)
- **AUTO-GAS-001:** Failing auth, still running hourly (noise in logs)
- **Claude MCP:** Read-only Google access → all writes via GPT (dependency)

**Open Questions:**
- Should we prioritize ngrok stability over other Phase 2.3 work?
- What's the timeline for n8n integration? (affects architecture decisions)
- Do we need Docker now or wait for n8n? (affects local setup)

**Pending Decisions:**
- DEC-004: ngrok paid plan vs cloud deployment
- DEC-005: AUTO-GAS-001 resolution (fix/migrate/disable)
```

---

## 📋 Session Template (Copy-Paste Ready)

```markdown
# Sync Agent Session: [DATE]

**Session ID:** sync-agent-[YYYYMMDD-HHMM]  
**Actor:** Claude Desktop + Or (+ GPT Operator if needed)  
**Mode:** INFRA_ONLY  
**Phase:** 2.2-2.3

---

## 📥 Inputs Read
- [ ] docs/AGENT_SYNC_OVERVIEW.md
- [ ] docs/system_state/SYSTEM_STATE_COMPACT.json
- [ ] docs/TOOL_INTEGRATION_MAP.md
- [ ] docs/system_state/timeline/EVENT_TIMELINE.jsonl (new events only)

---

## 🔄 OODA Loop

### O — Observe
**Last Session Timestamp:** [ISO timestamp from last session_init or sync event]

**Events Since Last Session:**
- [EVT-ID]: [summary]
- [EVT-ID]: [summary]

**Service Changes:**
- [service_id]: [old_status] → [new_status]

**Critical Issues:**
- [GAP-ID]: [description]

---

### O — Orient

**Gaps Detected:**
1. [Gap description]
2. [Gap description]

**Inconsistencies Detected:**
1. [Inconsistency description]
2. [Inconsistency description]

**Opportunities Identified:**
1. [Opportunity description]
2. [Opportunity description]

---

### D — Decide

**Proposed Blocks:**

#### BLOCK_[NAME]
- **Priority:** [Critical/High/Medium/Low]
- **Responsible:** [Claude/GPT/Or]
- **Time:** [estimate]
- **Dependencies:** [list or "None"]
- **Rationale:** [why needed]
- **Actions:**
  - [ ] [action 1]
  - [ ] [action 2]

[... repeat for each Block ...]

**Quick Wins (< 30 min):**
- [ ] [task 1]
- [ ] [task 2]

---

### A — Act

**Approved by Or:**
- [ ] BLOCK_[NAME] → [Status: In Progress / Completed / Deferred]
- [ ] Quick Win: [task] → [Status]

**Execution Log:**
- [timestamp]: [Actor] started [task]
- [timestamp]: [Actor] completed [task]
- [timestamp]: Logged [EVT-ID] to EVENT_TIMELINE

---

## 📤 Session Outputs

**Blocks Completed This Session:**
1. [BLOCK_ID]: [summary]

**Blocks Deferred:**
1. [BLOCK_ID]: [reason for deferral]

**Open Questions for Next Session:**
1. [Question]
2. [Question]

**Next Session Trigger:**
- [Planned date/time or event trigger]

---

**Session End:** [ISO timestamp]  
**Logged As:** [EVT-ID in EVENT_TIMELINE]
```

---

## 🔧 Usage Tips

### For Claude Desktop:
- Start sessions with: "Let's run a Sync Agent session"
- Use this template as a checklist
- Focus on OODA structure: don't skip Orient step (gap detection is critical)
- Log major actions to EVENT_TIMELINE immediately
- Keep Or in the loop: present findings before executing

### For GPT Operator:
- Can be called mid-session for strategic questions (e.g., "Research ngrok alternatives")
- Useful for writing specs that come out of Decide phase
- Can access Drive Snapshot for fuller context if needed

### For Or:
- Review findings summary first, then approve specific Blocks
- Can say "skip Orient, I know the gaps" if time-constrained
- Can defer Blocks to next session or later Phase
- Use this to guide "what should we work on today?" questions

---

## 🚦 Constraints (Phase 2.2-2.3)

**INFRA_ONLY Mode:**
- ❌ No automations on Or's life (Calendar, Gmail, Tasks)
- ❌ No n8n workflows (planned for Phase 2.4+)
- ❌ No autonomous execution (Human-in-the-Loop always)
- ✅ Focus: infrastructure, State Layer, documentation

**Safety:**
- ✅ All git commits require Or's approval before push
- ✅ All service deployments require Or's approval
- ✅ All CONSTITUTION changes require Or's explicit approval

---

## 📚 Related Documents

- **AGENT_SYNC_SPEC_BLACKBOARD_V0.md** — Full spec for Sync Agent architecture
- **TOOL_INTEGRATION_MAP.md** — Who accesses what and how
- **CONTROL_PLANE_SPEC.md** — Phase, Mode, and control variables
- **SESSION_INIT_CHECKLIST.md** — Standard session startup protocol
- **SNAPSHOT_LAYER_DESIGN.md** — State Layer architecture overview

---

**Version:** 1.0  
**Last Updated:** 2025-11-26  
**Status:** ✅ Ready for use in Phase 2.2-2.3

> "The Blackboard is the source of truth. The Sync Agent is the process that keeps it honest."
