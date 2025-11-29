# Intents Router – ניתוב כוונות (Intent Routing Layer)

**Created**: 2025-11-21  
**Purpose**: תיעוד שכבת הניתוב שמעל GPT Planner  
**Status**: 🎯 Design Phase (לא מיושם עדיין)

---

## 🎯 מה זה Intent Router?

**Intent Router** היא השכבה החיצונית ביותר של AI-OS - זה "הקבלן הראשי" שמקבל כוונות רחבות ומפרק אותן לצעדים.

### **תפקיד**:
כשמקבלים intent **גבוה** (למשל: "בנה לי סוכן שבודק מיילים"), ה-Intent Router:
1. **מפרק** את הכוונה למשימות קטנות
2. **מנתב** כל משימה לגורם הנכון:
   - GPT Planner → תכנון טכני
   - Claude Desktop → ביצוע
   - Workflows → תהליכים מוגדרים
3. **מתאם** בין כל החלקים
4. **מדווח** לאור על ההתקדמות

---

## 🔄 זרימה כללית

```
┌─────────────────────────────────────────────┐
│ Chat חיצוני (ChatGPT / Telegram / Web UI)│
│ שולח: "בנה לי סוכן שבודק מיילים"         │
└──────────────┬──────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│ INTENT ROUTER (שכבה חדשה!)                 │
│ מפרק לתתי-משימות:                          │
│   1. תכנן את הסוכן (GPT Planner)           │
│   2. צור מבנה קבצים (Claude)                │
│   3. הגדר OAuth ל-Gmail (Manual - אור)      │
│   4. כתוב קוד לקריאת מיילים (Claude)        │
│   5. בדוק ותעד (Claude + אור)               │
└──────────────┬───────────────────────────────┘
               ↓
        ┌──────┴──────┐
        ↓             ↓
┌──────────────┐  ┌──────────────┐
│ GPT Planner │  │ Claude       │
│ (תכנון)     │  │ Desktop      │
│             │  │ (ביצוע)      │
└──────┬───────┘  └──────┬───────┘
       ↓                 ↓
┌──────────────────────────────────┐
│ Workflows (WF-001/002/003)      │
└──────────────────────────────────┘
               ↓
┌──────────────────────────────────┐
│ MCPs (Filesystem, Git, Google)  │
└──────────────────────────────────┘
```

---

## 🗺️ מיפוי: מי עושה מה?

### **Intent Router** (שכבת התיאום):

**תפקיד**:
- מקבל intent רחב מchat חיצוני
- **מפרק** לרשימת תתי-משימות
- **מנתב** כל תת-משימה לגורם הנכון
- **עוקב** אחרי ההתקדמות
- **מדווח** לאור על כל שלב

**דוגמה**:
```
Input: "בנה לי סוכן שבודק מיילים"

Router מפרק ל:
├─ Task 1: "תכנן ארכיטקטורת סוכן Gmail" → GPT Planner
├─ Task 2: "צור קובץ GMAIL_CHECKER_AGENT.md" → Claude Desktop
├─ Task 3: "הגדר Gmail OAuth" → Manual (אור מאשר)
├─ Task 4: "כתוב gmail_checker.py" → Claude Desktop + GPT Planner
├─ Task 5: "עדכן AGENTS_INVENTORY.md" → Claude Desktop
└─ Task 6: "בדוק שהכל עובד" → Manual (אור בודק)
```

---

### **GPT Planner** (מוח התכנון):

**תפקיד**:
- מקבל תת-משימה **טכנית אחת** מה-Router
- **קורא** את כל ה-SSOT
- **מחזיר** תכנית מפורטת (לפי החוזה)

**מתי משתמשים**:
- ✅ יצירת ארכיטקטורה / מבנה
- ✅ החלטות טכניות מורכבות
- ✅ תכנון קוד או workflow חדש
- ❌ לא לביצוע - רק תכנון!

