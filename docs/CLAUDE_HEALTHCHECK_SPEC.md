# Claude Healthcheck Specification — v0.1

**Phase:** 2 — Stabilizing the Hands  
**Mode:** INFRA_ONLY

## Purpose
To define a consistent healthcheck protocol for Claude Desktop and its connected MCPs, ensuring transparency and reliability across all executions.

## MCP Health Matrix
| MCP | Description | Status Values | Notes |
|------|--------------|----------------|-------|
| Filesystem | Local file operations | OK / Flaky / Broken | Used for reading and writing local files |
| Git | Local Git operations | OK / Flaky / Broken | Manages repo sync and commits |
| Windows | OS-level automations | OK / Flaky / Broken | PowerShell, process handling |
| Google | Workspace integrations | OK / Flaky / Broken | Drive, Sheets, Docs, Calendar |
| Browser | Web interactions | OK / Flaky / Broken | Automation and scraping layer |
| Canva | Design automation | OK / Flaky / Broken | Image and presentation generation |
| Other MCPs | Any additional or custom connectors | OK / Flaky / Broken | To be appended dynamically |

## Report Format
Each session should produce a structured report in JSON or Markdown, containing:
```json
{
  "timestamp": "2025-11-25T23:54:00Z",
  "agent": "Claude",
  "phase": 2,
  "mcp_status": {
    "Filesystem": "OK",
    "Git": "Flaky",
    "Windows": "OK",
    "Google": "Broken"
  },
  "notes": "Google API timeout, retried twice."
}
```

## Error Digest Protocol
1. After each major session, Claude generates a brief summary called **Error Digest**.
2. The digest lists top 3–7 recurring issues with short explanations.
3. Digest is logged to the Event Timeline and reviewed by Or.

## Sync & Control Integration
- The Healthcheck feeds live data to the Control Plane.
- The Event Timeline receives updates for each MCP state change.
- GPT Operator consolidates health reports across all agents for a unified snapshot.

---

**Tech summary:**
- Added `CLAUDE_HEALTHCHECK_SPEC.md` v0.1
- Defines MCP status matrix and error digest process
- Integrates with Control Plane + Event Timeline
- Documentation only (no automation yet)
