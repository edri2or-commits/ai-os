ï»¿# AI-OS â ××××××ª ×××× (Core Decisions)

**×××¨×ª ×××¡××**: ×ª××¢×× ××××××ª ××¡××¨×××××ª ×××¨××××§××× ×××ª ×××¢×¨××ª AI-OS.

**×¤××¨××**: ×× ××××× ××ª××¢××ª ×¢× ×ª××¨××, ××§×©×¨, ××××× ××¨×¦××× ×.

---

## 2025-11-20 â ××××× #1: MCP Orchestration

### ××§×©×¨
××¢×¨××ª ×-MCP (Master Control Program) ××××ª× ××¢×¨××ª ×××¨×××ª ×× ×××× ×¡××× ××, ×ª×××× ×××× ×××¨×¦×××ª. ××× ×××××ª:
- `mcp/server/` - ×©×¨×ª ××¨×××
- `mcp/clients/` - ××§××××ª (web, iOS shortcuts)
- `mcp/github/` - ××× ×××¨×¦×××ª GitHub
- `mcp/google/` - ××× ×××¨×¦×××ª Google

**×©×××**: ××× ××××× ××ª MCP ××§×× ×¨×¥ ×-AI-OS?

### ××××××
**MCP ×× × ××§× ××§×× ×¨×¥ ×-AI-OS.**

- **×¡××××¡**: ðï¸ Legacy / Reference Only
- **×©××××©**: ××©××© ×××§××¨ ×¢××¦×× ××××¢ ××××
- **×××**: ×¤×¨××¡×, ××¤×¢××, ×× ×©××××© ××§×××× ××§××

### ×¨×¦××× ×

**××× ×× ×××××?**
1. **×××¨××××ª ×××××**: MCP ××ª×¤×ª× ×××¨×× ××ª ×××© ×× ×¨×××× ×¨××× ×©×× ××××¨× ××ª××¢×××.
2. **×ª×××ª ××ª×©×ª××ª**: ××× × ×× × ×¡××× ×ª×©×ª××ª ×¡×¤×¦××¤××ª (Cloud Run, Workflows) ×©×× ××××¨× × ×××¦× ×-AI-OS.
3. **×¢×§×¨×× Data-First**: AI-OS × ×× × ×××¤×¡ ×¢× ×¢×§×¨×× ××ª × ×§×××. ×¢×××£ ××× ××ª ×ª×©×ª××ª ×¤×©××× ×××¡×××¨×ª.

**×× ×× ×××§×××?**
- **×ª××× ××ª ×¢××¦××**: ××× MCP ×¤×ª×¨ ××¢×××ª ×©× ×ª××××, ××× ×××¨×¦×××ª, ×× ×××× ×¡××× ××.
- **××¤××¡× ×¢××××**: ×× ×¢×× ×××, ×× ××.
- **××¡××× ×ª××¢××**: ×××× ×¢××¨× ××¨××¤× ×××××¨ ×¢×××.

**×× ×××§××?**
- ××¢×ª××, ×× × ×××§×§ ××× ×× ×× orchestration - × ×× × ××× ×¤×©×× ×××××××¨× ×××¤×¡.
- ××¨××¢: ××× ×¦××¨× ××× ×× ×× ××¨×××. ××¡××× ×× ×¤××¢××× ×× ×¤×¨×.

### ××©×¤×¢× ×¢× CAPABILITIES_MATRIX
- **MCP-001**: MCP Orchestration â ðï¸ Legacy (Reference Only)
- **MCP-002**: MCP GitHub Integration â ðï¸ Legacy (Reference Only)
- **MCP-003**: MCP Google Integration â ðï¸ Legacy (Reference Only)

---

## 2025-11-20 â ××××× #2: GitHub Executor API

### ××§×©×¨
××¨××¤× ×××©× ×§××× ×§×× ××× ×©× `github-executor-api` - ×©××¨××ª Cloud Run ×©××¡×¤×§ API ×××××××¦×× ×©× GitHub. ××§××:
- ××××§× ×-`cloud-run/google-workspace-github-api/`
- ×××× 2 endpoints: health check + update file
- ××ª××× × ×-deployment ×-Cloud Run
- **××¢××**: Deployment ××¡×× (××¡×¨ GitHub PAT, ××¢×××ª config)

**×©×××**: ××× ××¤×¨××¡ ××ª ××§×× ××§××× ×-AI-OS?

### ××××××
**××§×× ××§××× ×× × ×¤×¨×¡ ××× ×××¤×¢×.**

- **×¡××××¡**: ð Designed (Not Deployed)
- **×©××××©**: ××©××© ×-Blueprint / Design Reference ××××
- **×××**: ×¤×¨××¡×, ××¤×¢××, ×× × ××¡××× ××ª×§× ××ª ××§×× ××§×××

### ×¨×¦××× ×

**××× ×× ××¤×¨××¡?**
2. **××¢×××ª deployment ×× ×¤×ª××¨××ª**: ××¡×¨ PAT, ××© ××××× (typo ×-Accept header), ×× ××¨××¨ ×× ××¡××××¡.
3. **××××××ª**: ××× ×× × ×©××××ª ×¤××§×× ×××××× ××¡×¤××§××ª ×××¤×¢××ª Executor ×××××××.
4. **×¢×§×¨×× Thin Slices**: ×¢×××£ ××× ××ª ××××××¦×× ×××¨××ª××ª ×××××§×¨×ª.

**×× ×× ×××§×××?**
- **××¢××¦××**: ××× ××× ××©× ×¢× endpoints, authentication, path validation.
- **×××§×××**: ×× ×××¢×××ª ×©××× × ××¡× ××¤×ª××¨.
- **×-Blueprint**: ×× ××¢×ª×× × ×××× ××× ××ª Executor - × ×©×ª××© ×× ×× ×§×××ª ××ª×××.

**×× ×××§××?**
- ××¨××¢: **××× ××××××¦×× ×©× ××ª××× ×-GitHub**.
- ××¢×ª××: ×× × ×¦××¨× Executor - × ×× × ××× ×××¤×¡, ×¢× ×©××××ª ××××××ª ××¨××¨××ª.

### ××©×¤×¢× ×¢× CAPABILITIES_MATRIX
- **GH-005**: GitHub Executor API â ð Designed (Not Deployed) - Reference Only

---

## 2025-11-20 â ××××× #3: GitHub Safe Git Policy

### ××§×©×¨
×××¢×¨××ª AI-OS ××© ××¡×¤×¨ ×××©×§×× (Claude Desktop, GPT, Chat1) ×©×××××× ×××©×ª ×-GitHub ××××¦×¢ ×¤×¢××××ª ×©×× ××ª. ×¦×¨×× ×××× ×××ª ××××××ª ××××× ×©××× ×¢× ××××.

**×©×××**: ×× ×××× ×××××××ª ×××ª××× ×-GitHub?

### ××××××
**Safe Git Policy - PR-First Approach**

- **×¡××××¡**: â Active - ×× ×¢× ×× ××××©×§××
- **××× ××¨×××**: PR-first approach - ××× push ××©××¨ ×-main ××× ×××©××¨ ××¤××¨×© ××××¨
- **×× ×¢×**: Claude Desktop, GPT, Chat1, ××× ×××©×§ ×¢×ª×××

### ×¨×¦××× ×

