# Agent Gateway HTTP API – שרת HTTP ל-AI-OS

**Created**: 2025-11-21  
**Purpose**: תיעוד ה-HTTP API של Agent Gateway  
**Status**: ✅ Implemented  
**Server**: FastAPI + Uvicorn

---

## 🎯 מטרת המסמך

מסמך זה מתעד את ה-**HTTP API** של Agent Gateway - השרת שמאפשר לכל סוכן חיצוני (Custom GPT, Telegram Bot, Web UI) לדבר עם AI-OS דרך HTTP.

**קשר ל-AGENT_GATEWAY_API.md**:
- `AGENT_GATEWAY_API.md` = תיעוד ה-API הפנימי (Python functions)
- `AGENT_GATEWAY_HTTP_API.md` = תיעוד ה-API החיצוני (HTTP endpoints) ← **זה המסמך**

---

## 🚀 הרצת השרת

### **אופן 1: הרצה פשוטה**

```bash
cd C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace
python -m ai_core.agent_gateway_server
```

### **אופן 2: עם Uvicorn ישירות**

```bash
uvicorn ai_core.agent_gateway_server:app --reload
```

### **פרמטרים נוספים**

```bash
# Custom port
python -m ai_core.agent_gateway_server --port 3000

# Or with uvicorn
uvicorn ai_core.agent_gateway_server:app --port 3000 --reload
```

### **מה תראה בטרמינל**

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

📖 API Documentation: http://localhost:8000/docs

⏸️  Press CTRL+C to stop
======================================================================

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 📐 API Endpoints

### **1. Root - Health Check**

```
GET /
```

**Response**:
```json
{
  "service": "AI-OS Agent Gateway API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "intent": "/api/v1/intent",
    "docs": "/docs",
    "health": "/health"
  }
}
```

---

### **2. Health Check**

```
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "service": "agent-gateway-api",
  "version": "1.0.0"
}
```

---

### **3. Process Intent** ⭐ **MAIN ENDPOINT**

```
POST /api/v1/intent
```

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "intent": "צור workflow חדש לניהול טוקנים",
  "auto_execute": false,
  "dry_run": false
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `intent` | string | ✅ Yes | - | User intent (Hebrew/English) |
| `auto_execute` | bool | ❌ No | `false` | Execute actions automatically? |
| `dry_run` | bool | ❌ No | `false` | Simulate execution (future) |

**Response** (Success - Plan Only):
```json
{
  "status": "plan_ready",
  "intent": "צור workflow חדש לניהול טוקנים",
  "plan": {
    "summary": "אור רוצה workflow חדש...",
    "context": "כרגע יש 3 workflows...",
    "steps": [
      "צור קובץ workflows/TOKEN_MANAGEMENT.md",
      "עדכן SYSTEM_SNAPSHOT",
      "commit + push"
    ],
    "actions_for_claude": [
      {
        "type": "file.create",
        "params": {
          "path": "workflows/TOKEN_MANAGEMENT.md",
          "content": "..."
        },
        "approval": "auto",
        "description": "יצירת workflow"
      }
    ],
    "decisions_for_or": [
      "האם השם TOKEN_MANAGEMENT מתאים"
    ],
    "version": "2.0"
  },
  "validation": {
    "valid": true,
    "total": 3,
    "valid_count": 3,
    "invalid_count": 0,
    "errors": []
  },
  "execution": null,
  "message": "Plan ready with 3 actions. Set auto_execute=True to execute."
}
```

**Response** (Success - Executed):
```json
{
  "status": "success",
  "intent": "עדכן README",
  "plan": {...},
  "validation": {...},
  "execution": {
    "executed": true,
    "executed_actions": [
      {
        "action_index": 1,
        "action": {...},
        "result": {
          "success": true,
          "message": "Updated: README.md"
        }
      }
    ],
    "pending_approval": [],
    "errors": [],
    "summary": {
      "total": 3,
      "executed": 3,
      "pending": 0,
      "failed": 0
    }
  },
  "message": "Successfully executed 3 actions"
}
```

