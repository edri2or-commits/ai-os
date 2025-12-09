#!/usr/bin/env python3
"""Check Judge Agent executions"""
import json
import urllib.request
import sys

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"

try:
    req = urllib.request.Request(
        "http://localhost:5678/api/v1/executions?workflowId=judge-agent-v1&limit=5",
        headers={"X-N8N-API-KEY": N8N_API_KEY}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read())
        executions = data.get("data", [])
        
        if not executions:
            print("❌ No executions found - workflow never ran!", file=sys.stderr)
        else:
            print(f"📊 Found {len(executions)} executions:\n", file=sys.stderr)
            for ex in executions:
                status = "✅" if ex.get("finished") else "❌"
                print(f"{status} {ex.get('startedAt')} - {ex.get('status', 'unknown')}", file=sys.stderr)
                if ex.get("stoppedAt"):
                    print(f"   Error: {ex.get('data', {}).get('resultData', {}).get('error')}", file=sys.stderr)
        
        print(json.dumps(executions, indent=2))
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
