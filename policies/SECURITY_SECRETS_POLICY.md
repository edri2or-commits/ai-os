# AI-OS – מדיניות סיקרטים ואבטחה (Security & Secrets Policy)

**Policy ID**: SEC-001  
**גרסה**: 1.0  
**תאריך יצירה**: 20 נובמבר 2025  
**סטטוס**: ✅ Active & Binding

---

## מטרות המדיניות

מדיניות זו נועדה ל:

1. **להגן על מידע רגיש** - סיסמאות, טוקנים, מפתחות API וגישה לכלים חיצוניים
2. **להגדיר גבולות ברורים** - מה מותר ומה אסור לכל סוכן/כלי ב-AI-OS
3. **למנוע חשיפת סיקרטים** - בצ'אטים, בלוגים, בקבצי Markdown או ב-commits
4. **לספק נהלי עבודה בטוחים** - איך מתקרבים לתיקיות/קבצים רגישים
5. **לאפשר אודיט** - מעקב אחר גישה למידע רגיש

---

## היקף המדיניות

מדיניות זו חלה על:

### **ריפואים**:
- ✅ `ai-os` (הריפו הנוכחי)- ✅ כל ריפו עתידי שיהיה חלק ממערכת AI-OS

### **כלים וממשקים**:
- ✅ GitHub (repos, secrets, tokens)
- ✅ Google Workspace (Gmail, Calendar, Drive)
- ✅ Make.com (אם בשימוש)
- ✅ Telegram Bot (אם בשימוש)
- ✅ GPT API
- ✅ Cloud Run / GCP (אם יפרוס)
- ✅ כל אינטגרציה חיצונית אחרת

### **סוכנים וכלי עזר**:
- ✅ Claude Desktop
- ✅ GPT GitHub Agent
- ✅ MCP Servers (GitHub, Filesystem, Windows, Google)
- ✅ כל סוכן/כלי עתידי

---

## עקרונות יסוד (Core Principles)

### **עקרון #1: No Secrets in Plain Text**
> **"אף פעם לא שומרים סיקרטים בטקסט חופשי"**

- ❌ **אסור** לשמור סיקרטים ב:
  - קבצי Markdown (`.md`)
  - קבצי תיעוד (`.txt`, `.doc`)
  - קבצי קוד (`.py`, `.js`, `.sh`) ללא הצפנה
  - קבצי config (`.yaml`, `.json`) ללא placeholder
  - Commit messages
  - Issue/PR descriptions
  - Chat logs / conversation history

