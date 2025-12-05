import requests
import json

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"
WORKFLOW_ID = "aGrqrbb8DIP6kwUt"

print("[+] Checking workflow status...")
r = requests.get(
    f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
    headers={"X-N8N-API-KEY": API_KEY}
)

if r.status_code == 200:
    data = r.json()
    print(f"[+] Workflow found: {data.get('name')}")
    print(f"[+] Active: {data.get('active')}")
    print(f"[+] ID: {data.get('id')}")
    
    if not data.get('active'):
        print("[!] Workflow is INACTIVE. Activating...")
        activate = requests.patch(
            f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
            headers={"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"},
            json={"active": True}
        )
        if activate.status_code == 200:
            print("[+] Activation SUCCESS")
        else:
            print(f"[-] Activation FAILED: {activate.status_code}")
            print(activate.text)
    else:
        print("[+] Workflow already ACTIVE")
else:
    print(f"[-] Workflow NOT FOUND: {r.status_code}")
    print(r.text)
