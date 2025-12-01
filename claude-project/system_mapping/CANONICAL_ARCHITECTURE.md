# Canonical Architecture – Personal AI Life OS

**Purpose:** Authoritative architectural model for the entire system  
**Status:** CANONICAL (all other docs must align with this)  
**Last Updated:** 2025-11-30  

---

## TL;DR: Core / Ports / Adapters (10-second version)

**Hexagonal Architecture:**

- **Core** = Git-backed Truth Layer  
  - The entire `C:\Users\edri2\Desktop\AI\ai-os` repository
  - Includes: Memory Bank, Governance Layer, all state files
  - Single source of truth (no state fragmentation)

- **Ports** = MCP servers (standardized interfaces)  
  - Examples: `filesystem`, `git` (future), `mcp_github_client`, `google_workspace_client`, `n8n-mcp`, `os_core_mcp`
  - Stateless interfaces to external systems
  - Supervisor-Worker pattern (all coordination through Adapters, no mesh networking)

- **Adapters** = Frontends / AI models (orchestrators)  
  - Current: Claude Desktop (primary reasoning orchestrator)
  - Future: ChatGPT, Gemini, Telegram bot, CLI
  - Replaceable without corrupting Core

- **Goal:** Model-agnostic, single-source-of-truth architecture that prevents drift and split-brain

---

## Why This Model?

**Problem Solved:**
- Previous docs had conflicting metaphors (Claude = CPU vs. Kernel vs. Adapter)
- Unclear what's Core vs. Tool vs. Frontend
- Split-brain risk: multiple "sources of truth"

**Solution:**
- **Core** = persistent state (git-backed files)
- **Ports** = standardized tool interfaces (MCP servers)
- **Adapters** = reasoning engines (replaceable AI models)

**Benefits:**
1. **Model-agnostic** – Replace Claude with ChatGPT/Gemini without breaking Core
2. **Single source of truth** – Git repo is canonical, not chat memory
3. **Standardized interfaces** – MCP = universal "device driver" for AI
4. **Safety** – Core is durable + version-controlled, Adapters are ephemeral
5. **ADHD-friendly** – Low friction (chat interface) + deterministic execution (Ports)

---

## 6 Core Invariants

### INV-001: Single Git Repository as Core

**Statement:**  
The Git repository at `C:\Users\edri2\Desktop\AI\ai-os` is the canonical Truth Layer. All durable state lives here. No state fragmentation across multiple repos or databases.

**Enforcement:**  
All state changes must be git-tracked.

**Violations:**
- Creating state files outside repo
- Using external databases for durable state
- Untracked state files in `.gitignore` for Core components

**Example (Good):**
```bash
# Update governance state
python governance/scripts/generate_snapshot.py
git add governance/snapshots/GOVERNANCE_LATEST.json
git commit -m "chore(governance): Update snapshot"
```

**Example (Bad):**
```bash
# Store state in external SQLite DB
sqlite3 /tmp/my_state.db "INSERT INTO ..."  # ❌ NOT in git repo
```

---

### INV-002: All State Changes via Known Paths

**Statement:**  
All modifications to the Truth Layer must go through documented paths:
- **Preferred:** MCP servers (Ports)
- **Temporary:** PowerShell bridges (documented as TD-XXX)
- **Never:** Direct file manipulation without tool abstraction

**Enforcement:**  
Every state change traceable to a Port or documented bridge.

**Violations:**
- Manual file edits without tool abstraction
- Undocumented scripts modifying Truth Layer
- Direct database writes bypassing reconciler

**Example (Good):**
```python
# Via MCP port (filesystem)
mcp.filesystem.write_file('memory-bank/00_Inbox/idea.md', content)
```

**Example (Temporary - Acceptable if documented):**
```powershell
# TD-001: Git MCP not configured, manual bridge required
git add "docs/file.md"
git commit -m "docs: Update file"
```

**Example (Bad):**
```python
# Direct file write, no tool abstraction
with open('docs/file.md', 'w') as f:  # ❌ Bypasses MCP
    f.write(content)
```

---

### INV-003: Frontends/Models are Replaceable Adapters

**Statement:**  
Frontends and AI models are Adapters (orchestrators), not Core components. Claude Desktop is the current primary adapter, but the system must support:
- Future: ChatGPT, Gemini, Telegram bot, CLI
- Constraint: Adapters orchestrate, Core persists
- Requirement: Replacing an Adapter must not corrupt Core

**Enforcement:**  
No adapter-specific logic in Core files.

**Violations:**
- Hardcoding "Claude" in Truth Layer schemas
- Adapter-dependent state (e.g., Claude-specific session IDs in Core)
- Core files importing adapter-specific libraries

**Example (Good):**
```yaml
# memory-bank/10_Projects/project.md
---
id: proj-2025-website
type: project
created_by_adapter: claude_desktop  # ✅ Generic field
created_at: 2025-11-30T10:00:00Z
---
```

