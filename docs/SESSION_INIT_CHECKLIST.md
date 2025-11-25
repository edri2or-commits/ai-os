# SESSION_INIT_CHECKLIST.md — Updated for Phase 2.2

## 📅 Date: 2025-11-25
**Owner:** GPT Operator (under Or’s supervision)

---

## ✅ Session Initialization Protocol
Every agent session (GPT, Claude, Chat1, Make) must perform these checks before execution.

| Step | Description | Responsible | Output |
|------|--------------|--------------|---------|
| 1 | Identify Agent & Role | All agents | Agent manifest (who am I, mode, phase) |
| 2 | Verify Repository Sync | Claude / GPT | Confirm branch = main (SSOT) |
| 3 | Load Core Docs | All agents | Constitution, System Snapshot, Decisions, Capabilities |
| 4 | Load Active Plan | Operator GPT | docs/active_plans/PHASE2_Stabilizing_The_Hands.md |
| 5 | Run Healthcheck | Claude Desktop | Execute `services/claude_healthcheck.py` → report JSON + summary |
| 6 | Evaluate Claude Status | Operator GPT | Parse latest report → update `CONTROL_PLANE_SPEC.md` (`claude_status`) |
| 7 | Declare Session Mode | Operator GPT | INFRA_ONLY / LIFE_AUTOMATIONS / EXPERIMENT |
| 8 | Log Session Start | GPT Operator | Append entry in `EVENT_TIMELINE` (actor, mode, phase) |

---

## 🩺 Step 5 — Healthcheck Integration (New in Phase 2.2)
- Claude runs the script: `python services/claude_healthcheck.py`
- Output stored in: `reports/healthcheck_YYYYMMDD_HHMMSS.json`
- Summary logged to `docs/CLAUDE_HEALTHCHECK_LOG.md`
- If any ❌ Broken modules detected → notify Or and halt automation flow.

---

## 🧭 Implementation Notes
- Healthcheck step is mandatory before any repo or Google action.
- Failing to run Healthcheck marks session as invalid.
- Future: integrate Chat1 alert for failed Healthchecks.

---

**Phase:** 2.2 – Claude Healthcheck & Error Digest  
**Next Phases:** 2.3 Chat1 Stabilization → 2.4 Make Integration → 2.5 Consolidation  
**Mode:** INFRA_ONLY  

> “Initialization without introspection is blindness.”