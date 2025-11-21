# Chat1 Integration Guide

**Created**: 2025-11-21  
**Status**: 🎯 Ready for Implementation  
**Goal**: Connect Custom GPT or Telegram Bot to Agent Gateway

---

## 🎯 Overview

Now that AI-OS has a working Agent Gateway HTTP API with health monitoring, the next step is to connect a chat interface (Chat1) that users can interact with naturally.

**What is Chat1?**
- A conversational interface (Custom GPT, Telegram Bot, etc.)
- Accepts natural language from users
- Sends HTTP requests to Agent Gateway
- Returns formatted responses

---

## 🏗️ Architecture

```
User
  ↓ (natural language)
Chat1 (Custom GPT / Telegram)
  ↓ (HTTP POST)
Agent Gateway API (localhost:8000/api/v1/intent)
  ↓
Intent Router → GPT Planner → Action Executor
  ↓
Git Operations / File Operations
  ↓ (response)
Chat1
  ↓ (formatted message)
User
```

---

## ✅ Prerequisites (All Done!)

- ✅ Agent Gateway HTTP API running
- ✅ Health Dashboard operational
- ✅ GPT Planner in Real mode
- ✅ Action Executor tested
- ✅ One-command startup (`python start.py`)

---

## 🔧 Option 1: Custom GPT

### **How It Works**

Custom GPT can make HTTP API calls using Actions (OpenAPI schema).

### **Steps to Implement**

1. **Create Custom GPT**
   - Go to: https://chat.openai.com/gpts/editor
   - Name: "AI-OS Assistant"
   - Description: "Your personal AI operating system assistant"

2. **Add Instructions**
```
You are an AI-OS Assistant. Your role is to help users manage their AI operating system by sending intents to the Agent Gateway.

When a user asks you to do something like "create a file" or "update documentation", you:
1. Parse their intent
2. Send it to the Agent Gateway API
3. Report back the results

Always be clear about what actions you're taking and ask for confirmation when needed.
```

3. **Add Actions (OpenAPI Schema)**

**Problem**: Custom GPT needs to reach localhost:8000, but it can't access local servers directly.

**Solutions**:
- **Option A**: Use ngrok/cloudflare tunnel to expose localhost
- **Option B**: Deploy Agent Gateway to cloud (Heroku, Railway, etc.)
- **Option C**: Run Custom GPT locally using OpenAI API (not web GPT)

### **Option A: ngrok (Quick Testing)**

```bash
# Install ngrok
# Download from: https://ngrok.com/download

# Expose localhost:8000
ngrok http 8000
```

This gives you a public URL like: `https://abc123.ngrok.io`

**OpenAPI Schema for Custom GPT**:
```yaml
openapi: 3.0.0
info:
  title: AI-OS Agent Gateway
  version: 1.0.0
servers:
  - url: https://abc123.ngrok.io  # Replace with your ngrok URL
paths:
  /api/v1/intent:
    post:
      operationId: sendIntent
      summary: Send an intent to AI-OS
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                intent:
                  type: string
                  description: Natural language intent
                auto_execute:
                  type: boolean
                  description: Whether to auto-execute actions
                  default: false
              required:
                - intent
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
```

---

## 🤖 Option 2: Telegram Bot

### **Why Telegram?**
- ✅ Works on mobile
- ✅ Easy webhook setup
- ✅ Can reach local server via tunneling
- ✅ Rich message formatting
- ✅ No subscription required

### **Steps to Implement**

1. **Create Telegram Bot**
```bash
# Talk to @BotFather on Telegram
/newbot
# Follow prompts, get your bot token
```

2. **Install Telegram Bot Library**
```bash
pip install python-telegram-bot
```

3. **Create Bot Script** (`telegram_bot.py`)

