# GPT Planner Contract – חוזה תכנון רשמי

**Created**: 2025-11-21  
**Purpose**: הגדרת הממשק הרשמי בין GPT Planner ל-Claude Desktop  
**Status**: ✅ Active

---

## 🎯 מטרת המסמך

מסמך זה מגדיר את **החוזה** בין שכבת התכנון (GPT Planner) לבין שכבת הביצוע (Claude Desktop):
- איזה פורמט GPT Planner מחזיר
- איך Claude Desktop מפרש ומבצע
- איך מדווחים לאור

**זהו ממשק קבוע** - כל שינוי בו דורש עדכון גרסה ותיעוד.

---

## 📤 פלט מ-GPT Planner (Output Contract)

### **פורמט תשובה סטנדרטי**:

GPT Planner **חייב** להחזיר תשובה במבנה הבא:

```markdown
1. מה הבנתי מהכוונה:
[סיכום קצר של ה-intent של אור - 1-3 משפטים]

2. הקשר רלוונטי מתוך ה-SSOT (בקצרה):
[אילו מסמכים/מדיניות רלוונטיים - 2-4 משפטים]

3. תכנית פעולה צעד-צעד:
   - [צעד 1: תיאור ברור]
   - [צעד 2: תיאור ברור]
   - [צעד N: תיאור ברור]

4. מה צריך Claude לעשות בפועל (פעולות טכניות):
   - [פעולה טכנית 1: קובץ/git/command]
   - [פעולה טכנית 2: קובץ/git/command]
   - [פעולה טכנית N: קובץ/git/command]

5. מה אור צריך רק לאשר / להחליט:
   - [החלטה 1]
   - [החלטה 2]
```

### **שדות חובה**:

| סעיף | חובה? | מטרה |
|------|-------|------|
| **1. מה הבנתי** | ✅ כן | אימות הבנה משותפת |
| **2. הקשר מ-SSOT** | ✅ כן | עקיבות עם מדיניות |
| **3. תכנית צעד-צעד** | ✅ כן | מפת דרכים ברורה |
| **4. פעולות Claude** | ✅ כן | הוראות ביצוע מפורשות |
| **5. מה אור מאשר** | ✅ כן | הבהרת נקודות החלטה |

---

## 📥 קלט ל-GPT Planner (Input Contract)

### **פורמט intent**:

```python
intent: str  # כוונה חופשית בטקסט טבעי
```

**דוגמאות**:
- ✅ "צור workflow חדש לניהול secrets"
- ✅ "עדכן את SYSTEM_SNAPSHOT עם המדיניות החדשה"
- ✅ "הוסף תיעוד על GPT Planner ל-AGENT_ONBOARDING"

**אין הגבלה על נוסח**, אבל ככל שהכוונה ברורה יותר - התכנית מדויקת יותר.

---

## ⚙️ ביצוע ב-Claude Desktop (Execution Contract)

### **איך Claude מפרש את הפלט**:

#### 1. **קריאת סעיף 4 ("מה צריך Claude לעשות בפועל")**
Claude עובר על רשימת הפעולות הטכניות ומזהה:

| סוג פעולה | איך מזהים | איזה כלי |
|-----------|-----------|----------|
| **יצירת קובץ** | "צור קובץ X.md", "הוסף קובץ" | `Filesystem:write_file` |
| **עריכת קובץ** | "ערוך X.md", "עדכן X.md" | `Filesystem:edit_file` |
| **מחיקת קובץ** | "מחק X.md" | ⚠️ דורש אישור כפול |
| **Git commit** | "עשה commit", "commit עם הודעה" | `autonomous-control:execute_command` |
| **Git push** | "push לגיטהאב", "העלה לremote" | `autonomous-control:execute_command` |
| **קריאת קובץ** | "קרא X.md", "בדוק תוכן" | `Filesystem:read_text_file` |

