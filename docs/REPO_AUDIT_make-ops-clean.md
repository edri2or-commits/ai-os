# make-ops-clean – Repo Audit (20 Nov 2025)

## סקירה כללית

ריפו make-ops-clean נראה כמו מרכז שליטה והפעלה עבור מערך סוכני AI וזרימות אוטומציה. הוא כולל שילוב בין הגדרות תיעוד (DOCS, docs), מסמכי החלטות ותוכניות, קוד לסוכנים (agents/gpt_agent), כלים לאינטגרציה מול GitHub וממשקי GPT, מודול ״Master Control Program״ (mcp) וזרימות אוטומציה/תפעול (OPS/ops, automation). בנוסף יש קונפיגורציות, מדיניות אבטחה ומסמכים המתארים יכולות, תהליכים וחוקים. במילים אחרות, זהו מאגר שמרכז ידע, תיעוד וקוד להפעלת מערכת מרובת סוכנים, עם דגש על תהליכים, תאימות ואוטומציה.

## טבלת קבצים ותיקיות חשובים

| Path | Type | Role (מה עושה) | Status | SuggestedTarget (ב־ai‑os) |
|------|------|----------------|--------|---------------------------|
| DOCS/ | Directory | תיעוד ברמה גבוהה: מדריכים, הנחיות וחוקים כלליים. | זהב | docs/ |
| docs/ | Directory | תיעוד נוסף; ייתכן גרסאות ניסוי/עבודה של מסמכים או סקציית תיעוד חדשה. | ניסוי/ישן | docs/ |
| RUNBOOKS/ | Directory | "Runbooks" – מדריכי הפעלה לטיפול בתקלות ותהליכים. | זהב | workflows/ |
| decisions/ | Directory | יומני החלטות, ADRs (Architectural Decision Records). | זהב | docs/ |
| plans/ | Directory | תוכניות פעולה/מפת דרכים לפרויקט ולעתיד. | זהב | docs/ |
| agents/ | Directory | קוד הגדרה והרצה של סוכנים כלליים במערכת. | זהב | agents/ |
| gpt_agent/ | Directory | מודול של סוכן GPT ספציפי (עוטף מודלים, פרומפטים וכו'). | זהב | agents/ |
| gpt-api/ | Directory | מעטפת ל‑API של GPT או שירותים חיצוניים; ייתכן מכיל wrappers וכלי חיבור. | זהב | tools/ |
| mcp/ | Directory | "Master Control Program" – הלב של המערכת: תכנון, תזמון, ניהול סוכנים וזרימות. | זהב | workflows/ |
| mcp-servers/ | Directory | הגדרות או קוד ספציפי לשרתים המפעילים MCP; ייתכן חומר היסטורי או ניסיוני. | לא ברור | archive/ (דורש סבב נוסף) |
| config/ | Directory | קבצי קונפיגורציה (yaml/json) המגדירים סוכנים, כלים ותהליכים. | זהב | policies/ |
| automation/ | Directory | סקריפטים לזרימות אוטומטיות (Makefile, Cron, תזמונים). | זהב | workflows/ |
| github_integration/ | Directory | קוד אינטגרציה מול GitHub – hooks, API wrappers, אוטומציות למאגרים. | זהב | tools/ |
| OPS/ | Directory | תיקיית תפעול (operation procedures); מסמכי runbook/מדיניות. | זהב | workflows/ |
| ops/ | Directory | מודול קוד לתהליכי תפעול ואוטומציה; כנראה מימוש של ״Ops" ב־Python/Make. | זהב | workflows/ |
| STATE_FOR_GPT/ | Directory | מצבי עבודה/סנאפ־שוטים שנשמרו עבור GPT; דטא ריצה. | ניסוי/ישן | archive/ (לא להעמיק עכשיו) |
| security/ | Directory | קבצים הקשורים למדיניות אבטחה, הרשאות, אולי רוטינות סינון. | זהב | policies/ |
| knowledge/ | Directory | מאגר ידע ומסמכים המציגים עקרונות, לקחים וחוקים. | זהב | docs/ |
| README.md | md | תיאור ראשוני של הפרויקט ומה מטרתו, שימושים ואיך להפעיל. | זהב | docs/ |
| DECISION_LOG.md | md | יומן החלטות מרכזי שמתעד החלטות בפרויקט. | זהב | docs/ |
| CAPABILITIES_MATRIX.md | md | טבלת יכולות של הסוכנים/מערכת; מתאר איזה כלים קיימים ואיך הם מחולקים. | זהב | docs/ |
| BRIDGE_PROPOSAL.md | md | הצעת גשר/אינטגרציה בין מערכות (למשל בין GPT ל‑MCP); מסמך אסטרטגי. | זהב | docs/ |
| WINDOWS_MCP_SAFETY_POLICY.md | md | מסמך מדיניות בטיחות להפעלת MCP בסביבת Windows. | זהב | policies/ |
| CURRENT_STATE.md | md | תיאור המצב הנוכחי של המערכת, גרסת סנאפ־שוט. | ניסוי/ישן | docs/ |
| GITHUB_ACTIONS_TRIGGER_BUG.md | md | תיעוד באג בהפעלת GitHub Actions – נועד לשחזור/פתרון. | ניסוי/ישן | archive/ |
| GOOGLE_MCP_AUTOMATION_PLAN.md | md | תכנון אוטומציה עבור MCP בגוגל (למשל Cloud Run); מסמך ארכיטקטורה. | זהב | docs/ |
| MCP_GPT_CAPABILITIES_BRIDGE.md | md | גשר יכולות בין MCP למודלי GPT – הגדרות ונהלים. | זהב | docs/ |
| MCP_WINDOWS_SHELL_DESIGN.md | md | עיצוב shell ל‑MCP ב‑Windows – מפרט טכני. | זהב | docs/ |
| MCP_WINDOWS_SHELL_HEALTHCHECK.md | md | הוראות וקריטריונים לבדיקות בריאות (healthchecks) של MCP ב‑Windows. | זהב | docs/ |
| PHASE2_TOOLS_DEFINITIONS.md | md | הגדרות כלים לשלב 2 בפרויקט – אילו כלים יש וכיצד הם משתלבים. | זהב | docs/ |
| SYSTEM_STATUS.md | md | מדדים וסטטוס של תתי־מערכות במצב נתון. | ניסוי/ישן | docs/ |
| TEST_PLAN.md | md | תוכנית בדיקות למערכת. | זהב | docs/ |
| WINDOWS_SHELL_MCP_SPRINT_SUMMARY.md | md | סיכום ספרינט בפיתוח ה‑MCP Shell ל‑Windows. | ניסוי/ישן | archive/ |
| קבצי Python ו־JSON נוספים כמו autopilot.py, autopilot-state.json, hello.py, vercel.json | py/json | סקריפטים וקבצי תצורה להפעלת מודולים (טייס אוטומטי, בדיקות, הגדרות ענן). | ניסוי/ישן | tools/ או archive/ בהתאם לחשיבות (דורש סבב נוסף) |
| תיקיות logs/, demo/, playground/, cleanup/, debug/, cloud-run/, jobs/, scripts/ | Directory | תיקיות תומכות לניסויים, הדגמות, ניקוי, רישום לוגים ו־CI/CD. | ניסוי/ישן | archive/ |
| תיקייה SECRETS/ | Directory | תוכן רגיש כמו טוקנים או סודות; לא נפתח. | זהב | archive/ (להישמר ולא לפתוח) |

## דברים שדורשים החלטה אנושית / סבב נוסף

1. **בדיקת עומק של תיקיות mcp-servers/, STATE_FOR_GPT/ ו־קבצי json/py** – לא בדקנו את התוכן כדי לא להיחשף למידע רגיש. מומלץ לעבור על כל קובץ שם ולהחליט אם הוא חיוני או ניתן לארכוב.

2. **הבדלים בין DOCS/ ל־docs/** – ייתכן שיש כפילות או גרסאות שונות של אותם מסמכים. צריך לבחור מקור אחד ולאחד תכנים.

3. **חפיפה בין OPS/ ל־ops/** – ייתכן שמדובר בגרסה חדשה לעומת ישנה; נדרש איחוד או העברה מתאימה.

4. **שכבות קונפיגורציה ובקרות** – מומלץ לבדוק את תיקיית config/ ולשלב חוקים ברורים על הרשאות והרמת כלים לפני העברת הקבצים.
