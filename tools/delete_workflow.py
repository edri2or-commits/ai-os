"""
Delete workflow from n8n
Usage: python delete_workflow.py <workflow_id>
"""
import requests
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python delete_workflow.py <workflow_id>")
    sys.exit(1)

WORKFLOW_ID = sys.argv[1]

# Read API key from .env
env_path = Path(__file__).parent.parent / "infra" / "n8n" / ".env"
api_key = None

if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('N8N_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
                break

if not api_key:
    print("ERROR: N8N_API_KEY not found in .env")
    sys.exit(1)

# First, get workflow name
print(f"[+] Fetching workflow info...")
r = requests.get(
    f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
    headers={"X-N8N-API-KEY": api_key}
)

if r.status_code != 200:
    print(f"[-] Workflow NOT FOUND: {r.status_code}")
    sys.exit(1)

wf_name = r.json().get('name', 'Unknown')
print(f"[+] Found: {wf_name}")
print(f"[!] Deleting workflow {WORKFLOW_ID}...")

# Delete
response = requests.delete(
    f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
    headers={"X-N8N-API-KEY": api_key}
)

if response.status_code == 200:
    print(f"[+] SUCCESS - Workflow deleted")
else:
    print(f"[-] FAILED: {response.status_code}")
    print(response.text)
    sys.exit(1)
