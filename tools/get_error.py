import requests
import json

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"
WORKFLOW_ID = "aGrqrbb8DIP6kwUt"

print("[+] Getting last execution details...")
r = requests.get(
    f"http://localhost:5678/api/v1/executions",
    headers={"X-N8N-API-KEY": API_KEY},
    params={"workflowId": WORKFLOW_ID, "limit": 1, "includeData": "true"}
)

if r.status_code == 200:
    data = r.json()
    if data.get('data'):
        exec_data = data['data'][0]
        print(f"[+] Execution ID: {exec_data.get('id')}")
        print(f"[+] Status: {exec_data.get('status')}")
        
        # Look for error in data
        exec_json = exec_data.get('data', {})
        result_data = exec_json.get('resultData', {})
        
        if result_data.get('error'):
            error = result_data['error']
            print(f"\n[-] ERROR FOUND:")
            print(f"    Message: {error.get('message')}")
            print(f"    Node: {error.get('node', {}).get('name')}")
        
        # Check each node for errors
        for node_name, node_data in exec_json.get('executionData', {}).get('nodeExecutionStack', [[]])[0]:
            if isinstance(node_data, dict) and node_data.get('error'):
                print(f"\n[-] Node '{node_name}' error:")
                print(f"    {node_data['error']}")
    else:
        print("[!] No executions found")
else:
    print(f"[-] Failed: {r.status_code}")
