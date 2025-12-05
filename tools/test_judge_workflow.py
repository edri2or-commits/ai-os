#!/usr/bin/env python3
"""Test Judge Agent workflow manually"""
import json
import urllib.request
import sys

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"

# Get workflow ID
try:
    req = urllib.request.Request(
        "http://localhost:5678/api/v1/workflows",
        headers={"X-N8N-API-KEY": N8N_API_KEY}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        workflows = json.loads(response.read())["data"]
        judge_wf = [w for w in workflows if "Judge Agent" in w["name"]][0]
        wf_id = judge_wf["id"]
        print(f"Found workflow: {judge_wf['name']} (ID: {wf_id})", file=sys.stderr)
except Exception as e:
    print(f"❌ Failed to find workflow: {e}", file=sys.stderr)
    sys.exit(1)

# Execute workflow manually
try:
    req = urllib.request.Request(
        f"http://localhost:5678/api/v1/workflows/{wf_id}/execute",
        data=b'{}',
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read())
        print(f"\n✅ Execution completed!", file=sys.stderr)
        print(f"   Finished: {result.get('finished', False)}", file=sys.stderr)
        print(f"   Status: {result.get('data', {}).get('resultData', {}).get('runData', {})}", file=sys.stderr)
        
        # Print full result for inspection
        print(json.dumps(result, indent=2))
except Exception as e:
    print(f"\n❌ Execution failed: {e}", file=sys.stderr)
    sys.exit(1)
