# Action Execution Schema – סכמת ביצוע פעולות

**Created**: 2025-11-21  
**Purpose**: הגדרת סכמה מובנית לפעולות טכניות של Claude  
**Status**: ✅ Active

---

## 🎯 מטרת המסמך

מסמך זה מגדיר **סכמה קפדנית** לפעולות שClaude מבצע, כך ש:
- GPT Planner מחזיר actions_for_claude כ-JSON מובנה (לא טקסט חופשי)
- Claude יכול לבצע כל action אוטומטית ללא אינטרפרטציה נוספת
- כל action ניתן לולידציה, לוגינג ולבדיקה

---

## 📐 סכמה כללית

כל Action הוא אובייקט JSON עם השדות הבאים:

```json
{
  "type": "ACTION_TYPE",
  "params": {
    // פרמטרים ספציפיים לסוג ה-action
  },
  "approval": "auto" | "manual",
  "description": "תיאור קצר למה הפעולה הזאת"
}
```

### **שדות חובה**:

| שדה | סוג | תיאור |
|-----|-----|-------|
| `type` | string | סוג הפעולה (מרשימה סגורה) |
| `params` | object | פרמטרים ספציפיים |
| `approval` | enum | "auto" או "manual" |
| `description` | string | הסבר למה הפעולה |

---

## 🔧 סוגי Actions נתמכים

### **1. file.create** - יצירת קובץ חדש

**מתי להשתמש**: כשצריך ליצור קובץ שלא קיים.

**פרמטרים**:
```json
{
  "type": "file.create",
  "params": {
    "path": "workflows/WF-004.md",
    "content": "# WF-004: Token Management\n\n..."
  },
  "approval": "auto",
  "description": "יצירת workflow חדש לניהול טוקנים"
}
```

| פרמטר | חובה | תיאור |
|-------|------|-------|
| `path` | ✅ | נתיב יחסי מroot הריפו |
| `content` | ✅ | תוכן הקובץ המלא |

---

### **2. file.update** - עדכון קובץ קיים

**מתי להשתמש**: כשצריך לערוך קובץ קיים (להוסיף/לשנות תוכן).

**פרמטרים**:
```json
{
  "type": "file.update",
  "params": {
    "path": "docs/SYSTEM_SNAPSHOT.md",
    "edits": [
      {
        "old_text": "## 3 workflows",
        "new_text": "## 4 workflows"
      }
    ]
  },
  "approval": "auto",
  "description": "עדכון מספר workflows ב-SYSTEM_SNAPSHOT"
}
```

| פרמטר | חובה | תיאור |
|-------|------|-------|
| `path` | ✅ | נתיב יחסי מroot הריפו |
| `edits` | ✅ | רשימת edits (old_text → new_text) |

**הערות**:
- כל edit חייב להכיל `old_text` (טקסט להחלפה) ו-`new_text` (טקסט חדש)
- `old_text` חייב להופיע **בדיוק פעם אחת** בקובץ
- שימוש ב-`Filesystem:edit_file` בפועל

---

### **3. file.delete** - מחיקת קובץ

**מתי להשתמש**: כשצריך למחוק קובץ (נדיר! דורש אישור).

**פרמטרים**:
```json
{
  "type": "file.delete",
  "params": {
    "path": "temp/old_file.txt"
  },
  "approval": "manual",
  "description": "מחיקת קובץ זמני ישן"
}
```

| פרמטר | חובה | תיאור |
|-------|------|-------|
| `path` | ✅ | נתיב יחסי מroot הריפו |

**⚠️ חשוב**: תמיד `approval: "manual"` למחיקות!

---

### **4. git.commit** - יצירת commit

**מתי להשתמש**: אחרי שינויים בקבצים, לפני push.

**פרמטרים**:
```json
{
  "type": "git.commit",
  "params": {
    "files": [
      "workflows/WF-004.md",
      "docs/SYSTEM_SNAPSHOT.md"
    ],
    "message": "Add WF-004: Token Management workflow"
  },
  "approval": "auto",
  "description": "commit של workflow חדש + עדכון תיעוד"
}
```

