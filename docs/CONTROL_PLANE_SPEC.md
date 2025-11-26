# CONTROL_PLANE_SPEC.md — Phase 2.2 Update

## 📅 Date: 2025-11-25
**Owner:** GPT Operator (under Or's supervision)

---

## 🎯 Purpose
Central configuration and real‑time state tracking document for AI‑OS.
Defines operational mode, automation state, active phase, and agent statuses.

---

## ⚙️ System Mode
| Field | Description | Example |
|-------|-------------|----------|
| `system_mode` | Defines global operation context | `INFRA_ONLY` / `LIFE_AUTOMATIONS` / `EXPERIMENT` |
| `automations_enabled` | Kill Switch for all automated flows | `false` |
| `sandbox_only` | Run tests in sandbox mode only | `true` |
| `active_phase` | Current development phase | `2.2 – Claude Healthcheck & Error Digest` |

---

## 🤖 Agent Status Tracking
Each core agent reports its status via session init or periodic healthchecks.

| Agent | Description | Status Field | Example |
|--------|--------------|---------------|----------|
| Claude Desktop | Local execution layer | `claude_status` | `OK` / `Flaky` / `Broken` |
| GPT Operator | Central orchestrator | `gpt_status` | `OK` |
| Chat1 | Telegram interface | `chat1_status` | `Flaky` |
| Make | Automation agent | `make_status` | `Inactive` |
| Google | Google Workspace connector | `google_status` | `OK` |

---

## 🩺 Healthcheck Integration (Phase 2.2)
- Claude's `services/claude_healthcheck.py` generates a JSON report under `/reports/`.
- Operator GPT reads latest report → updates `claude_status` here.
- Example snippet:

```json
"agents": {
  "claude_status": "OK",
  "gpt_status": "OK",
  "chat1_status": "Flaky",
  "make_status": "Inactive",
  "google_status": "OK"
}
```

### 🩺 Claude Desktop Status (Last Healthcheck)
**Updated:** 2025-11-26T12:47:24Z  
**Source:** `reports/healthcheck_20251126_124724.json`  
**Script:** `services/claude_healthcheck.py`

| Field | Value |
|-------|-------|
| **Overall Status** | `mostly_healthy` |
| **Modules OK** | `browser`, `canva` |
| **Modules Flaky** | `filesystem`, `git`, `google_read` |
| **Modules Broken** | None |
| **Total Checked** | 5 modules |

**Notes:**
- ✅ 2/5 modules fully operational
- 🟡 3/5 modules showing intermittent issues (non-critical)
- 🔴 0/5 modules broken
- Flaky modules require attention but don't block current work

---

## 🔐 Automation Control Fields
| Field | Description | Type | Default |
|--------|-------------|------|----------|
| `ttl` | Time‑to‑Live for temporary experiments | Integer (days) | `3` |
| `approved_by` | Human approver (Or) | String | `"Or"` |
| `last_review` | Last reviewed date | ISO‑date | `2025‑11‑25` |

---

## 📊 Event Timeline Link
All significant agent state changes are logged to `EVENT_TIMELINE.md` or a JSONL file.

Example entry:
```
2025‑11‑25T12:55:00Z | Claude | Healthcheck | Status=OK | Phase=2.2
```

---

## 📝 Current Session

### Session: claude-desktop-20251126-1247
**Session Mode:** `INFRA_ONLY`  
**Declared By:** GPT Operator (via Or)  
**Declared At:** 2025-11-26T12:52:00Z  
**Phase:** 2.2 (Claude Healthcheck & Error Digest)

**Session Constraints:**
- ⛔ No automations on Or's life during this session
- ✅ INFRA/STATE/DOCS work only
- ✅ Human-in-the-loop for all significant changes
- ⛔ No git push without explicit approval

---

**Phase:** 2.2 – Claude Healthcheck & Error Digest  
**Next Phases:** 2.3 Chat1 Stabilization → 2.4 Make Integration → 2.5 Consolidation  
**Mode:** INFRA_ONLY  

> "Control without visibility is illusion — the plane must always know its altitude."
