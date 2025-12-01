# Target Architecture Summary – Personal AI Life OS

**Purpose:** Comprehensive architecture specification derived from 29 research files  
**Methodology:** Clustering research into 6 families + extracting design principles  
**Approach:** Distinguish EXPLICIT (stated in docs) from PROPOSAL (inferred/design choice)  

---

## Document Structure

This document organizes the target architecture into **6 Research Families**:

1. **Architecture / Kernel / OS Design**
2. **Tools & MCP / Claude Desktop Role**
3. **ADHD / Cognitive Ergonomics / Governance**
4. **Infrastructure (Windows / WSL / Docker / n8n)**
5. **Safety / Drift / HITL / Circuit Breakers**
6. **Memory / Life Graph / RAG / Truth Layer**

Each family includes:
- Key architectural decisions (5-10 bullets)
- Supporting research files
- Distinction: **[EXPLICIT]** vs. **[PROPOSAL]**

---

## Core Design Principles (Cross-Cutting)

These 7 principles apply across all families:

1. **Truth Layer First** – Never rely only on conversation memory for system facts
2. **Chat → Spec → Change** – Cognitive pause before execution (ADHD-aware)
3. **Executive Function Prosthetic** – System compensates for ADHD executive dysfunction
4. **Local-First, Git-Backed** – Privacy + infinite rollback
5. **Prevention < Recovery** – Make mistakes reversible, not impossible
6. **Deterministic Hands** – n8n/automations execute, Claude plans
7. **Proactive Monitoring** – Observed State + Drift Detection

**Sources:**
- 06_2025-personal-ai-operating-system_architectural-review.md
- 11_cognitive_technical_symbiosis_personal_ai_life_os.md
- ai-life-os-claude-project-playbook.md

---

## Family 1: Architecture / Kernel / OS Design

### 1.0 Canonical Architecture Model **[CANONICAL]**

**FOR AUTHORITATIVE REFERENCE:** See `CANONICAL_ARCHITECTURE.md` (created 2025-11-30)

**Hexagonal Architecture (Core / Ports / Adapters):**

| Component | Role | Type |
|-----------|------|------|
| **Git-backed Truth Layer** | Single source of truth (entire repo) | **Core** |
| **MCP servers** | Standardized interfaces (filesystem, git, GitHub, Google, n8n, os_core) | **Ports** |
| **Claude Desktop** | Primary reasoning orchestrator (current) | **Adapter** |
| **ChatGPT/Gemini/Telegram/CLI** | Future reasoning orchestrators | **Adapters (future)** |
| **n8n** | Autonomous scheduled execution through Ports | **Port (scheduler)** |

**Key Invariants:**
1. Core = Git repo (no state fragmentation)
2. All state changes via Ports or documented bridges (TD-XXX)
3. Adapters are replaceable (model-agnostic)
4. Ports are stateless (state lives in Core)
5. Adapters are REACTIVE, n8n is autonomous
6. Git as infinite undo (all changes tracked)

**Previous Metaphors Superseded:**
- "Claude = CPU" → "Claude = Adapter" (replaceable)
- "MCP = Bus" → "MCP = Ports" (standardized interfaces)
- See CANONICAL_ARCHITECTURE.md for full contradiction resolution

---

### 1.1 Semantic Microkernel Architecture **[EXPLICIT - Historical Context]**

**NOTE:** This section preserved for historical context. For canonical model, see section 1.0 and CANONICAL_ARCHITECTURE.md.

**Original Metaphor:** Operating System for Personal AI

| Component | OS Metaphor (Legacy) | Role |
|-----------|---------------------|------|
| Claude Desktop | ~~CPU~~ → Adapter | Probabilistic processor, reasoning engine |
| MCP Servers | ~~Bus/I/O~~ → Ports | Standardized interfaces to external systems |
| Files + Git | Memory → Core | Persistent state, version control |
| Truth Layer | ~~RAM~~ → Core | Current system state |
| n8n | Scheduler → Port | Temporal/scheduled tasks |

**Key Decision:**
> "The kernel schedules attention and intent, not CPU cycles"

**Principle:** Claude = reactive processor (not autonomous agent running in background)

