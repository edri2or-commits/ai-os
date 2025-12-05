#!/usr/bin/env python3
"""Import with detailed error"""
import json
import urllib.request
import sys

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"

with open("C:\\Users\\edri2\\Desktop\\AI\\ai-os\\n8n_workflows\\judge_agent.json", "r") as f:
    workflow = json.load(f)

# Remove fields that might cause problems
workflow_clean = {
    "name": workflow["name"],
    "nodes": workflow["nodes"],
    "connections": workflow["connections"],
    "settings": workflow.get("settings", {})
}

try:
    req = urllib.request.Request(
        "http://localhost:5678/api/v1/workflows",
        data=json.dumps(workflow_clean).encode('utf-8'),
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        print(f"✅ Success! ID: {result['id']}", file=sys.stderr)
except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
