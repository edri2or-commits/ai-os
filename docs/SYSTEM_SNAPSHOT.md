# System Snapshot – מצב נוכחי (Version 2 – 2025-11-20)

זהו צילום מצב מעודכן של מערכת ה-AI-OS שלי, אחרי סידור ראשוני של תיעוד, סוכנים, כלים ומדיניות אבטחה.

---

## 1. ריפואים ומבנה

### `ai-os` (ריפו חדש – SSOT)
הריפו הזה הוא "המוח המרכזי" (Single Source of Truth) של המערכת.

**מבנה עיקרי**:
```
ai-os/
├── README.md                    ✅ מדריך ראשי מקיף (420 שורות)
├── docs/                        ✅ 5 מסמכי SSOT
│   ├── CONSTITUTION.md          ✅ 9 חוקי יסוד
│   ├── SYSTEM_SNAPSHOT.md       ✅ צילום מצב (הקובץ הזה)
│   ├── CAPABILITIES_MATRIX.md   ✅ v1.1 (22 יכולות + 3 החלטות)
│   ├── DECISIONS_AI_OS.md       ✅ 3 החלטות קריטיות נעולות
│   └── REPO_AUDIT_make-ops-clean.md ✅ אודיט מלא של הריפו הישן
├── agents/                      ✅ 2 מסמכי סוכנים
│   ├── AGENTS_INVENTORY.md      ✅ מיפוי 8 סוכנים
│   └── GPT_GITHUB_AGENT.md      ✅ תיעוד סוכן ליבה #1
├── workflows/                   ✅ 1 workflow פעיל
│   └── GITHUB_PLANNING_DRY_RUN.md ✅ WF-001 (570 שורות)
├── tools/                       ✅ 1 מסמך
│   └── TOOLS_INVENTORY.md       ✅ 24 כלים ממופים (327 שורות)
├── policies/                    ✅ 1 מדיניות
│   └── SECURITY_SECRETS_POLICY.md ✅ מדיניות אבטחה (720 שורות)
└── archive/                     📁 ריק (לעתיד)
```

**README.md מעודכן** כולל:
- מטרה ותיאור ברור
- מבנה תיקיות חזותי
- דיאגרמת זרימה של איך המערכת עובדת
- מדריך מהיר (5 שלבים)
- Roadmap (4 phases)
- FAQ (6 שאלות)
- דוגמאות שימוש

---

### `make-ops-clean` (ריפו ישן – Legacy)
- משמש כ"ארכיון חי" למערכת הקודמת
- מכיל קוד, קונפיגים, MCP, כלים ואוטומציות ישנות
- **סטטוס**: לא נחשב ל-SSOT, לא רץ כ-production
- **תיעוד**: `docs/REPO_AUDIT_make-ops-clean.md` ב-`ai-os`

**תיקיות רגישות זוהו**:
- 🚨 `SECRETS/` - OFF LIMITS (לא לפתוח)
- ⚠️ `config/` - ייתכן secrets inline (דורש סריקה)

---

## 2. מסמכי ליבה (SSOT)

### `docs/CONSTITUTION.md`
**9 חוקי היסוד** של המערכת:

1. **Data-First** - קודם מגדירים, אחר כך בונים
2. **Single Source of Truth** - הריפו הזה = מקור האמת
3. **DRY** - לא משכפלים לוגיקה
4. **Human-in-the-loop** - אישור לכל פעולה הרסנית
5. **שקיפות** - תיעוד לכל סוכן/כלי/תהליך
6. **Thin Slices** - שינויים קטנים וברורים
7. **אבטחה מעל הכל** - secrets רק במקומות מאובטחים
8. **זיכרון משותף** - הריפו = זיכרון בין מודלים
9. **כבוד למורשת** - הריפו הישן מתועד, לא נמחק

---

### `docs/SYSTEM_SNAPSHOT.md`
**הקובץ הנוכחי** - צילום מצב עדכני של המערכת.

**גרסאות**:
- v1 (20 נוב 2025) - מצב ראשוני
- v2 (20 נוב 2025) - אחרי תיעוד מקיף

---

### `docs/CAPABILITIES_MATRIX.md` (v1.1)
**מפת היכולות המלאה** - 22 יכולות מתועדות:

