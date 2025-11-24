# System Snapshot – AI-OS Current State
### Date: 2025-11-24

---

## 🎯 System Overview

AI-OS is a personal AI operating system with integrated services for GitHub and Google Workspace operations, controlled via Custom GPT Actions.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GPT Custom Actions                        │
│              (AI-OS GitHub + Google Manager)                │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTPS (ngrok)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Local Services                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │ MCP GitHub Client   │    │ Google Workspace Client     │ │
│  │ Port: 8081          │    │ Port: 8082                  │ │
│  ├─────────────────────┤    ├─────────────────────────────┤ │
│  │ • /github/read-file │    │ • /google/gmail/send        │ │
│  │ • /github/list-tree │    │ • /google/gmail/list        │ │
│  │ • /github/open-pr   │    │ • /google/calendar/*        │ │
│  │                     │    │ • /google/drive/search      │ │
│  │                     │    │ • /google/sheets/*          │ │
│  │                     │    │ • /google/docs/create       │ │
│  │                     │    │ • /google/tasks/create      │ │
│  └─────────────────────┘    └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                      │                       │
                      ▼                       ▼
              ┌───────────────┐    ┌─────────────────────┐
              │ GitHub API    │    │ Google Workspace    │
              │ (edri2or-     │    │ (edri2or@gmail.com) │
              │  commits/     │    │ OAuth 2.0           │
              │  ai-os)       │    └─────────────────────┘
              └───────────────┘
```

---

## ✅ Active Services

### 1. MCP GitHub Client
- **Status**: ✅ Operational
- **Port**: 8081
- **Repository**: `edri2or-commits/ai-os`
- **Endpoints**:
  | Endpoint | Description |
  |----------|-------------|
  | POST `/github/read-file` | Read file content from repo |
  | POST `/github/list-tree` | List repository structure |
  | POST `/github/open-pr` | Create Pull Request with changes |
- **Location**: `services/mcp_github_client/`

### 2. Google Workspace Client
- **Status**: ✅ Operational
- **Port**: 8082
- **Auth**: OAuth 2.0 (edri2or@gmail.com)
- **Endpoints**:
  | Endpoint | Description |
  |----------|-------------|
  | POST `/google/gmail/send` | Send email |
  | POST `/google/gmail/list` | List emails |
  | POST `/google/calendar/create-event` | Create calendar event |
  | POST `/google/calendar/list-events` | List events |
  | POST `/google/drive/search` | Search Drive files |
  | POST `/google/sheets/create` | Create spreadsheet |
  | POST `/google/sheets/read` | Read spreadsheet data |
  | POST `/google/docs/create` | Create Google Doc |
  | POST `/google/tasks/create` | Create task |
- **Location**: `services/google_workspace_client/`

### 3. ngrok Tunnel
- **Status**: ✅ Active
- **URL**: `https://beauish-supersweetly-twila.ngrok-free.dev`
- **Target**: Port 8082 (Google Workspace Client)
- **Note**: URL changes on restart - must update GPT Actions

---

## 🤖 GPT Integration

### Custom GPT: AI-OS GitHub Manager
- **Platform**: ChatGPT
- **Actions Configured**:
  - GitHub operations (via localhost:8081 or ngrok)
  - Google Workspace operations (via ngrok → localhost:8082)
- **Authentication**: None (ngrok provides public URL)
- **Status**: ✅ Tested and working

### Tested Operations
| Operation | Status | Test Date |
|-----------|--------|-----------|
| GitHub Read File | ✅ Working | 2025-11-23 |
| GitHub List Tree | ✅ Working | 2025-11-23 |
| GitHub Open PR | ✅ Working | 2025-11-23 |
| Gmail Send | ✅ Working | 2025-11-24 |
| Google Docs Create | ✅ Working | 2025-11-24 |

---

## 📁 Key Files & Locations

```
ai-os-claude-workspace/
├── services/
│   ├── mcp_github_client/          # GitHub API service
│   │   ├── main.py
│   │   ├── api/routes_github.py
│   │   ├── core/mcp_github_client.py
│   │   └── INTEGRATION_GUIDE.md
│   │
│   └── google_workspace_client/    # Google Workspace service
│       ├── main.py
│       ├── api/
│       │   ├── routes_gmail.py
│       │   ├── routes_calendar.py
│       │   ├── routes_drive.py
│       │   ├── routes_sheets.py
│       │   ├── routes_docs.py
│       │   └── routes_tasks.py
│       └── core/google_client.py
│
├── credentials.json                 # Google OAuth client config
├── token.json                       # Google OAuth token (auto-refresh)
├── start_github_client.py          # Start GitHub service
├── start-all-services.bat          # Start ALL services (one click)
└── Dockerfile                       # For cloud deployment (planned)
```

---

## 🚀 How to Start

### Option 1: One-Click Start (Recommended)
Double-click: `start-all-services.bat`

This starts:
1. GitHub Client (port 8081)
2. Google Workspace Client (port 8082)
3. ngrok tunnel

### Option 2: Manual Start
```powershell
# Terminal 1: GitHub Client
python start_github_client.py

# Terminal 2: Google Workspace Client
python -m uvicorn services.google_workspace_client.main:app --port 8082 --reload

# Terminal 3: ngrok
ngrok http 8082
```

---

## ⚠️ Known Limitations

1. **ngrok URL changes on restart** - Must update GPT Actions each time
2. **Services require local machine running** - No cloud deployment yet
3. **GitHub Client not exposed via ngrok** - Only Google Workspace is public

---

## 💬 Chat & User Interfaces

### Chat1 – Telegram UI (Official)

| Property | Value |
|----------|-------|
| **Status** | 🚧 Implemented in Code, Not Fully Deployed |
| **Location** | `chat/telegram_bot.py` |
| **Architecture** | Telegram → Bot → Agent Gateway → GPT Planner → Action Executor |
| **Interface** | Hebrew, Human-in-the-Loop with approval buttons |
| **Token** | Configured in SSOT (`.env.local` → `TELEGRAM_BOT_TOKEN`) |

**What Chat1 Does:**
- Receives natural language intents from Telegram
- Calls Agent Gateway (`ai_core/agent_gateway.py`)
- Presents plan to user with ✅/❌ buttons
- Executes only after explicit approval

**Current State:**
- ✅ Code implemented and functional
- ✅ Integrated with GPT Planner (ai_core/gpt_orchestrator.py)
- ⚠️ Not deployed as persistent service (requires manual startup)
- ⚠️ Requires OPENAI_API_KEY in environment

---

### Legacy / External Prototypes (Not Part of AI-OS)

There exists an **external Telegram prototype** outside this repository:
- Uses a "small LLM" (different from GPT Planner) via simple HTTP server
- Was used for early experimentation only
- **Not managed as part of AI-OS architecture**
- **Not connected to Agent Gateway**
- Should not be used for production workflows

> ⚠️ **Important**: Only Chat1 (`chat/telegram_bot.py`) is the official Telegram interface for AI-OS.

---

## 🔮 Next Steps (Planned)

1. [ ] Deploy to Google Cloud Run (always-on, no ngrok needed)
2. [ ] Fixed domain for GPT Actions
3. [ ] Merge both services into single unified service
4. [ ] Add more Google Workspace operations (Calendar edit, Drive upload)
5. [ ] Deploy Chat1 as persistent service

---

## 📊 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-23 | Initial MCP GitHub Client |
| 2.0 | 2025-11-24 | Added Google Workspace Client, GPT integration |

---

**Last Updated**: 2025-11-24
**Status**: ✅ Operational
