# AI-OS – CAPABILITIES MATRIX (Version 1.1)

**מפת היכולות של מערכת ההפעלה האישית**

**תאריך יצירה**: 20 נובמבר 2025  
**גרסה**: 1.2 (Google Workspace Integration)  
**עדכון אחרון**: 24 נובמבר 2025

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
| 🚧 **Operational (Limited)** | עובד עם מגבלות מכוונות | GPT GitHub Agent (DRY RUN בלבד) |
| 📋 **Designed (Not Deployed)** | תוכנן ומתועד, אבל לא פרוס | GitHub Executor API |
| 🔄 **Planned** | בתכנון ראשוני | אינטגרציה מלאה עם Google Workspace |
| ❌ **Not Available** | לא קיים ולא בתכנית מיידית | Voice/Audio Control |
| 🗄️ **Legacy (Reference Only)** | קיים בריפו הישן, משמש כמקור ידע בלבד | MCP Orchestration |

---

## טבלת יכולות

| CapabilityID | יכולת | תיאור קצר | Agents מעורבים | Tools / APIs | Status | Notes |
|--------------|--------|------------|-----------------|-------------|--------|-------|
| **GH-001** | GitHub Repository Analysis | קריאה וניתוח של ריפואים ב-GitHub | GPT GitHub Agent | GitHub MCP | ✅ Operational | עובד דרך Claude Desktop MCP |
| **GH-002** | GitHub Planning (DRY RUN) | תכנון פעולות GitHub (ללא ביצוע) | GPT GitHub Agent | `gpt_agent/github_agent.py` | 🚧 Operational (Limited) | **DECISION 2025-11-20**: Planner בלבד, אין פעולות כתיבה אוטומטיות |
| **GH-003** | GitHub Direct Writes (Docs) | כתיבה ישירה לקבצי תיעוד ב-GitHub | - | GitHub MCP | ✅ Operational | רק דרך Claude ידני, לא דרך GPT Agent |
| **GH-004** | GitHub PR Creation | יצירת Pull Requests | - | GitHub MCP | ✅ Operational | ידני או דרך Claude |
| **GH-005** | GitHub Executor API | API אוטומציה מלאה של GitHub | - | Legacy Blueprint | 📋 Designed (Not Deployed) | **DECISION 2025-11-20**: לא פרוס. משמש כ-Blueprint בלבד |
| **FS-001** | Local File System Access | קריאה/כתיבה לקבצים מקומיים | - | Filesystem MCP | ✅ Operational | גישה בתוך allowed directories |
| **FS-002** | File Search & Analysis | חיפוש וניתוח קבצים | - | Filesystem MCP | ✅ Operational | תמיכה ב-patterns ו-exclusions |
| **WIN-001** | Windows PowerShell Execution | הרצת פקודות PowerShell | - | Windows MCP | ✅ Operational | 10+ פקודות מאושרות |
| **WIN-002** | Windows Shell Control | שליטה ב-UI של Windows | - | Windows MCP | ✅ Operational | Click, Type, Scroll וכו' |
| **WIN-003** | Windows Application Launch | הפעלת אפליקציות Windows | - | Windows MCP | ✅ Operational | דרך Start Menu |
| **MCP-001** | MCP Orchestration | ניהול מרכזי של סוכנים וזרימות | - | Legacy (`mcp/`) | 🗄️ Legacy (Reference Only) | **DECISION 2025-11-20**: לא פעיל. משמש כמקור עיצוב בלבד |
| **MCP-002** | MCP GitHub Integration | אינטגרציה בין MCP ל-GitHub | - | Legacy (`mcp/github/`) | 🗄️ Legacy (Reference Only) | **DECISION 2025-11-20**: לא פעיל. משמש כמקור עיצוב בלבד |
| **MCP-003** | MCP Google Integration | אינטגרציה בין MCP ל-Google | - | Legacy (`mcp/google/`) | 🗄️ Legacy (Reference Only) | **DECISION 2025-11-20**: לא פעיל. משמש כמקור עיצוב בלבד |
| **GGL-001** | Google Calendar Read | קריאת אירועים מיומן | - | Google MCP | ✅ Operational | READ-ONLY |
| **GGL-002** | Google Gmail Read | קריאת מיילים | - | Google MCP | ✅ Operational | READ-ONLY |
| **GGL-003** | Google Drive Read | קריאת קבצים מ-Drive | - | Google MCP | ✅ Operational | READ-ONLY |
| **GGL-004** | Google Gmail Send | שליחת אימיילים דרך Gmail | GPT Custom Action | Google Workspace Client | ✅ Operational | **NEW 2025-11-24**: עובד דרך GPT Actions + ngrok |
| **GGL-005** | Google Calendar Write | יצירת אירועים ביומן | GPT Custom Action | Google Workspace Client | ✅ Operational | **NEW 2025-11-24**: עובד דרך GPT Actions + ngrok |
| **GGL-006** | Google Drive Search | חיפוש קבצים ב-Drive | GPT Custom Action | Google Workspace Client | ✅ Operational | **NEW 2025-11-24**: עובד דרך GPT Actions + ngrok |
| **GGL-007** | Google Sheets Create/Read | יצירת וקריאת גיליונות | GPT Custom Action | Google Workspace Client | ✅ Operational | **NEW 2025-11-24**: עובד דרך GPT Actions + ngrok |
| **GGL-008** | Google Docs Create | יצירת מסמכים | GPT Custom Action | Google Workspace Client | ✅ Operational | **NEW 2025-11-24**: נבדק ועובד! |
| **GGL-009** | Google Tasks Create | יצירת משימות | GPT Custom Action | Google Workspace Client | ✅ Operational | **NEW 2025-11-24**: עובד דרך GPT Actions + ngrok |
| **KB-001** | Knowledge Base Reading | קריאת מסמכי ידע והחלטות | - | Filesystem MCP | ✅ Operational | `docs/`, `decisions/`, `plans/` |
| **KB-002** | Decision Records (ADRs) | ניהול החלטות אדריכליות | - | Legacy (`ops/decisions/`) | 🗄️ Legacy (Reference Only) | טרם יובא ל-AI-OS |
| **DIAG-001** | System Diagnostics | אבחון מצב המערכת | - | Legacy (`ops/diag/`) | 🗄️ Legacy (Reference Only) | טרם יובא ל-AI-OS |
| **DIAG-002** | Health Checks | בדיקות בריאות של רכיבים | - | Various | 🔄 Planned | צריך להגדיר |
| **AUTO-001** | Self-Healing (Autopilot) | החלמה עצמית מכשלים | - | Legacy (`autopilot.py`) | 🗄️ Legacy (Reference Only) | POC בלבד, טרם הוחלט |
| **EXEC-001** | Local Execution | ביצוע פעולות מקומיות | - | Legacy (placeholder) | 🗄️ Legacy (Reference Only) | Placeholder ריק |

