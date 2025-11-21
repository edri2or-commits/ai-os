# AI-OS Setup Guide

**תכל'ס**: איך להפעיל את AI-OS במחשב שלך בלי טריקים.

---

## 🎯 מטרה

להפוך את AI-OS ממשהו ש"עובד בDemo" למערכת יציבה שאתה יכול לסמוך עליה.

---

## ⚡ Quick Start (5 דקות)

### **אופציה 1: Demo Mode (אין צורך ב-API key)**

```bash
# 1. הורד את הקוד (כבר יש לך)
cd C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace

# 2. Run setup
python setup_env.py
# בחר: 1 (Demo Mode)

# 3. התקן dependencies
pip install -r requirements.txt

# 4. הפעל!
python -m ai_core.agent_gateway_server
```

**זהו! השרת רץ על: http://localhost:8000**

---

### **אופציה 2: Real GPT (דורש API key)**

```bash
# 1. הורד את הקוד (כבר יש לך)
cd C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace

# 2. Run setup
python setup_env.py
# בחר: 2 (Real GPT)
# הדבק API key (מ-https://platform.openai.com/api-keys)

# 3. התקן dependencies
pip install -r requirements.txt

# 4. הפעל!
python -m ai_core.agent_gateway_server
```

**זהו! GPT Planner אמיתי עובד!**

---

## 📋 מה צריך?

### **חובה**
- ✅ Python 3.10+ (כבר יש לך)
- ✅ Git (כבר יש לך)
- ✅ הקוד (כבר יש לך)

### **אופציונלי**
- 🔑 OpenAI API Key (רק אם רוצה GPT אמיתי)
  - קבל כאן: https://platform.openai.com/api-keys
  - עלות: ~$0.01-0.05 לכל intent (זול!)

---

## 🔧 Setup מפורט

### **שלב 1: Environment Setup**

הרץ את `setup_env.py`:

```bash
python setup_env.py
```

זה ישאל אותך:
1. **Demo או Real GPT?**
   - Demo = לא צריך API key, משתמש בתשובות מדומות
   - Real = צריך API key, משתמש ב-GPT אמיתי

2. **API Key** (אם בחרת Real)
   - לך ל: https://platform.openai.com/api-keys
   - צור key חדש
   - העתק והדבק

3. **Model** (אם בחרת Real)
   - `gpt-4o-mini` (מומלץ) - מהיר וזול
   - `gpt-4o` - יותר חכם, יותר יקר
   - `gpt-4-turbo` - דור קודם

**תוצאה**: קובץ `.env` נוצר עם ההגדרות שלך

---

### **שלב 2: התקן Dependencies**

```bash
pip install -r requirements.txt
```

מה זה מתקין:
- `openai` - GPT API
- `python-dotenv` - קריאת .env
- `fastapi` - HTTP server
- `uvicorn` - ASGI server

---

### **שלב 3: בדיקה**

**בדיקה מהירה**:
```bash
python -c "from ai_core import agent_gateway; print('✅ OK')"
```

אם רואה `✅ OK` - הכל תקין!

---

### **שלב 4: הפעלה**

**להפעיל את השרת**:
```bash
python -m ai_core.agent_gateway_server
```

**מה תראה**:
```
======================================================================
AI-OS Agent Gateway HTTP API Server
======================================================================

🚀 Starting server...

📍 Endpoints:
   - Root:        http://localhost:8000/
   - API:         http://localhost:8000/api/v1/intent
   - Docs:        http://localhost:8000/docs
   - Health:      http://localhost:8000/health
```

**לבדוק שזה עובד**:
- פתח: http://localhost:8000/docs
- תראה Swagger UI אינטראקטיבי!

---

## 🎮 איך משתמשים?

### **דרך Python**

```python
from ai_core.agent_gateway import plan_and_optionally_execute

# Plan בלבד
result = plan_and_optionally_execute(
    "צור workflow חדש",
    auto_execute=False
)
print(result["plan"]["summary"])

# Plan + Execute
result = plan_and_optionally_execute(
    "עדכן README",
    auto_execute=True
)
print(f"Executed: {result['execution']['summary']['executed']}")
```

### **דרך HTTP**

```bash
curl -X POST http://localhost:8000/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": "צור workflow", "auto_execute": false}'
```

---

## 🐛 Troubleshooting

### **בעיה: ModuleNotFoundError**

```bash
pip install -r requirements.txt
```

### **בעיה: OPENAI_API_KEY not found**

```bash
python setup_env.py
```
ובחר אופציה מתאימה (Demo או Real)

### **בעיה: Port 8000 already in use**

```bash
# מצא מי משתמש בפורט
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# או השתמש בפורט אחר
uvicorn ai_core.agent_gateway_server:app --port 3000
```

### **בעיה: Server won't start**

בדוק:
1. Python גרסה 3.10+: `python --version`
2. Dependencies מותקנים: `pip list | findstr fastapi`
3. `.env` קיים: `dir .env`

---

## 📊 Demo Mode vs Real GPT

| Feature | Demo Mode | Real GPT |
|---------|-----------|----------|
| **API Key** | ❌ לא צריך | ✅ צריך |
| **עלות** | 💰 חינמי | 💰 ~$0.01-0.05 לintent |
| **GPT Planner** | 🎭 מדומה | 🚀 אמיתי |
| **Action Executor** | ✅ עובד | ✅ עובד |
| **Git Operations** | ✅ עובד | ✅ עובד |
| **HTTP API** | ✅ עובד | ✅ עובד |

**המלצה**:
- **Demo Mode** לבדיקות ופיתוח
- **Real GPT** לשימוש יום-יומי

---

## 🔄 עדכונים

### **לעדכן את הקוד**

```bash
git pull
pip install -r requirements.txt
```

### **לשנות mode (Demo ↔ Real)**

```bash
python setup_env.py
```
זה ישאל שוב ויעדכן את `.env`

---

## 🔒 Security

### **המפתח שלך**

- ✅ `.env` ignored ב-git (לא מועלה)
- ✅ רק במחשב שלך
- ⚠️ אל תשתף את `.env` או API key

### **להסיר API key**

```bash
# אופציה 1: החזר ל-Demo Mode
python setup_env.py

# אופציה 2: מחק .env
del .env
```

---

## 📚 קבצים חשובים

| קובץ | מה זה | git? |
|------|-------|------|
| `.env` | הגדרות + API key | ❌ ignored |
| `.env.template` | דוגמה | ✅ committed |
| `requirements.txt` | dependencies | ✅ committed |
| `setup_env.py` | setup אינטראקטיבי | ✅ committed |

---

## 🎯 Next Steps

אחרי ש-AI-OS רץ:

1. **נסה intent פשוט**:
   ```python
   python -c "from ai_core.agent_gateway import quick_plan; print(quick_plan('צור workflow'))"
   ```

2. **הרץ Iron Test**:
   ```bash
   python run_iron_test.py
   ```

3. **פתח Docs**:
   - http://localhost:8000/docs

4. **חבר Custom GPT / Telegram** (אופציונלי)

---

## 💡 Tips

- **Debug Mode**: הוסף `--log-level debug` ל-uvicorn
- **Auto Restart**: הוסף `--reload` ל-uvicorn
- **Different Port**: `--port 3000`

```bash
uvicorn ai_core.agent_gateway_server:app --reload --log-level debug --port 3000
```

---

**זהו! AI-OS מוכן לשימוש! 🚀**

**יש בעיות?** תפתח issue או תשאל את Claude.
