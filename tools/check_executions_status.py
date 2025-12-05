#!/usr/bin/env python3
"""Check if workflow can READ files now (test the volume mount)"""
import json
import urllib.request
import sys
import time

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"

print("🔍 בודק execution history...\n", file=sys.stderr)

try:
    req = urllib.request.Request(
        "http://localhost:5678/api/v1/executions",
        headers={"X-N8N-API-KEY": N8N_API_KEY}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        result = json.loads(response.read())
        executions = result.get("data", [])
        
        # Filter Judge Agent executions
        judge_execs = [e for e in executions if "Judge" in str(e.get("workflowData", {}).get("name", ""))]
        
        if not judge_execs:
            print("⚠️  אין executions של Judge Agent עדיין", file=sys.stderr)
            print("   (זה בסדר - workflow עדיין לא הופעל)", file=sys.stderr)
        else:
            print(f"מצאתי {len(judge_execs)} executions של Judge Agent:\n", file=sys.stderr)
            for i, ex in enumerate(judge_execs[:3], 1):
                status = "✅" if ex.get("finished") else "❌"
                started = ex.get("startedAt", "unknown")
                print(f"{i}. {status} {started}", file=sys.stderr)
                if not ex.get("finished") and ex.get("data"):
                    error_msg = str(ex.get("data", {}).get("resultData", {}).get("error", ""))[:100]
                    if error_msg:
                        print(f"   שגיאה: {error_msg}...", file=sys.stderr)
        
        print(f"\n📊 סטטוס כללי: {len(executions)} executions במערכת", file=sys.stderr)
        
except Exception as e:
    print(f"❌ {e}", file=sys.stderr)
    sys.exit(1)
