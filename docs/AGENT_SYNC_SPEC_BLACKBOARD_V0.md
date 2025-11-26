# AGENT_SYNC_SPEC_BLACKBOARD_V0.md

**Version:** 0.2 (Enhanced with Evolution Path)  
**Created:** 2025-11-26  
**Updated:** 2025-11-26 (SPEC_CRITIC review applied)  
**Author:** Claude Desktop (Block 3 + SPEC_CRITIC)  
**Status:** 📐 Design Phase  
**Phase:** Phase 2.2–2.3 (Stabilizing the Hands)  
**Mode:** INFRA_ONLY

---

## 1. Purpose

מסמך זה מגדיר כיצד **"סוכן מסנכרן" (Sync Agent v0)** פועל מעל State Layer הקיים בקבצים.

**מטרות:**
1. לוודא שכל הסוכנים (Claude Desktop, GPT Operator, Chat1 עתידי) משתמשים באותה **Single Source of Truth (SSOT)**
2. למנוע אי-עקביות, פערים (gaps), או מידע מיושן בין רכיבי המערכת
3. לספק מנגנון אחיד לסנכרון state בתחילת כל session
4. להפוך את State Layer ל**Blackboard** פעיל שעליו הסוכנים יכולים לקרוא, לכתוב, ולתאם פעולות

**State Layer Files (SSOT):**
- `docs/system_state/SYSTEM_STATE_COMPACT.json` — מצב המערכת המלא בפורמט JSON
- `docs/AGENT_SYNC_OVERVIEW.md` — סיכום מהיר לסוכנים בתחילת session
- `docs/system_state/timeline/EVENT_TIMELINE.jsonl` — לוג כרונולוגי של כל האירועים במערכת
- `docs/system_state/AUTOMATIONS_REGISTRY.jsonl` — מלאי מלא של כל האוטומציות

---

## 2. Core Concepts

### 2.1 Blackboard Architecture

**Blackboard** = מערכת הקבצים + Git + State Layer

בארכיטקטורת Blackboard:
- **הלוח השחור (Blackboard):** State Layer — קבצי JSON ו-Markdown שמכילים את state המערכת
- **סוכנים (Knowledge Sources):** Claude Desktop, GPT Operator, Chat1 — כל אחד קורא מהלוח, מעבד, וכותב בחזרה
- **Controller:** Sync Agent v0 — מתאם בין הסוכנים, מזהה gaps ומציע פעולות

**עקרונות:**
- אין תקשורת ישירה בין סוכנים — הכל עובר דרך הלוח
- כל שינוי מתועד ב-EVENT_TIMELINE
- Git משמש כ-version control של הלוח

---

**n8n as Nervous System (Future):**

In future phases (2.4+), **n8n** will serve as the "nervous system" of AI-OS — reacting to changes in the State Layer and routing tasks to appropriate agents.

**3 Core Workflows:**
1. **Watcher Workflow** — Monitors State Layer for changes:
   - GitHub webhooks (on push to main)
   - File polling (check EVENT_TIMELINE.jsonl every X minutes)
   - Google Sheets onEdit (via Apps Script webhook, Phase 3+)
   
2. **Dispatcher Workflow** — Routes tasks based on type:
   - `file_edit` → Claude Desktop
   - `spec_write` → GPT Operator
   - `healthcheck` → Run script directly
   - `analysis` → AgentKit (Phase 3+)

3. **Sync Workflow** — Periodic maintenance:
   - Daily healthchecks
   - Gap detection (inconsistencies between State files)
   - "What's new since last sync" summary generation

**Why "Nervous System"?**
- Like neurons, n8n **reacts** to stimuli (events in State Layer)
- Like synapses, n8n **routes** signals (tasks) to the right organs (agents)
- Like reflexes, n8n **executes** simple actions automatically (healthchecks, logs)

**Integration with Sync Agent:**
- **Phase 2.2-2.3:** Sync Agent is manual (Claude Desktop runs OODA)
- **Phase 2.4:** n8n can **trigger** Sync Agent on events (e.g., new commit → run OODA)
- **Phase 3+:** n8n becomes primary executor, Sync Agent becomes meta-coordinator via AgentKit

---

### 2.2 OODA Loop ברמת קבצים

**OODA = Observe → Orient → Decide → Act**

כל session של Sync Agent v0 עובר דרך מחזור OODA:

1. **Observe (תצפית):**
   - קריאת State Layer: SYSTEM_STATE_COMPACT.json, AGENT_SYNC_OVERVIEW.md
   - קריאת אירועים חדשים מ-EVENT_TIMELINE.jsonl (מאז session אחרון)
   - בדיקת AUTOMATIONS_REGISTRY.jsonl לשינויים

2. **Orient (התמצאות):**
   - זיהוי gaps: מה חסר? מה לא מעודכן?
   - זיהוי אי-עקביות: האם יש סתירות בין קבצים?
   - זיהוי הזדמנויות: מה אפשר לשפר?

3. **Decide (החלטה):**
   - קביעת Blocks חדשים לביצוע
   - קביעת priority: מה דחוף? מה יכול לחכות?
   - חלוקת משימות: מה ל-Claude? מה ל-GPT?

4. **Act (פעולה):**
   - Claude מבצע: קבצים, Git, Healthchecks
   - GPT מבצע: Specs, מחקר, design
   - תיעוד: EVENT_TIMELINE מתעדכן עם הפעולות

---

## 3. State Sources

### 3.1 SYSTEM_STATE_COMPACT.json

**מה הוא מכיל:**
- מצב המערכת המלא בפורמט JSON מובנה
- Interfaces (Claude, GPT, Chat1): capabilities, limitations, status
- Services (GitHub, Google Workspace, ngrok, etc.): status, ports, dependencies
- Open gaps ו-issues קריטיים
- Safety constraints שחלים על כל הסוכנים
- קישורים לקבצי State Layer אחרים

**מי קורא:**
- Claude Desktop בתחילת session (Session Init)
- GPT Operator כשצריך context מלא
- סוכנים חיצוניים (Deep Research, Analysis tools) שזקוקים למבנה מובנה
- Chat1 (עתידי) לבדיקת אילו capabilities זמינות

**מי כותב:**
- Claude Desktop — עדכון אחרי שינויים משמעותיים (Phase change, service up/down)
- GPT Operator — עדכון של gaps, decisions, או architecture changes

**איך Sync Agent v0 משתמש:**
- קורא בתחילת session כדי לקבל תמונה מלאה של state
- משווה עם SESSION_NOTE.md ו-AGENT_SYNC_OVERVIEW.md לזיהוי אי-עקביות
- מחפש gaps שלא מתועדים ומציע Blocks לסגירתם
- מוודא ש-services status תואם ל-SERVICES_STATUS.json

---

### 3.2 AGENT_SYNC_OVERVIEW.md

