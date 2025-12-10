# Telegram Bot Workflow - Final Configuration

**Created:** 2025-12-10 09:15  
**Status:** ✅ OPERATIONAL  
**Workflow ID:** Q3YsexsUupZFBuL8  
**Credential:** SALAMTUKBOT_FIXED (dix5dw0FF8qukJ00)

## Configuration

```json
{
  "name": "Telegram Bot - FINAL FIX",
  "nodes": [
    {
      "parameters": {
        "updates": ["message"]
      },
      "name": "TelegramTrigger",
      "type": "n8n-nodes-base.telegramTrigger",
      "typeVersion": 1.1,
      "position": [100, 300],
      "credentials": {
        "telegramApi": {
          "id": "dix5dw0FF8qukJ00"
        }
      }
    },
    {
      "parameters": {
        "text": "אני חי, קיים, וללא רווחים! 🚀",
        "chatId": "={{$json.message.chat.id}}"
      },
      "name": "SendMessage",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.2,
      "position": [350, 300],
      "credentials": {
        "telegramApi": {
          "id": "dix5dw0FF8qukJ00"
        }
      }
    }
  ],
  "connections": {
    "TelegramTrigger": {
      "main": [
        [
          {
            "node": "SendMessage",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {}
}
```

## Webhook Details

**URL:** `https://n8n.35.223.68.23.nip.io/webhook/Q3YsexsUupZFBuL8/telegramtrigger/webhook`

**Telegram Status:**
```json
{
  "url": "https://n8n.35.223.68.23.nip.io/webhook/Q3YsexsUupZFBuL8/telegramtrigger/webhook",
  "has_custom_certificate": false,
  "pending_update_count": 0,
  "last_error_message": null,
  "max_connections": 40,
  "ip_address": "35.223.68.23",
  "allowed_updates": ["message"]
}
```

## Environment Variables (VPS)

**File:** `/root/.env`

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=8119131809:AAHBSSxxQ3ldLzow6afTv1SLneSKfdmeaNY
TELEGRAM_CHAT_ID=5786217215

# n8n Configuration
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
N8N_EDITOR_BASE_URL=https://n8n.35.223.68.23.nip.io
WEBHOOK_URL=https://n8n.35.223.68.23.nip.io
```

## Critical Lessons

1. **WEBHOOK_URL:** MUST NOT have trailing slash
   - ❌ `https://n8n.35.223.68.23.nip.io/`
   - ✅ `https://n8n.35.223.68.23.nip.io`

2. **Node Names:** MUST NOT contain spaces
   - ❌ `Telegram Trigger` → URL: `.../telegram%20trigger/...`
   - ✅ `TelegramTrigger` → URL: `.../telegramtrigger/...`

3. **Activation:** Use API endpoint
   - ❌ `PUT /workflows/{id}` with `active: true`
   - ✅ `POST /workflows/{id}/activate`

4. **Verification:** Always check Telegram API
   ```bash
   curl https://api.telegram.org/bot{TOKEN}/getWebhookInfo
   ```

## Restoration Steps

If workflow is lost, recreate using:

1. Create credential via API:
```python
import requests
N8N_URL = "https://n8n.35.223.68.23.nip.io/api/v1"
API_KEY = "..." # Get from n8n UI

cred_payload = {
    "name": "SALAMTUKBOT_FIXED",
    "type": "telegramApi",
    "data": {"accessToken": "8119131809:AAHBSSxxQ3ldLzow6afTv1SLneSKfdmeaNY"}
}
requests.post(f"{N8N_URL}/credentials", headers={"X-N8N-API-KEY": API_KEY}, json=cred_payload)
```

2. Create workflow (use JSON above)
3. Activate: `POST /workflows/{id}/activate`
4. Verify: Check Telegram webhook info

---

**Last Updated:** 2025-12-10 09:15  
**Next:** HITL approval workflows extension
