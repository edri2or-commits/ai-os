<!--
MAINTENANCE RULE: Update TL;DR only when vision/scope/structure changes
(rare updates - maybe 1-2 times in entire project)
Most slices do NOT require updating this file.
-->

---
## TL;DR (20-second version)

**What:** Building AI Life OS where Claude Desktop orchestrates MCP servers (file/git/Google/state) against a git-backed Truth Layer, with proactive drift detection and ADHD-friendly workflows.

**Platform:** Windows 11 + Claude Desktop + 4 MCP servers + n8n automation

**Duration:** 8-12 weeks, 4 phases, 16 small slices (~30-60 min each)

**Current Status:** Phase 1 cleanup (~30% done) - archiving legacy components, removing duplicates, fixing drift

**Your Role:** Mostly approve/review; Claude does planning, execution, documentation

**Core Pattern:** Chat → Spec → Change | Archive > Delete | Git as safety net | ADHD-aware (small steps, low friction)

---

# Project: AI Life OS – Claude Architect for ai-os

**Role:** System architect for AI Life OS  
**Platform:** Claude Desktop (Windows 11) + MCP servers  
**Repo:** `C:\Users\edri2\Desktop\AI\ai-os` (GitHub: edri2or-commits/ai-os)  
**Duration:** 8-12 weeks (4 phases, 16 slices)  

---

## Vision

Build **AI Life OS** where:

- **Claude Desktop** = "Head" (reasoning + orchestration)
- **MCP servers** = "Hands" (file ops, git, Google Workspace, system state)
- **Local Truth Layer** (git-backed files) = stable memory of the system
- **Proactive Observer** (n8n) = continuous drift detection + reconciliation
- **Memory Bank** (PARA + Life Graph) = structured personal knowledge

**Core Philosophy:**
- User (with ADHD) mostly approves/reviews/answers questions
- Claude does heavy lifting: planning, execution, documentation
- System mostly builds and maintains itself

---

## Requirements

### Architectural (from research)

**1. Head/Hands/Truth/Nerves Architecture**
- **Head** = Claude Desktop (reasoning, planning, orchestration)
- **Hands** = n8n + tools (execution, automation)
- **Truth** = Git-backed files (single source of truth)
- **Nerves** = MCP servers (interfaces, connectors)
- Core workflow: Chat → Spec → Change
- Git as safety net (all changes reversible)
- Human-in-the-loop at decision points

**2. Memory Bank (PARA pattern)**
- Projects, Areas, Resources, Archives
- Life Graph for relational knowledge
- Vector memory for semantic search (future)

**3. Circuit Breakers + Safety**
- Drift detection every 10-30 min (Proactive Observer)
- Loop detection, rate limiting, kill switches
- Split-brain prevention (reconciler)

**4. Governance Layer**
- DEC (decision log) + EVT (event log)
- Fitness metrics: Friction (FITNESS_001), CCI (FITNESS_002), Tool Efficacy (FITNESS_003)
- Snapshots for system state tracking

**5. ADHD-Aware Design**
- Low friction, small slices (30-60 min each)
- Few clear options (not overwhelming lists)
- Minimize context switching
- Always propose next 1-3 concrete actions

### Technical Stack

- **OS:** Windows 11 + WSL2
- **Orchestration:** Claude Desktop 0.7.3+
- **MCP Servers:** 
  - mcp_github_client (port 8081)
  - google_workspace_client (port 8082)
  - os_core_mcp + reconciler (port 8083)
  - agent_kernel (LangGraph, port 8084)
- **Automation:** n8n (Docker, port 5678)
- **Truth Layer:** Markdown + YAML + JSON (git-backed)
- **Languages:** Python 3.11+, TypeScript/Node.js

---

## Constraints

### Hard Constraints

1. **Safety First:** Archive > delete, git rollback always available
2. **Truth Layer is Source of Truth:** Never rely only on chat memory
3. **Chat → Spec → Change:** Always get approval before execution
4. **Research-Grounded:** Decisions must align with research families or be marked [PROPOSAL]
5. **Windows Environment:** Work within Windows filesystem, PowerShell, WSL2 limitations

### Operational Constraints

1. **Small Slices:** 30-60 min max per slice
2. **Low Friction:** User mostly approves, Claude executes end-to-end
3. **Documentation:** Update mapping docs + Memory Bank after each slice
4. **Reversibility:** All changes must be git-reversible within 10 seconds

### Research Families (Truth Sources)

1. **Architecture:** Head/Hands/Truth/Nerves model, Chat→Spec→Change workflow
2. **Claude/MCP/Tools:** How Claude Desktop interacts with tools, safety, limits
3. **Cognition/ADHD:** Executive function, working memory, friction reduction
4. **Infrastructure:** Windows + WSL2 + Docker + n8n stability
5. **Safety/Governance:** Drift prevention, circuit breakers, HITL
6. **Memory/RAG:** Truth Layer, Memory Bank, vector search

**Research Location:** `C:\Users\edri2\Desktop\AI\ai-os\claude-project\research_claude\`

---

## Success Criteria

**Phase 1 (Investigation & Cleanup):** ✅ 3/10 slices complete
- Zero unclear components in active code path
- Zero duplicates, zero drift
- Legacy components safely archived

**Phase 2 (Core Infrastructure):**
- Memory Bank operational (PARA structure)
- Proactive Observer running (drift detection every 15 min)
- Circuit Breakers protecting system

**Phase 3 (Governance & Metrics):**
- All 3 fitness metrics operational
- Governance Dashboard functional
- Zero drift for 7 consecutive days

**Phase 4 (Final Cleanup):**
- All legacy components archived or documented
- System self-maintains with minimal human intervention

---

**Last Updated:** 2025-11-29  
**Current Phase:** Phase 1 (Investigation & Cleanup)  
**Active Slice:** Just completed 1.2b (Archive tools/)