**מה הוא מכיל:**
- סיכום מהיר (quick sync) לכל סוכן בתחילת session
- Phase & Mode נוכחיים
- Core State Snapshot — מה עובד, מה לא
- Infra summary — טבלת services
- Active plans ו-Blocks שהושלמו לאחרונה
- Open questions ו-decisions ממתינות
- Quick links למסמכים מרכזיים

**מי קורא:**
- **כל סוכן בתחילת session** — זהו נקודת הכניסה המרכזית
- Claude Desktop: לבדיקת Mode (INFRA_ONLY?) ו-Phase
- GPT Operator: לבדיקת active plans ו-pending decisions
- Chat1: לזיהוי מה זמין ומה לא

**מי כותב:**
- Claude Desktop — עדכון אחרי Blocks משמעותיים
- GPT Operator — עדכון של decisions או Phase changes

**איך Sync Agent v0 משתמש:**
- קורא **תמיד** בתחילת session — זה ה-"מצפן"
- מוודא ש-"Last Updated" לא ישן מדי (>24h = אזהרה)
- משווה "Recent Work / Blocks" עם EVENT_TIMELINE לזיהוי Blocks שלא תועדו
- בודק "Open Questions" ומציע Blocks שיכולים לענות עליהן

---

### 3.3 EVENT_TIMELINE.jsonl

**מה הוא מכיל:**
- לוג כרונולוגי של **כל אירוע משמעותי** במערכת (JSONL format)
- סוגי אירועים: `block_complete`, `session_init`, `state_baseline`, `sync`, `decision`, `error`, etc.
- כל אירוע כולל: timestamp, actor, action, details, phase, mode
- Schema line בראש הקובץ מגדירה את event_types התקפים

**מי קורא:**
- Sync Agent v0 — קורא **רק אירועים חדשים** מאז session אחרון (לפי timestamp)
- Claude Desktop — בודק היסטוריית Blocks ו-decisions
- GPT Operator — מנתח trends (כמה Blocks בשבוע? כמה errors?)
- Or — סקירה של פעילות מערכת

**מי כותב:**
- Claude Desktop — כל Block שהושלם, כל session_init, כל sync
- GPT Operator — Blocks שהוא מבצע (specs, docs)
- Chat1 (עתידי) — משימות שאושרו והופעלו

**איך Sync Agent v0 משתמש:**
- **CRITICAL:** קורא רק אירועים חדשים מאז timestamp של session אחרון
- מזהה patterns: אם יש הרבה `error` events → מציע healthcheck או debug Block
- מוודא עקביות: אם Block הושלם אבל AGENT_SYNC_OVERVIEW לא עודכן → מציע sync
- משתמש ל-"memory" של מה קרה מאז סשן אחרון

---

### 3.4 AUTOMATIONS_REGISTRY.jsonl

**מה הוא מכיל:**
- מלאי מלא של **כל האוטומציות** במערכת (JSONL format)
- כל אוטומציה כוללת: id, name, type, status, owner, triggers, dependencies, docs
- סוגי אוטומציות: custom_gpt, local_service, telegram_bot, tunnel, internal_service, state_sync

**מי קורא:**
- Sync Agent v0 — בודק האם כל automation ב-registry תואם ל-SERVICES_STATUS
- Claude Desktop — מזהה dependencies לפני הפעלת service
- GPT Operator — מתכנן Blocks חדשים (מה קיים? מה חסר?)
- Or — סקירת מלאי אוטומציות

**מי כותב:**
- Claude Desktop — כשמוסיף automation חדש (service, script)
- GPT Operator — כשמתכנן automation חדש (design phase)

**איך Sync Agent v0 משתמש:**
- משווה AUTOMATIONS_REGISTRY עם SERVICES_STATUS.json — מוודא עקביות
- מזהה "orphan automations" — automations ב-registry שלא מופיעים ב-SERVICES_STATUS
- מזהה "undocumented automations" — services running שלא ב-registry
- מציע Blocks לסגירת gaps (תיעוד חסר, dependencies לא ברורות)

---

### 3.5 Future: Drive State Mirror (Phase 3+ Design)

**Status:** Design Phase — NOT implemented in Phase 2.2-2.3

---

**In Phase 3+, State Layer expands to Google Drive:**

**GitHub State Layer (current):**
- **Purpose:** Infrastructure, services, automations, events
- **Location:** `/docs/system_state/` in GitHub repo
- **Files:** SYSTEM_STATE_COMPACT.json, EVENT_TIMELINE.jsonl, AUTOMATIONS_REGISTRY.jsonl, SERVICES_STATUS.json
- **Managed by:** Claude Desktop (files, Git), GPT Operator (specs, docs)

**Drive State Layer (future):**
- **Purpose:** Tasks, context, knowledge, inbox
- **Location:** `/AI-OS State Layer/` in Google Drive
- **Folders:**
  - `/01_Active_Context/` — Current tasks (JSON files with state, logs, output)
  - `/02_Knowledge_Graph/` — Long-term knowledge (Markdown)
  - `/03_Inbox/` — Raw inputs (emails, docs, voice notes)
  - `/04_Archive/` — Completed tasks
- **Managed by:** GPT Operator (Google Workspace actions), n8n (automation), AgentKit (future)

---

**Sync Strategy:**

**No direct sync** — two layers serve different purposes:
- **GitHub = code, infra, static docs**
- **Drive = tasks, dynamic state, knowledge**

**Links between layers:**
- EVENT_TIMELINE (GitHub) can reference Drive files:
  ```json
  {
    "event_type": "task_completed",
    "linked_drive_file": "/Active_Context/task-uuid-001.json"
  }
  ```
- Task JSON (Drive) can reference GitHub commits:
  ```json
  {
    "related_github_event": "EVT-2025-11-26-009",
    "related_commit": "abc1234"
  }
  ```

**Sync Agent (Phase 3+) reads both:**
- Identifies gaps: "Task in Drive but no EVENT logged in GitHub"
- Identifies orphans: "Automation in GitHub but no task files in Drive"
- Proposes Blocks to close gaps

---

**Why prepare now (Phase 2.2-2.3)?**
- Design GitHub State Layer to be **Drive-compatible**
- Add optional fields to EVENT_TIMELINE for Drive links
- Avoid breaking changes when Drive layer is added

**What we do NOT do now:**
- ❌ Create Drive folders
- ❌ Sync files to Drive
- ❌ Configure GPT to write to Drive State Layer

---

## 4. Responsibilities of Sync Agent v0

**Sync Agent v0 הוא גרסה ידנית (manual)** — לא daemon, לא רץ ברקע, לא autonomous.

הוא **מופעל בתחילת session** על ידי Claude Desktop או GPT Operator, ועובד בלופ עם Or.

### 4.1 קריאת State בתחילת Session

**מה הוא עושה:**
1. קורא `docs/AGENT_SYNC_OVERVIEW.md` — quick sync, Phase, Mode
2. קורא `docs/system_state/SYSTEM_STATE_COMPACT.json` — full state
3. קורא `docs/SESSION_NOTE.md` — session intent ו-constraints