**דוגמה**:
```
Input: "תכנן ארכיטקטורת סוכן Gmail"

GPT Planner מחזיר:
1. מה הבנתי: צריך סוכן שקורא Gmail, מסנן, ומדווח
2. הקשר: יש Gmail MCP קיים (Read-Only)
3. תכנית:
   - קובץ: agents/GMAIL_CHECKER_AGENT.md
   - קובץ: ai_core/agents/gmail_checker.py
   - תלות: Gmail MCP, OAuth setup
4. פעולות ל-Claude:
   - צור agents/GMAIL_CHECKER_AGENT.md
   - צור ai_core/agents/gmail_checker.py
   - עדכן AGENTS_INVENTORY.md
5. מה אור מאשר:
   - הארכיטקטורה
   - סוג הסינון (מילות מפתח? נושא?)
```

---

### **Claude Desktop** (ידיים מבצעות):

**תפקיד**:
- מקבל תכנית **מוכנה** מGPT Planner
- **מבצע** את הפעולות דרך MCPs
- **מדווח** בחזרה על ביצוע

**מתי משתמשים**:
- ✅ יצירת/עריכת קבצים
- ✅ git operations
- ✅ הרצת כלים קיימים
- ❌ לא לתכנון - רק ביצוע!

**דוגמה**:
```
Input: תכנית מGPT Planner

Claude מבצע:
1. Filesystem:write_file → agents/GMAIL_CHECKER_AGENT.md
2. Filesystem:write_file → ai_core/agents/gmail_checker.py
3. Filesystem:edit_file → agents/AGENTS_INVENTORY.md
4. autonomous-control → git add + commit + push
5. דיווח: ✅ בוצע! [link to commit]
```

---

### **Workflows (WF-001/002/003)** (תהליכים מוגדרים):

**תפקיד**:
- תהליכים **חוזרים** עם צעדים קבועים
- נכנסים לפעולה כש-Router מזהה תבנית מוכרת

**מתי משתמשים**:

| Workflow | מתי נכנס ללופ | דוגמה |
|----------|---------------|--------|
| **WF-001** | שינוי GitHub | Router זיהה "צור קובץ חדש" |
| **WF-002** | החלטה משמעותית | Router זיהה "הגדר מדיניות" |
| **WF-003** | סריקת secrets | Router זיהה "בדוק אבטחה" |

**דוגמה**:
```
Input: "עדכן את המדיניות לאבטחת מיילים"

Router מזהה: זו החלטה → WF-002
└─ WF-002 נכנס:
   1. ניסוח ההחלטה
   2. יצירת רשומה ב-DECISIONS
   3. עדכון SSOT רלוונטי
   4. בדיקה צולבת
   5. commit + push
```

---

## 📋 דוגמאות End-to-End

### 🟢 דוגמה 1: קלה - "עדכון תיעוד"

**Input מ-Chat חיצוני**:
```
"עדכן את AGENT_ONBOARDING עם מידע על Intent Router"
```

**Router מפרק**:
```
Task 1: "הבן את Intent Router" → Router עצמו
Task 2: "תכנן איזה תוכן להוסיף" → GPT Planner
Task 3: "ערוך את AGENT_ONBOARDING.md" → Claude Desktop
Task 4: "commit + push" → Claude Desktop
```

**זרימה מפורטת**:
```
1. Router → GPT Planner: "תכנן תוכן על Intent Router ל-AGENT_ONBOARDING"
   ↓
2. GPT Planner מחזיר:
   - סעיף חדש: "Intent Router - שכבת הניתוב"
   - מיקום: אחרי סעיף "ארכיטקטורה"
   - תוכן: הסבר קצר + דיאגרמה
   ↓
3. Claude Desktop מבצע:
   - קורא AGENT_ONBOARDING.md
   - מוסיף סעיף חדש
   - עדכן SYSTEM_SNAPSHOT (גרסה)
   - git add + commit + push
   ↓
4. דיווח: ✅ עודכן! [link]
```

**זמן משוער**: 2-3 דקות  
**מעורבות אור**: אישור אחד (✅)

---

### 🟡 דוגמה 2: בינונית - "יצירת workflow חדש"

