"""
Check which HTTP nodes exist in workflow
"""
import requests
import json
from pathlib import Path

WORKFLOW_ID = "tlrJ6tQ3ymr4R2sF"

# Read API key
env_path = Path(__file__).parent.parent / "infra" / "n8n" / ".env"
api_key = None

if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('N8N_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
                break

r = requests.get(
    f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
    headers={"X-N8N-API-KEY": api_key}
)

wf = r.json()

print(f"\n=== Workflow Nodes Analysis ===")
print(f"Name: {wf.get('name')}")
print(f"\nNodes:")

for node in wf.get('nodes', []):
    node_type = node.get('type')
    node_name = node.get('name')
    
    print(f"\n- {node_name} ({node_type})")
    
    # Check if HTTP Request (Langfuse)
    if 'httpRequest' in node_type.lower():
        params = node.get('parameters', {})
        url = params.get('url', 'N/A')
        print(f"  URL: {url}")
        
        # Check credentials
        creds = node.get('credentials', {})
        if creds:
            print(f"  Credentials: {creds}")
        else:
            print(f"  Credentials: MISSING ❌")
    
    # Check if Code node (might have Langfuse SDK)
    if 'code' in node_type.lower():
        code = node.get('parameters', {}).get('jsCode', '')
        if 'langfuse' in code.lower():
            print(f"  Uses Langfuse SDK: YES")
        else:
            print(f"  Uses Langfuse SDK: NO")

print(f"\n=== Verdict ===")
nodes_list = [n.get('name') for n in wf.get('nodes', [])]
if any('langfuse' in n.lower() for n in nodes_list):
    print("This is Judge V2 with Langfuse ✅")
else:
    print("This might be Judge V1 (no Langfuse) ⚠️")
