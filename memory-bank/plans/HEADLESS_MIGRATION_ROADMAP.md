# AI Life OS: Headless Migration Roadmap

**תאריך:** 2025-12-05  
**Lead טכני:** Claude (Technical Implementation Lead)  
**יועץ אסטרטגי:** GPT Deep Research (Strategic Advisory)  
**משתמש:** Or Edri (Product Owner + Approver)  
**סטטוס:** Roadmap Ready for Approval

---

## 📋 Executive Summary

AI Life OS עובר שינוי אסטרטגי: מעבר מ-**Desktop-Dependent Architecture** ל-**Headless/Always-On Architecture**.

**המטרה:**
- Claude Desktop/GPT/Gemini הופכים ל-**clients** של המערכת (לא המקום שבו היא "גרה")
- n8n + Qdrant + Git = **Core** (רץ 24/7, בלי תלות במחשב דולק)
- **Multi-Model Orchestration** אפשרי (route tasks לכל LLM לפי צורך + עלות)

**הממצא המרכזי:** 70% מהמערכת כבר Headless! צריך רק 3 API wrappers.

**Timeline:** 11-15 שעות, spread over 7-10 days (ADHD-friendly pacing)  
**Cost:** +$2/mo (VPS) for 24/7 uptime + multi-model capability  
**Risk:** Low-Medium (incremental, reversible changes)

---

## 🎯 Why This Migration? Strategic Justification

### Problem Statement (Pain Points of Current Architecture)

**A. Single Point of Failure (PC Dependency):**
- PC shutdown → Observer stops, Judge Agent missed, drift undetected
- Windows updates → forced restart → all processes killed
- Travel / laptop closed → system offline
- Power outage → everything halts

**B. Interactive Bottleneck (Claude Desktop Dependency):**
- MCP servers down → Email Watcher can't read Gmail
- Context lost → new Claude instance = amnesia (AP-XXX pattern)
- Can't delegate to GPT/Gemini (they don't have MCP access)
- Approval workflows blocked (need Claude Desktop open)

**C. Platform Lock-in (Windows-Specific):**
- Task Scheduler = Windows only
- Desktop Commander = PowerShell + Windows paths
- Can't deploy to cloud (no GUI, no Claude Desktop)

**D. No Multi-Model Orchestration:**
- Stuck with one model's capabilities
- Can't route fast tasks → GPT-4o, deep reasoning → o1
- Price optimization impossible

### Solution: Headless Core + Multi-Client Architecture

```
┌─────────────────────────────────────────────────────────┐
│        Headless Core (VPS - Always On)                  │
│        n8n + Qdrant + Langfuse + Git                    │
├─────────────────────────────────────────────────────────┤
│  API Gateway Layer                                      │
│  ├─ /api/gmail/*        (google-mcp wrapper)            │
│  ├─ /api/context/*      (Memory Bank)                   │
│  └─ /api/approvals/*    (HITL queue)                    │
└─────────────────────────────────────────────────────────┘
               ↑ HTTP APIs ↑
    ┌──────────┴────┬──────────┬─────────┐
    │               │          │         │
┌───┴────┐   ┌──────┴───┐  ┌───┴──┐  ┌──┴─────┐
│Claude  │   │ GPT-4o   │  │  o1  │  │ Gemini │
│Desktop │   │ (fast)   │  │(deep)│  │ (free) │
└────────┘   └──────────┘  └──────┘  └────────┘
```

**Benefits:**
- ✅ **24/7 Uptime:** No PC dependency
- ✅ **Multi-Model:** Route to optimal LLM (cost + capability)
- ✅ **Scalable:** Add new clients easily (Perplexity, Claude Opus, etc.)
- ✅ **Observable:** Langfuse dashboard shows all activity
- ✅ **Reversible:** Git + approval queue safety nets
- ✅ **ADHD-Friendly:** Async approvals, Telegram notifications

---

## 📊 Current State Analysis

### Infrastructure Topology (What's Running Where)

| Component | Location | PC Dependency | Claude Desktop Dependency | Status |
|-----------|----------|---------------|---------------------------|--------|
| n8n workflows | Docker (localhost) | ✅ Yes | ❌ No | ✅ Operational |
| Qdrant vector DB | Docker (localhost) | ✅ Yes | ❌ No | ✅ Operational |
| Langfuse observability | Docker (localhost) | ✅ Yes | ❌ No | ✅ Operational (6/6 services) |
| Observer drift detection | Task Scheduler | ✅ Yes | ❌ No | ✅ Every 15min |
| Watchdog (Git→Qdrant) | Task Scheduler | ✅ Yes | ❌ No | ✅ Every 15min |
| Judge Agent V2 | n8n workflow | ✅ Yes | ❌ No | ✅ Every 6hr |
| **MCP Servers** | stdio pipes | ✅ Yes | ✅ **Yes** | ⚠️ **Blocked** |
| **HITL Approvals** | Chat UI | ❌ No | ✅ **Yes** | ⚠️ **Blocked** |
| **Context Loading** | Local files | ✅ Yes | ⚠️ Partial | ⚠️ **Gap** |

**Key Finding:** 70% already Headless! Only need API wrappers for:
1. MCP servers (stdio → HTTP)
2. HITL approvals (Chat UI → Telegram Bot)
3. Context loading (files → REST API)

---

## 🗺️ Migration Roadmap: 4 Slices

### Overview

