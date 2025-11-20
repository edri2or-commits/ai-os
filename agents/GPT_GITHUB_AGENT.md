# GPT GitHub Agent – סוכן ליבה

**תאריך יצירה**: 20 נובמבר 2025  
**גרסה**: 1.0  
**סטטוס**: Imported from make-ops-clean

---

## תפקיד כללי

**GPT GitHub Agent** הוא סוכן מתכנן (Planner) שמנתח בקשות ממשתמש (Intent) ומתרגם אותן לתוכנית פעולה מפורטת על GitHub.

**במילים פשוטות**: אתה אומר לו "אני רוצה לעדכן את התיעוד בריפו" והוא:
1. קורא את מצב המערכת הנוכחי (Snapshot)
2. בודק מה המיפוי של היכולות שלו (Capabilities Matrix)
3. מחליט אם זה בטוח לעשות ישירות (OS_SAFE) או צריך PR ואישור (CLOUD_OPS_HIGH)
4. מציע לך תוכנית פעולה מפורטת

**חשוב**: כרגע הסוכן עובד במצב **DRY RUN בלבד** - הוא מתכנן אבל לא מבצע. הוא לא משנה קבצים, לא יוצר commits ולא מפעיל workflows.

---

## אחריות (Responsibilities)

### ✅ הסוכן **כן** אחראי על:

1. **ניתוח כוונות (Intent Analysis)**:
   - לקרוא בקשה מהמשתמש ("אני רוצה לעדכן את X")
   - להבין מה צריך לקרות ברמת GitHub (אילו קבצים, אילו פעולות)

2. **קריאת מקורות אמת (SSOT)**:
   - `DOCS/STATE_FOR_GPT_SNAPSHOT.md` - מה מצב המערכת כרגע
   - `CAPABILITIES_MATRIX.md` - מה הכלים והיכולות הזמינים
   - `DOCS/AGENT_GPT_MASTER_DESIGN.md` - חוקי התנהגות של הסוכן

3. **סיווג רמת סיכון**:
   - **OS_SAFE**: פעולות בטוחות (עדכוני תיעוד, קבצי State, מסמכי Design)
   - **CLOUD_OPS_HIGH**: פעולות מסוכנות (קוד, Workflows, Secrets, Permissions)

4. **יצירת תוכנית (Planning)**:
   - מציע צעדים מפורטים: אילו קבצים לשנות, איך לעשות commit, האם צריך PR
   - מסביר למשתמש למה הוא הציע מה שהציע

5. **החזרת תוכנית טקסטואלית בלבד**:
   - פלט הסוכן הוא תוכנית במילים, לא פעולות אמיתיות

### ❌ הסוכן **לא** אחראי על:

1. **ביצוע ישירות** (Execution):
   - אינו כותב קבצים
   - אינו יוצר commits
   - אינו פותח PRs
   - אינו מפעיל workflows

2. **פעולות מעבר ל-GitHub**:
   - לא עובד עם Google Workspace
   - לא עובד עם Cloud Run/GCP
   - לא עובד עם Windows/MCP

3. **קבלת החלטות סופיות**:
   - לא מחליט אם לבצע או לא - זה תמיד תפקיד המשתמש (Human-in-the-loop)

---

## מקורות היסטוריים

### מקור בריפו הישן:
- **קוד הסוכן**: `make-ops-clean/gpt_agent/github_agent.py`
- **תיקייה**: `make-ops-clean/gpt_agent/`

### מסמכים רלוונטיים:
1. **`DOCS/AGENT_GPT_MASTER_DESIGN.md`**:
   - עיצוב מלא של הסוכן
   - ארכיטקטורה: Or → GPT-Agent → Claude → Agents אחרים
   - מחזור חיים: Read Context → Plan → Approval → Execute → Reflect

2. **`DOCS/STATE_FOR_GPT_SNAPSHOT.md`**:
   - צילום מצב של המערכת
   - סטטוס של כל היכולות
   - Backlog ו-TODOs

3. **`CAPABILITIES_MATRIX.md`**:
   - טבלת יכולות מלאה של כל המערכת
   - חלוקה לרמות סיכון (OS_SAFE / CLOUD_OPS_HIGH)
   - סטטוס כל יכולת: Planned / Implemented / Verified / Blocked

