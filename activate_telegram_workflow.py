import requests
import json

# Configuration
N8N_URL = "https://n8n.35.223.68.23.nip.io/api/v1"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZDkzZjUzZC0wYmU1LTRjNzUtYmZiOS1mNDUwOTNmM2NhYzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY1MzI5MDEzLCJleHAiOjE3Njc5MDk2MDB9.aGbxJ-uAnyRzUvwkCwDjfvjzXeUSyjuWJt5MvAH0Tr4"
TELEGRAM_TOKEN = "8119131809:AAHBSSxxQ3ldLzow6afTv1SLneSKfdmeaNY"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

# Step 1: Create/Get Credential
print("Step 1: Creating credential...")
cred_payload = {
    "name": "SALAMTUKBOT_FIXED",
    "type": "telegramApi",
    "data": {"accessToken": TELEGRAM_TOKEN}
}

cred_res = requests.post(f"{N8N_URL}/credentials", headers=headers, json=cred_payload)
if cred_res.status_code in [200, 201]:
    cred_id = cred_res.json()['id']
    print(f"Credential ID: {cred_id}")
else:
    print(f"Credential creation failed (may already exist): {cred_res.status_code}")
    # Try to find existing - we'll use a known ID from previous attempts
    # Or we can manually provide it
    print("Trying with credential name reference...")
    cred_id = None

# Step 2: Create workflow
print("Step 2: Creating workflow...")
workflow = {
    "name": "Telegram Bot - WORKING",
    "nodes": [
        {
            "parameters": {
                "updates": ["message"]
            },
            "id": "telegram_trigger_node",
            "name": "Telegram Trigger",
            "type": "n8n-nodes-base.telegramTrigger",
            "typeVersion": 1.1,
            "position": [100, 300],
            "credentials": {
                "telegramApi": {
                    "id": cred_id if cred_id else "SALAMTUKBOT_FIXED",
                    "name": "SALAMTUKBOT_FIXED"
                }
            }
        },
        {
            "parameters": {
                "text": "אני חי וקיים על השרת בענן! 🚀",
                "chatId": "={{$json.message.chat.id}}"
            },
            "id": "send_message_node",
            "name": "Send Message",
            "type": "n8n-nodes-base.telegram",
            "typeVersion": 1.2,
            "position": [350, 300],
            "credentials": {
                "telegramApi": {
                    "id": cred_id if cred_id else "SALAMTUKBOT_FIXED",
                    "name": "SALAMTUKBOT_FIXED"
                }
            }
        }
    ],
    "connections": {
        "Telegram Trigger": {
            "main": [[{"node": "Send Message", "type": "main", "index": 0}]]
        }
    },
    "settings": {}
}

create_res = requests.post(f"{N8N_URL}/workflows", headers=headers, json=workflow)

if create_res.status_code not in [200, 201]:
    print(f"FAILURE creating: {create_res.status_code}")
    print(create_res.text)
    exit(1)

workflow_id = create_res.json()['id']
print(f"Created workflow: {workflow_id}")

# Step 3: Activate
print("Step 3: Activating workflow...")
activate_res = requests.post(f"{N8N_URL}/workflows/{workflow_id}/activate", headers=headers)

if activate_res.status_code == 200:
    print("SUCCESS: Workflow is now ACTIVE! 🟢")
    print(f"ID: {workflow_id}")
else:
    print(f"FAILURE activating: {activate_res.status_code}")
    print(activate_res.text)