| Slice | Duration | Complexity | Priority | Dependencies |
|-------|----------|------------|----------|--------------|
| **H1: MCP→REST Gateway** | 2-3 hours | Low | 🔴 Critical | None |
| **H2: Memory Bank API** | 2 hours | Low | 🟡 Medium | None |
| **H3: Telegram Approval Bot** | 3-4 hours | Medium | 🟠 High | None |
| **H4: VPS Deployment** | 4-6 hours | Medium | 🟢 Future | H1+H2+H3 |
| **Total Effort** | **11-15 hours** | - | - | Spread 7-10 days |

---

### 🔴 Slice H1: MCP → REST Gateway (Proof-of-Concept)

**Duration:** 2-3 hours  
**Risk:** Low (additive, non-breaking)  
**Goal:** Prove GPT can send Gmail without Claude Desktop

#### What We're Building

```
services/api-gateway/
├── server.js          // Express server wrapping google-mcp
├── package.json       // Dependencies: express, cors, body-parser
├── openapi.yaml       // API documentation (Swagger)
└── README.md          // Setup + usage guide
```

**API Endpoints:**
```http
POST /api/gmail/send
  Headers: { Authorization: "Bearer <token>" }
  Body: {
    "to": "recipient@example.com",
    "subject": "Test Subject",
    "body": "Test body content"
  }
  Response: {
    "success": true,
    "messageId": "1234567890abcdef"
  }
```

#### How It Works (Architecture)

```
External Client (GPT/Gemini)
    ↓ HTTP POST
API Gateway (Express server on :8080)
    ↓ spawn subprocess
google-mcp process (stdio)
    ↓ stdin: JSON-RPC request
    ↓ stdout: JSON-RPC response
API Gateway parses response
    ↓ HTTP 200
Client receives JSON
```

**Key Implementation Details:**

1. **Process Management:**
   ```javascript
   const { spawn } = require('child_process');
   
   function callMCP(method, params) {
     return new Promise((resolve, reject) => {
       const mcp = spawn('google-mcp.exe', [], {
         env: { ...process.env, GOOGLE_MCP_CREDENTIALS: "..." }
       });
       
       const request = {
         jsonrpc: "2.0",
         method: method,
         params: params,
         id: Date.now()
       };
       
       mcp.stdin.write(JSON.stringify(request) + '\n');
       mcp.stdout.on('data', (data) => resolve(JSON.parse(data)));
       mcp.stderr.on('data', (err) => reject(err));
     });
   }
   ```

2. **Error Handling:**
   - MCP process crash → 500 Internal Server Error
   - Invalid params → 400 Bad Request
   - Authentication fail → 401 Unauthorized

3. **Security:**
   - API key authentication (Bearer token)
   - Rate limiting (100 req/hour per key)
   - CORS whitelisting (localhost + approved domains)

#### Definition of Done ✅

- [ ] **Files Created:**
  - [ ] `services/api-gateway/server.js` (Express server)
  - [ ] `services/api-gateway/package.json` (dependencies)
  - [ ] `services/api-gateway/openapi.yaml` (API docs)
  - [ ] `services/api-gateway/README.md` (usage guide)
  - [ ] `services/api-gateway/.env.example` (config template)

- [ ] **Testing:**
  - [ ] curl test successful (Gmail sent)
  - [ ] **GPT test successful:**
    - Fresh GPT chat
    - Send OpenAPI spec
    - Ask: "Send me email via this API"
    - Email received ✅
  - [ ] Error handling tested (invalid params, MCP crash)

- [ ] **Documentation:**
  - [ ] OpenAPI spec complete (Swagger UI accessible)
  - [ ] README with curl examples
  - [ ] Security considerations documented

- [ ] **Git:**
  - [ ] Commit: `feat(api-gateway): MCP-REST wrapper POC (Gmail)`
  - [ ] Update Memory Bank: 01-active-context.md
  - [ ] Update SYSTEM_BOOK.md (new capability)

#### Testing Protocol

```bash
# Test 1: Local curl
curl -X POST http://localhost:8080/api/gmail/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-api-key-123" \
  -d '{
    "to": "or@example.com",
    "subject": "API Gateway Test",
    "body": "This email was sent via the new API Gateway! 🎉"
  }'

# Expected: { "success": true, "messageId": "..." }

# Test 2: GPT Integration
# 1. Fresh GPT chat (no context)
# 2. Upload: services/api-gateway/openapi.yaml
# 3. Prompt: "Send me an email using this API. Use subject: 'Hello from GPT' and body: 'This proves multi-model orchestration works!'"
# 4. Verify: Email received in inbox ✅
```

#### Rollback Plan

If something breaks:
```bash
# Stop the API Gateway
cd services/api-gateway
npm stop

# Revert Git commit
git revert HEAD

# System returns to Claude Desktop only (previous state)
```

---

### 🟡 Slice H2: Memory Bank API (Context for External LLMs)

**Duration:** 2 hours  
**Risk:** Low (read-only API)  
**Goal:** GPT/Gemini load project context in < 30 seconds

#### What We're Building

```
services/context-api/
├── main.py           // FastAPI server
├── requirements.txt  // fastapi, uvicorn, python-dotenv
└── README.md         // API documentation
```

**API Endpoints:**

```http
GET /api/context/current-state
  → Returns: 01-active-context.md (Phase, %, Recent Changes, Next Steps)

GET /api/context/project-brief
  → Returns: project-brief.md (Vision, TL;DR, Architecture)

GET /api/context/research/{family}
  → Returns: Research files by family
  → Example: /api/context/research/architecture
  → Response: { "family": "architecture", "files": [...], "content": "..." }

GET /api/context/protocols
  → Returns: All protocols (MAP-001, AEP-001, TFP-001, etc.)

GET /api/context/life-graph
  → Returns: Life Graph entities (Areas, Projects, Contexts)
```