4. **`MCP_GPT_CAPABILITIES_BRIDGE.md`**:
   - גשר בין GPT לבין יכולות Claude/MCP
   - הנחיות לאופן עבודה בין מודלים שונים

5. **`GPT_REPO_ACCESS_BRIDGE.md`**:
   - הנחיות גישה לריפו עבור GPT/Agents
   - מבנה תיקיות וכללי גישה

---

## יכולות ליבה (Capabilities)

### 🎯 Planning & Analysis

1. **קריאת הקשר (Context Loading)**:
   - טוען את כל מסמכי ה-SSOT לפני תכנון
   - מזהה את המצב הנוכחי של המערכת

2. **ניתוח Intent**:
   - מבין את הבקשה של המשתמש
   - מזהה אילו קבצים יושפעו
   - מסווג את רמת הסיכון

3. **סיווג רמת סיכון**:
   - **OS_SAFE**: 
     - עדכוני Docs (תיעוד)
     - עדכוני State (מצב המערכת)
     - עדכוני Design (עיצוב)
     - ✅ מומלץ: commit ישיר ל-main
   
   - **CLOUD_OPS_HIGH**:
     - שינויי קוד (`.py`, `.sh`, `.ps1`)
     - שינויי Workflows (`.github/workflows/*.yml`)
     - שינויי Secrets/Tokens/Permissions
     - ⚠️ מומלץ: PR + אישור אנושי

4. **יצירת תוכנית**:
   - רשימת צעדים מפורטת
   - הסבר למה כל צעד נדרש
   - המלצה על דרך הביצוע (ישיר / PR)

### 🔒 Safety Features

1. **DRY RUN Mode**:
   - כרגע הסוכן **רק מתכנן**
   - לא מבצע שום פעולה אמיתית
   - בטוח לחלוטין להרצה

2. **Human-in-the-loop**:
   - כל תוכנית דורשת אישור אנושי
   - המשתמש מקבל את התוכנית וצריך להחליט אם לבצע

3. **Clear Classification**:
   - סיווג ברור של כל פעולה לפי רמת סיכון
   - הסבר מפורט למה משהו מסווג כ-OS_SAFE או CLOUD_OPS_HIGH

### 📋 Output Format

הסוכן מחזיר תוכנית טקסטואלית עם המבנה הבא:

```
# GPT GitHub Agent — DRY RUN PLAN

## 1. Intent
[מה המשתמש ביקש]

## 2. Context Files Loaded
[רשימת מסמכי SSOT שנקראו]

## 3. Notes
- This is a DRY RUN only
- No files are modified

## 4. High-level Next Steps (Conceptual)
1. Classify as OS_SAFE / CLOUD_OPS_HIGH
2. Identify affected files
3. For OS_SAFE: propose direct updates
4. For CLOUD_OPS_HIGH: propose PR

## 5. Implementation TODOs
[מה צריך לעשות בעתיד]
```

---

## אינטגרציות וכלים

### כלים עכשוויים (v1.0)

1. **Python Script**:
   - קובץ: `gpt_agent/github_agent.py`
   - הרצה: `python github_agent.py --intent "your request"`
   - פלט: תוכנית טקסטואלית ל-stdout

2. **מסמכי SSOT** (Single Source of Truth):
   - טוען 3 מסמכים בכל הפעלה:
     - `DOCS/AGENT_GPT_MASTER_DESIGN.md`
     - `DOCS/STATE_FOR_GPT_SNAPSHOT.md`
     - `CAPABILITIES_MATRIX.md`

### אינטגרציות עתידיות (Roadmap)

1. **שלב A - Design + Docs בלבד**:
   - הסוכן יבצע (לא רק יתכנן) עדכונים ל-Docs/State
   - עדיין לא יגע בקוד Production

2. **שלב B - GitHub Actions**:
   - יפתח PRs אוטומטיים
   - ידרוש אישור משתמש
   - יבצע merge אחרי אישור

3. **שלב C - אינטגרציה מלאה**:
   - חיבור ל-Google Workspace
   - חיבור ל-GCP (Cloud Run, Pub/Sub)
   - חיבור ל-MCP Windows/Cloud Shell

