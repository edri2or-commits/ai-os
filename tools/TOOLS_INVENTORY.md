# Tools & Integrations Inventory – מלאי כלים ואינטגרציות

**מטרת המסמך**: מיפוי מקיף של כל הכלים, אינטגרציות וממשקים במערכת AI-OS.

**תאריך יצירה**: 20 נובמבר 2025  
**גרסה**: 1.0  
**מבוסס על**: CAPABILITIES_MATRIX.md, REPO_AUDIT, SYSTEM_SNAPSHOT, AGENTS_INVENTORY

---

## למה המסמך הזה חשוב?

1. **שקיפות מלאה** - יודעים בדיוק אילו כלים קיימים ומה הם עושים
2. **אבטחה** - מיפוי של כל נקודת גישה וסיקרט
3. **תכנון** - הבנה מה אפשר לעשות ומה חסר
4. **סדר** - אין כפילויות, הכל מתועד במקום אחד

---

## טבלת כלים ואינטגרציות

| # | ToolName | Type | Scope | DefinedIn | SecretsLocation | Status | RiskLevel | Notes |
|---|----------|------|-------|-----------|-----------------|--------|-----------|-------|
| **1** | Claude Desktop | MCP Client | GitHub, Filesystem, Windows, Google | Claude.ai App + Local Config | Local (Claude App) | ✅ Active | High | Gateway לכל ה-MCP servers. גישה מלאה למחשב ולגיטהאב |
| **2** | GitHub MCP Server | MCP | GitHub Repos | Claude Desktop MCP Servers | GitHub OAuth Token (Claude) | ✅ Active | High | קריאה/כתיבה לריפואים. משמש ל-`ai-os` ו-`make-ops-clean` |
| **3** | Filesystem MCP Server | MCP | Local Files | Claude Desktop MCP Servers | None (Local Access) | ✅ Active | High | גישה לקבצים מקומיים בתוך allowed directories |
| **4** | Windows MCP Server | MCP | Windows OS | Claude Desktop MCP Servers | None (Local Access) | ✅ Active | Critical | PowerShell, UI Control, App Launch. גישה מלאה למערכת |
| **5** | Google MCP Server | MCP | Gmail, Calendar, Drive | Claude Desktop MCP Servers | Google OAuth Token (Claude) | ✅ Active (READ) | Medium | READ-ONLY כרגע. Write דורש OAuth נוסף |
| **6** | GPT GitHub Agent | Python Script | GitHub Planning | `make-ops-clean/gpt_agent/github_agent.py` | GPT API Key (env) | 🚧 DRY RUN | Medium | Planner בלבד. אין write permissions |
| **7** | GPT API Wrapper | API Client | OpenAI GPT | `make-ops-clean/gpt-api/` | OpenAI API Key (env) | 🗄️ Legacy | Low | Wrapper ל-GPT API. לא בשימוש אקטיבי |
| **8** | GitHub Executor API | Cloud Run API | GitHub Automation | `make-ops-clean/cloud-run/google-workspace-github-api/` | GitHub PAT (Cloud Run Secrets) | 📋 Designed | Critical | **לא פרוס**. Blueprint בלבד. דורש PAT |
| **9** | MCP Server (Legacy) | Python Server | Agent Orchestration | `make-ops-clean/mcp/server/` | Various (config files) | 🗄️ Legacy | High | Master Control. **לא פעיל**. Reference בלבד |
| **10** | MCP GitHub Integration | Python Module | GitHub via MCP | `make-ops-clean/mcp/github/` | GitHub Token (mcp config) | 🗄️ Legacy | High | חלק מ-MCP הישן. **לא פעיל** |
| **11** | MCP Google Integration | Python Module | Google Workspace | `make-ops-clean/mcp/google/` | Google OAuth (mcp config) | 🗄️ Legacy | High | חלק מ-MCP הישן. **לא פעיל** |
| **12** | Make (Integromat) | SaaS | Automation Platform | `make-ops-clean/automation/` (מוזכר) | Make API Key | ❓ Unknown | Medium | מוזכר באודיט. לא ברור אם בשימוש |
| **13** | Telegram Bot | Bot API | Messaging | `make-ops-clean/` (מוזכר באודיט) | Telegram Bot Token | ❓ Unknown | Medium | מוזכר באודיט. לא ברור אם בשימוש |
| **14** | GitHub Actions | CI/CD | GitHub Workflows | `.github/workflows/` (בריפו) | GitHub Secrets | ❓ Unknown | High | לא ברור אילו workflows קיימים |
| **15** | Cloud Run | Cloud Platform | Hosting | `make-ops-clean/cloud-run/` | GCP Credentials | 🗄️ Legacy | Critical | תוכנן ל-deployment. **לא פרוס** |
| **16** | Autopilot Script | Python Script | Self-Healing | `make-ops-clean/autopilot.py` | Google Sheets API Key | 🗄️ Legacy | Medium | POC להחלמה עצמית. **לא פעיל** |
| **17** | Local Execution Agent | Python Script | Local Commands | `make-ops-clean/agents/local_execution_agent.py` | None | 🗄️ Legacy | High | Placeholder ריק. **לא פעיל** |
| **18** | GitHub Integration Scripts | Python Scripts | GitHub API | `make-ops-clean/github_integration/` | GitHub PAT (env) | 🗄️ Legacy | High | סקריפטים ישנים. **לא בשימוש** |
| **19** | Automation Scripts | Shell/Python | Task Automation | `make-ops-clean/automation/` | Various | 🗄️ Legacy | Medium | Makefiles, cron jobs. **לא בשימוש** |
| **20** | Config Files | YAML/JSON | System Config | `make-ops-clean/config/` | Inline secrets (⚠️) | 🗄️ Legacy | Critical | **דורש סקירת אבטחה**. ייתכן secrets |
| **21** | Canva Integration | API | Design Tools | Claude Desktop Tools | Canva OAuth | ✅ Active | Low | יצירת עיצובים, ניהול תוכן |
| **22** | Browser Control MCP | MCP | Web Browser | Claude Desktop (via MCP) | None (Local) | ✅ Active | Medium | ניווט, צילומי מסך, אינטראקציה |
| **23** | Autonomous Control | MCP | System Commands | Claude Desktop (via MCP) | None (Local) | ✅ Active | Critical | הרצת פקודות, התקנת תוכנה, Git |
| **24** | GitHub Control | MCP | GitHub Mgmt | Claude Desktop (via MCP) | GitHub OAuth | ✅ Active | High | ניהול repos, issues, PRs |

