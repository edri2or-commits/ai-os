import requests
import urllib3
import json
urllib3.disable_warnings()

r = requests.get(
    'https://n8n.35.223.68.23.nip.io/api/v1/workflows',
    headers={'X-N8N-API-KEY': 'n8n_api_bSIFNW5tn24T0k'},
    verify=False
)

print(f'Status: {r.status_code}')
print(f'Response: {json.dumps(r.json(), indent=2)}')
