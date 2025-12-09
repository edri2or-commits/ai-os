import requests
import json

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"
WORKFLOW_ID = "aGrqrbb8DIP6kwUt"

print("[+] Checking last execution...")
r = requests.get(
    f"http://localhost:5678/api/v1/executions",
    headers={"X-N8N-API-KEY": API_KEY},
    params={"workflowId": WORKFLOW_ID, "limit": 1}
)

if r.status_code == 200:
    data = r.json()
    if data.get('data'):
        exec_data = data['data'][0]
        print(f"[+] Last execution found:")
        print(f"    Status: {exec_data.get('status')}")
        print(f"    Started: {exec_data.get('startedAt')}")
        print(f"    Finished: {exec_data.get('stoppedAt')}")
        print(f"    Mode: {exec_data.get('mode')}")
    else:
        print("[!] No executions found yet")
        print("[!] Triggering manual test execution...")
        
        # Manual trigger
        trigger = requests.post(
            f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}/execute",
            headers={"X-N8N-API-KEY": API_KEY}
        )
        if trigger.status_code == 200:
            print("[+] Test execution STARTED")
        else:
            print(f"[-] Test execution FAILED: {trigger.status_code}")
else:
    print(f"[-] Failed to check executions: {r.status_code}")