```python
"""
AI-OS Telegram Bot

Connects Telegram users to Agent Gateway.
"""

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Get from @BotFather
AGENT_GATEWAY_URL = "http://localhost:8000/api/v1/intent"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    await update.message.reply_text(
        "👋 Hello! I'm your AI-OS Assistant.\n\n"
        "Send me a natural language intent and I'll execute it via Agent Gateway.\n\n"
        "Examples:\n"
        "- Create a README file\n"
        "- Update the documentation\n"
        "- Run a health check"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages"""
    user_intent = update.message.text
    
    # Send to Agent Gateway
    try:
        await update.message.reply_text("⏳ Processing your intent...")
        
        response = requests.post(
            AGENT_GATEWAY_URL,
            json={
                "intent": user_intent,
                "auto_execute": False  # Always plan first
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Format response
            status = result.get('status')
            
            if status == 'success':
                plan = result.get('plan', {})
                summary = plan.get('summary', 'Plan created')
                
                await update.message.reply_text(
                    f"✅ Plan created!\n\n{summary}\n\n"
                    f"Reply with 'execute' to run this plan."
                )
            else:
                error = result.get('error', 'Unknown error')
                await update.message.reply_text(f"❌ Error: {error}")
        else:
            await update.message.reply_text(
                f"❌ API returned status {response.status_code}"
            )
    
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    """Start the bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start polling
    print("🤖 Bot started!")
    application.run_polling()

if __name__ == '__main__':
    main()
```

4. **Run Bot**
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
python telegram_bot.py
```

---

## 🔐 Security Considerations

### **For Public Deployment**

If exposing Agent Gateway to the internet:

1. **Authentication**
   - Add API key to Agent Gateway
   - Validate requests from Chat1
   
2. **Rate Limiting**
   - Limit requests per user
   - Prevent abuse

3. **Input Validation**
   - Sanitize user intents
   - Block dangerous operations

4. **HTTPS Only**
   - Use SSL/TLS
   - No plain HTTP

### **For Local Development**

- ✅ localhost only = safe
- ✅ ngrok tunnel = temporary, password-protected
- ✅ Telegram polling = bot reaches you, not vice versa

---

## 🧪 Testing Chat1 Integration

### **Test 1: Simple Intent**
```
User: "Create a test file"
Expected: Plan returned, file created
```

### **Test 2: Complex Intent**
```
User: "Update README and add health check section"
Expected: Multi-step plan, both actions executed
```

### **Test 3: Error Handling**
```
User: "Delete everything"
Expected: Safety validation, blocked
```

---

## 📊 What's Missing for Chat1?

### **To Implement**

1. **Choose Interface** (Custom GPT vs Telegram)
   - Decide based on use case
   - Custom GPT = convenience
   - Telegram = mobile + webhooks

2. **Expose Agent Gateway** (if remote)
   - ngrok for testing
   - Cloud deployment for production
   - Or keep local-only

3. **Create Bot Script**
   - Use example above as template
   - Customize formatting
   - Add conversation context

4. **Test End-to-End**
   - Send intent via chat
   - Verify plan created
   - Execute actions
   - Check git commits

---

## 🎯 Next Steps

### **Immediate (Option A: Keep Local)**
```bash
# 1. Start Agent Gateway
python start.py

# 2. In another terminal, expose with ngrok
ngrok http 8000

# 3. Create Custom GPT with ngrok URL
# Or run Telegram bot locally
```

### **Production (Option B: Deploy)**
```bash
# 1. Choose platform (Heroku, Railway, etc.)
# 2. Add Procfile for deployment
# 3. Set environment variables
# 4. Deploy Agent Gateway
# 5. Connect Custom GPT or Telegram to public URL
```

---

## 🔗 Useful Links

- Custom GPT Editor: https://chat.openai.com/gpts/editor
- Telegram BotFather: https://t.me/BotFather
- ngrok: https://ngrok.com
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/

---

## 📝 Summary

**Current Status**:
- ✅ Agent Gateway API ready
- ✅ Health monitoring active
- ✅ Real GPT working
- ⏳ **Missing**: Chat interface connection

**To Complete Chat1**:
1. Choose interface (GPT or Telegram)
2. Expose localhost or deploy
3. Implement bot script
4. Test end-to-end
5. 🎉 **Full conversational AI-OS!**

**Estimated Time**: 1-2 hours for basic integration

---

**Status**: 🎯 Ready to implement  
**Blocker**: None - all prerequisites met  
**Next**: Choose interface and expose API
