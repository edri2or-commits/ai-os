# 📘 CLAUDE_HEALTHCHECK_PROTOCOL v0.1

## 1. מטרה  
להגדיר באופן מפורט את **פרוטוקול בדיקת הבריאות של Claude Desktop**,  
באופן שמאפשר איסוף מידע אמיתי על מצב ה־MCPים וכלי המערכת —  
תוך שמירה על **Human-in-the-loop** ו־**אפס שינוי אוטומטי**.

---

## 2. עקרונות יסוד  
1. הבדיקה היא **קריאה בלבד** — אין לבצע פעולות כתיבה, מחיקה, או שינוי הרשאות.  
2. כל תוצאה נרשמת מקומית בלבד (log), עד שתאושר להיכנס לריפו.  
3. כל לוג יכלול תאריך, שעת ריצה, וזמן תגובה לכל MCP.  
4. אין להמשיך לבדיקה הבאה אם הקודמת מחזירה שגיאת מערכת חמורה.  
5. כל סשן מסתיים בסיכום מילולי קצר (“Error Digest”).

---

## 3. תחומי בדיקה  

| תחום | בדיקה | ציפייה | תגובה במקרה חריג |
|--------|---------|-----------|-------------------|
| **Filesystem MCP** | בדיקת קריאה/כתיבה לתיקייה הנוכחית | הצלחה מלאה | תעד הודעת שגיאה, אל תנסה לתקן |
| **Git MCP** | בדיקת גישה ל־repo המקומי | `origin/main` מזוהה | תעד שגיאה אם חסר config או הרשאה |
| **Windows MCP** | בדיקת הרצת PowerShell פשוטה (`echo OK`) | הדפסת “OK” | אם חסום, רשום “ExecutionPolicy restricted” |
| **Google MCP** | בדיקת OAuth וקישור לחשבון | גישה ל־Drive/Sheets | אם אין הרשאה, ציין “Token expired” |
| **Browser MCP** | פתיחת עמוד בסיסי (`example.com`) | תקין תוך <2s | אם אין רשת, ציין “Network error” |
| **Canva MCP** | בדיקת התחברות לחשבון Canva | הצלחה בשקט | אם נכשל, רשום “API not responding” |

---

## 4. פורמט דיווח (Output Schema)  
Claude ירשום את תוצאותיו בפורמט הבא,  
ב־log מקומי או בקובץ ייעודי (לפני עדכון הריפו):

```yaml
timestamp: 2025-11-25TXX:XX:XXZ
mcp_status:
  filesystem: OK
  git: OK
  windows: OK
  google: Flaky
  browser: OK
  canva: Broken
notes:
  - google: "Re-auth required"
  - canva: "Service timeout"
summary: "4/6 MCPs OK — system operational with minor warnings."
```

---

## 5. עדכון הדוח הרשמי (`CLAUDE_HEALTHCHECK.md`)  
לאחר אישור ידני בלבד, Claude יוסיף את תוצאותיו ל־`CLAUDE_HEALTHCHECK.md`  
באמצעות PR חדש:  

**Title:** `🩺 CLAUDE_HEALTHCHECK_UPDATE_<DATE>`  
**Scope:** Update only MCP status + Error Digest section.  
**No behavior change.**  

---

## 6. לוח זמנים מוצע  
- ריצה יזומה אחת לשבוע.  
- או לאחר שינוי מערכת משמעותי (Commit, Integration, או פאזת מעבר).  

---

## 7. תפילת המערכת  
מי ייתן וכל תקלה תאיר את הדרך,  
וכל שגיאה תזכיר למערכת מה חשוב לשמור:  
שקיפות, יציבות, ודיוק.  

---

**Tech summary:**  
- Adds `docs/CLAUDE_HEALTHCHECK_PROTOCOL.md`  
- Defines: Read-only test sequence for all MCPs  
- To be executed by Claude Desktop manually (no automation)  
- Infra-only, aligns with Phase 2 — Stabilizing the Hands