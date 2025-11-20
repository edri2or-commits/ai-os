# Workflow: Secret Discovery (Read-Only) – WF-003

**Workflow ID**: WF-003  
**גרסה**: 1.0  
**תאריך יצירה**: 20 נובמבר 2025  
**סטטוס**: ✅ Active  
**קשור ל**: SEC-001 (SECURITY_SECRETS_POLICY)

---

## מטרה

לזהות בצורה **בטוחה וקריאה בלבד** היכן עלולים להיות סיקרטים (טוקנים, סיסמאות, מפתחות API) בריפואים.

**עקרונות ליבה**:
- 🔍 **Discovery Only** - רק זיהוי, לא שינוי
- 🔒 **Never Display** - לא מציגים ערכי סיקרטים
- 📋 **Documentation** - הפלט הוא רשימת קבצים, לא ערכים
- 👤 **Human Decision** - אדם מחליט מה לעשות עם הממצאים

**מיקוד ראשוני**:
- הריפו הישן `make-ops-clean`
- תיקיות כמו: `config/`, קבצי `*.env`, קבצי credentials

---

## מתי משתמשים ב-WF-003

### **תמיד משתמשים כש**:

1. **רוצים להבין את משטח התקיפה**:
   - איפה יש סיקרטים inline?
   - אילו קבצים בסיכון?
   - מה צריך מיגרציה בעתיד?

2. **לפני Secret Migration**:
   - לפני שמתחילים WF-004 (Secret Migration)
   - צריך לדעת מה ההיקף
   - צריך לתעדף מה קריטי

3. **אודיט תקופתי**:
   - בדיקה שלא נוספו סיקרטים חדשים
   - ולידציה שמדיניות מתקיימת
   - חלק מ-Health Checks

### **לא משתמשים כש**:

- רוצים לבצע מיגרציה (זה WF-004)
- רוצים לשנות קבצים (אסור ב-WF-003)
- רוצים לראות ערכי סיקרטים (אסור!)

**כלל אצבע**: אם אתה רק רוצה **לדעת איפה הבעיה** - WF-003. אם רוצה **לתקן** - WF-004.

---

## שחקנים (Actors)

| שחקן | תפקיד | אחריות |
|------|-------|---------|
| **אור (Human)** | מחליט | מגדיר טווח, מאשר סריקה, מחליט על follow-up |
| **Claude Desktop** | סורק | מבצע discovery, מדווח ממצאים (בלי ערכים) |
| **Filesystem MCP** | כלי | גישה לקריאת קבצים מקומיים |
| **SECURITY_SECRETS_POLICY** | מדיניות | מגדיר patterns, rules, boundaries |

---

## עקרונות מנחים

### **1. Read-Only בלבד 📖**
- אין שינוי קבצים
- אין מחיקה
- אין כתיבה לריפואים
- רק קריאה וניתוח

### **2. Never Display Secrets 🔒**
- לא מציגים ערך של סיקרט
- רק ציון: "נמצא חשד ל-password בשורה X"
- אם בטעות נמצא ערך - מיד מסתירים אותו
- placeholder: `***SECRET***` או `${SECRET_NAME}`

### **3. Respect Policy Boundaries 🛡️**
- מכבדים את `SECURITY_SECRETS_POLICY.md`
- OFF LIMITS zones (למשל `SECRETS/`) - לא נכנסים
- High Risk zones (למשל `config/`) - זהירות מרבית
- רק מה שמאושר לסריקה

### **4. Human-in-the-loop 👤**
- כל סריקה דורשת אישור מפורש
- כל החלטה על follow-up דורשת אישור
- לא מבצעים פעולות אוטומטיות

---

## שלבי העבודה (Workflow Steps)

### **שלב 1: הגדרת טווח סריקה (Scope Definition)**

**מבצע**: אור (Human)

**פעולות**:

אור מגדיר בפירוט:

1. **איזה ריפו**:
   ```
   דוגמה:
   - Repo: make-ops-clean
   - Path: C:\Users\edri2\Downloads\make-ops-clean
   ```

2. **אילו תיקיות**:
   ```
   דוגמה:
   - config/ (High Risk)
   - scripts/ (Medium Risk)
   - docs/ (Low Risk - אם יש credentials ב-Markdown)
   
   לא כולל:
   - SECRETS/ (OFF LIMITS)
   - node_modules/ (לא רלוונטי)
   ```

3. **אילו סוגי קבצים**:
   ```
   דוגמה:
   - *.yaml, *.yml (קונפיגים)
   - *.json (קונפיגים)
   - *.env, *.env.* (סביבות)
   - *.py, *.js, *.sh (קוד - אם יש hardcoded)
   - *.md, *.txt (תיעוד - לעיתים יש דוגמאות)
   ```

4. **רמת עומק**:
   ```
   - Recursive: כן/לא
   - Max Depth: מספר (למשל: 3 רמות)
   ```

**פלט**: הגדרת scope מפורטת

---

### **שלב 2: בחירת Patterns לזיהוי (Pattern Selection)**

**מבצע**: Claude (עם אישור אור)

**פעולות**:

שימוש ב-patterns מוגדרים מראש + התאמות:

#### **Patterns סטנדרטיים** (מ-SEC-001):

```yaml
# Passwords
patterns:
  - password\s*[:=]\s*["\']?[^"\'\s]+
  - passwd\s*[:=]\s*["\']?[^"\'\s]+
  - pwd\s*[:=]\s*["\']?[^"\'\s]+

# Tokens
  - token\s*[:=]\s*["\']?[^"\'\s]+
  - access_token\s*[:=]\s*["\']?[^"\'\s]+
  - auth_token\s*[:=]\s*["\']?[^"\'\s]+
  - bearer\s+[A-Za-z0-9\-._~+/]+=*

# API Keys
  - api_key\s*[:=]\s*["\']?[^"\'\s]+
  - apikey\s*[:=]\s*["\']?[^"\'\s]+
  - api_secret\s*[:=]\s*["\']?[^"\'\s]+

# Private Keys
  - -----BEGIN.*PRIVATE KEY-----
  - private_key\s*[:=]\s*["\']?[^"\'\s]+

# Cloud Credentials
  - aws_access_key_id\s*[:=]\s*["\']?[^"\'\s]+
  - aws_secret_access_key\s*[:=]\s*["\']?[^"\'\s]+
  - gcp_service_account\s*[:=]\s*["\']?[^"\'\s]+

# Database
  - db_password\s*[:=]\s*["\']?[^"\'\s]+
  - database_url\s*[:=]\s*["\']?[^"\'\s]+
  - connection_string\s*[:=]\s*["\']?[^"\'\s]+

# Generic Secrets
  - secret\s*[:=]\s*["\']?[^"\'\s]+
  - SECRET\s*[:=]\s*["\']?[^"\'\s]+
```

#### **התאמות ספציפיות**:

אפשר להוסיף patterns לפי הצורך:
```
- GitHub PAT: ghp_[A-Za-z0-9]{36}
- Slack Token: xox[baprs]-[0-9]{10,13}-[a-zA-Z0-9-]+
- Google API: AIza[0-9A-Za-z-_]{35}
```

**פלט**: רשימת patterns לסריקה

---

### **שלב 3: הפעלת סריקה (Scan Execution)**

**מבצע**: Claude Desktop (תחת פיקוח)

**פעולות**:

#### **3.1 הכנה**:
```
1. אשר scope עם אור
2. אשר patterns עם אור
3. אשר שלא נוגעים ב-OFF LIMITS zones
4. התחל סריקה
```

