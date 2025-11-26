# AI-OS – החלטות ליבה (Core Decisions)

**מטרת המסמך**: תיעוד החלטות אסטרטגיות וארכיטקטוניות במערכת AI-OS.

**פורמט**: כל החלטה מתועדת עם תאריך, הקשר, החלטה ורציונל.

---

## 2025-11-20 – החלטה #1: MCP Orchestration

### הקשר
מערכת ה-MCP (Master Control Program) בריפו הישן `make-ops-clean` היא מערכת מורכבת לניהול סוכנים, תזמון ואינטגרציות. היא כוללת:
- `mcp/server/` - שרת מרכזי
- `mcp/clients/` - לקוחות (web, iOS shortcuts)
- `mcp/github/` - אינטגרציית GitHub
- `mcp/google/` - אינטגרציית Google

**שאלה**: האם לייבא את MCP כקוד רץ ל-AI-OS?

### ההחלטה
**MCP לא נלקח כקוד רץ ל-AI-OS.**

- **סטטוס**: 🗄️ Legacy / Reference Only
- **שימוש**: משמש כמקור עיצוב וידע בלבד
- **אין**: פריסה, הפעלה, או שימוש אקטיבי בקוד

### רציונל

**למה לא לייבא?**
1. **מורכבות גבוהה**: MCP התפתח אורגנית ויש בו רבדים רבים שלא לגמרי מתועדים.
2. **תלות בתשתית**: הוא נבנה סביב תשתית ספציפית (Cloud Run, Workflows) שלא בהכרח נחוצה ב-AI-OS.
3. **עקרון Data-First**: AI-OS נבנה מאפס עם עקרונות נקיים. עדיף לבנות תשתית פשוטה ומסודרת.

**מה כן לוקחים?**
- **תובנות עיצוב**: איך MCP פתר בעיות של תזמון, אינטגרציות, וניהול סוכנים.
- **דפוסי עבודה**: מה עבד טוב, מה לא.
- **מסמכי תיעוד**: כולם עברו לריפו כחומר עיון.

**מה במקום?**
- בעתיד, אם נזדקק למנגנון orchestration - נבנה אחד פשוט ומודולרי מאפס.
- כרגע: אין צורך במנגנון מרכזי. הסוכנים פועלים בנפרד.

### השפעה על CAPABILITIES_MATRIX
- **MCP-001**: MCP Orchestration → 🗄️ Legacy (Reference Only)
- **MCP-002**: MCP GitHub Integration → 🗄️ Legacy (Reference Only)
- **MCP-003**: MCP Google Integration → 🗄️ Legacy (Reference Only)

---

## 2025-11-20 – החלטה #2: GitHub Executor API

### הקשר
בריפו הישן קיים קוד מלא של `github-executor-api` - שירות Cloud Run שמספק API לאוטומציה של GitHub. הקוד:
- ממוקם ב-`cloud-run/google-workspace-github-api/`
- מכיל 2 endpoints: health check + update file
- מתוכנן ל-deployment ב-Cloud Run
- **בעיה**: Deployment חסום (חסר GitHub PAT, בעיות config)

**שאלה**: האם לפרוס את הקוד הקיים ב-AI-OS?

### ההחלטה
**הקוד הקיים לא נפרס ולא מופעל.**

- **סטטוס**: 📋 Designed (Not Deployed)
- **שימוש**: משמש כ-Blueprint / Design Reference בלבד
- **אין**: פריסה, הפעלה, או ניסיון לתקן את הקוד הקיים

### רציונל

**למה לא לפרוס?**
1. **תוכנן למערכת אחרת**: הקוד נבנה עבור `make-ops-clean` עם דרישות ספציפיות.
2. **בעיות deployment לא פתורות**: חסר PAT, יש באגים (typo ב-Accept header), לא ברור מה הסטטוס.
3. **בטיחות**: אין לנו שכבות פיקוח ואבטחה מספיקות להפעלת Executor אוטומטי.
4. **עקרון Thin Slices**: עדיף לבנות אוטומציה הדרגתית ומבוקרת.