**Sources:**
- 01_architectural-blueprint_phase-3-ai-os.md
- 06_2025-personal-ai-operating-system_architectural-review.md
- 09_agentic_kernel_claude_desktop_mcp.md

---

### 1.2 Chat → Spec → Change Workflow **[EXPLICIT]**

**Three-phase pattern designed for ADHD:**

1. **Chat** (Zero Friction)
   - Natural language, conversational
   - No upfront structure required
   - Clarifying questions, not forms

2. **Spec** (Cognitive Pause)
   - Structured plan before execution
   - Goal, Inputs, Outputs, Risks
   - Which research families support it
   - **HITL approval gate here**

3. **Change** (Deterministic Execution)
   - Only after spec approval
   - Via tools (MCP, n8n)
   - Git-backed (reversible)

**Why this matters:**
- **Chat phase** = low activation energy (ADHD-friendly)
- **Spec phase** = prevents impulsive execution
- **Change phase** = deterministic, traceable

**Sources:**
- 10_claude_desktop_agentic_kernel_playbook_windows.md
- 11_cognitive_technical_symbiosis_personal_ai_life_os.md
- ai-life-os-claude-project-playbook.md

---

### 1.3 Truth Layer = Git-Backed Markdown/YAML **[EXPLICIT]**

**Design Decision:** 
- **Not** a database
- **Not** a vector store (for structure)
- **Yes** Git-backed plaintext

**Format:**
- Markdown for human readability
- YAML frontmatter for metadata
- JSONL for append-only logs (EVENT_TIMELINE)
- JSON for snapshots (SYSTEM_STATE, GOVERNANCE)

**Why Markdown:**
- Human-readable (LLM-native)
- Git-diffable
- Tool ecosystem (Obsidian, Logseq, VS Code)
- No proprietary lock-in

**Structure (PARA-inspired):**
```
00_Inbox/          # Unsorted capture
10_Projects/       # Active projects
20_Areas/          # Life areas
30_Resources/      # Reference materials
99_Archive/        # Completed/inactive
```

**Sources:**
- 01_architectural-blueprint_phase-3-ai-os.md
- 04_personal-ai-life-os_implementation-strategy.md
- 06_2025-personal-ai-operating-system_architectural-review.md
- 12.md (Life Graph schema)

---

### 1.4 Supervisor-Worker (Hub-and-Spoke) Architecture **[EXPLICIT]**

**Pattern:**
- **Claude Desktop** = Supervisor (central orchestrator)
- **MCP Servers** = Workers (specialized tools)
- **n8n** = Scheduled Workers (temporal tasks)

**Not a mesh network:**
- Workers don't talk to each other
- All coordination through Claude
- Reduces complexity

**When to use LangGraph:**
- Only for multi-day HITL flows
- "Agentic Sleep" scenarios (user away for hours/days)
- Example: Daily Context Sync with human checkpoints

**Sources:**
- 09_agentic_kernel_claude_desktop_mcp.md
- msg_020.md (LangGraph discussion)
- ai-life-os-claude-project-playbook.md

---

### 1.5 Host-Agnostic Interface Layer **[PROPOSAL]**

**Future Goal:** Multiple chat interfaces

Current:
- Claude Desktop only

Future:
- Telegram bot
- ChatGPT client (via OpenAI API)
- Gemini client
- WhatsApp bot

**Constraint:**
- All interfaces talk to same Truth Layer
- No state fragmentation
- Unified Memory Bank

**Sources:**
- 04_personal-ai-life-os_implementation-strategy.md
- Architecting_Personal_AI_Life_OS.md

---

## Family 2: Tools & MCP / Claude Desktop Role

### 2.1 MCP = Universal Device Driver for AI **[EXPLICIT]**

**Model Context Protocol (MCP):**
- Standard interface for connecting Claude to external systems
- Like USB for operating systems
- Transport modes: stdio (local) vs. sse (remote)

**Available MCP Servers:**
- `filesystem` – Local file access
- `git` – Repository operations
- `n8n-mcp` – n8n integration
- `n8n-workflow-builder` – Workflow creation
- `docs-fetch` – Documentation retrieval
- Custom: GitHub, Google Workspace, OS Core

