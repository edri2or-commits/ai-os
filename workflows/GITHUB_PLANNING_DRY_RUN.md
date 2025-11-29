# Workflow: GitHub Planning (DRY RUN)

**Workflow ID**: WF-001  
**גרסה**: 1.0  
**תאריך יצירה**: 20 נובמבר 2025  
**סטטוס**: ✅ Active

---

## מטרה

לתכנן בבטחה שינויים בריפואים בגיטהאב, בעזרת **GPT GitHub Agent**, בלי לבצע שום פעולה אוטומטית (**DRY RUN בלבד**).

**במילים פשוטות**:
> "אני רוצה לשנות משהו בריפו, אבל קודם אני רוצה תוכנית מסודרת - מה לשנות, איך לשנות, ולמה. אחרי שאני מאשר את התוכנית - אני מבצע את השינויים ידנית."

---

## שחקנים (Actors)

| שחקן | תפקיד | יכולות | מגבלות |
|------|-------|---------|--------|
| **אור (Human)** | מנסח בקשות, מאשר תוכניות, מבצע פעולות | החלטה סופית על כל שינוי | - |
| **GPT GitHub Agent** | Planner – מנתח, מתכנן, מציע | קריאת מסמכים, ניתוח, תכנון | ❌ אין כתיבה, commits, PRs |
| **Claude Desktop** | מבצע ידני / מסייע | GitHub MCP, Filesystem, Commands | פועל תחת פיקוח אנושי |

---

## Preconditions (תנאים מקדימים)

לפני הפעלת ה-workflow, וודא:

1. ✅ **הריפו `ai-os` קיים ומעודכן**:
   - יש תיקיות: `docs/`, `agents/`, `tools/`, `workflows/`, `policies/`, `archive/`
   - יש קבצים: `README.md`, `CONSTITUTION.md`, `CAPABILITIES_MATRIX.md`, `DECISIONS_AI_OS.md`

2. ✅ **GPT GitHub Agent מוגדר כ-Planner בלבד**:
   - סטטוס ב-`CAPABILITIES_MATRIX.md`: 🚧 Operational (Limited) - DRY RUN ONLY
   - אין לו הרשאות כתיבה
   - אין לו יכולת ליצור commits/PRs אוטומטית

3. ✅ **גישה לגיטהאב דרך Claude Desktop (MCP)**:
   - Claude Desktop מחובר ל-GitHub דרך MCP
   - יש אפשרות לקרוא קבצים, ליצור קבצים, ולעשות commits ידניים

4. ✅ **מסמכי SSOT זמינים וקריאים**:
   - `docs/CONSTITUTION.md` (חוקי היסוד)
   - `docs/CAPABILITIES_MATRIX.md` (מפת יכולות)
   - `docs/SYSTEM_SNAPSHOT.md` (צילום מצב)
   - `docs/DECISIONS_AI_OS.md` (החלטות נעולות)

---

## שלבי העבודה (Workflow Steps)

### **שלב 1: ניסוח הבקשה (Intent Formulation)**

**מבצע**: אור (Human)

**פעולות**:
1. אור מנסח בקשה ברורה:
   - **דוגמה 1**: "אני רוצה לסדר את תיקיית `docs/` בריפו `ai-os` לפי חוקי ה-AI-OS."
   - **דוגמה 2**: "אני רוצה ליצור קובץ חדש `tools/GITHUB_TOOLS.md` עם רשימת כלי GitHub."
   - **דוגמה 3**: "אני רוצה לעדכן את `CAPABILITIES_MATRIX.md` להוסיף יכולת חדשה."

2. אור מציין את הקשר הרלוונטי (אם יש):
   - איזה ריפו?
   - איזה תיקייה/קובץ?
   - למה זה חשוב?

**פלט**:
- בקשה ברורה ומנוסחת היטב

---

### **שלב 2: ניתוח וקריאת מסמכים (Context Loading)**

**מבצע**: GPT GitHub Agent

**פעולות**:
1. הסוכן קורא את **מסמכי SSOT הרלוונטיים**:
   - `docs/CONSTITUTION.md` – חוקי היסוד
   - `docs/CAPABILITIES_MATRIX.md` – מה המערכת יודעת לעשות
   - `docs/SYSTEM_SNAPSHOT.md` – מה המצב הנוכחי
   - `docs/DECISIONS_AI_OS.md` – החלטות נעולות
   - אודיט הריפו הישן (אם רלוונטי)

