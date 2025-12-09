"""Activate Judge Agent V2 on VPS using PATCH method."""
import requests

VPS_URL = 'https://n8n.35.223.68.23.nip.io/api/v1'
VPS_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZDkzZjUzZC0wYmU1LTRjNzUtYmZiOS1mNDUwOTNmM2NhYzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY1MDU4NjAwLCJleHAiOjE3Njc2NTA0MDB9.PG_jISgSnSwoy21dJFR7pkM6qpQ9EzngcI2EaRnAoVQ'

JUDGE_ID = 'QHZWeVUSdD4EZxUS'

# Try to activate using PATCH
url = f'{VPS_URL}/workflows/{JUDGE_ID}'
headers = {
    'X-N8N-API-KEY': VPS_API_KEY,
    'Content-Type': 'application/json'
}

payload = {'active': True}

print(f'Activating Judge Agent V2 (ID: {JUDGE_ID})...')
response = requests.patch(url, headers=headers, json=payload)

if response.status_code == 200:
    workflow = response.json()
    is_active = workflow.get('active', False)
    print(f'[OK] Workflow activated: {is_active}')
    print(f'Name: {workflow.get("name")}')
    print(f'Nodes: {len(workflow.get("nodes", []))}')
else:
    print(f'[ERROR] {response.status_code}')
    print(response.text)