**Principle:**
> "MCP is the nervous system. Keep it strictly scoped and secured"

**Sources:**
- 09_agentic_kernel_claude_desktop_mcp.md
- 10_claude_desktop_agentic_kernel_playbook_windows.md

---

### 2.2 Context Window Management (200K tokens) **[EXPLICIT]**

**Challenge:** "Lost in the Middle" phenomenon

**Problem:**
- Claude has 200K token context
- But retrieval accuracy drops in middle of context
- Can't just dump all files into context

**Solution: RAG Strategy**
- Pull ONLY relevant context per query
- Use semantic search (vector DB)
- Combine with keyword search
- Structured retrieval (not dump-everything)

**Implementation:**
- LightRAG / GraphRAG for semantic search
- Qdrant / LanceDB for vector storage
- Hybrid search (semantic + keyword)

**Sources:**
- 09_agentic_kernel_claude_desktop_mcp.md
- 11_cognitive_technical_symbiosis_personal_ai_life_os.md

---

### 2.3 Claude Desktop is Reactive, Not Proactive **[EXPLICIT]**

**Critical Constraint:**
- Claude Desktop does NOT run in background
- Cannot autonomously execute tasks while user away
- User must initiate interaction

**Implications:**
- n8n handles scheduled/temporal tasks
- Claude handles reasoning/planning
- Separation of concerns: Planning (Claude) vs. Execution (n8n)

**Example:**
- ❌ Claude cannot "check email every hour"
- ✅ n8n checks email, Claude reasons about it when invoked

**Sources:**
- 09_agentic_kernel_claude_desktop_mcp.md
- 10_claude_desktop_agentic_kernel_playbook_windows.md

---

### 2.4 MCP Server Security Scope **[EXPLICIT]**

**Best Practice: Minimal Scope**

**Filesystem MCP:**
- Restrict to specific directories
- No root access
- Read/write permissions granular

**GitHub MCP:**
- Repo-specific tokens
- Branch protection
- No force-push rights

**Google MCP:**
- OAuth with minimal scopes
- Read-only by default
- Write requires explicit grants

**Principle:**
> "Trust but verify. MCP servers are privileged – scope them tightly"

**Sources:**
- 10_claude_desktop_agentic_kernel_playbook_windows.md
- 13.md (security playbook)

---

## Family 3: ADHD / Cognitive Ergonomics / Governance

### 3.1 ADHD Cognitive Profile **[EXPLICIT]**

**Documented Challenges:**

1. **Executive Function Deficit**
   - Difficulty planning multi-step tasks
   - Poor prioritization
   - Hard to initiate tasks (activation energy)

2. **Working Memory Weakness**
   - Ideas vanish immediately
   - Cannot hold multiple steps in mind
   - "Out of sight, out of mind"

3. **Time Blindness**
   - Cannot estimate task duration
   - Deadlines feel abstract
   - "do_date" vs. "due_date" distinction critical

4. **Decision Paralysis**
   - Overwhelmed by too many options
   - Prefers 2-3 clear choices
   - Progressive disclosure over comprehensive lists

5. **Wall of Awful**
   - Emotional barrier to starting tasks
   - Especially for boring/admin work
   - Need for "body doubling" (Claude as presence)

6. **Object Permanence Issues**
   - What's not visible doesn't exist
   - Need for high-salience notifications
   - Visual cues critical

**Sources:**
- 10_claude_desktop_agentic_kernel_playbook_windows.md
- 11_cognitive_technical_symbiosis_personal_ai_life_os.md
- 18.md (ADHD deep dive)

---

### 3.2 ADHD-Aware Design Patterns **[EXPLICIT]**

**Low Activation Energy:**
- Chat interface (not forms)
- No upfront structure
- "Just talk" as starting point

**Progressive Disclosure:**
- Start simple (1-3 options)
- Reveal complexity only when needed
- Avoid overwhelming with choices

**High Salience Notifications:**
- Visual cues for urgent items
- "is_frog" boolean (hardest task first)
- Color-coded priorities

**Chunking:**
- Break into 5-15 minute blocks
- Each block independently completable
- Dopamine hits for micro-completions

