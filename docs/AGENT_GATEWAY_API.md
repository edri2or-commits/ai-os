# Agent Gateway API – ממשק אחוד לכל הסוכנים

**Created**: 2025-11-21  
**Purpose**: תיעוד ה-API של Agent Gateway - נקודת הכניסה היחידה ל-AI-OS  
**Status**: ✅ Active (Internal API - no HTTP yet)

---

## 🎯 מטרת המסמך

Agent Gateway הוא **השכבה האחת והיחידה** שסוכנים חיצוניים צריכים לדעת.

**כל** השילובים החיצוניים (Custom GPT, Telegram, Web UI, CLI) קוראים לאותו Gateway:
- קלט: Intent (טקסט טבעי)
- פלט: Plan + Validation + (אופציונלי) Execution
- הכל דרך פונקציה אחת: `plan_and_optionally_execute()`

---

## 📐 Internal API (Python Function)

### **פונקציה ראשית**

```python
from ai_core.agent_gateway import plan_and_optionally_execute

result = plan_and_optionally_execute(
    intent="צור workflow חדש",
    auto_execute=False,  # True = execute automatically
    dry_run=False        # Future: simulate without real changes
)
```

### **פרמטרים**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `intent` | string | ✅ Yes | - | User intent in natural language |
| `auto_execute` | bool | ❌ No | `False` | Execute actions automatically? |
| `dry_run` | bool | ❌ No | `False` | Simulate execution (not implemented yet) |

---

## 📤 Response Format

### **Success Response (Plan Only)**

