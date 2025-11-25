# Event Timeline Specification — v0.1

**Phase:** 2 — Stabilizing the Hands
**Mode:** INFRA_ONLY

## Purpose
To create a single, unified event log that records every significant action in the AI‑OS ecosystem.

## Format
Each event is recorded as a line in a JSONL or Markdown table with the following fields:

| Field | Description | Example |
|--------|-------------|----------|
| timestamp | UTC time of the event | 2025‑11‑25T22:58:00Z |
| actor | The agent performing the action | Claude / GPT / Chat1 / Make / Google |
| action | Short description of what was done | "Updated CONTROL_PLANE_SPEC.md to v0.2" |
| result | success / failure / pending | success |
| mode | Current system mode | INFRA_ONLY |
| ref | Link to commit, PR, or spec | https://github.com/edri2or-commits/ai-os/commit/b641a23ef72a6ef969f4d7ebd6c0a5679c7614de |

## Flow
1. Each agent logs its actions locally or via the gateway.
2. GPT Operator consolidates logs and updates a master Event Timeline file or Google Sheet.
3. Timeline is reviewed periodically by Or for validation and clarity.

## Governance
- All actions must include the actor and reason.
- Logs older than TTL_DEFAULT (7d) can be archived automatically.
- No automation may run without its events being logged.

---

**Tech summary:**
- Created EVENT_TIMELINE_SPEC.md v0.1
- Defines event structure, flow, and governance
- Documentation only, no runtime behavior