| פרמטר | חובה | תיאור |
|-------|------|-------|
| `files` | ✅ | רשימת קבצים ל-`git add` |
| `message` | ✅ | הודעת commit |

**הערות**:
- הודעה צריכה להיות בפורמט: `type: description`
- דוגמאות: `feat: ...`, `docs: ...`, `fix: ...`

---

### **5. git.push** - העלאה ל-GitHub

**מתי להשתמש**: אחרי commit, כשרוצים לפרסם שינויים.

**פרמטרים**:
```json
{
  "type": "git.push",
  "params": {},
  "approval": "auto",
  "description": "העלאת שינויים לגיטהאב"
}
```

**הערות**:
- אין פרמטרים נוספים
- תמיד רץ על main branch

---

### **6. workflow.run** - הרצת workflow קיים

**מתי להשתמש**: כשצריך להפעיל WF-001/002/003 או workflow אחר.

**פרמטרים**:
```json
{
  "type": "workflow.run",
  "params": {
    "workflow_id": "WF-002",
    "inputs": {
      "decision_title": "הוספת WF-004",
      "decision_context": "..."
    }
  },
  "approval": "manual",
  "description": "הפעלת WF-002 לתיעוד החלטה"
}
```

| פרמטר | חובה | תיאור |
|-------|------|-------|
| `workflow_id` | ✅ | מזהה workflow (WF-001/002/003) |
| `inputs` | ❌ | קלט ספציפי ל-workflow |

---

### **7. validation.check** - בדיקת תקינות

**מתי להשתמש**: כשרוצים לוודא שמשהו תקין לפני המשך.

**פרמטרים**:
```json
{
  "type": "validation.check",
  "params": {
    "check_type": "file_exists",
    "target": "workflows/WF-004.md"
  },
  "approval": "auto",
  "description": "וידוא שהקובץ נוצר בהצלחה"
}
```

| פרמטר | חובה | תיאור |
|-------|------|-------|
| `check_type` | ✅ | סוג הבדיקה (file_exists, syntax_check, etc) |
| `target` | ✅ | מה לבדוק |

---

## 🔒 מדיניות Approval

### **Approval Types**:

| ערך | משמעות | מתי להשתמש |
|-----|---------|------------|
| `"auto"` | Claude מבצע אוטומטית | פעולות בטוחות וחוזרות |
| `"manual"` | דורש אישור מפורש מאור | פעולות הרסניות או קריטיות |

### **כללי Approval**:

1. **תמיד `auto`**:
   - file.create (קבצים חדשים)
   - file.update (עדכון קבצים קיימים)
   - git.commit
   - git.push
   - validation.check

2. **תמיד `manual`**:
   - file.delete (מחיקה)
   - workflow.run (הפעלת תהליכים מורכבים)
   - כל פעולה שנוגעת ב-SECRETS/
   - כל פעולה שמשנה קבצים קריטיים (CONSTITUTION, DECISIONS)

3. **תלוי בהקשר**:
   - עדכון קבצי מדיניות → `manual`
   - עדכון תיעוד רגיל → `auto`

---

## 📊 דוגמאות מעשיות

### **דוגמה 1: יצירת workflow חדש**

**Intent**: "צור workflow חדש לניהול טוקנים"

