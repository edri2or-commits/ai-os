"""
Check workflow status and optionally activate it
Usage: python check_workflow.py <workflow_id>
"""
import requests
import json
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python check_workflow.py <workflow_id>")
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

print(f"[+] Checking workflow {WORKFLOW_ID}...")
r = requests.get(
    f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
    headers={"X-N8N-API-KEY": api_key}
)

if r.status_code == 200:
    data = r.json()
    print(f"[+] Workflow found: {data.get('name')}")
    print(f"[+] Active: {data.get('active')}")
    print(f"[+] ID: {data.get('id')}")
    print(f"[+] Created: {data.get('createdAt', 'N/A')[:19]}")
    print(f"[+] Updated: {data.get('updatedAt', 'N/A')[:19]}")
    
    # Check for credentials
    nodes = data.get('nodes', [])
    creds_found = []
    for node in nodes:
        if 'credentials' in node:
            creds_found.append(node.get('credentials'))
    
    if creds_found:
        print(f"[+] Credentials found: {len(creds_found)} nodes with credentials")
    
    if not data.get('active'):
        print("[!] Workflow is INACTIVE")
    else:
        print("[+] Workflow is ACTIVE")
else:
    print(f"[-] Workflow NOT FOUND: {r.status_code}")
    print(r.text)
    sys.exit(1)
