# n8n Infrastructure Setup

**Status:** INFRA_ONLY (Phase 2.3)  
**Purpose:** n8n Automation Kernel for AI-OS  
**Decision:** DEC-006 (approved)

---

## 🎯 What is this?

This directory contains the infrastructure setup for n8n - the automation kernel of AI-OS.

**Current Phase (2.3):**
- ✅ n8n running locally in Docker
- ✅ Basic auth configured
- ✅ Data persistence enabled
- ✅ **Daily Context Sync Orchestrator V1** (SLICE_DAILY_CONTEXT_SYNC_N8N_V1)
- ❌ No live workflows yet (no Gmail/Calendar/Tasks)

**Future Phase (2.4+):**
- Workflows connecting to Google Workspace
- Workflows connecting to GitHub
- Controlled automation with Human-in-the-Loop

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Copy template to .env
cp ENV_TEMPLATE.env .env

# Edit .env and change:
# - N8N_BASIC_AUTH_PASSWORD (choose a secure password)
# - N8N_ENCRYPTION_KEY (generate with: openssl rand -base64 32)
```

### 2. Start n8n

```bash
# Start in background
docker-compose up -d

# Check logs
docker-compose logs -f n8n

# Check health
docker-compose ps
```

### 3. Access n8n

Open: http://localhost:5678

**Default credentials (change in .env):**
- Username: admin
- Password: CHANGE_ME

---

## 📁 Directory Structure

```
infra/n8n/
├── docker-compose.yml    # Docker setup
├── ENV_TEMPLATE.env      # Environment variables template
├── .env                  # Actual env vars (DO NOT commit)
├── workflows/            # n8n workflow exports (version controlled)
│   └── daily_context_sync_orchestrator_v1.json
├── data/                 # n8n data directory (created on first run)
│   ├── database.sqlite   # SQLite database
│   └── credentials/      # Encrypted credentials
└── README.md             # This file
```

---

## 📦 Available Workflows

### DAILY_CONTEXT_SYNC_ORCHESTRATOR_V1

**Status:** ✅ Available (SLICE_DAILY_CONTEXT_SYNC_N8N_V1)  
**File:** `workflows/daily_context_sync_orchestrator_v1.json`  
**Purpose:** Orchestrate Daily Context Sync through Agent Kernel with trace_id

**What it does:**
1. Generates unique `trace_id` for the execution
2. Logs `N8N_WORKFLOW_STARTED` event to EVENT_TIMELINE
3. Calls Agent Kernel endpoint `/daily-context-sync/run` with trace_id
4. Checks success/error status
5. Logs `N8N_WORKFLOW_COMPLETE` or `N8N_WORKFLOW_ERROR` to EVENT_TIMELINE
6. (Optional) Runs State Layer Reconciler

**How to use:**

1. **Import workflow into n8n:**
   - Open n8n UI: http://localhost:5678
   - Click "Import from File"
   - Select `workflows/daily_context_sync_orchestrator_v1.json`
   - Click "Import"

2. **Prerequisites:**
   - Agent Kernel must be running on port 8084
   - OS Core MCP must be running on port 8083

3. **Execute workflow:**
   - Open the workflow in n8n
   - Click "Execute Workflow" button
   - Watch execution log for trace_id

4. **Enable Reconciler (optional):**
   - Open workflow editor
   - Find "Run Reconciler (Optional)" node
   - Right-click → "Enable"
   - Save workflow

**Trace IDs:**
Every execution generates a trace_id in format: `n8n-dcs-{timestamp}-{random}`

Example: `n8n-dcs-1732748400-abc123`

You can find this trace_id in:
- n8n execution log
- EVENT_TIMELINE.jsonl events
- Agent Kernel logs

---

## 🔐 Security Notes

1. **Never commit .env file** - it contains sensitive credentials
2. **Change default password** - use a strong password
3. **Generate encryption key** - used for credentials storage
4. **Keep data/ directory secure** - contains workflows and credentials

---

## 🛠️ Management Commands

```bash
# Start n8n
docker-compose up -d

# Stop n8n
docker-compose down

# Restart n8n
docker-compose restart

# View logs
docker-compose logs -f n8n

# Update n8n to latest version
docker-compose pull
docker-compose up -d

# Backup data
tar -czf n8n-backup-$(date +%Y%m%d).tar.gz data/

# Remove all (including data)
docker-compose down -v
```

---

## 🧪 Testing Workflows

### Test Daily Context Sync Orchestrator

```bash
# 1. Start all services
cd services/agent_kernel
python kernel_server.py &

cd services/os_core_mcp
python server.py &

cd infra/n8n
docker-compose up -d

# 2. Import and execute workflow in n8n UI

# 3. Verify results
# - Check n8n execution log for trace_id
# - Check EVENT_TIMELINE.jsonl for N8N_WORKFLOW_* events
# - Check SYSTEM_STATE_COMPACT.json for updated last_daily_context_sync_utc
```

---

## 📋 Next Steps (Phase 2.4+)

1. **Credentials Setup:**
   - Add Google OAuth credentials
   - Add GitHub token
   - Add any other integration credentials

2. **Workflow Development:**
   - Add Cron triggers to Daily Context Sync
   - Create more workflows (Weekly Summary, etc.)
   - Get approval from Or for each workflow

3. **Integration:**
   - Connect to AI-OS State Layer (✅ Done for Daily Context Sync)
   - Enable webhook endpoints
   - Set up monitoring and logging

---

## 🔗 Related Documentation

- **Slice:** `docs/slices/SLICE_DAILY_CONTEXT_SYNC_N8N_V1.md`
- **Decision:** `docs/DECISIONS_AI_OS.md` (DEC-006)
- **Infra Map:** `docs/INFRA_MAP.md`
- **Services Status:** `docs/system_state/registries/SERVICES_STATUS.json`
- **n8n Official Docs:** https://docs.n8n.io/

---

**Last Updated:** 2025-11-27  
**Updated By:** Claude Desktop (SLICE_DAILY_CONTEXT_SYNC_N8N_V1)  
**Phase:** 2.3 - INFRA_ONLY
