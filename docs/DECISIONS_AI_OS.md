# AI-OS – החלטות ליבה (Core Decisions)

**מטרת המסמך**: תיעוד החלטות אסטרטגיות וארכיטקטוניות במערכת AI-OS.

**פורמט**: כל החלטה מתועדת עם תאריך, הקשר, החלטה ורציונל.

---

## 2025-11-20 – החלטה #1: MCP Orchestration

### הקשר
מערכת ה-MCP (Master Control Program) בריפו הישן `make-ops-clean` היא מערכת מורכבת לניהול סוכנים, תזמון ואינטגרציות. היא כוללת:
- `mcp/server/` - שרת מרכזי
- `mcp/clients/` - לקוחות (web, iOS shortcuts)
- `mcp/github/` - אינטגרציית GitHub
- `mcp/google/` - אינטגרציית Google

**שאלה**: האם לייבא את MCP כקוד רץ ל-AI-OS?

### ההחלטה
**MCP לא נלקח כקוד רץ ל-AI-OS.**

- **סטטוס**: 🗄️ Legacy / Reference Only
- **שימוש**: משמש כמקור עיצוב וידע בלבד
- **אין**: פריסה, הפעלה, או שימוש אקטיבי בקוד

### רציונל

**למה לא לייבא?**
1. **מורכבות גבוהה**: MCP התפתח אורגנית ויש בו רבדים רבים שלא לגמרי מתועדים.
2. **תלות בתשתית**: הוא נבנה סביב תשתית ספציפית (Cloud Run, Workflows) שלא בהכרח נחוצה ב-AI-OS.
3. **עקרון Data-First**: AI-OS נבנה מאפס עם עקרונות נקיים. עדיף לבנות תשתית פשוטה ומסודרת.

**מה כן לוקחים?**
- **תובנות עיצוב**: איך MCP פתר בעיות של תזמון, אינטגרציות, וניהול סוכנים.
- **דפוסי עבודה**: מה עבד טוב, מה לא.
- **מסמכי תיעוד**: כולם עברו לריפו כחומר עיון.

**מה במקום?**
- בעתיד, אם נזדקק למנגנון orchestration - נבנה אחד פשוט ומודולרי מאפס.
- כרגע: אין צורך במנגנון מרכזי. הסוכנים פועלים בנפרד.

### השפעה על CAPABILITIES_MATRIX
- **MCP-001**: MCP Orchestration → 🗄️ Legacy (Reference Only)
- **MCP-002**: MCP GitHub Integration → 🗄️ Legacy (Reference Only)
- **MCP-003**: MCP Google Integration → 🗄️ Legacy (Reference Only)

---

## 2025-11-20 – החלטה #2: GitHub Executor API

### הקשר
בריפו הישן קיים קוד מלא של `github-executor-api` - שירות Cloud Run שמספק API לאוטומציה של GitHub. הקוד:
- ממוקם ב-`cloud-run/google-workspace-github-api/`
- מכיל 2 endpoints: health check + update file
- מתוכנן ל-deployment ב-Cloud Run
- **בעיה**: Deployment חסום (חסר GitHub PAT, בעיות config)

**שאלה**: האם לפרוס את הקוד הקיים ב-AI-OS?

### ההחלטה
**הקוד הקיים לא נפרס ולא מופעל.**

- **סטטוס**: 📋 Designed (Not Deployed)
- **שימוש**: משמש כ-Blueprint / Design Reference בלבד
- **אין**: פריסה, הפעלה, או ניסיון לתקן את הקוד הקיים

### רציונל

**למה לא לפרוס?**
1. **תוכנן למערכת אחרת**: הקוד נבנה עבור `make-ops-clean` עם דרישות ספציפיות.
2. **בעיות deployment לא פתורות**: חסר PAT, יש באגים (typo ב-Accept header), לא ברור מה הסטטוס.
3. **בטיחות**: אין לנו שכבות פיקוח ואבטחה מספיקות להפעלת Executor אוטומטי.
4. **עקרון Thin Slices**: עדיף לבנות אוטומציה הדרגתית ומבוקרת.

