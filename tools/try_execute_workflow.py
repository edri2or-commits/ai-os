"""
Try different execution methods for n8n workflow
"""
import requests
from pathlib import Path

# Read API key
env_path = Path(__file__).parent.parent / "infra" / "n8n" / ".env"
api_key = None
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('N8N_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
                break

wf_id = Path(__file__).parent / "judge_workflow_id.txt"
wf_id = wf_id.read_text().strip()

headers = {
    "X-N8N-API-KEY": api_key,
    "Content-Type": "application/json"
}

# Method 1: POST /workflows/{id}/execute
print("[1] Trying POST /workflows/{id}/execute...")
r1 = requests.post(
    f"http://localhost:5678/api/v1/workflows/{wf_id}/execute",
    headers=headers
)
print(f"    Result: {r1.status_code} - {r1.text[:200]}")

# Method 2: POST /executions (with workflowId in body)
print("\n[2] Trying POST /executions...")
r2 = requests.post(
    "http://localhost:5678/api/v1/executions",
    headers=headers,
    json={"workflowId": wf_id}
)
print(f"    Result: {r2.status_code} - {r2.text[:200]}")

# Method 3: GET /workflows/{id}/activate (toggle)
print("\n[3] Trying toggle active...")
r3 = requests.get(
    f"http://localhost:5678/api/v1/workflows/{wf_id}/activate",
    headers=headers
)
print(f"    Result: {r3.status_code} - {r3.text[:200]}")

# Method 4: Manual execution page link
print("\n[4] Manual execution via UI:")
print(f"    Open: http://localhost:5678/workflow/{wf_id}")
print(f"    Click: Test workflow button")