---

## פירוט לפי קטגוריות

### 🟢 **כלים פעילים (Active)**

אלה הכלים שבשימוש **היום** ב-AI-OS:

| Tool | Purpose | Access Level |
|------|---------|-------------|
| **Claude Desktop** | Gateway ראשי למערכת | Full System |
| **GitHub MCP** | עבודה על ריפואים | Read/Write |
| **Filesystem MCP** | גישה לקבצים מקומיים | Read/Write (Allowed dirs) |
| **Windows MCP** | שליטה ב-Windows | Full System |
| **Google MCP** | גישה ל-Gmail, Calendar, Drive | Read-Only |
| **GPT GitHub Agent** | תכנון שינויים ב-GitHub | Planning Only (DRY RUN) |
| **Canva** | יצירת עיצובים | Read/Write |
| **Browser Control** | אוטומציה של דפדפן | Full Browser |
| **Autonomous Control** | פקודות מערכת | Full System |
| **GitHub Control** | ניהול GitHub | Read/Write |

---

### 🟡 **כלים מתוכננים (Planned)**

אלה כלים שצפויים להיות מוספים/משודרגים:

| Tool | What's Missing | Priority |
|------|---------------|----------|
| **Google Workspace Write** | OAuth scopes נוספים | Medium |
| **GitHub Automation** | Executor מוגבל (OS_SAFE) | Low |
| **Health Checks** | מנגנון אבחון אוטומטי | Medium |
| **Multi-Agent Coordination** | תקשורת בין סוכנים | Low |

---

### 🔴 **כלים Legacy (לא פעילים)**

אלה כלים מהריפו הישן ש**לא בשימוש כרגע**:

| Tool | Why Legacy | Decision |
|------|------------|----------|
| **MCP Server** | מערכת מורכבת, נבנה מחדש | Reference Only |
| **GitHub Executor API** | Deployment חסום, בעיות אבטחה | Blueprint Only |
| **GPT API Wrapper** | לא נחוץ (יש API ישיר) | Archive |
| **Autopilot Script** | POC בלבד | Archive (אלא אם...) |
| **Local Execution Agent** | Placeholder ריק | Delete? |
| **GitHub Integration Scripts** | מיושן, יש MCP | Archive |
| **Automation Scripts** | מיושן | Archive |

---

### ❓ **כלים לא ברורים (Unknown)**

אלה דורשים **בדיקה ידנית**:

| Tool | What's Unclear | Action Required |
|------|----------------|-----------------|
| **Make.com** | האם בשימוש? | בדוק workflows |
| **Telegram Bot** | האם בשימוש? איזה bot? | בדוק config |
| **GitHub Actions** | אילו workflows קיימים? | סקור `.github/workflows/` |
| **Config Files** | האם יש secrets inline? | **סקירת אבטחה דחופה** |

---

## מיפוי סיקרטים (Secrets Mapping)

### 🔒 **איפה הסיקרטים חיים**

| Secret Type | Current Location | Recommended Location | Status |
|-------------|------------------|---------------------|--------|
| **GitHub OAuth Token** | Claude Desktop App | Claude App (OK) | ✅ Secure |
| **Google OAuth Token** | Claude Desktop App | Claude App (OK) | ✅ Secure |
| **GPT API Key** | Environment Variables | Env / Secret Manager | ⚠️ Review |
| **GitHub PAT (Executor)** | **Not Set** (Deployment חסום) | Cloud Run Secrets | ❌ N/A |
| **Make API Key** | Unknown | Env / Secret Manager | ⚠️ Unknown |
| **Telegram Bot Token** | Unknown | Env / Secret Manager | ⚠️ Unknown |
| **Google Sheets API** | Unknown (Autopilot) | Not in use | 🗄️ Legacy |
| **Config Files Secrets** | **Inline in code** (⚠️) | **MUST MIGRATE** | 🚨 Critical |

---

### 🚨 **אזהרות אבטחה**

1. **Config Files (`make-ops-clean/config/`)** - **דחוף**:
   - ייתכן שיש secrets inline בקבצי YAML/JSON
   - **חובה**: סרוק ומזז ל-environment variables או secret manager
   - **אל תעלה** את התיקייה הזו לגיט ציבורי

2. **SECRETS/ Directory** - **אל תפתח**:
   - התיקייה `make-ops-clean/SECRETS/` מכילה חומר רגיש
   - **לא לגלוש בה** בלי הכנה מתאימה
   - **לא להעביר** ל-`ai-os` ללא encryption

3. **GitHub PAT** - **חסר**:
   - GitHub Executor API מחכה ל-PAT שלא קיים
   - זה **טוב** - אין deployment מקרי
   - כשנחליט לפרוס - ניצור PAT חדש עם הרשאות מוגבלות

---

## מיפוי רמות סיכון (Risk Levels)

### 🔴 **Critical Risk** (גישה מלאה למערכת)

- **Windows MCP** - שליטה מלאה ב-OS
- **Autonomous Control** - הרצת פקודות
- **GitHub Executor API** (אם יפרוס) - כתיבה אוטומטית לקוד
- **Cloud Run** (אם יפרוס) - גישה לענן
- **Config Files** - ייתכן secrets

**הגנות נדרשות**:
- Human-in-the-loop חובה
- Dry-run לפני ביצוע
- Rollback mechanism
- Audit logs

---

### 🟠 **High Risk** (גישה לנתונים רגישים)

- **Claude Desktop** - gateway לכל המערכת
- **GitHub MCP** - קריאה/כתיבה לקוד
- **Filesystem MCP** - גישה לקבצים
- **MCP Server (Legacy)** - היה orchestrator מרכזי
- **GitHub Integration Scripts** - גישה ישירה ל-API

**הגנות נדרשות**:
- OAuth tokens מאובטחים
- Scope limitations
- Rate limiting
- Error handling

---

### 🟡 **Medium Risk** (גישה מוגבלת)

- **Google MCP** - READ-ONLY כרגע
- **GPT GitHub Agent** - DRY RUN בלבד
- **Browser Control** - מוגבל לדפדפן
- **Make.com** - automation platform
- **Telegram Bot** - messaging
- **Autopilot** - POC בלבד

