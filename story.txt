# AI Life OS: The Complete Story

**Last Updated:** 2025-12-06  
**Status:** Phase 2 (~78% Complete) | Production Infrastructure Operational  
**Purpose:** Single canonical source for "What is AI Life OS?"

---

## 🎯 30 Seconds (Elevator Pitch)

**AI Life OS** is a personal AI operating system designed as a **cognitive prosthetic** for ADHD. It's not a chatbot—it's a 24/7 autonomous system that:

- **Remembers for you** (external working memory)
- **Organizes for you** (executive function offload)
- **Learns from mistakes** (self-improving automation)
- **Defends your attention** (batched interruptions, quiet reliability)
- **Runs locally** (privacy-first, Git-backed, fully reversible)

**Built with:** Claude Desktop (reasoning) + MCP servers (tools) + n8n (automation) + Git (truth layer) + Qdrant (vector memory)

**Currently operational:** Observer (drift detection), Reconciler (change management), Judge Agent (error detection), Email automation, Telegram notifications, 44/44 tests passing.

**Next milestone:** VPS deployment (24/7 uptime) + multi-model orchestration (GPT/Claude/o1).

---

## 📖 2 Minutes (What/Why/How)

### What Is This?

AI Life OS is a **personal infrastructure layer** that sits between you and your digital life. Think of it as:

- **Cognitive prosthetic:** Compensates for ADHD executive function deficits
- **Autonomous agent:** Runs 24/7, monitors your systems, learns from patterns
- **Privacy-first:** All data local (Git repository), no cloud dependencies
- **Self-healing:** Detects drift, proposes fixes, learns from errors

### Why Does It Exist?

**ADHD is a performance disorder** with 4 core deficits:
1. **Working memory failure:** "Out of sight, out of mind" (object permanence)
2. **Initiation paralysis:** High activation energy for tasks
3. **Context switching cost:** 10-25 minutes to recover from interruptions
4. **Time blindness:** "Now" vs "Not Now" (no middle ground)

**Traditional productivity systems fail** because they assume:
- ✅ You remember tasks without prompts
- ✅ You can estimate time accurately
- ✅ You can prioritize rationally
- ✅ You can start tasks without friction

**ADHD brains need:**
- 🧠 External working memory (Git + Qdrant)
- 🧠 Ambient awareness (Observer + Dashboard)
- 🧠 Low activation energy (one-command execution)
- 🧠 Reversibility (Git undo for everything)

### How Does It Work?

**Architecture:** Hexagonal (Application Core + Ports + Adapters) + MAPE-K (Monitor-Analyze-Plan-Execute-Knowledge)

```
┌─────────────────────────────────────────────────┐
│ Application Core (Reasoning)                    │
│ Claude Desktop = reasoning head                 │
│ GPT/o1 = strategic advisors                     │
│ Or = product owner (final approvals)            │
├─────────────────────────────────────────────────┤
│ Ports & Adapters (Integration)                  │
│ MCP Servers = standardized tool interfaces      │
│ Desktop Commander, Google MCP, etc.             │
├─────────────────────────────────────────────────┤
│ Infrastructure (Execution)                      │
│ n8n = automation workflows                      │
│ Qdrant = vector memory                          │
│ Git = truth layer (immutable audit trail)       │
│ Docker = service isolation                      │
└─────────────────────────────────────────────────┘
```

**MAPE-K Loop (Autonomous Operation):**

1. **Monitor:** Observer checks system state every 15 minutes (Git HEAD, schema violations, orphaned files)
2. **Analyze:** Reconciler compares observed state vs. desired state (drift detection)
3. **Plan:** Generate Change Requests (CRs) with rollback plans
4. **Execute:** Apply approved CRs (Git commits, file updates)
5. **Knowledge:** Judge Agent learns from errors → LHO database → prevents recurrence

**Self-Learning Loop:**

```
Observer → EVENT_TIMELINE → Judge Agent (GPT-5.1)
    ↓
FauxPas Reports (4 types: Amnesia, Blindness, Loops, Hallucinations)
    ↓
[NEXT] Teacher Agent → Life Handling Objects (LHOs)
    ↓
Qdrant Vector DB → Librarian Agent → Context injection before tasks
```