**מה כן לוקחים?**
- **העיצוב**: איך הוא חשב על endpoints, authentication, path validation.
- **הלקחים**: מה הבעיות שהוא ניסה לפתור.
- **ה-Blueprint**: אם בעתיד נחליט לבנות Executor - נשתמש בו כנקודת התחלה.

**מה במקום?**
- כרגע: **אין אוטומציה של כתיבה ל-GitHub**.
- בעתיד: אם נצטרך Executor - נבנה אחד מאפס, עם שכבות בטיחות ברורות.

### השפעה על CAPABILITIES_MATRIX
- **GH-005**: GitHub Executor API → 📋 Designed (Not Deployed) - Reference Only

---

## 2025-11-20 – החלטה #3: GPT GitHub Agent – Execution Mode

### הקשר
הסוכן **GPT GitHub Agent** (`gpt_agent/github_agent.py`) הוא הסוכן המתוחכם ביותר שזוהה בריפו הישן. הוא:
- מנתח Intent של המשתמש
- קורא מסמכי SSOT (CAPABILITIES_MATRIX, DESIGN, SNAPSHOT)
- מסווג פעולות ל-OS_SAFE / CLOUD_OPS_HIGH
- מחזיר תוכנית מפורטת

**כרגע**: הסוכן פועל במצב **DRY RUN** - מתכנן אבל לא מבצע.

**שאלה**: האם לשדרג את הסוכן למצב Executor (מבצע פעולות)?

### ההחלטה
**הסוכן נשאר במצב DRY RUN בלבד.**

- **סטטוס**: 🚧 Operational (Limited) - DRY RUN ONLY
- **תפקיד**: Planner בלבד - מנתח, מתכנן, מציע
- **אין**: פעולות כתיבה אוטומטיות על GitHub

### רציונל

**למה DRY RUN?**
1. **בטיחות מעל הכל**: צריך לבנות אמון הדרגתי במערכת.
2. **Human-in-the-loop חובה**: כל פעולת כתיבה צריכה אישור אנושי מפורש.
3. **בדיקת יכולות**: DRY RUN מאפשר לבדוק את הסוכן בלי סיכון.
4. **עקרון Data-First**: קודם מגדירים חוקים, מדיניות ובקרות - אחר כך מפעילים אוטומציות.

**מה הסוכן כן עושה?**
- קורא את מצב המערכת (CAPABILITIES_MATRIX, SYSTEM_SNAPSHOT)
- מנתח בקשות ומסווג רמת סיכון
- מחזיר תוכנית מפורטת עם צעדים
- מסביר למה כל צעד נחוץ

**מה הסוכן לא עושה?**
- ❌ לא כותב קבצים ב-GitHub
- ❌ לא יוצר commits
- ❌ לא פותח PRs
- ❌ לא מפעיל workflows

**Roadmap עתידי**:
- **שלב 1** (נוכחי): DRY RUN בלבד
- **שלב 2** (אפשרי בעתיד): Executor מוגבל ל-OS_SAFE בלבד (Docs/State)
- **שלב 3** (רחוק): Executor מלא עם אישור אנושי ל-CLOUD_OPS_HIGH

**תנאים לשלב 2**:
1. שכבות אבטחה מוגדרות בבירור
2. מנגנון rollback אוטומטי
3. פיקוח ומוניטורינג מלא
4. בדיקות מקיפות של הסוכן
5. אישור אנושי מפורש מהמשתמש (אור)

### השפעה על CAPABILITIES_MATRIX
- **GH-002**: GitHub Planning (DRY RUN) → 🚧 Operational (Limited) - **DECISION 2025-11-20**: Planner בלבד, אין כתיבה אוטומטית

### השפעה על GPT_GITHUB_AGENT.md
- יתווסף ציון מפורש: **"הסוכן פועל במצב Planner בלבד (DRY RUN)"**
- יתווסף אזהרה: **"אין פעולות כתיבה אוטומטיות - כל פעולה דורשת אישור וביצוע ידני"**

---

## 2025-11-20 – החלטה #4: סיום Phase 1 (Foundation) של AI-OS