**הגנות נדרשות**:
- Validation של inputs
- Timeout mechanisms
- Error reporting

---

### 🟢 **Low Risk** (גישה מינימלית)

- **GPT API Wrapper** - קריאה ל-API בלבד
- **Canva** - עיצוב גרפי
- **Local Execution Agent** - placeholder ריק

**הגנות נדרשות**:
- API key rotation
- Basic error handling

---

## תוכנית פעולה (Action Plan)

### 🚨 **דחוף** (Critical Priority)

1. **סקירת אבטחה של `config/`**:
   - סרוק את `make-ops-clean/config/` לחיפוש secrets
   - מזז כל secret ל-environment variables
   - תעד מה מצאת ב-`DECISIONS_AI_OS.md`

2. **אל תיגע ב-`SECRETS/`**:
   - תסמן את התיקייה כ-OFF LIMITS
   - אם צריך גישה - תכנן קודם
   - אל תעלה לגיט בשום מצב

---

### ⚠️ **גבוה** (High Priority)

3. **בירור כלים לא ברורים**:
   - בדוק אם Make.com בשימוש
   - בדוק אם Telegram Bot קיים
   - סרוק `.github/workflows/` ל-GitHub Actions

4. **תיעוד Google MCP**:
   - תעד איזה OAuth scopes יש כרגע
   - תכנן מה צריך ל-Write access
   - רשום ב-`tools/GOOGLE_MCP.md`

---

### 📋 **בינוני** (Medium Priority)

5. **העברת כלים Legacy לארכיון**:
   - העבר `autopilot.py` ל-`archive/`
   - העבר `local_execution_agent.py` ל-`archive/`
   - תעד למה הם לא בשימוש

6. **תכנון GitHub Executor**:
   - קרא את Blueprint הקיים
   - תכנן גרסה חדשה (מאפס)
   - תעד דרישות אבטחה

---

### ✅ **נמוך** (Low Priority)

7. **תיעוד כלים פעילים**:
   - צור `tools/GITHUB_MCP.md`
   - צור `tools/WINDOWS_MCP.md`
   - צור `tools/FILESYSTEM_MCP.md`

8. **ניקוי ריפו ישן**:
   - מחק תיקיות debug/, playground/, demo/
   - ארגן logs/ לפי תאריכים
   - תעד מה נשאר

---

## שאלות פתוחות (Open Questions)

1. **Make.com**: 
   - ❓ האם זה בשימוש אקטיבי?
   - ❓ אם כן - לאילו workflows?
   - ❓ איפה ה-API key?

2. **Telegram Bot**:
   - ❓ איזה bot זה?
   - ❓ מה הוא עושה?
   - ❓ האם רלוונטי ל-AI-OS?

3. **GitHub Actions**:
   - ❓ אילו workflows קיימים?
   - ❓ מתי הם רצים?
   - ❓ האם צריכים אותם?

4. **Autopilot**:
   - ❓ האם מנגנון ההחלמה העצמית רלוונטי?
   - ❓ אם כן - איך לשדרג?
   - ❓ אם לא - למחוק?

5. **Local Execution Agent**:
   - ❓ האם היה מתוכנן לפיתוח?
   - ❓ או סתם placeholder?
   - ❓ למחוק או לפתח?

---

## המלצות כלליות

### ✅ **עשה**:
1. תעד כל כלי חדש ב-`tools/`
2. סמן בבירור את רמת הסיכון
3. רשום איפה הסיקרטים חיים
4. בדוק כלים לא ברורים
5. שמור על SSOT מעודכן

### ❌ **אל תעשה**:
1. אל תפתח את `SECRETS/` בלי תכנון
2. אל תעלה secrets לגיט
3. אל תשתמש בכלים Legacy בלי review
4. אל תייבא config files עם secrets inline
5. אל תפרוס כלים בלי שכבות בטיחות

---

**סטטוס מסמך זה**: ✅ Active  
**עדכון אחרון**: 20 נובמבר 2025  
**כלים מתועדים**: 24  
**כלים פעילים**: 10  
**כלים Legacy**: 8  
**כלים Unknown**: 4  
**רמת סיכון**: 6 Critical, 5 High, 6 Medium, 3 Low  

---

**צעד הבא**: סקירת אבטחה של `config/` וברור כלים Unknown
