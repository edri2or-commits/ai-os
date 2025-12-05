# AI Life OS - System Book

> Personal AI Operating System: Agentic Kernel for ADHD-aware productivity.  
> Autonomous life management through intelligent orchestration of Claude Desktop + MCP servers + n8n workflows + Git Truth Layer.

**Version:** Phase 1 (~85% complete) | **Platform:** Windows 11 + Claude Desktop  
**Owner:** Or (edri2or@gmail.com) | **Repo:** [github.com/edri2or-commits/ai-os](https://github.com/edri2or-commits/ai-os)

---

## 🎯 Quick Context Injection (< 500 tokens)

### What
An **autonomous AI operating system** that manages life, work, and bureaucracy through intelligent automation. Designed as a **Prosthetic Executive Cortex** for ADHD—offloading executive function to machines while maintaining human sovereignty.

### Architecture (C4 Context)
```
Or (Human) → Strategic Intent + Approval Gates
    ↓
Claude Desktop (Head) → Reasoning, Planning, Orchestration
    ↓ MCP Protocol (stdio)
MCP Servers (Hands) → Filesystem, Git, Google, Desktop Commander
    ↓
Truth Layer (Git-backed) → Life Graph YAML, System State JSON
    ↓
Automation (n8n + Qdrant) → Email classification, Memory indexing, Drift detection
```

### Core Workflow
**Chat → Spec → Change** | Human-in-the-loop at decision points | All changes reversible (Git safety net)

### Current State
- **Phase:** Phase 1 - Infrastructure Deployment (65% complete)
- **Operational:** Observer (drift detection), Validator (schema checks), Reconciler (CR management), Email Watcher (Gmail → Claude → Telegram), Memory Bank Watchdog (Git → Qdrant)
- **Running 24/7:** 3 automated processes via Windows Task Scheduler (every 15 min)
- **Testing:** 44 pytest tests passing
- **Next:** Gmail cleanup → Phase 2 (Real-world automation)

### Key Constraints
- **Safety:** Archive > delete, Git rollback always available
- **ADHD-aware:** Small slices (30-60 min), low friction, few clear options
- **Truth-First:** Git-backed files = single source of truth (never chat memory alone)
- **Research-backed:** Decisions cite sources or marked [PROPOSAL]

---

## 🗺️ System Book Structure

### 🔴 Essential (Start Here - New LLMs)

**For External LLMs (GPT, Gemini, etc.):**
1. [`memory-bank/START_HERE.md`](memory-bank/START_HERE.md) - Navigation index + onboarding checklist
2. [`memory-bank/project-brief.md`](memory-bank/project-brief.md) - Vision, requirements, success criteria (TL;DR: 20 seconds)
3. [`memory-bank/01-active-context.md`](memory-bank/01-active-context.md) - **GROUND TRUTH** (current phase, recent work, next steps)

**For Claude (This Session):**
You already have full context via Project Knowledge. Continue working per Memory Bank protocols.

---

### 📚 Operational Protocols

**Core Workflow:**
- [`memory-bank/protocols/MAP-001.md`](memory-bank/protocols/MAP-001.md) - Memory Bank Access Protocol v2.0
- [`memory-bank/protocols/AEP-001.md`](memory-bank/protocols/AEP-001.md) - ADHD-Aware Execution Protocol v2.0
- [`memory-bank/protocols/TSP-001.md`](memory-bank/protocols/TSP-001.md) - Tool Strategy Protocol v2.0
- [`memory-bank/protocols/SVP-001.md`](memory-bank/protocols/SVP-001.md) - Self-Validation Protocol v2.0
- [`memory-bank/protocols/TFP-001.md`](memory-bank/protocols/TFP-001.md) - Truth-First Protocol v2.0 (SEARCH FIRST, WRITE SECOND)

**Meta-Process:**
- **Protocol 1:** Post-Slice Reflection (auto-run after every slice)
  - Update Memory Bank
  - Detect meta-learning triggers (AP/BP/TD/incidents)
  - Git commit changes
  - **DO NOT ASK** - just do it automatically

---

### 🧠 Architectural Knowledge

**Theory & Design:**
- [`memory-bank/00_The_Sovereign_AI_Manifesto.md`](memory-bank/00_The_Sovereign_AI_Manifesto.md) - **WHY this system exists** (4 Core Principles + ADHD justification)
- [`docs/ATTENTION_CENTRIC_DESIGN.md`](docs/ATTENTION_CENTRIC_DESIGN.md) - **HOW to build ADHD-friendly interfaces** (5 Core Patterns + Visual Grammar)
- [`memory-bank/docs/decisions/`](memory-bank/docs/decisions/) - **Architecture Decision Records (ADRs)** - WHY specific tech choices

**Implementation:**
- [`docs/ARCHITECTURE_METAPHOR.md`](docs/ARCHITECTURE_METAPHOR.md) - Head/Hands/Truth/Nerves (canonical model)
- [`memory-bank/docs/LIFE_GRAPH_SCHEMA.md`](memory-bank/docs/LIFE_GRAPH_SCHEMA.md) - 6 entities (Area/Project/Task/Context/Identity/Log) + relationships
- [`memory-bank/02-progress.md`](memory-bank/02-progress.md) - Full chronological history (all slices)

**Research Corpus (18 files, 7 families):**
- Location: `claude-project/research_claude/`
- Families: Architecture, Claude/MCP/Tools, Cognition/ADHD, Infrastructure, Safety/Governance, Memory/RAG, Meta-process
- **Don't read all upfront** - reference as needed per domain

---

### 🔒 Safety & Governance

**Security:**
- Launcher Pattern (1Password CLI → ephemeral secrets)
- MCP sandboxing (filesystem scoped to ai-os directory only)
- N8N_BLOCK_ENV_ACCESS=true (no env variable leakage)
- Git pre-commit hooks (Gitleaks for secret scanning)

**Governance:**
- DEC (Decision Log) + EVT (Event Timeline)
- Fitness Metrics: FITNESS_001 (Friction), FITNESS_002 (CCI), FITNESS_003 (Drift)
- Incident Response Protocol (5 Whys analysis)

**Anti-Patterns (AP-XXX):**
Documented in `memory-bank/anti-patterns/` when detected via Meta-Learning Triggers

**Technical Debt (TD-XXX):**
Tracked in `memory-bank/technical-debt/` with priority/impact/resolution

---

## 🏗️ Core Architecture (C4 Level 1)

### Components

**Head (Reasoning Layer):**
- **Claude Desktop** - Semantic CPU, intent decomposition, tool orchestration
- Context window: 200K tokens
- Role: Planning, error handling, human communication

**Hands (Execution Layer):**
- **n8n** (Docker, localhost:5678) - Workflow automation, API integrations, scheduled tasks
- **Qdrant** (Docker, localhost:6333) - Vector database for semantic search
- 3 automated processes (Windows Task Scheduler, every 15 min):
  - Observer (drift detection)
  - Memory Bank Watchdog (Git → embeddings)
  - Email Watcher (Gmail → Claude classification → Telegram)

**Truth (Memory Layer):**
- **Git-backed filesystem** - Single source of truth
- Locations:
  - `life-graph/` - YAML entities (Areas, Projects, Tasks, etc.)
  - `truth-layer/drift/` - Change Requests (CR-*.yaml)
  - `memory-bank/` - PARA structure (Projects, Areas, Resources, Archives)
  - `docs/system_state/` - SYSTEM_STATE_COMPACT.json, snapshots, events

**Nerves (Interface Layer):**
- **MCP Servers** (Model Context Protocol):
  - `Desktop Commander` - Subprocess management, Python REPLs, shell execution, file operations
  - `google-mcp` (port 8082) - Gmail, Calendar, Drive, Tasks
  - Future: `mcp_github_client`, `os_core_mcp`, `agent_kernel`

---

## 📊 Capability Registry

### Active Tools (MCP Servers)

| Tool | Type | Scope | Operations | Status |
|------|------|-------|------------|--------|
| Desktop Commander | MCP | `ai-os` directory | read, write, subprocess, search | ✅ Active |
| google-mcp | MCP | Gmail, Calendar, Drive, Tasks | read, write, send, create | ✅ Active |
| Filesystem | Built-in | Project Knowledge | read only | ✅ Active |

### Automated Workflows (n8n)

| Workflow | Trigger | Status | Description |
|----------|---------|--------|-------------|
| Observer | Every 15 min | ✅ Running | Detects Git HEAD changes, schema violations, orphaned entities, staleness |
| Memory Bank Watchdog | Every 15 min (offset +7) | ✅ Running | Parses Memory Bank → generates embeddings → indexes to Qdrant |
| Email Watcher | Every 15 min (offset +10) | ✅ Running | Monitors Gmail unread → Claude classification → YAML drift report → Telegram urgent alerts |

**Test Results:**
- Email Watcher: 50 emails processed → 10 classified → 5 urgent alerts sent
- Observer: 6 drift categories monitored (Git HEAD, schema, orphans, timestamps, manual changes, CR staleness)

### Validation Infrastructure

- **pytest:** 44 tests passing
  - Life Graph schema validation
  - Observer drift detection
  - Reconciler CR application
  - Utility functions
- **Pre-commit hooks:** Gitleaks (secret scanning), ruff (Python linting)
- **Git safety:** All changes committed with detailed messages, reversible via `git revert`

---

## 🎓 How to Use This System Book

### If You Are Claude (This Session)
**You already have full context via Project Knowledge.**
- Continue working within Memory Bank protocols
- Follow Chat→Spec→Change workflow
- Auto-update Memory Bank after every slice (Protocol 1)
- Reference research files as needed (don't read all upfront)

---

### If You Are GPT / External LLM
**Welcome! Here's how to get productive in < 2 minutes:**

#### Step 1: Read Core Context (< 90 seconds)
1. [`memory-bank/START_HERE.md`](memory-bank/START_HERE.md) - Navigation + onboarding checklist
2. [`memory-bank/project-brief.md`](memory-bank/project-brief.md) - Vision, requirements (TL;DR: 20 sec)
3. [`memory-bank/01-active-context.md`](memory-bank/01-active-context.md) - **Most important** (current phase, recent work, next steps)

#### Step 2: Understand the Workflow
- **Chat:** Clarify intent, explore options (Hebrew responses, English thinking)
- **Spec:** Write structured proposal (Goal, Inputs, Outputs, Safety notes, Research citations)
- **Change:** Execute only after Or's explicit approval

#### Step 3: Know the Rules
- **Language:** Respond in Hebrew, think in English (unless Or asks for English)
- **ADHD-aware:** Small slices (30-60 min max), few clear options (2-3), low friction
- **Truth-First:** Read START_HERE + project-brief + 01-active-context BEFORE starting work
- **Safety:** Archive > delete, Git rollback always available, get approval for High-Impact Actions
- **Research-backed:** Cite sources (URL, date, quote) or mark [PROPOSAL]

#### Step 4: Summarize Before Working
**Before doing ANY work, tell Or in Hebrew:**
```
היי! קראתי את Memory Bank.

📍 איפה אנחנו:
- Phase X: [name] (~Y% complete)
- סיימנו לאחרונה: [from Recent Changes]
- הבא: [from Next Steps]

🎯 אפשרויות להמשך:
1. [Option A]
2. [Option B]
3. [Option C]

מה תרצה לעשות?
```

#### Step 5: Work Iteratively
- Propose 1-3 concrete next actions
- Get approval before executing
- Update Memory Bank after completion
- Use visual markers: ✅ (done), ❌ (blocked), ⚠️ (warning), 🔴 (critical)

**Key Principle:** You're a **consultant + executor**, not just a chatbot. Take ownership, but respect the human-in-the-loop gates.

---

### If You Are a Future AI Agent
**Welcome to the system. Here's your integration guide:**

#### Query Interface
- **Semantic search:** Use Qdrant (localhost:6333) for Memory Bank queries
- **File search:** Use Desktop Commander's search_files for filesystem
- **Git history:** Use Desktop Commander's subprocess for `git log`

#### Contribution Protocol
- **After every task:** Run Protocol 1 (Post-Slice Reflection)
  - Update `memory-bank/01-active-context.md`
  - Append to `memory-bank/02-progress.md`
  - Detect meta-learning triggers (AP/BP/TD/incidents)
  - Git commit with detailed message

#### Learning Protocol
- **Meta-Learning Triggers:** See Memory Bank Playbook Section 9
  - Trigger A: Repetition (2nd+ occurrence) → propose AP-XXX
  - Trigger B: Workaround used → propose TD-XXX
  - Trigger C: User surprise → check spec clarity
  - Trigger D: Research gap (3+ "not sure") → propose research slice
  - Trigger E: Friction point → propose automation
  - Trigger F: Protocol created → apply it immediately (self-activation)

#### Safety Constraints
- **NEVER** auto-apply changes to Git main branch without approval
- **ALWAYS** create drift reports before reconciliation
- **Filesystem scope:** Limited to `ai-os` directory only (Windows: `C:\Users\edri2\Desktop\AI\ai-os`)
- **N8N sandbox:** `N8N_BLOCK_ENV_ACCESS=true` (no env leakage)

---

## 📈 System State (Live)

### Infrastructure Health

**Docker Services:**
- n8n v1.122.4 (port 5678) - ✅ Running
- Qdrant v1.16.1 (port 6333) - ✅ Running
- Docker Desktop - ✅ Auto-start enabled

**Windows Task Scheduler:**
- Observer - ✅ Every 15 min
- Memory Bank Watchdog - ✅ Every 15 min (offset +7)
- Email Watcher - ✅ Every 15 min (offset +10)

**Validation:**
- pytest: 44/44 tests passing ✅
- Pre-commit hooks: Active ✅
- Git: Clean working tree ✅

### Current Phase Status

**Phase 1: Infrastructure Deployment**
- Progress: ~65% complete (7/8 slices done)
- Blockers: NONE
- Next: Gmail cleanup (15 min) → Close Phase 1

### Key Metrics

**Fitness Scores:**
- FITNESS_001 (Friction): TBD (Phase 2)
- FITNESS_002 (CCI - Closure/Checkpoint Interval): TBD (Phase 2)
- FITNESS_003 (Drift): Monitored 24/7 by Observer

**Activity:**
- Total Slices: ~25 completed
- Automation Coverage: Email ✅ | Calendar ⏳ | Tasks ⏳ | Drive ⏳
- Documentation: Memory Bank (10 protocols v2.0), Research (18 files)

**Recent Achievement:**
Slice 2.5: CLP-001 Integration Plan (2025-12-04)

(Auto-synced from 01-active-context.md via sync_system_book.py)

---

## 🔄 Maintenance & Updates

### Auto-Update Mechanisms

This file is **partially auto-updated** by:
- **Protocol 1** (Post-Slice Reflection) - Updates "Recent Achievement" section
- **Observer** (via n8n) - Updates "Docker Services" health status
- **Git pre-commit hooks** - Validates all internal links

**Manual updates required for:**
- Architecture changes (notify Or)
- New MCP servers added
- Phase transitions

### Changelog

**Major Updates:**
- 2025-12-03: Email Watcher deployed (Gmail → Claude → Telegram)
- 2025-12-03: All protocols upgraded to v2.0 (research-backed)
- 2025-12-03: n8n + Qdrant 24/7 deployment
- 2025-12-01: Observer + Watchdog + Task Scheduler automation

**Full History:** See [`memory-bank/02-progress.md`](memory-bank/02-progress.md)

---

## 📚 External Standards Referenced

This System Book follows industry best practices:

- **[llms.txt](https://llmstxt.org/)** - Markdown structure for AI agents (Jeremy Howard, 2024)
- **[C4 Model](https://c4model.com/)** - Architecture diagrams (Simon Brown)
- **[Arc42](https://arc42.org/)** - Documentation template
- **[ADR](https://adr.github.io/)** - Architectural Decision Records
- **[PARA](https://fortelabs.com/blog/para/)** - Knowledge organization (Tiago Forte)
- **MCP** - Model Context Protocol (Anthropic)

**Context Engineering Research:**
- Andrej Karpathy: "Context engineering is the delicate art and science of filling the context window with just the right information"
- LangChain Framework: Write/Select/Compress/Isolate strategies
- Anthropic: Effective context engineering for AI agents

---

## 🆘 Troubleshooting

### Common Issues

**"I can't find X in Memory Bank"**
- Use Qdrant semantic search: `http://localhost:6333` (if running)
- Or grep through `memory-bank/`: Use Desktop Commander's search_files
- Or check START_HERE.md navigation index

**"Where is the current state?"**
- **Always:** `memory-bank/01-active-context.md` (ground truth)
- Never: Chat history (not reliable)
- Never: Assumptions (always verify)

**"Should I update Memory Bank?"**
- **Don't ask** - Protocol 1 says update automatically after every slice
- If unsure, read Protocol 1 in Memory Bank

**"Can I [destructive action]?"**
- Archive > delete (always)
- Get approval before: deleting files, sending emails, committing to Git main
- Test in sandbox first

### Emergency Contacts

**Human:** Or (edri2or@gmail.com)  
**Telegram:** (Urgent alerts already configured via Email Watcher)  
**Repository:** [github.com/edri2or-commits/ai-os](https://github.com/edri2or-commits/ai-os)

---

## 🎉 Quick Wins (For External LLMs)

**Want to contribute something valuable in < 15 minutes?**

1. **Review 01-active-context.md** → Suggest next 2-3 concrete actions
2. **Analyze a research file** → Extract 3 actionable insights
3. **Propose a BP (Best Practice)** → Based on recent success patterns
4. **Identify an AP (Anti-Pattern)** → From recent friction points
5. **Suggest automation** → For repetitive manual tasks

**Template for contribution:**
```markdown
## [Contribution Type]: [Title]

**Context:** [From 01-active-context.md]
**Observation:** [What you noticed]
**Proposal:** [Specific, actionable suggestion]
**Expected Impact:** [Time saved / Friction reduced / Quality improved]
**Risk:** [Low/Medium/High + mitigation]

**Research Support:** [Cite sources or mark [PROPOSAL]]
```

---

**End of System Book**

**Last Updated:** 2025-12-03  
**Version:** 1.0.0  
**Maintained By:** Claude (Protocol 1) + Or (Manual sections)

---

**For questions, suggestions, or contributions:**  
Open an issue at [github.com/edri2or-commits/ai-os/issues](https://github.com/edri2or-commits/ai-os/issues)
