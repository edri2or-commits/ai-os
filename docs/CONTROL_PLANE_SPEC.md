# CONTROL_PLANE_SPEC — System Control Plane (v1.1)

## 🧭 Purpose
Defines the operational state of Or’s AI-OS — modes, active plans, automation flags, and sandboxing rules.

---

## ⚙️ Core Fields

```yaml
SYSTEM_MODE: INFRA_ONLY
AUTOMATIONS_ENABLED: false
SANDBOX_ONLY: true
ACTIVE_PHASE: 2
TTL_DEFAULT: 7d
active_master_plan: "docs/active_plans/PLAN_AI_OS_EVOLUTION.md"
```

---

## 🔍 Description
- **SYSTEM_MODE** — Current global mode (`INFRA_ONLY`, `LIFE_AUTOMATIONS`, `EXPERIMENT`).
- **AUTOMATIONS_ENABLED** — Global kill-switch for external automations.
- **SANDBOX_ONLY** — Ensures experiments run only in sandboxed environments.
- **ACTIVE_PHASE** — Tracks which phase is currently in progress.
- **TTL_DEFAULT** — Default time-to-live for experiments or automations.
- **active_master_plan** — Path to the currently active evolution plan.

---

## 🧩 Integration Notes
- Every agent during `Session Init` must load this file to know the global mode and current phase.
- When a new plan opens, this file is updated automatically with the plan’s path.
- Once a plan is closed, the pointer is cleared or replaced.

---

## 🧠 Future Extension
- Add real-time sync with Control Plane dashboard (Google Sheet / Make Scenario).
- Include agent-specific statuses (Claude, GPT, Chat1, Make).
- Link Event Timeline entries with Control Plane state changes.

---

*Updated automatically as part of AI-OS Phase 2 continuation (2025-11-25).*