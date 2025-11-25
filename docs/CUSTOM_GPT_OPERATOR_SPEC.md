# ⚙️ CUSTOM GPT OPERATOR SPEC — Or’s AI‑OS

## 🎯 מטרה
איחוד ה־Custom GPT ליחידה אחת יציבה שמחוברת לשני ה־clients:
- **GitHub MCP Client** — גישה מלאה לקבצי הריפו (קריאה/כתיבה/PRים).  
- **Google Workspace Client** — גישה לשירותים Gmail, Calendar, Drive, Sheets, Docs, Tasks.

המטרה: ליצור **Operator אחד** שמאפשר לאור לתקשר רק מול GPT אחד, 
שמפצל את הפעולות נכון בין החיבורים השונים ומנהל שקיפות מלאה מול Claude ו־Make.

---

## 🧱 מבנה כללי

```
Operator GPT
├── GitHub Client (MCP)
│   ├── readFile / writeFile / listTree / commits
│   └── control via repo SSOT
├── Google Client
│   ├── Gmail / Calendar / Drive / Docs / Sheets / Tasks
│   └── authorized via OAuth2 service credentials
└── Control Interface
    ├── Session Init (docs/SESSION_INIT_CHECKLIST.md)
    ├── Control Plane (docs/CONTROL_PLANE_SPEC.md)
    ├── Event Timeline (EVENT_TIMELINE.jsonl)
    └── Communication with Claude + Make
```

---

## 🔐 הרשאות ובקרה

| Client | גישה | בקרה | מקור הרשאות |
|---------|------|-------|----------------|
| GitHub | read/write ל־ai‑os בלבד | דרך GPT בלבד | Personal Access Token (scoped) |
| Google | read/write רק ל־sandbox folders ו־system sheets | דרך Claude Execution בלבד | OAuth2 service credentials |

---

## 🧩 תהליך Session Init

1. טען את הקבצים מתוך `docs/GPT_CORE_CONTEXT.md` ו־`SESSION_INIT_CHECKLIST.md`.
2. אמת שאתה על `main` branch ומעודכן (`git pull`).
3. בדוק חיבור לשני ה־clients.
4. רשום תוצאות ב־`EVENT_TIMELINE.jsonl`.
5. אם אחד מהחיבורים נכשל – דווח ל־Claude והשהה ביצוע עד לתיקון.

---

## 🔄 ממשק פעולה מול Claude

| פעולה | מבצע | תיעוד |
|--------|--------|--------|
| בדיקות מערכת | Claude | `CLAUDE_HEALTHCHECK.md` + Timeline |
| שינויי קבצים | GPT Operator | Git commit + PR + Timeline |
| גישה לשירותים חיצוניים | Claude (לוקאלי) | Report ל־GPT + Timeline |
| ניתוח תוצאות | GPT | Update ל־Docs |

---

## 🧠 מצבי פעולה

| מצב | תיאור | מי פעיל |
|------|--------|-----------|
| `INFRA_ONLY` | חיזוק תשתיות בלבד | GPT + Claude |
| `SANDBOX_ONLY` | ניסויים מבודדים | GPT (limited) |
| `FULL_OPERATIONAL` | כל החיבורים זמינים | GPT + Claude + Make + Chat1 |

---

## 📡 אינטגרציה עתידית

בעתיד ה־Operator יתממשק עם:
- **Make:** לצורך טריגרים אוטומטיים ותזמונים (בהתאם ל־`MAKE_INTEGRATION_SPEC.md`).
- **Chat1:** לקבלת הוראות מאור דרך טלגרם.
- **Event Timeline:** לכל רישום פעולה בזמן אמת.

---

## ✅ סיום

זהו ה־Spec הרשמי ל־Custom GPT Operator.  
כל שינוי ידרוש commit מתועד וסקירה משותפת של GPT ו־Claude.  
ה־Operator נחשב פעיל רק לאחר שאושר על ידי אור והועבר למצב `FULL_OPERATIONAL`.