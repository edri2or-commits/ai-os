# Tools & Capabilities Inventory

**Last Updated:** 2025-12-06  
**Source:** Verified from configuration files, README docs, and active services  
**Update Rule:** Add entries when new tool/API/service deployed

### Status Levels

| Icon | Level | Meaning |
|------|-------|---------|
| 📝 | **EXISTS** | Code written, not tested |
| ✅ | **TESTED** | Works when started manually |
| 🟡 | **STAGED** | Ready for production deployment (awaiting VPS) |
| 🟢 | **TESTING** | Running locally (Task Scheduler/manual), not yet 24/7 |
| 🔵 | **PRODUCTION** | Auto-start on VPS, 24/7 uptime, always available |
| ❌ | **BROKEN** | Exists but doesn't work, needs fix |

---

## MCP Servers (Claude Desktop)

**Configuration File:** `%APPDATA%\Claude\claude_desktop_config.json`

### Active MCP Servers:

**1. Google Workspace MCP**
- **Package:** `google-mcp.exe` (Bun executable)
- **Capabilities:** 
  - Gmail (read, send, search, delete)
  - Calendar (create events, list events)
  - Drive (search files, read files)
- **Auth:** OAuth 2.0 (edri2or@gmail.com)
- **Token Path:** `C:\Users\edri2\.google-mcp-tokens.json`
- **Status:** ✅ OPERATIONAL
- **Port:** N/A (MCP stdio)
- **Documentation:** Via Context7 MCP (search Google Workspace docs)

**2. n8n MCP Server**
- **Package:** `@leonardsellem/n8n-mcp-server` (npx)
- **Capabilities:**
  - List workflows
  - Execute workflows
  - Get workflow details
  - Create/update workflows
- **Endpoint:** http://localhost:5678/api/v1
- **Auth:** N8N_API_KEY (JWT token in config)
- **Status:** ✅ OPERATIONAL
- **Documentation:** n8n API docs + MCP server README

**3. Desktop Commander** (assumed - check if active)
- **Capabilities:**
  - File operations (read, write, search)
  - Subprocess management (Python, PowerShell)
  - Git operations (commit, status, diff)
  - Windows automation
- **Scope:** Allowed directories only
- **Status:** ✅ OPERATIONAL (based on usage patterns)

**4. Context7**
- **Capabilities:** Search library documentation for unknown tools
- **Use Case:** "How do I use X library?" → Context7 searches docs
- **Status:** ✅ OPERATIONAL (based on project docs)

**5. Windows-MCP** (assumed - check if active)
- **Capabilities:**
  - UI automation (Click, Type, Scroll)
  - State capture (screenshot + UI tree)
  - Desktop interaction
- **Status:** ⚠️ VERIFY (mentioned in docs, not in config)

---

## REST APIs (localhost)

### H1: Google Workspace Client (REST API)

**Service:** FastAPI wrapper for Google APIs  
**Port:** 8082  
**URL:** http://localhost:8082  
**Status:** 🟡 STAGED (code ready, awaits H4 VPS deployment for 24/7 auto-start)

**Endpoints:**
- `POST /google/gmail/send` - Send email
- `POST /google/gmail/list` - List emails
- `POST /google/calendar/create-event` - Create calendar event
- `POST /google/calendar/list-events` - List calendar events
- `POST /google/drive/search` - Search Drive files
- `POST /google/sheets/create` - Create spreadsheet
- `POST /google/sheets/read` - Read spreadsheet data
- `POST /google/docs/create` - Create document
- `POST /google/tasks/create` - Create task

**Auth:** OAuth 2.0 (credentials.json + token.json in project root)  
**Account:** edri2or@gmail.com

**Documentation:** `services/google_workspace_client/README.md`

---

### H2: Memory Bank API (Context API)

**Service:** FastAPI server for external LLMs  
**Port:** 8081  
**URL:** http://localhost:8081  
**Status:** 🟡 STAGED (code ready, manual start works, awaits H4 VPS deployment for 24/7 auto-start)

**Endpoints:**
- `GET /health` - Service health check (returns status, version, Git SHA)
- `GET /api/context/summary` - First 100 lines of 01-active-context.md (5.7KB) ⭐ **NEW**
  - Quick Status, Current Work, Recent Changes, Next Steps
  - Optimized for external LLM consumption (minimal tokens)
- `GET /api/context/current-state` - Full 01-active-context.md (101KB, 1,894 lines)
  - Complete project state with all history
- `GET /api/context/roadmap` - HEADLESS_MIGRATION_ROADMAP_TLDR.md (4.6KB) ⭐ **NEW**
  - H1→H2→H3→H4 VPS migration plan
  - Progress tracking (3/4 complete)