**פלט:**
- סיכום מצב למשתמש (Or): "Phase 2.2, Mode INFRA_ONLY, 8 services up, 3 partial"
- זיהוי constraints: "אין אוטומציות על החיים בסשן זה"

### 4.2 קריאת אירועים חדשים ב-EVENT_TIMELINE

**מה הוא עושה:**
1. מזהה את timestamp של session אחרון (מ-CONTROL_PLANE_SPEC או מתשאול Or)
2. קורא **רק שורות חדשות** ב-EVENT_TIMELINE.jsonl (timestamp > last_session)
3. מסכם: "מאז סשן אחרון: 3 Blocks הושלמו, 1 baseline הוכרז, 0 errors"

**פלט:**
- "What's new since last session" summary
- זיהוי אם יש דברים ש-Or צריך לדעת (errors, gaps)

---

**Git Diff Optimization (Future):**

**Current approach (Phase 2.2-2.3):**
- Sync Agent v0 reads **entire files**: EVENT_TIMELINE.jsonl, SYSTEM_STATE_COMPACT.json
- Filters events by timestamp: `timestamp > last_session_timestamp`

**Future approach (Phase 2.4+):**
- Use **`git diff`** to identify **deltas** instead of reading full files:
  ```bash
  git diff <last_session_commit> HEAD -- docs/system_state/
  ```
- Parse diff output to extract:
  - New lines in EVENT_TIMELINE.jsonl
  - Changed fields in SYSTEM_STATE_COMPACT.json
  - New/modified files in State Layer

**Benefits:**
- **Performance:** Only process what changed, not entire state
- **Precision:** Know exactly which fields were modified
- **History:** Git provides full audit trail

**Implementation:**
- Phase 2: Manual file reading (simpler, sufficient for small state)
- Phase 2.4+: Git diff parsing (optimized for larger state)

**Technique from Research 2 (Blackboard + OODA):**
- "Use Git diffs to detect deltas in the Blackboard"
- "Observe = git diff + parse changes"
- "Avoids re-reading entire state every session"

---

### 4.3 זיהוי Gaps / אי-עקביות / הזדמנויות

**מה הוא מחפש:**

**Gaps (פערים):**
- Service ב-SERVICES_STATUS אבל לא ב-AUTOMATIONS_REGISTRY
- Automation ב-AUTOMATIONS_REGISTRY אבל status "unknown"
- Block הושלם ב-EVENT_TIMELINE אבל AGENT_SYNC_OVERVIEW לא עודכן
- Open gap מתועד ב-SYSTEM_STATE_COMPACT אבל אין Block מתוכנן לסגירתו

**אי-עקביות (Inconsistencies):**
- AGENT_SYNC_OVERVIEW אומר "Phase 2.2" אבל CONTROL_PLANE_SPEC אומר "Phase 2.3"
- Service status "up" ב-SERVICES_STATUS אבל "partial" ב-SYSTEM_STATE_COMPACT
- Last healthcheck ישן מדי (>24h) ואין healthcheck מתוכנן

**הזדמנויות (Opportunities):**
- יש pending decisions ב-AGENT_SYNC_OVERVIEW שאפשר לטפל בהן
- יש automation שלא נבדק מזמן — מציע Block לבדיקה
- יש קבצים שלא עודכנו מזמן — מציע refresh

**פלט:**
- רשימת ממצאים: "נמצאו 2 gaps, 1 inconsistency, 3 opportunities"

### 4.4 הפקת Blocks חדשים

**מה הוא מציע:**
- **Block proposals** — כל אחד עם:
  - Block ID (לדוגמה: `BLOCK_HEALTHCHECK_REFRESH`)
  - Priority (Critical / High / Medium / Low)
  - Responsible (Claude / GPT / Or)
  - Estimated time
  - Dependencies
  - Rationale (למה Block זה נחוץ?)

**דוגמה:**
```
BLOCK_SERVICES_REGISTRY_SYNC
Priority: High
Responsible: Claude Desktop
Time: 15 minutes
Dependencies: None
Rationale: AUTOMATIONS_REGISTRY has 9 items, but SERVICES_STATUS.json shows 11 services. Need to sync and document 2 missing services.
```

### 4.5 הפקת משימות לסוכנים

**משימות ל-Claude Desktop ("הידיים"):**
- "Edit file X to fix inconsistency"
- "Run healthcheck script"
- "Update SYSTEM_STATE_COMPACT.json with latest service status"
- "Add missing automation to AUTOMATIONS_REGISTRY.jsonl"

**משימות ל-GPT Operator ("האדריכל"):**
- "Write spec for new service Y"
- "Research: What's the best approach for Z?"
- "Design Block for Phase 2.4 transition"
- "Update SNAPSHOT_LAYER_DESIGN.md with new learnings"

**פלט:**
- Organized task list: "For Claude: 3 tasks | For GPT: 2 tasks"

---

## 5. Interfaces

### 5.1 Claude Desktop

**תפקיד:** "הידיים" — Local Executor

**יכולות:**
- גישה מלאה למערכת הקבצים (read/write/edit)
- הרצת scripts (healthcheck, move_completed_plan, etc.)
- Git operations (add, commit, אבל לא push ללא אישור)
- Windows automation (PowerShell, UI control)
- MCP tools (GitHub, Google read-only, Filesystem, Browser, Canva)

**איך מתקשר עם Sync Agent v0:**
- **Input:** Claude מקבל task list מ-Sync Agent
- **Output:** Claude מבצע ומתעדך EVENT_TIMELINE
- **Feedback loop:** אם נתקל בבעיה → מדווח ל-Or → Or מחליט

**דוגמה:**
```
Sync Agent: "Claude, please update SERVICES_STATUS.json to mark ngrok as 'up' with current URL"
Claude: [edits file, verifies JSON validity, logs to EVENT_TIMELINE]
Claude: "Done. EVT-2025-11-26-007 logged."
```

---

### 5.2 GPT Operator

**תפקיד:** "האדריכל" — Strategic Planner

**יכולות:**
- Custom Actions ל-Google Workspace (Gmail, Drive, Docs, Sheets)
- Custom Actions ל-GitHub (read/write files, branches, PRs)
- גישה ל-Drive Snapshot (SYSTEM_SNAPSHOT_DRIVE)
- כתיבת specs, designs, research docs
- תכנון Blocks ו-Phases

**איך מתקשר עם Sync Agent v0:**
- **Input:** GPT מקבל strategic questions / spec requests מ-Sync Agent
- **Output:** GPT כותב specs, מעדכן Drive docs, מתעד ב-EVENT_TIMELINE
- **Feedback loop:** GPT מייעץ ל-Or לגבי החלטות אסטרטגיות

**דוגמה:**
```
Sync Agent: "GPT, we need a spec for n8n integration. Please research and write SPEC_N8N_INTEGRATION.md"
GPT: [researches, writes spec in Google Drive or GitHub]
GPT: "Spec ready: docs/specs/N8N_INTEGRATION_SPEC.md. Logged EVT-2025-11-26-008."
```

