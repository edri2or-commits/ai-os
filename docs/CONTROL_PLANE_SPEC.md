# Control Plane Specification — v0.3

**Phase:** 2 — Stabilizing the Hands  
**Mode:** INFRA_ONLY  
**Last Updated:** 2025-11-25 (Block 5)

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

## Drive Snapshot Layer

The **Drive Snapshot Layer** provides a synchronized view of the system state for agents that don't have direct repo access.

### What is SYSTEM_SNAPSHOT_DRIVE?

| Property | Value |
|----------|-------|
| **Type** | Google Doc |
| **Name** | `SYSTEM_SNAPSHOT_DRIVE` |
| **Location** | Google Drive (AI-OS System State folder) |
| **Link** | https://docs.google.com/document/d/1-ysIo2isMJpHjlYXsUgIBdkL4y21QPb- |
| **Role** | **Derivative view** of repo state, not SSOT |
| **Primary Consumer** | GPT Planning Model |

### Key Principles

1. **SSOT Remains the Repo** — The Drive snapshot is a **view**, not a competing source of truth.
2. **Human-Triggered Sync** — Updates are triggered manually by Or (at least for now).
3. **Freshness Metadata** — Every snapshot includes generation time and confidence level.

### Who Updates the Snapshot?

| Actor | Role |
|-------|------|
| **Claude Desktop** | Primary generator — reads repo, writes to Drive |
| **GPT GitHub Operator** | Secondary — can sync after repo PRs |
| **Or (Human)** | Triggers updates, approves sync |
| **GPT Planning Model** | Consumer only — reads, does not write |

### When to Refresh the Snapshot

| Trigger | Priority |
|---------|----------|
| Before planning a new system phase | 🟢 High |
| After significant architecture changes | 🟢 High |
| After a major block series (like Blocks 1-5) | 🟢 High |
| Weekly refresh (prevent staleness) | 🟡 Medium |
| On explicit request from Or or any agent | 🟢 Always |

### Data Sources for Snapshot Generation

The Drive snapshot is generated from these repo files:

- `docs/SYSTEM_SNAPSHOT.md` — Primary state source
- `docs/CONTROL_PLANE_SPEC.md` — Mode, phase, variables
- `docs/system_state/AUTOMATIONS_REGISTRY.jsonl` — Automation inventory
- `agents/AGENTS_INVENTORY.md` — Agent roles and status
- `docs/PHASE2_CHECKLIST.md` — Current phase progress

### Related Documentation

- **Design Doc:** `docs/SNAPSHOT_LAYER_DESIGN.md`
- **Template:** `docs/system_state/SYSTEM_SNAPSHOT_DRIVE_TEMPLATE.md`
- **Registry Entry:** `AUTO-009` in `AUTOMATIONS_REGISTRY.jsonl`

---

**Tech summary:**
- Control Plane v0.3
- Added direct-write transparency policy
- Added sync + logging cycle
- Added Drive Snapshot Layer documentation (Block 5)
- Documentation only, no automation changes
