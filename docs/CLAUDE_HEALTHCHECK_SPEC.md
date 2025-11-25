# CLAUDE_HEALTHCHECK_SPEC.md — Phase 2.2

## 📅 Date: 2025-11-25
**Status:** Draft (In Progress)
**Owner:** GPT Operator (under Or’s supervision)

---

## 🎯 Purpose
Define a structured health monitoring protocol for **Claude Desktop** — ensuring it can self‑report reliability, detect connection or permission issues, and summarize errors for human readability.

---

## 🧩 Scope
Applies to all Claude Desktop MCP integrations and local automations:
- Filesystem
- Git
- Windows Automation
- Google (Read)
- Browser
- Canva

---

## 🩺 Healthcheck Structure

Each MCP or module reports one of three states:
| State | Meaning | Required Action |
|--------|----------|-----------------|
| ✅ **OK** | Fully functional | None |
| ⚠️ **Flaky** | Intermittent or partial failures | Log in Digest, retry next session |
| ❌ **Broken** | Persistent failure | Alert Or, create GitHub issue, mark in Control Plane |

---

## 🧠 Data Model

```json
{
  "timestamp": "2025-11-25T12:34:56Z",
  "agent": "Claude Desktop",
  "phase": "2.2",
  "modules": {
    "filesystem": "OK",
    "git": "OK",
    "google_read": "Flaky",
    "browser": "OK",
    "canva": "Broken"
  },
  "summary": {
    "total_ok": 3,
    "total_flaky": 1,
    "total_broken": 1
  },
  "digest": [
    {
      "module": "canva",
      "error": "Authentication expired",
      "suggested_fix": "Re‑auth via Claude settings"
    },
    {
      "module": "google_read",
      "error": "Token refresh latency",
      "suggested_fix": "Run OAuth refresh script"
    }
  ]
}
```

---

## 📋 Reporting Format

At the end of each Claude Desktop session:
1. Run `claude_healthcheck.py`
2. Generate JSON file → `reports/healthcheck_YYYYMMDD.json`
3. Append summary line to `docs/CLAUDE_HEALTHCHECK_LOG.md`
4. If any ❌ Broken modules → notify GPT Operator + log in Control Plane

---

## 🧾 Digest Example (Markdown Summary)

```
### Claude Healthcheck — 2025‑11‑25
✅ Filesystem: OK  
✅ Git: OK  
⚠️ Google Read: Flaky (Token refresh latency)  
✅ Browser: OK  
❌ Canva: Broken (Authentication expired)

**Summary:** 3 OK, 1 Flaky, 1 Broken
**Next Step:** Re‑auth Canva, monitor Google latency.
```

---

## 🔗 Integration Points
- Update `SESSION_INIT_CHECKLIST.md` → add Healthcheck step.
- Add `claude_status` field to `CONTROL_PLANE_SPEC.md`.
- Report digest summary to `EVENT_TIMELINE` when active.

---

## 🧭 Implementation Notes
- Python script `claude_healthcheck.py` will scan logs and APIs.
- Uses standard exit codes: 0 (OK), 1 (Flaky), 2 (Broken).
- Future: Add Slack/Telegram (Chat1) notification integration.

---

## 🔮 Evolution Path
| Step | Description | Status |
|------|--------------|---------|
| 1 | Define Healthcheck Spec (this file) | ✅ Done |
| 2 | Implement `claude_healthcheck.py` | 🚧 In Progress |
| 3 | Integrate into Session Init & Control Plane | 🔜 Next |
| 4 | Automate periodic reports | ⏳ Planned |

---

**Phase:** 2.2 – Claude Healthcheck & Error Digest  
**Next Phases:** 2.3 Chat1 Stabilization → 2.4 Make Integration → 2.5 Consolidation  
**Mode:** INFRA_ONLY  

> “The system must feel its own heartbeat before it can move its hands.”