---

### 5.3 Future: n8n as Nervous System & AgentKit as Super-Layer

---

#### 5.3.1 n8n: The Nervous System (Phase 2.4)

**תפקיד:** "המערכת העצבית" — Automation Executor & Event Reactor

**מתי יפעל:**
- **כרגע:** לא פעיל (Phase 2.2–2.3 הוא INFRA_ONLY)
- **Phase 2.4:** n8n מופעל כ"nervous system" שמגיב לאירועים
- **Phase 3+:** n8n כמנוע ביצוע עבור AgentKit

---

**3 Workflows מרכזיים:**

**1. Watcher Workflow — "חיישנים"**
- **Purpose:** Detect changes in State Layer
- **Triggers:**
  - GitHub webhooks (on push to main)
  - File polling (every X minutes, check for new EVENTs in EVENT_TIMELINE.jsonl)
  - Google Sheets onEdit (via Apps Script webhook, Phase 3+)
- **Action:** When change detected → send to Dispatcher

**2. Dispatcher Workflow — "מנתב"**
- **Purpose:** Route tasks to appropriate agent
- **Input:** Task from Watcher or COMMAND_CENTER (Sheets, Phase 3+)
- **Logic:**
  ```
  IF task_type == "file_edit" → trigger Claude Desktop (via API or manual notification)
  IF task_type == "spec_write" → trigger GPT Operator (via GitHub issue or manual)
  IF task_type == "healthcheck" → run script directly
  IF task_type == "analysis" → send to AgentKit (Phase 3+)
  ```
- **Output:** Task routed, status logged to EVENT_TIMELINE

**3. Sync Workflow — "תחזוקה"**
- **Purpose:** Periodic maintenance and gap detection
- **Schedule:** Daily or on-demand
- **Actions:**
  - Run `claude_healthcheck.py`
  - Check for inconsistencies (AUTOMATIONS_REGISTRY vs SERVICES_STATUS)
  - Generate "What's new" summary since last sync
  - Update SYSTEM_STATE_COMPACT.json if needed
- **Output:** Healthcheck report, gap list

---

**איך n8n מתחבר ל-State Layer:**
1. **Read:** n8n reads EVENT_TIMELINE.jsonl, AUTOMATIONS_REGISTRY.jsonl
2. **React:** When specific event types appear (e.g., `state_baseline`, `error`), n8n triggers workflows
3. **Write back:** n8n logs its own actions to EVENT_TIMELINE:
   ```json
   {
     "timestamp": "2025-11-26T14:00:00Z",
     "event_type": "automation_triggered",
     "actor": "n8n Dispatcher",
     "action": "Routed BLOCK_HEALTHCHECK_REFRESH to Claude Desktop",
     "details": {"workflow_id": "n8n-dispatcher-v1", "task_uuid": "..."}
   }
   ```

**Security:**
- Human-in-the-loop: n8n can **propose** actions but requires Or's approval for critical tasks
- Sandbox: All n8n workflows tested in dev environment before production
- State Layer integrity: n8n can only **append** to EVENT_TIMELINE, not modify history

---

#### 5.3.2 AgentKit: The Super-Layer (Phase 3+)

**תפקיד:** "המוח המתאם" — Reasoning & Planning Platform

**מתי יפעל:**
- **Phase 3+:** When AI-OS transitions from INFRA_ONLY to LIFE_AUTOMATIONS mode

---

**איך AgentKit מתחבר למערכת הקיימת:**

```
┌─────────────────────────────────────────────────────────┐
│                     AgentKit Platform                    │
│  (Reasoning, Planning, Orchestration)                   │
└────────────────┬────────────────────────────────────────┘
                 │
                 ├──► MCP GitHub Client (port 8081)
                 │     └─► GitHub API → State Layer updates
                 │
                 ├──► MCP Google Client (port 8082)
                 │     └─► Google Workspace → Drive State Layer
                 │
                 ├──► MCP Filesystem tools
                 │     └─► Read/Write local State files
                 │
                 └──► n8n Webhooks
                       └─► Trigger deterministic workflows
```

**Key Insight:** AgentKit **reuses** Claude's existing MCP servers — no duplicate integrations.

---

**Example Flow: AgentKit processes a task**

1. **Or updates MASTER_CONTROL Sheet:** Sets task status to `QUEUED`
2. **Apps Script webhook** → n8n Dispatcher
3. **n8n** reads task details, sends to **AgentKit** (if task requires reasoning)
4. **AgentKit:**
   - Reads State Layer via **MCP Filesystem** (`SYSTEM_STATE_COMPACT.json`)
   - Reasons about the task (using o1/GPT-4o)
   - Decides on actions:
     - Call **MCP GitHub Client** to update files
     - Call **MCP Google Client** to write results to Drive
     - Trigger **n8n workflow** for email notification
5. **n8n** executes deterministic steps (send email, update Sheet status)
6. **EVENT_TIMELINE** logged with all actions

---

**AgentKit Benefits:**
- **Visual Builder:** Design complex agent flows without code
- **Export to Code:** Export agent logic to Python/TS, manage in GitHub
- **MCP Native:** Uses existing MCP tools — no rebuild needed
- **n8n Integration:** AgentKit thinks, n8n executes

**AgentKit is NOT:**
- A replacement for Claude Desktop (still need local executor)
- A replacement for n8n (still need deterministic workflows)
- Required for Phase 2 (optional future enhancement)

---

**Constraints (Phase 2.2-2.3):**
- AgentKit is **design-only** — not implemented yet
- Mentioned here to prepare State Layer structure
- Ensures future compatibility — no breaking changes needed

---

## 6. Text-Only Workflows

### 6.1 Workflow: GAP ב-SYSTEM_STATE_COMPACT

**תרחיש:**
Gap מזוהה: "Chat1 Telegram Bot status is 'partial' but no deployment plan exists"

**שלבים:**

1. **Observe (Sync Agent):**
   - קורא `SYSTEM_STATE_COMPACT.json`
   - רואה: `"chat1_telegram": {"status": "partial", ...}`
   - רואה ב-open_gaps: `GAP-003: Chat1 not deployed persistently`
   - בודק `active_plans/` → אין תוכנית לפריסת Chat1

2. **Orient (Sync Agent):**
   - מסיק: "יש GAP תיעודי — Chat1 קיים כקוד אבל אין תוכנית deployment"
   - Priority: Medium (לא Critical כי לא חוסם עבודה נוכחית)
   - אחראי: צריך spec מ-GPT ואז deployment מ-Claude

3. **Decide (Sync Agent):**
   - מציע Block: `BLOCK_CHAT1_DEPLOYMENT_PLAN`
   - Actions:
     - GPT: כתוב `docs/chat1/CHAT1_DEPLOYMENT_PLAN.md`
     - Claude: אחרי שה-spec מוכן, בצע deployment steps
   - דורש אישור מ-Or

