# TOOL_INTEGRATION_MAP V1

**Version:** 1.0  
**Created:** 2025-11-26  
**Author:** Claude Desktop (INFRA_ONLY alignment)  
**Purpose:** מפת אינטגרציה מפורטת - מי ניגש לאיזה שירות, באיזה מסלול, ובאיזה מצב

---

## 📋 Overview

מסמך זה מסכם את דפוסי הגישה (Access Patterns) של כל ממשק (Interface) לשירותים השונים במערכת AI-OS.

המטרה: **לתעד את המציאות** - איך הגישה עובדת בפועל, לא איך היא צריכה לעבוד.

---

## 🔧 Integration Map

| Service / Tool | Interfaces that can use it | Access Path | Status | Notes |
|----------------|---------------------------|-------------|--------|-------|
| **GitHub** | Claude Desktop, GPT Operator | **Claude:** MCP GitHub Client + local clone<br>**GPT:** Custom Action via ngrok | `up` | GPT access depends on stable ngrok URL. URL changes on restart require GPT Actions update. |
| **Google Gmail** | GPT Operator (full), Claude Desktop (read-only) | **GPT:** Google Workspace Custom Action (send/list)<br>**Claude:** google-mcp (read-only) | `up` | Used for email automations in future phases. OAuth 2.0 authenticated. |
| **Google Calendar** | GPT Operator (full), Claude Desktop (read-only) | **GPT:** Google Workspace Custom Action (create/list events)<br>**Claude:** google-mcp (read-only) | `up` | Event management, future automation triggers. |
| **Google Drive** | GPT Operator (full), Claude Desktop (read-only) | **GPT:** Google Workspace Custom Action (search/create/update)<br>**Claude:** google-mcp (search only) | `up` | Source for future Drive State Layer. Used for Drive Snapshot sync. |
| **Google Docs** | GPT Operator | **GPT:** Google Workspace Custom Action (create/read/write) | `up` | Used for SYSTEM_SNAPSHOT_DRIVE, briefs, documentation. |
| **Google Sheets** | GPT Operator | **GPT:** Google Workspace Custom Action (create/read/write) | `partial` | Connected but not used as Control Plane yet. Reserved for future dashboard UI (Phase 3+). |
| **Google Tasks** | GPT Operator | **GPT:** Google Workspace Custom Action (create/read/update) | `partial` | Reserved for future task orchestration. Not integrated into main workflows yet. |
| **n8n** | (none yet) | Planned: Docker instance | `planned` | Designed as future "nervous system" (Phase 2.4+). No active instance currently. |
| **Collector_Gmail_to_Records** | (Apps Script, legacy) | Time-based trigger (hourly) | `error_auth` | Legacy Apps Script failing with "Authorization is required to perform that action." Not part of new AI-OS orchestration. To be reviewed in future infra pass. |

---

## 🔍 Access Pattern Details

### Claude Desktop
**תפקיד:** Local Executor ("הידיים")

**גישה לשירותים:**
- **GitHub:** MCP GitHub Client (port 8081) + local clone → full read/write, commits allowed (push needs approval)
- **Google Workspace:** google-mcp → **read-only** (Gmail, Calendar, Drive search only)
- **Local System:** Full access via PowerShell, filesystem, Windows automation

**מגבלות:**
- ❌ אין write ל-Google Workspace (read-only only)
- ✅ יכול לקרוא מיילים, אירועים, קבצים ב-Drive
- ✅ מבצע commits מקומיים, push דורש אישור

---

### GPT Operator
**תפקיד:** Strategic Planner & Google Workspace Executor ("האדריכל")

**גישה לשירותים:**
- **GitHub:** Custom Action via ngrok (port 8081) → read/write files, branches, commits, PRs
- **Google Workspace:** Custom Action via ngrok (port 8082) → **full read/write**
  - Gmail: send/list emails
  - Calendar: create/list events
  - Drive: search/create/update files
  - Docs: create/read/write documents
  - Sheets: create/read/write spreadsheets
  - Tasks: create/read/update tasks