**Dopamine Menus:**
- Pre-approved low-energy tasks
- For when executive function is low
- "Energy-matched" task lists

**Energy Management > Time Management:**
- Tasks tagged by energy_profile: [high_focus, low_focus, creative, admin]
- Match task to current energy level
- Not "when to do" but "what energy state needed"

**Body Doubling:**
- Claude as virtual presence
- "Working alongside" mode
- Reduces activation barrier

**Fearless Experimentation:**
- Git rollback = infinite undo
- "Try anything, can always revert"
- Removes fear of breaking things

**Sources:**
- 11_cognitive_technical_symbiosis_personal_ai_life_os.md
- 18.md
- ai-life-os-claude-project-playbook.md

---

### 3.3 Chat → Spec → Change as ADHD Mitigation **[EXPLICIT]**

**Why this workflow:**

**Chat Phase:**
- Zero friction (ADHD-friendly start)
- No planning required upfront
- Natural language (low cognitive load)

**Spec Phase:**
- Forced cognitive pause
- Prevents impulsive execution
- Externalizes working memory (write it down)
- Human review before action

**Change Phase:**
- Deterministic (reduces anxiety)
- Git-backed (reversible)
- Traceable (clear audit trail)

**Principle:**
> "The system is an Executive Function Prosthetic"

**Sources:**
- 10_claude_desktop_agentic_kernel_playbook_windows.md
- 11_cognitive_technical_symbiosis_personal_ai_life_os.md

---

### 3.4 Governance = Fitness Metrics, Not Control **[EXPLICIT]**

**Not a permission system:**
- Governance ≠ "Can you do X?"
- Governance = "How well is the system working?"

**Three Fitness Metrics:**

**FITNESS_001: Friction** (Operational Overhead)
- open_gaps_count
- time_since_last_daily_context_sync
- recent_error_events_count

**FITNESS_002: CCI** (Cognitive Capacity Index)
- active_services_count / total_services_count
- recent_event_types_count (diversity)
- recent_work_blocks_count (momentum)
- pending_decisions_count (backlog)

**FITNESS_003: Tool Efficacy** (Planned)
- Success rates
- Retry patterns
- Execution times

**Sources:**
- 08_ai_os_current_state_snapshot.md
- governance/README.md (in repo)
- DEC-010 (Governance Truth Layer Bootstrap)

---

## Family 4: Infrastructure (Windows / WSL / Docker / n8n)

### 4.1 The Filesystem Chasm (Windows + WSL2) **[EXPLICIT]**

**Problem:**
- WSL2 = Linux kernel in Hyper-V VM
- Bind-mounting NTFS → Docker/Linux = terrible performance
- Permission issues (NTFS ↔ Linux mismatch)

**Solution: WSL2-Native Storage Strategy**

❌ **Don't:**
```
docker run -v C:\Users\...\data:/app/data
```

✅ **Do:**
```
docker run -v /home/user/wsl-data:/app/data
```

**Store data in WSL2 filesystem, not Windows NTFS**

**Sources:**
- 10_claude_desktop_agentic_kernel_playbook_windows.md
- msg_020.md (Windows infra deep dive)

---

### 4.2 The Networking Ambiguity (Docker on Windows) **[EXPLICIT]**

**Problem:**
- `localhost` inside container ≠ Windows host
- Container-to-container networking different from host access

**Solution:**
- Use `host.docker.internal` to reach Windows host from container
- Use Docker network names for container-to-container
- Port mapping: `-p 5678:5678` for external access

**Example:**
```yaml
# From n8n container, reach OS Core MCP on Windows
http://host.docker.internal:8083/state
```

**Sources:**
- 10_claude_desktop_agentic_kernel_playbook_windows.md
- infra/n8n/README.md (in repo)

---

### 4.3 n8n State Vulnerability (SQLite Default) **[EXPLICIT]**

**Problem:**
- n8n default = SQLite in ephemeral storage
- Container restart = **AMNESIA** (all workflows/credentials lost)

**Solution: Named Volumes or PostgreSQL**

**Option A: Named Volumes**
```yaml
volumes:
  - n8n-data:/home/node/.n8n
```