4. **Act:**
   - **Or מאשר:** "כן, בואו נכתוב תוכנית"
   - **GPT כותב spec:**
     - `docs/chat1/CHAT1_DEPLOYMENT_PLAN.md` — איך לפרוס Chat1 כ-service
     - לוגג: `{"event_type": "block_complete", "block_id": "BLOCK_CHAT1_DEPLOYMENT_PLAN", ...}`
   - **EVENT_TIMELINE מתעדכן:**
     - שורה חדשה: `EVT-2025-11-26-009`
   - **Sync Agent מזהה ב-session הבא:**
     - "Block הושלם! Chat1 spec קיים, מוכן לביצוע."

**תוצאה:**
- Gap תועד ונסגר
- יש spec ברור לפריסה
- EVENT_TIMELINE מתעד את כל התהליך

---

### 6.2 Workflow: אוטומציה חדשה ב-AUTOMATIONS_REGISTRY

**תרחיש:**
אוטומציה חדשה נוספה: `AUTO-010: n8n Workflow Manager`

**שלבים:**

1. **Observe (Sync Agent):**
   - קורא `AUTOMATIONS_REGISTRY.jsonl`
   - רואה שורה חדשה: `{"id": "AUTO-010", "name": "n8n Workflow Manager", "status": "planned", ...}`
   - בודק `SERVICES_STATUS.json` → n8n לא רשום שם

2. **Orient (Sync Agent):**
   - מסיק: "אוטומציה חדשה תוכננה אבל לא מופיעה ב-services registry"
   - Priority: Medium (תוכנן אבל לא deployed עדיין)
   - צריך לוודא: האם n8n מותקן? מוכן? צריך INFRA work?

3. **Decide (Sync Agent):**
   - מציע Block: `BLOCK_N8N_INFRA_PREP`
   - Actions:
     - Claude: בדוק אם Docker מותקן, אם n8n image קיים
     - GPT: עדכן `INFRA_MAP.md` עם n8n entry
     - Claude: אם צריך התקנה → הוסף task "Install Docker Desktop"
   - מציע גם: עדכון `SERVICES_STATUS.json` עם n8n entry (status: "planned")

4. **Act:**
   - **Or מאשר:** "בואו נבדוק אם אנחנו מוכנים ל-n8n"
   - **Claude בודק:**
     - `docker --version` → "Docker not found"
     - מסקנה: צריך להתקין Docker לפני n8n
   - **Claude מעדכן `INFRA_MAP.md`:**
     - מוסיף שורה: `n8n | 📋 planned | Depends on Docker Desktop installation`
   - **EVENT_TIMELINE מתעדכן:**
     - `{"event_type": "block_complete", "block_id": "BLOCK_N8N_INFRA_PREP", "action": "Checked n8n prerequisites, Docker missing"}`
   - **Sync Agent מסכם:**
     - "n8n תוכנן, אבל Docker חסר. יש Block חדש: BLOCK_DOCKER_INSTALL"

**תוצאה:**
- אוטומציה חדשה תועדה
- Prerequisites זוהו
- INFRA gap נסגר בהדרגה
- EVENT_TIMELINE מתעד המסע

---

## 7. Constraints & Phase

### 7.1 Phase & Mode

**Current Phase:** 2.2–2.3 (Stabilizing the Hands)  
**Current Mode:** INFRA_ONLY

**משמעות:**
- **Focus:** יציבות תשתית, תיעוד, State Layer
- **לא** לוקחים משימות חדשות של LIFE_AUTOMATIONS (Google Calendar events, Gmail automation)
- כל עבודה היא על **INFRA/STATE/DOCS** בלבד

### 7.2 No Automations על החיים של Or

**כלל ברזל:**
- בשלב זה (Phase 2.2–2.3) **אין אוטומציות** שפועלות על:
  - יומן של Or
  - מיילים של Or
  - משימות של Or
  - קבצים אישיים של Or

**למה?**
- אנחנו עדיין "מייצבים את הידיים" — לא מוכנים לנגוע בחיים האמיתיים
- צריך לוודא ש-State Layer יציב לפני שמפעילים automations critical

**מה כן מותר:**
- קריאה (read-only) של Google Workspace לצורך בדיקה
- כתיבת test docs ב-Drive
- אוטומציות על ה-INFRA עצמה (healthchecks, logs, state sync)

### 7.3 No Daemons — הכל בסשנים עם Human-in-the-Loop

**כלל:**
- אין תהליכים שרצים ברקע (daemons) ללא פיקוח
- כל session מתחיל עם Or, עובד עם Or, ומסתיים עם Or
- כל פעולה משמעותית דורשת אישור מ-Or

**למה?**
- שקיפות מלאה — Or רואה כל דבר שקורה
- בטיחות — אין "הפתעות" של automation שרץ לבד
- למידה — Or לומד איך המערכת עובדה בזמן אמת

**מה זה אומר ל-Sync Agent v0:**
- Sync Agent v0 לא רץ אוטומטית בכל שינוי ב-State Layer
- Sync Agent v0 מופעל **ידנית** בתחילת session
- Sync Agent v0 מציע פעולות, Or מאשר, ואז הביצוע מתחיל

### 7.4 Git: Commit מותר, Push דורש אישור

**כלל:**
- `git add` ו-`git commit` מותרים (מתעד שינויים לוקאליים)
- `git push` דורש **אישור מפורש מ-Or** בכל פעם

**למה?**
- Local commits = גיבוי ו-undo capability
- Push = שיתוף עם העולם → דורש החלטה מודעת

**מה זה אומר ל-Sync Agent v0:**
- Sync Agent יכול להציע: "Commit these changes?"
- Sync Agent **לא יכול** להציע push ללא שאלה: "Or, ready to push?"

---

## 8. Summary & Next Steps

**מסמך זה מגדיר:**
- ✅ Blackboard architecture מעל State Layer
- ✅ OODA Loop workflow לסנכרון
- ✅ תפקידים ברורים לכל State Source (JSON, JSONL, MD)
- ✅ אחריות Sync Agent v0 (manual, session-based)
- ✅ Interfaces: Claude (hands), GPT (architect), n8n/AgentKit (future)
- ✅ 2 workflows כתובים (Gap closure, Automation prep)
- ✅ Constraints: Phase 2.2–2.3, INFRA_ONLY, Human-in-the-Loop

---

**Evolution Stages:**

AI-OS will evolve through 3 stages as State Layer and interfaces mature:

**Stage 1: Manual Sync (Phase 2.2-2.3) — Current**
- **Sync Agent:** Manual, session-based (Claude Desktop runs OODA)
- **State Layer:** File-based in GitHub repo only
- **Interfaces:** Claude (hands), GPT (architect), n8n (planned but not active)
- **Constraints:** INFRA_ONLY, no automations on Or's life, Human-in-the-Loop for all actions
- **Focus:** Stabilizing State Layer, documenting interfaces, establishing SSOT

