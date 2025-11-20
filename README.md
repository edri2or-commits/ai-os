# AI-OS – מערכת ההפעלה האישית שלי ל-AI

`ai-os` הוא ריפו ה־**Single Source of Truth (SSOT)** שלי למערכת הפעלה אישית מרובת־סוכנים (Multi-Agent OS).  
זו שכבת הבקרה שמחברת בין סוכני AI, כלים, אינטגרציות ו־workflows – בצורה **בטוחה, שקופה ומבוקרת**.

**המטרה**: לאסוף את כל היכולות, הסוכנים והחוקים שלי למקום אחד יציב, שאפשר לפתח ממנו מערכת חיה לאורך זמן.

---

## 🎯 מה זה AI-OS?

AI-OS היא מערכת שמאפשרת לי:
- ✅ **לתכנן שינויים בצורה מבוקרת** (בלי לשבור דברים)
- ✅ **לנהל מספר סוכני AI** עם תפקידים ברורים
- ✅ **לשמור על תיעוד מדויק** של כל מה שקורה
- ✅ **לעבוד עם GitHub, Google, Windows** בצורה אחידה
- ✅ **להבטיח בטיחות** - כל פעולה מסוכנת דורשת אישור אנושי

---

## 📂 מבנה הריפו

```
ai-os/
├── docs/              📚 מסמכי ליבה (SSOT)
│   ├── CONSTITUTION.md              ← 9 חוקי יסוד
│   ├── SYSTEM_SNAPSHOT.md           ← מצב המערכת כרגע
│   ├── CAPABILITIES_MATRIX.md       ← מפת היכולות (22 יכולות)
│   ├── DECISIONS_AI_OS.md           ← 3 החלטות קריטיות נעולות
│   └── REPO_AUDIT_make-ops-clean.md ← אודיט הריפו הישן
│
├── agents/            🤖 סוכני AI
│   ├── AGENTS_INVENTORY.md          ← רשימת כל הסוכנים
│   └── GPT_GITHUB_AGENT.md          ← סוכן ליבה #1 (DRY RUN)
│
├── workflows/         ⚙️ תהליכי עבודה
│   └── GITHUB_PLANNING_DRY_RUN.md   ← WF-001: תכנון בטוח
│
├── tools/             🛠️ תיעוד כלים (בפיתוח)
├── policies/          📋 מדיניות והרשאות (בתכנון)
├── archive/           📦 חומר היסטורי (עתידי)
└── README.md          ← המדריך שאתה קורא עכשיו
```

---

## 🚀 מה יש במערכת כרגע (V1.0)

### ✅ **מסמכי SSOT** (5 מסמכים)
| מסמך | מה יש בתוכו | סטטוס |
|------|-------------|-------|
| **CONSTITUTION.md** | 9 חוקי יסוד של המערכת | ✅ Active |
| **SYSTEM_SNAPSHOT.md** | צילום מצב: ריפואים, כלים, מה עובד | ✅ Active |
| **CAPABILITIES_MATRIX.md** | 22 יכולות מתועדות (GitHub, Windows, Google...) | ✅ v1.1 |
| **DECISIONS_AI_OS.md** | 3 החלטות קריטיות נעולות | ✅ Active |
| **REPO_AUDIT** | אודיט מלא של `make-ops-clean` | ✅ Reference |

### ✅ **סוכני AI** (1 סוכן פעיל)
| סוכן | תפקיד | מצב ביצוע |
|------|-------|-----------|
| **GPT GitHub Agent** | Planner לשינויים ב-GitHub | 🚧 DRY RUN בלבד |

### ✅ **Workflows** (1 workflow פעיל)
| Workflow | מטרה | מתי להשתמש |
|----------|------|-----------|
| **GITHUB_PLANNING_DRY_RUN** | תכנון בטוח של שינויים ב-GitHub | כל פעם שרוצים לשנות משהו בריפו |

### ✅ **יכולות פעילות** (עיקריות)
- 📂 **GitHub**: קריאה מלאה, כתיבה ידנית, תכנון אוטומטי
- 💻 **Windows**: פקודות PowerShell, שליטה ב-UI, פתיחת אפליקציות
- 📁 **File System**: קריאה/כתיבה מקומית, חיפוש, ניתוח
- 📧 **Google**: קריאת Gmail, Calendar, Drive (READ-ONLY)

---

## 🎮 איך המערכת עובדת

### **עקרון מרכזי: DRY RUN + Human-in-the-loop**