**יכולות פעילות** (✅):
- **GitHub** (GH-001 עד GH-004): קריאה, ניתוח, כתיבה ידנית, PRs
- **Filesystem** (FS-001, FS-002): גישה מקומית, חיפוש וניתוח
- **Windows** (WIN-001 עד WIN-003): PowerShell, UI Control, App Launch
- **Google** (GGL-001 עד GGL-003): Calendar, Gmail, Drive (READ-ONLY)
- **Knowledge Base** (KB-001): קריאת מסמכי ידע

**יכולות מוגבלות** (🚧):
- **GitHub Planning** (GH-002): GPT Agent (DRY RUN בלבד)

**יכולות מתוכננות** (📋):
- **GitHub Executor API** (GH-005): Blueprint בלבד, לא פרוס
- **Google Write** (GGL-004): דורש OAuth נוסף

**יכולות Legacy** (🗄️):
- **MCP Orchestration** (MCP-001 עד MCP-003): Reference Only
- **ADRs, Diagnostics, Autopilot** (KB-002, DIAG-001/002, AUTO-001)

**3 החלטות קריטיות נעולות**:
1. MCP Orchestration = Reference Only
2. GitHub Executor API = Not Deployed
3. GPT GitHub Agent = DRY RUN Only

---

### `docs/DECISIONS_AI_OS.md`
**לוג החלטות רשמי** - 3 החלטות ליבה:

#### **החלטה #1: MCP Orchestration**
- **החלטה**: לא נלקח כקוד רץ ל-AI-OS
- **סטטוס**: 🗄️ Legacy / Reference Only
- **רציונל**: מורכבות גבוהה, תלות בתשתית, עדיף לבנות חדש

#### **החלטה #2: GitHub Executor API**
- **החלטה**: לא פרוס, לא מופעל
- **סטטוס**: 📋 Designed (Not Deployed)
- **רציונל**: תוכנן למערכת אחרת, בעיות deployment, חוסר שכבות בטיחות

#### **החלטה #3: GPT GitHub Agent – Execution Mode**
- **החלטה**: נשאר במצב DRY RUN בלבד
- **סטטוס**: 🚧 Operational (Limited)
- **רציונל**: בטיחות, בניית אמון הדרגתי, Human-in-the-loop חובה

**Roadmap עתידי**:
- שלב 1 (נוכחי): DRY RUN
- שלב 2 (עתיד): Executor מוגבל ל-OS_SAFE
- שלב 3 (רחוק): Executor מלא עם אישור

---

### `docs/REPO_AUDIT_make-ops-clean.md`
**אודיט מפורט** של הריפו הישן:

**ממצאים עיקריים**:
- 30+ תיקיות וקבצים חשובים
- סיווג: זהב / ניסוי / לא ברור
- הצעות מיקום ב-`ai-os`
- זיהוי אזורים רגישים

**תיקיות ליבה**:
- `DOCS/`, `docs/` - תיעוד
- `agents/`, `gpt_agent/` - סוכנים
- `mcp/` - Master Control Program
- `config/` - קונפיגורציה (⚠️ רגיש)
- `SECRETS/` - חומר רגיש (🚨 OFF LIMITS)

---

## 3. סוכנים (Agents)

### `agents/AGENTS_INVENTORY.md`
**מיפוי 8 סוכנים** מהריפו הישן:

| Agent | Role | Status | Decision |
|-------|------|--------|----------|
| **GPT GitHub Agent** | Planner (DRY RUN) | 🚧 Active | סוכן ליבה |
| **MCP Master Control** | Orchestration | 🗄️ Legacy | Reference Only |
| **GitHub Executor API** | Automation | 📋 Designed | Blueprint |
| **Autopilot** | Self-Healing | 🗄️ Legacy | Archive |
| **Local Execution Agent** | Placeholder | 🗄️ Legacy | Delete? |
| **OPS Decision Manager** | ADRs | 🗄️ Legacy | Workflow Comp |
| **OPS Diagnostics** | Health Checks | 🗄️ Legacy | Workflow Comp |
| **GitHub Executor Bootstrap** | Triggers | 🗄️ Legacy | Workflow Doc |

**סטטוס נוכחי**:
- 1 סוכן פעיל: GPT GitHub Agent (DRY RUN)
- 0 סוכנים אוטונומיים עם כתיבה
- Human-in-the-loop על כל פעולה

---

### `agents/GPT_GITHUB_AGENT.md`
**תעודת זהות** לסוכן הליבה הראשון:

**תפקיד**: Planner לפעולות GitHub

**אחריות**:
- קריאת SSOT documents
- ניתוח Intent משתמש
- סיווג רמת סיכון (OS_SAFE / CLOUD_OPS_HIGH)
- יצירת תוכנית מפורטת

**גבולות**:
- ❌ לא כותב קבצים
- ❌ לא יוצר commits
- ❌ לא פותח PRs
- ✅ רק מתכנן ומציע

**מקור**: `make-ops-clean/gpt_agent/github_agent.py`

---

## 4. כלים ואינטגרציות (Tools)

### `tools/TOOLS_INVENTORY.md`
**מיפוי מקיף** של 24 כלים:

#### **כלים פעילים** (10):
- **Claude Desktop** - Gateway ראשי (Critical Risk)
- **GitHub MCP** - Read/Write לריפואים (High Risk)
- **Filesystem MCP** - גישה מקומית (High Risk)
- **Windows MCP** - שליטה ב-OS (Critical Risk)
- **Google MCP** - READ-ONLY (Medium Risk)
- **GPT GitHub Agent** - DRY RUN (Medium Risk)
- **Canva** - עיצוב גרפי (Low Risk)
- **Browser Control** - אוטומציית דפדפן (Medium Risk)
- **Autonomous Control** - פקודות מערכת (Critical Risk)
- **GitHub Control** - ניהול repos (High Risk)

#### **כלים Legacy** (8):
- MCP Server, MCP GitHub Int., MCP Google Int.
- GPT API Wrapper, Autopilot, Local Execution
- GitHub Scripts, Automation Scripts

#### **כלים Unknown** (4 - דורשים בדיקה):
- **Make.com** - Automation Platform
- **Telegram Bot** - Messaging
- **GitHub Actions** - CI/CD
- **Config Files** - 🚨 דורש סקירת אבטחה

#### **כלים Designed** (1):
- **GitHub Executor API** - Blueprint בלבד

**מיפוי סיקרטים**:
- GitHub OAuth → Claude App (✅ Secure)
- Google OAuth → Claude App (✅ Secure)
- GPT API Key → Env (⚠️ Review)
- Config Secrets → **Inline** (🚨 Critical - דורש מיגרציה)

---

## 5. מדיניות וחוקים (Policies)

### `policies/SECURITY_SECRETS_POLICY.md`
**מדיניות אבטחה מקיפה** (720 שורות):

#### **4 עקרונות יסוד**:

1. **No Secrets in Plain Text**
   - ❌ לא ב-Markdown, קוד, config
   - ✅ רק ב-GitHub Secrets, Env, Secret Manager

2. **Never Display Secrets**
   - ❌ לא ערך מלא, לא חלקי
   - ✅ רק placeholders: `***SECRET***`

3. **Human Authorization Required**
   - כל פעולה עם secrets דורשת אישור
   - יצירה, שינוי, מחיקה, העברה, מיגרציה

4. **Minimal Privilege**
   - כל סוכן/כלי מקבל רק מה שצריך
   - רמות: Public → Internal → Confidential → Secret

#### **3 זונות רגישות**:

1. **Zone 1: SECRETS/** - 🔴 CRITICAL
   - `make-ops-clean/SECRETS/`
   - OFF LIMITS - אסור לפתוח

2. **Zone 2: config/** - ⚠️ HIGH RISK
   - `make-ops-clean/config/`
   - ייתכן secrets inline
   - דורש סריקה מבוקרת

3. **Zone 3: Other Sensitive Files** - ⚠️ MEDIUM
   - `*.env`, `secrets.*`, `credentials.*`

#### **כללים לסוכנים**:
- **Claude**: פועל לפי policy, לא מציג secrets
- **GPT Agent**: משתמש בplaceholders, אין write
- **MCP Servers**: מכבד exclusion list

#### **תהליך מיגרציה** (6 צעדים):
1. Identify secrets
2. Document findings
3. Create secrets in secure location
4. Update config עם placeholders
5. Validate שעובד
6. Cleanup + Rotate

#### **תרחישי חירום**:
- Secret exposed in chat → Rotate + Clean
- Secret exposed in commit → Filter + Rotate
- SECRETS/ accessed → Stop + Rotate all

#### **תוכנית יישום** (5 phases):
- **Phase 1** (Immediate): `.gitignore`, סימון SECRETS/
- **Phase 2** (שבוע 1): סריקת config/, רשימת מיגרציה
- **Phase 3** (שבוע 2-3): מיגרציה ל-env
- **Phase 4** (שבוע 4): validation
- **Phase 5** (ongoing): prevention, audits

---

## 6. Workflows

### `workflows/GITHUB_PLANNING_DRY_RUN.md` (WF-001)
**Workflow רשמי** לתכנון שינויים בגיטהאב (570 שורות):

#### **שחקנים**:
- אור (Human) - מנסח בקשות, מאשר
- GPT GitHub Agent - Planner
- Claude Desktop - מבצע ידני
- GitHub - ריפואים

#### **7 שלבים**:

1. **ניסוח הבקשה**
   - אור מנסח מה רוצה לשנות

2. **ניתוח וקריאה**
   - GPT Agent קורא SSOT, מנתח מצב

3. **סיווג סיכון**
   - OS_SAFE או CLOUD_OPS_HIGH

4. **יצירת תוכנית**
   - מצב נוכחי, מצב רצוי, צעדים מפורטים

5. **סקירה ואישור**
   - אור בודק ומאשר

6. **ביצוע ידני**
   - אור + Claude מבצעים

7. **תיעוד ועדכון**
   - עדכון SSOT אם נדרש

#### **Safety & Boundaries**:
- GPT Agent לא מבצע פעולות כתיבה
- כל פעולה הרסנית דורשת אישור
- תמיד אפשר rollback

#### **דוגמאות שימוש**:
- יצירת workflow חדש (OS_SAFE)
- הוספת כלי חדש (OS_SAFE)
- שינוי קוד (CLOUD_OPS_HIGH)

#### **Roadmap**:
- שלב 1 (נוכחי): DRY RUN בלבד
- שלב 2: Semi-Automated (טיוטות PR)
- שלב 3: Executor מוגבל
- שלב 4: Executor מלא

---

## 7. מצב אבטחה

### **מדיניות מוגדרת**:
- ✅ `SECURITY_SECRETS_POLICY.md` פעילה
- ✅ 4 עקרונות יסוד ברורים
- ✅ 3 זונות רגישות מוגדרות
- ✅ כללים לכל סוכן/כלי

### **ממצאים**:
- 🚨 `SECRETS/` - OFF LIMITS (לא נגעו)
- ⚠️ `config/` - טרם נסרק (Phase 2)
- ⚠️ 4 כלים Unknown - דורשים בדיקה

### **תוכנית פעולה**:
- [ ] Phase 1: `.gitignore` + סימון
- [ ] Phase 2: סריקת config/
- [ ] Phase 3: מיגרציה
- [ ] Phase 4: validation
- [ ] Phase 5: prevention

### **KPIs**:
| Metric | Target | Current |
|--------|--------|---------|
| Secrets in plain text | 0 | ❓ TBD |
| Config files scanned | 100% | 0% |
| Secrets migrated | 100% | 0% |
| Security incidents | 0 | 0 ✅ |

---

## 8. איפה אנחנו עכשיו בתהליך (Version 2)

### ✅ **Phase 1 (Foundation) - הושלם!** 🎉

**DECISION 2025-11-20 #4**: Phase 1 הושלם בהצלחה!

1. **תשתית בסיסית**:
   - [x] ריפו `ai-os` נוצר
   - [x] מבנה תיקיות הוגדר
   - [x] README מקיף (420 שורות)

2. **מסמכי SSOT**:
   - [x] CONSTITUTION (9 חוקים)
   - [x] SYSTEM_SNAPSHOT (v2)
   - [x] CAPABILITIES_MATRIX (v1.1, 22 יכולות)
   - [x] DECISIONS_AI_OS (4 החלטות)
   - [x] REPO_AUDIT (אודיט מלא)

3. **סוכנים**:
   - [x] AGENTS_INVENTORY (8 סוכנים)
   - [x] GPT_GITHUB_AGENT (תיעוד מלא)

4. **כלים**:
   - [x] TOOLS_INVENTORY (24 כלים)

5. **מדיניות**:
   - [x] SECURITY_SECRETS_POLICY (720 שורות)

6. **Workflows**:
   - [x] WF-001: GITHUB_PLANNING_DRY_RUN (570 שורות)
   - [x] WF-002: DECISION_LOGGING_AND_SSOT_UPDATE (737 שורות)

**סטטוס מערכת**: ✅ Ready for Controlled Use  
**תיעוד**: 14 מסמכים, ~4,800 שורות  
**Workflows**: 2 פעילים  
**המערכת מוכנה לשימוש מבוקר!**

---

### 🔄 **Phase 2 - הבא**:

**אפשרות 1: אבטחת סיקרטים** (Phase 1-2):
- [ ] הוספת `.gitignore` rules
- [ ] סימון `SECRETS/` כמוגן
- [ ] warning ב-README
- [ ] סריקת `config/` לחיפוש secrets
- [ ] יצירת רשימת מיגרציה

**אפשרות 2: Workflows נוספים**:
- [ ] WF-003: Health Checks
- [ ] WF-003: Secret Migration Process
- [ ] WF-003: SSOT Auto-Update (חלקי)

**אפשרות 3: ברור כלים Unknown**:
- [ ] בדיקת Make.com - בשימוש?
- [ ] בדיקת Telegram Bot - איזה bot?
- [ ] סריקת GitHub Actions - אילו workflows?
- [ ] סקירת Config Files - secrets inline?

**אפשרות 4: תיעוד כלים פעילים**:
- [ ] `tools/GITHUB_MCP.md`
- [ ] `tools/WINDOWS_MCP.md`
- [ ] `tools/FILESYSTEM_MCP.md`
- [ ] `tools/GOOGLE_MCP.md`

---

## 9. סטטיסטיקות

### **תיעוד**:
- 📚 **מסמכים**: 14 קבצים (+1)
- 📄 **סה"ך שורות**: ~4,800 שורות תיעוד (+800)
- 📊 **גודל ממוצע**: ~340 שורות למסמך

### **כיסוי**:
- ✅ **חוקים**: 9/9 (100%)
- ✅ **סוכנים**: 8 ממופים
- ✅ **כלים**: 24 ממופים
- ✅ **יכולות**: 22 מתועדות
- ✅ **Workflows**: 2 מלאים (+1)
- ✅ **מדיניות**: 1 מקיפה
- ✅ **החלטות**: 4 נעולות (+1)

### **רמות בשלות**:
- **Documentation**: ⭐⭐⭐⭐⭐ (מצוין)
- **Automation**: ⭐⭐ (DRY RUN בלבד)
- **Security**: ⭐⭐⭐⭐ (מדיניות מוגדרת, טרם יושמה)
- **Testing**: ⭐ (טרם הוגדר)
- **Monitoring**: ⭐ (טרם הוגדר)

---

## 10. עקרונות הנחייה

המערכת פועלת לפי:

1. **Data-First** - תיעוד לפני קוד
2. **Human-in-the-loop** - אישור לכל פעולה מסוכנת
3. **Thin Slices** - שינויים קטנים וברורים
4. **DRY RUN First** - תכנון לפני ביצוע
5. **Security First** - בטיחות מעל נוחות
6. **Single Source of Truth** - הריפו = מקור האמת
7. **Transparency** - כל שינוי מתועד

---

## 11. משימות פתוחות

### **🚨 Critical**:
- [ ] סריקת `config/` לסיקרטים
- [ ] סימון `SECRETS/` כמוגן
- [ ] `.gitignore` rules

### **⚠️ High**:
- [ ] ברור כלים Unknown (Make, Telegram, Actions)
- [ ] תיעוד Google MCP OAuth scopes
- [ ] תכנון GitHub Executor v2

### **📋 Medium**:
- [ ] העברת Legacy tools לארכיון
- [ ] Workflows נוספים
- [ ] תיעוד כלים פעילים

### **✅ Low**:
- [ ] ניקוי ריפו ישן
- [ ] Health Checks
- [ ] Monitoring setup

---

**סטטוס Snapshot זה**: ✅ Active & Current  
**גרסה**: 2.0  
**עדכון אחרון**: 20 נובמבר 2025  
**עדכון הבא**: לאחר השלמת Phase 1 או הוספת Workflow נוסף

---

**המערכת מוכנה לשימוש!** 🚀

הבסיס יציב, התיעוד מקיף, והמדיניות ברורה. עכשיו אפשר:
- להפעיל workflows קיימים
- להוסיף workflows חדשים
- לטפל באבטחה (Phase 1-2)
- לברר כלים לא ברורים

**הצעד הבא תלוי בך!** 🎯