---

## החלטות קריטיות (2025-11-20)

### 🔒 **החלטה #1: MCP Orchestration**
**סטטוס**: 🗄️ Legacy (Reference Only)

- MCP לא נלקח כקוד רץ ל-AI-OS.
- משמש **אך ורק** כמקור עיצוב וידע.
- לא פרוס ולא פעיל במערכת.

**רציונל**: 
- MCP היה מערכת מורכבת שהתפתחה אורגנית.
- AI-OS נבנה מאפס עם עקרונות נקיים.
- נשתמש בתובנות מה-MCP אבל נבנה תשתית חדשה ופשוטה יותר.

---

### 🔒 **החלטה #2: GitHub Executor API**
**סטטוס**: 📋 Designed (Not Deployed)

- הקוד הקיים **לא פרוס ולא מופעל**.
- משמש כ-**Blueprint** לתכנון Executor עתידי אפשרי.
- כל אוטומציית כתיבה על GitHub תיבנה מחדש בצורה הדרגתית ובטוחה.

**רציונל**:
- הקוד הקיים תוכנן למערכת אחרת.
- יש בעיות deployment לא פתורות.
- עדיף לבנות מחדש בצורה מבוקרת עם שכבות בטיחות ברורות.

---

### 🔒 **החלטה #3: GPT GitHub Agent – Execution Mode**
**סטטוס**: 🚧 Operational (Limited) - **DRY RUN ONLY**

- הסוכן פועל במצב **Planner בלבד**.
- **אין פעולות כתיבה אוטומטיות** על GitHub דרך הסוכן.
- הסוכן מנתח, מתכנן, ומציע - אבל לא מבצע.

**Roadmap**:
- בעתיד ניתן לשקול מצב Executor מוגבל (OS_SAFE בלבד).
- דורש הגדרת שכבות אבטחה ופיקוח מתאימות.
- Human-in-the-loop נשאר חובה לכל פעולה.

**רציונל**:
- בטיחות מעל הכל.
- צריך לבנות אמון הדרגתי במערכת.
- DRY RUN מאפשר לבדוק את היכולות בלי סיכון.

---

## פירוט לפי קטגוריות

### 📂 **1. GitHub & Code Operations**

**יכולות**: GH-001 עד GH-005

**מה זה אומר בפועל?**
- אני יכול לבקש מהמערכת לנתח ריפו, לקרוא קבצים.
- **GPT GitHub Agent מתכנן** פעולות אבל **לא מבצע אוטומטית**.
- עדכוני תיעוד - אני עושה ידנית דרך Claude Desktop.