#### Response Format

```json
{
  "content": "# QUICK STATUS\n\nAI Life OS | Phase 2...",
  "metadata": {
    "path": "memory-bank/01-active-context.md",
    "last_modified": "2025-12-05T20:30:00Z",
    "git_sha": "a1b2c3d",
    "size_bytes": 68432,
    "line_count": 1254
  }
}
```

#### Implementation (Python FastAPI)

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from datetime import datetime
import subprocess

app = FastAPI(
    title="AI Life OS Context API",
    description="Provides project context to external LLMs",
    version="1.0.0"
)

# CORS - allow GPT/Gemini access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["GET"],
    allow_headers=["*"],
)

MEMORY_BANK = Path(__file__).parent.parent.parent / "memory-bank"

def get_git_sha():
    """Get current Git commit SHA"""
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=MEMORY_BANK.parent,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

@app.get("/api/context/current-state")
def get_current_state():
    """Returns 01-active-context.md"""
    file = MEMORY_BANK / "01-active-context.md"
    if not file.exists():
        raise HTTPException(404, "Current state file not found")
    
    return {
        "content": file.read_text(encoding="utf-8"),
        "metadata": {
            "path": str(file.relative_to(MEMORY_BANK.parent)),
            "last_modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat(),
            "git_sha": get_git_sha(),
            "size_bytes": file.stat().st_size
        }
    }

@app.get("/api/context/project-brief")
def get_project_brief():
    """Returns project-brief.md"""
    file = MEMORY_BANK / "project-brief.md"
    if not file.exists():
        raise HTTPException(404, "Project brief not found")
    
    return {
        "content": file.read_text(encoding="utf-8"),
        "metadata": {
            "path": str(file.relative_to(MEMORY_BANK.parent)),
            "last_modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
        }
    }

@app.get("/api/context/research/{family}")
def get_research(family: str):
    """Returns research files by family"""
    research_dir = MEMORY_BANK.parent / "claude-project" / "research_claude"
    files = list(research_dir.glob(f"*{family}*.md"))
    
    if not files:
        raise HTTPException(404, f"No research files found for family: {family}")
    
    return {
        "family": family,
        "files": [
            {
                "filename": f.name,
                "path": str(f.relative_to(MEMORY_BANK.parent)),
                "size_bytes": f.stat().st_size,
                "content": f.read_text(encoding="utf-8")
            }
            for f in files
        ],
        "count": len(files)
    }
```

#### Definition of Done ✅

- [ ] **Files Created:**
  - [ ] `services/context-api/main.py` (FastAPI server)
  - [ ] `services/context-api/requirements.txt`
  - [ ] `services/context-api/README.md`
  - [ ] `services/context-api/.env.example`

- [ ] **Endpoints Working:**
  - [ ] `/api/context/current-state` returns valid JSON
  - [ ] `/api/context/project-brief` returns valid JSON
  - [ ] `/api/context/research/{family}` returns files
  - [ ] `/docs` (auto-generated Swagger UI) accessible

- [ ] **GPT Onboarding Test:**
  - [ ] Fresh GPT chat (no prior context)
  - [ ] Send prompt: "Load my AI Life OS context from http://localhost:8081/api/context/current-state"
  - [ ] Ask follow-up: "What's Phase 2 status? What are the next 2-3 steps?"
  - [ ] GPT answers accurately:
    - Phase 2: ~70% complete
    - Recent: Judge V2 cleanup
    - Next: Enhanced Judge, Teacher Agent, or continue Phase 2
  - [ ] ✅ Onboarding time < 30 seconds

- [ ] **Git:**
  - [ ] Commit: `feat(context-api): Memory Bank REST API`
  - [ ] Update Memory Bank (new capability)
  - [ ] OpenAPI docs auto-generated

#### Testing Protocol

```bash
# Test 1: Start server
cd services/context-api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8081

# Test 2: curl
curl http://localhost:8081/api/context/current-state | jq .metadata
# Expected: {"path": "...", "last_modified": "...", "git_sha": "a1b2c3d"}

# Test 3: GPT Integration
# Fresh GPT chat, prompt:
"""
Load my AI Life OS project context from this API:
http://localhost:8081/api/context/current-state

After loading, answer these questions:
1. What Phase is the project in and what % complete?
2. What was the most recent work completed?
3. What are the next 2-3 recommended steps?
"""

# Expected GPT response (accurate):
"""
Based on the context loaded:

1. **Phase 2: Architectural Alignment (~70% complete)**
2. **Most Recent:** Judge V2 Cleanup + Memory Bank Sync (verified state: 1 workflow active, 0 duplicates)
3. **Next Steps:**
   - Option A: Test Langfuse Dashboard (15 min, familiarization)
   - Option B: Document Meta-Learning (20 min, BP/AP creation)
   - Option C: Enhanced Judge Integration (45 min, connect to Langfuse)
"""
```

---

### 🟠 Slice H3: Telegram Approval Bot (HITL Headless)

**Duration:** 3-4 hours  
**Risk:** Medium (new dependency: Telegram Bot API)  
**Goal:** Async approvals via Telegram, no Claude Desktop required

#### What We're Building

```
services/approval-bot/
├── bot.py            // Telegram bot (python-telegram-bot)
├── database.py       // SQLite for pending approvals
├── requirements.txt  // python-telegram-bot, aiosqlite
├── .env.example      // TELEGRAM_BOT_TOKEN, CHAT_ID
└── README.md         // Setup guide
```

**Approval Workflow:**

```
1. Reconciler detects drift
   ↓
2. Generates CR (Change Request)
   ↓