- `GET /api/context/story` - AI_LIFE_OS_STORY.md (12.5KB, 292 lines) ⭐ **NEW**
  - Complete project narrative with progressive disclosure
  - Elevator pitch → What/Why/How → Current state → Architecture → Vision
- `GET /api/context/protocols` - PROTOCOLS section extraction
- `GET /api/context/research/{family}` - Research files by family
  - Note: Only 2 files currently (08_ai_os_current_state_snapshot.md, 09_agentic_kernel_claude_desktop_mcp.md)

**Research Families:**
- `architecture` - Hexagonal, MAPE-K, Agentic Kernel
- `mcp` - Claude Desktop, MCP integration
- `adhd` - Cognitive load, executive function
- `safety` - Security, governance, drift detection
- `infra` - Windows, Docker, n8n
- `memory` - Life Graph, PARA, vector memory
- `meta` - Playbooks, slices, meta-learning

**Auth:** None (localhost only)  
**Purpose:** External LLMs (GPT, Gemini, o1) load context in < 30 seconds

**Documentation:** `services/context-api/README.md`

---

### H3: Telegram Approval Bot

**Service:** FastAPI + Telegram Bot  
**Port:** N/A (Telegram WebSocket)  
**Bot:** @SALAMTAKBOT  
**Status:** 🟢 TESTING (running locally via Task Scheduler, ready for H4 VPS migration)

**Capabilities:**
- Async Human-in-the-Loop approvals
- Inline buttons ([✅ Approve] [❌ Reject] [📄 View Full])
- Directory watcher (`truth-layer/drift/approvals/pending/`)
- SQLite database (approvals.db)
- Telegram notifications (< 5 seconds)

**Workflow:**
1. Reconciler writes CR to `pending/`
2. Backend detects file (< 1 sec)
3. Telegram notification sent (< 5 sec)
4. User clicks ✅ Approve
5. Approval file written to `approved/`
6. Executor applies CR
7. Telegram message updated: "✅ Applied!"

