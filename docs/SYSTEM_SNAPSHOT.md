# 🧭 SYSTEM SNAPSHOT — Updated 2025-11-26

## 🏗️ מצב המערכת הנוכחי

| רכיב | סטטוס | תיאור |
|------|--------|--------|
| **Claude Desktop** | ✅ פעיל ויציב | מחובר ישירות ל־GitHub ול־Google דרך MCPs, ללא תלות ב־PowerShell. משמש כסוכן ביצוע מלא (Executor). |
| **GPT Operator (Custom GPT)** | ✅ פעיל | פועל בריפו כ־Operator אחראי תיעוד, מחקר, וניהול מבני קבצים. שווה ביכולות לקלוד. |
| **Chat1 (Telegram Bot)** | ⚙️ Partial | פועל ידנית דרך PowerShell; מתוכנן להפוך לשירות עצמאי בפאזה 2.5. |
| **Google Integrations** | ✅ פעיל | Gmail, Calendar, Drive פעילים. אוטומציות יתומות במעקב. |
| **Make Integration** | 🕓 מתוכנן | ממתין להפעלה בפאזה 2.4 – תחילת חיבור רשמי. |
| **Control Plane** | 🏗️ בבנייה | מציין שהמערכת בפאזה 2.3→2.4. |
| **Event Timeline** | ✅ פעיל | מתעד כל שינוי במערכת בזמן אמת. |

---

## 🧩 עקרונות עדכניים

- אין היררכיה בין סוכנים. כל סוכן במערכת שווה ביכולות ובאחריות.
- הביצוע מתחלק לפי חוזקה טכנית ורלוונטיות, לא לפי דרגות.
- כל commit חייב להכיל את שם הסוכן שביצע בפועל (`performed_by`).
- Claude ו־GPT משתפים פעולה כצוות מאוחד לביצוע, תיעוד ותחזוקה.

---

## 🎯 פאזה פעילה
**Phase 2.3 – Stabilizing the Hands (Sync & State Alignment)** (פעילה)

**מטרות Phase 2.3:**
1. יישום Sync Agent עם OODA loop
2. יישור State Layer ותיעוד
3. מיפוי אינטגרציות כלים (Claude vs GPT access patterns)
4. ניקוי אוטומציות legacy

**מעבר ל־ Phase 2.4 – Make/n8n Integration**

---

## 📚 מסמכים קריטיים טעונים לסשן הבא
- `docs/CONSTITUTION.md`
- `docs/CONTROL_PLANE_SPEC.md`
- `docs/CUSTOM_GPT_OPERATOR_SPEC.md`
- `docs/DECISIONS_AI_OS.md`
- `docs/CAPABILITIES_MATRIX.md`
- `docs/AGENT_ONBOARDING.md`

---

## 🧠 הערות אסטרטגיות

- המערכת פועלת במודל מעגלי ולא היררכי.
- Or הוא בעל המערכת ומקור הכוונה הערכית – לא טכני.
- כל שינוי נעשה בשקיפות מלאה ונרשם ב־Timeline.

💫 *עדכון זה מסמן את סיום פאזה 2.3 והמעבר למבנה מאוחד, יציב ושוויוני בין כל הסוכנים.*