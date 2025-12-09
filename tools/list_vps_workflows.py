import requests
import json

# VPS n8n endpoint
N8N_URL = "https://n8n.35.223.68.23.nip.io"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZDkzZjUzZC0wYmU1LTRjNzUtYmZiOS1mNDUwOTNmM2NhYzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY1MDU4NjAwLCJleHAiOjE3Njc2NTA0MDB9.PG_jISgSnSwoy21dJFR7pkM6qpQ9EzngcI2EaRnAoVQ"

print("Listing all workflows on VPS...")

headers = {
    "X-N8N-API-KEY": API_KEY
}

try:
    response = requests.get(
        N8N_URL + "/api/v1/workflows",
        headers=headers,
        timeout=10
    )
    
    print("\nStatus: " + str(response.status_code))
    
    if response.status_code == 200:
        data = response.json()
        workflows = data.get('data', [])
        print("\nFound " + str(len(workflows)) + " workflows:")
        for wf in workflows:
            print("\n- ID: " + wf.get('id'))
            print("  Name: " + wf.get('name'))
            print("  Active: " + str(wf.get('active')))
    else:
        print("\nError:")
        print(response.text)
        
except Exception as e:
    print("\nError: " + str(e))
