"""
Test workflow execution
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

if not api_key:
    print("[-] ERROR: N8N_API_KEY not found")
    exit(1)

# Read workflow ID
wf_id_file = Path(__file__).parent / "judge_workflow_id.txt"
wf_id = wf_id_file.read_text().strip()

print(f"[+] Testing workflow: {wf_id}")

# Trigger manual execution
r = requests.post(
    f"http://localhost:5678/api/v1/workflows/{wf_id}/execute",
    headers={
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }
)

if r.status_code == 200:
    result = r.json()
    print(f"[+] Execution started!")
    print(f"[+] Execution ID: {result.get('data', {}).get('executionId')}")
    
    # Wait a bit and check status
    import time
    time.sleep(3)
    
    exec_id = result.get('data', {}).get('executionId')
    if exec_id:
        status = requests.get(
            f"http://localhost:5678/api/v1/executions/{exec_id}",
            headers={"X-N8N-API-KEY": api_key}
        )
        if status.status_code == 200:
            exec_data = status.json()
            finished = exec_data.get('finished')
            status_text = exec_data.get('status')
            print(f"[+] Status: {status_text}")
            print(f"[+] Finished: {finished}")
            
            if status_text == 'success':
                print(f"✅ WORKFLOW WORKS!")
            else:
                print(f"❌ Execution failed")
                print(exec_data)
else:
    print(f"[-] FAILED: {r.status_code}")
    print(r.text)