### הקשר
במהלך התקופה האחרונה בנינו ריפו חדש בשם `ai-os` שנועד להיות ה-SSOT של מערכת ההפעלה האישית ל-AI (AI-OS).

**נוצרו**:
- **README** חדש ומפורט (420 שורות)
- **מסמכי ליבה** (5 מסמכים):
  - `CONSTITUTION.md` - 9 חוקי יסוד
  - `SYSTEM_SNAPSHOT.md` v2 - צילום מצב מקיף
  - `CAPABILITIES_MATRIX.md` v1.1 - 22 יכולות מתועדות
  - `DECISIONS_AI_OS.md` - לוג החלטות (המסמך הזה)
  - `REPO_AUDIT_make-ops-clean.md` - אודיט מלא של הריפו הישן
- **מיפוי סוכנים** (2 מסמכים):
  - `AGENTS_INVENTORY.md` - 8 סוכנים ממופים
  - `GPT_GITHUB_AGENT.md` - תיעוד מלא של סוכן ליבה #1
- **מיפוי כלים**:
  - `TOOLS_INVENTORY.md` - 24 כלים ואינטגרציות
- **מדיניות אבטחה**:
  - `SECURITY_SECRETS_POLICY.md` - מדיניות מקיפה (720 שורות)
- **שני Workflows רשמיים**:
  - `WF-001` – GITHUB_PLANNING_DRY_RUN (570 שורות)
  - `WF-002` – DECISION_LOGGING_AND_SSOT_UPDATE (737 שורות)

**שאלה**: האם Phase 1 (Foundation) הושלם? האם המערכת מוכנה לשימוש?

### ההחלטה
**Phase 1 – Foundation של AI-OS נחשב הושלם.**

- **סטטוס**: ✅ Phase 1 Complete - System Ready for Controlled Use
- **מכאן והלאה**:
  - `ai-os` הוא **מקור האמת היחיד** (SSOT) לתיעוד, יכולות, סוכנים, כלים ומדיניות
  - המערכת מוכנה לשימוש **מבוקר** בחיים האמיתיים
  - כל שינוי מהותי חדש יעבור דרך אחד מה-Workflows הרשמיים (לפחות WF-001 או WF-002)
- **אין**: שימוש production אוטומטי, סוכנים אוטונומיים עם כתיבה, פעולות לא מפוקחות

### רציונל

**למה Phase 1 הושלם?**

1. **כיסוי תיעודי חזק**:
   - יש חוקה (9 עקרונות)
   - יש צילום מצב מלא
   - יש מפת יכולות (22 יכולות)
   - יש לוג החלטות (4 החלטות כולל זו)

2. **תיעוד ברור של רכיבים**:
   - סוכן ליבה מתועד (GPT GitHub Agent)
   - 24 כלים ממופים
   - 8 סוכנים מסווגים
   - יכולות ברורות לכל רכיב

3. **מדיניות אבטחה**:
   - מדיניות מקיפה לסיקרטים (720 שורות)
   - זיהוי אזורים רגישים (SECRETS/, config/)
   - כללים ברורים לכל סוכן/כלי
   - תהליכי מיגרציה ו-incident response

4. **Workflows מגינים**:
   - WF-001: הגנה על שינויי GitHub (DRY RUN)
   - WF-002: הגנה על החלטות + סנכרון SSOT
   - Human-in-the-loop על כל פעולה קריטית

5. **מיפוי סיכונים**:
   - כל כלי מסווג לפי Risk Level
   - זיהוי Unknown Tools (Make, Telegram, GitHub Actions)
   - תוכנית ברורה לטיפול באבטחה

**מה הושג?**
- ✅ תשתית יציבה
- ✅ תיעוד מקיף
- ✅ מדיניות ברורה
- ✅ בקרות בטיחות
- ✅ Workflows פעילים

**מה עדיין חסר?**
- ⏳ סריקת אבטחה מלאה (config/, secrets)
- ⏳ ברור Unknown Tools
- ⏳ אוטומציה מתקדמת (Semi-Automated)
- ⏳ Monitoring & Health Checks

