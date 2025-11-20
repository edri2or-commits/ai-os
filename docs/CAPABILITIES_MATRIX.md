# AI-OS – CAPABILITIES MATRIX (Version 1.0)

**מפת היכולות של מערכת ההפעלה האישית**

**תאריך יצירה**: 20 נובמבר 2025  
**גרסה**: 1.0 (AI-OS Bootstrap)  
**עדכון אחרון**: 20 נובמבר 2025

---

## מטרת המסמך

מסמך זה הוא **מקור האמת היחיד (SSOT)** לכל היכולות התפעוליות של מערכת AI-OS.

**למה זה חשוב?**
- **סנכרון בין מודלים**: כשאני עובד עם Claude, GPT, או סוכנים אחרים - כולם מסתכלים על אותו מסמך ויודעים מה המערכת יודעת לעשות.
- **שקיפות מלאה**: אני יודע בדיוק מה עובד, מה לא עובד, ומה בתכנון.
- **מניעת כפילויות**: אם יכולת כבר קיימת, לא בונים אותה שוב.
- **תכנון מושכל**: לפני שמוסיפים יכולת חדשה, בודקים אם היא משתלבת עם הקיים.

---

## רשימת סטטוסים

| סטטוס | משמעות | דוגמה |
|-------|--------|-------|
| ✅ **Operational** | עובד ומוכן לשימוש | GitHub Read/Write דרך MCP |
| 🚧 **Partial** | עובד חלקית או עם מגבלות | GPT GitHub Agent (DRY RUN בלבד) |
| 📋 **Designed** | תוכנן ומתועד, אבל לא מומש | GitHub Executor API |
| 🔄 **Planned** | בתכנון ראשוני | אינטגרציה מלאה עם Google Workspace |
| ❌ **Not Available** | לא קיים ולא בתכנית מיידית | Voice/Audio Control |
| 🗄️ **Legacy** | קיים בריפו הישן, טרם הוחלט על גורלו | Autopilot Self-Healing |

---

## טבלת יכולות