**Option B: PostgreSQL Container**
```yaml
environment:
  - DB_TYPE=postgresdb
  - DB_POSTGRESDB_HOST=postgres
```

**Critical:**
- `N8N_BLOCK_ENV_ACCESS_IN_NODE=true` (prevent credential dumping)

**Sources:**
- 10_claude_desktop_agentic_kernel_playbook_windows.md
- infra/n8n/docker-compose.yml (in repo)

---

### 4.4 Docker Best Practices for AI-OS **[EXPLICIT]**

**Custom Image:**
- Base: `n8nio/n8n:latest`
- Add: jq, curl, git, python (toolbelt)
- Reduces runtime installs

**Volume Mounts:**
- Data persistence (named volumes)
- Config injection (read-only mounts)

**Health Checks:**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5678/healthz"]
  interval: 30s
  timeout: 10s
  retries: 3
```

**Docker Scout:**
- Scan images for vulnerabilities
- Before deploying to "production"

**Sources:**
- 10_claude_desktop_agentic_kernel_playbook_windows.md

---

### 4.5 Local-First is Privacy, But Windows/WSL2 is Fragile **[EXPLICIT]**

**Principle:**
> "Local-first is privacy, but Windows/WSL2 is fragile. Plan for failure"

**Implications:**
- Backup strategy essential
- Git as source of truth (not just WSL2 files)
- Regular exports to Git
- Health checks for WSL2 state

**Backup Strategy:**
- Daily exports of Truth Layer → Git
- n8n workflow exports (version controlled)
- State snapshots to governance/

**Sources:**
- 10_claude_desktop_agentic_kernel_playbook_windows.md

---

## Family 5: Safety / Drift / HITL / Circuit Breakers

### 5.1 Drift = Split Brain Problem **[EXPLICIT]**

**Definition:**
- Drift = gap between system's belief (Truth Layer files) and reality

**Example (from current repo):**
- Truth Layer: `last_commit: 43b308a`
- Actual Git HEAD: `41581fae...`
- **This is drift**

**Consequences:**
- Hallucinations (system acts on false beliefs)
- Incorrect decisions
- Loss of trust → abandonment

**Sources:**
- 08_ai_os_current_state_snapshot.md
- 13.md (Drift Detection playbook)

---

### 5.2 Dual Truth Architecture **[EXPLICIT]**

**Two layers of truth:**

**1. Static Truth (Policy)**
- Stored in Git
- Examples: DEC (decisions), GOVERNANCE (policies), service configs
- **Human-authored, human-approved**

**2. Observed State (Reality)**
- **Measured, not declared**
- Examples: Git HEAD (actual), service ports (actual), n8n health (actual)
- Files: OBSERVED_STATE.json, EVENT_TIMELINE.jsonl

**3. Reconciliation Ledger**
- Change Requests (CRs): "Gap X → Proposal Y → Approved/Rejected → Applied/Failed"
- Tracks drift resolution

**Sources:**
- 08_ai_os_current_state_snapshot.md
- 13.md

---

### 5.3 Circuit Breakers **[EXPLICIT]**

**Pattern:** Prevent runaway loops

**Types:**

**Loop Detection:**
- Semantic hash of reasoning traces
- If same reasoning repeated → TRIP

**Rate Limiting:**
- If 50+ file writes/sec → TRIP
- Prevents accidental DOS

**States:**
- **Closed** – Normal operation
- **Open** – Tripped (blocked)
- **Half-Open** – Probation (retry with caution)

**Kill Switch:**
- Emergency: Ctrl+Alt+Esc
- Sends SIGSTOP to container
- Human intervention required

**Sources:**
- 13.md (Circuit Breaker spec)
- msg_020.md

---

### 5.4 HITL (Human-In-The-Loop) Gates **[EXPLICIT]**

**Approval Required For:**

**Destructive Actions:**
- File deletion
- Branch deletion
- Database drops
- Credential changes

**Keyword Pattern:**
- `CONFIRM_NUCLEAR_RESET` for dangerous operations
- Forces explicit human typing

**Spec Approval:**
- Every Change phase requires Spec approval
- No auto-execution

**Sources:**
- ai-life-os-claude-project-playbook.md
- 13.md

---

### 5.5 Git as Safety Net **[EXPLICIT]**

**Infinite Undo:**
- `git revert <commit>` – Undo specific change
- `git reset --hard HEAD~1` – Roll back last commit
- `git reflog` – Recover "lost" commits

**Pre-Commit Hooks:**
- Gitleaks: Scan for secrets before commit
- Prevents accidental credential leaks

**Branch Protection:**
- AI cannot push to `main` directly
- Must create PR → human review → merge

**Sources:**
- 10_claude_desktop_agentic_kernel_playbook_windows.md
- policies/SECURITY_SECRETS_POLICY.md (in repo)

---

### 5.6 Security Threats (STRIDE for AI) **[EXPLICIT]**

**Indirect Prompt Injection:**
- Malicious content in files/emails
- "Ignore previous instructions, do X"
- **Mitigation:** Sandboxing, content filtering

**Confused Deputy:**
- Claude performs dangerous action thinking it's safe
- **Mitigation:** HITL gates, confirmation keywords

**Secret Leakage:**
- Environment variables in plaintext
- Credentials in logs
- **Mitigation:** Launcher Pattern (1Password CLI), no plaintext secrets

**Filesystem Escape:**
- MCP misconfigured → access to C:\
- **Mitigation:** Strict scoping, allowlists

**Sources:**
- 13.md (Security Playbook)
- policies/SECURITY_SECRETS_POLICY.md (in repo)

---

### 5.7 Launcher Pattern (Windows Secret Management) **[PROPOSAL]**

**Pattern:**
```powershell
# launcher.ps1
$OPENAI_KEY = op read "op://vault/openai/key"
$env:OPENAI_API_KEY = $OPENAI_KEY

