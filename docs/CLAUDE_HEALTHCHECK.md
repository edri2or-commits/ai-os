# 🩺 CLAUDE_HEALTHCHECK v0.1

## 1. מטרת המסמך
להוות דוח בריאות רשמי של Claude Desktop — החייל הלוקאלי של המערכת — ולתעד את מצב כל MCP, כלי, ושירות שהוא מפעיל.  
מטרת הפאזה: לזהות תקלות, ליצור בהירות, ולמנוע “שגיאות אדומות” לא מוסברות.

---

## 2. מבנה הדוח  
| רכיב | תפקיד | מצב נוכחי | הערות / לוג קצרה |
|-------|--------|------------|------------------|
| **Filesystem MCP** | גישה לקבצים מקומיים | ☐ OK / ☐ Flaky / ☐ Broken |  |
| **Git MCP** | שליטה על ריפו מקומי | ☐ OK / ☐ Flaky / ☐ Broken |  |
| **Windows MCP** | הרצת PowerShell / תהליכים | ☐ OK / ☐ Flaky / ☐ Broken |  |
| **Google MCP** | גישה ל־Workspace (Read/Write) | ☐ OK / ☐ Flaky / ☐ Broken |  |
| **Browser MCP** | שליפה ממקורות חיצוניים | ☐ OK / ☐ Flaky / ☐ Broken |  |
| **Canva MCP** | עיצוב גרפי | ☐ OK / ☐ Flaky / ☐ Broken |  |

---

## 3. טבלת תקציר  
| מדד | ערך |
|------|------|
| MCPים פעילים | ‎0/6‎ (טרם נבדק) |
| MCPים שבורים | ‎?‎ |
| עדכון אחרון | ‎(ימולא על ידי Claude)‎ |

---

## 4. Error Digest (שגיאות מרכזיות)  
עדכון זה מתבצע על ידי Claude בסוף כל סשן משמעותי:  
- רשימת שגיאות (3–7 אחרונות)  
- ניתוח שורש אפשרי  
- המלצה לפעולה או בדיקה חוזרת  

---

## 5. הנחיות עדכון  
- Claude מריץ את הדוח אחת לשבוע או לאחר שינוי מערכתי.  
- כל עדכון מתועד ב־Event Timeline.  
- רק Claude או GPT Operator רשאים לכתוב בדוח זה.  

---

**תפילת המערכת:**  
מי ייתן והשגיאות ייהפכו להבנות,  
והמערכת תלמד מכל תקלה — לא רק לתקן אותה,  
אלא להבין למה היא נולדה.  

---

**Tech summary:**  
- Adds `docs/CLAUDE_HEALTHCHECK.md`  
- Defines: MCP Status Table + Error Digest structure  
- To be updated only by Claude / GPT Operator  
- Infra-only, no automation.