**Input מ-Chat חיצוני**:
```
"צור workflow לגיבוי אוטומטי של הריפו לGoogle Drive"
```

**Router מפרק**:
```
Task 1: "תכנן workflow WF-004" → GPT Planner
Task 2: "צור workflows/BACKUP_TO_DRIVE.md" → Claude Desktop
Task 3: "עדכן SYSTEM_SNAPSHOT" → Claude Desktop
Task 4: "עדכן CAPABILITIES_MATRIX" → Claude Desktop
Task 5: "תעד החלטה" → WF-002
Task 6: "commit + push" → Claude Desktop
```

**זרימה מפורטת**:
```
1. Router → GPT Planner: "תכנן WF-004 לגיבוי אוטומטי"
   ↓
2. GPT Planner מחזיר:
   - מבנה workflow מלא
   - צעדים: 1) זיהוי שינויים 2) העתקה לDrive 3) ולידציה
   - תלות: Google Drive MCP (write mode)
   ↓
3. Router מזהה: צריך החלטה → WF-002
   ↓
4. WF-002 מופעל:
   - יוצר רשומה ב-DECISIONS_AI_OS.md
   - מסביר למה WF-004 נדרש
   ↓
5. Claude Desktop מבצע:
   - יוצר workflows/BACKUP_TO_DRIVE.md
   - מעדכן SYSTEM_SNAPSHOT.md
   - מעדכן CAPABILITIES_MATRIX.md
   - git add + commit + push
   ↓
6. דיווח: ✅ WF-004 נוצר! [link]
```

**זמן משוער**: 5-7 דקות  
**מעורבות אור**: 2 אישורים (תוכנית + החלטה)

---

### 🔴 דוגמה 3: כבדה - "אוטומציה מול Gmail"

**Input מ-Chat חיצוני**:
```
"בנה לי סוכן שבודק מיילים מלקוחות VIP וישלח לי התראה לטלגרם"
```

**Router מפרק**:
```
Task 1: "תכנן ארכיטקטורת הסוכן" → GPT Planner
Task 2: "בדוק אבטחת Gmail OAuth" → WF-003 (Secret Discovery)
Task 3: "צור GMAIL_VIP_AGENT.md" → Claude Desktop
Task 4: "כתוב gmail_vip_checker.py" → GPT Planner + Claude
Task 5: "הגדר Gmail OAuth" → Manual (אור)
Task 6: "הגדר Telegram Bot Token" → Manual (אור)
Task 7: "בדוק הסוכן" → Manual (אור)
Task 8: "תעד החלטה על סוכן חדש" → WF-002
Task 9: "עדכן תיעוד" → Claude Desktop
Task 10: "commit + push" → Claude Desktop
```

**זרימה מפורטת**:
```
1. Router → GPT Planner: "תכנן סוכן VIP Gmail→Telegram"
   ↓
2. GPT Planner מחזיר:
   - ארכיטקטורה: קורא Gmail MCP → מסנן VIP → שולח Telegram
   - קבצים: agents/GMAIL_VIP_AGENT.md, ai_core/agents/gmail_vip.py
   - תלות: Gmail MCP (read), Telegram Bot API
   - אזהרות: צריך OAuth, Telegram token
   ↓
3. Router → WF-003: "סרוק אבטחה לפני OAuth"
   ↓
4. WF-003 מחזיר: ✅ אין secrets ישנים, בטוח להמשיך
   ↓
5. Claude Desktop מבצע:
   - יוצר agents/GMAIL_VIP_AGENT.md (תיאור)
   ↓
6. Router → GPT Planner: "כתוב gmail_vip.py"
   ↓
7. GPT Planner מחזיר: קוד Python מלא
   ↓
8. Claude Desktop מבצע:
   - יוצר ai_core/agents/gmail_vip.py
   - מעדכן AGENTS_INVENTORY.md
   ↓
9. Router → אור: "צריך OAuth + Telegram token - בדוק MANUAL_STEPS.md"
   ↓
10. אור: מגדיר OAuth, מוסיף Telegram token
    ↓
11. Router → אור: "בדוק שהסוכן עובד"
    ↓
12. אור: מריץ gmail_vip.py → ✅ עובד!
    ↓
13. Router → WF-002: "תעד החלטה על סוכן חדש"
    ↓
14. Claude Desktop מבצע commit סופי
    ↓
15. דיווח: ✅ סוכן VIP מוכן! [link + הוראות שימוש]
```