```
┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
│  אור (Human) │ ───> │ GPT GitHub Agent│ ───> │ תוכנית מפורטת│
│              │      │   (Planner)     │      │  (DRY RUN)   │
└──────────────┘      └─────────────────┘      └──────────────┘
                                                       │
                                                       ▼
┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
│   GitHub     │ <─── │ Claude Desktop  │ <─── │ אישור + ביצוע│
│  (מעודכן)   │      │   (Executor)    │      │    ידני     │
└──────────────┘      └─────────────────┘      └──────────────┘
```

**במילים פשוטות**:
1. אני אומר מה אני רוצה לשנות
2. GPT Agent קורא מסמכים ומתכנן תוכנית מפורטת
3. אני בודק את התוכנית ומאשר
4. Claude Desktop מבצע את השינויים ידנית (תחת פיקוח שלי)
5. אנחנו מעדכנים את התיעוד

---

## 🔒 3 החלטות קריטיות (נעולות 2025-11-20)

### **החלטה #1: MCP Orchestration**
- ❌ **לא פעיל** - המערכת הישנה לא מיובאת כקוד רץ
- ✅ **Reference Only** - משמש כמקור השראה בלבד

### **החלטה #2: GitHub Executor API**
- ❌ **לא פרוס** - אין אוטומציה של כתיבה ל-GitHub
- ✅ **Blueprint** - משמש כתכנון בלבד

### **החלטה #3: GPT GitHub Agent – Execution Mode**
- ✅ **DRY RUN בלבד** - הסוכן מתכנן, לא מבצע
- ❌ **אין כתיבה אוטומטית** - כל פעולה דורשת אישור אנושי

**למה?** בטיחות מעל הכל. קודם בונים אמון, אחר כך אוטומציה.

---

## 📖 מדריך מהיר: איך מתחילים

### **שלב 1: הבן את החוקים**
קרא את [`docs/CONSTITUTION.md`](docs/CONSTITUTION.md) להבנת 9 העקרונות המנחים.

**עקרונות מרכזיים**:
1. **Data-First** - תיעוד לפני קוד
4. **Human-in-the-loop** - אישור אנושי לכל פעולה מסוכנת
6. **Thin Slices** - צעד אחד בכל פעם
7. **אבטחה מעל הכל** - בטיחות תמיד במקום ראשון

---

### **שלב 2: הבן מה המערכת יודעת לעשות**
עבור ל-[`docs/CAPABILITIES_MATRIX.md`](docs/CAPABILITIES_MATRIX.md) לראות:
- 22 יכולות מתועדות
- מי אחראי על כל יכולת
- מה הסטטוס (✅ Operational / 🚧 Limited / 📋 Planned)

---

### **שלב 3: הכר את הסוכנים**
קרא את [`agents/AGENTS_INVENTORY.md`](agents/AGENTS_INVENTORY.md) ו-[`agents/GPT_GITHUB_AGENT.md`](agents/GPT_GITHUB_AGENT.md).

**הסוכן הראשון: GPT GitHub Agent**
- תפקיד: Planner לשינויים ב-GitHub
- מצב: DRY RUN בלבד (לא מבצע אוטומטית)
- יכולות: קריאה, ניתוח, תכנון

---

### **שלב 4: הרץ Workflow ראשון**

**תרחיש לדוגמה: רוצה לעדכן README**

1. **פתח את** [`workflows/GITHUB_PLANNING_DRY_RUN.md`](workflows/GITHUB_PLANNING_DRY_RUN.md)
2. **נסח בקשה**: "אני רוצה לעדכן את README להוסיף סעיף על workflows"
3. **GPT Agent יחזיר תוכנית**:
   ```markdown
   # Plan:
   1. קרא README נוכחי
   2. זהה איפה להוסיף סעיף
   3. כתוב טקסט מוצע
   4. הצע commit message
   ```
4. **אתה בודק ומאשר**
5. **Claude Desktop מבצע** (עם אישור שלך לכל צעד)
6. **עדכון תיעוד** (אם נדרש)

---

### **שלב 5: שמור על SSOT מעודכן**

כל שינוי משמעותי:
- ✅ מתועד ב-`docs/SYSTEM_SNAPSHOT.md`
- ✅ מעדכן `docs/CAPABILITIES_MATRIX.md` (אם הוספת יכולת)
- ✅ מוסיף ל-`docs/DECISIONS_AI_OS.md` (אם זו החלטה קריטית)

**חוק ברזל**: המסמכים = מקור האמת. אם זה לא מתועד, זה לא קיים.

---

## 🛠️ כלים וטכנולוגיות

