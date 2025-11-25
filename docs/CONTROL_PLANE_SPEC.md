# Control Plane Specification — v0.2

**Phase:** 2 — Stabilizing the Hands
**Mode:** INFRA_ONLY

## Purpose
Defines how all system agents (GPT, Claude, Chat1, Make, Google) maintain synchronized state and report their status.

## Core Variables
| Variable | Description | Example |
|-----------|--------------|----------|
| SYSTEM_MODE | Current operational mode | "INFRA_ONLY" |
| AUTOMATIONS_ENABLED | Global kill switch | false |
| SANDBOX_ONLY | Restricts changes to sandbox environments | true |
| ACTIVE_PHASE | Current development phase | "2 - Stabilizing the Hands" |
| TTL_DEFAULT | Default time-to-live for experiments | "7d" |

## Responsibilities
- Each agent must report its status to the Control Plane.
- Status includes: online/offline, last sync time, last error, active tasks.
- The Control Plane aggregates all statuses into a unified system snapshot.
- Or (the human) approves transitions between modes or phases.
- Direct writes by any agent (GPT/Claude/Chat1) are allowed **only** if they are logged and committed with a traceable message.

## Sync Cycle
1. Each agent sends a heartbeat every session.
2. The Control Plane updates the System Snapshot.
3. GPT Operator generates a summary for Or if inconsistencies appear.
4. Event Timeline is updated for every system action.

## Logging & Accountability
- Every change is logged in the Event Timeline.
- Commits must include the actor and reason.
- Human-Approved Writes Only: Or retains ultimate oversight on all persistent changes.

---

**Tech summary:**
- Updated Control Plane to v0.2
- Added direct-write transparency policy
- Added sync + logging cycle
- Documentation only, no automation changes