#### 2. **ביצוע הפעולות לפי סדר**
Claude מבצע את הפעולות **בדיוק בסדר שצוין** בסעיף 3 ("תכנית צעד-צעד").

#### 3. **טיפול בשגיאות**
- אם פעולה נכשלת → Claude עוצר ומדווח
- לא ממשיך לפעולה הבאה בלי פתרון
- אם זו מגבלת כלי → מעבר ל-DESIGN mode

---

## 📊 דיווח לאור (Reporting Contract)

### **פורמט דיווח סטנדרטי**:

```markdown
✅ **בוצע בהצלחה!**

### מה נעשה:
- [פעולה 1: תיאור קצר]
- [פעולה 2: תיאור קצר]
- [פעולה N: תיאור קצר]

### Commit:
- **SHA**: [commit hash]
- **Message**: "[commit message]"
- **קישור**: https://github.com/edri2or-commits/ai-os/commit/[hash]

### סיכום:
[משפט 1-2: מה השתנה במערכת]
```

### **אם היו בעיות**:

```markdown
⚠️ **הושלם חלקית**

### מה בוצע:
- [✅ פעולה מוצלחת 1]
- [✅ פעולה מוצלחת 2]

### מה נתקע:
- [❌ פעולה שנכשלה: סיבה]

### פתרון מוצע:
[מה צריך לעשות כדי להשלים]
```

---

## 🔄 תהליך מלא (End-to-End Flow)

### **זרימה מלאה**:

```
1. אור: "צור workflow חדש לX"
   ↓
2. Claude: [קורא ל-GPT Planner עם intent]
   ↓
3. GPT Planner: [מחזיר תכנית מובנית]
   ↓
4. Claude: [מציג תכנית לאור]
   "📋 תכנית מ-GPT Planner:
    1. צור קובץ WF-004.md
    2. עדכן SYSTEM_SNAPSHOT
    3. commit + push
    
    ✅ לאשר ולבצע?"
   ↓
5. אור: "✅"
   ↓
6. Claude: [מבצע לפי סעיף 4]
   - Filesystem:write_file → WF-004.md
   - Filesystem:edit_file → SYSTEM_SNAPSHOT.md
   - autonomous-control → git add + commit + push
   ↓
7. Claude: [מדווח]
   "✅ בוצע! [קישור ל-commit]
    שינויים: WF-004 נוצר, SYSTEM_SNAPSHOT עודכן"
```

---

## 🚫 מה אסור לעשות

### **GPT Planner לא יכול**:
- ❌ לבצע פעולות בעצמו (הוא רק מתכנן)
- ❌ לדלג על אחד מ-5 הסעיפים
- ❌ לבקש מאור פעולות טכניות
- ❌ להמציא מידע שלא ב-SSOT

### **Claude Desktop לא יכול**:
- ❌ להמציא פעולות שלא בסעיף 4
- ❌ לדלג על אישור של אור
- ❌ להמשיך אחרי כשל בלי דיווח
- ❌ לבקש מאור פעולות טכניות

### **אור לא צריך**:
- ❌ לעשות git commands
- ❌ ליצור/לערוך קבצים
- ❌ להריץ פקודות
- ✅ רק: לאשר ✅ או לבקש שינויים

---

## 📝 דוגמאות מלאות

### **דוגמה 1: יצירת workflow חדש**

**Input (intent)**:
```
"צור workflow חדש לניהול גיבויים אוטומטי"
```