3. POST /api/approvals
   {
     "cr_id": "CR_2025-12-05_001",
     "type": "TRUTH_RECONCILIATION",
     "risk": "low",
     "proposal": [...]
   }
   ↓
4. Approval Bot receives webhook
   ↓
5. Stores CR in SQLite (status: PENDING)
   ↓
6. Sends Telegram message:
   "🔔 Change Request Approval
   
   ID: CR_2025-12-05_001
   Type: TRUTH_RECONCILIATION
   Risk: low
   
   [✅ Approve] [❌ Reject] [📄 View Diff]"
   ↓
7. User clicks button (Telegram inline keyboard)
   ↓
8. Callback received (callback_data: "approve:CR_2025-12-05_001")
   ↓
9. Update SQLite (status: APPROVED)
   ↓
10. Write approval file: truth-layer/drift/approvals/CR_2025-12-05_001_APPROVED.json
   ↓
11. Executor watches this directory (inotify/watchdog)
   ↓
12. Executor runs: applies CR, commits to Git
   ↓
13. Bot updates Telegram message:
   "✅ Applied at 20:45
   Commit: a1b2c3d"
```

#### Implementation (Python + Telegram Bot API)

```python
# bot.py
import os
import json
from pathlib import Path
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import aiosqlite

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))  # Your Telegram user ID
APPROVALS_DIR = Path("truth-layer/drift/approvals")
APPROVALS_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = "approvals.db"

async def init_db():
    """Initialize SQLite database"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS approvals (
                cr_id TEXT PRIMARY KEY,
                type TEXT,
                risk TEXT,
                proposal TEXT,
                status TEXT,
                created_at TEXT,
                updated_at TEXT,
                telegram_message_id INTEGER
            )
        """)
        await db.commit()

async def send_approval_request(cr_data: dict):
    """Send CR to Telegram for approval"""
    cr_id = cr_data['cr_id']
    
    # Store in DB
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO approvals (cr_id, type, risk, proposal, status, created_at)
            VALUES (?, ?, ?, ?, 'PENDING', ?)
        """, (
            cr_id,
            cr_data['type'],
            cr_data['risk'],
            json.dumps(cr_data['proposal']),
            datetime.utcnow().isoformat()
        ))
        await db.commit()
    
    # Build message
    proposal_summary = json.dumps(cr_data['proposal'], indent=2)[:500]  # Truncate
    message = f"""
🔔 **Change Request Approval**

**ID:** `{cr_id}`
**Type:** {cr_data['type']}
**Risk:** {cr_data['risk']}