| CapabilityID | יכולת | תיאור קצר | Agents מעורבים | Tools / APIs | Status | Notes |
|--------------|--------|------------|-----------------|-------------|--------|-------|
| **GH-001** | GitHub Repository Analysis | קריאה וניתוח של ריפואים ב-GitHub | GPT GitHub Agent | GitHub MCP | ✅ Operational | עובד דרך Claude Desktop MCP |
| **GH-002** | GitHub Planning (DRY RUN) | תכנון פעולות GitHub (ללא ביצוע) | GPT GitHub Agent | `gpt_agent/github_agent.py` | 🚧 Partial | מתכנן בלבד, לא מבצע |
| **GH-003** | GitHub Direct Writes (Docs) | כתיבה ישירה לקבצי תיעוד ב-GitHub | GPT GitHub Agent | GitHub MCP | ✅ Operational | רק לקבצי Docs/State (OS_SAFE) |
| **GH-004** | GitHub PR Creation | יצירת Pull Requests | - | GitHub MCP | ✅ Operational | ידני או דרך Claude |
| **GH-005** | GitHub Executor API | API אוטומציה מלאה של GitHub | - | Cloud Run API (להיות) | 📋 Designed | קוד מוכן, deployment חסום |
| **FS-001** | Local File System Access | קריאה/כתיבה לקבצים מקומיים | - | Filesystem MCP | ✅ Operational | גישה בתוך allowed directories |
| **FS-002** | File Search & Analysis | חיפוש וניתוח קבצים | - | Filesystem MCP | ✅ Operational | תמיכה ב-patterns ו-exclusions |
| **WIN-001** | Windows PowerShell Execution | הרצת פקודות PowerShell | - | Windows MCP | ✅ Operational | 10+ פקודות מאושרות |
| **WIN-002** | Windows Shell Control | שליטה ב-UI של Windows | - | Windows MCP | ✅ Operational | Click, Type, Scroll וכו' |
| **WIN-003** | Windows Application Launch | הפעלת אפליקציות Windows | - | Windows MCP | ✅ Operational | דרך Start Menu |
| **MCP-001** | MCP Orchestration (Legacy) | ניהול מרכזי של סוכנים וזרימות | MCP Master Control | `mcp/` directory | 🗄️ Legacy | קיים בריפו הישן, טרם יובא |
| **MCP-002** | MCP GitHub Integration | אינטגרציה בין MCP ל-GitHub | - | `mcp/github/` | 🗄️ Legacy | טרם הוחלט על ייבוא |
| **MCP-003** | MCP Google Integration | אינטגרציה בין MCP ל-Google | - | `mcp/google/` | 🗄️ Legacy | טרם הוחלט על ייבוא |
| **GGL-001** | Google Calendar Read | קריאת אירועים מיומן | - | Google MCP | ✅ Operational | READ-ONLY |
| **GGL-002** | Google Gmail Read | קריאת מיילים | - | Google MCP | ✅ Operational | READ-ONLY |
| **GGL-003** | Google Drive Read | קריאת קבצים מ-Drive | - | Google MCP | ✅ Operational | READ-ONLY |
| **GGL-004** | Google Workspace Write | כתיבה ל-Google Workspace | - | Google MCP (להרחיב) | 🔄 Planned | דורש OAuth scopes נוספים |
| **KB-001** | Knowledge Base Reading | קריאת מסמכי ידע והחלטות | - | Filesystem MCP | ✅ Operational | `docs/`, `decisions/`, `plans/` |
| **KB-002** | Decision Records (ADRs) | ניהול החלטות אדריכליות | OPS Decision Manager | `ops/decisions/` | 🗄️ Legacy | טרם יובא |
| **DIAG-001** | System Diagnostics | אבחון מצב המערכת | OPS Diagnostics | `ops/diag/` | 🗄️ Legacy | טרם יובא |
| **DIAG-002** | Health Checks | בדיקות בריאות של רכיבים | - | Various | 🔄 Planned | צריך להגדיר |
| **AUTO-001** | Self-Healing (Autopilot) | החלמה עצמית מכשלים | Autopilot Agent | `autopilot.py` | 🗄️ Legacy | POC בלבד, טרם הוחלט |
| **EXEC-001** | Local Execution | ביצוע פעולות מקומיות | Local Execution Agent | `agents/local_execution_agent.py` | 🗄️ Legacy | Placeholder בלבד |

---

## פירוט לפי קטגוריות

### 📂 **1. GitHub & Code Operations**

**יכולות**: GH-001 עד GH-005

**מה זה אומר בפועל?**
- אני יכול לבקש מהמערכת לנתח ריפו, לקרוא קבצים, ולעדכן תיעוד ישירות.
- כשצריך לשנות קוד או workflows - המערכת מתכננת לי תוכנית מפורטת (GPT GitHub Agent).
- בעתיד: אוטומציה מלאה דרך GitHub Executor API.

**סטטוס נוכחי**:
- ✅ **קריאה וניתוח**: עובד מעולה דרך Claude Desktop + MCP
- ✅ **עדכון תיעוד**: עובד (OS_SAFE - קבצי Docs בלבד)
- 🚧 **תכנון משימות**: עובד במצב DRY RUN (GPT GitHub Agent)
- 📋 **ביצוע אוטומטי**: מתוכנן (GitHub Executor API)

**דוגמה לשימוש**:
> "קרא את הקובץ `README.md` בריפו `ai-os`, ועדכן את הסעיף 'המטרות' עם הטקסט הבא..."

---

### 🖥️ **2. Local Machine & Windows Control**

**יכולות**: FS-001, FS-002, WIN-001, WIN-002, WIN-003

**מה זה אומר בפועל?**
- אני יכול לבקש מהמערכת לקרוא/לכתוב קבצים במחשב שלי.
- להריץ פקודות PowerShell (עם הגבלות בטיחות).
- לשלוט באפליקציות Windows (לחיצות, הקלדה, גלילה).

**סטטוס נוכחי**:
- ✅ **גישה לקבצים**: עובד בתוך תיקיות מאושרות
- ✅ **פקודות PowerShell**: 10+ פקודות מאושרות זמינות
- ✅ **שליטה ב-UI**: Click, Type, Scroll, Launch apps