**מה כן לוקחים?**
- **העיצוב**: איך הוא חשב על endpoints, authentication, path validation.
- **הלקחים**: מה הבעיות שהוא ניסה לפתור.
- **ה-Blueprint**: אם בעתיד נחליט לבנות Executor - נשתמש בו כנקודת התחלה.

**מה במקום?**
- כרגע: **אין אוטומציה של כתיבה ל-GitHub**.
- בעתיד: אם נצטרך Executor - נבנה אחד מאפס, עם שכבות בטיחות ברורות.

### השפעה על CAPABILITIES_MATRIX
- **GH-005**: GitHub Executor API → 📋 Designed (Not Deployed) - Reference Only

---

## 2025-11-20 – החלטה #3: GitHub Safe Git Policy

### הקשר
במערכת AI-OS יש מספר ממשקים (Claude Desktop, GPT, Chat1) שיכולים לגשת ל-GitHub ולבצע פעולות שונות. צריך מדיניות בטיחות אחידה שחלה על כולם.

**שאלה**: מה כללי הבטיחות לכתיבה ל-GitHub?

### ההחלטה
**Safe Git Policy - PR-First Approach**

- **סטטוס**: ✅ Active - חל על כל הממשקים
- **כלל מרכזי**: PR-first approach - אין push ישיר ל-main ללא אישור מפורש מאור
- **חל על**: Claude Desktop, GPT, Chat1, וכל ממשק עתידי

### רציונל

**למה PR-first?**
1. **בטיחות**: כל שינוי עובר review לפני merge ל-main
2. **שקיפות**: כל שינוי גלוי ומתועד
3. **Rollback**: אפשר לבטל שינויים בקלות
4. **Human-in-the-loop**: אור מאשר כל שינוי משמעותי

**המדיניות:**
1. כל ממשק יכול ליצור commits מקומיים
2. כל ממשק יכול ליצור PRs (Pull Requests)
3. רק אור מאשר merge ל-main
4. Push ישיר ל-main רק עם אישור מפורש מאור

**אין היררכיה:**
- אין "GPT = תכנון בלבד" או "Claude = ביצוע בלבד"
- יש רק יכולות טכניות שונות + אותן מגבלות בטיחות

### השפעה על המערכת
- כל הממשקים כפופים לאותה מדיניות Git
- אין "DRY RUN" לממשק אחד ו-"Full Write" לאחר
- יש capabilities שונות אבל constraints זהים

---

## 2025-11-20 – החלטה #4: סיום Phase 1 (Foundation) של AI-OS

### הקשר
במהלך התקופה האחרונה בנינו ריפו חדש בשם `ai-os` שנועד להיות ה-SSOT של מערכת ההפעלה האישית ל-AI (AI-OS).

**נוצרו**:
- **README** חדש ומפורט (420 שורות)
- **מסמכי ליבה** (5 מסמכים):
  - `CONSTITUTION.md` - 9 חוקי יסוד
  - `SYSTEM_SNAPSHOT.md` v2 - צילום מצב מקיף
  - `CAPABILITIES_MATRIX.md` v1.1 - 22 יכולות מתועדות
  - `DECISIONS_AI_OS.md` - לוג החלטות (המסמך הזה)
  - `REPO_AUDIT_make-ops-clean.md` - אודיט מלא של הריפו הישן
- **מיפוי סוכנים** (2 מסמכים):
  - `AGENTS_INVENTORY.md` - 8 סוכנים ממופים
  - `GPT_GITHUB_AGENT.md` - תיעוד מלא של סוכן ליבה #1
- **מיפוי כלים**:
  - `TOOLS_INVENTORY.md` - 24 כלים ואינטגרציות
- **מדיניות אבטחה**:
  - `SECURITY_SECRETS_POLICY.md` - מדיניות מקיפה (720 שורות)
- **שני Workflows רשמיים**:
  - `WF-001` – GITHUB_PLANNING_DRY_RUN (570 שורות)
  - `WF-002` – DECISION_LOGGING_AND_SSOT_UPDATE (737 שורות)

**שאלה**: האם Phase 1 (Foundation) הושלם? האם המערכת מוכנה לשימוש?

