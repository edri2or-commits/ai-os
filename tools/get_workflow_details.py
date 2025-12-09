"""
Get full workflow details including nodes and credentials
"""
import requests
import json
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python get_workflow_details.py <workflow_id>")
    sys.exit(1)

WORKFLOW_ID = sys.argv[1]

# Read API key
env_path = Path(__file__).parent.parent / "infra" / "n8n" / ".env"
api_key = None

if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('N8N_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
                break

if not api_key:
    print("ERROR: N8N_API_KEY not found")
    sys.exit(1)

# Get workflow
r = requests.get(
    f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
    headers={"X-N8N-API-KEY": api_key}
)

if r.status_code != 200:
    print(f"ERROR: {r.status_code}")
    sys.exit(1)

wf = r.json()

print(f"\n=== Workflow: {wf.get('name')} ===")
print(f"ID: {wf.get('id')}")
print(f"Active: {wf.get('active')}")
print(f"Created: {wf.get('createdAt', 'N/A')[:19]}")
print(f"Updated: {wf.get('updatedAt', 'N/A')[:19]}")

# Check trigger
print(f"\n=== Trigger Configuration ===")
nodes = wf.get('nodes', [])
for node in nodes:
    if 'Trigger' in node.get('type', ''):
        print(f"Type: {node.get('type')}")
        print(f"Name: {node.get('name')}")
        params = node.get('parameters', {})
        print(f"Parameters: {json.dumps(params, indent=2)}")

# Check credentials
print(f"\n=== Credentials ===")
creds_found = False
for node in nodes:
    if 'credentials' in node:
        creds_found = True
        print(f"Node: {node.get('name')}")
        for cred_type, cred_info in node.get('credentials', {}).items():
            print(f"  Type: {cred_type}")
            print(f"  ID: {cred_info.get('id', 'N/A')}")
            print(f"  Name: {cred_info.get('name', 'N/A')}")

if not creds_found:
    print("No credentials configured!")

# Check if schedule is set
print(f"\n=== Schedule Status ===")
settings = wf.get('settings', {})
print(f"Settings: {json.dumps(settings, indent=2)}")