**Output (מ-GPT Planner)**:
```markdown
1. מה הבנתי מהכוונה:
אור רוצה workflow חדש (WF-004) לניהול גיבויים אוטומטי של הריפו.

2. הקשר רלוונטי מתוך ה-SSOT (בקצרה):
יש כרגע 3 workflows (WF-001 עד WF-003). הוספת WF-004 דורשת עדכון SYSTEM_SNAPSHOT ו-CAPABILITIES_MATRIX.

3. תכנית פעולה צעד-צעד:
   - צור קובץ workflows/BACKUP_AUTOMATION.md (WF-004)
   - עדכן SYSTEM_SNAPSHOT.md - הוסף WF-004 לרשימה
   - עדכן CAPABILITIES_MATRIX.md - הוסף capability חדש
   - commit + push

4. מה צריך Claude לעשות בפועל (פעולות טכניות):
   - צור קובץ workflows/BACKUP_AUTOMATION.md עם מבנה workflow
   - ערוך docs/SYSTEM_SNAPSHOT.md - הוסף WF-004 לרשימת workflows
   - ערוך docs/CAPABILITIES_MATRIX.md - הוסף capability
   - git add workflows/BACKUP_AUTOMATION.md docs/SYSTEM_SNAPSHOT.md docs/CAPABILITIES_MATRIX.md
   - git commit -m "Add WF-004: Backup Automation workflow"
   - git push

5. מה אור צריך רק לאשר / להחליט:
   - האם התוכן של WF-004 מתאים
   - האם השם "BACKUP_AUTOMATION" נכון
```

**Execution (Claude)**:
```
[Claude מציג את התכנית]
[אור: ✅]
[Claude מבצע 6 פעולות]
[Claude מדווח: ✅ בוצע! [link]]
```

---

### **דוגמה 2: עדכון מסמך קיים**

**Input (intent)**:
```
"עדכן את AGENT_ONBOARDING עם מידע על GPT Planner"
```

**Output (מ-GPT Planner)**:
```markdown
1. מה הבנתי מהכוונה:
אור רוצה להוסיף סעיף על GPT Planner ל-AGENT_ONBOARDING.md.

2. הקשר רלוונטי מתוך ה-SSOT (בקצרה):
AGENT_ONBOARDING הוא מדריך לסוכנים. GPT Planner הוא שכבת תכנון חדשה שצריכה להיות מוסברת.

3. תכנית פעולה צעד-צעד:
   - קרא את AGENT_ONBOARDING.md הנוכחי
   - הוסף סעיף חדש על GPT Planner
   - עדכן SYSTEM_SNAPSHOT - גרסה חדשה
   - commit + push

4. מה צריך Claude לעשות בפועל (פעולות טכניות):
   - קרא docs/AGENT_ONBOARDING.md
   - ערוך docs/AGENT_ONBOARDING.md - הוסף סעיף "GPT Planner"
   - ערוך docs/SYSTEM_SNAPSHOT.md - עדכן גרסה
   - git add docs/AGENT_ONBOARDING.md docs/SYSTEM_SNAPSHOT.md
   - git commit -m "docs: add GPT Planner section to AGENT_ONBOARDING"
   - git push

5. מה אור צריך רק לאשר / להחליט:
   - האם התוכן מתאים
   - האם המיקום בסעיפים נכון
```

---

## 🔧 עדכון החוזה

### **מתי לעדכן**:
- שינוי בפורמט הפלט של GPT Planner
- הוספת שדות חדשים
- שינוי בתהליך הביצוע
- תיקון באגים בפרשנות

### **איך לעדכן**:
1. תעד את השינוי ב-DECISIONS_AI_OS (WF-002)
2. עדכן מסמך זה עם גרסה חדשה
3. הודע לכל הסוכנים על השינוי

---

## 📌 גרסה נוכחית

**Version**: 1.0  
**Last Updated**: 2025-11-21  
**Compatible With**:
- GPT Planner: `ai_core/gpt_orchestrator.py` v1.0
- Claude Desktop: Latest
- Model: gpt-4o-mini

---

## ✅ Checklist תאימות

לפני שמשתמשים בחוזה, וודא:

- [ ] GPT Planner מחזיר את 5 הסעיפים
- [ ] Claude יודע לפרש סעיף 4
- [ ] יש אישור מאור לפני ביצוע
- [ ] Commit message ברור
- [ ] דיווח סופי כולל קישור

---

**זהו החוזה הרשמי. כל שינוי דורש עדכון מסמך זה.** ✨
