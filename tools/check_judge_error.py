#!/usr/bin/env python3
"""Get detailed error from latest Judge Agent execution"""
import json
import urllib.request
import sys

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"

try:
    # Get latest execution ID (4)
    req = urllib.request.Request(
        "http://localhost:5678/api/v1/executions/4",
        headers={"X-N8N-API-KEY": N8N_API_KEY}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        execution = json.loads(response.read())
        
        print("🔍 Execution Details:\n", file=sys.stderr)
        print(f"Status: {execution.get('status')}", file=sys.stderr)
        print(f"Mode: {execution.get('mode')}", file=sys.stderr)
        print(f"Started: {execution.get('startedAt')}", file=sys.stderr)
        print(f"Stopped: {execution.get('stoppedAt')}", file=sys.stderr)
        
        # Get error from data
        data = execution.get('data', {})
        result = data.get('resultData', {})
        
        if 'error' in result:
            print(f"\n❌ ERROR: {result['error']}", file=sys.stderr)
        
        # Check runData for node errors
        run_data = result.get('runData', {})
        for node_name, node_data in run_data.items():
            for run in node_data:
                if 'error' in run:
                    print(f"\n❌ Node '{node_name}' error:", file=sys.stderr)
                    print(f"   {run['error']}", file=sys.stderr)
        
        # Full JSON for inspection
        print("\n" + json.dumps(execution, indent=2))
        
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
