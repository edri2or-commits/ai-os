#!/usr/bin/env python3
"""Activate Judge Agent using PUT (full update)"""
import json
import urllib.request
import sys

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"

# Get full workflow
try:
    req = urllib.request.Request(
        "http://localhost:5678/api/v1/workflows",
        headers={"X-N8N-API-KEY": N8N_API_KEY}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        workflows = json.loads(response.read())["data"]
        judge_wf = [w for w in workflows if "Judge Agent" in w["name"]][0]
        wf_id = judge_wf["id"]
        print(f"Found: {judge_wf['name']}", file=sys.stderr)
        print(f"Status: {'ACTIVE' if judge_wf.get('active') else 'INACTIVE'}", file=sys.stderr)
except Exception as e:
    print(f"❌ {e}", file=sys.stderr)
    sys.exit(1)

# Get full workflow details
try:
    req = urllib.request.Request(
        f"http://localhost:5678/api/v1/workflows/{wf_id}",
        headers={"X-N8N-API-KEY": N8N_API_KEY}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        workflow_full = json.loads(response.read())
except Exception as e:
    print(f"❌ Failed to get full workflow: {e}", file=sys.stderr)
    sys.exit(1)

# Update to active
workflow_full["active"] = True

try:
    req = urllib.request.Request(
        f"http://localhost:5678/api/v1/workflows/{wf_id}",
        data=json.dumps(workflow_full).encode('utf-8'),
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        },
        method="PUT"
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        result = json.loads(response.read())
        print(f"\n✅ Workflow activated!", file=sys.stderr)
        print(f"   Status: {'ACTIVE' if result.get('active') else 'INACTIVE'}", file=sys.stderr)
        print(f"   Runs every: 6 hours", file=sys.stderr)
        print(f"   Check: http://localhost:5678", file=sys.stderr)
except Exception as e:
    print(f"\n❌ Activation failed: {e}", file=sys.stderr)
    sys.exit(1)
