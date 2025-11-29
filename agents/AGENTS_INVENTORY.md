ï»¿# Agents Inventory - ×××× ××¡××× ×× ×××¢×¨××ª

---

## ××××ª ×¡××× ××

| AgentName | OldPath | Role | StatusFromAudit | SuggestedRoleInAIOS | Notes |
|-----------|---------|------|-----------------|---------------------|-------|
| **Local Execution Agent** | `agents/local_execution_agent.py` | ×××¦××¢ ×¤×¢××××ª ××§×××××ª ×¢× ××××©× (×§×××¥ placeholder ××¡××¡×) | ××× | ×¡××× ×¢××¨ / Archive | ××§×××¥ ×××× ×¨×§ ×××¤×¡×ª Hello World. ×××¨×© ×××××: ××× ×× ××× ××ª××× × ××¤××ª×× ×¢×ª××× ×× ×©×¨×§ placeholder? |
| **GPT GitHub Agent** | `gpt_agent/github_agent.py` | ××ª×× × ××©××××ª GitHub ××× ×ª× ××× ×× × ×××©×ª××© ××¤× CAPABILITIES_MATRIX. ×¤××¢× ×××¦× DRY RUN. | ××× | ×¡××× ×××× | ××× ×¡××× ××ª×××× ×©××ª×× × ×¤×¢××××ª ×¢× ××¡××¡ ××¡××× DESIGN ×-CAPABILITIES_MATRIX. ×××××¥ ××××× ×××¤×ª× ×¢××. |
| **MCP Master Control Program** | `mcp/` (×× ××ª××§×××) | ××× ×©× ×××¢×¨××ª: × ×××× ×¡××× ××, ×ª××××, ××× ×××¨×¦×××ª (GitHub, Google), ×-API server | ××× | Workflow Engine / ×¡××× ×××× | ×××× clients, servers ×-integrations. ××× ×"×××" ×©× ××¢×¨××ª ××¡××× ××. ×××¨×© ×¤××¨××§ ××¨×××××: `mcp/server/` â workflows/, `mcp/clients/` â tools/ |
| **GitHub Executor API** | `mcp/server/worker/` + ×ª××¢×× ×-CAPABILITIES_MATRIX | API ××××××¦×× ×©× GitHub (×§×× ×××, deployment ××¡××) | ××× (××ª××× ×) | ××× / API Wrapper | ××¤× CAPABILITIES_MATRIX ×× ×§×× ×××× ×©×××× ×-deployment. ×××××¥ ×××¢×××¨ ×-`tools/` ×¢× ×ª××¢×× ×××. |
| **Autopilot / Self-Healing Agent** | `autopilot.py` + `autopilot-state.json` | ×¡××× ××××× ×¢×¦×××ª (Self-Healing) - ×× ×¡× ××©×××¨ ×××©× ×-Google Sheets | × ××¡××/××©× | Archive / ×¡××× ×¢××¨ | × ×¨×× ×-POC ×©× ×× ×× ×× ×××××. ×××¨×© ×××××: ××× ×¨×××× ×× ×¢××××? |
| **OPS Decision Manager** | `ops/decisions/` | × ×××× ××××××ª ×ª×¤×¢×××××ª (ADRs - Architectural Decision Records) | ××× | Workflow Component | ×××× ×§××¦× ××××× ××× `2025-11-02-L2-approval.md`. ××ª××× ×-`workflows/` ×× `docs/decisions/` |
| **OPS Diagnostics** | `ops/diag/` | ××× ××××× ×××××§××ª ××¢×¨××ª | ××× | Workflow Component | ×××× `cloudshell_check.md`, `REMOTE_MCP_EVIDENCE.md` ×××'. ××ª××× ×-`workflows/diagnostics/` |
| **GitHub Executor Bootstrap** | `ops/TRIGGERS/github_executor_bootstrap.md` | ××¡×× bootstrap ×××¤×¢××ª GitHub Executor | ××× | Workflow Documentation | ×ª××¢×× ××¨×××¨×× ×××¤×¢×× - ××ª××× ×-`workflows/` |
| **Chat1 Telegram Interface Agent** | `chat/telegram_bot.py` | ×××©×§ ××××¨× ×¨×©×× ×-AI-OS, ××××¨ ×¢× Agent Gateway | ××× | ×¡××× UI ×¨×©×× | ×××©×§ ××××¨× ×××× ×-AI-OS. Human-in-the-Loop ×¢× ××¤×ª××¨× ×××©××¨. ×××××¨ ×-GPT Planner |