**Proposal:**
```
{proposal_summary}
```
"""
    
    # Inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve:{cr_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject:{cr_id}")
        ],
        [InlineKeyboardButton("📄 View Full Diff", callback_data=f"diff:{cr_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send to Telegram
    app = Application.builder().token(TOKEN).build()
    msg = await app.bot.send_message(
        chat_id=CHAT_ID,
        text=message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    # Update DB with message ID
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE approvals SET telegram_message_id = ? WHERE cr_id = ?",
            (msg.message_id, cr_id)
        )
        await db.commit()

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    action, cr_id = query.data.split(":", 1)
    
    if action == "approve":
        # Update DB
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE approvals SET status = 'APPROVED', updated_at = ? WHERE cr_id = ?",
                (datetime.utcnow().isoformat(), cr_id)
            )
            await db.commit()
        
        # Write approval file (triggers Executor)
        approval_file = APPROVALS_DIR / f"{cr_id}_APPROVED.json"
        approval_file.write_text(json.dumps({
            "status": "approved",
            "timestamp": datetime.utcnow().isoformat(),
            "approved_by": "telegram_user"
        }))
        
        # Update Telegram message
        await query.edit_message_text(
            text=query.message.text + "\n\n✅ **Approved!** Executor is running...",
            parse_mode='Markdown'
        )
        await query.answer("✅ Approved! Executor triggered.")
    
    elif action == "reject":
        # Update DB
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE approvals SET status = 'REJECTED', updated_at = ? WHERE cr_id = ?",
                (datetime.utcnow().isoformat(), cr_id)
            )
            await db.commit()
        
        # Write rejection file
        rejection_file = APPROVALS_DIR / f"{cr_id}_REJECTED.json"
        rejection_file.write_text(json.dumps({
            "status": "rejected",
            "timestamp": datetime.utcnow().isoformat(),
            "rejected_by": "telegram_user"
        }))
        
        # Update Telegram message
        await query.edit_message_text(
            text=query.message.text + "\n\n❌ **Rejected**",
            parse_mode='Markdown'
        )
        await query.answer("❌ Rejected.")
    
    elif action == "diff":
        # Fetch full proposal from DB
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT proposal FROM approvals WHERE cr_id = ?",
                (cr_id,)
            ) as cursor:
                row = await cursor.fetchone()
        
        if row:
            proposal = json.loads(row[0])
            diff_text = "**Full Proposal:**\n```json\n" + json.dumps(proposal, indent=2) + "\n```"
            await query.answer()
            await context.bot.send_message(
                chat_id=CHAT_ID,
                text=diff_text,
                parse_mode='Markdown'
            )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "🤖 AI Life OS Approval Bot\n\n"
        "I'll send you Change Requests for approval.\n"
        "Click the buttons to approve or reject."
    )

def main():
    """Start the bot"""
    app = Application.builder().token(TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    # Initialize DB
    import asyncio
    asyncio.run(init_db())
    
    # Start polling
    print("Bot started! Listening for approvals...")
    app.run_polling()

if __name__ == "__main__":
    main()
```

#### Security Features

1. **Chat ID Whitelist:**
   ```python
   # Only allow specific Telegram user
   if update.effective_chat.id != CHAT_ID:
       await update.message.reply_text("⛔ Unauthorized")
       return
   ```

2. **Audit Trail:**
   - Every approval/rejection logged in SQLite
   - Timestamp + user ID recorded
   - Approval files in Git (truth-layer/drift/approvals/)

3. **Privacy Mode:**
   - Bot configured via @BotFather with Privacy Mode: Enabled
   - Bot cannot read group chat messages (only direct commands)

#### Definition of Done ✅

- [ ] **Telegram Bot Setup:**
  - [ ] Bot created via @BotFather
  - [ ] Token saved to `.env`
  - [ ] Chat ID retrieved (send `/start` to bot, log user ID)
  - [ ] Privacy Mode enabled

- [ ] **Files Created:**
  - [ ] `services/approval-bot/bot.py`
  - [ ] `services/approval-bot/database.py`
  - [ ] `services/approval-bot/requirements.txt`
  - [ ] `services/approval-bot/README.md`
  - [ ] `services/approval-bot/.env.example`

- [ ] **Testing:**
  - [ ] Manual approval test:
    - POST approval to API (simulate Reconciler)
    - Telegram notification received < 5 sec
    - Buttons work (Approve/Reject/Diff)
    - Approval triggers executor
    - Telegram message updated with status
  - [ ] End-to-end test:
    - Observer detects drift
    - Reconciler generates CR
    - Telegram notification
    - User approves
    - Executor applies CR
    - Git commit successful
    - Audit trail in truth-layer/drift/approvals/

- [ ] **Integration:**
  - [ ] Reconciler updated to POST approvals
  - [ ] Executor watches approval directory (file watcher)
  - [ ] Langfuse traces approval flow

- [ ] **Git:**
  - [ ] Commit: `feat(approval-bot): Telegram HITL workflow`
  - [ ] Update Memory Bank

#### Testing Protocol

```bash
# Setup
cd services/approval-bot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Get your Chat ID
python bot.py
# Send /start to bot in Telegram
# Bot logs: "User 123456789 sent /start"
# Add this ID to .env: TELEGRAM_CHAT_ID=123456789

# Test 1: Manual approval
python test_approval.py
# Script POSTs test CR to API
# Expected:
# - Telegram message received
# - Buttons visible
# - Click "Approve" → executor file created

# Test 2: End-to-end
# 1. Manually edit truth-layer/drift/reports/OBSERVED_STATE.json
# 2. Wait for Observer (15min) or trigger manually
# 3. Reconciler generates CR
# 4. Telegram notification ✅
# 5. Approve via button
# 6. Executor runs
# 7. Git commit applied
# 8. Verify with: git log --oneline -5
```

---

### 🟢 Slice H4: VPS Deployment (Future - 24/7 Uptime)

**Duration:** 4-6 hours (first deployment)  
**Risk:** Medium (new platform, secrets management)  
**Goal:** True always-on, PC-independent

#### Provider Selection (Based on DR2 Analysis)

**Recommended:** Hetzner Cloud CPX31  
**Specs:** 4 vCPU, 8GB RAM, 160GB NVMe SSD  
**Cost:** €14.76/mo (~$16/mo)  
**Location:** Falkenstein or Nuremberg, Germany (60-80ms from Israel)

**Why Hetzner over DigitalOcean:**
- 30% cost advantage for same specs
- NVMe storage (crucial for Qdrant performance)
- 20TB egress included (vs 1TB DO)
- AMD EPYC CPUs (better multi-threading)

**Alternative:** Fly.io (Free Tier)  
**Pros:** $0/mo for 3 shared-cpu VMs  
**Cons:** Shared CPU = variable performance, may not support full stack

#### Migration Checklist

**Phase 1: VPS Provisioning (1 hour)**
- [ ] Create Hetzner account
- [ ] Provision CPX31 instance (Ubuntu 24.04 LTS)
- [ ] Configure SSH keys (disable password login)
- [ ] Setup UFW firewall:
  ```bash
  ufw allow 22/tcp   # SSH
  ufw allow 80/tcp   # HTTP
  ufw allow 443/tcp  # HTTPS
  ufw enable
  ```
- [ ] Install Docker + docker-compose:
  ```bash
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker $USER
  ```
- [ ] Install Fail2Ban (SSH brute-force protection)

**Phase 2: Git + Secrets (1 hour)**
- [ ] Clone repo:
  ```bash
  git clone https://github.com/edri2or-commits/ai-os.git
  cd ai-os
  ```
- [ ] Copy secrets to VPS (secure transfer):
  ```bash
  # Local machine
  scp .env user@vps-ip:/opt/ai-os/.env
  
  # Or use Hetzner secrets management
  ```
- [ ] Verify `.gitignore` excludes secrets:
  ```bash
  git check-ignore .env  # Should return: .env
  ```

**Phase 3: Docker Stack Deployment (2 hours)**
- [ ] Create `docker-compose.prod.yml`:
  ```yaml
  version: '3.8'
  
  services:
    caddy:
      image: caddy:2-alpine
      restart: unless-stopped
      ports:
        - "80:80"
        - "443:443"
      volumes:
        - ./Caddyfile:/etc/caddy/Caddyfile
        - caddy_data:/data
        - caddy_config:/config
      networks:
        - ai_os_net
    
    api-gateway:
      build: ./services/api-gateway
      restart: unless-stopped
      env_file: .env
      networks:
        - ai_os_net
    
    context-api:
      build: ./services/context-api
      restart: unless-stopped
      env_file: .env
      networks:
        - ai_os_net
    
    approval-bot:
      build: ./services/approval-bot
      restart: unless-stopped
      env_file: .env
      networks:
        - ai_os_net
    
    n8n:
      image: n8nio/n8n:latest
      restart: unless-stopped
      env_file: .env
      volumes:
        - n8n_data:/home/node/.n8n
      networks:
        - ai_os_net
    
    qdrant:
      image: qdrant/qdrant:latest
      restart: unless-stopped
      env_file: .env
      volumes:
        - qdrant_data:/qdrant/storage
      networks:
        - ai_os_net
    
    langfuse-web:
      # ... (6 Langfuse services)
  
  networks:
    ai_os_net:
      driver: bridge
  
  volumes:
    caddy_data:
    caddy_config:
    n8n_data:
    qdrant_data:
  ```

- [ ] Create `Caddyfile`:
  ```
  api.ai-os.example.com {
    reverse_proxy api-gateway:8080
  }
  
  context.ai-os.example.com {
    reverse_proxy context-api:8081
  }
  
  langfuse.ai-os.example.com {
    reverse_proxy langfuse-web:3000
  }
  ```

- [ ] Deploy stack:
  ```bash
  docker-compose -f docker-compose.prod.yml up -d
  ```

- [ ] Verify health:
  ```bash
  docker ps  # All containers running
  docker logs -f caddy  # Auto-HTTPS working
  curl https://api.ai-os.example.com/health  # 200 OK
  ```

**Phase 4: Cron → Systemd (1 hour)**
- [ ] Convert Observer to systemd timer:
  ```ini
  # /etc/systemd/system/observer.service
  [Unit]
  Description=AI Life OS Observer
  
  [Service]
  Type=oneshot
  WorkingDirectory=/opt/ai-os
  ExecStart=/opt/ai-os/venv/bin/python tools/observer.py
  User=ai-os
  ```
  
  ```ini
  # /etc/systemd/system/observer.timer
  [Unit]
  Description=Run Observer every 15 minutes
  
  [Timer]
  OnBootSec=5min
  OnUnitActiveSec=15min
  
  [Install]
  WantedBy=timers.target
  ```

- [ ] Enable timers:
  ```bash
  sudo systemctl enable observer.timer
  sudo systemctl start observer.timer
  sudo systemctl enable watchdog.timer
  sudo systemctl start watchdog.timer
  ```

**Phase 5: Git Webhook (30 min)**
- [ ] Setup GitHub webhook:
  - Repo Settings → Webhooks → Add webhook
  - Payload URL: `https://api.ai-os.example.com/webhooks/github`
  - Secret: (generate strong secret)
  - Events: `push` to `main` branch

- [ ] Create webhook handler:
  ```python
  # services/api-gateway/webhook.py
  @app.post("/webhooks/github")
  async def github_webhook(request: Request):
      # Verify signature
      signature = request.headers.get("X-Hub-Signature-256")
      # ... verify with secret
      
      # Pull latest code
      subprocess.run(["git", "pull"], cwd="/opt/ai-os")
      
      # Restart services
      subprocess.run(["docker-compose", "restart"], cwd="/opt/ai-os")
      
      return {"status": "deployed"}
  ```

**Phase 6: Monitoring + Backups (1 hour)**
- [ ] Setup Uptime Kuma (self-hosted monitoring):
  ```bash
  docker run -d -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma
  ```

- [ ] Configure 3-2-1 backup:
  - 3 copies: Local (VPS), Remote (GitHub), Archive (S3-compatible)
  - 2 media: Disk (VPS SSD), Object Storage (Backblaze B2)
  - 1 offsite: Backblaze B2 (€5/mo for 50GB)

- [ ] Backup script:
  ```bash
  #!/bin/bash
  # backup.sh - runs daily via cron
  
  # Backup Git repo
  cd /opt/ai-os
  git push origin main
  
  # Backup Docker volumes
  docker run --rm \
    -v n8n_data:/data \
    -v /backup:/backup \
    alpine tar czf /backup/n8n_$(date +%Y%m%d).tar.gz /data
  
  # Upload to B2
  b2 sync /backup b2://ai-os-backups/$(date +%Y%m)
  ```

#### Cost Breakdown (Monthly)

| Item | Cost | Notes |
|------|------|-------|
| Hetzner CPX31 | €14.76 (~$16) | 4 vCPU, 8GB RAM, 20TB egress |
| Domain (ai-os.example.com) | $1 | Amortized ($12/year) |
| Backblaze B2 (50GB) | $0.30 | First 10GB free |
| **Subtotal** | **$17.30** | Infrastructure |
| OpenAI API (GPT-4o) | $4 | Usage-based (current) |
| **Total** | **$21.30/mo** | vs $14/mo (local PC power) |

**Net Δ:** +$7/mo for 24/7 uptime + multi-model capability

**ROI:**
- Multi-model routing → 40% API cost savings
- PC idle time → $10/mo power savings
- **Effective Δ:** ~$1/mo for always-on infrastructure

#### Definition of Done ✅

- [ ] VPS provisioned + hardened
- [ ] Docker stack deployed (all services healthy)
- [ ] Caddy auto-HTTPS working (Let's Encrypt)
- [ ] Systemd timers running (Observer, Watchdog)
- [ ] Git webhook deployed (auto-deploy on push)
- [ ] Monitoring dashboard accessible
- [ ] Backup script tested (restore successful)
- [ ] Cost < $25/mo verified
- [ ] Uptime > 99.9% (7-day test)
- [ ] Multi-model access tested (GPT + Claude via APIs)
- [ ] Documentation: VPS_DEPLOYMENT_GUIDE.md

---

## 📐 Architecture Diagrams

### Current State (Desktop-Dependent)

```
┌─────────────────────────────────────────────────────┐
│         Windows 11 PC (Single Point of Failure)     │
├─────────────────────────────────────────────────────┤
│  Claude Desktop (Interactive Only)                  │
│  ├─ MCP Servers (stdio) - google-mcp, n8n-mcp      │
│  └─ Desktop Commander (PowerShell + Windows paths) │
├─────────────────────────────────────────────────────┤
│  Docker Services (24/7 if PC on)                   │
│  ├─ n8n:5678                                        │
│  ├─ qdrant:6333                                     │
│  └─ langfuse stack (6 services)                     │
├─────────────────────────────────────────────────────┤
│  Task Scheduler (Windows-specific)                  │
│  ├─ Observer (every 15min)                          │
│  ├─ Watchdog (every 15min)                          │
│  └─ Email Watcher (periodic)                        │
└─────────────────────────────────────────────────────┘
```

### Target State (Headless Always-On)

```
┌─────────────────────────────────────────────────────────────┐
│              VPS (Hetzner CPX31 - Always On)                │
│              Ubuntu 24.04 + Docker Compose                  │
├─────────────────────────────────────────────────────────────┤
│  Caddy (Reverse Proxy + Auto-HTTPS)                        │
│  ├─ api.ai-os.example.com → api-gateway:8080               │
│  ├─ context.ai-os.example.com → context-api:8081           │
│  └─ langfuse.ai-os.example.com → langfuse-web:3000         │
├─────────────────────────────────────────────────────────────┤
│  API Services (Docker internal network)                    │
│  ├─ api-gateway:8080 (MCP→REST wrapper)       [H1] ✅      │
│  ├─ context-api:8081 (Memory Bank API)        [H2] ✅      │
│  ├─ approval-bot:8082 (Telegram HITL)         [H3] ✅      │
│  ├─ n8n:5678 (orchestration)                               │
│  ├─ qdrant:6333 (vector memory)                            │
│  └─ langfuse stack (observability - 6 services)            │
├─────────────────────────────────────────────────────────────┤
│  Systemd Timers (cron replacement)                         │
│  ├─ observer.timer (every 15min)                           │
│  └─ watchdog.timer (every 15min)                           │
├─────────────────────────────────────────────────────────────┤
│  Git Truth Layer                                            │
│  └─ /opt/ai-os/ (clone from GitHub)                        │
└─────────────────────────────────────────────────────────────┘
                   ↑ HTTPS APIs ↑
      ┌────────────┴────┬──────────┬─────────┐
      │                 │          │         │
  ┌───┴────┐     ┌──────┴───┐  ┌───┴──┐  ┌──┴─────┐
  │Claude  │     │ GPT-4o   │  │  o1  │  │ Gemini │
  │Desktop │     │ (fast)   │  │(deep)│  │ (free) │
  └────────┘     └──────────┘  └──────┘  └────────┘
  (Architect)    (Executor)    (Analyst) (Scout)
  
  Any device:    Desktop, Laptop, Phone, Tablet
  Any location:  Home, Travel, Office
```

---

## 🔒 Security Architecture

### Network Isolation (Defense in Depth)

```
Internet (Untrusted)
    ↓
Firewall (UFW)
  - Allow: 22 (SSH), 80 (HTTP), 443 (HTTPS)
  - Deny: All other ports
    ↓
Caddy (TLS Termination + Reverse Proxy)
  - Auto-HTTPS (Let's Encrypt)
  - Rate limiting (100 req/min per IP)
  - CORS policies
    ↓
Docker Bridge Network (ai_os_net - Trusted)
  - api-gateway (public)
  - context-api (public)
  - approval-bot (public, webhook only)
  - n8n (internal only, no port mapping)
  - qdrant (internal only)
  - langfuse (internal only)
```

**Key Principle:** Only Caddy exposes ports to host. All internal services communicate via Docker DNS.

### Authentication & Authorization

| Service | Auth Method | Access Control |
|---------|-------------|----------------|
| API Gateway | Bearer token (API key) | Rate limiting + CORS |
| Context API | None (read-only public data) | - |
| Approval Bot | Telegram Chat ID whitelist | Only authorized user |
| n8n | Internal only (no external access) | Docker network isolation |
| Qdrant | API key (QDRANT__SERVICE__API_KEY) | Internal only |
| Langfuse | Basic Auth (admin panel) | Internal only |

### Secrets Management

**Local Development:**
- `.env` file (gitignored)
- Desktop Commander reads from .env

**VPS Deployment:**
- Hetzner Cloud: Use "User Data" for initial secrets
- Fly.io: `fly secrets set KEY=value`
- Docker: `env_file: .env` (file encrypted at rest)

**Rotation Policy:**
- API keys: Rotate quarterly
- Telegram bot token: Rotate on compromise
- Database passwords: Rotate annually

### Audit Logging

All actions logged to:
1. **Langfuse:** API calls, LLM interactions, traces
2. **Git:** Truth Layer changes (who, what, when)
3. **SQLite:** Approval decisions (Telegram bot)
4. **Syslog:** System events (systemd, Docker)

---

## 📊 Success Metrics & Validation

### Phase 1: Local Headless (H1+H2+H3)

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| **GPT sends email (H1)** | ✅ Success | curl + GPT test |
| **GPT loads context < 30s (H2)** | ✅ < 30 sec | GPT onboarding test |
| **CR approval < 10s (H3)** | ✅ < 10 sec | End-to-end timing |
| **Judge Agent operational** | ✅ No regression | Existing workflow runs |
| **Langfuse traces all APIs** | ✅ 100% coverage | Dashboard verification |
| **Zero downtime** | ✅ No outages | Monitoring (local Docker) |

### Phase 2: Cloud Deployment (H4)

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| **VPS uptime** | ≥ 99.9% | Uptime Kuma dashboard |
| **API response time** | < 500ms (p95) | Langfuse latency metrics |
| **Cost** | < $25/mo | Monthly invoice |
| **Backup restore** | < 30 min | Manual restore test |
| **Multi-model routing** | ✅ Working | GPT + Claude both functional |
| **PC power off** | ✅ System still running | Manual test (shutdown PC) |

### Regression Testing (After Each Slice)

**Critical Workflows (Must Not Break):**
- [ ] Observer detects drift (every 15min)
- [ ] Judge Agent runs (every 6hr)
- [ ] Watchdog indexes Memory Bank (every 15min)
- [ ] Langfuse records traces
- [ ] Git commits work
- [ ] n8n workflows execute

**Testing Protocol:**
```bash
# After each slice
cd tests
pytest -v  # All 44 tests must pass

# Specific workflow test
python -m tools.test_judge_agent

# End-to-end smoke test
python -m tools.smoke_test
```

---

## 🚨 Risk Analysis & Mitigation

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| MCP wrapper fails | Medium | High | Error handling, fallback to Claude Desktop |
| Telegram bot API rate limit | Low | Medium | Batch notifications, respect limits |
| VPS provider outage | Low | High | Backup to secondary provider (Fly.io) |
| Cost overrun | Low | Medium | Budget alerts, cap at $25/mo |
| Data loss | Low | Critical | 3-2-1 backup strategy |
| Security breach | Low | Critical | Firewall, auth, audit logs |

### Process Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing workflows | Medium | High | Regression tests before each slice |
| User confusion (new workflow) | Medium | Medium | Clear docs + Telegram bot onboarding |
| Time estimate exceeded | Medium | Low | ADHD-friendly pacing, 2-3 days per slice |
| Technical debt accumulation | Medium | Medium | Protocol 1 (auto-documentation) |

### Rollback Strategy

**If something breaks:**

1. **Immediate:** Stop new service
   ```bash
   docker stop api-gateway
   # System reverts to Claude Desktop only
   ```

2. **Git Revert:**
   ```bash
   git revert HEAD
   git push origin main
   ```

3. **Restore Backup (worst case):**
   ```bash
   # Restore Git repo
   git reset --hard <last-known-good-commit>
   
   # Restore Docker volumes
   docker run --rm \
     -v n8n_data:/data \
     -v /backup:/backup \
     alpine tar xzf /backup/n8n_backup.tar.gz -C /data
   ```

---

## 📚 References & Research Foundation

### Architectural Decisions
- **ADR-001:** Hexagonal Architecture (Ports & Adapters) as canonical pattern
- **CANONICAL_TERMINOLOGY.md:** Official terms dictionary
- **METAPHOR_GUIDE.md:** When to use which metaphor

### Research Reports
- **DR1:** Architectural Validation (this is "note_20251205_202412.md")
- **DR2:** Comprehensive Implementation Report (this is "note_20251205_203736.md")
- **HEADLESS_ARCHITECTURE_ANALYSIS.md:** Strategic analysis by Claude + GPT

### Industry Standards
- **MCP Specification:** Model Context Protocol (Anthropic)
- **OpenTelemetry:** Observability standard (Langfuse implements this)
- **Docker Compose:** IaC standard for container orchestration
- **Telegram Bot API:** Official Telegram documentation
- **Let's Encrypt:** Free SSL/TLS certificates

### Infrastructure Providers
- **Hetzner Cloud:** VPS pricing analysis (DR2, Section 1.1.1)
- **Caddy:** Reverse proxy selection rationale (DR2, Section 2.1)
- **n8n:** Open-source automation (already operational)

---

## ✅ Approval & Next Steps

### Questions for Or (Product Owner)

**1. Roadmap Approval:**
- ✅ Agree with 3 slices (H1+H2+H3)?
- ✅ Order makes sense? (MCP-REST → Context API → Telegram Bot)
- ⚠️ Any changes to priorities?

**2. Timeline:**
- Start H1 now, or wait?
- Pace: 1 slice every 2-3 days acceptable?

**3. Budget:**
- $0 for H1+H2+H3 (local) - approved?
- ~$16/mo for H4 (VPS) - approved?
- Cap at $25/mo total?

**4. Risk Tolerance:**
- Comfortable with incremental changes?
- Prefer more testing, or move fast?

**5. GPT Involvement:**
- When to consult GPT for strategic advice?
- Which decisions need GPT input?

### If Approved → Immediate Next Step

**Slice H1: MCP-REST Gateway (Gmail POC)**
- Duration: 2-3 hours
- Risk: Low
- Starting now unless Or says otherwise

**Git Branch:**
```bash
git checkout -b feature/h1-mcp-rest-gateway
```

**Deliverables:**
- `services/api-gateway/server.js`
- `services/api-gateway/openapi.yaml`
- `services/api-gateway/README.md`
- GPT test successful (email sent via API)

---

## 📝 Change Log

**Version 1.0 (2025-12-05):**
- Initial roadmap created
- 4 slices defined (H1-H4)
- Architecture diagrams complete
- Cost analysis included
- Risk mitigation strategies documented
- Testing protocols defined

---

**End of Document**

**Status:** Ready for Or's approval  
**Next Action:** Or reviews + approves → Claude starts H1  
**Contact:** Or Edri (Product Owner), Claude (Technical Lead), GPT (Strategic Advisor)