**Stage 2: n8n Nervous System (Phase 2.4)**
- **Sync Agent:** Semi-automated (n8n triggers OODA on events)
- **State Layer:** GitHub repo + Drive State Layer begins (Active Context, Inbox folders)
- **Interfaces:** Claude (executor), GPT (planner), n8n (reactive executor)
- **n8n Workflows:** Watcher (detect changes), Dispatcher (route tasks), Sync (periodic maintenance)
- **Constraints:** Still INFRA_ONLY, Human-in-the-Loop for critical actions, Drive State experimental
- **Focus:** Reactive automation, gap detection, Drive State Layer setup

**Stage 3: AgentKit Super-Layer (Phase 3+)**
- **Sync Agent:** Full platform (AgentKit meta-coordinator, Sync Agent as orchestrator)
- **State Layer:** GitHub (infra/code) + Drive (tasks/context) fully integrated
- **Interfaces:** Claude (executor), GPT (planner), AgentKit (super-layer), n8n (executor), Google Sheets (Control Plane UI)
- **New Capabilities:**
  - MASTER_CONTROL Sheet: Dashboard UI with state machine
  - AgentKit reuses MCP servers (no duplicate integrations)
  - Visual Builder + Export to Code
  - Apps Script webhooks → n8n workflows
- **Constraints:** Transitions to LIFE_AUTOMATIONS mode (with safeguards), Human-in-the-Loop for sensitive tasks
- **Focus:** Production-grade automation, knowledge management, life task execution

---

**Design Principle for All Stages:**
- **State Layer remains SSOT** — files in GitHub/Drive are the truth, not agent memory
- **Human-in-the-Loop always available** — Or can intervene at any stage
- **Incremental enhancement** — each stage builds on the previous, no breaking changes

---

**Next Steps:**
1. Or reviews this spec (including evolution path)
2. If approved → Claude implements first Sync Agent v0 run
3. Test workflow: Run OODA loop in next session
4. Log results to EVENT_TIMELINE
5. Iterate and improve based on real usage
6. Prepare for Phase 2.4 transition (n8n integration design)

---

## 9. Evolution Path & Super-Layer (Design)

**Current State (Phase 2.2-2.3):**
- Sync Agent v0 is **manual** and **session-based**
- State Layer is **file-based** (GitHub repo only)
- Interfaces: Claude (hands), GPT (architect), n8n (planned but not active)

**Future State (Phase 3+):**
- Sync Agent evolves into **Agent Platform** using **OpenAI AgentKit**
- State Layer expands to **Google Drive** (tasks, context, knowledge)
- Control Plane UI: **Google Sheets** (MASTER_CONTROL dashboard)

---

### 9.1 Evolution Stages

**Stage 1: Manual Sync (Phase 2.2-2.3) — Current**
- Sync Agent v0 = Claude Desktop running OODA manually
- State Layer = files in GitHub (SYSTEM_STATE_COMPACT.json, EVENT_TIMELINE.jsonl, etc.)
- No automation, full Human-in-the-Loop
- Focus: stabilizing State Layer, documenting interfaces

**Stage 2: n8n Nervous System (Phase 2.4)**
- n8n becomes the "nervous system" of AI-OS
- 3 core workflows:
  - **Watcher:** Detects changes in State Layer (GitHub webhooks, file polling)
  - **Dispatcher:** Routes tasks to appropriate agent (Claude/GPT/API)
  - **Sync:** Periodic healthchecks, state refresh, gap detection
- Semi-automated: n8n triggers Sync Agent on events, but Or approves actions
- Drive State Layer begins: Active Context, Knowledge Graph files

**Stage 3: AgentKit Super-Layer (Phase 3+)**
- **OpenAI AgentKit** becomes the reasoning/planning layer
- **MCP servers reuse:** AgentKit uses existing MCP tools (GitHub, Google, Filesystem) — no duplication
- **Visual Builder + Export to Code:** Design agents visually, export to Python/TS, manage in GitHub
- **Google Sheets Control Plane:** MASTER_CONTROL sheet as UI for state machine
- **State Machine enforced:** DRAFT → QUEUED → PROCESSING → REVIEW_NEEDED → APPROVED → COMPLETED/ERROR
- **Apps Script webhooks:** Sheet updates trigger n8n workflows

---

### 9.2 Why AgentKit as Super-Layer?

**Reasoning from Research:**
- AgentKit supports **MCP natively** → reuses Claude's existing MCP servers
- Works well with **n8n** as execution engine: AgentKit decides, n8n executes
- **Visual Builder** reduces prompt engineering burden for complex workflows
- **Export to Code** allows version control in GitHub
- OpenAI's **o1/GPT-4o models** provide strong planning capabilities

**What AgentKit is NOT:**
- Not a replacement for Claude Desktop (local executor)
- Not a replacement for n8n (deterministic workflows)
- Not a replacement for State Layer (files remain SSOT)

**What AgentKit IS:**
- A **meta-coordinator** that sits above current interfaces
- Reads State Layer → reasons → calls MCP tools → triggers n8n flows
- Provides **Visual UI** for designing complex agent behaviors

---

### 9.3 MCP Reuse Strategy

**Current MCP Servers (Phase 2):**
- GitHub Client (port 8081)
- Google Workspace Client (port 8082)
- Filesystem tools
- Browser automation
- Windows automation

**Future (Phase 3+):**
- **AgentKit agents** will call these same MCP servers
- No need to rebuild integrations — just configure AgentKit to use MCP endpoints
- Example flow:
  ```
  AgentKit Agent → MCP GitHub Client → GitHub API → Update State Layer → EVENT_TIMELINE logged
  ```

**Benefits:**
- DRY: Don't Repeat Yourself — no duplicate integrations
- Consistency: Same tools used by Claude and AgentKit
- Version control: MCP server improvements benefit both

---

### 9.4 Design Hooks (Not Implementation)

**CRITICAL:** Stage 2 and Stage 3 are **design-only** at this phase.

**What we prepare now (Phase 2.2-2.3):**
- Document State Layer structure to be **AgentKit-compatible**
- Design EVENT_TIMELINE schema to support **state machine** fields (optional now, required later)
- Create **placeholder** in AUTOMATIONS_REGISTRY for future AgentKit agents
- Keep State Layer **clean and well-documented** so AgentKit can read it easily

**What we do NOT implement now:**
- No AgentKit setup or configuration
- No n8n workflows (beyond planning)
- No Google Sheets Control Plane UI
- No Apps Script webhooks

**Why prepare?**
- Avoid re-architecture later — design State Layer right now
- Make Phase 3 transition smooth — no breaking changes to State Layer
- Keep options open — AgentKit, Vertex AI, or other platforms could work

---

## 10. Google Workspace Control Plane (Future Design)

**Status:** Design Phase — NOT implemented in Phase 2.2-2.3