**Actions**:
```json
[
  {
    "type": "file.create",
    "params": {
      "path": "workflows/TOKEN_MANAGEMENT.md",
      "content": "# WF-004: Token Management\n\n## Purpose\nManage API tokens securely...\n\n## Steps\n1. Identify tokens\n2. Store in secure location\n3. Rotate periodically"
    },
    "approval": "auto",
    "description": "יצירת קובץ workflow WF-004"
  },
  {
    "type": "file.update",
    "params": {
      "path": "docs/SYSTEM_SNAPSHOT.md",
      "edits": [
        {
          "old_text": "├── workflows/                   ✅ 1 workflow פעיל",
          "new_text": "├── workflows/                   ✅ 2 workflows פעילים"
        }
      ]
    },
    "approval": "auto",
    "description": "עדכון SYSTEM_SNAPSHOT עם WF-004"
  },
  {
    "type": "workflow.run",
    "params": {
      "workflow_id": "WF-002",
      "inputs": {
        "decision_title": "הוספת WF-004: Token Management"
      }
    },
    "approval": "manual",
    "description": "תיעוד החלטה על workflow חדש"
  },
  {
    "type": "git.commit",
    "params": {
      "files": [
        "workflows/TOKEN_MANAGEMENT.md",
        "docs/SYSTEM_SNAPSHOT.md"
      ],
      "message": "feat: add WF-004 Token Management workflow"
    },
    "approval": "auto",
    "description": "commit של כל השינויים"
  },
  {
    "type": "git.push",
    "params": {},
    "approval": "auto",
    "description": "העלאה לגיטהאב"
  }
]
```

---

### **דוגמה 2: עדכון תיעוד פשוט**

**Intent**: "עדכן את README עם הסבר על Intent Router"

**Actions**:
```json
[
  {
    "type": "file.update",
    "params": {
      "path": "README.md",
      "edits": [
        {
          "old_text": "## Architecture\n\nAI-OS consists of:",
          "new_text": "## Architecture\n\nAI-OS consists of:\n\n### Intent Router\nHigh-level orchestration layer that routes user intents to appropriate components."
        }
      ]
    },
    "approval": "auto",
    "description": "הוספת הסבר על Intent Router"
  },
  {
    "type": "git.commit",
    "params": {
      "files": ["README.md"],
      "message": "docs: add Intent Router explanation to README"
    },
    "approval": "auto",
    "description": "commit של עדכון README"
  },
  {
    "type": "git.push",
    "params": {},
    "approval": "auto",
    "description": "העלאה לגיטהאב"
  }
]
```

---

### **דוגמה 3: יצירת סוכן חדש (מורכב)**

**Intent**: "בנה לי סוכן Gmail שבודק מיילים VIP"

**Actions**:
```json
[
  {
    "type": "file.create",
    "params": {
      "path": "agents/GMAIL_VIP_AGENT.md",
      "content": "# Gmail VIP Agent\n\n## Purpose\nMonitor Gmail for VIP messages...\n\n## Capabilities\n- Read Gmail via MCP\n- Filter by sender/subject\n- Send notifications"
    },
    "approval": "auto",
    "description": "יצירת תיעוד סוכן"
  },
  {
    "type": "file.create",
    "params": {
      "path": "ai_core/agents/gmail_vip.py",
      "content": "#!/usr/bin/env python3\n\"\"\"Gmail VIP Agent\"\"\"\n\nfrom typing import List\n\ndef check_vip_emails() -> List[dict]:\n    # Implementation\n    pass"
    },
    "approval": "auto",
    "description": "יצירת קוד הסוכן"
  },
  {
    "type": "file.update",
    "params": {
      "path": "agents/AGENTS_INVENTORY.md",
      "edits": [
        {
          "old_text": "## Active Agents",
          "new_text": "## Active Agents\n\n### Gmail VIP Agent\n- **File**: `agents/GMAIL_VIP_AGENT.md`\n- **Status**: Active"
        }
      ]
    },
    "approval": "auto",
    "description": "עדכון רשימת סוכנים"
  },
  {
    "type": "validation.check",
    "params": {
      "check_type": "file_exists",
      "target": "ai_core/agents/gmail_vip.py"
    },
    "approval": "auto",
    "description": "וידוא שהקוד נוצר"
  },
  {
    "type": "git.commit",
    "params": {
      "files": [
        "agents/GMAIL_VIP_AGENT.md",
        "ai_core/agents/gmail_vip.py",
        "agents/AGENTS_INVENTORY.md"
      ],
      "message": "feat: add Gmail VIP monitoring agent"
    },
    "approval": "auto",
    "description": "commit של סוכן חדש"
  },
  {
    "type": "git.push",
    "params": {},
    "approval": "auto",
    "description": "העלאה לגיטהאב"
  }
]
```

