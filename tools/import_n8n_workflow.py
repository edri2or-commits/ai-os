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

# Load workflow
workflow_path = Path(r"C:\Users\edri2\Desktop\AI\ai-os\n8n-workflows\email-watcher.json")
with open(workflow_path, 'r', encoding='utf-8') as f:
    workflow = json.load(f)

print("[INFO] Importing workflow to n8n...")

# n8n API endpoint
n8n_url = "http://localhost:5678/api/v1/workflows"

# Import workflow
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
    print(f"[OK] Workflow imported successfully!")
    print(f"[ID] Workflow ID: {workflow_id}")
    print(f"[URL] http://localhost:5678/workflow/{workflow_id}")
else:
    print(f"[ERROR] {response.text}")
