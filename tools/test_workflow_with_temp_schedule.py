"""
Temporarily change schedule to 1 minute, wait for execution, restore to 6 hours
"""
import requests
import json
import time
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

print(f"[+] Testing workflow: {wf_id}")

# Step 1: Get current workflow
print("[1] Fetching current workflow...")
r = requests.get(
    f"http://localhost:5678/api/v1/workflows/{wf_id}",
    headers=headers
)
if r.status_code != 200:
    print(f"[-] Failed to fetch: {r.status_code}")
    exit(1)

workflow = r.json()
print(f"[+] Current workflow fetched")

# Step 2: Modify schedule to 1 minute
print("[2] Changing schedule to 1 minute...")
for node in workflow.get('nodes', []):
    if node.get('type') == 'n8n-nodes-base.scheduleTrigger':
        node['parameters'] = {
            "rule": {
                "interval": [
                    {
                        "field": "minutes",
                        "minutesInterval": 1
                    }
                ]
            }
        }
        print(f"[+] Modified schedule trigger")

# Step 3: Update workflow
r = requests.put(
    f"http://localhost:5678/api/v1/workflows/{wf_id}",
    headers=headers,
    json=workflow
)
if r.status_code != 200:
    print(f"[-] Failed to update: {r.status_code}")
    print(r.text)
    exit(1)

print(f"[+] Workflow updated - will run in ~1 minute")

# Step 4: Wait and check for execution
print("[3] Waiting 90 seconds for execution...")
time.sleep(90)

# Step 5: Check executions
print("[4] Checking executions...")
r = requests.get(
    f"http://localhost:5678/api/v1/executions",
    headers=headers,
    params={"workflowId": wf_id}
)

if r.status_code == 200:
    executions = r.json().get('data', [])
    if executions:
        latest = executions[0]
        print(f"✅ EXECUTION FOUND!")
        print(f"   ID: {latest.get('id')}")
        print(f"   Status: {latest.get('status')}")
        print(f"   Finished: {latest.get('finished')}")
        
        if latest.get('status') == 'success':
            print(f"   ✅ WORKFLOW WORKS!")
        else:
            print(f"   ❌ Execution failed")
    else:
        print(f"❌ No executions yet (waited 90s)")
else:
    print(f"[-] Failed to check: {r.status_code}")

# Step 6: Restore 6-hour schedule
print("[5] Restoring 6-hour schedule...")
for node in workflow.get('nodes', []):
    if node.get('type') == 'n8n-nodes-base.scheduleTrigger':
        node['parameters'] = {
            "rule": {
                "interval": [
                    {
                        "field": "hours",
                        "hoursInterval": 6
                    }
                ]
            }
        }

r = requests.put(
    f"http://localhost:5678/api/v1/workflows/{wf_id}",
    headers=headers,
    json=workflow
)
if r.status_code == 200:
    print(f"[+] Schedule restored to 6 hours ✅")
else:
    print(f"[-] Failed to restore: {r.status_code}")
