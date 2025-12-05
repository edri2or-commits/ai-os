#!/usr/bin/env python3
"""Execute Judge Agent workflow now"""
import json
import urllib.request
import sys
import time

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"

WORKFLOW_ID = "RCaMjVxqwrFEC43i"

print("🚀 Executing Judge Agent...\n", file=sys.stderr)

try:
    # Trigger workflow execution
    req = urllib.request.Request(
        f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}/run",
        data=b'{}',
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read())
        execution_id = result.get("data", {}).get("executionId")
        
        print(f"✅ Execution started! ID: {execution_id}", file=sys.stderr)
        print("   Waiting for completion...", file=sys.stderr)
        
        # Wait and check status
        time.sleep(3)
        
        # Check execution status
        req2 = urllib.request.Request(
            f"http://localhost:5678/api/v1/executions/{execution_id}",
            headers={"X-N8N-API-KEY": N8N_API_KEY}
        )
        
        with urllib.request.urlopen(req2, timeout=5) as response2:
            exec_result = json.loads(response2.read())
            finished = exec_result.get("finished", False)
            
            if finished:
                print("\n✅ Execution completed successfully!", file=sys.stderr)
                print(f"   Check: C:\\Users\\edri2\\Desktop\\AI\\ai-os\\truth-layer\\drift\\faux_pas\\", file=sys.stderr)
            else:
                print("\n⏳ Execution still running...", file=sys.stderr)
                print("   Check status in UI: http://localhost:5678", file=sys.stderr)
                
except urllib.error.HTTPError as e:
    error_body = e.read().decode()
    print(f"\n❌ HTTP {e.code}:", file=sys.stderr)
    print(error_body, file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}", file=sys.stderr)
    sys.exit(1)
