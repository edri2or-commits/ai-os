#!/usr/bin/env python3
"""
Create PR Intent - Helper script to create PR intents

Creates a new intent in PR_INTENTS.jsonl for later processing by pr_worker.py.

Usage:
    python scripts/create_pr_intent.py \\
        --title "SLICE_EXAMPLE - Description" \\
        --description-file pr_description.txt \\
        --file docs/EXAMPLE.md:example_content.txt \\
        --operation create
        
Examples:
    # Single file
    python scripts/create_pr_intent.py \\
        --title "Add documentation" \\
        --description "Added new docs" \\
        --file docs/NEW.md:content.txt
    
    # Multiple files
    python scripts/create_pr_intent.py \\
        --title "Update configs" \\
        --description-file desc.txt \\
        --file config/a.json:a_content.json \\
        --file config/b.json:b_content.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


# Paths
REPO_ROOT = Path(__file__).parent.parent
INTENTS_FILE = REPO_ROOT / "docs" / "system_state" / "outbox" / "PR_INTENTS.jsonl"
TIMELINE_FILE = REPO_ROOT / "docs" / "system_state" / "timeline" / "EVENT_TIMELINE.jsonl"


def generate_intent_id() -> str:
    """Generate unique intent ID"""
    import random
    import string
    
    timestamp = int(datetime.utcnow().timestamp())
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    return f"pr-intent-{timestamp}-{random_part}"


def read_file_content(file_path: Path) -> str:
    """Read content from a file"""
    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)
    
    try:
        return file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"[ERROR] Failed to read {file_path}: {e}")
        sys.exit(1)


def parse_file_spec(file_spec: str) -> tuple[str, str]:
    """
    Parse file specification: PATH:CONTENT_FILE
    
    Returns:
        (repo_path, content_file_path)
    """
    if ':' not in file_spec:
        print(f"[ERROR] Invalid file spec: {file_spec}")
        print("Expected format: REPO_PATH:CONTENT_FILE")
        print("Example: docs/EXAMPLE.md:example_content.txt")
        sys.exit(1)
    
    repo_path, content_file = file_spec.split(':', 1)
    return repo_path.strip(), content_file.strip()


def create_intent(
    title: str,
    description: str,
    files: List[Dict[str, str]],
    base_branch: str = "main",
    use_ai: bool = False
) -> Dict[str, Any]:
    """Create an intent object"""
    intent_id = generate_intent_id()
    now = datetime.utcnow().isoformat() + "Z"
    
    return {
        "intent_id": intent_id,
        "created_at": now,
        "created_by": "create_pr_intent",
        "status": "pending",
        "pr_spec": {
            "title": title,
            "description": description,
            "files": files,
            "base_branch": base_branch,
            "use_ai_generation": use_ai
        },
        "trace_id": intent_id,
        "result": None,
        "error": None,
        "error_type": None,
        "processed_at": None
    }


def save_intent(intent: Dict[str, Any]) -> None:
    """Append intent to PR_INTENTS.jsonl"""
    INTENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(INTENTS_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(intent, ensure_ascii=False) + '\n')


def log_event(intent: Dict[str, Any]) -> None:
    """Log PR_INTENT_CREATED event"""
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": "PR_INTENT_CREATED",
        "source": "create_pr_intent",
        "payload": {
            "intent_id": intent["intent_id"],
            "pr_title": intent["pr_spec"]["title"],
            "created_by": intent["created_by"],
            "files_count": len(intent["pr_spec"]["files"])
        }
    }
    
    TIMELINE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(TIMELINE_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(event, ensure_ascii=False) + '\n')


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Create a PR intent for processing by pr_worker.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python scripts/create_pr_intent.py \\
      --title "Add documentation" \\
      --description "Added new documentation file" \\
      --file docs/NEW.md:content.txt
  
  # Multiple files with description file
  python scripts/create_pr_intent.py \\
      --title "Update configs" \\
      --description-file pr_desc.txt \\
      --file config/a.json:a.json \\
      --file config/b.json:b.json \\
      --operation update
        """
    )
    
    parser.add_argument(
        "--title",
        required=True,
        help="PR title"
    )
    
    parser.add_argument(
        "--description",
        help="PR description (inline)"
    )
    
    parser.add_argument(
        "--description-file",
        type=Path,
        help="Path to file containing PR description"
    )
    
    parser.add_argument(
        "--file",
        action="append",
        dest="files",
        help="File to include: REPO_PATH:CONTENT_FILE (can specify multiple times)"
    )
    
    parser.add_argument(
        "--operation",
        default="create",
        choices=["create", "update"],
        help="Operation type for files (default: create)"
    )
    
    parser.add_argument(
        "--base-branch",
        default="main",
        help="Base branch to merge into (default: main)"
    )
    
    parser.add_argument(
        "--use-ai",
        action="store_true",
        help="Use AI to refine PR description"
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.description and not args.description_file:
        print("[ERROR] Must provide either --description or --description-file")
        sys.exit(1)
    
    if args.description and args.description_file:
        print("[ERROR] Cannot provide both --description and --description-file")
        sys.exit(1)
    
    if not args.files:
        print("[ERROR] Must provide at least one --file")
        sys.exit(1)
    
    # Get description
    if args.description_file:
        description = read_file_content(args.description_file)
    else:
        description = args.description
    
    # Parse files
    print("\n[INFO] Creating PR intent...")
    print(f"  Title: {args.title}")
    print(f"  Files: {len(args.files)}")
    
    file_changes = []
    for file_spec in args.files:
        repo_path, content_file = parse_file_spec(file_spec)
        content_path = Path(content_file)
        
        # Read content
        content = read_file_content(content_path)
        
        file_changes.append({
            "path": repo_path,
            "content": content,
            "operation": args.operation
        })
        
        print(f"    - {repo_path} ({args.operation}, {len(content)} chars)")
    
    # Create intent
    intent = create_intent(
        title=args.title,
        description=description,
        files=file_changes,
        base_branch=args.base_branch,
        use_ai=args.use_ai
    )
    
    # Save intent
    save_intent(intent)
    print(f"\n[SUCCESS] Intent created: {intent['intent_id']}")
    
    # Log event
    log_event(intent)
    print(f"[INFO] Event logged: PR_INTENT_CREATED")
    
    # Next steps
    print("\n" + "=" * 70)
    print("Next steps:")
    print("=" * 70)
    print(f"1. Review intent: {INTENTS_FILE}")
    print("2. Run worker: python scripts/pr_worker.py")
    print()


if __name__ == "__main__":
    main()