**Example (Bad):**
```yaml
# memory-bank/10_Projects/project.md
---
id: proj-2025-website
type: project
claude_session_id: abc123  # ❌ Adapter-specific
---
```

---

### INV-004: MCP Servers are Stateless Ports

**Statement:**  
MCP servers are Ports (standardized interfaces to external systems):
- Each MCP server = one port to a specific domain (GitHub, Google, OS, etc.)
- Ports are stateless (all state in Core)
- Supervisor-Worker pattern (no mesh networking between ports)

**Enforcement:**  
MCP servers store zero durable state.

**Violations:**
- MCP server with its own database
- Ports talking to each other directly
- Port caching state without syncing to Core

**Example (Good):**
```python
# services/mcp_github_client/api/routes_github.py
@app.post("/create_issue")
async def create_issue(repo: str, title: str, body: str):
    # Stateless: call GitHub API, return result
    result = github_client.create_issue(repo, title, body)
    return result
```

**Example (Bad):**
```python
# services/mcp_github_client/api/routes_github.py
db = sqlite3.connect('github_cache.db')  # ❌ Port storing state

@app.post("/create_issue")
async def create_issue(repo: str, title: str, body: str):
    # Cache result in port's database
    db.execute("INSERT INTO cache ...")  # ❌ Violates statelessness
```

---

### INV-005: Separation of Concerns

**Statement:**  
Clear responsibility boundaries:
- **Planning/Reasoning:** Adapters (Claude, ChatGPT, etc.)
- **Execution/Scheduling:** Ports & Tools (MCP, n8n)
- **Persistence:** Core (Git-backed files)

**Constraint:**  
Adapters are REACTIVE (user-initiated), not autonomous. Autonomous execution requires n8n (scheduled tasks through Ports).

**Enforcement:**  
Claude Desktop never runs in background.

**Violations:**
- Adapter attempting to self-schedule
- Port attempting to reason (e.g., "smart" MCP server making decisions)
- Core containing execution logic

**Example (Good):**
```yaml
# n8n workflow (scheduled task)
schedule:
  every: 15 minutes
tasks:
  - call: http://localhost:8083/observe  # ✅ Port execution
  - call: http://localhost:8083/reconcile
```

**Example (Bad):**
```python
# Claude Desktop trying to self-schedule
import schedule  # ❌ Adapter cannot run in background

def check_email():
    # Claude Desktop is REACTIVE, cannot self-schedule
    pass

schedule.every(15).minutes.do(check_email)  # ❌ Violation
```

---

### INV-006: Git as Infinite Undo

**Statement:**  
Every change to the Truth Layer is git-tracked and reversible:
- All files under version control
- Rollback always available (`git revert`, `git reset`)
- Pre-commit hooks prevent secret leakage (Gitleaks)

**Enforcement:**  
Every durable state change = git commit.

**Violations:**
- Untracked state files
- `.gitignore` for Core components
- No-commit changes to Truth Layer

**Example (Good):**
```bash
# Every state change is a commit
python memory-bank/tools/create_project.py "Website redesign"
git add memory-bank/10_Projects/proj-2025-website.md
git commit -m "feat(memory): Add website redesign project"

# Rollback if needed
git revert HEAD  # ✅ Infinite undo
```

**Example (Bad):**
```bash
# State change without git commit
python memory-bank/tools/create_project.py "Website redesign"
# ❌ No git add/commit = state not tracked
```

---

## Contradiction Resolution

**5 contradictions resolved from previous docs:**

| Old Metaphor / Pattern | New Canonical | Rationale |
|------------------------|---------------|-----------|
| "Claude Desktop = CPU" | "Claude Desktop = Adapter" | Models are replaceable; Core (Truth Layer) is the persistent "brain" |
| "MCP = Bus" | "MCP = Ports" | Emphasizes standardized interfaces, not routing. Supervisor-Worker, not mesh. |
| "Truth Layer on Windows (C:\...) vs WSL2" | "Windows is canonical NOW; WSL2 is future optimization" | Current setup works; WSL2 migration only if Docker performance critical (Phase 4) |
| "Everything via MCP" vs PowerShell bridges | "Temporary bridges acceptable if documented (TD-XXX)" | Git MCP missing (TD-001) → manual bridge is temporary but safe |
| "Claude is autonomous" vs "Claude is reactive" | "Claude is REACTIVE; n8n is autonomous" | Claude Desktop cannot run in background; n8n handles scheduled tasks |

---

## Pattern Classification

**What's canonical NOW vs future vs legacy:**