- **Drive Snapshot:** Access to SYSTEM_SNAPSHOT_DRIVE doc when available

**מגבלות:**
- ⚠️ תלוי ב-ngrok URL יציב (משתנה בכל הפעלה מחדש)
- ❌ אין גישה ישירה לריפו מקומי או MCP
- ❌ GitHub Actions ב-DRY RUN mode (החלטה DEC-003)

---

### Chat1 Telegram Bot
**תפקיד:** Hebrew Natural Language UI

**גישה לשירותים:**
- **Agent Gateway:** Routes intents to GPT Planner
- **GPT Planner:** Creates execution plans
- **Action Executor:** Executes approved plans (via Claude or GPT)

**מגבלות:**
- ⚠️ לא deployed באופן קבוע - דורש הפעלה ידנית
- ✅ UI only - לא מבצע ללא אישור
- 🔐 Human-in-the-Loop enforced (כפתורי ✅/❌)

---

## 🚨 Critical Issues

### 1. ngrok URL Instability
**בעיה:** URL משתנה בכל הפעלה מחדש של ngrok  
**השפעה:** GPT Custom Actions נשברים, צריך עדכון ידני  
**פתרון אפשרי:** Cloud deployment (Google Cloud Run) או ngrok paid plan

### 2. Legacy Apps Script Failing
**בעיה:** `Collector_Gmail_to_Records` נכשל עם שגיאת הרשאה  
**השפעה:** רץ כל שעה ומנסה לגשת לג'ימייל, מציף שגיאות  
**פתרון אפשרי:** לתקן הרשאות, לשדרג לארכיטקטורה החדשה, או להשבית

### 3. Google Workspace Read-Only בClaude
**בעיה:** Claude יכול רק לקרוא, לא לכתוב ל-Google Workspace  
**השפעה:** כל פעולות כתיבה חייבות לעבור דרך GPT  
**פתרון אפשרי:** להוסיף write capabilities ל-google-mcp (Phase עתידי)

---

## 📝 Context & Constraints

**Phase:** 2.2–2.3 (Stabilizing the Hands)  
**Mode:** INFRA_ONLY

**משמעות:**
- ✅ תיעוד מצב קיים - אין שינוי התנהגות
- ✅ יישור State Layer עם המציאות
- ❌ אין הוספת אוטומציות חדשות
- ❌ אין אוטומציות על החיים של Or (מיילים, יומן, משימות אישיות)

**שירותים עתידיים:**
- **n8n:** יתווסף ב-Phase 2.4+ כ-"nervous system" (Watcher/Dispatcher/Sync workflows)
- **Google Sheets Control Plane:** יתווסף ב-Phase 3+ כ-Dashboard UI עם State Machine
- **AgentKit Super-Layer:** יתווסף ב-Phase 3+ למטא-תיאום מעל MCP + n8n

---

## 🔗 Related Documents

- **SERVICES_STATUS.json:** `docs/system_state/registries/SERVICES_STATUS.json`
- **AUTOMATIONS_REGISTRY.jsonl:** `docs/system_state/AUTOMATIONS_REGISTRY.jsonl`
- **AGENT_CAPABILITY_PROFILE.md:** `docs/system_state/agents/AGENT_CAPABILITY_PROFILE.md`
- **SYSTEM_STATE_COMPACT.json:** `docs/system_state/SYSTEM_STATE_COMPACT.json`
- **AGENT_SYNC_SPEC_BLACKBOARD_V0.md:** `docs/AGENT_SYNC_SPEC_BLACKBOARD_V0.md`

---

**Last Updated:** 2025-11-26  
**Updated By:** Claude Desktop (INFRA_ONLY alignment - TOOL_INTEGRATION_MAP_V1)  
**Status:** ✅ Documented - reflects actual access patterns as of Phase 2.2-2.3

> "Documentation is infrastructure — know your tools before you build on them."
