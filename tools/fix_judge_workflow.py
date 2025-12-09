"""
Fix Judge V2 workflow - remove wrong credentials from OpenAI node
"""
import requests
import json
from pathlib import Path

# Read API key
env_path = Path(__file__).parent.parent / "infra" / "n8n" / ".env"
api_key = None
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('N8N_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
                break

wf_id = "SF9E5Dr8AeAqzoq2"

headers = {
    "X-N8N-API-KEY": api_key,
    "Content-Type": "application/json"
}

print(f"[+] Fixing workflow: {wf_id}")

# Step 1: Get current workflow
print("[1] Fetching workflow...")
r = requests.get(
    f"http://localhost:5678/api/v1/workflows/{wf_id}",
    headers=headers
)
if r.status_code != 200:
    print(f"[-] Failed: {r.status_code}")
    exit(1)

workflow = r.json()

# Step 2: Fix "Call GPT-4o Judge" node
print("[2] Fixing 'Call GPT-4o Judge' node...")
for node in workflow.get('nodes', []):
    if node.get('name') == 'Call GPT-4o Judge':
        # Remove authentication (will use manual headers instead)
        if 'authentication' in node['parameters']:
            del node['parameters']['authentication']
        if 'genericAuthType' in node['parameters']:
            del node['parameters']['genericAuthType']
        
        # Remove wrong credentials
        if 'credentials' in node:
            del node['credentials']
        
        print(f"   [+] Removed Langfuse credentials from OpenAI node")
        break

# Step 3: Update workflow
print("[3] Updating workflow...")
r = requests.put(
    f"http://localhost:5678/api/v1/workflows/{wf_id}",
    headers=headers,
    json=workflow
)

if r.status_code == 200:
    print(f"✅ SUCCESS - Workflow fixed!")
    print(f"[+] URL: http://localhost:5678/workflow/{wf_id}")
else:
    print(f"[-] Failed: {r.status_code}")
    print(r.text)
    exit(1)