| Pattern | Status | Phase | Notes |
|---------|--------|-------|-------|
| Claude Desktop as Adapter | ✅ **CANONICAL** | Now | Current primary reasoning orchestrator |
| MCP servers as Ports | ✅ **CANONICAL** | Now | Standardized interfaces (filesystem, GitHub, Google, os_core) |
| Git-backed Truth Layer on Windows | ✅ **CANONICAL** | Now | `C:\Users\edri2\Desktop\AI\ai-os` |
| PowerShell bridges (documented as TD-XXX) | ⚠️ **TEMPORARY** | Now → Phase 2 | TD-001: Git MCP missing, manual bridge acceptable |
| n8n for scheduled tasks | ✅ **CANONICAL** | Phase 2 | Autonomous execution through Ports |
| Memory Bank (PARA structure) | ✅ **CANONICAL** | Phase 1-2 | Already created, being populated |
| Observer + Reconciler | ✅ **CANONICAL** | Phase 2 | Drift detection + CR-based sync |
| Circuit Breakers | ✅ **CANONICAL** | Phase 2 | Loop detection, rate limiting, kill switch |
| ChatGPT/Gemini as Adapters | 🔮 **FUTURE** | Phase 3-4 | Multi-model support |
| Truth Layer on WSL2 | 🔮 **FUTURE** | Phase 4 (if needed) | Only if Docker performance critical |
| LangGraph for multi-day HITL | 🔮 **FUTURE** | Phase 3 | Agentic sleep with checkpoints |
| Vector Memory (LightRAG/Qdrant) | 🔮 **FUTURE** | Phase 2-3 | Design in Phase 2, implement in Phase 3 |
| Direct PowerShell (undocumented) | ❌ **LEGACY** | Phase 1 cleanup | Must be abstracted or documented as TD-XXX |
| "Claude = CPU" metaphor | ❌ **LEGACY** | Phase 1 update | Replace with "Claude = Adapter" |
| "MCP = Bus" metaphor | ❌ **LEGACY** | Phase 1 update | Replace with "MCP = Ports" |

---

## How This Affects Migration Plan

**Impact on existing plan:**

1. **Phase 1 (Investigation & Cleanup):** ✅ Already aligned
   - Archive legacy components (ai_core/, tools/) ✅ Complete
   - Remove duplicates ✅ Complete
   - Fix drift ✅ Complete
   - **NEW:** Codify canonical architecture ✅ This slice

2. **Phase 2 (Core Infrastructure):**
   - Memory Bank (PARA) → **Core** creation
   - Observer + Reconciler → **Ports** for drift detection
   - Circuit Breakers → **Ports** safety layer
   - n8n workflows → **Autonomous execution** through Ports

3. **Phase 3 (Governance & Metrics):**
   - Fitness metrics (FITNESS_001-003) → **Core** instrumentation
   - Governance dashboard → **Adapter** for visualization

4. **Phase 4 (Legacy Cleanup):**
   - Deprecate confirmed legacy → Remove non-canonical patterns
   - Consolidate scripts → Align with Ports pattern
   - Archive research → Clean up after migration

**Technical Debt Mapping:**

- **TD-001 (Git MCP):** Part of "Ports completion" strategy
  - Git operations currently via PowerShell bridge (temporary)
  - Future: Git MCP server configured → full autonomy
  - Does not block current work, but reduces friction

---

## Research Grounding

This canonical model is grounded in:

- **Architecture/Kernel research family**
  - Semantic Microkernel pattern (01, 06, 09)
  - Chat→Spec→Change workflow (10, 11, playbook)
  - Supervisor-Worker architecture (09, msg_020)

- **Safety/Drift research family**
  - Dual Truth Architecture (Policy + Observed State) (08, 13)
  - Drift detection and reconciliation (08, 13)
  - Circuit Breakers and HITL gates (13, msg_020)

- **Memory/Truth Layer research family**
  - Git-backed Markdown + Memory Bank (01, 04, 06)
  - PARA pattern (Projects/Areas/Resources/Archive) (12)
  - Life Graph schema for ADHD optimization (12, 18)

**Key Research Files Referenced:**
- 01_architectural-blueprint_phase-3-ai-os.md
- 06_2025-personal-ai-operating-system_architectural-review.md
- 08_ai_os_current_state_snapshot.md
- 09_agentic_kernel_claude_desktop_mcp.md
- 10_claude_desktop_agentic_kernel_playbook_windows.md
- 11_cognitive_technical_symbiosis_personal_ai_life_os.md
- 12.md (Life Graph schema)
- 13.md (Safety playbook)
- 18.md (ADHD deep dive)
- ai-life-os-claude-project-playbook.md

---

## Compliance Checklist for New Work

**Before creating any new component, ask:**

1. ✅ Is this Core, Port, or Adapter?
2. ✅ If Core: Is it git-tracked?
3. ✅ If Port: Is it stateless? Does it use MCP?
4. ✅ If Adapter: Is it model-agnostic? Can it be replaced?
5. ✅ Does it align with the 6 invariants?
6. ✅ Is it classified as canonical/future/legacy?

**If ANY answer is unclear → Consult this document first.**

---

**Document Version:** 1.0  
**Status:** CANONICAL (authoritative)  
**Created:** 2025-11-30  
**By:** Claude Desktop (Slice 1.5)  
**Authority:** All other architectural docs must align with this model
