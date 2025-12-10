import requests
import json

N8N_URL = "https://n8n.35.223.68.23.nip.io/api/v1"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZDkzZjUzZC0wYmU1LTRjNzUtYmZiOS1mNDUwOTNmM2NhYzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY1MzI5MDEzLCJleHAiOjE3Njc5MDk2MDB9.aGbxJ-uAnyRzUvwkCwDjfvjzXeUSyjuWJt5MvAH0Tr4"
BROKEN_WF_ID = "KklrOimDEK3vdnHm"
CRED_ID = "dix5dw0FF8qukJ00"

headers = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}

# 1. Delete Broken Workflow
print(f"1. Deleting broken workflow {BROKEN_WF_ID}...")
requests.delete(f"{N8N_URL}/workflows/{BROKEN_WF_ID}", headers=headers)

# 2. Create FIXED Workflow (WITHOUT active flag)
workflow_json = {
  "name": "Telegram Bot - FINAL FIX",
  "nodes": [
    {
      "parameters": {"updates": ["message"]},
      "name": "TelegramTrigger",
      "type": "n8n-nodes-base.telegramTrigger",
      "typeVersion": 1.1,
      "position": [100, 300],
      "credentials": {"telegramApi": {"id": CRED_ID}}
    },
    {
      "parameters": {"text": "אני חי, קיים, וללא רווחים! 🚀", "chatId": "={{$json.message.chat.id}}"},
      "name": "SendMessage",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.2,
      "position": [350, 300],
      "credentials": {"telegramApi": {"id": CRED_ID}}
    }
  ],
  "connections": {
    "TelegramTrigger": {"main": [[{"node": "SendMessage", "type": "main", "index": 0}]]}
  },
  "settings": {}
}

print("2. Creating Fixed Workflow...")
create_res = requests.post(f"{N8N_URL}/workflows", headers=headers, json=workflow_json)

if create_res.status_code not in [200, 201]:
    print(f"FAILURE: {create_res.status_code}")
    print(create_res.text)
    exit(1)

new_wf_id = create_res.json()['id']
print(f"   Created: {new_wf_id}")

# 3. Activate the workflow
print("3. Activating workflow...")
activate_res = requests.post(f"{N8N_URL}/workflows/{new_wf_id}/activate", headers=headers)

if activate_res.status_code == 200:
    print("SUCCESS: Workflow is now ACTIVE!")
    print(f"ID: {new_wf_id}")
else:
    print(f"FAILURE: {activate_res.status_code}")
    print(activate_res.text)
