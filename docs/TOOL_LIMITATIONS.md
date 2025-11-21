# Tool Limitations – מגבלות כלים ידועות

**Created**: 2025-11-21  
**Purpose**: תיעוד מגבלות כלים וכישלונות טכניים שנתגלו  
**Status**: ✅ Active

---

## 🎯 מטרת המסמך

מסמך זה מתעד:
- מגבלות ידועות של MCPs וכלים
- כישלונות טכניים שנתקלנו בהם
- פתרונות עוקפים או ארכיטקטורה חלופית
- מה חסר לנו וצריך להוסיף

**חשוב**: כאשר Claude נתקל במגבלת כלי במהלך ביצוע משימה, הוא מתעד כאן במקום להעביר עבודה טכנית לאור.

---

## 📋 מגבלות ידועות

### ❌ אין גישה ל-OpenAI API מ-Claude's Computer

**תאריך**: 2025-11-21  
**כלי מושפע**: GPT Planner (`ai_core/gpt_orchestrator.py`)  
**תיאור**:
- GPT Planner דורש `openai` Python package
- Claude's computer (במרחב ה-bash) אין לו את החבילה
- Claude's computer לא יכול להריץ את GPT Planner ישירות

**פתרון עוקף נוכחי**:
✅ GPT Planner רץ **במחשב של אור** (Windows)
- אור מריץ: `python ai_core/gpt_orchestrator.py`
- הסקריפט קורא SSOT, קורא ל-GPT, ומחזיר תכנית
- Claude Desktop מקבל את התכנית ומבצע

**מה זה אומר**:
- Claude Desktop **לא** מריץ את GPT Planner בעצמו
- Claude Desktop מקבל תוכנית **מוכנה** מ-GPT Planner
- התהליך עדיין אוטומטי אחרי אישור של אור

**האם זו בעיה?**
❌ **לא** - זה בדיוק התכנון:
- אור: מנסח כוונה
- GPT Planner: מתכנן (במחשב של אור)
- Claude Desktop: מבצע (עם MCPs)

**האם צריך לפתור?**
- ⚠️ **אפשרי אבל לא הכרחי** - אפשר להוסיף MCP ל-OpenAI API בעתיד
- ✅ **הפתרון הנוכחי עובד טוב** - המערכת פועלת כמתוכנן

---

### ℹ️ bash_tool עובד רק ב-Claude's Computer

**תאריך**: 2025-11-21  
**כלי מושפע**: `bash_tool`  
**תיאור**:
- `bash_tool` מריץ פקודות ב-Claude's computer (Linux container)
- לא יכול לגשת ישירות לקבצים של אור ב-Windows

**פתרון נוכחי**:
✅ שימוש ב-`Filesystem` MCP ו-`autonomous-control` לגישה למחשב של אור
- `Filesystem:read_text_file` - קריאת קבצים מ-Windows
- `Filesystem:write_file` - כתיבת קבצים ל-Windows  
- `autonomous-control:execute_command` - הרצת git/PowerShell ב-Windows

**האם זו בעיה?**
❌ **לא** - יש לנו את הכלים הנכונים

---

## ✅ כלים שעובדים מצוין

### Filesystem MCP
- ✅ קריאת קבצים מ-Windows של אור
- ✅ כתיבת קבצים ל-Windows של אור
- ✅ עריכת קבצים (str_replace)
- ✅ יצירת תיקיות

### autonomous-control MCP
- ✅ git commands (add, commit, push)
- ✅ PowerShell commands
- ✅ הרצת Python scripts

### GitHub MCP
- לא נבדק עדיין - יש פונקציונליות גיבוי

---

## 🔧 פתרונות ארכיטקטורה

### דפוס עבודה נוכחי (עובד! ✅)

```
1. אור: "צור workflow חדש"
   ↓
2. Claude Desktop קורא ל:
   python ai_core/gpt_orchestrator.py --intent "צור workflow חדש"
   (רץ במחשב של אור, עם OpenAI SDK)
   ↓
3. GPT Planner מחזיר תכנית מובנית
   ↓
4. Claude Desktop מציג ומבקש אישור
   ↓
5. אור: ✅
   ↓
6. Claude Desktop מבצע עם Filesystem + autonomous-control MCPs
```

**למה זה עובד טוב**:
- ✅ OpenAI API רץ במקום הנכון (Windows)
- ✅ SSOT נגיש (Filesystem MCP)
- ✅ ביצוע אוטומטי (autonomous-control)
- ✅ אור לא עושה טכני

---

## 📊 סטטוס סיכום

| רכיב | מצב | הערות |
|------|-----|-------|
| **GPT Planner** | ✅ פעיל | רץ במחשב של אור |
| **Claude Desktop** | ✅ פעיל | מבצע דרך MCPs |
| **Filesystem MCP** | ✅ עובד | גישה מלאה לקבצים |
| **autonomous-control** | ✅ עובד | git + PowerShell |
| **GPT Planner ב-Claude's computer** | ⚠️ לא זמין | לא הכרחי |

---

## 🚀 שיפורים אפשריים (עתיד)

### אופציה 1: MCP לקריאת GPT API
- ליצור MCP שקורא ל-OpenAI API
- Claude Desktop יכול לקרוא ישירות
- **יתרון**: צעד אחד פחות
- **חיסרון**: צריך לפתח MCP חדש

### אופציה 2: להשאיר כמו שזה
- הדפוס הנוכחי עובד טוב
- אור מריץ GPT Planner כשצריך
- Claude מבצע את התכנית
- **יתרון**: פשוט ועובד
- **חיסרון**: צעד נוסף (לא אוטומטי לגמרי)

---

## 📝 לוג שינויים

### 2025-11-21
- ✅ תיעוד מגבלת OpenAI API ב-Claude's computer
- ✅ תיעוד הדפוס העובד הנוכחי
- ✅ תיעוד כלים שעובדים מצוין

---

**נזכיר**: כל כישלון טכני שנתקלים בו = תיעוד כאן + הצעת פתרון + המשך עבודה.  
**לא** = העברת עבודה טכנית לאור. ✨