**Response** (Validation Failed):
```json
{
  "status": "validation_failed",
  "intent": "...",
  "plan": {...},
  "validation": {
    "valid": false,
    "total": 3,
    "valid_count": 2,
    "invalid_count": 1,
    "errors": [
      "Action #2: Missing required param 'content'"
    ]
  },
  "execution": null,
  "message": "Validation failed: 1 invalid actions"
}
```

**HTTP Status Codes**:
- `200 OK` - Success (even if validation failed - check `status` field)
- `400 Bad Request` - Invalid request format
- `500 Internal Server Error` - Unexpected error

---

## 💻 Usage Examples

### **cURL**

**Example 1: Plan only**
```bash
curl -X POST http://localhost:8000/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "צור workflow חדש",
    "auto_execute": false
  }'
```

**Example 2: Plan + Execute**
```bash
curl -X POST http://localhost:8000/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "עדכן README עם הסבר על Agent Gateway",
    "auto_execute": true
  }'
```

---

### **Python (requests)**

```python
import requests

# Server URL
API_URL = "http://localhost:8000/api/v1/intent"

# Example 1: Plan only
response = requests.post(
    API_URL,
    json={
        "intent": "צור workflow חדש לניהול טוקנים",
        "auto_execute": False
    }
)

result = response.json()
print(f"Status: {result['status']}")
print(f"Plan: {result['plan']['summary']}")
print(f"Actions: {result['validation']['total']}")

# Example 2: Plan + Execute
response = requests.post(
    API_URL,
    json={
        "intent": "עדכן README",
        "auto_execute": True
    }
)

result = response.json()
print(f"Executed: {result['execution']['summary']['executed']}")
```

---

### **JavaScript (fetch)**

```javascript
// Example: Plan only
fetch('http://localhost:8000/api/v1/intent', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    intent: 'צור workflow חדש',
    auto_execute: false
  })
})
  .then(response => response.json())
  .then(data => {
    console.log('Status:', data.status);
    console.log('Plan:', data.plan.summary);
    console.log('Actions:', data.validation.total);
  });
```

---

## 📖 Interactive API Documentation

FastAPI provides **automatic interactive documentation**:

### **Swagger UI**
```
http://localhost:8000/docs
```
- Interactive API testing
- Try out endpoints
- See request/response schemas

### **ReDoc**
```
http://localhost:8000/redoc
```
- Alternative documentation style
- Better for reading

---

## 🔌 Integration Examples

### **Custom GPT (ChatGPT Actions)**

**OpenAPI Schema** (for ChatGPT):

```yaml
openapi: 3.0.0
info:
  title: AI-OS Agent Gateway
  version: 1.0.0
servers:
  - url: http://your-server.com
paths:
  /api/v1/intent:
    post:
      operationId: processIntent
      summary: Process user intent
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                intent:
                  type: string
                  description: User intent in natural language
                auto_execute:
                  type: boolean
                  default: false
                  description: Execute automatically?
              required:
                - intent
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
```

**In ChatGPT**:
1. Go to "Actions" tab
2. Add new action
3. Paste OpenAPI schema above
4. Set server URL to your deployed server
5. Test!

---

### **Telegram Bot**

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests

API_URL = "http://localhost:8000/api/v1/intent"

async def handle_intent(update: Update, context):
    intent = update.message.text
    
    # Send to API
    response = requests.post(
        API_URL,
        json={"intent": intent, "auto_execute": False}
    )
    
    result = response.json()
    
    if result["status"] == "validation_failed":
        await update.message.reply_text(f"❌ {result['message']}")
        return
    
    # Show plan
    plan_text = result["plan"]["summary"]
    actions_count = result["validation"]["total"]
    
    await update.message.reply_text(
        f"📋 Plan:\n{plan_text}\n\n"
        f"Actions: {actions_count}\n\n"
        f"Execute? Reply /yes or /no"
    )
    
    # Store for approval
    context.user_data["pending_intent"] = intent

