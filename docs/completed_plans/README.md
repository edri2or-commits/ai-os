# Completed Plans — Archive

This directory stores finalized and archived evolution plans of Or’s AI-OS.

Each plan is moved here automatically (or manually) when its status switches
from `active` to `closed`. The filename and metadata preserve its history.

---

## 📁 Structure
- `PLAN_NAME.md` — The full final version of the plan.
- `PLAN_NAME.meta.yaml` — Metadata (dates, agents, final status, approvals).

---

## 🧩 Automation (Future)
In future phases, Control Plane or Make scenarios will:
- Detect when an `active_plan` is marked `closed`.
- Move the plan file and create metadata automatically.
- Update `CONTROL_PLANE_SPEC.md` to remove the `active_master_plan` pointer.
- Log this transition to the Event Timeline.

---

*Created automatically as part of AI-OS Phase 2 evolution (2025-11-25).*