| כלי | מטרה | סטטוס |
|-----|------|-------|
| **Claude Desktop** | מבצע ידני + גישה ל-MCP | ✅ Active |
| **GitHub MCP** | קריאה/כתיבה לריפואים | ✅ Active |
| **Filesystem MCP** | גישה לקבצים מקומיים | ✅ Active |
| **Windows MCP** | שליטה ב-Windows + PowerShell | ✅ Active |
| **Google MCP** | גישה ל-Gmail, Calendar, Drive | ✅ Active (READ) |
| **GPT GitHub Agent** | תכנון שינויים | ✅ Active (DRY RUN) |

---

## 🗺️ Roadmap – לאן זה הולך

### **✅ Phase 1: Foundation (DONE)**
- תיעוד ליבה (CONSTITUTION, CAPABILITIES, DECISIONS)
- סוכן ראשון (GPT GitHub Agent)
- Workflow ראשון (GITHUB_PLANNING_DRY_RUN)

### **🔄 Phase 2: Expansion (IN PROGRESS)**
- [ ] תיעוד כלים ב-`tools/`
- [ ] Workflows נוספים (Decision Logging, SSOT Updates)
- [ ] העשרת `CAPABILITIES_MATRIX` עם יכולות נוספות

### **🔮 Phase 3: Automation (FUTURE)**
- [ ] מעבר ל-Semi-Automated (GPT Agent יוצר טיוטות PR)
- [ ] Executor מוגבל ל-OS_SAFE בלבד
- [ ] Health Checks אוטומטיים
- [ ] Multi-Agent Coordination

### **🌟 Phase 4: Advanced (FAR FUTURE)**
- [ ] Executor מלא עם אישור אנושי
- [ ] Self-Healing capabilities
- [ ] Voice/Audio Control
- [ ] Advanced Analytics

---

## 📚 מסמכים חיוניים (קרא אותם!)

### **לכניסה למערכת (Start Here)**:
1. [`docs/CONSTITUTION.md`](docs/CONSTITUTION.md) - חוקי היסוד
2. [`docs/SYSTEM_SNAPSHOT.md`](docs/SYSTEM_SNAPSHOT.md) - מצב נוכחי
3. [`docs/CAPABILITIES_MATRIX.md`](docs/CAPABILITIES_MATRIX.md) - מה המערכת יודעת

### **להבנת הסוכנים**:
4. [`agents/AGENTS_INVENTORY.md`](agents/AGENTS_INVENTORY.md) - רשימת סוכנים
5. [`agents/GPT_GITHUB_AGENT.md`](agents/GPT_GITHUB_AGENT.md) - סוכן ליבה #1

### **לעבודה מעשית**:
6. [`workflows/GITHUB_PLANNING_DRY_RUN.md`](workflows/GITHUB_PLANNING_DRY_RUN.md) - איך לתכנן שינויים

### **להבנת החלטות**:
7. [`docs/DECISIONS_AI_OS.md`](docs/DECISIONS_AI_OS.md) - החלטות נעולות
8. [`docs/REPO_AUDIT_make-ops-clean.md`](docs/REPO_AUDIT_make-ops-clean.md) - מה היה קודם

---

## 🤝 עקרונות עבודה

### **1. בטיחות תמיד ראשון 🔒**
- אין אוטומציה בלי בקרה אנושית
- כל פעולה מסוכנת דורשת אישור מפורש
- תמיד אפשר לעשות rollback

### **2. תיעוד = מקור האמת 📝**
- אם זה לא ב-`docs/`, זה לא קיים
- כל שינוי משמעותי מתועד
- SSOT עדיף על זיכרון

### **3. Thin Slices 🍰**
- צעד אחד בכל פעם
- בדיקה אחרי כל צעד
- לא מתקדמים בלי אישור

### **4. DRY RUN First 🏃**
- קודם מתכננים, אחר כך מבצעים
- GPT Agent מציע, Human מחליט
- לא קופצים ישר לביצוע

---

## ⚠️ מה המערכת לא עושה (ולא תעשה בקרוב)

- ❌ **אין אוטומציה של כתיבה ל-GitHub** בלי אישור
- ❌ **אין ביצוע פעולות הרסניות** (מחיקה, שינוי מבנה) אוטומטית
- ❌ **אין גישה לסיסמאות/טוקנים** מהסוכנים
- ❌ **אין הרצת קוד לא בדוק** על המחשב
- ❌ **אין שינוי workflows/סקריפטים** בלי review

**למה?** כי בטיחות חשובה יותר מנוחות.

---

## 🔒 אבטחה וסיקרטים (Security & Secrets)

### **עקרונות אבטחה**

הריפו `ai-os` נבנה להיות **בטוח מיסודו**:

✅ **אף סיקרט לא נשמר בקוד**:
- אין סיסמאות, טוקנים או מפתחות API בקבצי Markdown
- אין credentials בקבצי config או קוד
- אין קבצי `.env` בגיט

✅ **סיקרטים רק במקומות מאובטחים**:
- GitHub Secrets (repository/organization)
- Environment Variables (לא בגיט!)
- Secret Manager חיצוני (Google Secret Manager, 1Password, וכו')
- OS Keychain / איחסון מקומי מוצפן

✅ **הגנה אוטומטית**:
- קובץ `.gitignore` מגן על קבצי סיקרטים
- אזהרות מובנות לפני commits
- בדיקות אבטחה ב-workflows

### **מה מוגן**

ה-`.gitignore` מונע אוטומטית מ-commit:
- קבצי סביבה: `*.env`, `.env.*`
- קבצי סיקרטים: `secrets.*`, `*.key`, `*.pem`
- קונפיגים מקומיים: `config/local*`, `config/dev*`
- לוגים ודאמפים: `*.log`, `*.dump`, `logs/`

### **מדיניות מלאה**

למידע מקיף על מדיניות האבטחה, ראה:
📜 [`policies/SECURITY_SECRETS_POLICY.md`](policies/SECURITY_SECRETS_POLICY.md)

המדיניות כוללת:
- 4 עקרונות יסוד (No Plain Text, Never Display, Human Auth, Minimal Privilege)
- כללים לכל סוכן/כלי
- תהליכי מיגרציה ו-incident response
- אזורים רגישים (High Risk Zones)

### **אם מצאת סיקרט בקוד 🚨**

1. **לא לעשות commit!**
2. הסר את הסיקרט מהקובץ
3. החלף ב-placeholder: `${SECRET_NAME}`
4. שמור את הסיקרט ב-GitHub Secrets / Environment
5. רוטט את הסיקרט (יצירת אחד חדש)

**זכור**: אם סיקרט כבר נכנס ל-commit, הוא **נשאר בהיסטוריה לצמיתות** וחייב רוטציה.

---

## 💡 FAQ

### **ש: למה כל זה נראה מורכב?**
**ת**: זה לא מורכב, זה **מבוקר**. המטרה היא לא לזרוק סקריפטים ולקוות לטוב - המטרה היא לבנות מערכת שאפשר לסמוך עליה לאורך זמן.

### **ש: למה DRY RUN ולא ביצוע אוטומטי?**
**ת**: כי צריך לבנות אמון הדרגתי. אחרי שנראה שהתכנון עובד טוב (100+ הפעלות מוצלחות), נשקול semi-automation.

### **ש: איפה הקוד של הסוכנים?**
**ת**: כרגע הקוד בריפו הישן (`make-ops-clean`). אנחנו מתכננים בצורה מבוקרת איך לייבא אותו. ראה [`docs/DECISIONS_AI_OS.md`](docs/DECISIONS_AI_OS.md).

### **ש: למה יש כל כך הרבה תיעוד?**
**ת**: כי **תיעוד = זיכרון**. בלי תיעוד, כל שיחה עם AI מתחילה מאפס. עם תיעוד - המערכת זוכרת הכל.

### **ש: אפשר להוסיף סוכן חדש?**
**ת**: כן! פשוט תעד אותו ב-`agents/` ועדכן את `AGENTS_INVENTORY.md` + `CAPABILITIES_MATRIX.md`.

### **ש: מה עושים אם משהו נשבר?**
**ת**: Rollback! כל שינוי הוא commit נפרד, אז תמיד אפשר לחזור לגרסה קודמת עם `git revert`.

---

## 📞 צור קשר / תרומה

המערכת הזו נבנית כרגע בעבור משתמש אחד (אור), אבל אם יש לך רעיונות או שאלות:
- פתח Issue ב-GitHub
- תן כוכב ⭐ לריפו אם אהבת את הגישה

---

## 📜 רישיון

MIT License - תשתמש בחופשיות, אבל בלי אחריות 😊

---

**סטטוס מערכת**: ✅ Active & Operational (DRY RUN Mode)  
**גרסה**: 1.0  
**עדכון אחרון**: 20 נובמבר 2025  
**צעד הבא**: להפעיל את ה-workflow על משימה אמיתית!

---

**זכור**: המערכת הזו לא מושלמת, אבל היא **מתועדת, בטוחה, ושקופה**. וזה יותר טוב מסקריפט מגניב שאף אחד לא זוכר איך הוא עובד אחרי שבוע.

**בהצלחה! 🚀**
