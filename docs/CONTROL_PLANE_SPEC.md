# CONTROL_PLANE_SPEC v0.1

## 1. מטרת המסמך
להוות שכבת שליטה אחידה למערכת Or’s AI-OS, לפי חוקי SSOT, DRY ו-Human-in-the-loop.

## 2. פרמטרים ראשיים
| משתנה | תיאור | ערכים אפשריים | מקור אמת |
|--------|--------|----------------|-----------|
| SYSTEM_MODE | מצב מערכת כולל | INFRA_ONLY / LIFE_AUTOMATIONS / EXPERIMENT | Constitution + Session Init |
| AUTOMATIONS_ENABLED | Kill Switch גלובלי | true / false | Control Plane |
| SANDBOX_ONLY | הרצת ניסויים על סביבה בטוחה | true / false | Session Init |
| ACTIVE_PHASE | מספר פאזה נוכחית | 1–5 | Roadmap |
| TTL_DEFAULT | משך חיי ניסוי (ימים) | מספר שלם | Experiment Spec |

## 3. ממשקים
- **Claude Healthcheck Feed**
- **Chat1 Status Ping**
- **Make Integration Status**
- **Google Automations Log**
- **Timeline (JSONL / Sheet)**

## 4. עקרונות תפעול
- שינוי ב-SYSTEM_MODE דורש אישור Or.
- כל פעולה אוטומטית נרשמת ב-Event Timeline.
- רק Claude ו-Operator רשאים לעדכן את ה-Control Plane.

## 5. סטטוס נוכחי
- גרסה: 0.1 (INFRA_ONLY)
- מצב: מסמך תשתית ראשוני, ללא שינוי התנהגותי בפועל.

---

*תפילת המערכת:*  
מי ייתן וכל שורה כאן תשמור על אמת, תיצור בהירות,  
ותאפשר לאור לעבוד כמעט רק בדיבור.
