#!/usr/bin/env python3
"""Activate Judge Agent V2 - Langfuse Integration"""
import json
import urllib.request
import sys

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"
WORKFLOW_ID = "aGrqrbb8DIP6kwUt"

# Get workflow
print("=" * 60, file=sys.stderr)
print("Activating Judge Agent V2 - Langfuse Integration", file=sys.stderr)
print("=" * 60, file=sys.stderr)

try:
    req = urllib.request.Request(
        f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
        headers={"X-N8N-API-KEY": N8N_API_KEY}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        workflow = json.loads(response.read())
        print(f"\n[*] Found: {workflow['name']} (ID: {workflow['id']})", file=sys.stderr)
        print(f"    Current status: {'ACTIVE' if workflow.get('active') else 'INACTIVE'}", file=sys.stderr)
except Exception as e:
    print(f"\n[-] Error fetching workflow: {e}", file=sys.stderr)
    sys.exit(1)

# Activate it via workflow update (not PATCH)
try:
    # Update workflow with active=true
    workflow['active'] = True
    
    req = urllib.request.Request(
        f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
        data=json.dumps(workflow).encode('utf-8'),
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        },
        method="PUT"
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read())
        
        print(f"\n[+] SUCCESS!", file=sys.stderr)
        print(f"    Workflow activated!", file=sys.stderr)
        print(f"    Name: {result['name']}", file=sys.stderr)
        print(f"    Active: {result.get('active', False)}", file=sys.stderr)
        print(f"\n[*] Workflow will run:", file=sys.stderr)
        print(f"    - Every 6 hours (Schedule Trigger)", file=sys.stderr)
        print(f"    - Fetches traces from Langfuse API", file=sys.stderr)
        print(f"    - Analyzes with GPT-4o Judge", file=sys.stderr)
        print(f"    - Writes FauxPas reports", file=sys.stderr)
        print(f"\n[*] View workflow:", file=sys.stderr)
        print(f"    http://localhost:5678/workflow/{WORKFLOW_ID}", file=sys.stderr)
        print(f"\n" + "=" * 60, file=sys.stderr)
        print(f"[+] Activation Complete!", file=sys.stderr)
        print(f"=" * 60, file=sys.stderr)
        
except Exception as e:
    print(f"\n[-] Activation failed: {e}", file=sys.stderr)
    sys.exit(1)
