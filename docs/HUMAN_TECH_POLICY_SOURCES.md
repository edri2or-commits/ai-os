# Human-Tech Policy Sources – מקורות מהריפו הישן

**Created**: 2025-11-21  
**Purpose**: מיפוי מקורות מדיניות "אור לא עושה טכני" מ-make-ops-clean

---

## 🎯 מה המסמך הזה

זהו מיפוי של **כל המקורות** בריפו הישן שמכילים עקרונות של:
- אור לא מבצע פעולות טכניות
- Human-in-the-loop חובה
- Approval gates
- חלוקת אחריות בין אור/סוכנים/כלים

**למה זה חשוב?**
- לא להמציא חוקים - לבסס על מה שכבר היה
- לראות איך זה עבד במערכת הישנה
- להבין את הרציונל

---

## 📋 טבלת מקורות

| Source File | Path | Summary | Relevant to Or Policy | Notes |
|------------|------|---------|----------------------|-------|
| **WINDOWS_MCP_SAFETY_POLICY.md** | `make-ops-clean/` | מדיניות בטיחות Windows MCP | ✅✅✅ HIGH | Human-in-the-loop, Approval phrases |
| **GPT_OS_POLICY.md** | `make-ops-clean/knowledge/` | מדיניות GPT Agent | ✅✅✅ HIGH | "User: NO technical execution" |
| **SECRETS_CLEANUP_PLAYBOOK.md** | `make-ops-clean/` | Playbook לניקוי סיקרטים | ✅✅ MEDIUM | Single/Double approval gates |
| **SECURITY_FINDINGS_SECRETS.md** | `make-ops-clean/` | ממצאי אבטחה | ✅ LOW | Safety measures, audit trail |

---

## 📖 ציטוטים מרכזיים

### 1. WINDOWS_MCP_SAFETY_POLICY.md

#### 1.1 Core Principle - Human-in-the-loop
```markdown
Or reviews and approves:
- Hebrew approval phrase required
- Approval is time-bounded (single session)
- Approval covers specific operation only
```

**רלוונטי ל**: עקרון שאור מאשר אבל לא מבצע

---

#### 1.2 Approval Flow
```markdown
1. Claude proposes operation:
   - Shows exact commands
   - Explains risk/impact
   - Provides audit trail location

2. Or reviews and approves:
   - Hebrew approval phrase required
   - Approval is time-bounded
   - Approval covers specific operation only

3. Claude executes via Windows Shell MCP
```

**רלוונטי ל**: תהליך אישור ברור - אור רק מאשר

---

#### 1.3 Emergency Stop
```markdown
Emergency Stop:
"עצור עכשיו" or "STOP NOW" → Immediate halt
```

**רלוונטי ל**: אור יכול לעצור אבל לא מתקן בעצמו

---

#### 1.4 What Claude MUST NOT Do
```markdown
Claude MUST NOT:
- Try alternate commands without approval
- Escalate privileges
- Modify safety policy without approval
- Continue on error
```

**רלוונטי ל**: סוכן לא עוקף אישור, לא מבקש מאור לעשות workaround טכני

---

### 2. GPT_OS_POLICY.md

#### 2.1 User Role Definition - CRITICAL!
```markdown
**User (Aor):**
- Strategic direction only
- Approval of major changes
- Policy decisions
- NO technical execution
```

**זהו הציטוט המרכזי ביותר!** ⭐

**רלוונטי ל**: הגדרה מפורשת שאור לא עושה טכני

---

#### 2.2 Division of Responsibilities
```markdown
GPT (You):
- Business logic and workflow orchestration
- User interaction and intent parsing
- Data analysis and reporting
- Decision-making within policy bounds

Claude:
- Infrastructure provisioning and management
- MCP server development and deployment
- Cloud resource management
- Emergency system repairs

User (Aor):
- Strategic direction only
- Approval of major changes
- Policy decisions
- NO technical execution
```

**רלוונטי ל**: חלוקה ברורה - אור לא בתשתית ולא בביצוע

---

#### 2.3 What GPT Does NOT Handle
```markdown
For User (Aor):
- Strategic direction only
- Policy approval
- Major architecture decisions
- Emergency authorization
```

**רלוונטי ל**: אור לא מטפל בטכני

---

### 3. SECRETS_CLEANUP_PLAYBOOK.md

#### 3.1 Approval Gates
```markdown
| Phase | Risk | Reversible | Approval |
|-------|------|------------|----------|
| A | None | N/A | ✅ Single |
| B | LOW | ✅ Yes | ✅ Single |
| E | HIGH | ❌ No | ✅✅ Double |
| G | CRITICAL | ❌ No | ✅✅ Double |
```

**רלוונטי ל**: רמות אישור - אור מאשר, לא מבצע

---

#### 3.2 Emergency Stop
```markdown
### Emergency Stop
"עצור עכשיו" or "STOP NOW" → Immediate halt
```

