#!/usr/bin/env python3
"""Execute workflow via test endpoint"""
import json
import urllib.request
import sys
import time

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"

WORKFLOW_ID = "RCaMjVxqwrFEC43i"

print("🚀 Testing Judge Agent execution...\n", file=sys.stderr)

# Try the test-webhook endpoint (for manual testing)
try:
    req = urllib.request.Request(
        f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}/test",
        data=b'{"data":{}}',
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=45) as response:
        result = json.loads(response.read())
        print("✅ Execution completed!", file=sys.stderr)
        print(json.dumps(result, indent=2))
        
except urllib.error.HTTPError as e:
    error_body = e.read().decode()
    print(f"❌ HTTP {e.code}:", file=sys.stderr)
    
    # If test doesn't work, just open the UI
    print("\nOpening n8n UI for manual execution...", file=sys.stderr)
    import webbrowser
    webbrowser.open(f"http://localhost:5678/workflow/{WORKFLOW_ID}")
    print(f"\n👆 Click 'Test workflow' or 'Execute' in the UI", file=sys.stderr)
    
except Exception as e:
    print(f"❌ {e}", file=sys.stderr)
    sys.exit(1)
