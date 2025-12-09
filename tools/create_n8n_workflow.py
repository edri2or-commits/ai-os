import requests
import json
from pathlib import Path
import os
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Get n8n API key
n8n_api_key = os.getenv("N8N_API_KEY")

# Simplified workflow structure
workflow = {
    "name": "Email Watcher - Gmail to Drift Report",
    "nodes": [
        {
            "parameters": {
                "rule": {
                    "interval": [{"field": "minutes", "minutesInterval": 15}]
                }
            },
            "name": "Schedule Every 15min",
            "type": "n8n-nodes-base.scheduleTrigger",
            "typeVersion": 1.1,
            "position": [250, 300]
        }
    ],
    "connections": {},
    "settings": {}
}

print("[INFO] Creating workflow in n8n...")

# n8n API endpoint
n8n_url = "http://localhost:5678/api/v1/workflows"

# Create workflow
response = requests.post(
    n8n_url,
    json=workflow,
    headers={
        "Content-Type": "application/json",
        "X-N8N-API-KEY": n8n_api_key
    }
)

print(f"[STATUS] {response.status_code}")

if response.status_code in [200, 201]:
    data = response.json()
    workflow_id = data.get("id")
    print(f"[OK] Workflow created successfully!")
    print(f"[ID] Workflow ID: {workflow_id}")
    print(f"[URL] http://localhost:5678/workflow/{workflow_id}")
    print("")
    print("[NEXT] Open the workflow in n8n and add the following nodes:")
    print("1. Gmail - Search unread emails")
    print("2. HTTP Request - Claude API classification")
    print("3. Write to file - Save drift report")
else:
    print(f"[ERROR] {response.text}")
