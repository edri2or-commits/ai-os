#!/usr/bin/env python3
"""Check last execution error details"""
import json
import urllib.request

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"

# Get latest execution
req = urllib.request.Request(
    "http://localhost:5678/api/v1/executions?limit=1",
    headers={"X-N8N-API-KEY": N8N_API_KEY}
)

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read())
    latest = result["data"][0]
    
    print(f"Execution ID: {latest['id']}")
    print(f"Status: {latest['status']}")
    print(f"Workflow: {latest.get('workflowData', {}).get('name')}")
    print(f"\nError details:")
    
    # Try to get error from data
    if latest.get('data'):
        print(json.dumps(latest['data'], indent=2))
    else:
        print("No error data available")
