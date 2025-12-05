<!--
MAINTENANCE RULE: Update TL;DR only when vision/scope/structure changes
(rare updates - maybe 1-2 times in entire project)
Most slices do NOT require updating this file.
-->

---
## TL;DR (20-second version)

**What:** Building AI Life OS - a **Cognitive Prosthetic** for ADHD. Claude Desktop (Application Core) orchestrates MCP Adapters (filesystem/git/Google/n8n) against a git-backed Truth Layer, with MAPE-K autonomic loop (Observer/Reconciler/Executor) and ADHD-friendly workflows.

**Architecture:** Hexagonal (Ports & Adapters) + MAPE-K Control Loop (per ADR-001)

**Platform:** Windows 11 + Claude Desktop + MCP servers + n8n automation + Docker

**Duration:** 8-12 weeks, 4 phases, small slices (~30-60 min each)

**Current Status:** Phase 2 Architectural Alignment (~15% done) - Foundation docs complete (ADR-001, Canonical Terminology, Architecture Reference, Metaphor Guide)

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

Build **AI Life OS** - a **Cognitive Prosthetic** for ADHD where:

- **Application Core** (Claude Desktop) = reasoning + orchestration layer
- **MCP Adapters** = Secondary Adapters implementing Ports (filesystem, git, Google Workspace, n8n)
- **Truth Layer** (git-backed files) = persistent state + version control
- **MAPE-K Control Loop** = autonomic behavior (Monitor/Analyze/Plan/Execute/Knowledge)
  - Observer (Monitor) = drift detection
  - Reconciler (Plan) = change request generation  
  - Executor (Execute) = approved change application
- **Memory Bank** (PARA + Life Graph) = structured personal knowledge
- **n8n** = Dual-role Adapter (both Driving and Driven, per architecture)

**Core Philosophy:**
- User (with ADHD) mostly approves/reviews/answers questions
- Claude does heavy lifting: planning, execution, documentation
- System mostly builds and maintains itself

**Architecture:** Hexagonal (Ports & Adapters) as canonical pattern - see ADR-001

📐 **For canonical architecture:** Read `memory-bank/docs/decisions/ADR-001-architectural-alignment.md`
🔤 **For official terminology:** Read `memory-bank/docs/CANONICAL_TERMINOLOGY.md`
❤️ **For WHY this system exists:** Read `memory-bank/00_The_Sovereign_AI_Manifesto.md`

---

## Narrative Architecture

The AI Life OS has a **3-layer narrative structure** that explains WHY and HOW it works:

### Layer 1: The Manifesto (WHY)
?? **File:** `memory-bank/00_The_Sovereign_AI_Manifesto.md`

Answers: "Why does this system exist?"

**Content:**
- 4 Core Principles:
  1. **Cognitive Sovereignty:** My data, my model, my interface
  2. **Attention Defense:** System serves focus, not engagement
  3. **Executive Prosthesis:** AI as scaffold, not builder
  4. **The Gardener:** Cultivation over consumption
- Each principle justified by ADHD cognitive needs
- Journey Map connecting to all documentation

**When to read:**
- New to the project
- Feeling lost ("������ �����")
- Need to explain system to others
- Questioning architectural decisions

### Layer 2: ADRs (WHY Technical Choices)
📐 **Directory:** `memory-bank/docs/decisions/`

Answers: "Why did we choose technology X?"

**Content:**
- Architecture Decision Records (ADRs)
- Format: Context → Options → Decision → Justification → Consequences
- Each includes **ADHD Relevance** section where applicable
- Energy State tracking (meta-cognition for decisions)

**Key ADR:** ADR-001 (Architectural Alignment)
- **Decision:** Hexagonal Architecture (Ports & Adapters) as PRIMARY pattern
- **Secondary:** MAPE-K Control Loop for autonomic behavior  
- **Rejects:** "Semantic Microkernel" (not canonical), "QAL Machine" (no reference)
- **Authority:** Alistair Cockburn (Hexagonal), IBM (MAPE-K), Michael Nygard (ADR format)
- **Companions:** 
  - `CANONICAL_TERMINOLOGY.md` - Official terms dictionary (ONLY authoritative source)
  - `ARCHITECTURE_REFERENCE.md` - Detailed technical guide (300+ lines)
  - `METAPHOR_GUIDE.md` - When to use which metaphor