**דוגמה לשימוש**:
> "צור קובץ חדש בשם `report.txt` בתיקיית Downloads עם התוכן הבא..."
> "הפעל את Excel וצור קובץ חדש"

---

### ⚙️ **3. MCP & System Orchestration**

**יכולות**: MCP-001, MCP-002, MCP-003

**מה זה אומר בפועל?**
- MCP (Master Control Program) היה "המוח" של המערכת הישנה.
- הוא ניהל תזמון, אינטגרציות, וסנכרון בין סוכנים שונים.

**סטטוס נוכחי**:
- 🗄️ **Legacy**: כל רכיבי ה-MCP עדיין בריפו הישן
- ⏳ **החלטה נדרשת**: האם לייבא? איך לפרק לרכיבים?

**שאלות פתוחות**:
1. האם MCP נחוץ ב-AI-OS או שאפשר לבנות מנגנון פשוט יותר?
2. אם כן - איזה חלקים לייבא ראשונים?
3. האם לשמור את הארכיטקטורה המקורית או לעצב מחדש?

---

### 🌐 **4. Google Workspace & Cloud**

**יכולות**: GGL-001 עד GGL-004

**מה זה אומר בפועל?**
- אני יכול לבקש מהמערכת לקרוא אימיילים, אירועי יומן, או קבצים ב-Drive.
- כרגע רק קריאה (READ-ONLY).
- בעתיד: כתיבה מלאה (שליחת מיילים, יצירת אירועים, עדכון מסמכים).

**סטטוס נוכחי**:
- ✅ **קריאה**: Calendar, Gmail, Drive - הכל עובד
- 🔄 **כתיבה**: בתכנון (דורש OAuth scopes נוספים)

**דוגמה לשימוש**:
> "הצג לי את 5 המיילים האחרונים שקיבלתי"
> "מה יש לי ביומן מחר?"

---

### 📚 **5. Knowledge Base & Documentation**

**יכולות**: KB-001, KB-002

**מה זה אומר בפועל?**
- המערכת יכולה לקרוא ולנתח את כל מסמכי התיעוד, החלטות ותוכניות.
- זה מאפשר לסוכנים "ללמוד" מההיסטוריה ולקבל החלטות מושכלות.

**סטטוס נוכחי**:
- ✅ **קריאה**: `docs/`, `decisions/`, `plans/` - הכל זמין
- 🗄️ **ADRs מהריפו הישן**: טרם יובאו

**דוגמה לשימוש**:
> "קרא את החוקה של AI-OS והסבר לי את העיקרון השלישי"
> "מה ההחלטות האחרונות שתועדו במערכת?"

---

### 🔍 **6. Diagnostics & Observability**

**יכולות**: DIAG-001, DIAG-002

**מה זה אומר בפועל?**
- המערכת יכולה לבדוק את עצמה: האם הכל עובד? איפה יש בעיות?
- כרגע רוב כלי האבחון עדיין בריפו הישן.

**סטטוס נוכחי**:
- 🗄️ **OPS Diagnostics**: טרם יובאו
- 🔄 **Health Checks**: צריך להגדיר מה לבדוק

**שאלות פתוחות**:
1. אילו health checks חיוניים ל-AI-OS?
2. איך מדווחים על בעיות (logs? alerts? dashboard?)

---

### 🤖 **7. Self-Healing & Automation**

**יכולות**: AUTO-001, EXEC-001

**מה זה אומר בפועל?**
- **Autopilot**: סוכן שמנסה לתקן בעיות אוטומטית (למשל, לשחזר גישה ל-Google Sheets).
- **Local Execution**: סוכן שאמור להריץ פעולות מקומיות.

**סטטוס נוכחי**:
- 🗄️ **Autopilot**: POC בלבד בריפו הישן, טרם הוחלט אם רלוונטי
- 🗄️ **Local Execution Agent**: קובץ Placeholder ריק

**שאלות פתוחות**:
1. האם Self-Healing נחוץ? אם כן - באילו תרחישים?
2. האם Local Execution Agent צריך להתפתח או לזרוק?

---

### 🔮 **8. Future / Planned Capabilities**

**יכולות שבתכנון או שחסרות**:

| יכולת | סטטוס | הערות |
|-------|-------|-------|
| **Voice/Audio Control** | ❌ Not Available | לא קיים ולא בתכנית מיידית |
| **OS GUI Automation (Advanced)** | 🔄 Planned | מעבר לשליטה בסיסית |
| **Telegram Integration** | 🗄️ Legacy | מוזכר באודיט, טרם הוחלט |
| **Make.com Workflows** | 🗄️ Legacy | מוזכר באודיט, טרם הוחלט |
| **GPT API Direct Calls** | 🔄 Planned | לסוכנים שצריכים GPT ישירות |
| **Multi-Agent Coordination** | 🔄 Planned | ריבוי סוכנים שעובדים ביחד |

---

## נקודות לא ברורות / שאלות פתוחות

### 🔴 **גבוה (Critical) - דורש החלטה מיידית**

1. **MCP Orchestration**:
   - ❓ האם לייבא את כל מערכת ה-MCP מהריפו הישן?
   - ❓ אם כן - איך לפרק לרכיבים (`mcp/server/`, `mcp/clients/`, `mcp/github/`, `mcp/google/`)?
   - ❓ אם לא - איך מתפקדים בלי מנגנון ניהול מרכזי?

2. **GitHub Executor API**:
   - ❓ לפתח אותו ב-AI-OS או להשתמש בגרסה הקיימת?
   - ❓ איפה ל-deploy (Cloud Run? Local server?)?
   - ❓ איך מתחברים אליו (API key? OAuth?)?

3. **GPT GitHub Agent - Executor Mode**:
   - ❓ להשאיר DRY RUN או לשדרג ל-Executor?
   - ❓ אם Executor - רק OS_SAFE או גם CLOUD_OPS_HIGH (עם אישור)?

---

### 🟡 **בינוני (Medium) - חשוב אבל לא דחוף**

4. **Autopilot Self-Healing**:
   - ❓ האם רלוונטי ל-AI-OS?
   - ❓ אם כן - אילו תרחישים צריך לטפל בהם?

5. **Local Execution Agent**:
   - ❓ לפתח או לזרוק?
   - ❓ אם לפתח - מה התפקיד המדויק?

6. **OPS Components** (Decisions, Diagnostics, Triggers):
   - ❓ אילו חלקים לייבא ראשונים?
   - ❓ איך משתלבים עם המערכת החדשה?

---

### 🟢 **נמוך (Low) - נחמד לדעת**

7. **Google Workspace Write**:
   - ❓ באיזה עדיפות לפתח?
   - ❓ אילו פעולות חיוניות (שליחת מייל? יצירת אירוע?)?

8. **Telegram / Make.com Integration**:
   - ❓ האם אלה כלים שעדיין בשימוש?
   - ❓ אם כן - איך מתועדים ומשתלבים?

9. **Health Checks & Monitoring**:
   - ❓ מה צריך לבדוק?
   - ❓ איך מדווחים (logs? dashboard? alerts?)?

---

## מדיניות עדכון

**חוקי עדכון של CAPABILITIES_MATRIX**:

1. ✅ **הוספת יכולת חדשה**:
   - חייב להוסיף שורה לטבלה הראשית
   - חייב לעדכן את הקטגוריה הרלוונטית
   - חייב לתעד ב-commit message

2. ✅ **שינוי סטטוס**:
   - חייב לעדכן את עמודת Status
   - מומלץ להוסיף הערה ב-Notes למה השתנה

3. ✅ **הסרת יכולת**:
   - לא מוחקים! משנים ל-❌ Not Available
   - מוסיפים הערה למה הוסרה

4. ✅ **גרסאות**:
   - כל שינוי משמעותי = עדכון מספר גרסה
   - Minor: 1.0 → 1.1 (הוספת יכולת אחת)
   - Major: 1.x → 2.0 (שינוי ארכיטקטורה)

---

**סטטוס מסמך זה**: ✅ Bootstrap Version  
**עדכון הבא מתוכנן**: אחרי ייבוא הסוכן הראשון (GPT GitHub Agent)  
**צעד הבא**: החלטות על 9 השאלות הפתוחות + התחלת ייבוא יכולות מהריפו הישן