### השתלבות עתידית ב-AI-OS

**מומלץ**:
1. הסוכן יישאר **סוכן ליבה** במערכת
2. ימוקם ב-`agents/gpt-github-agent/`
3. יהיה אחראי על **כל תכנון פעולות GitHub**
4. סוכנים אחרים יפנו אליו לקבלת תוכניות

**אפשרות חלופית**:
1. לשדרג אותו ל-**Executor** (לא רק Planner)
2. לאפשר לו לבצע פעולות OS_SAFE באופן אוטומטי
3. לשמור על Human-in-the-loop רק ל-CLOUD_OPS_HIGH

---

## סטטוס נוכחי

### לפי האודיט: **זהב 🏆**

הסוכן מסומן בריפו הישן כ-**"זהב"** - משמע: איכותי, מתוחכם, ומוכן לשימוש.

### הערכה והמלצות:

**✅ חוזקות**:
1. **תיעוד מצוין**: יש מסמך עיצוב מלא (AGENT_GPT_MASTER_DESIGN)
2. **ארכיטקטורה ברורה**: מבנה Planner → Approval → Executor מוגדר היטב
3. **בטיחות**: DRY RUN mode מונע טעויות
4. **סיווג חכם**: חלוקה ל-OS_SAFE / CLOUD_OPS_HIGH מתחשבת בסיכונים

**⚠️ מגבלות נוכחיות**:
1. **DRY RUN בלבד**: לא מבצע, רק מתכנן
2. **תלות במסמכים חיצוניים**: דורש 3 מסמכי SSOT בנתיב מסוים
3. **ללא LLM אמיתי**: הקוד הנוכחי הוא תבנית סטטית, לא משתמש ב-GPT/Claude API

**🔧 דברים לשיפור**:
1. **שדרוג ל-Executor**:
   - להוסיף יכולת ביצוע אמיתית (לא רק תכנון)
   - לשמור על Human-in-the-loop ל-CLOUD_OPS_HIGH

2. **חיבור ל-LLM**:
   - להחליף את התבנית הסטטית בקריאה אמיתית ל-GPT/Claude API
   - לאפשר ניתוח חכם יותר של Intent

3. **הכללה**:
   - כרגע הסוכן ספציפי ל-GitHub
   - אפשר להכלילו לעבוד גם עם Google Workspace, GCP וכו'

4. **תיקון תלויות**:
   - להפוך את נתיבי המסמכים לגמישים (לא קשיחים)
   - לאפשר הגדרת SSOT דרך config

### המלצה סופית: **סוכן ליבה ב-AI-OS ✅**

הסוכן הזה **חייב** להיות חלק ממערכת AI-OS כי:
1. הוא הסוכן המתוחכם ביותר שזוהה בריפו הישן
2. יש לו תיעוד מצוין ועיצוב מוקפד
3. הוא מגדיר דפוס עבודה נכון: Plan → Approve → Execute → Reflect
4. ניתן לבנות סביבו מערכת שלמה של סוכנים

---

## נקודות להחלטה אנושית

### 1️⃣ האם לשדרג ל-Executor?

**שאלה**: האם הסוכן צריך רק לתכנן (DRY RUN) או גם לבצע?

**אפשרויות**:
- **A**: להשאיר DRY RUN - בטוח לחלוטין, אבל דורש ביצוע ידני
- **B**: לשדרג ל-Executor עבור OS_SAFE בלבד - יכול לעדכן תיעוד אוטומטית
- **C**: לשדרג ל-Executor מלא - יכול לעשות הכל, אבל רק אחרי אישור למשימות CLOUD_OPS_HIGH

**המלצה שלי**: **אפשרות B** - לאפשר ביצוע אוטומטי רק ל-OS_SAFE, לשמור Human-in-the-loop ל-CLOUD_OPS_HIGH.

---

### 2️⃣ האם לחבר ל-LLM אמיתי?

**שאלה**: הקוד הנוכחי הוא תבנית סטטית. האם לחבר אותו ל-GPT/Claude API?