**למה "מבוקר" ולא "Production"?**
- אין סוכנים אוטונומיים עם כתיבה
- כל פעולה דורשת אישור אנושי
- טרם בוצעה סריקת אבטחה מלאה
- Human-in-the-loop נשאר חובה

### השפעה על SSOT

**מסמכים שעודכנו** ✅:

1. **`docs/SYSTEM_SNAPSHOT.md`**:
   - ✅ סעיף "איפה אנחנו עכשיו":
     - הוסף: "✔ Phase 1 (Foundation) הושלם"
     - עדכן: "⏳ בשלב הבא: Phase 2 - Security & Automation"
   - ✅ סעיף "משימות פתוחות":
     - הזז משימות Phase 1 ל-"הושלם"

2. **`README.md`**:
   - ✅ סעיף Roadmap:
     - Phase 1: ~~In Progress~~ → **✅ COMPLETE**
     - Phase 2: Upcoming → **🔄 NEXT**

3. **`docs/CAPABILITIES_MATRIX.md`**:
   - ✅ הוסף הערה בראש המסמך:
     - "**System Status**: Foundation Complete (DECISION 2025-11-20 #4) - Ready for Controlled Use"

4. **`docs/DECISIONS_AI_OS.md`** (מסמך זה):
   - ✅ הוסף החלטה #4
   - ✅ עדכן סיכום החלטות (4 החלטות)
   - ✅ עדכן "עדכון אחרון"

### Follow-ups

**Phase 2 Options** - לבחור Thin Slice ראשון:

**אפשרות A: Security Phase 1** (מומלץ):
- [ ] הוספת `.gitignore` rules
- [ ] סימון `SECRETS/` כמוגן
- [ ] Warning ב-README על אזורים רגישים
- [ ] סריקת `config/` לחיפוש secrets inline
- [ ] יצירת רשימת מיגרציה

**אפשרות B: Workflows נוספים**:
- [ ] WF-003: Health Checks
- [ ] WF-003: SSOT Auto-Update (חלקי)
- [ ] WF-003: Secret Migration Process

**אפשרות C: ברור Unknown Tools**:
- [ ] בדיקת Make.com - בשימוש?
- [ ] בדיקת Telegram Bot - איזה bot?
- [ ] סריקת GitHub Actions - אילו workflows?
- [ ] סקירת Config Files - secrets inline?

**אפשרות D: תיעוד כלים פעילים**:
- [ ] `tools/GITHUB_MCP.md`
- [ ] `tools/WINDOWS_MCP.md`
- [ ] `tools/FILESYSTEM_MCP.md`
- [ ] `tools/GOOGLE_MCP.md`

**חובה**: כל החלטה דומה בעתיד תעבור דרך **WF-002** ותעודכן ב-DECISIONS_AI_OS + SSOT.

---

## סיכום ההחלטות

| # | נושא | החלטה | סטטוס |
|---|------|-------|-------|
| **1** | MCP Orchestration | לא נלקח כקוד רץ | 🗄️ Legacy (Reference Only) |
| **2** | GitHub Executor API | לא פרוס | 📋 Designed (Not Deployed) |
| **3** | GPT GitHub Agent Mode | DRY RUN בלבד | 🚧 Operational (Limited) |
| **4** | Phase 1 Foundation | הושלם | ✅ Complete - Ready for Use |

---

## עקרונות מנחים

ההחלטות האלה משקפות את **חוקי היסוד של AI-OS**:

1. **Data-First** (חוק #1): קודם מגדירים, אחר כך בונים
2. **Human-in-the-loop** (חוק #4): אין פעולות הרסניות בלי אישור
3. **Thin Slices** (חוק #6): בונים בצורה הדרגתית ומבוקרת
4. **אבטחה מעל הכל** (חוק #7): בטיחות תמיד במקום הראשון

---

**סטטוס מסמך זה**: ✅ Active  
**עדכון אחרון**: 20 נובמבר 2025  
**החלטות נעולות**: 4 החלטות קריטיות  
**הערה**: החלטות אלה ניתנות לשינוי בעתיד, אבל רק אחרי דיון מפורש ותיעוד של הרציונל לשינוי.