---

## Non-Repo Prototypes (×¤×¨××××××¤×× ×©×× ×× ××××× ××¡××× ××)

| ×©× | ×ª××××¨ | ×¡××××¡ | ××¢×¨××ª |
|------|-------|-------|-------|
| **Telegram + Small LLM Prototype** | ×¤×¨××××××¤ ×××¦×× × ×©××××¨ ××××¨× ×-LLM ×§×× ××¨× HTTP ×¤×©×× | ðï¸ Legacy / External | ×× ×××§ ××¨××¤× ai-os. ××× × ×××××¨ ×-Agent Gateway. ×©×××© ×× ××¡×× ×¨××©×× × ××××. **××¡××¨ ××× ××ª ×¢××× ×ª×××××× ×¨×©××××** |

> â ï¸ **××©××**: ××¡××× ××¨×©×× ××××× ××××©×§ ××××¨× ××× **Chat1** ×©× ××¦× ×-`chat/telegram_bot.py`. ×× ×¤×¨××××××¤ ×××¨ ××× ×× ××¡×× ×××× × ×××§ ××××¨××××§×××¨× ×©× AI-OS.

---

## ×¡×××× ×××¦×××

### ×¡××× ×× ×©×××× ××××¨××¨:
1. **GPT GitHub Agent** â ×¡××× ×××× ××ª×××× (××ª×× × ××©××××ª)
2. **MCP** â ×ª×©×ª××ª/×× ××¢ × ×××× ××¨××× (×× ×¡××× ×××× ××× ××¢×¨××ª)
3. **GitHub Executor API** â ××× ××××××¦×× (API wrapper)
4. **Autopilot** â ×¡××× ××××× ×¢×¦×××ª (× ×¨×× POC)
5. **Local Execution Agent** â placeholder / ×× ××¤××ª×

### ×¨××××× ×ª×¤×¢××××× (×× ××××¨× "×¡××× ××" ××× ×ª××××××):
- **OPS/decisions** â ×× ×× ××××××ª
- **OPS/diag** â ××× ×××××
- **OPS/TRIGGERS** â ×× ×× ×× × ××¤×¢××

---

## ×××¨×× ×©×××¨×©×× ××××× ×× ××©××ª

1. **Local Execution Agent**: ××× ×× ××× ××××¨ ×××××ª ×¡××× ××××ª× ×× ×¡×ª× placeholder? ×¦×¨×× ×××××× ×× ×××¨××§ ×× ××¤×ª×.

2. **MCP Structure**: ××ª××§××× `mcp/` ×¢× ×§××ª ×××××× ×©×¨×ª××, ××§××××ª ×××× ×××¨×¦×××ª. ×¦×¨×× ××¤×¨×§ ×××ª× ××¨×××××:
   - `mcp/server/` â `workflows/mcp-server/`
   - `mcp/clients/` â `tools/mcp-clients/`
   - `mcp/github/`, `mcp/google/` â `tools/integrations/`

3. **Autopilot Status**: ××× ×× ×× ×× ×××××× ××¢×¦×××ª ×¢×××× ×¨×××× ××? ×× ×× - ×¦×¨×× ××©××¨× ×××ª×¢×. ×× ×× - ×××¨××.

4. **OPS Components**: ××× `ops/` ××× ×××§ ×××¢×¨××ª ××¡××× ×× ×× ×¨×§ ××× ×ª×¤×¢×× ×ª×××? ××© ×¦××¨× ××××× × ××¨××¨×.

5. **GitHub Executor API**: ×§×× ×××× ×©×××× ×-deployment. ×¦×¨×× ××××××:
   - ××× ××××× ××× ×©×××?
   - ××× ××©×× ×××¢×¨××ª MCP?
   - ××× ×××¤×× ×××× ×¢×¦××× ×-`tools/`?

---

## ××××¦××ª ×¦×¢× ×××