**אפשרויות**:
- **A**: להשאיר סטטי - פשוט, צפוי, בטוח
- **B**: לחבר ל-GPT API - חכם יותר, גמיש יותר
- **C**: לחבר ל-Claude API דרך MCP - מנצל תשתית קיימת

**המלצה שלי**: **אפשרות C** - לחבר ל-Claude דרך MCP, כי זה משתלב עם שאר המערכת.

---

### 3️⃣ איפה למקם את הסוכן ב-AI-OS?

**שאלה**: איזה מבנה תיקיות מתאים לסוכן הזה?

**אפשרויות**:
- **A**: `agents/gpt-github-agent/` - תיקייה ייעודית עם כל הקבצים
- **B**: `agents/github-planner.py` - קובץ יחיד פשוט
- **C**: `workflows/github-agent/` - כחלק מתהליכי עבודה

**המלצה שלי**: **אפשרות A** - תיקייה ייעודית, כי יש הרבה מסמכים תומכים.

---

### 4️⃣ האם לייבא את כל מסמכי התיעוד?

**שאלה**: בריפו הישן יש 5+ מסמכים קשורים לסוכן. האם לייבא הכל?

**מסמכים**:
1. `AGENT_GPT_MASTER_DESIGN.md` ✅ חובה
2. `STATE_FOR_GPT_SNAPSHOT.md` ⚠️ ספציפי לריפו הישן
3. `CAPABILITIES_MATRIX.md` ✅ חשוב
4. `MCP_GPT_CAPABILITIES_BRIDGE.md` ✅ חשוב
5. `GPT_REPO_ACCESS_BRIDGE.md` ⚠️ ספציפי לריפו הישן

**המלצה שלי**: לייבא רק את **AGENT_GPT_MASTER_DESIGN.md** במלואו. את השאר - להתאים ל-AI-OS (יצירת גרסאות חדשות).

---

### 5️⃣ האם לשמור תאימות עם הריפו הישן?

**שאלה**: האם הסוכן החדש צריך לעבוד גם עם `make-ops-clean`?

**אפשרויות**:
- **A**: כן - תאימות לאחור מלאה
- **B**: לא - התמקדות רק ב-AI-OS
- **C**: מצב "legacy" - יכול לעבוד עם שניהם דרך config

**המלצה שלי**: **אפשרות C** - להוסיף פרמטר `--repo` שמאפשר לעבוד עם שני הריפואים.

---

### 6️⃣ מה לעשות עם GPT Tasks Executor?

**שאלה**: בריפו הישן יש גם "GPT Tasks Executor" (Workflow ב-GitHub Actions) שכרגע שבור. האם לתקן אותו?

**סטטוס**: Partial/Broken - הוא מוגדר אבל לא עובד בפועל.

**אפשרויות**:
- **A**: להתעלם - לא צריך אותו בשלב זה
- **B**: לתקן - לגלות למה הוא שבור ולתקן
- **C**: להחליף - ליצור מנגנון execution חדש

**המלצה שלי**: **אפשרות A** (בינתיים) - להתמקד קודם בסוכן הבסיסי, לתקן את ה-Executor רק אם נצטרך אותו.

---

### 7️⃣ איך לנהל את מסמכי ה-SSOT?

**שאלה**: הסוכן תלוי ב-3 מסמכי SSOT. איפה הם צריכים לחיות ב-AI-OS?

**מסמכים**:
1. `AGENT_GPT_MASTER_DESIGN.md` → `docs/agents/GPT_GITHUB_AGENT_DESIGN.md`?
2. `STATE_FOR_GPT_SNAPSHOT.md` → `docs/SYSTEM_SNAPSHOT.md`? (כבר יש!)
3. `CAPABILITIES_MATRIX.md` → `docs/CAPABILITIES_MATRIX.md`?

**המלצה שלי**: 
- להשתמש ב-`docs/SYSTEM_SNAPSHOT.md` הקיים
- ליצור `docs/CAPABILITIES_MATRIX.md` חדש (גרסת AI-OS)
- ליצור `agents/gpt-github-agent/DESIGN.md` בתוך תיקיית הסוכן

---

**סטטוס מסמך זה**: ✅ הושלם  
**צעד הבא**: קבלת החלטות על 7 הנקודות למעלה לפני ייבוא הסוכן