```json
{
  "status": "plan_ready",
  "intent": "צור workflow חדש",
  "plan": {
    "summary": "אור רוצה workflow חדש...",
    "context": "כרגע יש 3 workflows...",
    "steps": [
      "צור קובץ workflows/WF-004.md",
      "עדכן SYSTEM_SNAPSHOT",
      "commit + push"
    ],
    "actions_for_claude": [
      {
        "type": "file.create",
        "params": {"path": "...", "content": "..."},
        "approval": "auto",
        "description": "..."
      }
    ],
    "decisions_for_or": [
      "האם השם מתאים"
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

### **Success Response (Plan + Execute)**

```json
{
  "status": "success",
  "intent": "עדכן README",
  "plan": {
    "summary": "...",
    "context": "...",
    "steps": [...],
    "actions_for_claude": [...],
    "decisions_for_or": [...],
    "version": "2.0"
  },
  "validation": {
    "valid": true,
    "total": 3,
    "valid_count": 3,
    "invalid_count": 0,
    "errors": []
  },
  "execution": {
    "executed": true,
    "executed_actions": [
      {
        "action_index": 1,
        "action": {...},
        "result": {
          "success": true,
          "message": "Created: test.md",
          "details": {...}
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

### **Error Response (Validation Failed)**

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

### **Error Response (Execution Failed)**

```json
{
  "status": "execution_failed",
  "intent": "...",
  "plan": {...},
  "validation": {...},
  "execution": null,
  "message": "Execution failed: File not found",
  "error": "FileNotFoundError: README.md"
}
```

---

## 🔄 Status Values

| Status | Meaning | When |
|--------|---------|------|
| `plan_ready` | Plan generated, not executed | `auto_execute=False` |
| `success` | Plan + execution successful | `auto_execute=True` + all actions succeeded |
| `execution_partial` | Some actions failed | `auto_execute=True` + some failed |
| `validation_failed` | Actions invalid | Validation errors |
| `planning_failed` | GPT Planner failed | API error, malformed intent |
| `execution_failed` | Executor crashed | Unexpected error |

---

## 🔧 Convenience Functions

### **1. Quick Plan**
```python
from ai_core.agent_gateway import quick_plan

summary = quick_plan("צור workflow")
print(summary)
# "אור רוצה workflow חדש..."
```

### **2. Plan and Execute**
```python
from ai_core.agent_gateway import plan_and_execute

result = plan_and_execute("עדכן README")
print(result["execution"]["summary"])
# {"total": 3, "executed": 3, "pending": 0, "failed": 0}
```

### **3. Validate Only**
```python
from ai_core.agent_gateway import validate_only

result = validate_only("צור workflow")
print(result["valid"])
# True
```

---

## 🌐 Future: HTTP API (Not Implemented Yet)

When we add an HTTP server, the API will look like this:

### **Endpoint**

```
POST /api/v1/intent
```

### **Request Body**

```json
{
  "intent": "צור workflow חדש",
  "auto_execute": false,
  "dry_run": false
}
```

### **Response**

Same as the Python function response (JSON).

### **Authentication**

TBD - probably API key in header:
```
Authorization: Bearer YOUR_API_KEY
```

---

## 📊 Integration Examples

### **Example 1: Custom GPT (ChatGPT Actions)**

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "AI-OS Agent Gateway",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://your-server.com"
    }
  ],
  "paths": {
    "/api/v1/intent": {
      "post": {
        "operationId": "processIntent",
        "summary": "Process user intent",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "intent": {"type": "string"},
                  "auto_execute": {"type": "boolean"}
                },
                "required": ["intent"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Success",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### **Example 2: Telegram Bot**

```python
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from ai_core.agent_gateway import plan_and_optionally_execute

async def handle_intent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intent = update.message.text
    
    # Step 1: Plan
    result = plan_and_optionally_execute(intent, auto_execute=False)
    
    if result["status"] == "validation_failed":
        await update.message.reply_text(f"❌ Invalid: {result['message']}")
        return
    
    # Step 2: Ask approval
    plan_text = result["plan"]["summary"]
    await update.message.reply_text(f"📋 Plan:\n{plan_text}\n\nApprove? /yes or /no")
    
    # Store plan for approval
    context.user_data["pending_plan"] = result

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pending = context.user_data.get("pending_plan")
    if not pending:
        await update.message.reply_text("No pending plan")
        return
    
    # Execute!
    result = plan_and_optionally_execute(
        pending["intent"],
        auto_execute=True
    )
    
    await update.message.reply_text(f"✅ {result['message']}")
```

### **Example 3: CLI Tool**

```python
import click
from ai_core.agent_gateway import plan_and_optionally_execute

@click.command()
@click.argument('intent')
@click.option('--execute', is_flag=True, help='Execute automatically')
def ai_os(intent, execute):
    """AI-OS CLI: Process intents"""
    
    result = plan_and_optionally_execute(intent, auto_execute=execute)
    
    click.echo(f"Status: {result['status']}")
    click.echo(f"Message: {result['message']}")
    
    if result['execution']:
        summary = result['execution']['summary']
        click.echo(f"Executed: {summary['executed']}/{summary['total']}")

if __name__ == '__main__':
    ai_os()
```

Usage:
```bash
# Plan only
$ python cli.py "צור workflow"

# Plan + execute
$ python cli.py "צור workflow" --execute
```

---

## 🔒 Security Considerations

### **Current (Internal API)**
- No authentication - runs locally
- Full file system access
- Direct git operations

### **Future (HTTP API)**
- **Must have**: API key authentication
- **Should have**: Rate limiting
- **Should have**: IP whitelisting
- **Must have**: Input validation (SQL injection, etc)
- **Should have**: Audit logging

---

## 🚀 Deployment Scenarios

### **Scenario 1: Local only (Current)**
```
User → Python script → agent_gateway.py
```
- No network
- No authentication
- Direct function calls

### **Scenario 2: HTTP Server (Future)**
```
User → Custom GPT → HTTPS → Flask/FastAPI → agent_gateway.py
```
- Public endpoint
- Authentication required
- Rate limiting

### **Scenario 3: Hybrid (Future)**
```
User → Telegram Bot → Webhook → Lambda → agent_gateway.py
```
- Serverless
- Scales automatically
- Pay per use

---

## 📊 Response Times (Estimated)

| Operation | Time | Depends On |
|-----------|------|------------|
| Plan only | ~2-5s | GPT-4 API latency |
| Validate | <100ms | Local computation |
| Execute (1 action) | <500ms | File/git operations |
| Execute (5 actions) | ~2s | Multiple operations |
| Full flow (plan+execute) | ~4-7s | All of the above |

---

## 🔄 Versioning

### **Current Version**: `1.0`

**Breaking changes** will increment major version:
- v1.x → v2.x: Response format changes
- v1.x → v1.y: Backward-compatible additions

### **Response Version Field**
```json
{
  "version": "2.0",  // Action schema version
  "gateway_version": "1.0"  // Gateway API version (future)
}
```

---

## 📝 Usage Examples

### **Python Example (Full Flow)**

```python
from ai_core.agent_gateway import plan_and_optionally_execute

# User intent
intent = "צור workflow חדש לגיבוי"

# Step 1: Plan
plan_result = plan_and_optionally_execute(intent, auto_execute=False)

print(f"Plan: {plan_result['plan']['summary']}")
print(f"Actions: {plan_result['validation']['total']}")
print(f"Valid: {plan_result['validation']['valid']}")

# Step 2: Ask user approval
if input("Execute? (y/n): ").lower() == 'y':
    # Execute
    exec_result = plan_and_optionally_execute(intent, auto_execute=True)
    
    print(f"Status: {exec_result['status']}")
    print(f"Executed: {exec_result['execution']['summary']['executed']}")
```

---

## 🎯 Next Steps

1. **Add HTTP server** (Flask/FastAPI)
   - Endpoint: `POST /api/v1/intent`
   - Authentication: API key
   - CORS for web UIs

2. **Add Telegram bot**
   - Command: `/intent [text]`
   - Interactive approval
   - Status updates

3. **Add Custom GPT action**
   - OpenAPI schema
   - Action: `processIntent`
   - Response formatting for chat

4. **Add Web UI**
   - React frontend
   - Real-time updates (WebSocket?)
   - Visual plan approval

---

**Document Status**: ✅ Active  
**Version**: 1.0  
**Last Updated**: 2025-11-21  
**Next Review**: After HTTP server implementation