async def approve(update: Update, context):
    intent = context.user_data.get("pending_intent")
    if not intent:
        await update.message.reply_text("No pending plan")
        return
    
    # Execute!
    response = requests.post(
        API_URL,
        json={"intent": intent, "auto_execute": True}
    )
    
    result = response.json()
    await update.message.reply_text(f"✅ {result['message']}")

# Setup
app = Application.builder().token("YOUR_BOT_TOKEN").build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_intent))
app.add_handler(CommandHandler("yes", approve))
app.run_polling()
```

---

## 🔒 Security Considerations

### **Current Implementation**
⚠️ **No authentication** - for local/development use only!

### **Production Requirements**

**Must implement**:
1. **API Key Authentication**
   ```python
   from fastapi import Header, HTTPException
   
   async def verify_api_key(x_api_key: str = Header(...)):
       if x_api_key != "your-secret-key":
           raise HTTPException(status_code=401, detail="Invalid API key")
   ```

2. **Rate Limiting**
   ```python
   from slowapi import Limiter
   
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post("/api/v1/intent")
   @limiter.limit("10/minute")
   async def process_intent(...):
       ...
   ```

3. **HTTPS Only**
   - Never expose over HTTP in production
   - Use reverse proxy (nginx/caddy) with SSL

4. **Input Validation**
   - Already handled by Pydantic
   - Max intent length (implement if needed)

5. **CORS Configuration**
   ```python
   # Tighten CORS in production
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-frontend.com"],  # Specific origins
       allow_credentials=True,
       allow_methods=["POST"],
       allow_headers=["Content-Type", "X-API-Key"],
   )
   ```

---

## 🚀 Deployment

### **Option 1: Local (Current)**
```bash
python -m ai_core.agent_gateway_server
```
- No internet required
- Development/testing only

### **Option 2: ngrok (Quick public URL)**
```bash
# Terminal 1: Start server
python -m ai_core.agent_gateway_server

# Terminal 2: Expose with ngrok
ngrok http 8000
```
- Instant public URL
- Good for testing with ChatGPT
- Free tier available

### **Option 3: Cloud Platforms**

**Railway / Render / Fly.io**:
1. Create `requirements.txt`:
   ```
   fastapi
   uvicorn
   openai
   ```
2. Create `Procfile` or configure start command:
   ```
   web: uvicorn ai_core.agent_gateway_server:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy!

**Heroku**:
```bash
git push heroku main
```

**Docker**:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "ai_core.agent_gateway_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📊 Performance

### **Response Times**
| Operation | Time | Notes |
|-----------|------|-------|
| Health check | <10ms | No processing |
| Plan only | ~2-5s | GPT API call |
| Plan + validate | ~2-5s | Same |
| Plan + execute | ~4-8s | + file/git ops |

### **Scalability**
- **Single instance**: ~10 req/s
- **With load balancer**: Horizontal scaling
- **Bottleneck**: GPT API rate limits

---

## 🐛 Troubleshooting

### **Server won't start**

**Error**: `Address already in use`
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill it (Windows)
taskkill /PID <PID> /F

# Or use different port
python -m ai_core.agent_gateway_server --port 3000
```

### **OPENAI_API_KEY not found**

Set environment variable:
```bash
# Windows (cmd)
set OPENAI_API_KEY=your-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-key-here"

# Linux/Mac
export OPENAI_API_KEY=your-key-here
```

### **Module not found errors**

```bash
pip install fastapi uvicorn openai
```

---

## 📝 Change Log

### **v1.0.0** (2025-11-21)
- ✅ Initial release
- ✅ POST /api/v1/intent endpoint
- ✅ FastAPI server
- ✅ Auto-generated docs (/docs, /redoc)
- ✅ Health check endpoint
- ⚠️ No authentication (local only)

---

**Document Status**: ✅ Active  
**Server Status**: ✅ Implemented  
**Version**: 1.0.0  
**Last Updated**: 2025-11-21
