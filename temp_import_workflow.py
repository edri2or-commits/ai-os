import requests
import urllib3
import json

urllib3.disable_warnings()

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io'

# Read workflow JSON
with open(r'C:\Users\edri2\Desktop\AI\ai-os\n8n_workflows\judge_agent_v2_langfuse.json', 'r', encoding='utf-8') as f:
    workflow = json.load(f)

# Import to VPS n8n
url = 'https://n8n.35.223.68.23.nip.io/api/v1/workflows'

response = requests.post(
    url,
    json=workflow,
    headers={'X-N8N-API-KEY': API_KEY},
    verify=False
)

print(f'Status: {response.status_code}')
if response.status_code in [200, 201]:
    result = response.json()
    print(f'OK Imported: {result["name"]} (id={result["id"]})')
else:
    print(f'Error: {response.text}')
