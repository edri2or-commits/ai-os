#!/usr/bin/env python3
"""Import fixed Judge Agent workflow to n8n"""
import json
import urllib.request
import sys

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"

# Read workflow JSON
with open("C:\\Users\\edri2\\Desktop\\AI\\ai-os\\n8n_workflows\\judge_agent.json", "r") as f:
    workflow = json.load(f)

# Delete old workflow first
try:
    req = urllib.request.Request(
        "http://localhost:5678/api/v1/workflows/judge-agent-v1",
        headers={"X-N8N-API-KEY": N8N_API_KEY},
        method="DELETE"
    )
    urllib.request.urlopen(req, timeout=5)
    print("✅ Deleted old workflow", file=sys.stderr)
except:
    print("⚠️  Old workflow not found (OK)", file=sys.stderr)

# Create new workflow
try:
    req = urllib.request.Request(
        "http://localhost:5678/api/v1/workflows",
        data=json.dumps(workflow).encode('utf-8'),
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        result = json.loads(response.read())
        print(f"✅ Imported workflow: {result['name']}", file=sys.stderr)
        print(f"   ID: {result['id']}", file=sys.stderr)
except Exception as e:
    print(f"❌ Import failed: {e}", file=sys.stderr)
    sys.exit(1)
