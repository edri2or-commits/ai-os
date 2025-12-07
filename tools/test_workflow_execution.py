import requests
import json

# VPS n8n endpoint
N8N_URL = "https://n8n.35.223.68.23.nip.io"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZDkzZjUzZC0wYmU1LTRjNzUtYmZiOS1mNDUwOTNmM2NhYzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY1MDU4NjAwLCJleHAiOjE3Njc2NTA0MDB9.PG_jISgSnSwoy21dJFR7pkM6qpQ9EzngcI2EaRnAoVQ"
WORKFLOW_ID = "KvXai5AffNBh5YxW"

print("Testing workflow execution...")
print("Workflow ID: " + WORKFLOW_ID)

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

try:
    # Execute the workflow
    response = requests.post(
        N8N_URL + "/api/v1/workflows/" + WORKFLOW_ID + "/execute",
        headers=headers,
        timeout=15
    )
    
    print("\nStatus: " + str(response.status_code))
    
    if response.status_code == 200:
        data = response.json()
        print("\nSUCCESS! Workflow executed.")
        print("\nExecution result:")
        print(json.dumps(data, indent=2))
    else:
        print("\nError:")
        print(response.text)
        
except Exception as e:
    print("\nError: " + str(e))