**××× PR-first?**
1. **××××××ª**: ×× ×©×× ×× ×¢×××¨ review ××¤× × merge ×-main
2. **×©×§××¤××ª**: ×× ×©×× ×× ×××× ×××ª××¢×
3. **Rollback**: ××¤×©×¨ ×××× ×©×× ×××× ××§×××ª
4. **Human-in-the-loop**: ×××¨ ×××©×¨ ×× ×©×× ×× ××©××¢××ª×

**××××× ×××ª:**
1. ×× ×××©×§ ×××× ×××¦××¨ commits ××§×××××
2. ×× ×××©×§ ×××× ×××¦××¨ PRs (Pull Requests)
3. ×¨×§ ×××¨ ×××©×¨ merge ×-main
4. Push ××©××¨ ×-main ×¨×§ ×¢× ×××©××¨ ××¤××¨×© ××××¨

**××× ×××¨×¨×××:**
- ××× "GPT = ×ª×× ×× ××××" ×× "Claude = ×××¦××¢ ××××"
- ××© ×¨×§ ××××××ª ××× ×××ª ×©×× ××ª + ×××ª× ××××××ª ××××××ª

### ××©×¤×¢× ×¢× ×××¢×¨××ª
- ×× ××××©×§×× ××¤××¤×× ××××ª× ×××× ×××ª Git
- ××× "DRY RUN" ××××©×§ ××× ×-"Full Write" ××××¨
- ××© capabilities ×©×× ××ª ××× constraints ××××

---

## 2025-11-20 â ××××× #4: ×¡××× Phase 1 (Foundation) ×©× AI-OS

### ××§×©×¨
××××× ××ª×§××¤× ××××¨×× × ×× ×× × ×¨××¤× ×××© ××©× `ai-os` ×©× ××¢× ×××××ª ×-SSOT ×©× ××¢×¨××ª ×××¤×¢×× ××××©××ª ×-AI (AI-OS).

**× ××¦×¨×**:
- **README** ×××© ×××¤××¨× (420 ×©××¨××ª)
- **××¡××× ××××** (5 ××¡××××):
  - `CONSTITUTION.md` - 9 ×××§× ××¡××
  - `SYSTEM_SNAPSHOT.md` v2 - ×¦×××× ××¦× ××§××£
  - `CAPABILITIES_MATRIX.md` v1.1 - 22 ××××××ª ××ª××¢×××ª
  - `DECISIONS_AI_OS.md` - ××× ××××××ª (×××¡×× ×××)- **×××¤×× ×¡××× ××** (2 ××¡××××):
  - `AGENTS_INVENTORY.md` - 8 ×¡××× ×× ××××¤××
  - `GPT_GITHUB_AGENT.md` - ×ª××¢×× ××× ×©× ×¡××× ×××× #1
- **×××¤×× ××××**:
  - `TOOLS_INVENTORY.md` - 24 ×××× ×××× ×××¨×¦×××ª
- **×××× ×××ª ×××××**:
  - `SECURITY_SECRETS_POLICY.md` - ×××× ×××ª ××§××¤× (720 ×©××¨××ª)
- **×©× × Workflows ×¨×©××××**:
  - `WF-001` â GITHUB_PLANNING_DRY_RUN (570 ×©××¨××ª)
  - `WF-002` â DECISION_LOGGING_AND_SSOT_UPDATE (737 ×©××¨××ª)

**×©×××**: ××× Phase 1 (Foundation) ×××©××? ××× ×××¢×¨××ª ×××× × ××©××××©?

### ××××××
**Phase 1 â Foundation ×©× AI-OS × ××©× ×××©××.**

- **×¡××××¡**: â Phase 1 Complete - System Ready for Controlled Use
- **×××× ×××××**:
  - `ai-os` ××× **××§××¨ ××××ª ×××××** (SSOT) ××ª××¢××, ××××××ª, ×¡××× ××, ×××× ××××× ×××ª
  - ×××¢×¨××ª ×××× × ××©××××© **××××§×¨** ××××× ×××××ª×××
  - ×× ×©×× ×× ××××ª× ×××© ××¢×××¨ ××¨× ××× ××-Workflows ××¨×©×××× (××¤×××ª WF-001 ×× WF-002)
- **×××**: ×©××××© production ×××××××, ×¡××× ×× ××××× ××××× ×¢× ××ª×××, ×¤×¢××××ª ×× ××¤××§×××ª

### ×¨×¦××× ×

**××× Phase 1 ×××©××?**

1. **×××¡×× ×ª××¢××× ×××§**:
   - ××© ×××§× (9 ×¢×§×¨×× ××ª)
   - ××© ×¦×××× ××¦× ×××
   - ××© ××¤×ª ××××××ª (22 ××××××ª)
   - ××© ××× ××××××ª (4 ××××××ª ×××× ××)

2. **×ª××¢×× ××¨××¨ ×©× ×¨×××××**:
   - ×¡××× ×××× ××ª××¢× (GPT GitHub Agent)
   - 24 ×××× ××××¤××
   - 8 ×¡××× ×× ××¡×××××
   - ××××××ª ××¨××¨××ª ××× ×¨×××

3. **×××× ×××ª ×××××**:
   - ×××× ×××ª ××§××¤× ××¡××§×¨××× (720 ×©××¨××ª)
   - ××××× ××××¨×× ×¨×××©×× (SECRETS/, config/)
   - ××××× ××¨××¨×× ××× ×¡×××/×××
   - ×ª××××× ××××¨×¦×× ×-incident response

4. **Workflows ×××× ××**:
   - WF-001: ××× × ×¢× ×©×× ××× GitHub (DRY RUN)
   - WF-002: ××× × ×¢× ××××××ª + ×¡× ××¨×× SSOT
   - Human-in-the-loop ×¢× ×× ×¤×¢××× ×§×¨××××ª

5. **×××¤×× ×¡×××× ××**:
   - ×× ××× ××¡××× ××¤× Risk Level
   - ××××× Unknown Tools (Make, Telegram, GitHub Actions)
   - ×ª××× ××ª ××¨××¨× ××××¤×× ××××××

**×× ×××©×?**
- â ×ª×©×ª××ª ××¦×××
- â ×ª××¢×× ××§××£
- â ×××× ×××ª ××¨××¨×
- â ××§×¨××ª ××××××ª
- â Workflows ×¤×¢××××

**×× ×¢×××× ××¡×¨?**
- â³ ×¡×¨××§×ª ××××× ×××× (config/, secrets)
- â³ ××¨××¨ Unknown Tools
- â³ ××××××¦×× ××ª×§×××ª (Semi-Automated)
- â³ Monitoring & Health Checks

**××× "××××§×¨" ××× "Production"?**
- ××× ×¡××× ×× ××××× ××××× ×¢× ××ª×××
- ×× ×¤×¢××× ×××¨×©×ª ×××©××¨ ×× ××©×
- ××¨× ×××¦×¢× ×¡×¨××§×ª ××××× ××××
- Human-in-the-loop × ×©××¨ ××××

### ××©×¤×¢× ×¢× SSOT

**××¡×××× ×©×¢×××× ×** â:

1. **`docs/SYSTEM_SNAPSHOT.md`**:
   - â ×¡×¢××£ "×××¤× ×× ×× × ×¢××©××":
     - ×××¡×£: "â Phase 1 (Foundation) ×××©××"
     - ×¢×××: "â³ ××©×× ×××: Phase 2 - Security & Automation"
   - â ×¡×¢××£ "××©××××ª ×¤×ª××××ª":
     - ××× ××©××××ª Phase 1 ×-"×××©××"

2. **`README.md`**:
   - â ×¡×¢××£ Roadmap:
     - Phase 1: ~~In Progress~~ â **â COMPLETE**
     - Phase 2: Upcoming â **ð NEXT**

3. **`docs/CAPABILITIES_MATRIX.md`**:
   - â ×××¡×£ ××¢×¨× ××¨××© ×××¡××:
     - "**System Status**: Foundation Complete (DECISION 2025-11-20 #4) - Ready for Controlled Use"

4. **`docs/DECISIONS_AI_OS.md`** (××¡×× ××):
   - â ×××¡×£ ××××× #4
   - â ×¢××× ×¡×××× ××××××ª (4 ××××××ª)
   - â ×¢××× "×¢×××× ×××¨××"

### Follow-ups

**Phase 2 Options** - ×××××¨ Thin Slice ×¨××©××:

**××¤×©×¨××ª A: Security Phase 1** (×××××¥):
- [ ] ×××¡×¤×ª `.gitignore` rules
- [ ] ×¡×××× `SECRETS/` ×××××
- [ ] Warning ×-README ×¢× ××××¨×× ×¨×××©××
- [ ] ×¡×¨××§×ª `config/` ××××¤××© secrets inline
- [ ] ××¦××¨×ª ×¨×©×××ª ××××¨×¦××

**××¤×©×¨××ª B: Workflows × ××¡×¤××**:
- [ ] WF-003: Health Checks
- [ ] WF-003: SSOT Auto-Update (×××§×)
- [ ] WF-003: Secret Migration Process

**××¤×©×¨××ª C: ××¨××¨ Unknown Tools**:
- [ ] ××××§×ª Make.com - ××©××××©?
- [ ] ××××§×ª Telegram Bot - ×××× bot?
- [ ] ×¡×¨××§×ª GitHub Actions - ×××× workflows?
- [ ] ×¡×§××¨×ª Config Files - secrets inline?

**××¤×©×¨××ª D: ×ª××¢×× ×××× ×¤×¢××××**:
- [ ] `tools/GITHUB_MCP.md`
- [ ] `tools/WINDOWS_MCP.md`
- [ ] `tools/FILESYSTEM_MCP.md`
- [ ] `tools/GOOGLE_MCP.md`

**××××**: ×× ××××× ×××× ××¢×ª×× ×ª×¢×××¨ ××¨× **WF-002** ××ª×¢×××× ×-DECISIONS_AI_OS + SSOT.

---

## 2025-11-24 â ××××× #5: Telegram UI â Official Interface (AI-OS-DECISION-TELEGRAM-001)

### ××§×©×¨
×××¢×¨××ª ×§××××× ×©× × "×¢×××××ª" ×©× ××××¨×:

1. **Chat1 â ×××©×§ ×¨×©×× ××ª×× ai-os**:
   - × ××¦× ×-`chat/telegram_bot.py`
   - ×××××¨ ×-Agent Gateway (`ai_core/agent_gateway.py`)
   - ×××©×§ ××¢××¨××ª ×¢× Human-in-the-Loop (××¤×ª××¨× ×××©××¨)
   - ××ª××¢× ××××§ ××××¨××××§×××¨× ×©× AI-OS

2. **×¤×¨××××××¤ ×××¦×× × (××××¥ ××¨××¤×)**:
   - × ××¦× ××ª××§×× ××§××××ª ××××¥ ×-ai-os
   - ××××¨ ××××¨× ×-LLM ×§×× ××¨× HTTP ×¤×©××
   - **××** ×××××¨ ×-Agent Gateway
   - ×©×××© ×× ××¡×× ×¨××©×× × ××××

**×©×××**: ×× ××××©×§ ××¨×©×× ×××××¨× ×-AI-OS?

### ××××××
**××© ×¨×§ ×××©×§ ××××¨× ×¨×©×× ××× ×-AI-OS: Chat1 ××¨× Agent Gateway.**

- **×¡××××¡ Chat1**: ð§ Implemented (Not Fully Deployed)
- **×¡××××¡ ×¤×¨××××××¤ ×××¦×× ×**: ðï¸ Legacy / External
- **×××§×× Chat1**: `chat/telegram_bot.py`

### ×¨×¦××× ×

**××× Chat1 ××× ××××©×§ ××¨×©××?**
1. **×××××¨ ×××¨××××§×××¨×**: ××××¨ ×¢× Agent Gateway â GPT Planner - ×××¨××× ×× ××× ×.
2. **Human-in-the-Loop**: ××¦×× ×ª××× ××ª ××××§×© ×××©××¨ ××¤× × ×××¦××¢.
3. **××ª××¢×**: ××§×× ××¨××¤×, ×××§ ××-SSOT.
4. **×¢××¨××ª**: ×××©×§ ××¢××¨××ª.

**××× ××¤×¨××××××¤ ××××¦×× × ××× × ×¨×©××?**
1. **×× ×××××¨ ×-Agent Gateway**: ××××¨ ×¢× LLM ×××¦×× ×, ×× ×¢× ××ª×©×ª××ª ×©× AI-OS.
2. **×× ××ª××¢×**: × ××¦× ××××¥ ××¨××¤×.
3. **× ××¡×× ××××**: ×©×××© ××××××, ×× ××©××××© ××××ª×.

### ××××× ×××××××

1. **××¡××¨** ××× ××ª ×ª×××××× ×¨×©×××× ×¢× ××¤×¨××××××¤ ××××¦×× ×.
2. ×××××ª ××¦××¨×, ××© ×××××¢ ××ª××¢×× ×× ×¤×¨××××××¤ ××× ××§××× ×× × ×× ×.
3. **Chat1 ××× ××××©×§ ××¨×©×× ×××××** ×××××¨× ×-AI-OS.

---

---

## 2025-11-27 â DEC-006: n8n ×-Automation Kernel ×¨×©×× ×©× AI-OS (Make.com ×× ××××)

**Date:** 2025-11-27  
**Owner:** Or  
**Status:** Approved  