### ההחלטה
**Phase 1 – Foundation של AI-OS נחשב הושלם.**

- **סטטוס**: ✅ Phase 1 Complete - System Ready for Controlled Use
- **מכאן והלאה**:
  - `ai-os` הוא **מקור האמת היחיד** (SSOT) לתיעוד, יכולות, סוכנים, כלים ומדיניות
  - המערכת מוכנה לשימוש **מבוקר** בחיים האמיתיים
  - כל שינוי מהותי חדש יעבור דרך אחד מה-Workflows הרשמיים (לפחות WF-001 או WF-002)
- **אין**: שימוש production אוטומטי, סוכנים אוטונומיים עם כתיבה, פעולות לא מפוקחות

### רציונל

**למה Phase 1 הושלם?**

1. **כיסוי תיעודי חזק**:
   - יש חוקה (9 עקרונות)
   - יש צילום מצב מלא
   - יש מפת יכולות (22 יכולות)
   - יש לוג החלטות (4 החלטות כולל זו)

2. **תיעוד ברור של רכיבים**:
   - סוכן ליבה מתועד (GPT GitHub Agent)
   - 24 כלים ממופים
   - 8 סוכנים מסווגים
   - יכולות ברורות לכל רכיב

3. **מדיניות אבטחה**:
   - מדיניות מקיפה לסיקרטים (720 שורות)
   - זיהוי אזורים רגישים (SECRETS/, config/)
   - כללים ברורים לכל סוכן/כלי
   - תהליכי מיגרציה ו-incident response

4. **Workflows מגינים**:
   - WF-001: הגנה על שינויי GitHub (DRY RUN)
   - WF-002: הגנה על החלטות + סנכרון SSOT
   - Human-in-the-loop על כל פעולה קריטית

5. **מיפוי סיכונים**:
   - כל כלי מסווג לפי Risk Level
   - זיהוי Unknown Tools (Make, Telegram, GitHub Actions)
   - תוכנית ברורה לטיפול באבטחה

**מה הושג?**
- ✅ תשתית יציבה
- ✅ תיעוד מקיף
- ✅ מדיניות ברורה
- ✅ בקרות בטיחות
- ✅ Workflows פעילים

**מה עדיין חסר?**
- ⏳ סריקת אבטחה מלאה (config/, secrets)
- ⏳ ברור Unknown Tools
- ⏳ אוטומציה מתקדמת (Semi-Automated)
- ⏳ Monitoring & Health Checks

**למה "מבוקר" ולא "Production"?**
- אין סוכנים אוטונומיים עם כתיבה
- כל פעולה דורשת אישור אנושי
- טרם בוצעה סריקת אבטחה מלאה
- Human-in-the-loop נשאר חובה

### השפעה על SSOT

**מסמכים שעודכנו** ✅:

1. **`docs/SYSTEM_SNAPSHOT.md`**:
   - ✅ סעיף "איפה אנחנו עכשיו":
     - הוסף: "✔ Phase 1 (Foundation) הושלם"
     - עדכן: "⏳ בשלב הבא: Phase 2 - Security & Automation"
   - ✅ סעיף "משימות פתוחות":
     - הזז משימות Phase 1 ל-"הושלם"

2. **`README.md`**:
   - ✅ סעיף Roadmap:
     - Phase 1: ~~In Progress~~ → **✅ COMPLETE**
     - Phase 2: Upcoming → **🔄 NEXT**

3. **`docs/CAPABILITIES_MATRIX.md`**:
   - ✅ הוסף הערה בראש המסמך:
     - "**System Status**: Foundation Complete (DECISION 2025-11-20 #4) - Ready for Controlled Use"

4. **`docs/DECISIONS_AI_OS.md`** (מסמך זה):
   - ✅ הוסף החלטה #4
   - ✅ עדכן סיכום החלטות (4 החלטות)
   - ✅ עדכן "עדכון אחרון"

### Follow-ups

**Phase 2 Options** - לבחור Thin Slice ראשון:

**אפשרות A: Security Phase 1** (מומלץ):
- [ ] הוספת `.gitignore` rules
- [ ] סימון `SECRETS/` כמוגן
- [ ] Warning ב-README על אזורים רגישים
- [ ] סריקת `config/` לחיפוש secrets inline
- [ ] יצירת רשימת מיגרציה