**הערה**: סוכן זה דורש גם OAuth setup ידני מאור (לא ב-actions).

---

### **דוגמה 4: מחיקה (דורשת אישור)**

**Intent**: "מחק קבצים ישנים מ-temp/"

**Actions**:
```json
[
  {
    "type": "file.delete",
    "params": {
      "path": "temp/old_test.py"
    },
    "approval": "manual",
    "description": "מחיקת קובץ בדיקה ישן"
  },
  {
    "type": "file.delete",
    "params": {
      "path": "temp/debug.log"
    },
    "approval": "manual",
    "description": "מחיקת לוג זמני"
  },
  {
    "type": "git.commit",
    "params": {
      "files": ["."],
      "message": "chore: clean up temp files"
    },
    "approval": "manual",
    "description": "commit של מחיקות"
  },
  {
    "type": "git.push",
    "params": {},
    "approval": "auto",
    "description": "העלאה לגיטהאב"
  }
]
```

**⚠️ שים לב**: כל מחיקה דורשת `approval: "manual"`!

---

## ✅ ולידציה

### **כללי ולידציה**:

1. **type חייב להיות מהרשימה הסגורה**:
   - file.create
   - file.update
   - file.delete
   - git.commit
   - git.push
   - workflow.run
   - validation.check

2. **params חייבים להכיל שדות חובה**:
   - לכל type יש פרמטרים שונים (ראה למעלה)
   - שדה חסר → Error

3. **approval חייב להיות "auto" או "manual"**

4. **description חובה** (string לא ריק)

5. **paths חייבים להיות יחסיים** (לא מוחלטים):
   - ✅ `workflows/WF-004.md`
   - ❌ `/home/user/ai-os/workflows/WF-004.md`
   - ❌ `C:\Users\...\workflows\WF-004.md`

---

## 🚫 דוגמאות לא תקינות

### ❌ דוגמה 1: type לא קיים
```json
{
  "type": "file.modify",  // ❌ אין כזה type!
  "params": {...}
}
```
**Error**: `Unknown action type: file.modify. Use file.update instead.`

---

### ❌ דוגמה 2: פרמטר חסר
```json
{
  "type": "file.create",
  "params": {
    "path": "test.md"
    // ❌ חסר "content"!
  }
}
```
**Error**: `Missing required param: content for action type file.create`

---

### ❌ דוגמה 3: approval לא חוקי
```json
{
  "type": "file.delete",
  "params": {...},
  "approval": "yes"  // ❌ חייב להיות "auto" או "manual"
}
```
**Error**: `Invalid approval value: yes. Must be 'auto' or 'manual'.`

---

## 🔄 תאימות עם HUMAN_TECH_INTERACTION_POLICY

סכמה זו מיושרת מלאה עם `HUMAN_TECH_INTERACTION_POLICY.md`:

| עיקרון מדיניות | איך הסכמה מכבדת |
|----------------|-----------------|
| **אור לא עושה טכני** | כל action מבוצע ע"י Claude |
| **Human-in-the-loop** | `approval: "manual"` לפעולות קריטיות |
| **Thin Slices** | כל action הוא פעולה אחת קטנה |
| **שקיפות** | כל action יש לו `description` ברור |
| **אבטחה** | מחיקות תמיד דורשות אישור |

---

## 📝 הרחבות עתידיות

סוגי actions נוספים שאפשר להוסיף:

- `tool.install` - התקנת כלי (npm, pip, etc)
- `api.call` - קריאה ל-API חיצוני
- `mcp.invoke` - הפעלת MCP ישירות
- `test.run` - הרצת בדיקות
- `notification.send` - שליחת התראה

---

**Document Status**: ✅ Active  
**Version**: 1.0  
**Last Updated**: 2025-11-21  
**Next Review**: לאחר שימוש ראשון בביצוע אוטומטי