---

## 🏗️ 5 Minutes (Current State + Recent Wins)

### What's Operational Right Now (2025-12-06)

**Phase 2: Architectural Alignment & Governance** (~78% complete)

#### Infrastructure (100% operational ✅)
- **Desktop Commander MCP:** Windows automation, subprocess management
- **Observer:** Runs every 15 min (Task Scheduler), detects drift
- **Reconciler:** Applies Change Requests with safety checks
- **Validator:** 44/44 pytest tests passing (zero warnings)
- **n8n v1.122.4:** Automation platform (24/7 Docker)
- **Qdrant v1.16.1:** Vector database (24/7 Docker)
- **Langfuse V3:** Professional telemetry (6/6 services healthy)
- **Docker Desktop:** Auto-start on boot configured

#### Automation (3 processes, 24/7) ✅
1. **Observer:** Drift detection (Git HEAD, schema violations)
2. **Memory Bank Watchdog:** Auto-indexes Markdown → Qdrant
3. **Email Watcher:** Gmail monitoring → Claude classification → Telegram alerts

#### Recent Wins (Last 48 Hours) 🎉

**H3: Telegram Approval Bot** (2025-12-06 13:27 UTC - TESTED!)
- **Achievement:** Async HITL via Telegram (no Claude Desktop required)
- **Test:** CR detected (5s) → Telegram sent ✅ → User approved ✅ → DB updated ✅
- **Impact:** Headless approvals, ADHD-friendly (approve from phone), VPS-ready

**H2: Memory Bank REST API** (2025-12-06 01:30 UTC)
- **Achievement:** External LLMs (GPT, o1, Gemini) load context < 30 seconds
- **Test:** Fresh GPT conversation → API call → accurate answers ✅
- **Impact:** Multi-model freedom, zero "artificial amnesia"

**H1: Gmail MCP Gateway** (2025-12-06 00:50 UTC)
- **Achievement:** GPT sends Gmail without Claude Desktop (headless proof)
- **Test:** Python → HTTP POST → Gmail API → Email delivered ✅
- **Impact:** Multi-model orchestration validated

**Judge Agent V2 + Langfuse** (2025-12-05)
- **Achievement:** Automated error detection operational
- **Test:** 44/44 tests passing, GPT-4o integrated, FauxPas reports generated
- **Gap Identified:** Judge can't see conversation transcripts yet (fix planned)

### What's Next (3 Clear Options)

**Option 1: H4 - VPS Deployment** 🌐 (4-6h, $16/mo)
- Deploy headless core to Hetzner Cloud VPS
- True 24/7 uptime (PC-independent)
- Multi-model routing (40% cost savings potential)

**Option 2: Judge V2 Enhancement** 👨‍⚖️ (60 min)
- Connect Judge to Langfuse (see conversation context)
- Protocol 1 auto-logging (every slice → trace)
- Result: Judge sees "what you asked" + "what Claude did" + "outcome"

**Option 3: Teacher Agent** 🧑‍🏫 (90 min)
- Convert FauxPas reports → Life Handling Objects (LHOs)
- Store in Qdrant (vector search)
- Enable "just-in-time learning" (system reads lessons before tasks)

---

## 🧠 10 Minutes (Architecture + Philosophy)

### The 4 Core Principles (Manifesto)

#### I. Cognitive Sovereignty
> "My thoughts, my data, and my inference are extensions of my mind."

**Implementation:**
- **Local-First:** Truth Layer resides on hardware you control (C:\Users\...\ai-os)
- **Memory Independence:** Qdrant vectors + Git history = portable, interoperable, yours
- **Model Agnosticism:** Swap LLMs freely (Claude, GPT, o1, Gemini) via REST APIs

**ADHD Relevance:** No network-induced anxiety, offline capability, object permanence via visible files

#### II. Attention Defense
> "The system serves my focus, not the engagement metrics of others."

**Implementation:**
- **Quiet by Design:** Batch notifications (Daily Standup via Telegram)
- **Interruption as Failure:** Context switching minimized (15-min Observer cycles)
- **Visual Calm:** Text-first, no spinners, no dark patterns

**ADHD Relevance:** Flow state is precious (20-min recovery from interruptions), notification fatigue eliminated