**סטטוס נוכחי**:
- ✅ **קריאה וניתוח**: עובד מעולה דרך Claude Desktop + MCP
- ✅ **עדכון תיעוד**: ידני דרך Claude (לא אוטומטי)
- 🚧 **תכנון משימות**: GPT GitHub Agent (DRY RUN) - **לא מבצע!**
- 📋 **ביצוע אוטומטי**: לא פרוס (GitHub Executor API = Blueprint בלבד)

**החלטה חשובה**: 
> כרגע **אין אוטומציה של כתיבה ל-GitHub**. הכל ידני או דרך Claude Desktop בפיקוח אנושי.

**דוגמה לשימוש**:
> "תכנן לי איך לעדכן את `README.md` בריפו `ai-os`" ← GPT Agent מחזיר תוכנית  
> "עדכן את `README.md`" ← אני מבצע ידנית או דרך Claude

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

**החלטה רשמית (2025-11-20)**:
> MCP נשאר **Legacy / Reference Only**.  
> לא נלקח כקוד רץ ל-AI-OS.

**מה זה אומר בפועל?**
- MCP (Master Control Program) היה "המוח" של המערכת הישנה.
- **אנחנו לא משתמשים בו באופן פעיל**.
- נשתמש בתובנות ובעיצוב שלו כהשראה, אבל נבנה מחדש.

**סטטוס נוכחי**:
- 🗄️ **MCP Orchestration**: Reference Only
- 🗄️ **MCP GitHub Integration**: Reference Only
- 🗄️ **MCP Google Integration**: Reference Only

**מה במקום?**
- נבנה מנגנון orchestration פשוט יותר בעתיד.
- כרגע אין צורך במנגנון מרכזי - הסוכנים פועלים בנפרד.

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
- 🗄️ **ADRs מהריפו הישן**: Reference Only (טרם יובאו)

**דוגמה לשימוש**:
> "קרא את החוקה של AI-OS והסבר לי את העיקרון השלישי"
> "מה ההחלטות האחרונות שתועדו במערכת?" ← קרא `docs/DECISIONS_AI_OS.md`

---

### 🔍 **6. Diagnostics & Observability**

**יכולות**: DIAG-001, DIAG-002

**מה זה אומר בפועל?**
- המערכת יכולה לבדוק את עצמה: האם הכל עובד? איפה יש בעיות?
- כרגע רוב כלי האבחון עדיין בריפו הישן (Reference Only).

**סטטוס נוכחי**:
- 🗄️ **OPS Diagnostics**: Reference Only (טרם יובאו)
- 🔄 **Health Checks**: בתכנון (צריך להגדיר מה לבדוק)

**שאלות פתוחות**:
1. אילו health checks חיוניים ל-AI-OS?
2. איך מדווחים על בעיות (logs? alerts? dashboard?)

---

### 🤖 **7. Self-Healing & Automation**

**יכולות**: AUTO-001, EXEC-001

**מה זה אומר בפועל?**
- **Autopilot**: סוכן שמנסה לתקן בעיות אוטומטית.
- **Local Execution**: סוכן שאמור להריץ פעולות מקומיות.

**סטטוס נוכחי**:
- 🗄️ **Autopilot**: Reference Only (POC בלבד בריפו הישן)
- 🗄️ **Local Execution Agent**: Reference Only (placeholder ריק)

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
| **Telegram Integration** | 🗄️ Legacy (Reference) | מוזכר באודיט, טרם הוחלט |
| **Make.com Workflows** | 🗄️ Legacy (Reference) | מוזכר באודיט, טרם הוחלט |
| **GPT API Direct Calls** | 🔄 Planned | לסוכנים שצריכים GPT ישירות |
| **Multi-Agent Coordination** | 🔄 Planned | ריבוי סוכנים שעובדים ביחד |
| **GitHub Automation (Safe)** | 🔄 Planned | Executor מוגבל ל-OS_SAFE בלבד |

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

3. ✅ **החלטה קריטית**:
   - מתעדים בסעיף "החלטות קריטיות" בראש המסמך
   - מוסיפים **DECISION YYYY-MM-DD** ב-Notes
   - מעדכנים את `docs/DECISIONS_AI_OS.md`

4. ✅ **הסרת יכולת**:
   - לא מוחקים! משנים ל-❌ Not Available
   - מוסיפים הערה למה הוסרה

5. ✅ **גרסאות**:
   - כל שינוי משמעותי = עדכון מספר גרסה
   - Minor: 1.0 → 1.1 (שינוי סטטוס או הוספת יכולת)
   - Major: 1.x → 2.0 (שינוי ארכיטקטורה)

---

**סטטוס מסמך זה**: ✅ Version 1.1 (Critical Decisions Locked)  
**עדכון אחרון**: 20 נובמבר 2025  
**החלטות נעולות**: 3 החלטות קריטיות (MCP, GitHub Executor, GPT Agent Mode)  
**צעד הבא**: ייבוא הסוכן הראשון (GPT GitHub Agent) עם הגבלות DRY RUN
