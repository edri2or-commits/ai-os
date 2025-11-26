# INFRA_MAP.md — מפת תשתיות ואינטגרציות

**Version:** 0.1  
**Created:** 2025-11-26  
**Last Updated:** 2025-11-26 (Block STATE_LAYER_COMPLETION_V1)  
**Purpose:** מיפוי מרכזי של כל השירותים, הכלים והחיבורים במערכת AI-OS

---

## 📊 טבלת שירותים ואינטגרציות

| Service ID | Name | Type | Status | Connected Via | Primary Use | Notes / Risks |
|------------|------|------|--------|---------------|-------------|---------------|
| `github` | GitHub | code_hosting | ✅ up | MCP GitHub Client (8081) + Claude MCP | Repo management, code storage | Full R/W access via GPT Actions |
| `google-gmail` | Gmail | email | ✅ up | Google Workspace Client (8082) | Send/read emails | OAuth 2.0, edri2or@gmail.com |
| `google-calendar` | Google Calendar | calendar | ✅ up | Google Workspace Client (8082) | Event management | OAuth 2.0 |
| `google-drive` | Google Drive | storage | ✅ up | Google Workspace Client (8082) + Claude MCP | File search, Drive Snapshot | Read-heavy, write via client |
| `google-docs` | Google Docs | documents | ✅ up | Google Workspace Client (8082) | Doc creation | Used for SYSTEM_SNAPSHOT_DRIVE |
| `google-sheets` | Google Sheets | spreadsheets | 🟡 partial | Google Workspace Client (8082) | Data storage | Not heavily used yet |
| `google-tasks` | Google Tasks | tasks | 🟡 partial | Google Workspace Client (8082) | Task creation | Not heavily used yet |
| `ngrok` | ngrok Tunnel | networking | ✅ up | CLI + start-all-services.bat | Public URL for GPT Actions | ⚠️ URL changes on restart |
| `claude-desktop` | Claude Desktop | agent | ✅ up | Local app + MCPs | Primary executor, local access | Full system access |
| `gpt-actions` | GPT Custom Actions | agent | ✅ up | HTTPS via ngrok | Planner, architecture | Depends on ngrok URL |
| `telegram-chat1` | Chat1 Telegram Bot | ui | 🟡 partial | telegram_bot.py | Human interface | Code ready, not deployed persistently |
| `n8n` | n8n Automation | automation | 📋 planned | Docker (planned) | Workflow automation | Not configured yet |
| `make` | Make.com | automation | ❓ unknown | External SaaS | Automation platform | Status unclear |
| `docker` | Docker | containerization | 📋 planned | Local Docker Desktop | Service deployment | Not in active use |

---

## 🔌 Connection Architecture

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
│  └─────────────────────┘    └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                      │                       │
                      ▼                       ▼
              ┌───────────────┐    ┌─────────────────────┐
              │ GitHub API    │    │ Google Workspace    │
              └───────────────┘    └─────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   Claude Desktop (Local)                     │
├─────────────────────────────────────────────────────────────┤
│  MCPs: GitHub, Filesystem, Windows, Google, Canva, Browser  │
│  Direct repo access: C:\Users\edri2\Work\AI-Projects\...    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Authentication & Secrets

| Service | Auth Type | Token Location | Status |
|---------|-----------|----------------|--------|
| GitHub (MCP) | OAuth | Claude Desktop App | ✅ Secure |
| GitHub (Client) | PAT | Environment / .env | ✅ Configured |
| Google Workspace | OAuth 2.0 | token.json (auto-refresh) | ✅ Secure |
| ngrok | API Key | ngrok config | ✅ Configured |
| Telegram | Bot Token | .env / SSOT | ⚠️ Review needed |
| OpenAI GPT | API Key | .env | ✅ Configured |

---

## ⚠️ Known Issues / Gaps

### Critical
- **ngrok URL instability**: URL changes on every restart → must update GPT Actions manually
- **No persistent deployment**: All services require local machine running

### High Priority
- **Chat1 not deployed persistently**: Code ready but not running as service
- **n8n not configured**: Planned for automation but not set up yet

### Medium Priority
- **Make.com status unknown**: May or may not be in use
- **Google Sheets/Tasks underutilized**: Connected but not integrated into workflows
- **Drive Snapshot sync is manual**: No auto-refresh mechanism

### Low Priority
- **Docker not in active use**: Prepared but not deployed
- **Legacy MCP code exists**: In make-ops-clean, not migrated

---

## 📋 Service Status Summary

| Status | Count | Services |
|--------|-------|----------|
| ✅ up | 8 | github, gmail, calendar, drive, docs, ngrok, claude-desktop, gpt-actions |
| 🟡 partial | 3 | sheets, tasks, telegram-chat1 |
| 📋 planned | 2 | n8n, docker |
| ❓ unknown | 1 | make |

---

## 🔗 Related Documents

- **Detailed status**: `docs/system_state/registries/SERVICES_STATUS.json`
- **Agent capabilities**: `docs/system_state/agents/AGENT_CAPABILITY_PROFILE.md`
- **System snapshot**: `docs/SYSTEM_SNAPSHOT.md`
- **Control plane**: `docs/CONTROL_PLANE_SPEC.md`

---

**Last Updated:** 2025-11-26  
**Updated By:** Claude Desktop (Block STATE_LAYER_COMPLETION_V1)
