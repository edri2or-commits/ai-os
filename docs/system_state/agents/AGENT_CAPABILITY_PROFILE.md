# AGENT_CAPABILITY_PROFILE.md — פרופיל יכולות ממשקים

**Version:** 0.2  
**Created:** 2025-11-26  
**Last Updated:** 2025-11-26 (Block ROLE_MODEL_SIMPLIFICATION_V1)  
**Purpose:** תיאור יכולות ומגבלות טכניות של ממשקי AI-OS

---

## 🎯 מודל המערכת

**AI-OS** = מערכת אחת משולבת המורכבת מכלל הסוכנים, הכלים והשירותים.

**Interfaces (ממשקים):**
- Claude Desktop
- GPT (ChatGPT)
- Chat1 / Telegram (עתידי)

כל ממשק יכול לשמש **גם לתכנון וגם לביצוע**, בהתאם ליכולות הטכניות הזמינות באותו רגע.

**Or:**
- בעל המערכת
- מקור הכוונה והעדיפויות
- מאשר פעולות משמעותיות/מסוכנות
- יכול לעבוד גם ישירות עם הכלים אם רוצה

**אין היררכיה קשיחה.** אין "X תמיד מתכנן" או "Y רק מבצע". יש יכולות טכניות שונות, וכל ממשק משתמש במה שזמין לו.

---

## 📊 ממשקים זמינים

### Claude Desktop

**יכולות טכניות:**
- ✅ גישת MCP מלאה: GitHub, Filesystem, Windows, Google (read-only), Canva, Browser
- ✅ גישה ישירה לריפו מקומי: `C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace`
- ✅ פעולות Git: clone, commit, push (עם אישור)
- ✅ שליטה במערכת Windows: PowerShell, UI automation
- ✅ יצירה ועריכה של מסמכים: Word, PowerPoint, Excel, PDF
- ✅ עדכון State Layer: EVENT_TIMELINE, SERVICES_STATUS, INFRA_MAP

**מגבלות בטיחות:**
- ❌ אין push ל-remote ללא אישור מפורש מ-Or
- ❌ אין deployment אוטונומי של שירותים
- ❌ אין שינוי CONSTITUTION.md ללא אישור מפורש מ-Or
- ❌ אין write ל-Google (רק read דרך MCP)

**מתי נוח להשתמש:**
- כשצריך גישה לקבצים מקומיים
- כשצריך להריץ קוד או PowerShell
- כשצריך לעדכן את הריפו
- כשצריך לעבוד עם Windows

---

### GPT (ChatGPT)

**יכולות טכניות:**
- ✅ גישה ל-Google Workspace (דרך Custom Actions): Gmail, Calendar, Drive, Docs, Sheets, Tasks
- ✅ גישה ל-GitHub (דרך Custom Actions): read/write files, branches, commits, PRs
- ✅ תכנון ועיצוב ברמה גבוהה
- ✅ כתיבת Specs ותיעוד
- ✅ גישה ל-Drive Snapshot (כשזמין)

**מגבלות טכניות:**
- ❌ אין גישת MCP (בינתיים)
- ❌ אין גישה ישירה לריפו מקומי
- ⚠️ תלוי ב-ngrok tunnel לחיבור לשירותים מקומיים

**מגבלות בטיחות:**
- 🔐 כל כתיבה חייבת להיות logged ב-EVENT_TIMELINE

**מתי נוח להשתמש:**
- כשצריך לעבוד עם Google Workspace
- כשצריך תכנון אסטרטגי ברמה גבוהה
- כשצריך לנתח ולתעד
- כשצריך נגישות מכל מקום (לא רק מהמחשב המקומי)

---

### Chat1 Telegram Bot

**יכולות טכניות:**
- ✅ קבלת intents בשפה טבעית (עברית)
- ✅ הצגת תוכניות עם כפתורי אישור (✅/❌)
- ✅ ניתוב ל-Agent Gateway
- ✅ אכיפת Human-in-the-loop

**מגבלות טכניות:**
- ⚠️ לא deployed באופן קבוע - דורש הפעלה ידנית
- ⚠️ מוגבל לממשק Telegram
- ⚠️ תלוי ב-TELEGRAM_BOT_TOKEN ו-OPENAI_API_KEY

**מגבלות בטיחות:**
- ❌ לא מבצע בלי אישור - UI בלבד

**מתי נוח להשתמש:**
- כשצריך לתקשר מהטלפון
- כשצריך ממשק עברי פשוט
- כשצריך אישור מהיר על תוכניות

**סטטוס:** הקוד מוכן ב-`chat/telegram_bot.py` אבל לא רץ כ-service כרגע.

---

## 🔐 מגבלות בטיחות (חלות על כולם)

אלה מגבלות שחלות על **כל** ממשק, ללא קשר למי משתמש בו:

1. **No push without approval** - אין push ל-remote ללא אישור מפורש מ-Or
2. **INFRA_ONLY constraints** - ב-Phase 2, אין אוטומציות חיות על החיים של Or
3. **Human-Approved Writes** - כל כתיבה חייבת logging ב-EVENT_TIMELINE + commit message ברור
4. **No CONSTITUTION changes** - שינויים ב-CONSTITUTION רק עם אישור מפורש
5. **Transparency** - כל שינוי גלוי, ניתן להסבר ומתועד

---

## 🔄 תקשורת בין ממשקים

אין פרוטוקול קשיח של "מי מדבר עם מי". כל ממשק יכול:
- לבקש מידע מ-State Layer (AGENT_SYNC_OVERVIEW, INFRA_MAP, וכו')
- לעדכן State Layer אחרי שינויים משמעותיים
- לתאם עם Or לגבי המשך העבודה

**העקרון:** המערכת גמישה. אם אתה צריך עזרה - תבקש. אם אתה יכול לעשות משהו - תעשה (בכפוף למגבלות בטיחות).

---

## 📝 מסמכים קשורים

- **Constitution:** `docs/CONSTITUTION.md`
- **Control Plane:** `docs/CONTROL_PLANE_SPEC.md`
- **System Snapshot:** `docs/SYSTEM_SNAPSHOT.md`
- **Session Init:** `docs/SESSION_INIT_CHECKLIST.md`

---

**Last Updated:** 2025-11-26  
**Updated By:** Claude Desktop (Block ROLE_MODEL_SIMPLIFICATION_V1)
