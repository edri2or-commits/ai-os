# Agents Sync Protocol — v0.1

**Phase:** 2 — Stabilizing the Hands  
**Mode:** INFRA_ONLY

## Purpose
Define how all system agents (Claude, GPT, Chat1, Make, Google) coordinate, exchange status, and maintain full operational synchronization.

## Roles & Responsibilities
| Agent | Role | Responsibilities |
|--------|------|------------------|
| **Claude** | Local Executor | Executes file operations, local scans, MCP integrations, reports errors and health status. |
| **GPT Operator** | Orchestrator | Manages phases, documentation, PRs, and Control Plane updates. |
| **Chat1 (Telegram)** | UI Gateway | Collects natural-language commands from Or, relays approved requests to GPT Operator. |
| **Make** | Automation Engine | Executes scheduled or triggered workflows, logs every action to Event Timeline. |
| **Google** | Workspace Agent | Provides data layer: Drive, Calendar, Sheets, Docs — must log every change through Event Timeline. |

## Sync Cycle
1. **Session Start:** Each agent runs its `SESSION_INIT_CHECKLIST.md` procedure.
2. **Heartbeat:** Every active agent sends a heartbeat with current state (online/offline, last action, last error).
3. **Control Plane Update:** GPT Operator aggregates all statuses into a unified snapshot (`docs/SYSTEM_SNAPSHOT.md`).
4. **Conflict Detection:** If inconsistencies are found (e.g., different modes or timestamps), Operator requests clarification from Or.
5. **Event Logging:** Each sync or action is appended to the `Event Timeline` with timestamp and actor.

## Handoff Protocol
- Tasks are handed off explicitly with: **{actor_from, actor_to, task_id, reason, next_step}**.
- No implicit delegation — every handoff must be logged.
- Or (the human) retains override authority for any task or sync issue.

## Reporting Standard
Each agent must maintain a small YAML or JSON object with:
```yaml
status: online
phase: 2
mode: INFRA_ONLY
last_sync: 2025-11-25T23:42:00Z
active_task: "Control Plane update"
last_error: null
```
Stored or referenced by Control Plane.

---

**Tech summary:**
- Added `AGENTS_SYNC_PROTOCOL.md` v0.1
- Defines sync cycle, handoff format, and reporting standards
- Connects Control Plane ↔ Event Timeline
- Documentation only (no automation yet)
