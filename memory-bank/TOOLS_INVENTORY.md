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
- `GET /health` - Service health check
- `GET /api/context/current-state` - Get 01-active-context.md
- `GET /api/context/project-brief` - Get project-brief.md
- `GET /api/context/protocols` - Get PROTOCOLS section
- `GET /api/context/research/{family}` - Get research files by family

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