# Start service with secrets in memory
python service.py
```

**Principle:**
- Secrets injected at runtime
- Never on disk
- 1Password CLI as secret source

**Sources:**
- 10_claude_desktop_agentic_kernel_playbook_windows.md
- 13.md

---

## Family 6: Memory / Life Graph / RAG / Truth Layer

### 6.1 Truth Layer (Short-Term "RAM") **[EXPLICIT]**

**Format:** Git-backed Markdown + YAML frontmatter

**Structure:**
```
memory-bank/
├── 00_Inbox/          # Unsorted capture
├── 10_Projects/       # Active projects (deadline-driven)
├── 20_Areas/          # Life areas (ongoing)
├── 30_Resources/      # Reference materials
└── 99_Archive/        # Completed/inactive
```

**Why Markdown:**
- Human-readable
- LLM-native (no parsing)
- Git-diffable
- Tool ecosystem (Obsidian, Logseq, VS Code)

**Frontmatter (YAML):**
```yaml
---
id: proj-2025-q1-website
type: project
area: professional
status: active
do_date: 2025-02-01
due_date: 2025-03-15
energy_profile: [high_focus, creative]
is_frog: true
---
```

**Sources:**
- 01_architectural-blueprint_phase-3-ai-os.md
- 04_personal-ai-life-os_implementation-strategy.md
- 12.md (Life Graph schema)

---

### 6.2 Vector Memory (Long-Term Episodic) **[EXPLICIT]**

**Technologies:**

**LightRAG / GraphRAG:**
- Knowledge graph (entities + relationships)
- Semantic search over knowledge

**Qdrant / LanceDB:**
- Vector database
- Similarity search

**Mem0:**
- Automatic preference extraction
- User profile building

**Hybrid Search:**
- Semantic (vector similarity)
- Keyword (BM25 / Elasticsearch)
- Combine scores for best results

**Sources:**
- 04_personal-ai-life-os_implementation-strategy.md
- 06_2025-personal-ai-operating-system_architectural-review.md
- 12.md

---

### 6.3 Life Graph Schema **[EXPLICIT]**

**Core Entities:**

**Area:**
- Life domains (Health, Finance, Relationships, Career)
- Ongoing (no deadline)

**Identity:**
- Roles (CEO, Writer, Father, Friend)
- Context for decision-making

**Context:**
- Constraints (@MacBook, @Phone, @LowEnergy, @HighNoise)
- Determines task feasibility

**Project:**
- Finite goals with deadline
- Example: "Launch website by Q1"

**Task:**
- Atomic work unit
- Must be completable in 5-60 minutes

**Log:**
- Stream-of-consciousness thoughts
- Unstructured capture

**Sources:**
- 12.md (comprehensive Life Graph schema)

---

### 6.4 Critical Metadata for ADHD **[EXPLICIT]**

**Energy Profile:**
```yaml
energy_profile: [high_focus, low_focus, creative, admin]
```

**Dopamine Level:**
```yaml
dopamine_level: high | medium | low
```

**Is Frog:**
```yaml
is_frog: true  # The hardest/most dreaded task
```

**Do Date vs. Due Date:**
```yaml
do_date: 2025-02-01      # When to START
due_date: 2025-03-15     # When to FINISH
```

**Why this matters:**
- **Energy matching** – Match task to current energy state
- **Dopamine tracking** – Avoid low-dopamine spirals
- **Frog first** – Tackle hardest task early
- **Do vs. Due** – Time blindness mitigation

**Sources:**
- 12.md
- 18.md (ADHD deep dive)

---

### 6.5 Memory = Git (Structure) + Vector DB (Semantics) **[EXPLICIT]**

**Principle:**
> "Both are essential"

**Git (Structure):**
- Explicit organization (folders, tags)
- Version control
- Human-readable

**Vector DB (Semantics):**
- Similarity search
- Emergent connections
- AI-readable

**Synergy:**
- Git = stable, explicit structure
- Vector = flexible, implicit connections
- Together = powerful hybrid memory

**Sources:**
- 04_personal-ai-life-os_implementation-strategy.md
- 12.md

---

## Proposals vs. Explicit Decisions

### Explicit in Research Docs

✅ All design decisions above marked **[EXPLICIT]** are stated in research files  
✅ Sources cited for each decision  

### Proposals (Inferred/Design Choices)

**[PROPOSAL]** tags indicate:
- Inferred from research but not explicitly stated
- Logical extensions of explicit principles
- Design choices where research provides options but not prescription

**Examples of Proposals:**
- Host-Agnostic Interface Layer (future multi-client)
- Launcher Pattern (specific implementation of secret management)

---

## Summary: Target Architecture in One Page

**System Type:** Personal AI Life Operating System

**Core Architecture:**
- **Kernel:** Claude Desktop (Semantic Microkernel)
- **Bus:** MCP (Model Context Protocol)
- **Memory:** Git-backed Markdown/YAML + Vector DB
- **Scheduler:** n8n (temporal/scheduled tasks)
- **Storage:** Truth Layer (files) + Governance Layer (metrics)

**Key Workflows:**
- **Chat → Spec → Change** (ADHD-aware execution)
- **Dual Truth** (Policy + Observed State)
- **Drift Detection → Reconciliation** (Observer + CRs)

**Safety:**
- **HITL Gates** (human approval for destructive actions)
- **Circuit Breakers** (loop/rate limiting)
- **Git as Rollback** (infinite undo)

**ADHD Optimization:**
- **Low Activation Energy** (chat interface)
- **Progressive Disclosure** (2-3 options max)
- **Energy Matching** (tasks tagged by energy_profile)
- **Dopamine Menus** (pre-approved low-energy tasks)
- **Fearless Experimentation** (Git rollback)

**Infrastructure:**
- **Windows 11 + WSL2** (with filesystem/networking caveats)
- **Docker** (named volumes, health checks)
- **n8n** (PostgreSQL or named volumes for persistence)

---

## Next Steps

With this target architecture defined:

1. ✅ **current_state_map.md** – What exists today
2. ✅ **target_architecture_summary.md** – What SHOULD exist (this document)
3. 📋 **current_vs_target_matrix.md** – Map legacy → target
4. 📋 **migration_plan.md** – Stepwise migration plan

**Awaiting approval to proceed to Step 3.**

---

**Document Version:** 1.0  
**Created:** 2025-11-29  
**By:** Claude Desktop (Phase 0, Step 2)  
**Sources:** 29 research files in `/mnt/project/`  
**Confidence:** High (explicit sources cited throughout)