**Purpose:** Use Google Sheets + Drive as UI and state management for AI-OS in Phase 3+.

---

### 10.1 Why Google Sheets as Control Plane?

**Problem with Chat UI:**
- No visibility into 10+ parallel tasks
- Hard to intervene mid-execution
- Everything is unstructured text
- No persistent state

**Solution: MASTER_CONTROL Sheet**
- **Dashboard:** See all tasks at a glance (status, priority, links)
- **State Machine:** Task status as FSM (DRAFT → QUEUED → PROCESSING → etc.)
- **Human-in-the-Loop:** Or approves transitions (REVIEW_NEEDED → APPROVED)
- **Structured Data:** Each task = row with UUID, timestamp, intent, parameters (JSON)

---

### 10.2 MASTER_CONTROL Sheet Structure

**Sheet: COMMAND_CENTER**

| TASK_UUID | TIMESTAMP | TRIGGER_SOURCE | INTENT | PARAMETERS_JSON | STATUS | LINKED_STATE_FILE | OUTPUT_SUMMARY |
|-----------|-----------|----------------|--------|-----------------|--------|-------------------|----------------|
| uuid-001 | 2025-11-26T10:00 | Manual | Meeting_Prep | `{"meeting_id": "cal-123"}` | COMPLETED | `/Active_Context/meeting-cal-123.json` | [Brief ready](link) |
| uuid-002 | 2025-11-26T11:00 | Calendar | Research | `{"topic": "AI agents"}` | PROCESSING | `/Active_Context/research-ai-agents.json` | In progress... |
| uuid-003 | 2025-11-26T12:00 | Email | Knowledge_Ingest | `{"doc_id": "doc-456"}` | REVIEW_NEEDED | `/Inbox/doc-456.md` | [Review](link) |

---

### 10.3 State Machine (Task Lifecycle)

```
DRAFT
  ↓
QUEUED ──► (Or or automation queues the task)
  ↓
PROCESSING ──► (Agent/n8n working on it)
  ↓
REVIEW_NEEDED ──► (Human review required)
  ↓
APPROVED ──► (Or approves)
  ↓
COMPLETED
  ↓
ARCHIVED

(Error path)
PROCESSING → ERROR → RETRY → QUEUED (or) → FAILED
```

**State Transitions:**
- DRAFT → QUEUED: Or clicks "Queue" button or automation triggers
- QUEUED → PROCESSING: n8n Dispatcher picks up task
- PROCESSING → REVIEW_NEEDED: Agent completes, requires Or's approval
- REVIEW_NEEDED → APPROVED: Or reviews and approves
- APPROVED → COMPLETED: Final execution step
- Any state → ERROR: Something fails, log details
- ERROR → RETRY: Or clicks "Retry" or automation retries

---

### 10.4 Apps Script + n8n Integration

**Apps Script (in MASTER_CONTROL Sheet):**
```javascript
function onEdit(e) {
  var sheet = e.source.getActiveSheet();
  if (sheet.getName() !== "COMMAND_CENTER") return;
  
  var row = e.range.getRow();
  var col = e.range.getColumn();
  var STATUS_COL = 6; // Column F
  
  if (col === STATUS_COL) {
    var status = e.value;
    var triggerStatuses = ["QUEUED", "APPROVED", "RETRY"];
    
    if (triggerStatuses.indexOf(status) !== -1) {
      var rowData = sheet.getRange(row, 1, 1, sheet.getLastColumn()).getValues()[0];
      var payload = {
        task_uuid: rowData[0],
        timestamp: rowData[1],
        intent: rowData[3],
        parameters: JSON.parse(rowData[4]),
        status: rowData[5]
      };
      
      // Send webhook to n8n
      UrlFetchApp.fetch("https://n8n-webhook-url.com/command-center", {
        method: "post",
        contentType: "application/json",
        payload: JSON.stringify(payload)
      });
    }
  }
}
```

**n8n Workflow (Webhook Receiver):**
1. Receive webhook from Apps Script
2. Parse `intent` field → route to sub-workflow:
   - Meeting_Prep → Call AgentKit/Claude to generate briefing
   - Research → Trigger Deep Research workflow
   - Knowledge_Ingest → Parse doc, extract knowledge, update Knowledge Graph
3. Execute sub-workflow
4. Write results to Drive State Layer (`/Active_Context/...`)
5. Update COMMAND_CENTER Sheet:
   - Set STATUS to COMPLETED
   - Add OUTPUT_SUMMARY with link to result
   - Update LINKED_STATE_FILE path

---

### 10.5 Drive State Layer Structure

**Root: `/AI-OS State Layer/`**

**Folder Structure:**
```
/AI-OS State Layer/
├── /01_Active_Context/          # Current tasks, active state
│   ├── task-uuid-001.json       # Task state: status, logs, context
│   ├── task-uuid-002.json
│   └── meeting-cal-123.json     # Meeting prep output
│
├── /02_Knowledge_Graph/         # Long-term knowledge (Markdown)
│   ├── concepts/
│   ├── people/
│   ├── projects/
│   └── index.md                 # Knowledge index
│
├── /03_Inbox/                   # Raw inputs (emails, docs, notes)
│   ├── email-2025-11-26.md
│   ├── doc-456.md
│   └── voice-note-001.txt
│
└── /04_Archive/                 # Completed tasks (moved from Active)
    ├── 2025-11/
    │   ├── task-uuid-001.json
    │   └── task-uuid-002.json
    └── 2025-10/
```

---

**Task State JSON (Example: `/Active_Context/task-uuid-001.json`):**
```json
{
  "task_uuid": "uuid-001",
  "created_at": "2025-11-26T10:00:00Z",
  "updated_at": "2025-11-26T10:30:00Z",
  "intent": "Meeting_Prep",
  "parameters": {
    "meeting_id": "cal-123",
    "attendees": ["alice@example.com", "bob@example.com"],
    "agenda": "Q4 Planning"
  },
  "status": "COMPLETED",
  "execution_log": [
    {"timestamp": "2025-11-26T10:00:00Z", "actor": "n8n Dispatcher", "action": "Task queued"},
    {"timestamp": "2025-11-26T10:05:00Z", "actor": "AgentKit", "action": "Started briefing generation"},
    {"timestamp": "2025-11-26T10:25:00Z", "actor": "AgentKit", "action": "Briefing completed"},
    {"timestamp": "2025-11-26T10:30:00Z", "actor": "n8n", "action": "Updated Sheet, marked COMPLETED"}
  ],
  "output": {
    "type": "Google Doc",
    "url": "https://docs.google.com/document/d/...",
    "summary": "Meeting briefing with 3 agenda items, background research, and suggested talking points."
  },
  "linked_files": [
    "/Knowledge_Graph/projects/Q4_Planning.md"
  ]
}
```

---

### 10.6 Sync Between GitHub State & Drive State