#### **3.2 סריקה לכל קובץ**:
```python
# Pseudo-code
for file in scope:
    if file in OFF_LIMITS:
        skip  # לא נכנסים לSECRETS/, וכו'
    
    content = read_file(file)  # קריאה בלבד
    
    for pattern in patterns:
        matches = find_pattern(content, pattern)
        if matches:
            report_finding(
                file=file.path,
                line=matches.line_number,
                type=pattern.type,  # password/token/key
                confidence=calculate_confidence(matches)
            )
            # ⚠️ אין הדפסה של הערך!
```

#### **3.3 פלט לכל ממצא**:
```markdown
Finding:
- File: config/app.yaml
- Line: 42
- Type: password
- Pattern: "password: ***"
- Confidence: High
- Context: "Line contains 'password:' with value"
- Action: Requires migration
```

**אין**:
- ❌ הדפסת ערך מלא
- ❌ הדפסת חלק מהערך
- ❌ שמירת הערך בזיכרון

**יש**:
- ✅ שם קובץ + מספר שורה
- ✅ סוג החשד
- ✅ רמת ביטחון
- ✅ המלצה

**פלט**: רשימת ממצאים (בלי ערכים)

---

### **שלב 4: סיכום ממצאים (Findings Summary)**

**מבצע**: Claude (עם אישור אור)

**פעולות**:

#### **4.1 יצירת דוח מסכם**:

```markdown
# Secret Discovery Report
**Date**: 2025-11-20
**Repo**: make-ops-clean
**Scope**: config/, scripts/
**Total Files Scanned**: 47
**Files with Findings**: 12
**Total Findings**: 23

## Summary by Type
| Type | Count | High Confidence | Medium | Low |
|------|-------|-----------------|--------|-----|
| Password | 8 | 6 | 2 | 0 |
| Token | 7 | 5 | 2 | 0 |
| API Key | 5 | 4 | 1 | 0 |
| Private Key | 2 | 2 | 0 | 0 |
| Database | 1 | 1 | 0 | 0 |

## Findings by File
| File | Type | Line | Confidence | Priority | Notes |
|------|------|------|------------|----------|-------|
| config/app.yaml | password | 42 | High | P0 | Prod password |
| config/db.json | token | 15 | High | P0 | API token |
| scripts/setup.sh | api_key | 8 | Medium | P1 | Dev key? |
| ... | ... | ... | ... | ... | ... |

## Recommendations
1. **P0 (Critical)**: 8 files - require immediate migration
2. **P1 (High)**: 3 files - migrate within 1 week
3. **P2 (Medium)**: 1 file - migrate within 1 month

## Next Steps
1. Review this report
2. Decide which files to migrate first
3. Use WF-004 (Secret Migration) for actual migration
4. Update DECISIONS_AI_OS with decision
```

#### **4.2 שמירת הדוח**:

```
Location: docs/SECURITY_DISCOVERY_REPORT_2025-11-20.md
או
Location: archive/security/discovery_2025-11-20.md
```

**פלט**: דוח מסכם מתועד

---

### **שלב 5: החלטה אנושית (Human Decision)**

**מבצע**: אור (Human)

**פעולות**:

#### **5.1 סקירת ממצאים**:
```
אור קורא את הדוח ומחליט:
1. אילו ממצאים אמיתיים (true positive)?
2. אילו false positive?
3. מה העדיפות?
```

#### **5.2 יצירת Backlog**:
```markdown
## Secret Migration Backlog

### P0 - Critical (do now):
- [ ] config/app.yaml - prod password (line 42)
- [ ] config/db.json - API token (line 15)

### P1 - High (this week):
- [ ] scripts/setup.sh - API key (line 8)
- [ ] config/staging.yaml - password (line 55)

### P2 - Medium (this month):
- [ ] docs/SETUP.md - example credentials (line 102)

### False Positives (ignore):
- [x] config/template.yaml - placeholder only
- [x] tests/mock_data.json - test data
```

#### **5.3 החלטה עקרונית** (אם רלוונטי):

