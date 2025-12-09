#!/usr/bin/env python3
"""
System Inventory - Comprehensive state checker
Queries n8n, Docker, Git to build complete system picture
Saves to memory-bank/system-inventory.json
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Paths
ROOT = Path(__file__).parent.parent
INVENTORY_FILE = ROOT / "memory-bank" / "system-inventory.json"
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io"

def run_command(cmd):
    """Run shell command, return output or None"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

def check_n8n_workflows():
    """Query n8n API for workflows"""
    try:
        import urllib.request
        req = urllib.request.Request(
            "http://localhost:5678/api/v1/workflows",
            headers={"X-N8N-API-KEY": N8N_API_KEY}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            workflows = []
            for wf in data.get("data", []):
                workflows.append({
                    "id": wf.get("id"),
                    "name": wf.get("name"),
                    "active": wf.get("active", False),
                    "nodes": len(wf.get("nodes", [])),
                    "updatedAt": wf.get("updatedAt")
                })
            return workflows
    except Exception as e:
        return {"error": str(e)}

def check_n8n_credentials():
    """Query n8n API for credential types (not secrets!)"""
    try:
        import urllib.request
        req = urllib.request.Request(
            "http://localhost:5678/api/v1/credentials",
            headers={"X-N8N-API-KEY": N8N_API_KEY}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            creds = []
            for cred in data.get("data", []):
                creds.append({
                    "id": cred.get("id"),
                    "name": cred.get("name"),
                    "type": cred.get("type")
                })
            return creds
    except Exception as e:
        return {"error": str(e)}

def check_docker_containers():
    """Get Docker container status"""
    output = run_command('docker ps -a --format "{{.Names}}|{{.Status}}|{{.Ports}}"')
    if not output:
        return []
    
    containers = []
    for line in output.split("\n"):
        if "|" in line:
            parts = line.split("|")
            containers.append({
                "name": parts[0],
                "status": parts[1] if len(parts) > 1 else "unknown",
                "ports": parts[2] if len(parts) > 2 else ""
            })
    return containers

def check_git_status():
    """Get Git repository status"""
    branch = run_command("git rev-parse --abbrev-ref HEAD")
    commit = run_command("git rev-parse --short HEAD")
    dirty = run_command("git status --porcelain")
    
    return {
        "branch": branch or "unknown",
        "commit": commit or "unknown",
        "clean": not bool(dirty),
        "uncommitted_changes": len(dirty.split("\n")) if dirty else 0
    }

def check_key_files():
    """Check existence of key system files"""
    files_to_check = [
        "truth-layer/timeline/EVENT_TIMELINE.jsonl",
        "prompts/judge_agent_prompt.md",
        "n8n_workflows/judge_agent.json",
        "tools/observer.py",
        "tools/watchdog.py",
        ".env"
    ]
    
    files = {}
    for f in files_to_check:
        path = ROOT / f
        files[f] = {
            "exists": path.exists(),
            "size": path.stat().st_size if path.exists() else 0
        }
    return files

def main():
    print("🔍 System Inventory - Starting...", file=sys.stderr)
    
    inventory = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "n8n": {
            "workflows": check_n8n_workflows(),
            "credentials": check_n8n_credentials()
        },
        "docker": {
            "containers": check_docker_containers()
        },
        "git": check_git_status(),
        "files": check_key_files()
    }
    
    # Save inventory
    INVENTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    INVENTORY_FILE.write_text(json.dumps(inventory, indent=2, ensure_ascii=False))
    
    print(f"✅ Inventory saved: {INVENTORY_FILE}", file=sys.stderr)
    
    # Print summary
    print("\n📊 SUMMARY:", file=sys.stderr)
    
    if isinstance(inventory["n8n"]["workflows"], list):
        active = sum(1 for w in inventory["n8n"]["workflows"] if w.get("active"))
        total = len(inventory["n8n"]["workflows"])
        print(f"   n8n Workflows: {active}/{total} active", file=sys.stderr)
    else:
        print(f"   n8n Workflows: ERROR", file=sys.stderr)
    
    if isinstance(inventory["n8n"]["credentials"], list):
        print(f"   n8n Credentials: {len(inventory['n8n']['credentials'])} configured", file=sys.stderr)
    else:
        print(f"   n8n Credentials: ERROR", file=sys.stderr)
    
    running = sum(1 for c in inventory["docker"]["containers"] if "Up" in c.get("status", ""))
    total_containers = len(inventory["docker"]["containers"])
    print(f"   Docker: {running}/{total_containers} running", file=sys.stderr)
    
    print(f"   Git: {inventory['git']['commit']} ({'clean' if inventory['git']['clean'] else 'dirty'})", file=sys.stderr)
    
    print("\n✅ Done!\n", file=sys.stderr)

if __name__ == "__main__":
    main()