**Why this matters:**
- Prevents architectural drift (multiple competing metaphors)
- Enables technology swapping (change n8n without rewriting Core)
- Provides professional vocabulary (industry-standard patterns)
- Enforces consistency (all decisions reference ADR-001)

### Layer 3: Design Guide (HOW to Build)
?? **File:** `docs/ATTENTION_CENTRIC_DESIGN.md`

Answers: "How do we build ADHD-friendly interfaces?"

**Content:**
- 5 Core Patterns (backed by cognitive science):
  1. **North Star:** Persistent Context (externalizes working memory)
  2. **Time Materialization:** Visual timers (combats time blindness)
  3. **The Bouncer:** Interruption management (protects flow)
  4. **Conversational Scaffolding:** Task decomposition (reduces paralysis)
  5. **Panic Button:** Safe reset (nothing lost)
- Visual Grammar: Typography, color, whitespace, lists, animations
- Implementation Checklist + Heuristic Evaluation
- Research grounding: Barkley, Sweller, Miller, Humane Tech

**When to use:**
- Building new UI/UX
- Evaluating external tools (Obsidian, Notion, etc.)
- Making design decisions
- Validating ADHD-friendliness

### Integration

These 3 layers connect:
- **Manifesto principles** ? guide ADR decisions
- **ADR decisions** ? reference Manifesto sections
- **Design patterns** ? implement Manifesto Executive Prosthesis principle
- **All layers** ? grounded in ADHD cognitive science

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

1. **Architecture:** Hexagonal (Ports & Adapters), MAPE-K Loop, Chat→Spec→Change workflow
2. **Claude/MCP/Tools:** How Application Core interacts with MCP Adapters, safety, limits
3. **Cognition/ADHD:** Executive function, working memory, friction reduction, Cognitive Prosthetic
4. **Infrastructure:** Windows + WSL2 + Docker + n8n stability
5. **Safety/Governance:** Drift prevention, circuit breakers, HITL, ADRs
6. **Memory/Life Graph:** Truth Layer, Memory Bank (PARA), Life Graph entities

**Research Location:** `C:\Users\edri2\Desktop\AI\ai-os\claude-project\research_claude\`

**⚠️ CRITICAL TERMINOLOGY NOTE:**
All research docs were written BEFORE ADR-001 (Architectural Alignment). They may use **deprecated terms**:
- `"The Brain"` / `"The Head"` → Use **"Application Core"** instead
- `"The Hands"` → Use **"Automation Engine (n8n)"** or **"MCP Adapters"** instead
- `"Semantic Microkernel"` → Use **"Application Core"** (ADR-001 rejects this term)

**When reading research:** Mentally translate old terms to canonical terms from `CANONICAL_TERMINOLOGY.md`

---

## Success Criteria

**Phase 1 (Infrastructure Deployment):** ✅ COMPLETE
- Observer operational (drift detection every 15 min)
- Memory Bank Watchdog (Git → Qdrant)
- Email Watcher (Gmail → Claude → Telegram)
- Pre-commit hooks + validation (44 tests passing)

**Phase 2 (Architectural Alignment):** 🔄 IN PROGRESS (~15%)
- ✅ Foundation docs complete (ADR-001, Terminology, Architecture, Metaphor)
- 🔄 Apply canonical terms to codebase
- 🔄 Add automated enforcement (Vale linter)

**Phase 3 (Real-World Automation):**
- Choose 1-2 life flows for AI OS ownership
- Email automation complete (already started in Phase 1)
- Calendar management automation
- Task integration with Life Graph

**Phase 4 (Autonomy & Self-Improvement):**
- Meta-learning loops operational
- System autonomously improves based on patterns
- Minimal human intervention required

---

**Last Updated:** 2025-12-04  
**Current Phase:** Phase 2 (Architectural Alignment)  
**Active Slice:** Just completed Slice 2.0 (Foundation docs - ADR-001, Canonical Terminology, Architecture Reference, Metaphor Guide)
