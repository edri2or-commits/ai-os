#!/usr/bin/env python3
"""
PR Worker - Processes pending PR intents

Reads PR_INTENTS.jsonl, executes pending intents via mcp_github_client,
updates status, and logs events to EVENT_TIMELINE.jsonl.

Usage:
    python scripts/pr_worker.py
    
Prerequisites:
    - mcp_github_client running on http://localhost:8081
    - PR_INTENTS.jsonl exists with pending intents
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

try:
    import httpx
except ImportError:
    print("[ERROR] httpx not installed")
    print("Install with: pip install httpx")
    sys.exit(1)

# Paths
REPO_ROOT = Path(__file__).parent.parent
INTENTS_FILE = REPO_ROOT / "docs" / "system_state" / "outbox" / "PR_INTENTS.jsonl"
TIMELINE_FILE = REPO_ROOT / "docs" / "system_state" / "timeline" / "EVENT_TIMELINE.jsonl"

# Configuration
MCP_GITHUB_URL = "http://localhost:8081/github/open-pr"
TIMEOUT_SECONDS = 30.0


def load_intents(path: Path) -> List[Dict[str, Any]]:
    """Load all intents from JSONL file"""
    if not path.exists():
        print(f"[WARNING] Intents file not found: {path}")
        return []
    
    intents = []
    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                intent = json.loads(line)
                intents.append(intent)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Invalid JSON on line {line_num}: {e}")
                continue
    
    return intents


def save_intents(path: Path, intents: List[Dict[str, Any]]) -> None:
    """Save all intents back to JSONL file"""
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        for intent in intents:
            f.write(json.dumps(intent, ensure_ascii=False) + '\n')


def log_event(event_type: str, payload: Dict[str, Any]) -> None:
    """Log an event to EVENT_TIMELINE.jsonl"""
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "source": "pr_worker",
        "payload": payload
    }
    
    TIMELINE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(TIMELINE_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(event, ensure_ascii=False) + '\n')


def process_intent(intent: Dict[str, Any], intents: List[Dict[str, Any]]) -> bool:
    """
    Process a single intent
    
    Returns:
        True if successful, False if failed
    """
    intent_id = intent["intent_id"]
    pr_title = intent["pr_spec"]["title"]
    
    print(f"\n[INFO] Processing intent: {intent_id}")
    print(f"  Title: {pr_title}")
    
    # Mark as processing
    intent["status"] = "processing"
    save_intents(INTENTS_FILE, intents)
    log_event("PR_INTENT_PROCESSING", {
        "intent_id": intent_id,
        "pr_title": pr_title
    })
    
    # Call mcp_github_client
    try:
        print(f"  Calling mcp_github_client...")
        response = httpx.post(
            MCP_GITHUB_URL,
            json=intent["pr_spec"],
            timeout=TIMEOUT_SECONDS
        )
        response.raise_for_status()
        result = response.json()
        
        # Success path
        if result.get("ok"):
            intent["status"] = "completed"
            intent["result"] = {
                "pr_number": result["pr_number"],
                "pr_url": result["pr_url"],
                "branch_name": result["branch_name"]
            }
            intent["processed_at"] = datetime.utcnow().isoformat() + "Z"
            save_intents(INTENTS_FILE, intents)
            
            log_event("PR_CREATED", {
                "intent_id": intent_id,
                "pr_number": result["pr_number"],
                "pr_url": result["pr_url"],
                "branch_name": result["branch_name"],
                "pr_title": pr_title
            })
            
            print(f"  [SUCCESS] PR created: #{result['pr_number']}")
            print(f"  URL: {result['pr_url']}")
            return True
        
        # Failure path (ok=False)
        else:
            intent["status"] = "failed"
            intent["error"] = result.get("message", "Unknown error")
            intent["error_type"] = result.get("error_type", "unknown")
            intent["processed_at"] = datetime.utcnow().isoformat() + "Z"
            save_intents(INTENTS_FILE, intents)
            
            log_event("PR_CREATION_FAILED", {
                "intent_id": intent_id,
                "error": intent["error"],
                "error_type": intent["error_type"],
                "pr_title": pr_title
            })
            
            print(f"  [ERROR] Failed: {intent['error']}")
            return False
    
    except httpx.RequestError as e:
        # Connection error
        intent["status"] = "failed"
        intent["error"] = f"Connection error: {str(e)}"
        intent["error_type"] = "connection_error"
        intent["processed_at"] = datetime.utcnow().isoformat() + "Z"
        save_intents(INTENTS_FILE, intents)
        
        log_event("PR_CREATION_FAILED", {
            "intent_id": intent_id,
            "error": intent["error"],
            "error_type": "connection_error",
            "pr_title": pr_title
        })
        
        print(f"  [ERROR] Connection error: {e}")
        return False
    
    except Exception as e:
        # Unexpected error
        intent["status"] = "failed"
        intent["error"] = f"Unexpected error: {str(e)}"
        intent["error_type"] = "unexpected_error"
        intent["processed_at"] = datetime.utcnow().isoformat() + "Z"
        save_intents(INTENTS_FILE, intents)
        
        log_event("PR_CREATION_FAILED", {
            "intent_id": intent_id,
            "error": intent["error"],
            "error_type": "unexpected_error",
            "pr_title": pr_title
        })
        
        print(f"  [ERROR] Unexpected error: {e}")
        return False


def main():
    """Main entry point"""
    print("=" * 70)
    print("  AI-OS PR Worker - Sync Write Contract")
    print("=" * 70)
    
    # Load intents
    print(f"\n[1/3] Loading intents from: {INTENTS_FILE}")
    intents = load_intents(INTENTS_FILE)
    print(f"  Total intents: {len(intents)}")
    
    # Filter pending
    pending = [i for i in intents if i.get("status") == "pending"]
    print(f"  Pending intents: {len(pending)}")
    
    if not pending:
        print("\n[INFO] No pending intents to process")
        print("\nNext steps:")
        print("  - Create an intent: python scripts/create_pr_intent.py --help")
        return
    
    # Process each
    print(f"\n[2/3] Processing {len(pending)} pending intent(s)...")
    completed_count = 0
    failed_count = 0
    
    for intent in pending:
        success = process_intent(intent, intents)
        if success:
            completed_count += 1
        else:
            failed_count += 1
    
    # Summary
    print("\n" + "=" * 70)
    print(f"[3/3] Summary")
    print("=" * 70)
    print(f"  Completed: {completed_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Total processed: {completed_count + failed_count}")
    print()
    
    if failed_count > 0:
        print("[WARNING] Some intents failed. Check PR_INTENTS.jsonl for details.")
        print("To retry failed intents, manually change their status back to 'pending'.")
    
    if completed_count > 0:
        print("[SUCCESS] PRs created successfully!")
        print("Check GitHub: https://github.com/edri2or-commits/ai-os/pulls")


if __name__ == "__main__":
    main()
