"""List workflows from local n8n instance."""
import requests
import json

# Local n8n configuration
LOCAL_URL = 'http://localhost:5678/api/v1/workflows'
LOCAL_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io'

headers = {'X-N8N-API-KEY': LOCAL_API_KEY}

print("Fetching workflows from local n8n...")
response = requests.get(LOCAL_URL, headers=headers)

if response.status_code == 200:
    workflows = response.json()['data']
    print(f'\n=== LOCAL N8N WORKFLOWS ({len(workflows)} total) ===\n')
    
    for w in workflows:
        active_status = '[ACTIVE]' if w.get('active') else '[INACTIVE]'
        print(f'{active_status} {w["name"]}')
        print(f'   ID: {w["id"]}')
        print(f'   Nodes: {len(w.get("nodes", []))}')
        print()
    
    # Save workflow IDs for import
    workflow_ids = [w['id'] for w in workflows]
    with open('workflow_ids_to_import.txt', 'w') as f:
        f.write('\n'.join(workflow_ids))
    
    print(f'Saved {len(workflow_ids)} workflow IDs to workflow_ids_to_import.txt')
else:
    print(f'Error: {response.status_code}')
    print(response.text)
