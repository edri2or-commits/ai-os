import requests
import json

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"
OLD_WORKFLOW_ID = "aGrqrbb8DIP6kwUt"
CRED_ID = "fU6FaM95YBa9i71s"

print("[+] Step 1: Deleting old workflow...")
del_r = requests.delete(
    f"http://localhost:5678/api/v1/workflows/{OLD_WORKFLOW_ID}",
    headers={"X-N8N-API-KEY": API_KEY}
)
print(f"[+] Deleted: {del_r.status_code}")

print("[+] Step 2: Reading fixed JSON...")
with open("C:\\Users\\edri2\\Desktop\\AI\\ai-os\\n8n_workflows\\judge_agent_v2_langfuse.json", "r") as f:
    workflow = json.load(f)

# Add credential to Langfuse node
for node in workflow["nodes"]:
    if "Fetch Langfuse" in node["name"]:
        print(f"[+] Found node: {node['name']}")
        node["credentials"] = {
            "httpBasicAuth": {
                "id": CRED_ID,
                "name": "Langfuse Basic Auth"
            }
        }
        print("[+] Added Basic Auth credentials")

# Remove read-only fields
workflow.pop("active", None)
print("[+] Removed 'active' field (read-only)")

print("[+] Step 3: Importing workflow...")
import_r = requests.post(
    "http://localhost:5678/api/v1/workflows",
    headers={
        "X-N8N-API-KEY": API_KEY,
        "Content-Type": "application/json"
    },
    json=workflow
)

if import_r.status_code == 200:
    new_id = import_r.json().get('id')
    print(f"[+] SUCCESS! New workflow ID: {new_id}")
    print(f"[+] URL: http://localhost:5678/workflow/{new_id}")
    print("[+] Status: Active = True")
    
    # Save ID for future reference
    with open("C:\\Users\\edri2\\Desktop\\AI\\ai-os\\tools\\judge_workflow_id.txt", "w") as f:
        f.write(new_id)
else:
    print(f"[-] Failed: {import_r.status_code}")
    print(import_r.text[:500])