- ✅ **מותר** לשמור סיקרטים רק ב:
  - GitHub Secrets (repository/organization)
  - Environment Variables (`.env` לא בגיט!)
  - Secret Manager חיצוני (Google Secret Manager, AWS Secrets Manager)
  - Encrypted vaults (1Password, Bitwarden, וכו')
  - Local secure storage (Claude App, OS Keychain)

---

### **עקרון #2: Never Display Secrets**
> **"אף פעם לא מציגים סיקרטים בצ'אט"**

כשסוכן/כלי פוגש סיקרט:

- ✅ **מותר**:
  - לזהות שקיים סיקרט: "נמצא GitHub PAT בקובץ X"
  - להציג placeholder: `***SECRET***` או `${GITHUB_TOKEN}`
  - לדווח על מיקום: "הטוקן צריך להיות ב-Environment Variable"
  - לספור: "נמצאו 3 סיקרטים בתיקייה"

- ❌ **אסור**:
  - להציג ערך מלא: `ghp_1234567890abcdef...`
  - להציג חלקי: `ghp_****ef` (גם זה לא!)
  - להעתיק לצ'אט
  - להעתיק ל-log
  - להעתיק ל-Markdown
  - להעביר בין מודלים/סוכנים

---

### **עקרון #3: Human Authorization Required**
> **"כל פעולה עם סיקרטים דורשת אישור אנושי"**

פעולות הדורשות אישור מפורש:

1. **יצירת סיקרט חדש**
2. **שינוי סיקרט קיים**
3. **מחיקת סיקרט**
4. **העברת סיקרט** בין מערכות
5. **מיגרציה** של סיקרטים inline לסביבה מאובטחת
6. **גישה לתיקיות רגישות** (`SECRETS/`, `config/` עם secrets)

**תהליך אישור**:
1. הסוכן/כלי מציג בקשה מפורטת
2. אור (Human) בוחן ומחליט
3. רק אחרי אישור מפורש - מתבצע
4. תיעוד בלוג החלטות (אם משמעותי)

---

### **עקרון #4: Minimal Privilege**
> **"כל סוכן/כלי מקבל רק את ההרשאות שהוא צריך"**

רמות גישה:

| Level | Description | Examples |
|-------|-------------|----------|
| **Public** | מידע פומבי | README, docs, public repos |
| **Internal** | מידע פנימי לא רגיש | Code, configs ללא secrets |
| **Confidential** | מידע רגיש | Logs עם PII, business data |
| **Secret** | מידע קריטי | Tokens, passwords, keys |

**כלל**: סוכן שלא צריך גישה ל-Secrets - לא מקבל אותה.

---

## תיקיות וקבצים רגישים (High Risk Zones)

### 🚨 **Zone 1: SECRETS/ Directory**


**Classification**: **CRITICAL - OFF LIMITS**

**Rules**:
- ❌ **אסור** לפתוח קבצים בתיקייה זו
- ❌ **אסור** להציג תוכן בצ'אט
- ❌ **אסור** לקרוא אפילו שמות קבצים פנימיים
- ✅ **מותר** רק לציין: "התיקייה קיימת ומכילה חומר רגיש"

**Access Protocol**:
1. אם יש צורך בגישה - לתכנן תחילה
2. ליצור תוכנית מיגרציה מפורטת
3. לקבל אישור מפורש מאור
4. לבצע במנותק מצ'אטים (local script עם הצפנה)

**Future Plan**:
- התיקייה תיסגר/תימחק לאחר מיגרציה מלאה
- כל התוכן יועבר למערכת Secrets מאובטחת
- התיקייה לא תיכנס אף פעם ל-`ai-os`

---

### ⚠️ **Zone 2: config/ Directory**


**Classification**: **HIGH RISK - Potential Inline Secrets**

**Known Issues**:
- ייתכן קבצי YAML/JSON עם secrets inline
- לא נסרקו עדיין בצורה מקיפה
- דורשים סקירת אבטחה דחופה

**Scanning Protocol**:

כשסורקים קובץ מ-`config/`:

1. **לא מדפיסים ערכים** - רק מזהים דפוסים
2. **מחפשים patterns**:
   ```
   - password: ...
   - token: ...
   - api_key: ...
   - secret: ...
   - credentials: ...
   - auth: ...
   ```
3. **מדווחים**: "נמצא/לא נמצא סיקרט inline בקובץ X"
4. **אם נמצא** - מציעים מיגרציה (לא מציגים ערך!)

**Migration Plan** (עתידי):
```yaml
# Before:
github:
  token: ghp_1234567890abcdef...

# After:
github:
  token: ${GITHUB_TOKEN}
```

**Action Required**:
- [ ] סריקה מלאה של `config/`
- [ ] רשימת קבצים עם secrets
- [ ] תוכנית מיגרציה
- [ ] ביצוע + validation
- [ ] תיעוד במסמך החלטות

---

### ⚠️ **Zone 3: Other Sensitive Files**

**Potential Locations**:
- `*.env` files
- `secrets.yaml` / `secrets.json`
- `credentials.*`
- `.git-credentials`
- `auth-config.*`
- Anywhere with "secret", "password", "token" in filename

**Detection Rules**:

כשפוגשים קובץ חשוד:

1. **Check filename patterns**:
   - `*secret*`, `*password*`, `*token*`, `*key*`, `*auth*`
   - `.env*`, `credentials*`

2. **Check content patterns**:
   - `password =`
   - `token :`
   - `api_key:`
   - `secret_key =`
   - Base64 strings (long alphanumeric)
   - JWT tokens (starts with `ey...`)
   - GitHub tokens (starts with `ghp_`, `gho_`, `ghs_`)
   - AWS keys (starts with `AKIA...`)

3. **Report without showing**:
   - "קובץ X מכיל pattern של סיקרט בשורה Y"
   - "דורש סקירה ידנית"

---

## כללי עבודה לסוכנים (Agent Rules)

### 🤖 **Claude Desktop**

**Permissions**: Full System Access

**Rules**:
- ✅ יכול לקרוא קבצים (בתוך allowed directories)
- ✅ יכול לכתוב קבצים (עם אישור)
- ✅ יכול לגשת ל-GitHub (דרך MCP)
- ⚠️ **חייב לפעול לפי מדיניות זו**
- ❌ לא מציג secrets בצ'אט
- ❌ לא נכנס ל-`SECRETS/` בלי אישור

**When encountering secret**:
```
❌ Bad: "הטוקן שלך הוא: ghp_1234..."
✅ Good: "מצאתי GitHub token בקובץ X, צריך להעביר ל-environment variable"
```

---

### 🧠 **GPT GitHub Agent**

**Permissions**: Planning Only (DRY RUN)

**Rules**:
- ✅ יכול לקרוא SSOT documents
- ✅ יכול לנתח מבנה ריפו
- ✅ יכול להציע תוכניות
- ❌ **אין** write access
- ❌ **אין** גישה ל-secrets
- ❌ לא מבצע פעולות אוטומטית

**When planning with secrets**:
```
❌ Bad: "צעד 1: העתק את הטוקן ghp_123..."
✅ Good: "צעד 1: וודא ש-${GITHUB_TOKEN} מוגדר ב-environment"
```

---

### 🔧 **MCP Servers**

**Permissions**: Varies by server

#### **GitHub MCP**:
- ✅ Read/Write לריפואים
- ✅ גישה דרך OAuth (מנוהל ע"י Claude App)
- ❌ לא חושף את ה-OAuth token

#### **Filesystem MCP**:
- ✅ Read/Write בתוך allowed directories
- ⚠️ צריך לכבד את רשימת ההחרגות:
  - `SECRETS/` → ❌ חסום
  - `config/` → ⚠️ זהירות
  - `.env*` → ⚠️ זהירות

#### **Windows MCP**:
- ✅ פקודות PowerShell מאושרות
- ⚠️ גישה למערכת - דורש זהירות
- ❌ לא מריץ פקודות שחושפות secrets

#### **Google MCP**:
- ✅ Read-only כרגע
- ✅ גישה דרך OAuth (מנוהל ע"י Claude App)
- 🔄 Write יידרש OAuth נוסף

---

## סריקת סיקרטים (Secret Scanning)

### 🔍 **כלים לזיהוי**

**Regex Patterns לזיהוי**:

```regex
# GitHub Tokens
ghp_[a-zA-Z0-9]{36}
gho_[a-zA-Z0-9]{36}
ghs_[a-zA-Z0-9]{36}

# AWS Keys
AKIA[0-9A-Z]{16}

# Generic API Keys
[a-zA-Z0-9_-]{32,}

# JWT Tokens
eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+

# Passwords in config
password\s*[:=]\s*['""][^'""]+['""]
```

**Python Script Example** (לשימוש עתידי):
```python
import re

SECRET_PATTERNS = {
    'github_token': r'ghp_[a-zA-Z0-9]{36}',
    'aws_key': r'AKIA[0-9A-Z]{16}',
    'jwt': r'eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+',
}

def scan_file(filepath):
    """
    Scan file for secrets.
    Returns: list of findings (WITHOUT showing values!)
    """
    findings = []
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            for secret_type, pattern in SECRET_PATTERNS.items():
                if re.search(pattern, line):
                    findings.append({
                        'file': filepath,
                        'line': line_num,
                        'type': secret_type,
                        # DON'T include the actual value!
                    })
    return findings
```

---

### 📋 **תהליך סריקה**

**Phase 1: Discovery**
1. זיהוי קבצים חשודים
2. סריקה עם patterns
3. יצירת רשימה (בלי ערכים!)

**Phase 2: Analysis**
1. סיווג לפי רמת חומרה
2. החלטה: real secret או false positive?
3. תעדוף לפי criticality

**Phase 3: Remediation**
1. תוכנית מיגרציה לכל secret
2. ביצוע מבוקר (תחת פיקוח)
3. Validation שהמיגרציה הצליחה

**Phase 4: Prevention**
1. הוספת `.gitignore` rules
2. Pre-commit hooks (אם נדרש)
3. תיעוד ב-policy

---

## מיגרציית סיקרטים (Secret Migration)

### 🔄 **תהליך סטנדרטי**

#### **Step 1: Identification**
```bash
# Scan config directory
  \( -name "*.yaml" -o -name "*.json" \) \
  -exec grep -l "password\|token\|secret\|key" {} \;
```

#### **Step 2: Documentation**
```markdown
# Secret Migration Plan

## Found:
- File: `config/github.yaml`
- Line: 5
- Type: GitHub PAT
- Usage: GitHub API access

## Migration:
- From: inline in YAML
- To: Environment Variable
- Name: `GITHUB_TOKEN`
```

#### **Step 3: Create Secret**
```bash
# Local (for development)
export GITHUB_TOKEN="value_here"

# GitHub Secrets (for production)
gh secret set GITHUB_TOKEN
```

#### **Step 4: Update Config**
```yaml
# Before:
github:
  token: ghp_1234567890abcdef...

# After:
github:
  token: ${GITHUB_TOKEN}
```

#### **Step 5: Validation**
```bash
# Test that it works
python test_github_connection.py
# Should succeed with env var
```

#### **Step 6: Cleanup**
```bash
# Remove old secret from file
git add config/github.yaml
git commit -m "Migrate GitHub token to env var"

# Rotate the old secret (create new one)
# Revoke old token on GitHub
```

---

### 📝 **Migration Tracking**

**Document**: `policies/SECRET_MIGRATION_LOG.md` (עתידי)

```markdown
| Date | File | Secret Type | Status | Notes |
|------|------|-------------|--------|-------|
| 2025-11-20 | config/github.yaml | GitHub PAT | ✅ Done | Migrated to env |
| 2025-11-20 | config/google.yaml | OAuth | 🔄 In Progress | Waiting for new scopes |
```

---

## אחריות (Responsibilities)

### 👤 **אור (Human)**

**Responsibilities**:
- ✅ אישור כל שינוי במדיניות
- ✅ אישור כל פעולה עם secrets
- ✅ החלטה על מיגרציות
- ✅ ניהול secret stores (GitHub Secrets, env vars)
- ✅ סקירת ממצאי אבטחה

**Authority**:
- החלטה סופית על כל נושא אבטחה
- יכול לעצור כל workflow שמסכן secrets
- יכול לשנות את המדיניות (עם תיעוד)

---

### 🤖 **Claude Desktop**

**Responsibilities**:
- ✅ ביצוע המדיניות בכל פעולה
- ✅ זיהוי secrets וסימונם
- ✅ דיווח על ממצאים (בלי ערכים!)
- ✅ הצעת תוכניות מיגרציה
- ❌ אסור לו לעקוף את המדיניות

**Escalation**:
- אם רואה secret - מדווח ועוצר
- אם לא בטוח - שואל את אור
- אם יש conflict - המדיניות גוברת

---

### 🧠 **GPT Agents**

**Responsibilities**:
- ✅ תכנון תוך התחשבות במדיניות
- ✅ שימוש ב-placeholders במקום ערכים
- ✅ המלצה על best practices
- ❌ אין להם גישה ישירה ל-secrets
- ❌ אין להם יכולת לבצע מיגרציה

---

### 🔧 **Tools & Integrations**

**Responsibilities**:
- ✅ לנהל secrets דרך מנגנונים מאובטחים
- ✅ לא לרשום secrets בלוגים
- ✅ להשתמש ב-OAuth כשאפשר
- ✅ לסובב secrets במקרה של חשיפה

---

## תרחישי חירום (Emergency Procedures)

### 🚨 **Secret Exposed in Chat**

**What to do**:
1. ⏸️ **עצור מיד** את השיחה
2. 🔄 **Rotate** את הסיקרט (צור חדש, בטל ישן)
3. 🗑️ **נקה** chat history (אם אפשר)
4. 📝 **תעד** incident ב-log
5. 🔍 **בדוק** איפה עוד היה בשימוש
6. ✅ **Update** כל מקום שצריך את החדש

---

### 🚨 **Secret Exposed in Commit**

**What to do**:
1. ⏸️ **עצור** push (אם לא נדחף עדיין)
2. 🔄 **Rotate** הסיקרט מיד
3. 🗑️ **מחק** מהhistory:
   ```bash
   # Use git filter-branch or BFG Repo Cleaner
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch PATH_TO_FILE' \
     --prune-empty --tag-name-filter cat -- --all
   ```
4. ⚠️ **Force push** (זהירות!)
5. 📝 **תעד** incident
6. 🔍 **סקור** כל הriפo לשאר secrets

---

### 🚨 **SECRETS/ Directory Accessed**

**What to do**:
1. ⏸️ **עצור** מיד
2. 🔍 **בדוק** מה נחשף
3. 🔄 **Rotate** כל הsecrets שנגעו בהם
4. 📝 **תעד** מה קרה ולמה
5. 🔒 **חזק** הגנות (permissions, .gitignore)
6. ✅ **Validate** שהמערכת בטוחה

---

## מדדים ומעקב (Metrics & Monitoring)

### 📊 **KPIs**

| Metric | Target | Current |
|--------|--------|---------|
| **Secrets in plain text** | 0 | ❓ TBD |
| **Config files scanned** | 100% | 0% |
| **Secrets migrated** | 100% | 0% |
| **Security incidents** | 0 | 0 |
| **Policy violations** | 0 | 0 |

---

### 📋 **Audit Log**

**Template**: `policies/SECURITY_AUDIT_LOG.md` (עתידי)

```markdown
| Date | Event | Actor | Result | Notes |
|------|-------|-------|--------|-------|
| 2025-11-20 | Policy Created | Claude | ✅ Success | v1.0 |
| TBD | config/ Scan | Claude | 🔄 Pending | Not started |
```

---

## תוכנית יישום (Implementation Plan)

### **Phase 1: Immediate** (עכשיו)

- [x] יצירת מדיניות זו
- [ ] הוספת `.gitignore` rules:
  ```
  # Secrets
  SECRETS/
  *.env
  .env.*
  *secret*
  *credential*
  ```
- [ ] סימון `SECRETS/` כ-OFF LIMITS
- [ ] הוספת warning ב-README

---

### **Phase 2: Discovery** (שבוע 1)

- [ ] סריקה מלאה של `config/`
- [ ] זיהוי כל הsecrets
- [ ] יצירת רשימת מיגרציה
- [ ] תעדוף לפי criticality

---

### **Phase 3: Migration** (שבוע 2-3)

- [ ] מיגרציה של secrets ל-env vars
- [ ] בדיקת כל מיגרציה
- [ ] עדכון documentation
- [ ] rotation של secrets ישנים

---

### **Phase 4: Validation** (שבוע 4)

- [ ] וידוא שהכל עובד
- [ ] סריקה נוספת לוודא אין שאריות
- [ ] תיעוד שינויים
- [ ] עדכון SSOT

---

### **Phase 5: Prevention** (ongoing)

- [ ] pre-commit hooks
- [ ] automated scanning
- [ ] regular audits
- [ ] policy reviews

---

## שינויים במדיניות (Policy Changes)

**Version History**:

| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| **1.0** | 2025-11-20 | Initial policy creation | אור |

---

**תהליך שינוי**:

1. הצעת שינוי (מי שהוא מזהה צורך)
2. תיעוד הצעה במסמך
3. דיון + אישור אנושי (אור)
4. עדכון המדיניות
5. תקשור לכל הצוותים/סוכנים
6. update גרסה

---

## קישורים למסמכים רלוונטיים

- [`docs/CONSTITUTION.md`](../docs/CONSTITUTION.md) - חוקי יסוד (חוק #7: אבטחה)
- [`docs/CAPABILITIES_MATRIX.md`](../docs/CAPABILITIES_MATRIX.md) - מיפוי כלים וגישות
- [`tools/TOOLS_INVENTORY.md`](../tools/TOOLS_INVENTORY.md) - מיפוי secrets locations
- [`docs/DECISIONS_AI_OS.md`](../docs/DECISIONS_AI_OS.md) - החלטות קריטיות

---

## נספחים (Appendices)

### **נספח A: דוגמאות טובות ורעות**

#### ❌ **דוגמה רעה**:
```markdown
# How to connect to GitHub

1. Get your token: ghp_1234567890abcdef...
2. Export it: `export GITHUB_TOKEN=ghp_123...`
3. Run the script
```

#### ✅ **דוגמה טובה**:
```markdown
# How to connect to GitHub

1. Create a GitHub Personal Access Token with `repo` scope
2. Export it: `export GITHUB_TOKEN=<your_token_here>`
3. Verify: `echo $GITHUB_TOKEN` (you should see it masked)
4. Run the script
```

---

### **נספח B: Glossary**

| Term | Definition |
|------|------------|
| **Secret** | כל מידע שנותן גישה: token, password, API key, certificate |
| **Inline** | secret שנמצא בתוך קובץ קוד/config (לא env var) |
| **Rotation** | החלפת secret ישן בחדש |
| **Migration** | העברת secret ממקום לא מאובטח למאובטח |
| **Placeholder** | מחרוזת שמייצגת secret בלי לחשוף אותו: `${VAR_NAME}` |
| **OAuth** | מנגנון אימות שלא דורש שמירת סיסמה |

---

**סטטוס מדיניות זו**: ✅ Active & Binding  
**חובה על**: כל סוכן, כלי, workflow ב-AI-OS  
**עדכון אחרון**: 20 נובמבר 2025  
**גרסה**: 1.0  
**צעד הבא**: סריקת `config/` וזיהוי secrets