#### III. Executive Prosthesis
> "The AI is the scaffold, not the builder."

**Implementation:**
- **Externalize Everything:** Git captures every thought/task/decision immediately
- **Point of Performance:** Assistance provided when/where problem occurs
- **Transparent Reasoning:** Audit chain-of-thought, inspect tool calls, verify data

**ADHD Relevance:** Working memory is porous (Barkley: "performance deficit at point of performance"), external structure compensates

#### IV. The Gardener
> "I cultivate my system; I do not just consume it."

**Implementation:**
- **Small, Sharp Tools:** Composable MCP servers (not monolithic super-app)
- **Evolutionary Resilience:** Plain text (Markdown/JSON), standard protocols (Git/HTTP)
- **Human in the Loop:** Critical decisions require explicit approval (HITL gates)

**ADHD Relevance:** Complexity is the enemy, modularity allows gradual adoption, "forever tools" reduce relearning anxiety

### Hexagonal Architecture (Canonical)

**Why Hexagonal?** (ADR-001, 2025-12-04)

Traditional layered architecture creates **vendor lock-in**:
```
UI → Business Logic → Database
(tight coupling = fragile)
```

**Hexagonal separates concerns:**
```
       ┌──────────────────────────┐
       │  Application Core        │
       │  (Business Logic)        │
       │  - Life Graph entities   │
       │  - Drift detection rules │
       │  - ADHD-aware patterns   │
       └──────────────────────────┘
                  ↕ Ports (interfaces)
       ┌──────────────────────────┐
       │  Adapters (Implementations) │
       │  - MCP: Desktop Commander │
       │  - MCP: Google Workspace  │
       │  - n8n workflows          │
       │  - Git operations         │
       └──────────────────────────┘
```

**Benefits:**
1. **Testability:** Mock adapters in tests (fast, isolated)
2. **Flexibility:** Swap MCP servers without touching core logic
3. **Maintainability:** Changes in one adapter don't cascade
4. **Multi-Model:** Claude/GPT/o1 = different adapters, same core

### MAPE-K Loop (Autonomic Computing)

**Why MAPE-K?** Industry standard for self-managing systems (IBM, 2003)

```
Monitor → Analyze → Plan → Execute
    ↑                        ↓
    └────── Knowledge ←──────┘
```

**AI Life OS Implementation:**

| MAPE-K Phase | Component | Frequency | Output |
|--------------|-----------|-----------|--------|
| **Monitor** | Observer | Every 15 min | OBSERVED_STATE.json |
| **Analyze** | Reconciler | On drift | Change Requests (CRs) |
| **Plan** | n8n workflows | On CR approval | Execution plan |
| **Execute** | Desktop Commander | Atomic operations | Git commit |
| **Knowledge** | Judge → LHOs | Every 6 hours | FauxPas → Lessons learned |

**Self-Learning Extension (Meta-MAPE-K):**
- **Fast Loop:** Observer → Reconciler (tactical, 15-min cycle)
- **Slow Loop:** Judge → Teacher → Librarian (strategic, 6-hour cycle)

### Life Graph (Data Model)

**7 Entity Types (ADHD-Optimized Schema):**

1. **Area:** Life domain (Career, Health, Relationships)
2. **Project:** Time-bounded goal (6 months max, ADHD attention span)
3. **Task:** Atomic action (30-60 min, one sitting)
4. **Context:** Required state (location, tools, energy level)
5. **Log:** Daily journal entry (what happened today)
6. **Event:** System occurrence (drift detected, CR applied)
7. **Note:** Standalone thought (captured immediately)

**ADHD Fields (every entity):**
- `energy_profile`: "low" | "medium" | "high" (match task to energy)
- `dopamine_level`: 1-10 (prioritize rewarding tasks first)
- `is_frog`: boolean ("eat the frog" - do hard thing first)
- `do_date`: YYYY-MM-DD (deadline, not "someday")

**Why Git-Backed?**
- **Immutable audit trail:** Every change is commit (rollback anytime)
- **Visual diff:** See what changed (`git diff`)
- **Branching:** Experiment safely (`git checkout -b experiment`)
- **Remote backup:** GitHub/GitLab (disaster recovery)