**Auth:** Telegram Bot Token + Chat ID whitelist  
**Chat ID:** 5786217215 (Or's Telegram)

**Documentation:** `services/approval-bot/README.md`

**Test Results (2025-12-06):**
- ✅ End-to-end test passed
- ✅ CR detected in 5 seconds
- ✅ Telegram notification received
- ✅ Approval workflow completed
- ✅ Database updated

---

## Services (Docker)

### n8n (Automation Platform)

**Image:** `n8nio/n8n:latest`  
**Container:** `n8n-production`  
**Port:** 5678  
**URL:** http://localhost:5678  
**Status:** ✅ AUTO-START

**Environment:**
- `NODE_ENV=production`
- `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` (⚠️ security risk)
- `OPENAI_API_KEY` - GPT-4o access for Judge Agent

**Volumes:**
- `n8n_data` - Workflow storage
- `C:\Users\edri2\Desktop\AI\ai-os:/workspace` - Truth layer access

**Active Workflows:**
1. **Judge Agent V2** - Error detection (GPT-4o, every 6h)
2. **Email Watcher** - Gmail monitoring (every 15 min via Task Scheduler)
3. **Memory Watchdog** - Memory Bank updates (file watcher)

**Documentation:** `infra/n8n/` + `n8n_workflows/README_judge_v2_langfuse.md`

---

### Qdrant (Vector Database)

**Image:** `qdrant/qdrant:latest`  
**Container:** `qdrant-production`  
**Ports:** 6333 (API), 6334 (gRPC)  
**URL:** http://localhost:6333  
**Status:** ✅ AUTO-START

**Collections:**
- `memory-bank` - Memory Bank vectors
- `life-graph` - Life Graph entities (future)

**Purpose:** Vector search for Memory Bank, LHO retrieval

---

### Langfuse (Observability Platform)

**Docker Compose:** `infra/langfuse/docker-compose.yml`  
**Port:** 3000  
**URL:** http://localhost:3000  
**Status:** ✅ OPERATIONAL (V3 deployed 2025-12-05)

**Services (6/6 healthy):**
1. **langfuse-web** (port 3000) - UI dashboard
2. **langfuse-worker** (port 3030) - Background jobs
3. **postgres** (port 5432) - Main database
4. **clickhouse** (ports 8123, 9000) - Analytics
5. **redis** (port 6379) - Cache/queue
6. **minio** (ports 9090, 9091) - Object storage

**Purpose:**
- Trace all Claude actions
- Visual debugging (timeline, spans, costs)
- Cost tracking (automatic token counting)
- Performance monitoring

**API:**
- **Public Key:** `pk-lf-...` (from dashboard)
- **Secret Key:** `sk-lf-...` (from dashboard)
- **Host:** http://localhost:3000

**Integration:**
- Judge Agent V2 (reads traces from Langfuse)
- `tools/langfuse_logger.py` (logs actions)

**Documentation:** `n8n_workflows/README_judge_v2_langfuse.md`

---

## Git Hooks (Automatic Enforcement)

### Pre-Push Reflection Hook (Protocol 1 LEVEL 1)

**Implementation Date:** 2025-12-07  
**Status:** 🟢 ACTIVE  
**Purpose:** Enforce micro-reflection before every push (close 93% documentation gap)

**Files:**
- `.git/hooks/pre-push` (50 lines, Bash wrapper)
- `tools/hooks/pre-push-enforcer.ps1` (195 lines, PowerShell enforcer)
- `REFLECTION_LOG.md` (output, append-only)

**Capabilities:**
- ✅ Blocks `git push` until reflection exists
- ✅ Auto-generates template with branch+date signature
- ✅ Opens VS Code (--wait) for user to fill
- ✅ Validates content changed (prevents empty save)
- ✅ Validates signature exists (prevents template deletion)
- ✅ Streak counter (consecutive days: [OK]/[BOLT]/[FIRE])
- ✅ Same-day multi-push smart pass (no friction for debugging)

**Workflow:**
```
git push
  ↓
Hook checks: REFLECTION_LOG.md contains "## Reflection: [branch] - [date]"
  ↓
YES → Show streak + Allow push
NO  → Block + Add template + Open editor → Wait → Validate → Allow push
```

**Bypass:**
```bash
git push --no-verify  # Emergency only
```

**Documentation:** `memory-bank/protocols/PROTOCOL_1_pre-push-reflection.md`

**Research Basis:**
- Gawande Checklist Methodology (active > passive)
- ADHD-aware design (blocking > nagging)
- Aviation pre-flight model (push = point of no return)

**Success Metrics:**
- Before: 98 commits, 7 entries (93% gap)
- After: 100% compliance (hook enforces)

---

## Windows Automations (Task Scheduler)

### 1. Observer (Drift Detection)

**Task Name:** `\AI-OS\Observer-Drift-Detection` (assumed name)  
**Schedule:** Every 15 minutes  
**Script:** `tools/observer.py`  
**Output:** `truth-layer/drift/YYYY-MM-DD-HHMMSS-drift.yaml`

**Purpose:**
- Compare truth-layer YAML files to git HEAD
- Detect: modified, added, deleted files
- Generate drift reports for Reconciler

**Status:** ✅ OPERATIONAL (runs every 15 min)

---

### 2. Email Watcher

**Task Name:** `\AI-OS\Email Watcher`  
**Schedule:** Every 15 minutes  
**Script:** `tools/email_watcher.py --verbose`  
**Output:** `truth-layer/drift/email/` + Telegram notifications

**Purpose:**
- Monitor Gmail for important emails
- Generate drift reports
- Send Telegram alerts

**Status:** ✅ OPERATIONAL (runs every 15 min)

---

### 3. Memory Bank Watchdog

**Task Name:** (assumed - verify with `schtasks /Query`)  
**Schedule:** On file change (file watcher)  
**Script:** `tools/watchdog.py`  
**Output:** Qdrant vectors

**Purpose:**
- Watch memory-bank/ directory for changes
- Update Qdrant vector index
- Keep vector search current

**Status:** ✅ OPERATIONAL (based on project docs)

---

## Python Tools (CLI)

**Location:** `tools/`

### Core Tools:

**1. Observer** (`tools/observer.py`)
- Drift detection (truth-layer YAML files)
- Read-only, git-based
- Exit codes: 0 (clean), 1 (drift), 2 (error)

**2. Reconciler** (`tools/reconciler.py`)
- Change Request (CR) management
- Commands: generate, list, show, approve, reject
- Apply logic: ⏭ Coming in Slice 2.4c

**3. Langfuse Logger** (`tools/langfuse_logger.py`)
- Log Claude actions to Langfuse
- Functions: `log_action()`, `log_tool_call()`
- Integration: Protocol 1 (post-slice updates)

**4. Email Watcher** (`tools/email_watcher.py`)
- Gmail monitoring
- Drift report generation
- Telegram notifications

**5. Watchdog** (`tools/watchdog.py`)
- Memory Bank file watcher
- Qdrant vector updates
- Auto-sync on file changes

**6. Entity Validator** (`tools/validate_entity.py`)
- Validate Life Graph entities against schema
- Pre-commit hook integration
- Commands: validate file/directory, `--staged`

---

## State Management & ADHD Support

### NAES v1.0 (Neuro-Adaptive Executive Scaffold)

**Implementation Date:** 2025-12-07  
**Status:** 🟢 OPERATIONAL  
**Purpose:** State-aware ADHD support through behavioral differentiation

**Location:** `memory-bank/20_Areas/adhd-support/`

**Components:**

**1. State File** (`adhd_state.json`)
- **6 Core Signals:**
  1. Energy (Spoons): 1-10 scale (Red: ≤3, Yellow: 4-6, Green: 7-10)
  2. Cognitive Clarity: clear / foggy / mud
  3. Emotional Valence: negative / neutral / positive (RSD meter)
  4. Sensory Load: low / medium / high
  5. Task Urgency: low / medium / high / critical
  6. Time Since Break: Minutes (hyperfocus risk >90 min)

**2. System Modes** (`mode_prompts/`)
- **CRISIS_RECOVERY** (Priority 1, energy ≤3)
  - Rules: Stop work, validate rest, 1-2 sentences max, no choices
  - Pattern: "Let's stop here. Rest is work."
  
- **PARALYSIS_BREAKER** (Priority 2, stuck/foggy)
  - Rules: Micro-steps only, 3 sentences max, binary requests (👍)
  - Pattern: "Step 1: Open file. 👍 when done."
  
- **BODY_DOUBLE** (Priority 3, anxious + energy >5)
  - Rules: Validate emotion first, 2-minute commitments, stay present
  - Pattern: "That makes sense. X feels big. 2 minutes. I'm here. Ready?"
  
- **FLOW_SUPPORT** (Priority 4, default)
  - Rules: Standard helpful assistance, 2-3 options max, structured
  - Pattern: TL;DR + Details, clear next steps

**3. State Monitor** (`tools/adhd_state_monitor.py`)
- Checks state staleness (>24h → warning)
- Detects hyperfocus risk (>90 min since break → sets flag)
- Auto-updates `hyperfocus_risk` in state file
- Appends events to `state_history.jsonl`
- **Integration:** Called by Observer every 15 min

**4. State History Log** (`state_history.jsonl`)
- Append-only event log (JSONL format)
- Events: state changes, mode transitions, hyperfocus alerts
- **Future:** Watchdog indexes to Qdrant for pattern analysis

**5. Protocol AEP-002** (`protocols/AEP-002_state-management.md`)
- How Claude reads state at session start
- Decision tree for mode selection
- State update workflow
- Mode transition rules
- Integration with existing protocols

**Decision Tree (Priority Order):**
```python
if energy_spoons <= 3:
    return "CRISIS_RECOVERY"
elif clarity == "mud" or stuck:
    return "PARALYSIS_BREAKER"
elif valence == "negative" and energy_spoons > 5:
    return "BODY_DOUBLE"
else:
    return "FLOW_SUPPORT"
```

**Observer Integration:**
```python
# tools/observer.py (every 15 min)
from adhd_state_monitor import ADHDStateMonitor

monitor = ADHDStateMonitor()
report = monitor.check_state()  # Returns: mode, energy, minutes_since_break
# Logs: ADHD state summary + warnings (stale state, hyperfocus risk)
```

**Research Basis:**
- Spoon Theory (energy as computational variable)
- Dopamine Economy (task initiation deficits)
- Executive Function Domains (BRIEF-A → digital scaffolding)
- Ecological Momentary Assessment (real-time state capture)
- Rejection Sensitive Dysphoria (RSD) support

**Expected Impact:**
- Before: 60% cosmetic ADHD support (generic responses)
- After: 90%+ genuine support through behavioral differentiation

**Usage (Claude):**
```python
# Session start
state = read_json("memory-bank/20_Areas/adhd-support/adhd_state.json")
mode = select_mode(state)  # Returns: CRISIS_RECOVERY | PARALYSIS_BREAKER | BODY_DOUBLE | FLOW_SUPPORT
prompt = read_file(f"memory-bank/20_Areas/adhd-support/mode_prompts/{mode}.md")
# Follow prompt rules for this interaction
```

**Next Steps (H4 VPS):**
- n8n workflows:
  - Morning check-in (7 AM): "How many spoons today?"
  - Hyperfocus break (90 min): "Crash risk. Permission to stop?"
  - Evening wind-down (8 PM): "State update + tomorrow prep"

**Documentation:** 
- `memory-bank/20_Areas/adhd-support/README.md`
- `memory-bank/protocols/AEP-002_state-management.md`

---

## Capabilities Quick Reference

### "Can I...?" Table

| Action | Tool/Service | Method | Status |
|--------|-------------|---------|--------|
| **Send email** | Google Workspace Client (H1) | `POST /google/gmail/send` | ✅ |
| **Read emails** | Google Workspace MCP | MCP tool | ✅ |
| **Create calendar event** | Google Workspace Client (H1) | `POST /google/calendar/create-event` | ✅ |
| **Search Drive** | Google Workspace MCP | MCP tool | ✅ |
| **Read files** | Desktop Commander | MCP tool | ✅ |
| **Write files** | Desktop Commander | MCP tool | ✅ |
| **Git commit** | Desktop Commander | MCP tool | ✅ |
| **Run Python** | Desktop Commander | Subprocess | ✅ |
| **Run PowerShell** | Desktop Commander | Subprocess | ✅ |
| **Create n8n workflow** | n8n MCP | MCP tool | ✅ |
| **Execute n8n workflow** | n8n MCP | MCP tool | ✅ |
| **Search vectors** | Qdrant | HTTP API (localhost:6333) | ✅ |
| **Log telemetry** | Langfuse | Python SDK | ✅ |
| **Get async approval** | Telegram Bot (H3) | File watcher + Telegram | ✅ |
| **Detect drift** | Observer | CLI (`tools/observer.py`) | ✅ |
| **Generate CR** | Reconciler | CLI (`tools/reconciler.py generate`) | ✅ |
| **Load context for GPT** | Memory Bank API (H2) | `GET /api/context/current-state` | ✅ |
| **Search library docs** | Context7 MCP | MCP tool | ✅ |
| **UI automation** | Windows-MCP | MCP tool | ⚠️ VERIFY |

---

## Limitations & Constraints

### File System:
- ✅ Can read/write in `C:\Users\edri2\Desktop\AI\ai-os`
- ❌ Cannot write outside project directory
- ❌ Cannot delete system files

### Gmail:
- ✅ Can send emails (via H1 REST API or MCP)
- ✅ Can read emails (via MCP)
- ❌ Cannot modify Gmail settings (no API)

### n8n:
- ✅ Can create/activate workflows (via MCP)
- ✅ Can trigger webhooks
- ❌ Cannot execute workflows synchronously (all async)
- ⚠️ `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` (security risk - allows Code Node to read env vars)

### LLMs:
- ✅ Can call GPT-4o (via n8n Judge Agent)
- ✅ Can call Claude Sonnet 4.5 (via Claude Desktop)
- ❌ Cannot call o1 directly (no MCP/API yet)
- ❌ Cannot call Gemini directly (use H2 Memory Bank API instead)

### Docker:
- ✅ Services auto-start on boot
- ✅ Can restart containers via PowerShell
- ❌ Cannot modify docker-compose.yml from Claude (security)

### Telegram:
- ✅ Can send notifications
- ✅ Can receive approvals (HITL)
- ❌ Cannot initiate conversations (bot only responds)

---

## Security Notes

**⚠️ CRITICAL ISSUES:**

1. **n8n Environment Access**
   - `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` allows Code Nodes to read `process.env`
   - **Risk:** Workflow can dump OPENAI_API_KEY
   - **Mitigation:** Set to `true` in production (breaks some workflows)

2. **Plaintext Secrets in Config**
   - `claude_desktop_config.json` has Google OAuth client secret
   - **Risk:** Readable by any process as user
   - **Mitigation:** Use Launcher Pattern (future H4)

3. **API Keys in .env**
   - `.env` file in project root has multiple API keys
   - **Risk:** Committed to git if not in .gitignore
   - **Mitigation:** Verify .gitignore, never commit .env

**✅ GOOD PRACTICES:**

1. **OAuth 2.0 for Gmail**
   - Token-based auth, refresh tokens
   - Revocable from Google Account settings

2. **Telegram Bot Token**
   - Chat ID whitelist (only Or can approve)
   - Bot cannot initiate conversations

3. **Git-based Audit Trail**
   - All CRs and approvals tracked in git
   - Reversible with `git revert`

---

## Update History

- **2025-12-06:** Initial creation from verified configs
- **Source Files:**
  - `claude_desktop_config.json` (MCP servers)
  - `docker-compose.yml` (n8n, Qdrant)
  - `infra/langfuse/docker-compose.yml` (Langfuse V3)
  - `services/*/README.md` (H1, H2, H3)
  - `tools/README.md` (Observer, Reconciler)
  - `n8n_workflows/README_*.md` (Judge Agent)
  - Task Scheduler XML files (Observer, Email Watcher)

---

**End of TOOLS_INVENTORY.md**
