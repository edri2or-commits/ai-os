import requests
import json

# VPS n8n endpoint
N8N_URL = "https://n8n.35.223.68.23.nip.io"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZDkzZjUzZC0wYmU1LTRjNzUtYmZiOS1mNDUwOTNmM2NhYzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY1MDU4NjAwLCJleHAiOjE3Njc2NTA0MDB9.PG_jISgSnSwoy21dJFR7pkM6qpQ9EzngcI2EaRnAoVQ"

# Workflow JSON (with settings)
workflow = {
    "name": "Infrastructure Test 1 - HTTP Request",
    "nodes": [
        {
            "parameters": {},
            "name": "Start",
            "type": "n8n-nodes-base.manualTrigger",
            "typeVersion": 1,
            "position": [240, 300],
            "id": "start-node"
        },
        {
            "parameters": {
                "url": "https://httpbin.org/get",
                "options": {}
            },
            "name": "HTTP Request",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [460, 300],
            "id": "http-node"
        }
    ],
    "connections": {
        "Start": {
            "main": [
                [
                    {
                        "node": "HTTP Request",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
    },
    "settings": {
        "executionOrder": "v1"
    }
}

print("Importing workflow to VPS n8n...")
print("URL: " + N8N_URL + "/api/v1/workflows")

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

try:
    response = requests.post(
        N8N_URL + "/api/v1/workflows",
        headers=headers,
        json=workflow,
        timeout=10
    )
    print("\nStatus: " + str(response.status_code))
    
    if response.status_code == 200 or response.status_code == 201:
        data = response.json()
        workflow_id = data.get('id')
        workflow_name = data.get('name')
        print("\nSUCCESS!")
        print("Workflow ID: " + str(workflow_id))
        print("Workflow Name: " + str(workflow_name))
        print("\nOpen in browser:")
        print(N8N_URL + "/workflow/" + str(workflow_id))
    else:
        print("\nError response:")
        print(response.text)
        
except Exception as e:
    print("\nError: " + str(e))
