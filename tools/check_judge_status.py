"""Check Judge workflow executions"""
import requests
from pathlib import Path

env_path = Path(__file__).parent.parent / "infra" / "n8n" / ".env"
api_key = None
for line in env_path.read_text().split('\n'):
    if line.startswith('N8N_API_KEY='):
        api_key = line.split('=', 1)[1].strip()
        break

wf_id = "cJVkH8vMkTLkN875"

r = requests.get(
    f"http://localhost:5678/api/v1/executions",
    params={"workflowId": wf_id},
    headers={"X-N8N-API-KEY": api_key}
)

print(f"Status: {r.status_code}")
data = r.json()
print(f"Keys: {list(data.keys())}")

if 'data' in data:
    execs = data['data']
    print(f"\nTotal executions: {len(execs)}")
    if execs:
        for e in execs[:3]:
            print(f"  - {e['startedAt']}: {e['status']}")
    else:
        print("  No executions yet (will run in next 6 hours)")