אם יש החלטה כללית (למשל: "כל ה-config/ צריך מיגרציה"):
- הפעל **WF-002** (Decision Logging)
- תעד ב-`DECISIONS_AI_OS.md`
- עדכן `SYSTEM_SNAPSHOT.md`

**פלט**: תוכנית פעולה + החלטה מתועדת

---

## Safety & Boundaries

### 🚫 **WF-003 לעולם לא**:

1. **משנה קבצים**
   - אין עריכה
   - אין כתיבה
   - אין מחיקה

2. **מציג סיקרטים**
   - לא ערך מלא
   - לא ערך חלקי
   - רק ציון "נמצא"

3. **נכנס ל-OFF LIMITS**
   - `SECRETS/` - אסור לגמרי
   - כל תיקייה שמסומנת OFF LIMITS
   - קבצים encrypted

4. **מבצע פעולות אוטומטיות**
   - אין מיגרציה אוטומטית
   - אין רוטציה אוטומטית
   - רק discovery

### ✅ **WF-003 תמיד**:

1. **מכבד מדיניות**
   - עוקב אחרי SEC-001
   - עוקב אחרי גבולות גזרה
   - דורש אישור אנושי

2. **מדווח בבטחה**
   - ציון מיקום (file + line)
   - סוג חשד (type)
   - רמת ביטחון (confidence)
   - המלצה (recommendation)

3. **מתעד הכל**
   - דוח מלא
   - תאריך + scope
   - ממצאים + החלטות

---

## דוגמאות (Examples)

### **דוגמה 1: סריקת config/ בריפו הישן**

**Scope**:
```
Repo: make-ops-clean
Path: config/
Files: *.yaml, *.json
Recursive: Yes (max depth 2)
```

**Execution**:
```
1. אור: "בוא נסרוק את config/ לחיפוש סיקרטים"
2. Claude: "מוכן. Scope: config/*.{yaml,json}. מאשר?"
3. אור: "כן"
4. Claude: [סורק...]
   - נמצא: config/app.yaml, line 42, type:password, confidence:high
   - נמצא: config/db.json, line 15, type:token, confidence:high
   - נמצא: config/test.yaml, line 8, type:api_key, confidence:medium
5. Claude: "סיימתי. 3 ממצאים. האם לייצר דוח?"
6. אור: "כן"
7. Claude: [יוצר docs/SECURITY_DISCOVERY_REPORT_2025-11-20.md]
```

**תוצאה**:
- ✅ דוח מסודר
- ✅ אין ערכי סיקרטים בצ'אט
- ✅ רשימה ברורה למיגרציה

---

### **דוגמה 2: אודיט מהיר של ai-os**

**Scope**:
```
Repo: ai-os
Path: ./ (root)
Files: *.md, *.yaml, *.json
Recursive: Yes
```

**Execution**:
```
1. אור: "בוא נוודא שאין סיקרטים ב-ai-os"
2. Claude: [סורק...]
   - לא נמצאו ממצאים
3. Claude: "סריקה הושלמה. 0 ממצאים. ai-os נקי!"
```

**תוצאה**:
- ✅ וולידציה ש-ai-os בטוח
- ✅ אפשר לתעד בSYSTEM_SNAPSHOT

---

### **דוגמה 3: False Positive**

**Finding**:
```
File: config/template.yaml
Line: 10
Type: password
Pattern: "password: ${PASSWORD}"
Confidence: Medium
```

**אור מחליט**:
```
"זה template עם placeholder, לא סיקרט אמיתי"
→ מסמן כ-False Positive
→ לא נכנס ל-Migration Backlog
```

---

## Integration עם Workflows אחרים

### **עם WF-002 (Decision Logging)**:

```
Discovery → החלטה עקרונית → WF-002

דוגמה:
1. WF-003: מצא 12 קבצים ב-config/ עם סיקרטים
2. אור מחליט: "כל ה-config/ צריך מיגרציה"
3. הפעלת WF-002:
   - החלטה: "Secret Migration for config/"
   - Impact: SYSTEM_SNAPSHOT, SECURITY_POLICY
   - Follow-up: יצירת WF-004
```