**Two State Layers:**
- **GitHub State Layer** (Phase 2.2-2.3): Files in `/docs/system_state/`
  - Source of truth for: infrastructure, services, automations, events
  - Managed by: Claude Desktop, Git
  - Format: JSON, JSONL, Markdown
  
- **Drive State Layer** (Phase 3+): Files in `/AI-OS State Layer/`
  - Source of truth for: tasks, context, knowledge, inbox
  - Managed by: GPT Operator, n8n, AgentKit
  - Format: JSON, Markdown

**Sync Strategy:**
- **No direct sync** — two layers serve different purposes
- **Links between layers:**
  - EVENT_TIMELINE (GitHub) can reference Drive files: `"linked_drive_file": "/Active_Context/task-uuid-001.json"`
  - Task JSON (Drive) can reference GitHub commits: `"related_commit": "abc123"`
- **Sync Agent reads both:**
  - Phase 2: Reads GitHub only
  - Phase 3+: Reads GitHub + Drive, identifies gaps between them

---

### 10.7 Constraints (Phase 2.2-2.3)

**This section is DESIGN-ONLY.**

**What we do NOT do now:**
- ❌ Create MASTER_CONTROL Sheet
- ❌ Write Apps Script webhooks
- ❌ Set up Drive State Layer folders
- ❌ Configure n8n to listen to Sheets

**What we DO prepare now:**
- ✅ Design State Layer to be **Drive-compatible**
- ✅ Add optional `"task_status"` field to EVENT_TIMELINE schema
- ✅ Document future sync strategy between GitHub + Drive
- ✅ Ensure STATE_LAYER_BASELINE_V1 remains the foundation

**Why design now?**
- Avoid re-architecture later
- Make Phase 3 transition smooth
- Keep State Layer clean and extensible

---

## 11. State Machine & Task Lifecycle (Future Design)

**Status:** Design Phase — NOT implemented in Phase 2.2-2.3

**Purpose:** Define task states and lifecycle for Phase 3+ (Google Sheets Control Plane).

---

### 11.1 Task State Machine

```
┌──────────┐
│  DRAFT   │ ──► Or creates task, fills parameters
└────┬─────┘
     │
     ↓
┌──────────┐
│  QUEUED  │ ──► Or or automation queues task for execution
└────┬─────┘
     │
     ↓
┌─────────────┐
│ PROCESSING  │ ──► Agent/n8n working on task
└──────┬──────┘
       │
       ├──► (Success path)
       ↓
 ┌─────────────────┐
 │ REVIEW_NEEDED   │ ──► Human review required before completion
 └────────┬────────┘
          │
          ↓
    ┌──────────┐
    │ APPROVED │ ──► Or approves, final execution
    └────┬─────┘
         │
         ↓
    ┌───────────┐
    │ COMPLETED │ ──► Task done, results available
    └─────┬─────┘
          │
          ↓
    ┌──────────┐
    │ ARCHIVED │ ──► Moved to /Archive/ folder
    └──────────┘

       │
       ├──► (Error path)
       ↓
   ┌───────┐
   │ ERROR │ ──► Something failed, details logged
   └───┬───┘
       │
       ├──► Or clicks "Retry"
       ↓
   ┌───────┐
   │ RETRY │ ──► Back to QUEUED
   └───┬───┘
       │
       ├──► (If retry fails multiple times)
       ↓
   ┌────────┐
   │ FAILED │ ──► Permanent failure, manual intervention needed
   └────────┘
```

---

### 11.2 Integration with Current State Layer

**Phase 2.2-2.3 (Current):**
- **Optional:** EVENT_TIMELINE events can include `"task_status"` field
- **Example:**
  ```json
  {
    "timestamp": "2025-11-26T14:00:00Z",
    "event_type": "block_complete",
    "event_id": "EVT-2025-11-26-009",
    "actor": "Claude Desktop",
    "action": "BLOCK_HEALTHCHECK_REFRESH completed",
    "task_status": "COMPLETED"
  }
  ```
- **Not required:** State machine is design-only, not enforced

**Phase 3+ (Future):**
- **Required:** Every task in MASTER_CONTROL Sheet has `STATUS` column
- **Enforced:** Apps Script validates state transitions
- **Logged:** Every transition logged to EVENT_TIMELINE + Drive task JSON

---

### 11.3 AUTOMATIONS_REGISTRY Integration

**Current (Phase 2.2-2.3):**
- AUTOMATIONS_REGISTRY tracks automations: `{"id": "AUTO-001", "status": "up", ...}`
- Status values: `up`, `down`, `partial`, `planned`, `not_configured`

**Future (Phase 3+):**
- Add `"current_task_status"` field for automations that execute tasks:
  ```json
  {
    "id": "AUTO-010",
    "name": "n8n Meeting Prep Workflow",
    "type": "n8n_workflow",
    "status": "up",
    "current_task_status": "PROCESSING",
    "last_task_uuid": "uuid-001",
    "last_run": "2025-11-26T14:00:00Z"
  }
  ```
- Sync Agent can detect: "Automation is 'up' but task status is 'ERROR' → investigate"

---

### 11.4 State Transitions & Permissions

**Who can transition states:**

| Transition | Allowed Actors | Mechanism |
|------------|----------------|-----------|
| DRAFT → QUEUED | Or, GPT Operator | Manual (Sheet edit) or automation (calendar trigger) |
| QUEUED → PROCESSING | n8n Dispatcher | Automatic (when workflow starts) |
| PROCESSING → REVIEW_NEEDED | Agent (Claude, GPT, AgentKit) | Automatic (when task needs human review) |
| REVIEW_NEEDED → APPROVED | Or only | Manual (Sheet edit, Or's decision) |
| APPROVED → COMPLETED | Agent or n8n | Automatic (final execution step) |
| COMPLETED → ARCHIVED | Sync Agent or cron | Automatic (after X days) |
| Any → ERROR | Any agent | Automatic (on failure, with error details logged) |
| ERROR → RETRY | Or or automation | Manual or policy-based (retry up to 3 times) |
| RETRY → FAILED | System | Automatic (after max retries exceeded) |

---

### 11.5 Constraints (Phase 2.2-2.3)

**This is design-only.**

**What we do NOT implement now:**
- ❌ Enforce state machine in code
- ❌ Require `task_status` field in events
- ❌ Build UI for state transitions

**What we DO prepare now:**
- ✅ Add **optional** `task_status` field to EVENT_TIMELINE schema
- ✅ Document state machine for future reference
- ✅ Design AUTOMATIONS_REGISTRY to support task tracking

**Why design now?**
- Ensure EVENT_TIMELINE schema is extensible
- Avoid breaking changes when Sheets Control Plane is added
- Provide clear path from manual (Phase 2) to automated (Phase 3+)

---

**Version:** 0.2 (Enhanced)  
**Status:** Design complete, awaiting Or's approval  
**To be committed:** After review  

> "Coordination without a shared blackboard is chaos — clarity comes from a single source of truth. The future is designed today."