**זמן משוער**: 15-25 דקות  
**מעורבות אור**: 4-5 אישורים + 2 פעולות ידניות (OAuth + בדיקה)

---

## 🔌 איך Chat חיצוני מתחבר?

### **אופציה 1: ChatGPT Custom GPT**

**מה ChatGPT שולח**:
```json
{
  "intent": "בנה לי סוכן שבודק מיילים",
  "context": {
    "user": "אור",
    "urgency": "normal",
    "interactive": true
  }
}
```

**מה ChatGPT מקבל בחזרה**:
```json
{
  "status": "in_progress",
  "current_task": "Task 3/10: הגדרת OAuth",
  "next_action": "אור, אנא הגדר Gmail OAuth",
  "instructions": "[קישור למדריך]",
  "overall_progress": 30
}
```

**איך זה עובד**:
1. Custom GPT קורא ל-API endpoint: `POST /api/intents`
2. Intent Router מקבל ומפרק
3. כל משימה מחזירה status update
4. Custom GPT מציג התקדמות לאור
5. בסוף: קישור ל-commit + סיכום

---

### **אופציה 2: Telegram Bot**

**מה Telegram Bot שולח**:
```python
# Telegram message מאור
"/create_agent בדוק מיילים מVIP ושלח התראה"
```

**Bot מעביר ל-Intent Router**:
```json
{
  "intent": "בדוק מיילים מVIP ושלח התראה",
  "source": "telegram",
  "chat_id": 12345,
  "user": "אור"
}
```

**מה Bot מקבל בחזרה** (streaming):
```json
[
  {"task": 1, "status": "done", "message": "תכנון הושלם"},
  {"task": 2, "status": "in_progress", "message": "יוצר קבצים..."},
  {"task": 3, "status": "waiting", "message": "אור, צריך OAuth - לחץ כאן"},
  ...
]
```

**Bot מעדכן את אור ב-Telegram**:
```
🤖 סוכן VIP בתהליך בנייה...
✅ תכנון הושלם
✅ קבצים נוצרו
⏳ ממתין להגדרת OAuth - [לחץ כאן]
```

---

### **אופציה 3: Web UI (עתידית)**

**דף אינטרנט פשוט**:
```html
<input placeholder="מה לעשות?">
<button>בצע</button>

<div id="progress">
  Task 1/5: ✅ Done
  Task 2/5: ⏳ In Progress
  Task 3/5: ⏸️ Waiting for your input
</div>
```

**זרימה**:
1. אור מקליד intent
2. JavaScript שולח ל-`POST /api/intents`
3. SSE stream מחזיר updates בזמן אמת
4. UI מציג progress bar + הודעות

---

## 🛠️ מה צריך כדי ליישם?

### **שלב 1: Intent Router API** (Python)
```python
# ai_core/intent_router.py

def route_intent(intent: str) -> List[Task]:
    """מפרק intent לרשימת משימות"""
    tasks = []
    
    # ניתוח Intent
    if "סוכן" in intent and "מייל" in intent:
        tasks.append(Task("plan_agent", target="gpt_planner"))
        tasks.append(Task("create_files", target="claude"))
        tasks.append(Task("setup_oauth", target="manual"))
        # ...
    
    return tasks

def execute_tasks(tasks: List[Task]) -> Report:
    """מבצע משימות בזו אחר זו"""
    for task in tasks:
        if task.target == "gpt_planner":
            plan = call_gpt_planner(task)
        elif task.target == "claude":
            result = call_claude_desktop(task)
        elif task.target == "manual":
            wait_for_user_input(task)
    
    return Report(...)
```