**אפשרות B: Workflows נוספים**:
- [ ] WF-003: Health Checks
- [ ] WF-003: SSOT Auto-Update (חלקי)
- [ ] WF-003: Secret Migration Process

**אפשרות C: ברור Unknown Tools**:
- [ ] בדיקת Make.com - בשימוש?
- [ ] בדיקת Telegram Bot - איזה bot?
- [ ] סריקת GitHub Actions - אילו workflows?
- [ ] סקירת Config Files - secrets inline?

**אפשרות D: תיעוד כלים פעילים**:
- [ ] `tools/GITHUB_MCP.md`
- [ ] `tools/WINDOWS_MCP.md`
- [ ] `tools/FILESYSTEM_MCP.md`
- [ ] `tools/GOOGLE_MCP.md`

**חובה**: כל החלטה דומה בעתיד תעבור דרך **WF-002** ותעודכן ב-DECISIONS_AI_OS + SSOT.

---

## 2025-11-24 – החלטה #5: Telegram UI – Official Interface (AI-OS-DECISION-TELEGRAM-001)

### הקשר
במערכת קיימים שני "עולמות" של טלגרם:

1. **Chat1 – ממשק רשמי בתוך ai-os**:
   - נמצא ב-`chat/telegram_bot.py`
   - מחובר ל-Agent Gateway (`ai_core/agent_gateway.py`)
   - ממשק בעברית עם Human-in-the-Loop (כפתורי אישור)
   - מתועד כחלק מהארכיטקטורה של AI-OS

2. **פרוטוטיפ חיצוני (מחוץ לריפו)**:
   - נמצא בתיקיה מקומית מחוץ ל-ai-os
   - מחבר טלגרם ל-LLM קטן דרך HTTP פשוט
   - **לא** מחובר ל-Agent Gateway
   - שימש לניסוי ראשוני בלבד

**שאלה**: מה הממשק הרשמי לטלגרם ב-AI-OS?

### ההחלטה
**יש רק ממשק טלגרם רשמי אחד ל-AI-OS: Chat1 דרך Agent Gateway.**

- **סטטוס Chat1**: 🚧 Implemented (Not Fully Deployed)
- **סטטוס פרוטוטיפ חיצוני**: 🗄️ Legacy / External
- **מיקום Chat1**: `chat/telegram_bot.py`

### רציונל

**למה Chat1 הוא הממשק הרשמי?**
1. **מחובר לארכיטקטורה**: מדבר עם Agent Gateway → GPT Planner - הזרימה הנכונה.
2. **Human-in-the-Loop**: מציג תוכנית ומבקש אישור לפני ביצוע.
3. **מתועד**: הקוד בריפו, חלק מה-SSOT.
4. **עברית**: ממשק בעברית.

**למה הפרוטוטיפ החיצוני אינו רשמי?**
1. **לא מחובר ל-Agent Gateway**: מדבר עם LLM חיצוני, לא עם התשתית של AI-OS.
2. **לא מתועד**: נמצא מחוץ לריפו.
3. **ניסוי בלבד**: שימש ללמידה, לא לשימוש אמיתי.

### כללים מחייבים

1. **אסור** לבנות תהליכים רשמיים על הפרוטוטיפ החיצוני.
2. במידת הצורך, יש ליידע בתיעוד אם פרוטוטיפ כזה מקודם או נזנח.
3. **Chat1 הוא הממשק הרשמי היחיד** לטלגרם ב-AI-OS.

---

---

## 2025-11-27 – DEC-006: n8n כ-Automation Kernel רשמי של AI-OS (Make.com לא ליבה)

**Date:** 2025-11-27  
**Owner:** Or  
**Status:** Approved  

