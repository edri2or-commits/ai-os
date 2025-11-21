# Tool Limitations - מגבלות כלים טכניים

**Created**: 2025-11-21  
**Purpose**: תיעוד מגבלות הכלים הטכניים של Claude וכיצד לעקוף אותן  
**Status**: Active

---

## 🎯 מטרת המסמך

מסמך זה מתעד מגבלות ידועות בכלים שClaude משתמש בהם, כדי:
- לא לבזבז זמן על ניסיונות שידועים כנכשלים
- להציע פתרונות עיצוביים במקום workarounds טכניים
- לשמור על העיקרון: **אור לא עושה שום פעולה טכנית**

---

## 🚫 מגבלות ידועות

### **1. Tunnel Services (Cloudflare/ngrok) - Authentication Required**

**תיאור המגבלה**:
- Cloudflare Tunnel דורש login דרך דפדפן (OAuth)
- ngrok דורש API token (נרכש אחרי הרשמה)
- LocalTunnel לא יציב מספיק לשימוש production

**מה לא אפשרי**:
- ❌ Claude לא יכול לפתוח דפדפן ולהתחבר
- ❌ Claude לא יכול להירשם לשירותים חדשים
- ❌ Claude לא יכול לקבל tokens אוטומטית

**פתרון עיצובי**: 
→ **אור צריך לבצע הרשמה חד-פעמית, ואז Claude ישתמש ב-token**

**תיעוד הפתרון**: `docs/PUBLIC_HTTPS_SETUP.md`

---

### **2. Environment Variables - No Persistent Session**

**תיאור המגבלה**:
- Claude יכול להגדיר `set VARIABLE=value` ב-cmd
- אבל זה תקף רק לחלון הפקודה הנוכחי
- אין דרך לעדכן system environment באופן קבוע

**מה לא אפשרי**:
- ❌ הגדרת OPENAI_API_KEY קבועה
- ❌ הגדרת tokens קבועות
- ❌ שמירת קונפיגורציה בין הרצות

**פתרון עיצובי**:
→ **שימוש ב-.env files + python-dotenv**

---

### **3. Browser/GUI Operations - No Visual Access**

**תיאור המגבלה**:
- Claude לא יכול לפתוח דפדפן
- Claude לא יכול ללחוץ על כפתורים ב-GUI
- Claude לא יכול להזין credentials באתרים

**מה לא אפשרי**:
- ❌ Login לשירותים דרך דפדפן
- ❌ OAuth flows
- ❌ CAPTCHA solving

**פתרון עיצובי**:
→ **אור מבצע setup חד-פעמי, Claude משתמש ב-CLI/API**

---

## ✅ פתרונות מומלצים

### **Tunnel Setup - המלצה**

**תהליך מומלץ**:

1. **אור מבצע (פעם אחת)**:
   ```bash
   # Install Cloudflare Tunnel
   winget install Cloudflare.cloudflared
   
   # Login (opens browser)
   cloudflared tunnel login
   
   # Create tunnel
   cloudflared tunnel create ai-os-gateway
   
   # Get tunnel ID
   cloudflared tunnel list
   ```

2. **Claude ממשיך**:
   - קורא את ה-tunnel ID מהפלט
   - יוצר config.yml
   - מפעיל את ה-tunnel
   - מחזיר PUBLIC_URL

**תיעוד מלא**: `docs/PUBLIC_HTTPS_SETUP.md`

---

### **Environment Variables - המלצה**

**במקום `set` זמני, שימוש ב-.env**:

```python
# .env file
OPENAI_API_KEY=sk-...
TUNNEL_TOKEN=...

# Python code
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
```

**יתרונות**:
- ✅ קובץ `.env` נשמר בין הרצות
- ✅ לא נכנס ל-git (בזכות `.gitignore`)
- ✅ Claude יכול לקרוא/לכתוב אותו

---

## 📝 תהליך מומלץ לפיצ'רים חדשים

כשצריך פיצ'ר שדורש external service:

1. **Claude מזהה מגבלה** → מעבר ל-DESIGN mode
2. **Claude יוצר**:
   - מסמך setup (`docs/FEATURE_SETUP.md`)
   - הוראות ברורות לאור (צעדים מינימליים)
   - סקריפט שClaude ירוץ אחרי שאור סיים
3. **אור מבצע setup** (פעם אחת, מינימלי)
4. **Claude ממשיך** עם ה-automation

---

## 🎯 עקרונות תיעוד מגבלות

כשמזהים מגבלה חדשה:

1. **תעד כאן** (TOOL_LIMITATIONS.md)
2. **הסבר למה** זה לא אפשרי
3. **הצע פתרון עיצובי** (לא workaround)
4. **צור מסמך setup** נפרד אם צריך
5. **שמור על העיקרון**: אור עושה מינימום, Claude מקסימום

---

**Document Status**: ✅ Active  
**Last Updated**: 2025-11-21  
**Next Review**: When new limitations discovered
