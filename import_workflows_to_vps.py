import json
import requests

# VPS n8n endpoint
N8N_URL = "https://n8n.35.223.68.23.nip.io/api/v1"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

# Load workflows
with open(r'C:\Users\edri2\Desktop\AI\ai-os\exports\workflows_local_backup_20251206_233656.json', encoding='utf-8') as f:
    workflows = json.load(f)

# Filter: skip TEST workflow
workflows_to_import = [w for w in workflows if "TEST" not in w["name"]]

print(f"Importing {len(workflows_to_import)} workflows...\n")

for i, workflow in enumerate(workflows_to_import):
    name = workflow["name"]
    print(f"{i+1}. Importing: {name}... ", end="")
    
    # Remove id (n8n will generate new one)
    workflow_data = workflow.copy()
    if "id" in workflow_data:
        del workflow_data["id"]
    
    try:
        response = requests.post(
            f"{N8N_URL}/workflows",
            headers=headers,
            json=workflow_data,
            verify=False  # Skip SSL verification for self-signed cert
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"OK Success (ID: {result.get('id', 'N/A')})")
        else:
            print(f"FAIL: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

print("\nOK Import complete!")
