import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Get keys
n8n_api_key = os.getenv("N8N_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

workflow_id = "3CBsD70avEmYwuA3"

# Full workflow with all nodes
workflow = {
    "name": "Email Watcher - Gmail to Drift Report",
    "nodes": [
        {
            "parameters": {
                "rule": {
                    "interval": [{"field": "minutes", "minutesInterval": 15}]
                }
            },
            "id": "schedule-trigger",
            "name": "Every 15 Minutes",
            "type": "n8n-nodes-base.scheduleTrigger",
            "typeVersion": 1.1,
            "position": [250, 300]
        },
        {
            "parameters": {
                "url": "https://gmail.googleapis.com/gmail/v1/users/me/messages",
                "authentication": "predefinedCredentialType",
                "nodeCredentialType": "googleApi",
                "qs": {
                    "parameters": [
                        {"name": "q", "value": "is:unread"},
                        {"name": "maxResults", "value": "50"}
                    ]
                }
            },
            "id": "gmail-search",
            "name": "Search Unread Emails",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [450, 300]
        },
        {
            "parameters": {
                "url": "https://api.anthropic.com/v1/messages",
                "method": "POST",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {"name": "x-api-key", "value": f"{anthropic_key}"},
                        {"name": "anthropic-version", "value": "2023-06-01"},
                        {"name": "content-type", "value": "application/json"}
                    ]
                },
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": json.dumps({
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 1024,
                    "messages": [{
                        "role": "user",
                        "content": "={{ \"Classify emails: \" + JSON.stringify($json) }}"
                    }]
                })
            },
            "id": "claude-classify",
            "name": "Claude Classification",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [650, 300]
        },
        {
            "parameters": {
                "operation": "write",
                "fileName": "=memory-bank/drift/email-drift-{{ $now.format('YYYY-MM-DD-HHmmss') }}.yaml",
                "fileContent": "={{ JSON.stringify($json, null, 2) }}"
            },
            "id": "write-file",
            "name": "Save Drift Report",
            "type": "n8n-nodes-base.writeFile",
            "typeVersion": 1,
            "position": [850, 300]
        }
    ],
    "connections": {
        "Every 15 Minutes": {
            "main": [[{"node": "Search Unread Emails", "type": "main", "index": 0}]]
        },
        "Search Unread Emails": {
            "main": [[{"node": "Claude Classification", "type": "main", "index": 0}]]
        },
        "Claude Classification": {
            "main": [[{"node": "Save Drift Report", "type": "main", "index": 0}]]
        }
    },
    "settings": {}
}

print("[INFO] Updating workflow with all nodes...")

# Update workflow
response = requests.put(
    f"http://localhost:5678/api/v1/workflows/{workflow_id}",
    json=workflow,
    headers={
        "Content-Type": "application/json",
        "X-N8N-API-KEY": n8n_api_key
    }
)

print(f"[STATUS] {response.status_code}")

if response.status_code == 200:
    print(f"[OK] Workflow updated with all nodes!")
    print(f"[URL] http://localhost:5678/workflow/{workflow_id}")
    print("")
    print("[NEXT STEPS]")
    print("1. Open workflow in browser")
    print("2. Configure Gmail OAuth2 credential")
    print("3. Activate workflow")
else:
    print(f"[ERROR] {response.text}")