1. **×××ª××× ×¢× GPT GitHub Agent**:
   - ××××× ××ª `gpt_agent/github_agent.py` â `agents/gpt-github-agent/`
   - ××××× ××ª ××¡××× ××ª××¢×× ×× ××××× (AGENT_GPT_MASTER_DESIGN.md ×××')
   - ×××¦××¨ README.md ××ª××§××× ×©××¡×××¨ ×ª×¤×§××, dependencies ×××¨×¦×

2. **××ª×¢× ××ª MCP ×-Workflow Engine**:
   - ×××¦××¨ `workflows/MCP_OVERVIEW.md`
   - ×××××× ×¢× ×¤××¨××§ ××¨×××××

3. **×××¢×××¨ ××ª GitHub Executor API ×-tools/**:
   - ×××¦××¨ `tools/github-executor-api/`
   - ××ª×¢× deployment requirements

4. **×××¨×× ××ª Autopilot**:
   - ×××¢×××¨ ×-`archive/autopilot/` ××× ×× ××© ××××× ×××¨×ª

---

## ×¡××× ×× ×¤×¢×××× (2025-11-24)

### GPT AI-OS Manager
| ×ª××× × | ×¤××¨×× |
|--------|-------|
| **×©×** | AI-OS GitHub Manager |
| **×¤×××¤××¨××** | ChatGPT Custom GPT |
| **×¡××××¡** | â Operational |
| **××××××ª** | GitHub (read/write/PR) + Google Workspace (×××) |
| **×××××¨** | ngrok â localhost:8082 |

**×¤×¢××××ª ×××× ××ª**:
- ×§×¨×××ª ×§××¦×× ×-GitHub
- ××¦××¨×ª Pull Requests
- ×©××××ª ××××××××
- ××¦××¨×ª ×××¨××¢×× ×××××
- ×××¤××© ×§××¦×× ×-Drive
- ××¦××¨×ª ××¡××× Google Docs
- ××¦××¨×ª ×××××× ××ª Google Sheets
- ××¦××¨×ª ××©××××ª

---

## ×©××¨××ª×× ×ª××××× (Backend Services)

### MCP GitHub Client
| ×ª××× × | ×¤××¨×× |
|--------|-------|
| **Port** | 8081 |
| **×¡××××¡** | â Operational |
| **×××§××** | `services/mcp_github_client/` |
| **×ª××¢××** | `services/mcp_github_client/README.md` |

### Google Workspace Client
| ×ª××× × | ×¤××¨×× |
|--------|-------|
| **Port** | 8082 |
| **×¡××××¡** | â Operational |
| **×××§××** | `services/google_workspace_client/` |
| **×ª××¢××** | `services/google_workspace_client/README.md` |
| **Auth** | OAuth 2.0 (edri2or@gmail.com) |

---

**×¡××××¡**: â ×××¤×× ×¨××©×× × ×××©×× + ×¡××× ×× ×¤×¢××××  
**×¦×¢× ×××**: Deploy ×-Cloud (×ª××× ×¤×¢××)

---

## Claude Desktop

**Role:** Primary Executor  
**Status:** ✅ Operational  
**Last Verified:** 2025-11-29

### Integration Method

**GitHub Access:**
- Method: PowerShell → HTTP API calls
- Server: MCP GitHub Client (localhost:8081)
- Tool: Windows-MCP:Powershell-Tool
- Protocol: HTTP REST API (not stdio MCP)

**Other Integrations:**
- Google Workspace: google-mcp (OAuth, read-only)
- Windows: Windows-MCP (PowerShell, app control, filesystem)
- File System: filesystem-mcp (local file access)

### Verified Operations (2025-11-29)

✅ **GitHub Operations:**
- Read files from repository
- List repository tree structure
- Create Pull Requests (PR #22, #23, #24 created successfully)
- Write files to main branch
- Delete files
- List branches
- Get commit history

✅ **HTTP API Endpoints Used:**
- /github/read-file - Fetch file content
- /github/open-pr - Create Pull Requests
- /github/list-tree - Browse repository
- /health - Server health check

### Example Usage

```powershell
# Read file from GitHub
$body = @{ path = "README.md"; ref = "main" } | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:8081/github/read-file" `
    -Method Post -Body $body -ContentType "application/json"

# Create PR
$prBody = @{
    title = "Update documentation"
    description = "Description here..."
    files = @(
        @{ path = "docs/file.md"; content = "..."; operation = "create" }
    )
    base_branch = "main"
} | ConvertTo-Json -Depth 10

$pr = Invoke-RestMethod -Uri "http://localhost:8081/github/open-pr" `
    -Method Post -Body $prBody -ContentType "application/json"
```

### Related

- **DEC-011:** Claude Desktop HTTP Integration
- **MCP GitHub Server:** services/mcp_github_client/
- **Test PRs:** #22, #23, #24