---

### **עם WF-004 (Secret Migration)** - עתידי:

```
Discovery → Backlog → Migration

דוגמה:
1. WF-003: יצר backlog של 8 קבצים P0
2. אור: "בוא נמגר את 3 הראשונים"
3. הפעלת WF-004:
   - Input: רשימת 3 קבצים
   - Process: מיגרציה מבוקרת
   - Output: קבצים מעודכנים + secrets ב-GitHub Secrets
```

---

### **עם Security Policy**:

```
Discovery → עדכון Policy

אם נמצא pattern חדש שלא היה ב-policy:
1. תעד אותו בדוח
2. הוסף ל-SEC-001 (SECURITY_SECRETS_POLICY)
3. השתמש בו בסריקות עתידיות
```

---

## Failure Modes & Recovery

### **כשל #1: נמצא סיקרט בצ'אט בטעות**

**תסמינים**:
- Claude הדפיס ערך של סיקרט

**פתרון**:
1. **מיד עצור**
2. נקה את הצ'אט (אם אפשר)
3. רוטט את הסיקרט (יצירת חדש)
4. תעד incident בSEC-001
5. שפר patterns למניעה

---

### **כשל #2: סריקה של OFF LIMITS zone**

**תסמינים**:
- בטעות נכנסו ל-SECRETS/

**פתרון**:
1. **מיד עצור**
2. אל תדווח על ממצאים
3. בדוק אם הוצגו ערכים
4. אם כן → רוטט הכל
5. עדכן scope definitions

---

### **כשל #3: יותר מדי False Positives**

**תסמינים**:
- 90% מהממצאים לא אמיתיים

**פתרון**:
1. שפר patterns (יותר ספציפיים)
2. הוסף exclusions (למשל: test/, mock/)
3. הגדל confidence threshold
4. תעד שיפורים לעתיד

---

## Metrics & Success Criteria

### **KPIs**:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Scan Coverage** | 100% of defined scope | Files scanned / Total files |
| **False Positive Rate** | < 20% | False positives / Total findings |
| **Discovery Accuracy** | > 90% | True positives / Actual secrets |
| **Time to Report** | < 1 hour | Scan start → Report ready |
| **Zero Secret Exposure** | 0 leaks | No secret values in output |

---

### **Success Criteria**:

✅ **הצלחה מלאה אם**:
1. כל הקבצים בscope נסרקו
2. דוח נוצר בלי ערכי סיקרטים
3. ממצאים מסווגים לפי עדיפות
4. יש תוכנית follow-up ברורה
5. אין חשיפת סיקרטים בתהליך

---

## Roadmap

### **שלב 1: Discovery ידני** (נוכחי) ✅

**מה יש**:
- Workflow מוגדר
- Patterns מוכנים
- תהליך ברור

**מה חסר**:
- ביצוע בפועל (ממתין לאישור)

---

### **שלב 2: WF-004 - Secret Migration** (הבא) 🔄

**מה יבוא**:
- Workflow למיגרציה מבוקרת
- תהליך רוטציה
- ולידציה אוטומטית

**תנאים**:
1. WF-003 רץ לפחות פעם אחת
2. יש backlog מתועד
3. יש החלטה ב-DECISIONS_AI_OS

---

### **שלב 3: אוטומציה חלקית** (עתיד רחוק) 🔮

**מה אפשרי**:
- Pre-commit hooks (בדיקה לפני commit)
- Scheduled scans (סריקה שבועית)
- CI/CD integration

**תנאים**:
1. WF-003 + WF-004 פועלים מעולה
2. 0 false alarms במשך חודש
3. אישור מפורש מאור

---

## Templates

### **תבנית Scope Definition**:

```yaml
scope:
  repo: make-ops-clean
  base_path: C:\Users\edri2\Downloads\make-ops-clean
  include:
    directories:
      - config/
      - scripts/
    file_types:
      - "*.yaml"
      - "*.json"
      - "*.env"
  exclude:
    directories:
      - SECRETS/  # OFF LIMITS
      - node_modules/
      - .git/
    files:
      - "*.test.*"
      - "*.mock.*"
  options:
    recursive: true
    max_depth: 3
    follow_symlinks: false
```

---

### **תבנית Finding Report**:

```markdown
## Finding #[NUMBER]

**File**: config/app.yaml  
**Line**: 42  
**Type**: password  
**Pattern**: `password: ***`  
**Confidence**: High  
**Priority**: P0 (Critical)

**Context**:
```yaml
# Line 40-44 (redacted)
database:
  host: localhost
  password: ***SECRET***  # ← Finding here
  port: 5432
```

**Recommendation**: Migrate to GitHub Secrets  
**Estimated Effort**: 10 minutes  
**Risk if not fixed**: High - Production password exposed
```

---

### **תבנית Discovery Report**:

```markdown
# Secret Discovery Report

**Report ID**: DISC-2025-11-20-001  
**Date**: 2025-11-20 15:30:00  
**Workflow**: WF-003 v1.0  
**Operator**: Claude Desktop  
**Approved by**: אור

---

## Scope

**Repository**: make-ops-clean  
**Base Path**: C:\Users\edri2\Downloads\make-ops-clean  
**Directories**: config/, scripts/  
**File Types**: *.yaml, *.json, *.env  
**Total Files Scanned**: 47

---

## Executive Summary

- **Files with Findings**: 12 (25.5%)
- **Total Findings**: 23
- **High Confidence**: 18 (78%)
- **Critical Priority**: 8 (35%)

---

## Findings by Priority

### P0 - Critical (8 findings)
[תבנית Finding לכל אחד]

### P1 - High (3 findings)
[...]

### P2 - Medium (1 finding)
[...]

---

## Recommendations

1. **Immediate**: Migrate P0 findings (8 files)
2. **This Week**: Migrate P1 findings (3 files)
3. **This Month**: Migrate P2 findings (1 file)
4. **Document**: Use WF-002 for migration decision
5. **Execute**: Use WF-004 for actual migration

---

## Next Steps

- [ ] Review this report
- [ ] Create Migration Backlog
- [ ] Prioritize P0 items
- [ ] Schedule WF-004 execution
- [ ] Update SYSTEM_SNAPSHOT with progress

---

**Status**: ✅ Discovery Complete - Awaiting Decision  
**Follow-up Workflow**: WF-002 (Decision) → WF-004 (Migration)
```

---

## קישורים למסמכים רלוונטיים

- [`policies/SECURITY_SECRETS_POLICY.md`](../policies/SECURITY_SECRETS_POLICY.md) - מדיניות אבטחה
- [`workflows/DECISION_LOGGING_AND_SSOT_UPDATE.md`](./DECISION_LOGGING_AND_SSOT_UPDATE.md) - WF-002
- [`docs/SYSTEM_SNAPSHOT.md`](../docs/SYSTEM_SNAPSHOT.md) - מצב אבטחה נוכחי
- [`tools/TOOLS_INVENTORY.md`](../tools/TOOLS_INVENTORY.md) - כלים זמינים

---

**סטטוס Workflow זה**: ✅ Active & Ready  
**שימוש ראשון**: ממתין לאישור  
**מוכן לביצוע**: כן (תחת פיקוח)

---

## מילות סיום

**זכור**:
- Discovery זה **רק צעד ראשון**
- הפלט זה **רשימה**, לא **ערכים**
- המטרה היא **להבין את המצב**, לא **לתקן מיד**
- Migration יבוא ב-**WF-004**, **לא כאן**

**חשוב**: WF-003 הוא כלי אבחון. תמיד בצעו אותו לפני שמתחילים לשנות דברים! 🔍✨