2. הסוכן קורא את **מצב הריפו הנוכחי** (READ-ONLY):
   - מבנה תיקיות
   - קבצים קיימים
   - תוכן רלוונטי

3. הסוכן מזהה:
   - מה קיים (What is)
   - מה חסר (What's missing)
   - מה צריך לשנות (What should change)

**פלט**:
- הבנה מלאה של הקשר
- זיהוי פערים וצרכים

---

### **שלב 3: סיווג רמת סיכון (Risk Classification)**

**מבצע**: GPT GitHub Agent

**פעולות**:
הסוכן מסווג את הפעולה המבוקשת לפי רמת סיכון:

#### **OS_SAFE (בטוח)**:
- עדכוני תיעוד (`docs/*.md`)
- עדכוני מצב (`SYSTEM_SNAPSHOT.md`)
- עדכוני עיצוב (`DESIGN*.md`)
- הוספת קבצי ידע חדשים
- **אין שינוי קוד, workflows, או secrets**

#### **CLOUD_OPS_HIGH (מסוכן)**:
- שינוי קוד (`.py`, `.sh`, `.ps1`)
- שינוי workflows (`.github/workflows/*.yml`)
- שינוי secrets, tokens, permissions
- מחיקת קבצים
- שינוי מבנה תיקיות מהותי

**פלט**:
- סיווג ברור: OS_SAFE או CLOUD_OPS_HIGH
- הסבר למה הפעולה מסווגת כך

---

### **שלב 4: יצירת תוכנית מפורטת (Planning)**

**מבצע**: GPT GitHub Agent

**פעולות**:
הסוכן יוצר **תוכנית מפורטת** הכוללת:

1. **מצב נוכחי (Current State)**:
   - מה קיים עכשיו?
   - מה המבנה הנוכחי?
   - מה הבעיות/פערים?

2. **מצב מטרה (Target State)**:
   - איך זה צריך להיראות?
   - מה השינוי הרצוי?

3. **צעדים מפורטים (Detailed Steps)**:
   - **צעד 1**: מה לעשות (קריאה/כתיבה/מחיקה)
   - **צעד 2**: באיזה קובץ/תיקייה
   - **צעד 3**: איזה תוכן להוסיף/לשנות
   - וכו'...

4. **הצעת Commits**:
   - commit message מומלץ
   - אילו קבצים לכלול ב-commit
   - האם צריך יותר מ-commit אחד?

5. **הצעת PRs** (אם CLOUD_OPS_HIGH):
   - האם ליצור branch נפרד?
   - איזה שם ל-branch?
   - מה כותרת ה-PR?

6. **שינויים נדרשים במסמכי SSOT** (אם רלוונטי):
   - האם צריך לעדכן `CAPABILITIES_MATRIX.md`?
   - האם צריך לעדכן `SYSTEM_SNAPSHOT.md`?
   - האם צריך להוסיף החלטה ל-`DECISIONS_AI_OS.md`?

**פורמט הפלט**:
```markdown
# GPT GitHub Agent — DRY RUN PLAN

## 1. Intent
[הבקשה המקורית של אור]

## 2. Context Files Loaded
- CONSTITUTION.md
- CAPABILITIES_MATRIX.md
- SYSTEM_SNAPSHOT.md
- [רשימת קבצים נוספים שנקראו]

## 3. Risk Classification
- **Classification**: OS_SAFE / CLOUD_OPS_HIGH
- **Reason**: [הסבר למה]

## 4. Current State
[תיאור מה קיים עכשיו]

## 5. Target State
[תיאור מה צריך להיות]

## 6. Detailed Action Plan

### Step 1: [שם הצעד]
- **Action**: Create / Update / Delete
- **File**: `path/to/file.md`
- **Content**: [מה לכתוב/לשנות]
- **Reason**: [למה צריך את זה]

### Step 2: ...
[וכו']

## 7. Proposed Commits
- **Commit 1**: "Add initial workflow documentation"
  - Files: `workflows/GITHUB_PLANNING_DRY_RUN.md`
- **Commit 2**: ...

## 8. Required SSOT Updates
- [ ] Update `CAPABILITIES_MATRIX.md` (if new capability added)
- [ ] Update `SYSTEM_SNAPSHOT.md` (if system state changed)
- [ ] Add decision to `DECISIONS_AI_OS.md` (if critical decision made)

## 9. Safety Notes
- [אזהרות/הערות בטיחות]
- [דברים לשים לב אליהם]
```

**פלט**:
- תוכנית DRY RUN מפורטת
- אין ביצוע ממשי!

---

### **שלב 5: סקירה ואישור (Review & Approval)**

**מבצע**: אור (Human) + Claude Desktop (מסייע)

**פעולות**:
1. אור קורא את התוכנית שה-GPT Agent החזיר
2. אור שואל שאלות הבהרה (אם צריך):
   - "למה צריך לשנות את הקובץ הזה?"
   - "האם אפשר לעשות את זה בצורה פשוטה יותר?"
   - "מה קורה אם לא נעשה צעד X?"

3. אור מחליט:
   - ✅ **אישור מלא**: "תבצע הכל כמו שמוצע"
   - ⚠️ **אישור חלקי**: "תבצע רק צעדים 1-3, את 4-5 נדלג"
   - ❌ **דחייה**: "לא מתאים, צריך חשיבה אחרת"

4. אם אושר - אור מתכונן לביצוע ידני

**פלט**:
- החלטה ברורה: לבצע / לא לבצע / לשנות

---

### **שלב 6: ביצוע ידני (Manual Execution)**

**מבצע**: אור + Claude Desktop

**פעולות**:

#### **אם OS_SAFE** (בטוח):
1. אור מבקש מ-Claude Desktop לבצע את הצעדים:
   - "צור קובץ `workflows/GITHUB_PLANNING_DRY_RUN.md` עם התוכן הבא..."
   - "עדכן את `CAPABILITIES_MATRIX.md` להוסיף שורה..."

2. Claude Desktop מבצע את הפעולות **תחת פיקוח אנושי**:
   - קורא קבצים
   - כותב קבצים
   - עושה commits
   - דוחף ל-GitHub

3. אור בודק תוצאות לאחר כל צעד

#### **אם CLOUD_OPS_HIGH** (מסוכן):
1. אור יוצר branch חדש ידנית או מבקש מ-Claude:
   - `git checkout -b feature/new-capability`

2. אור מבצע שינויים בקוד בזהירות:
   - צעד אחד בכל פעם
   - בדיקה אחרי כל שינוי

3. אור יוצר PR:
   - כותב תיאור מפורט
   - מוסיף checklist
   - מבקש review (אם יש צוות)

4. אור מבצע merge **רק אחרי בדיקה מלאה**

**פלט**:
- שינויים בפועל ב-GitHub
- Commits חדשים
- PRs (אם רלוונטי)

---

### **שלב 7: תיעוד ועדכון SSOT (Documentation Update)**

**מבצע**: אור + Claude Desktop

**פעולות**:

אם בוצעו שינויים משמעותיים, יש לעדכן:

1. **`SYSTEM_SNAPSHOT.md`** - אם השתנה מצב המערכת:
   - תיקיות חדשות
   - קבצים חשובים חדשים
   - שינוי בתהליך העבודה

2. **`CAPABILITIES_MATRIX.md`** - אם נוספה/שונתה יכולת:
   - הוספת שורה חדשה לטבלה
   - עדכון סטטוס יכולת קיימת
   - עדכון מספר גרסה (1.0 → 1.1)

3. **`DECISIONS_AI_OS.md`** - אם ננעלה החלטה קריטית:
   - תיעוד ההחלטה עם תאריך
   - הקשר, החלטה, רציונל
   - השפעה על מסמכים אחרים

4. **Commit לעדכונים אלה**:
   - commit message: "Update SSOT: document changes from workflow WF-001"

**פלט**:
- מסמכי SSOT מעודכנים
- המערכת משקפת את המצב האמיתי

---

## Safety & Boundaries (בטיחות וגבולות)

### 🔒 **גבולות GPT GitHub Agent**:

**מה הסוכן לא עושה - EVER**:
- ❌ לא כותב קבצים ב-GitHub
- ❌ לא יוצר commits
- ❌ לא פותח PRs
- ❌ לא מוחק קבצים
- ❌ לא משנה branches
- ❌ לא מפעיל workflows

**מה הסוכן כן עושה**:
- ✅ קורא מסמכים
- ✅ מנתח מצב
- ✅ מתכנן צעדים
- ✅ מציע תוכנית
- ✅ מסביר רציונל

---

### 🛡️ **כללי בטיחות לאור**:

1. **אישור מפורש נדרש לכל פעולה הרסנית**:
   - מחיקת קבצים
   - שינוי גדול במבנה תיקיות
   - שינוי קוד production
   - שינוי workflows

2. **עקרון Thin Slices**:
   - לבצע צעד אחד בכל פעם
   - לבדוק תוצאות
   - רק אז להמשיך

3. **גיבוי לפני שינויים גדולים**:
   - לעשות branch חדש
   - לשמור commit ישן כנקודת שחזור

4. **תיעוד חובה**:
   - כל שינוי משמעותי מתועד
   - עדכון מסמכי SSOT
   - commit messages ברורים

---

## דוגמאות שימוש (Examples)

### **דוגמה 1: יצירת workflow חדש** (OS_SAFE)

**בקשה**:
> "צור workflow חדש לתכנון שינויים ב-GitHub בצורה בטוחה."

**תוכנית (מ-GPT Agent)**:
1. צור קובץ `workflows/GITHUB_PLANNING_DRY_RUN.md`
2. כלול: מטרה, שחקנים, שלבים, בטיחות
3. עדכן `SYSTEM_SNAPSHOT.md` עם הוספת workflow ראשון

**ביצוע (אור + Claude)**:
- Claude יוצר את הקובץ
- אור בודק
- Claude עושה commit: "Add first workflow: GitHub Planning DRY RUN"
- Claude דוחף ל-GitHub

**תיעוד**:
- עדכון `SYSTEM_SNAPSHOT.md`: "נוסף workflow ראשון"

---

### **דוגמה 2: הוספת כלי חדש** (OS_SAFE)

**בקשה**:
> "תיעד את כלי GitHub שאנחנו משתמשים בהם."

**תוכנית (מ-GPT Agent)**:
1. צור קובץ `tools/GITHUB_TOOLS.md`
2. רשום: GitHub MCP, GitHub CLI, GitHub Actions
3. לכל כלי: מה הוא עושה, איך משתמשים, מגבלות
4. עדכן `CAPABILITIES_MATRIX.md` להוסיף Tool Documentation capability

**ביצוע (אור + Claude)**:
- Claude יוצר את הקובץ
- אור מוסיף פרטים
- Claude עושה 2 commits:
  1. "Add GitHub tools documentation"
  2. "Update CAPABILITIES_MATRIX: add Tool Documentation capability"

---

### **דוגמה 3: שינוי קוד** (CLOUD_OPS_HIGH)

**בקשה**:
> "שדרג את GPT GitHub Agent לתמוך ב-multiline planning."

**תוכנית (מ-GPT Agent)**:
1. **Risk**: CLOUD_OPS_HIGH (שינוי קוד)
2. צור branch: `feature/multiline-planning`
3. ערוך `agents/gpt-github-agent/agent.py`
4. הוסף tests ב-`agents/gpt-github-agent/tests/`
5. עדכן `agents/GPT_GITHUB_AGENT.md` עם הפיצ'ר החדש
6. צור PR עם תיאור מפורט

**ביצוע (אור + Claude)**:
- אור יוצר branch
- Claude עוזר לכתוב קוד
- אור בודק בזהירות
- אור יוצר PR
- אור עושה merge רק אחרי review

---

## Postconditions (תנאים לאחר הביצוע)

לאחר הפעלה מוצלחת של ה-workflow:

1. ✅ **השינויים המבוקשים בוצעו ב-GitHub**
2. ✅ **Commits נוצרו עם messages ברורים**
3. ✅ **PRs נוצרו (אם רלוונטי) ונבדקו**
4. ✅ **מסמכי SSOT עודכנו (אם נדרש)**:
   - `SYSTEM_SNAPSHOT.md`
   - `CAPABILITIES_MATRIX.md`
   - `DECISIONS_AI_OS.md`
5. ✅ **אור מרוצה מהתוצאה**
6. ✅ **אין שברים, אין אובדן מידע**

---

## Failure Modes & Recovery (מצבי כשל והתאוששות)

### **כשל אפשרי #1: GPT Agent החזיר תוכנית לא ברורה**

**תסמינים**:
- הצעדים לא מפורטים
- לא ברור מה לעשות
- חסר הסבר למה

**פתרון**:
1. אור מבקש הבהרה: "תסביר את צעד 3 בפירוט"
2. GPT Agent מחזיר תוכנית מעודכנת
3. אם עדיין לא ברור - אור לא מבצע

---

### **כשל אפשרי #2: Claude Desktop נתקע באמצע ביצוע**

**תסמינים**:
- commit לא הושלם
- קובץ נוצר חלקית
- שגיאת GitHub API

**פתרון**:
1. אור בודק מה בוצע עד כה: `git status`
2. אור מבטל שינויים שלא הושלמו: `git reset --hard`
3. אור מתחיל מחדש מהצעד האחרון שהצליח

---

### **כשל אפשרי #3: שינוי גרם לבעיה לא צפויה**

**תסמינים**:
- קובץ נראה לא נכון
- מבנה שבור
- איבדנו מידע

**פתרון**:
1. **אל תפאניקה**
2. בדוק את ה-commit האחרון: `git log`
3. חזור לגרסה הקודמת: `git revert <commit>`
4. או: חזור לגרסה טובה ידועה: `git reset --hard <commit>`
5. דחוף את ה-revert/reset ל-GitHub

---

## Metrics & Success Criteria (מדדים וקריטריונים להצלחה)

### **קריטריונים להצלחת Workflow**:

1. ✅ **GPT Agent החזיר תוכנית תוך < 2 דקות**
2. ✅ **התוכנית הייתה ברורה ומפורטת**
3. ✅ **אור הבין את כל הצעדים**
4. ✅ **הביצוע הצליח ללא שגיאות**
5. ✅ **אין regressions (שברים של פיצ'רים קיימים)**
6. ✅ **מסמכי SSOT מעודכנים ומדויקים**

### **מדדים לטווח ארוך**:

- **זמן ממוצע להשלמת workflow**: < 30 דקות
- **אחוז הצלחה**: > 90%
- **מספר rollbacks**: < 5%
- **שביעות רצון אור**: 8/10 ומעלה

---

## Roadmap לשדרוג עתידי

### **שלב 1 (נוכחי)**: DRY RUN בלבד
- ✅ GPT Agent מתכנן
- ✅ אור + Claude מבצעים ידנית
- ✅ Human-in-the-loop מלא

---

### **שלב 2 (עתיד קרוב)**: Semi-Automated (OS_SAFE בלבד)
- 🔄 GPT Agent יכול **להציע טיוטת PR**
- 🔄 הטיוטה נוצרת **אבל לא נפתחת** אוטומטית
- 🔄 אור בודק את הטיוטה ומאשר פתיחת PR

**תנאים**:
1. שכבות אבטחה מוגדרות
2. מנגנון rollback אוטומטי
3. 100+ הפעלות מוצלחות של שלב 1

---

### **שלב 3 (עתיד רחוק)**: Executor מוגבל
- 🔮 GPT Agent יכול **ליצור PR אוטומטית**
- 🔮 רק ל-OS_SAFE (Docs/State בלבד)
- 🔮 אור עדיין צריך **לאשר merge**

**תנאים**:
1. פיקוח ומוניטורינג מלא
2. בדיקות אוטומטיות (tests/linting)
3. אישור אנושי מפורש מאור

---

### **שלב 4 (עתיד מאוד רחוק)**: Executor מלא
- 🔮 GPT Agent יכול **לבצע גם CLOUD_OPS_HIGH**
- 🔮 רק אחרי אישור אנושי **מפורש לכל פעולה**
- 🔮 עם rollback אוטומטי במקרה של בעיה

**תנאים**:
1. כל התנאים של שלבים 1-3
2. מערכת AI validation מתקדמת
3. ביטחון מלא במערכת

---

## קישורים למסמכים רלוונטיים

- [`docs/CONSTITUTION.md`](../docs/CONSTITUTION.md) - חוקי היסוד
- [`docs/CAPABILITIES_MATRIX.md`](../docs/CAPABILITIES_MATRIX.md) - מפת יכולות
- [`docs/DECISIONS_AI_OS.md`](../docs/DECISIONS_AI_OS.md) - החלטות קריטיות
- [`agents/GPT_GITHUB_AGENT.md`](../agents/GPT_GITHUB_AGENT.md) - תיעוד הסוכן

---

**סטטוס Workflow זה**: ✅ Active & Ready  
**נוצר**: 20 נובמבר 2025  
**גרסה**: 1.0  
**שימוש הבא**: כל תכנון שינוי ב-GitHub