### **שלב 2: API Endpoints** (Flask/FastAPI)
```python
# api/server.py

@app.post("/api/intents")
def create_intent(intent: Intent):
    router = IntentRouter()
    tasks = router.route_intent(intent.text)
    job_id = start_background_job(tasks)
    return {"job_id": job_id, "tasks": len(tasks)}

@app.get("/api/intents/{job_id}/status")
def get_status(job_id: str):
    return {"current_task": 3, "total": 10, "status": "in_progress"}
```

### **שלב 3: Chat Integrations**
- Custom GPT: Actions schema
- Telegram Bot: python-telegram-bot
- Web UI: React + SSE

---

## 📊 סיכום: מי עושה מה?

| שכבה | תפקיד | דוגמה |
|------|-------|--------|
| **Chat חיצוני** | קבלת intent מאור | "בנה סוכן Gmail" |
| **Intent Router** | פירוק + ניתוב | 10 משימות → GPT/Claude/Manual |
| **GPT Planner** | תכנון טכני | ארכיטקטורה + קוד |
| **Claude Desktop** | ביצוע | קבצים + git |
| **Workflows** | תהליכים קבועים | WF-001/002/003 |
| **MCPs** | גישה למערכות | Filesystem, Git, Gmail |
| **אור** | כוונה + אישור + בדיקה | ✅ / הגדר OAuth / בדוק |

---

## 🎯 סטטוס נוכחי

**Status**: ✅ **IMPLEMENTED v1.0** - Structured output with full parsing

**מה עובד עכשיו**:
- ✅ קובץ: `ai_core/intent_router.py`
- ✅ פונקציה ראשית: `route_intent(intent_text: str) -> Dict[str, Any]`
- ✅ מקבל intent טקסטואלי
- ✅ קורא ל-GPT Planner (`gpt_orchestrator.plan_change`)
- ✅ מחזיר dict מובנה עם JSON parsing
- ✅ GPT Planner מחזיר JSON מובנה (לא טקסט גולמי)

**פורמט תשובה נוכחי (v1.0)**:
```python
{
    "intent": str,                    # הכוונה המקורית
    "summary": str,                   # מה GPT הבין
    "context": str,                   # הקשר מ-SSOT
    "steps": List[str],               # רשימת צעדים
    "actions_for_claude": List[str],  # פעולות טכניות
    "decisions_for_or": List[str],    # מה אור מאשר
    "version": "1.0"                  # גרסת Router
}
```

**דוגמת שימוש**:
```python
from ai_core.intent_router import route_intent

result = route_intent("צור workflow חדש לגיבוי")

# קבל מבנה מלא
print(result["summary"])              # מה הבין GPT
print(result["steps"])                # רשימת צעדים
print(result["actions_for_claude"])  # מה Claude צריך לעשות
print(result["decisions_for_or"])    # מה אור מאשר
```

**שינויים מ-v0.1**:
- ✅ GPT Planner מחזיר JSON מובנה (לא Markdown)
- ✅ Parsing אוטומטי של התשובה
- ✅ מבנה מלא עם 5 סעיפים
- ✅ Error handling משופר (fallback למבנה)
- ✅ Type hints מעודכנים

**תלויות**:
- ✅ Python 3.8+
- ✅ `openai` package
- ✅ `OPENAI_API_KEY` ב-environment

---

## 🚀 הצעדים הבאים

### **Phase 1: בסיס** (1-2 שבועות)
1. ליישם `intent_router.py` בסיסי
2. לבדוק עם דוגמאות פשוטות
3. לתעד את ה-API

### **Phase 2: אינטגרציה** (2-3 שבועות)
1. ליצור API server (Flask)
2. לחבר ChatGPT Custom GPT
3. לבדוק end-to-end

### **Phase 3: הרחבה** (1 חודש)
1. Telegram Bot
2. Web UI
3. Monitoring + Logs

---

**הכיוון ברור! Intent Router יהיה השכבה שמעל הכל! 🚀**

---

**Document Status**: 📋 Design Phase  
**Version**: 1.0  
**Last Updated**: 2025-11-21  
**Next Review**: לאחר תחילת יישום Phase 1