**רלוונטי ל**: אור יכול לעצור תהליכים

---

#### 3.3 Or's Role
```markdown
**Next Step**: אור reviews → Answers open questions → Approves Phase A
```

**רלוונטי ל**: אור עונה על שאלות ומאשר, לא מבצע

---

### 4. SECURITY_FINDINGS_SECRETS.md

#### 4.1 Audit Trail
```markdown
**Remediation Details**:
- Date: 2025-11-11
- Method: Soft delete (moved to quarantine)
- New Storage: Windows Credential Manager
```

**רלוונטי ל**: סוכן/אוטומציה עשתה את העבודה הטכנית, לא אור

---

## 🔑 עקרונות מרכזיים שעולים

### 1. אור לא מבצע טכני - מפורש
**מקור**: GPT_OS_POLICY.md
**ציטוט**: "User (Aor): NO technical execution"

### 2. Human-in-the-loop = אישור, לא ביצוע
**מקור**: WINDOWS_MCP_SAFETY_POLICY.md
**ציטוט**: "Or reviews and approves" + "Claude executes"

### 3. Emergency Stop - עצירה, לא תיקון
**מקור**: WINDOWS_MCP_SAFETY_POLICY.md, SECRETS_CLEANUP_PLAYBOOK.md
**ציטוט**: "עצור עכשיו"

### 4. Approval Levels - Single/Double
**מקור**: SECRETS_CLEANUP_PLAYBOOK.md
**רעיון**: אור מאשר לפי רמת סיכון, לא מבצע

### 5. Rollback - אוטומציה, לא ידני
**מקור**: SECRETS_CLEANUP_PLAYBOOK.md
**רעיון**: "Files remain available until archived" - המערכת מטפלת

---

## 🚫 מה אור לא עושה - רשימה

על בסיס המקורות:

### פעולות שאור לא עושה:
- ❌ הרצת פקודות shell / PowerShell
- ❌ עריכה ידנית של קבצי config
- ❌ העתקה/הדבקה של טוקנים גולמיים
- ❌ יצירה/מחיקה של קבצים בריפו
- ❌ git operations (commit, push, pull)
- ❌ פתיחת consoles / terminals
- ❌ התקנת תוכנות
- ❌ שינוי הגדרות מערכת
- ❌ גישה ישירה לSecret Manager / cloud services
- ❌ תיקון bugs ידני
- ❌ workarounds כשכלים נכשלים

### מה אור כן עושה:
- ✅ ניסוח כוונה והחלטות
- ✅ אישור פעולות (single/double)
- ✅ עצירת תהליכים ("עצור עכשיו")
- ✅ מענה על שאלות
- ✅ קבלת החלטות מדיניות
- ✅ (אופציונלי) לחיצה על כפתור אישור אחד
- ✅ (אופציונלי) הדבקת טוקן פעם אחת במקרי קיצון
- ✅ (אופציונלי) הכנסת קוד 2FA

---

## 📝 מסקנות למדיניות החדשה

### 1. עקרון ברזל
אם סוכן/Workflow מגיע למצב שהוא אומר:
> "אור, תפתח אתר / תריץ פקודה / תעתיק טוקן"

זה **באג ארכיטקטורה**, לא "פתרון".

**התגובה הנכונה**: לתכנן Automation / כלי / Workflow שיפתור את זה.

---

### 2. רמת מעורבות מקסימלית
**מותר**:
- לחיצה על כפתור אישור ✅
- הכנסת קוד חד-פעמי (2FA) ✅
- הדבקת טוקן פעם אחת אם אין שום דרך אחרת ⚠️

**אסור**:
- כתיבה/הרצה של פקודות ❌
- עריכה ידנית של קונפיגים ❌
- שמירה/העתקה של טוקנים לאורך זמן ❌

---

### 3. אישור ≠ ביצוע
אור מאשר:
- Single approval (✅): פעולות הפיכות/read-only
- Double approval (✅✅): פעולות בלתי הפיכות

אבל **תמיד** סוכן/אוטומציה מבצעים, לא אור.

---

### 4. Emergency Powers
אור יכול:
- לעצור ("עצור עכשיו") ✅
- לבטל אישור ✅

אור לא יכול:
- לתקן בעצמו ❌
- לעקוף מדיניות ❌

---

## 🔄 עדכון מסמך זה

**מתי**:
- נמצא מקור נוסף בריפו הישן
- התגלה ציטוט חשוב שלא נכלל
- השתנתה הבנה של מדיניות קיימת

**איך**:
- הוסף שורה לטבלת מקורות
- הוסף ציטוט לסעיף הרלוונטי
- עדכן מסקנות אם נדרש

---

**Status**: ✅ Active  
**Created**: 2025-11-21  
**Based On**: make-ops-clean repo analysis  
**Next**: Create HUMAN_TECH_INTERACTION_POLICY.md based on these sources
