# AGENT_SYNC_SPEC_BLACKBOARD_V0.md

**Version:** 0.1 (Draft)  
**Created:** 2025-11-26  
**Author:** Claude Desktop (Block 3)  
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

### 5.3 Future: n8n / AgentKit

**תפקיד:** "המפעילים" — Automation Executors (עתידי)

**מתי יפעל:**
- **כרגע:** לא פעיל (Phase 2.2–2.3 הוא INFRA_ONLY)
- **בעתיד (Phase 2.4+):** כשעוברים ל-LIFE_AUTOMATIONS mode

**איך יתחברו לState Layer:**
1. **EVENT_TIMELINE monitoring:**
   - n8n webhook מקשיב לשינויים ב-EVENT_TIMELINE (דרך GitHub webhook או Google Sheets sync)
   - כשאירוע חדש מתועד → n8n מפעיל workflow תואם

2. **AUTOMATIONS_REGISTRY as source:**
   - n8n קורא את AUTOMATIONS_REGISTRY לזיהוי אוטומציות שצריך להפעיל
   - AgentKit משתמש ב-SYSTEM_STATE_COMPACT כ-context למשימות

3. **Write back to State Layer:**
   - n8n לוגג ל-EVENT_TIMELINE כל פעולה שהוא מבצע
   - AgentKit מעדכן AUTOMATIONS_REGISTRY כש-automation חדש נוסף

**אבטחה:**
- Human-in-the-loop: כל automation דורש אישור מ-Or לפני הפעלה ראשונה
- Sandbox: בדיקות ב-test environment לפני production

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

**Next Steps:**
1. Or reviews this spec
2. If approved → Claude implements first Sync Agent v0 run
3. Test workflow: Run OODA loop in next session
4. Log results to EVENT_TIMELINE
5. Iterate and improve based on real usage

---

**Version:** 0.1 (Draft)  
**Status:** Awaiting Or's review  
**To be committed:** After approval  

> "Coordination without a shared blackboard is chaos — clarity comes from a single source of truth."
