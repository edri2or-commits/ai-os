"""
Delete old workflow and import fixed version
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

headers = {
    "X-N8N-API-KEY": api_key,
    "Content-Type": "application/json"
}

old_wf_id = "SF9E5Dr8AeAqzoq2"

# Step 1: Delete old workflow
print(f"[1] Deleting old workflow: {old_wf_id}...")
r = requests.delete(
    f"http://localhost:5678/api/v1/workflows/{old_wf_id}",
    headers=headers
)

if r.status_code in [200, 204]:
    print(f"   [+] Deleted successfully")
else:
    print(f"   [-] Delete failed: {r.status_code} (continuing anyway)")

# Step 2: Load and fix workflow JSON
print("[2] Loading workflow JSON...")
wf_file = Path(__file__).parent.parent / "n8n_workflows" / "judge_agent_v2_langfuse.json"
with open(wf_file, 'r', encoding='utf-8') as f:
    workflow = json.load(f)

# Remove 'active' field
if 'active' in workflow:
    del workflow['active']

# Step 3: Fix nodes
print("[3] Fixing nodes...")

# Get credential ID
cred_id_file = Path(__file__).parent / "langfuse_cred_id.txt"
cred_id = cred_id_file.read_text().strip()

for node in workflow.get('nodes', []):
    node_name = node.get('name')
    node_type = node.get('type')
    
    # Fix Langfuse HTTP Request node (keep Langfuse credentials)
    if node_name == 'Fetch Langfuse Traces (Last 6hr)':
        node['credentials'] = {
            'httpBasicAuth': {
                'id': cred_id,
                'name': 'Langfuse API'
            }
        }
        print(f"   [+] Fixed: {node_name} (Langfuse creds)")
    
    # Fix OpenAI node (remove credentials, use env var)
    elif node_name == 'Call GPT-4o Judge':
        # Remove authentication fields
        if 'authentication' in node.get('parameters', {}):
            del node['parameters']['authentication']
        if 'genericAuthType' in node.get('parameters', {}):
            del node['parameters']['genericAuthType']
        
        # Remove credentials
        if 'credentials' in node:
            del node['credentials']
        
        print(f"   [+] Fixed: {node_name} (removed wrong creds, using $env.OPENAI_API_KEY)")

# Step 4: Import new workflow
print("[4] Importing fixed workflow...")
r = requests.post(
    "http://localhost:5678/api/v1/workflows",
    headers=headers,
    json=workflow
)

if r.status_code in [200, 201]:
    result = r.json()
    new_id = result.get('id')
    print(f"✅ SUCCESS - Workflow imported!")
    print(f"[+] New ID: {new_id}")
    
    # Activate
    print("[5] Activating...")
    activate = requests.patch(
        f"http://localhost:5678/api/v1/workflows/{new_id}",
        headers=headers,
        json={"active": True}
    )
    
    if activate.status_code == 200:
        print(f"✅ ACTIVATED")
    
    # Save ID
    id_file = Path(__file__).parent / "judge_workflow_id.txt"
    id_file.write_text(new_id)
    print(f"[+] Saved ID: {new_id}")
    print(f"[+] URL: http://localhost:5678/workflow/{new_id}")
    
else:
    print(f"[-] Import failed: {r.status_code}")
    print(r.text)