**Context:**
AI-OS אישי בנוי על:
- GitHub כשכבת State בקבצים (JSON/YAML/Markdown) – Source of Truth.
- Google Workspace כ-Control Plane (UI לבני אדם – Sheets/Docs וכו'.).
- שכבת סוכנים (AgentKit / MCP / LangChain) כ-Super-Layer.

נדרש "Automation Kernel" – פלטפורמת וורקפלואים שתהיה:
- קרובה ל-Git ולקבצים (Local / Docker),
- ללא גביית "אופרציות" על כל צעד,
- מוכנה לאינטגרציה עמוקה עם סוכנים (MCP / Tools),
- ניתנת לניהול כ-Infrastructure (GitOps, Docker, backups).

בוצע מחקר השוואתי n8n מול Make.com, והוגדר GAP-004: בחירת פלטפורמת אוטומציה רשמית ל-Phase 2.4+.

**Options Considered:**
1. **Option A – n8n (Self-Hosted, Docker):**
   - רצה כ-Container מקומי/VPS.
   - ללא הגבלה על מספר Executions (ב-Community / Self-hosted).
   - גישה ישירה למערכת הקבצים (Volume Mount) → מתאים ל-GitHub State בקבצים.
   - תמיכה ב-Code Nodes (JS/Python) ובאינטגרציות מודרניות (MCP / LangChain).
   - ניתן לגרסה בתצורת INFRA_ONLY (רק אוטומציות מערכתיות, בלי לגעת בחיים האישיים).

2. **Option B – Make.com (SaaS, Operation-based):**
   - פלטפורמת SaaS נוחה, low-code.
   - מודל תמחור לפי אופרציות – יקר לסוכנים "פטפטניים" (Agents).
   - אין גישה ישירה ל-Filesystem/Git; עבודה בעיקר דרך GitHub API.
   - Storage לוגיקה בפורמט קנייני בענן Make (קשה ל-GitOps).
   - תלות חזקה ב-SaaS חיצוני לחלק הכי עמוק של ה-OS.

3. **Option C – Hybrid/None:**
   - לעבוד בלי Kernel רשמי (רק MCP/סקריפטים נקודתיים).
   - או להשתמש גם ב-n8n וגם ב-Make.com בלי הכרעה ברורה.
   - תוצאה: מורכבות, חוסר עקביות, קושי בניהול State ובתיעוד.

**Decision:**
- **n8n נבחר כ-Automation Kernel רשמי של ה-AI-OS** החל מ-Phase 2.4 ואילך.
- הפרויקט יתבסס על **n8n Self-Hosted (Docker)** כתשתית ראשית לוורקפלואים:
  - מערכתית (Infra / State / Healthchecks / Sync),
  - ובהמשך גם לחלק מהאוטומציות על החיים, תחת קונטרול ובקרה.
- **Make.com לא חלק מהליבה של ה-AI-OS**:
  - לא תלוי בו, לא מסתמך עליו כקרנל.
  - מותר שימוש נקודתי/ניסויי על ידי אור, אבל לא כמרכיב מרכזי במערכת.
- GitHub נשאר **ה-SSOT**: גם ה-State וגם ה-Workflows של n8n יתועדו/ייגובו ב-Git.

**Implementation Notes:**
- Phase 2.3 (INFRA_ONLY):
  - BLOCK_N8N_INFRA_BOOTSTRAP_V1 already executed (infra/n8n/* + State Layer updates).
  - n8n מוגדר כ-service status=up, אך השימוש בו מוגבל לאינפרה בלבד.
  - אין אוטומציות על החיים (Gmail/Calendar/Tasks) עד שינוי Mode.

- Phase 2.4:
  - להוסיף Blocks:
    - `BLOCK_N8N_CONTROL_PLANE_INTEGRATION_V1` – workflows שעובדים רק מול GitHub State ו-Google כ-UI, עדיין INFRA בלבד.
    - `BLOCK_N8N_BACKUP_AND_GITOPS_V1` – גיבוי אוטומטי של Workflows ל-Git (Export → Commit).
  - לעדכן:
    - `SERVICES_STATUS.json`: make.com = not_core / optional_saas.
    - `SYSTEM_STATE_COMPACT.json`: להסיר סתירות ("DEC-006 pending") ולהפנות ל-DEC-006 הרשמי.

- Phase 3+:
  - אינטגרציה של n8n עם AgentKit / MCP כ-"Tool Server" עבור סוכנים.
  - פתיחת אפשרות לאוטומציות חיים תחת Human-in-the-Loop לפי Mode/Phase.

**Related:**
- GAP-004: n8n vs Make.com → **Closed by DEC-006**
- BLOCK_N8N_INFRA_BOOTSTRAP_V1
- POLICY-001: NO-KOMBINOT for Infrastructure Tools
- DEC-007: No Hierarchy Between Interfaces

---

## 2025-11-26 – DEC-004: Connectivity Strategy for GPT Actions & Remote Access (ngrok vs Cloudflare)

**Date:** 2025-11-26  
**Owner:** Or  
**Status:** Approved  

**Context:**  
AI-OS האישי רץ כרגע על מחשב מקומי מאחורי NAT, עם חשיפה החוצה דרך ngrok (תוכנית חינמית).  
GPT Actions דורשות:
- URL יציב ב-HTTPS, עם TLS תקין,
- שלא ישתנה בכל restart,
- בלי מסכים באמצע (Interstitial) שיכולים לשבור קריאות אוטומטיות.

בדו"ח BLOCK_NGROK_STABILITY_RESEARCH זוהה GAP-001:
- ngrok חינמי עם URL מתחלף = חיכוך גבוה (כל restart דורש לעדכן את ה-Action),
- תחזוקה ידנית של ה-URL שוברת את חוויית "OS" ויוצרת חוסר יציבות.

מחקר עדכני מראה:
- ל-ngrok יש היום יכולת static domain גם בחינם (דומיין קבוע אחד שלא משתנה) – אבל בתוכנית החינמית יש עדיין מגבלות קשות: session קצר, תקרה על רוחב פס, ואזהרות/interstitial לפני ה-API, מה שעלול לשבור אינטגרציה עם GPT Actions.
- Cloudflare Tunnel מאפשר חיבור Outbound-only דרך `cloudflared` ל-edge של Cloudflare, שימוש בדומיין אישי, ו-WAF חזק – בחינם, כל עוד יש דומיין.

מטרת ההחלטה:
- להגדיר אסטרטגיית קישוריות רשמית ל-AI-OS עבור GPT Actions ושירותי HTTP,
- בלי להתחייב עדיין ל-"production 24/7", אבל עם פחות חיכוך והרבה יותר יציבות.

**Options Considered:**

1. **Option A – להישאר עם ngrok חינמי כמו עכשיו**  
   - URL אקראי (אם לא משתמשים ב-static domain).  
   - צורך לעדכן ידנית את GPT Actions בכל restart.  
   - מגבלות תכנית חינמית: Session קצר, תקרה על תעבורה, אזהרות/interstitial.  
   - יתרון: 0 שינוי, 0 מאמץ.  
   - חסרון: חוויית פיתוח שבירה, לא מתאים ל-OS.

2. **Option B – ngrok Personal / Paid (דומיין קבוע + TCP)**  
   - Personal plan (סביב $8/חודש) כולל custom domain אחד + כתובת TCP קבועה.  
   - משפר משמעותית יציבות: דומיין/כתובת לא משתנים, בלי interstitial של Free.  
   - עדיין: תעבורה עוברת דרך רשת ngrok, עם מגבלות שימוש וחיוב Usage-Based.  
   - יתרון: קל להטמעה, בלי לשנות הרבה בארכיטקטורה.  
   - חסרון: עלות קבועה לפרויקט אישי בשלב תשתית, תלות חזקה ב-SaaS יחיד.

3. **Option C – Cloudflare Tunnel Free Tier + דומיין פרטי (הפתרון שנבחר בהחלטה זו)**  
   - התקנת `cloudflared` מקומית שיוצר חיבור מוצפן חד-כיווני (Outbound-only) ל-Cloudflare.  
   - שימוש בדומיין שלי (עלות ~10$ לשנה) + Cloudflare Free Plan (SSL, WAF, DDoS בחינם).  
   - URL יציב לחלוטין (DNS-based), גם אם המחשב נכבה וחוזר.  
   - הגדרת חוק WAF שמדלג על סינון עבור GPT / ChatGPT (לפי User-Agent / IP), כדי למנוע חסימות "בוטים".  
   - יתרון:  
     - יציבות גבוהה,  
     - אבטחה טובה,  
     - לא תלוי במודל התמחור של ngrok,  
     - מתאים לטווח הבינוני והארוך של ה-OS.  
   - חסרון: מעט יותר מורכב מ-ngrok להקמה ראשונית.

4. **Option D – VPS + FRP / פתרון Self-Hosted (טווח ארוך יותר)**  
   - שכירת VPS זול + התקנת FRP (Fast Reverse Proxy) לשליטה מלאה ב-IP וכניסות.  
   - מתאים יותר לשלב Production (Phase 3+), לא ל-Phase 2.3 INFRA_ONLY.  
   - יתרון: ריבונות מלאה, zero SaaS lock-in.  
   - חסרון: דורש DevOps מלא; מוקדם מדי עכשיו.

**Decision:**  

1. לטווח המיידי (Phase 2.3 – INFRA_ONLY):  
   - להפסיק להתבסס על ngrok כפתרון "מובן מאליו" ל-GPT Actions.  
   - לא לעבור כרגע לתכנית בתשלום (Option B) – עלות קבועה מיותרת בשלב תשתית.  
   - לאמץ Cloudflare Tunnel כפתרון הקישוריות הראשי עבור GPT Actions ושירותי HTTP הקריטיים ל-AI-OS (Option C), על בסיס דומיין פרטי.

2. לטווח הבינוני (Phase 2.4 – "Nervous System"):  
   - להשאיר ngrok ככלי משני/מקומי לפיתוח חד־פעמי (אם צריך), אבל:
     - Cloudflare Tunnel הוא ה-"gateway הרשמי" של ה-OS מול GPT.  
   - לשקול הוספת Tailscale / VPN ל-use cases של TCP פרטיים (לא GPT), בהחלטה נפרדת.

3. לטווח הארוך (Phase 3+):  
   - להשאיר Option D (VPS + FRP) כנתיב שדרוג אפשרי, אם ה-AI-OS יהפוך לתשתית קריטית ויהיה צריך רמת יציבות/ריבונות גבוהה יותר.

**Implementation Notes (לשלבים הבאים, לא לבצע בלי אישור נוסף):**

- BLOCK_CLOUDFLARE_TUNNEL_SETUP_V1  
- BLOCK_CLOUDFLARE_WAF_RULE_FOR_GPT_V1  
- BLOCK_GPT_ACTIONS_BASE_URL_UPDATE_V1  
- BLOCK_SERVICES_STATUS_UPDATE_V2  

**Related:**
- GAP-001: ngrok URL instability  
- GAP-002: No persistent deployment (indirectly)  
- BLOCK_NGROK_STABILITY_RESEARCH  
- Phase: 2.3 (INFRA_ONLY, Connectivity focus)

---

## 2025-11-26 – DEC-007: No Fixed Role Hierarchy Between Interfaces

**Date:** 2025-11-26  
**Owner:** Or  
**Status:** Approved  

**Context:**  
במסמכים שונים של AI-OS נמצאו שרידים של ניסוח היררכי שמתאר:
- GPT כ"מתכנן בלבד" או "DRY RUN mode"
- Claude כ"הידיים" או "המבצע הראשי"
- Chat1 כ"UI בלבד"
- היררכיה תפקודית קבועה לפי ממשק

זה מתנגש עם **ROLE_MODEL_SIMPLIFICATION_V1** (Block מ-2025-11-26) שביטל היררכיה קשיחה.

**Problem:**  
ניסוח כמו "GPT = DRY RUN בלבד" יוצר רושם שגוי ש-GPT "לא באמת עושה דברים", במקום לתאר בדיוק את:
- היכולות הטכניות שלו (מה הוא יכול לעשות)
- מגבלות הבטיחות שלו (מה אסור לעשות בלי אישור)

הבעיה: ניסוחים אלה מציגים את הממשקים כ"דרגות" במקום כממשקים שונים עם יכולות שונות.

**Decision:**

1. **אין היררכיית תפקידים קבועה** בין הממשקים (Claude/GPT/Chat1):
   - אין "מוח לעומת ידיים"
   - אין "מתכנן לעומת מבצע"
   - אין "DRY RUN לעומת אמיתי"
   - אין "ממשק ראשי" או "ממשק משני"

2. **יש רק שני סוגי מאפיינים:**
   - **Technical Capabilities** — מה כל ממשק יכול לעשות מבחינה טכנית (גישה לכלים, APIs)
   - **Safety Constraints** — מגבלות בטיחות שחלות על כולם (כמו Safe Git Policy)

3. **מדיניות GitHub אחידה:**
   - **לכל הממשקים** חל אותו Safe Git Policy:
     - "PR-first approach, no direct push to main without Or's explicit approval"
   - לא "GPT = DRY RUN" ו-"Claude = Full Write"

4. **ניסוח מומלץ במסמכים:**
   - ✅ **נכון**: "Claude Desktop: Full MCP access including local Git operations, subject to Safe Git Policy"
   - ✅ **נכון**: "GPT: GitHub access via Custom Actions (read/write), subject to Safe Git Policy"
   - ❌ **לא נכון**: "Claude = Primary Executor", "GPT = Planner Only", "DRY RUN mode"

5. **מונחים להסיר מהתיעוד:**
   - "Hands" / "Brain" / "Primary" / "Secondary"
   - "Executor" / "Planner Only" / "DRY RUN mode"
   - "Real" vs "Simulated"

**Implementation:**
עדכון 5 קבצים:
- `docs/DECISIONS_AI_OS.md` (החלטה #3 עודכנה)
- `docs/AGENT_SYNC_OVERVIEW.md`
- `docs/system_state/agents/AGENT_CAPABILITY_PROFILE.md`
- `docs/system_state/SYSTEM_STATE_COMPACT.json`
- `docs/system_state/registries/SERVICES_STATUS.json`

**Impact:**
- תיעוד ברור יותר של יכולות ומגבלות
- אין בלבול על "מי עושה מה"
- גמישות בעבודה - כל ממשק יכול לעשות מה שיכול (בכפוף לבטיחות)

**Related:**
- ROLE_MODEL_SIMPLIFICATION_V1 (Block, 2025-11-26)
- DEC-003 (Safe Git Policy)
- CONSTITUTION.md Law #4 (Human-in-the-Loop)

---

## סיכום ההחלטות

| # | נושא | החלטה | סטטוס |
|---|------|-------|-------|
| **1** | MCP Orchestration | לא נלקח כקוד רץ | 🗄️ Legacy (Reference Only) |
| **2** | GitHub Executor API | לא פרוס | 📋 Designed (Not Deployed) |
| **3** | GitHub Safe Git Policy | PR-first for all interfaces | ✅ Active |
| **4** | Phase 1 Foundation | הושלם | ✅ Complete - Ready for Use |
| **5** | Telegram UI - Official Interface | Chat1 בלבד | ✅ Decision Locked |
| **DEC-004** | Connectivity Strategy (ngrok vs Cloudflare) | Cloudflare Tunnel | ✅ Approved |
| **DEC-006** | n8n as Automation Kernel | n8n Self-Hosted | ✅ Approved |
| **DEC-007** | No Fixed Role Hierarchy | Capabilities + Constraints model | ✅ Approved |

---

## עקרונות מנחים

ההחלטות האלה משקפות את **חוקי היסוד של AI-OS**:

1. **Data-First** (חוק #1): קודם מגדירים, אחר כך בונים
2. **Human-in-the-loop** (חוק #4): אין פעולות הרסניות בלי אישור
3. **Thin Slices** (חוק #6): בונים בצורה הדרגתית ומבוקרת
4. **אבטחה מעל הכל** (חוק #7): בטיחות תמיד במקום הראשון

---

**סטטוס מסמך זה**: ✅ Active  
**עדכון אחרון**: 27 נובמבר 2025  
**החלטות נעולות**: 8 החלטות קריטיות  
**הערה**: החלטות אלה ניתנות לשינוי בעתיד, אבל רק אחרי דיון מפורש ותיעוד של הרציונל לשינוי.