**Context:**
AI-OS ×××©× ×× ×× ×¢×:
- GitHub ××©×××ª State ××§××¦×× (JSON/YAML/Markdown) â Source of Truth.
- Google Workspace ×-Control Plane (UI ××× × ××× â Sheets/Docs ×××'.).
- ×©×××ª ×¡××× ×× (AgentKit / MCP / LangChain) ×-Super-Layer.

× ××¨×© "Automation Kernel" â ×¤×××¤××¨××ª ×××¨×§×¤××××× ×©×ª×××:
- ×§×¨××× ×-Git ×××§××¦×× (Local / Docker),
- ××× ×××××ª "×××¤×¨×¦×××ª" ×¢× ×× ×¦×¢×,
- ×××× × ×××× ×××¨×¦×× ×¢×××§× ×¢× ×¡××× ×× (MCP / Tools),
- × ××ª× ×ª ×× ×××× ×-Infrastructure (GitOps, Docker, backups).

×××¦×¢ ×××§×¨ ××©××××ª× n8n ××× Make.com, ××××××¨ GAP-004: ××××¨×ª ×¤×××¤××¨××ª ××××××¦×× ×¨×©×××ª ×-Phase 2.4+.

**Options Considered:**
1. **Option A â n8n (Self-Hosted, Docker):**
   - ×¨×¦× ×-Container ××§×××/VPS.
   - ××× ××××× ×¢× ××¡×¤×¨ Executions (×-Community / Self-hosted).
   - ×××©× ××©××¨× ×××¢×¨××ª ××§××¦×× (Volume Mount) â ××ª××× ×-GitHub State ××§××¦××.
   - ×ª×××× ×-Code Nodes (JS/Python) ××××× ×××¨×¦×××ª ××××¨× ×××ª (MCP / LangChain).
   - × ××ª× ×××¨×¡× ××ª×¦××¨×ª INFRA_ONLY (×¨×§ ××××××¦×××ª ××¢×¨××ª×××ª, ××× ×××¢×ª ××××× ××××©×××).

2. **Option B â Make.com (SaaS, Operation-based):**
   - ×¤×××¤××¨××ª SaaS × ×××, low-code.
   - ×××× ×ª××××¨ ××¤× ×××¤×¨×¦×××ª â ××§×¨ ××¡××× ×× "×¤××¤×× ×××" (Agents).
   - ××× ×××©× ××©××¨× ×-Filesystem/Git; ×¢×××× ××¢××§×¨ ××¨× GitHub API.
   - Storage ×××××§× ××¤××¨×× ×§× ××× × ××¢× × Make (×§×©× ×-GitOps).
   - ×ª×××ª ×××§× ×-SaaS ×××¦×× × ××××§ ××× ×¢×××§ ×©× ×-OS.

3. **Option C â Hybrid/None:**
   - ××¢××× ××× Kernel ×¨×©×× (×¨×§ MCP/×¡×§×¨××¤××× × ×§×××ª×××).
   - ×× ×××©×ª××© ×× ×-n8n ××× ×-Make.com ××× ×××¨×¢× ××¨××¨×.
   - ×ª××¦××: ×××¨××××ª, ×××¡×¨ ×¢×§××××ª, ×§××©× ×× ×××× State ×××ª××¢××.

**Decision:**
- **n8n × ×××¨ ×-Automation Kernel ×¨×©×× ×©× ×-AI-OS** ××× ×-Phase 2.4 ×××××.
- ××¤×¨×××§× ××ª××¡×¡ ×¢× **n8n Self-Hosted (Docker)** ××ª×©×ª××ª ×¨××©××ª ××××¨×§×¤×××××:
  - ××¢×¨××ª××ª (Infra / State / Healthchecks / Sync),
  - ×××××©× ×× ××××§ ××××××××¦×××ª ×¢× ×××××, ×ª××ª ×§×× ××¨×× ×××§×¨×.
- **Make.com ×× ×××§ ×××××× ×©× ×-AI-OS**:
  - ×× ×ª××× ××, ×× ××¡×ª×× ×¢××× ××§×¨× ×.
  - ×××ª×¨ ×©××××© × ×§×××ª×/× ××¡××× ×¢× ××× ×××¨, ××× ×× ×××¨××× ××¨××× ×××¢×¨××ª.
- GitHub × ×©××¨ **×-SSOT**: ×× ×-State ××× ×-Workflows ×©× n8n ××ª××¢××/×××××× ×-Git.

**Implementation Notes:**
- Phase 2.3 (INFRA_ONLY):
  - BLOCK_N8N_INFRA_BOOTSTRAP_V1 already executed (infra/n8n/* + State Layer updates).
  - n8n ×××××¨ ×-service status=up, ×× ××©××××© ×× ××××× ×××× ×¤×¨× ××××.
  - ××× ××××××¦×××ª ×¢× ××××× (Gmail/Calendar/Tasks) ×¢× ×©×× ×× Mode.

- Phase 2.4:
  - ××××¡××£ Blocks:
    - `BLOCK_N8N_CONTROL_PLANE_INTEGRATION_V1` â workflows ×©×¢××××× ×¨×§ ××× GitHub State ×-Google ×-UI, ×¢×××× INFRA ××××.
    - `BLOCK_N8N_BACKUP_AND_GITOPS_V1` â ××××× ××××××× ×©× Workflows ×-Git (Export â Commit).
  - ××¢×××:
    - `SERVICES_STATUS.json`: make.com = not_core / optional_saas.
    - `SYSTEM_STATE_COMPACT.json`: ×××¡××¨ ×¡×ª××¨××ª ("DEC-006 pending") ××××¤× ××ª ×-DEC-006 ××¨×©××.

- Phase 3+:
  - ××× ×××¨×¦×× ×©× n8n ×¢× AgentKit / MCP ×-"Tool Server" ×¢×××¨ ×¡××× ××.
  - ×¤×ª×××ª ××¤×©×¨××ª ×××××××¦×××ª ×××× ×ª××ª Human-in-the-Loop ××¤× Mode/Phase.

**Related:**
- GAP-004: n8n vs Make.com â **Closed by DEC-006**
- BLOCK_N8N_INFRA_BOOTSTRAP_V1
- POLICY-001: NO-KOMBINOT for Infrastructure Tools
- DEC-007: No Hierarchy Between Interfaces

---

## 2025-11-26 â DEC-004: Connectivity Strategy for GPT Actions & Remote Access (ngrok vs Cloudflare)

**Date:** 2025-11-26  
**Owner:** Or  
**Status:** Approved  

**Context:**  
AI-OS ××××©× ×¨×¥ ××¨××¢ ×¢× ×××©× ××§××× ×××××¨× NAT, ×¢× ××©××¤× ××××¦× ××¨× ngrok (×ª××× ××ª ××× ×××ª).  
GPT Actions ×××¨×©××ª:
- URL ××¦×× ×-HTTPS, ×¢× TLS ×ª×§××,
- ×©×× ××©×ª× × ××× restart,
- ××× ××¡××× ××××¦×¢ (Interstitial) ×©×××××× ××©×××¨ ×§×¨××××ª ×××××××××ª.

×××"× BLOCK_NGROK_STABILITY_RESEARCH ×××× GAP-001:
- ngrok ××× ×× ×¢× URL ××ª×××£ = ××××× ×××× (×× restart ×××¨×© ××¢××× ××ª ×-Action),
- ×ª××××§× ××× ××ª ×©× ×-URL ×©×××¨×ª ××ª ××××××ª "OS" ××××¦×¨×ª ×××¡×¨ ××¦××××ª.

×××§×¨ ×¢××× × ××¨××:
- ×-ngrok ××© ×××× ×××××ª static domain ×× ×××× × (×××××× ×§×××¢ ××× ×©×× ××©×ª× ×) â ××× ××ª××× ××ª ×××× ×××ª ××© ×¢×××× ××××××ª ×§×©××ª: session ×§×¦×¨, ×ª×§×¨× ×¢× ×¨××× ×¤×¡, ×××××¨××ª/interstitial ××¤× × ×-API, ×× ×©×¢××× ××©×××¨ ××× ×××¨×¦×× ×¢× GPT Actions.
- Cloudflare Tunnel ×××¤×©×¨ ×××××¨ Outbound-only ××¨× `cloudflared` ×-edge ×©× Cloudflare, ×©××××© ××××××× ×××©×, ×-WAF ×××§ â ×××× ×, ×× ×¢×× ××© ××××××.

×××¨×ª ××××××:
- ××××××¨ ××¡××¨×××××ª ×§××©××¨×××ª ×¨×©×××ª ×-AI-OS ×¢×××¨ GPT Actions ××©××¨××ª× HTTP,
- ××× ×××ª×××× ×¢×××× ×-"production 24/7", ××× ×¢× ×¤×××ª ××××× ×××¨×× ×××ª×¨ ××¦××××ª.

**Options Considered:**

1. **Option A â ××××©××¨ ×¢× ngrok ××× ×× ××× ×¢××©××**  
   - URL ××§×¨×× (×× ×× ××©×ª××©×× ×-static domain).  
   - ×¦××¨× ××¢××× ××× ××ª ××ª GPT Actions ××× restart.  
   - ××××××ª ×ª×× ××ª ××× ×××ª: Session ×§×¦×¨, ×ª×§×¨× ×¢× ×ª×¢×××¨×, ××××¨××ª/interstitial.  
   - ××ª×¨××: 0 ×©×× ××, 0 ××××¥.  
   - ××¡×¨××: ××××××ª ×¤××ª×× ×©×××¨×, ×× ××ª××× ×-OS.

2. **Option B â ngrok Personal / Paid (×××××× ×§×××¢ + TCP)**  
   - Personal plan (×¡××× $8/××××©) ×××× custom domain ××× + ××ª×××ª TCP ×§×××¢×.  
   - ××©×¤×¨ ××©××¢××ª××ª ××¦××××ª: ××××××/××ª×××ª ×× ××©×ª× ××, ××× interstitial ×©× Free.  
   - ×¢××××: ×ª×¢×××¨× ×¢×××¨×ª ××¨× ×¨×©×ª ngrok, ×¢× ××××××ª ×©××××© ××××× Usage-Based.  
   - ××ª×¨××: ×§× ×××××¢×, ××× ××©× ××ª ××¨×× ×××¨××××§×××¨×.  
   - ××¡×¨××: ×¢×××ª ×§×××¢× ××¤×¨×××§× ×××©× ××©×× ×ª×©×ª××ª, ×ª×××ª ×××§× ×-SaaS ××××.

3. **Option C â Cloudflare Tunnel Free Tier + ×××××× ×¤×¨×× (××¤×ª×¨×× ×©× ×××¨ ×××××× ××)**  
   - ××ª×§× ×ª `cloudflared` ××§××××ª ×©×××¦×¨ ×××××¨ ×××¦×¤× ××-××××× × (Outbound-only) ×-Cloudflare.  
   - ×©××××© ××××××× ×©×× (×¢×××ª ~10$ ××©× ×) + Cloudflare Free Plan (SSL, WAF, DDoS ×××× ×).  
   - URL ××¦×× ××××××× (DNS-based), ×× ×× ××××©× × ××× ×××××¨.  
   - ××××¨×ª ×××§ WAF ×©×××× ×¢× ×¡×× ×× ×¢×××¨ GPT / ChatGPT (××¤× User-Agent / IP), ××× ××× ××¢ ××¡××××ª "×××××".  
   - ××ª×¨××:  
     - ××¦××××ª ×××××,  
     - ××××× ××××,  
     - ×× ×ª××× ××××× ××ª××××¨ ×©× ngrok,  
     - ××ª××× ××××× ×××× ×× × ××××¨×× ×©× ×-OS.  
   - ××¡×¨××: ××¢× ×××ª×¨ ×××¨×× ×-ngrok ×××§×× ×¨××©×× ××ª.

4. **Option D â VPS + FRP / ×¤×ª×¨×× Self-Hosted (×××× ××¨×× ×××ª×¨)**  
   - ×©×××¨×ª VPS ××× + ××ª×§× ×ª FRP (Fast Reverse Proxy) ××©×××× ×××× ×-IP ××× ××¡××ª.  
   - ××ª××× ×××ª×¨ ××©×× Production (Phase 3+), ×× ×-Phase 2.3 INFRA_ONLY.  
   - ××ª×¨××: ×¨×××× ××ª ××××, zero SaaS lock-in.  
   - ××¡×¨××: ×××¨×© DevOps ×××; ×××§×× ××× ×¢××©××.

**Decision:**  

1. ××××× ×××××× (Phase 2.3 â INFRA_ONLY):  
   - ×××¤×¡××§ ×××ª××¡×¡ ×¢× ngrok ××¤×ª×¨×× "×××× ×××××" ×-GPT Actions.  
   - ×× ××¢×××¨ ××¨××¢ ××ª×× ××ª ××ª×©××× (Option B) â ×¢×××ª ×§×××¢× ××××ª×¨×ª ××©×× ×ª×©×ª××ª.  
   - ××××¥ Cloudflare Tunnel ××¤×ª×¨×× ××§××©××¨×××ª ××¨××©× ×¢×××¨ GPT Actions ××©××¨××ª× HTTP ××§×¨××××× ×-AI-OS (Option C), ×¢× ××¡××¡ ×××××× ×¤×¨××.

2. ××××× ×××× ×× × (Phase 2.4 â "Nervous System"):  
   - ×××©×××¨ ngrok ×××× ××©× ×/××§××× ××¤××ª×× ××Ö¾×¤×¢×× (×× ×¦×¨××), ×××:
     - Cloudflare Tunnel ××× ×-"gateway ××¨×©××" ×©× ×-OS ××× GPT.  
   - ××©×§×× ×××¡×¤×ª Tailscale / VPN ×-use cases ×©× TCP ×¤×¨×××× (×× GPT), ×××××× × ×¤×¨××ª.

3. ××××× ×××¨×× (Phase 3+):  
   - ×××©×××¨ Option D (VPS + FRP) ×× ×ª×× ×©××¨×× ××¤×©×¨×, ×× ×-AI-OS ×××¤×× ××ª×©×ª××ª ×§×¨××××ª ××××× ×¦×¨×× ×¨××ª ××¦××××ª/×¨×××× ××ª ××××× ×××ª×¨.

**Implementation Notes (××©×××× ×××××, ×× ×××¦×¢ ××× ×××©××¨ × ××¡×£):**

- BLOCK_CLOUDFLARE_TUNNEL_SETUP_V1  
- BLOCK_CLOUDFLARE_WAF_RULE_FOR_GPT_V1  
- BLOCK_GPT_ACTIONS_BASE_URL_UPDATE_V1  
- BLOCK_SERVICES_STATUS_UPDATE_V2  

**Related:**
- GAP-001: ngrok URL instability  
- GAP-002: No persistent deployment (indirectly)  
- BLOCK_NGROK_STABILITY_RESEARCH  
- Phase: 2.3 (INFRA_ONLY, Connectivity focus)

---

## 2025-11-26 â DEC-007: No Fixed Role Hierarchy Between Interfaces

**Date:** 2025-11-26  
**Owner:** Or  
**Status:** Approved  

**Context:**  
×××¡×××× ×©×× ×× ×©× AI-OS × ××¦×× ×©×¨×××× ×©× × ××¡×× ×××¨×¨×× ×©××ª××¨:
- GPT ×"××ª×× × ××××" ×× "DRY RUN mode"
- Claude ×"××××××" ×× "××××¦×¢ ××¨××©×"
- Chat1 ×"UI ××××"
- ×××¨×¨××× ×ª×¤×§××××ª ×§×××¢× ××¤× ×××©×§

×× ××ª× ××© ×¢× **ROLE_MODEL_SIMPLIFICATION_V1** (Block ×-2025-11-26) ×©×××× ×××¨×¨××× ×§×©×××.

**Problem:**  
× ××¡×× ××× "GPT = DRY RUN ××××" ×××¦×¨ ×¨××©× ×©××× ×©-GPT "×× ××××ª ×¢××©× ×××¨××", ×××§×× ××ª××¨ ×××××§ ××ª:
- ×××××××ª ×××× ×××ª ×©×× (×× ××× ×××× ××¢×©××ª)
- ××××××ª ×××××××ª ×©×× (×× ××¡××¨ ××¢×©××ª ××× ×××©××¨)

×××¢××: × ××¡×××× ××× ××¦×××× ××ª ××××©×§×× ×"××¨×××ª" ×××§×× ××××©×§×× ×©×× ×× ×¢× ××××××ª ×©×× ××ª.

**Decision:**

1. **××× ×××¨×¨××××ª ×ª×¤×§×××× ×§×××¢×** ××× ××××©×§×× (Claude/GPT/Chat1):
   - ××× "××× ××¢×××ª ×××××"
   - ××× "××ª×× × ××¢×××ª ×××¦×¢"
   - ××× "DRY RUN ××¢×××ª ××××ª×"
   - ××× "×××©×§ ×¨××©×" ×× "×××©×§ ××©× ×"

2. **××© ×¨×§ ×©× × ×¡××× ×××¤××× ××:**
   - **Technical Capabilities** â ×× ×× ×××©×§ ×××× ××¢×©××ª ××××× × ××× ××ª (×××©× ×××××, APIs)
   - **Safety Constraints** â ××××××ª ××××××ª ×©××××ª ×¢× ×××× (××× Safe Git Policy)

3. **×××× ×××ª GitHub ×××××:**
   - **××× ××××©×§××** ×× ×××ª× Safe Git Policy:
     - "PR-first approach, no direct push to main without Or's explicit approval"
   - ×× "GPT = DRY RUN" ×-"Claude = Full Write"

4. **× ××¡×× ×××××¥ ×××¡××××:**
   - â **× ×××**: "Claude Desktop: Full MCP access including local Git operations, subject to Safe Git Policy"
   - â **× ×××**: "GPT: GitHub access via Custom Actions (read/write), subject to Safe Git Policy"
   - â **×× × ×××**: "Claude = Primary Executor", "GPT = Planner Only", "DRY RUN mode"

5. **××× ××× ×××¡××¨ ×××ª××¢××:**
   - "Hands" / "Brain" / "Primary" / "Secondary"
   - "Executor" / "Planner Only" / "DRY RUN mode"
   - "Real" vs "Simulated"

**Implementation:**
×¢×××× 5 ×§××¦××:
- `docs/DECISIONS_AI_OS.md` (××××× #3 ×¢×××× ×)
- `docs/AGENT_SYNC_OVERVIEW.md`
- `docs/system_state/agents/AGENT_CAPABILITY_PROFILE.md`
- `docs/system_state/SYSTEM_STATE_COMPACT.json`
- `docs/system_state/registries/SERVICES_STATUS.json`

**Impact:**
- ×ª××¢×× ××¨××¨ ×××ª×¨ ×©× ××××××ª ×××××××ª
- ××× ××××× ×¢× "×× ×¢××©× ××"
- ××××©××ª ××¢×××× - ×× ×××©×§ ×××× ××¢×©××ª ×× ×©×××× (×××¤××£ ×××××××ª)

**Related:**
- ROLE_MODEL_SIMPLIFICATION_V1 (Block, 2025-11-26)
- DEC-003 (Safe Git Policy)
- CONSTITUTION.md Law #4 (Human-in-the-Loop)

---

## 2025-11-27 â DEC-008: Governance Layer Bootstrap V1 + OS Core MCP Minimal

**Date:** 2025-11-27  
**Owner:** Or  
**Status:** Approved  

**Context:**

AI-OS v2 planning requires systematic measurement of operational fitness:
- **FITNESS_001**: Friction (operational overhead, tool retries, decision latency)
- **FITNESS_002**: CCI (Cognitive Capacity Index - autonomy vs manual work)
- **FITNESS_003**: Tool Efficacy (success rates, execution times)

Additionally, multiple agents (Claude Desktop, GPT Operator, future LangGraph workflows, n8n) need unified, programmatic access to State Layer without directly manipulating JSON files.

Current state (Phase 2.3):
- State Layer exists as JSON files in `docs/system_state/`
- No measurement/governance infrastructure
- No unified API gateway to State
- Agents access files directly â risk of inconsistency

**Decision:**

**Part A: Governance Layer Bootstrap V1**

Create `/governance` directory structure at repo root:
```
governance/
âââ DEC/           # Decision records (governance-related)
âââ EVT/           # Event logs (governance-specific)
âââ metrics/       # Computed metrics storage
âââ scripts/       # Measurement scripts
â   âââ measure_friction.py
â   âââ measure_cci.py
â   âââ measure_tool_efficacy.py
â   âââ generate_snapshot.py
âââ snapshots/     # Periodic governance snapshots
```

**Bootstrap V1 Scope:**
- Directory structure created
- Scripts are **stubs** (interface defined, no implementation yet)
- Each script prints "TODO: Governance V1" when run
- README.md documents purpose and next steps

**Not in Bootstrap V1:**
- Actual measurement logic (comes in subsequent vertical slice)
- Metrics storage format (TBD)
- Periodic snapshot generation (needs n8n or cron)
- Visualization/reporting layer (Phase 3+)

**Part B: OS Core MCP Minimal**

Create unified HTTP gateway to State Layer at `services/os_core_mcp/`:
- FastAPI server on port 8083
- Three core tools:
  1. `GET /state` â read SYSTEM_STATE_COMPACT.json
  2. `GET /services` â read SERVICES_STATUS.json
  3. `POST /events` â append to EVENT_TIMELINE.jsonl

**Design Principles:**
- All file paths are relative to repo root (not hardcoded to specific machine)
- Graceful error handling (404 if file missing, 500 if JSON invalid)
- Auto-create EVENT_TIMELINE.jsonl if it doesn't exist
- Logging of all state access
- CORS enabled for GPT Custom Actions integration

**Not in Minimal:**
- Write operations on state/services (read-only for now, except events)
- Validation/schemas (comes later)
- Caching (not needed yet)
- Access control (all agents have same permissions)
- Webhooks/notifications (Phase 3+)

**Rationale:**

**Why Governance Layer now?**
1. **Measurement-driven evolution**: Can't optimize what we don't measure
2. **Aligns with v2 planning**: CONTROL_PLANE_GOVERNANCE_SPEC_V1 and AIOS_V2_INFRA_UPGRADE_PLAN
3. **Bootstrap early**: Infrastructure in place, implementation follows incrementally
4. **Thin Slice approach**: Structure first, logic later (Slice 2+)

**Why OS Core MCP?**
1. **Single point of access**: Instead of 5 agents manipulating files directly
2. **Consistency**: All state access goes through one gateway
3. **Observability**: Can log/track who accessed what
4. **Future-proof**: Easy to add validation, caching, access control later
5. **Integration ready**: Works with Claude Desktop, GPT Actions, n8n, future LangGraph

**Why minimal scope?**
- Avoids over-engineering
- Gets core functionality working immediately
- Follows Thin Slices principle (Law #6)
- Can iterate based on real usage

**Implementation Notes:**

Files created:
- `governance/` directory structure (6 directories)
- `governance/README.md` (documentation)
- `governance/scripts/*.py` (4 stub scripts)
- `services/os_core_mcp/server.py` (FastAPI server, 3 endpoints)
- `services/os_core_mcp/README.md` (API documentation)
- `services/os_core_mcp/requirements.txt` (dependencies)

Next steps (Slice 2):
1. Implement actual measurement logic in governance scripts
2. Add governance metrics to SERVICES_STATUS
3. Create first LangGraph workflow using OS Core MCP
4. Integrate Langfuse for observability

**Related:**
- CONTROL_PLANE_GOVERNANCE_SPEC_V1 (if exists in docs/)
- AIOS_V2_INFRA_UPGRADE_PLAN (planning document)
- Phase 2.3: Stabilizing the Hands (current phase)
- DEC-006: n8n as Automation Kernel
- DEC-007: No Fixed Role Hierarchy

---

## 2025-11-27 â DEC-009: Slice 2A â Daily Context Sync V1 (Agent Kernel + LangGraph)

**Date:** 2025-11-27  
**Owner:** Or  
**Status:** Approved  

**Context:**

Following DEC-008 (Governance Layer Bootstrap + OS Core MCP Minimal), AI-OS v2 now has:
- Governance Layer structure (stubs ready for measurement)
- OS Core MCP (unified HTTP gateway to State Layer on port 8083)

Next step: First LangGraph-based workflow to demonstrate:
1. Orchestration via LangGraph (graph-based AI workflows)
2. Integration with OS Core MCP (read state, write state, log events)
3. Systematic state updates (rather than ad-hoc file edits)

This is Slice 2A of the v2 architecture - introducing the Agent Kernel as the workflow execution engine.

**Decision:**

**Part A: OS Core MCP Extension - State Update Endpoint**

Add new endpoint to `services/os_core_mcp/server.py`:
- `POST /state/update`
- Input: `{"patch": {...}, "source": "..."}`
- Behavior:
  - Reads SYSTEM_STATE_COMPACT.json
  - Merges patch (top-level keys only in V1)
  - Writes back to file
  - Returns: `{"status": "ok", "state": {...}}`
- Error handling: 404 if file missing, 500 if JSON invalid or write fails

**Part B: Agent Kernel Service - LangGraph Execution Engine**

Create new service at `services/agent_kernel/`:
- FastAPI server on port 8084
- Endpoint: `POST /daily-context-sync/run`
- Implements first LangGraph workflow: `daily_context_sync_graph`

**Graph Structure:**
1. **start_node**:
   - Reads current state: `GET http://localhost:8083/state`
   - Logs event: `POST http://localhost:8083/events` (DAILY_CONTEXT_SYNC_STARTED)

2. **compute_patch**:
   - Generates patch: `{"last_daily_context_sync_utc": "<now UTC ISO8601>"}`

3. **apply_patch**:
   - Applies patch: `POST http://localhost:8083/state/update`
   - Logs event: `POST http://localhost:8083/events` (DAILY_CONTEXT_SYNC_COMPLETED)

**Result:**
```json
{
  "status": "ok",
  "last_sync_time": "2025-11-27T16:02:21Z"
}
```

**Side Effects:**
- `SYSTEM_STATE_COMPACT.json` gets new field: `last_daily_context_sync_utc`
- `EVENT_TIMELINE.jsonl` gets 2 new events (STARTED + COMPLETED)

**Rationale:**

**Why Daily Context Sync?**
1. **Simple but complete**: Demonstrates full graph â OS Core MCP â State Layer flow
2. **Non-destructive**: Only adds/updates a timestamp, doesn't delete anything
3. **Observable**: Clear events in timeline
4. **Extensible**: Foundation for more complex workflows

**Why LangGraph?**
1. **Graph-based orchestration**: Natural fit for multi-step AI workflows
2. **State management**: Built-in state passing between nodes
3. **Integration-ready**: Works with LangChain ecosystem
4. **Observability prep**: Foundation for Langfuse integration (Slice 2B)

**Why Agent Kernel as separate service?**
1. **Separation of concerns**: State Layer (OS Core MCP) â  Workflow Engine (Agent Kernel)
2. **Scalability**: Can add more workflows without touching OS Core
3. **Technology isolation**: LangGraph in Agent Kernel, FastAPI in OS Core
4. **Independent deployment**: Can restart Agent Kernel without affecting State access

**Not in Slice 2A:**
- n8n integration (scheduled triggers) â Slice 2B
- Langfuse observability (tracing) â Slice 2B
- Checkpointing/pause/resume â Future
- More complex workflows â Future
- Actual governance measurement implementation â Slice 3+

**Implementation Notes:**

Files created/modified:
- `services/os_core_mcp/server.py` (added POST /state/update endpoint)
- `services/agent_kernel/` (new directory)
- `services/agent_kernel/kernel_server.py` (FastAPI server, port 8084)
- `services/agent_kernel/requirements.txt` (langgraph, fastapi, httpx, etc.)
- `services/agent_kernel/README.md` (documentation)
- `services/agent_kernel/graphs/daily_context_sync_graph.py` (LangGraph implementation)
- `services/agent_kernel/smoke_test_slice_2a.py` (end-to-end test)
- `docs/system_state/SYSTEM_STATE_COMPACT.json` (added last_daily_context_sync_utc field)
- `docs/system_state/timeline/EVENT_TIMELINE.jsonl` (added DAILY_CONTEXT_SYNC_* events)

Smoke test results:
- â OS Core MCP /health: 200 OK
- â Agent Kernel /health: 200 OK
- â Daily Context Sync execution: 200 OK
- â State updated with timestamp
- â Events logged (STARTED + COMPLETED)

Next steps (Slice 2B):
1. n8n workflow to trigger daily context sync on schedule
2. Langfuse integration for workflow tracing
3. Add more workflows (weekly summary, governance metrics calculation)
4. Implement actual governance measurement scripts

**Related:**
- DEC-008: Governance Layer Bootstrap + OS Core MCP Minimal
- DEC-006: n8n as Automation Kernel (integration pending in Slice 2B)
- DEC-007: No Fixed Role Hierarchy (Agent Kernel = tool for all interfaces)
- Phase 2.3: INFRA_ONLY (this is infrastructure work, not live automations yet)

---

## 2025-11-27 â DEC-010: Governance Truth Layer Bootstrap V1

**Date:** 2025-11-27  
**Owner:** Or  
**Status:** â Approved  
**Phase:** 2.3 (INFRA_ONLY)

### Context

Following DEC-008 (Governance Layer Bootstrap + OS Core MCP Minimal) and DEC-009 (Slice 2A â Daily Context Sync), AI-OS now has:
- **Truth Layer** operational: EVENT_TIMELINE.jsonl + SYSTEM_STATE_COMPACT.json + SERVICES_STATUS.json
- **OS Core MCP** providing unified API gateway (ports 8083-8084)
- **Agent Kernel** with LangGraph workflows

However, the Governance Layer (governance/) was only infrastructure (stub scripts) - no actual measurements or snapshots were being generated.

### Decision

**Implement Governance Truth Layer Bootstrap V1:**

1. **Truth Layer Definition** (Canonical Sources):
   - `docs/system_state/timeline/EVENT_TIMELINE.jsonl` â Event Log (append-only)
   - `docs/system_state/SYSTEM_STATE_COMPACT.json` â System State Truth
   - `docs/system_state/registries/SERVICES_STATUS.json` â Services Registry Truth

2. **Snapshot Generation** (governance/scripts/generate_snapshot.py):
   - Read from all 3 truth sources
   - Collect git metadata (branch, commit)
   - Calculate fitness metrics:
     - **FITNESS_001_FRICTION**: open_gaps_count, time_since_last_daily_context_sync_minutes, recent_error_events_count
     - **FITNESS_002_CCI**: active_services_count, recent_event_types_count, recent_work_blocks_count, pending_decisions_count
   - Generate snapshot JSON with full metadata
   - Save to: `governance/snapshots/SNAPSHOT_<timestamp>.json`
   - Update: `governance/snapshots/GOVERNANCE_LATEST.json` (always points to latest)

3. **Governance Documentation**:
   - DEC stored in: `governance/DEC/DEC_GOVERNANCE_TRUTH_BOOTSTRAP_V1.md`
   - EVT stored in: `governance/EVT/EVT_GOVERNANCE_TRUTH_BOOTSTRAP_V1_<timestamp>.json`

### Rationale

- **Operationalize Governance:** Move from stub infrastructure to actual measurements
- **Observable Fitness:** Enable systematic tracking of system health via metrics
- **Foundation for Automation:** Create snapshots that n8n can trigger/consume (Slice 2B+)
- **Truth Layer Formalization:** Establish canonical sources for all governance measurements

### Implementation

**Branch:** `feature/slice_governance_truth_bootstrap_v1`

**Files Modified:**
- `governance/scripts/generate_snapshot.py` - full implementation (was stub)

**Files Created:**
- `governance/snapshots/SNAPSHOT_<timestamp>.json` - first real snapshot
- `governance/snapshots/GOVERNANCE_LATEST.json` - pointer to latest snapshot
- `governance/DEC/DEC_GOVERNANCE_TRUTH_BOOTSTRAP_V1.md` - local decision record
- `governance/EVT/EVT_GOVERNANCE_TRUTH_BOOTSTRAP_V1_<timestamp>.json` - completion event

**Snapshot Structure:**
```json
{
  "snapshot_id": "GOVERNANCE_SNAPSHOT_<timestamp>",
  "created_at": "<timestamp>",
  "source": "governance/scripts/generate_snapshot.py",
  "git": {"branch": "...", "last_commit": "..."},
  "system_state": {"phase": "...", "mode": "..."},
  "services_summary": {"up": N, "total": N},
  "event_log_summary": {"last_event_timestamp": "...", "last_event_type": "..."},
  "fitness_metrics": {
    "FITNESS_001_FRICTION": {...},
    "FITNESS_002_CCI": {...}
  }
}
```

### Testing

**Smoke Test:**
- Run: `python governance/scripts/generate_snapshot.py`
- Verify: Snapshot created in `governance/snapshots/`
- Verify: `GOVERNANCE_LATEST.json` exists and contains valid structure
- Verify: Fitness metrics populated with real values

**First Snapshot Results:**
- â Snapshot generated: `SNAPSHOT_20251127_174131.json`
- â GOVERNANCE_LATEST.json created
- â Fitness metrics calculated:
  - FITNESS_001_FRICTION: 8 open gaps, 87 minutes since last sync, 0 recent errors
  - FITNESS_002_CCI: 9/14 services active, 12 event types, 9 recent blocks

### Next Steps (Post-Bootstrap)

1. **Slice 2B:** n8n workflow to generate snapshots on schedule (daily/weekly)
2. **Implement actual measurement scripts:**
   - `measure_friction.py` - detailed friction analysis
   - `measure_cci.py` - cognitive capacity deep dive
   - `measure_tool_efficacy.py` - tool/service effectiveness
3. **Visualization:** Build dashboard/reporting layer for governance metrics
4. **Integration:** Connect snapshots to OS Core MCP for programmatic access

### Related Decisions

- **DEC-008:** Governance Layer Bootstrap (infrastructure only)
- **DEC-009:** Slice 2A - Daily Context Sync (Agent Kernel + LangGraph)
- **DEC-006:** n8n as Automation Kernel (will trigger snapshot generation in future)

**Phase:** 2.3 (INFRA_ONLY)  
**Mode:** Infrastructure work - no live automations yet

---

## ×¡×××× ×××××××ª

| # | × ××©× | ××××× | ×¡××××¡ |
|---|------|-------|-------|
| **1** | MCP Orchestration | ×× × ××§× ××§×× ×¨×¥ | ðï¸ Legacy (Reference Only) |
| **2** | GitHub Executor API | ×× ×¤×¨××¡ | ð Designed (Not Deployed) |
| **3** | GitHub Safe Git Policy | PR-first for all interfaces | â Active |
| **4** | Phase 1 Foundation | ×××©×× | â Complete - Ready for Use |
| **5** | Telegram UI - Official Interface | Chat1 ×××× | â Decision Locked |
| **DEC-004** | Connectivity Strategy (ngrok vs Cloudflare) | Cloudflare Tunnel | â Approved |
| **DEC-006** | n8n as Automation Kernel | n8n Self-Hosted | â Approved |
| **DEC-007** | No Fixed Role Hierarchy | Capabilities + Constraints model | â Approved |
| **DEC-008** | Governance Layer Bootstrap + OS Core MCP | Bootstrap V1 + Minimal API | â Approved |
| **DEC-009** | Slice 2A â Daily Context Sync V1 | Agent Kernel + LangGraph | â Approved |
| **DEC-010** | Governance Truth Layer Bootstrap V1 | Snapshot Generation + Fitness Metrics | â Approved |

---

## ×¢×§×¨×× ××ª ×× ×××

×××××××ª ×××× ××©×§×¤××ª ××ª **×××§× ×××¡×× ×©× AI-OS**:

1. **Data-First** (×××§ #1): ×§××× ×××××¨××, ×××¨ ×× ××× ××
2. **Human-in-the-loop** (×××§ #4): ××× ×¤×¢××××ª ××¨×¡× ×××ª ××× ×××©××¨
3. **Thin Slices** (×××§ #6): ××× ×× ××¦××¨× ×××¨××ª××ª ×××××§×¨×ª
4. **××××× ××¢× ×××** (×××§ #7): ××××××ª ×ª××× ×××§×× ××¨××©××

---

**×¡××××¡ ××¡×× ××**: â Active  
**×¢×××× ×××¨××**: 27 × ×××××¨ 2025  
**××××××ª × ×¢××××ª**: 10 ××××××ª ×§×¨×××××ª  
**××¢×¨×**: ××××××ª ××× × ××ª× ××ª ××©×× ×× ××¢×ª××, ××× ×¨×§ ×××¨× ×××× ××¤××¨×© ××ª××¢×× ×©× ××¨×¦××× × ××©×× ××.
