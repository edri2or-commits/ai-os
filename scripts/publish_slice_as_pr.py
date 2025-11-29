#!/usr/bin/env python3
"""
Publish Slice as PR - Create PR Intent from completed slice

Reads slice metadata and creates a PR Intent using PR_CONTRACT_V1.

Usage:
    python scripts/publish_slice_as_pr.py --slice-name SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1
    python scripts/publish_slice_as_pr.py --slice-name SLICE_X_V1 --dry-run
    python scripts/publish_slice_as_pr.py --slice-name SLICE_X_V1 --title "Custom Title"
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


# Paths
REPO_ROOT = Path(__file__).parent.parent
SLICES_DIR = REPO_ROOT / "docs" / "slices"
TIMELINE_FILE = REPO_ROOT / "docs" / "system_state" / "timeline" / "EVENT_TIMELINE.jsonl"
INTENTS_FILE = REPO_ROOT / "docs" / "system_state" / "outbox" / "PR_INTENTS.jsonl"


def generate_intent_id(slice_name: str) -> str:
    """Generate intent ID for slice"""
    import random
    import string
    
    timestamp = int(datetime.utcnow().timestamp())
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    return f"slice-{slice_name}-{timestamp}-{random_part}"


def find_slice_complete_event(slice_name: str) -> Optional[Dict[str, Any]]:
    """
    Find SLICE_COMPLETE event for the given slice in timeline
    
    Returns:
        Event payload or None if not found
    """
    if not TIMELINE_FILE.exists():
        return None
    
    try:
        with open(TIMELINE_FILE, 'r', encoding='utf-8') as f:
            # Read in reverse to get most recent first
            lines = f.readlines()
            
            for line in reversed(lines):
                try:
                    event = json.loads(line)
                    if (event.get("event_type") == "SLICE_COMPLETE" and
                        event.get("payload", {}).get("slice_name") == slice_name):
                        return event.get("payload", {})
                except json.JSONDecodeError:
                    continue
        
        return None
    
    except Exception as e:
        print(f"[WARNING] Failed to read timeline: {e}", file=sys.stderr)
        return None


def parse_slice_doc(slice_doc_path: Path) -> Dict[str, Any]:
    """
    Parse slice doc to extract metadata
    
    Returns:
        {
            "summary": "Brief description",
            "files_created": ["path1", "path2"],
            "files_modified": ["path3"],
            "key_features": ["feature1", "feature2"]
        }
    """
    metadata = {
        "summary": "",
        "files_created": [],
        "files_modified": [],
        "key_features": []
    }
    
    if not slice_doc_path.exists():
        return metadata
    
    try:
        content = slice_doc_path.read_text(encoding='utf-8')
        
        # Extract summary from Goal section
        goal_match = re.search(r'## 🎯 Goal\s+(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if goal_match:
            goal_text = goal_match.group(1).strip()
            # Get first non-empty line after "Transform..." or similar
            lines = [l.strip() for l in goal_text.split('\n') if l.strip()]
            if lines:
                # Remove markdown formatting
                summary = lines[0].replace('**', '').replace('*', '')
                metadata["summary"] = summary
        
        # Extract files from Files Created/Modified section
        files_section = re.search(
            r'## 📁 Files Created/Modified.*?###\s+Created.*?\n(.*?)(?=###|##|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        
        if files_section:
            files_text = files_section.group(1)
            # Find file paths in numbered list
            file_matches = re.findall(r'\*\*`([^`]+)`\*\*', files_text)
            metadata["files_created"] = file_matches
        
        # Extract modified files
        modified_section = re.search(
            r'###\s+Modified.*?\n(.*?)(?=###|##|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        
        if modified_section:
            mod_text = modified_section.group(1)
            file_matches = re.findall(r'\*\*`([^`]+)`\*\*', mod_text)
            metadata["files_modified"] = file_matches
        
        return metadata
    
    except Exception as e:
        print(f"[WARNING] Failed to parse slice doc: {e}", file=sys.stderr)
        return metadata


def read_file_content(file_path: Path) -> str:
    """Read file content from disk"""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return file_path.read_text(encoding='utf-8')


def build_pr_description(
    slice_name: str,
    summary: str,
    files_created: List[str],
    files_modified: List[str],
    key_features: List[str],
    phase: str = "2.3"
) -> str:
    """Build PR description from slice metadata"""
    description_parts = []
    
    # Overview
    description_parts.append("## Overview\n")
    description_parts.append(f"{summary}\n")
    
    # Changes
    description_parts.append("\n## Changes\n")
    
    if files_created:
        description_parts.append("\n**Created:**\n")
        for file in files_created:
            description_parts.append(f"- `{file}`\n")
    
    if files_modified:
        description_parts.append("\n**Modified:**\n")
        for file in files_modified:
            description_parts.append(f"- `{file}`\n")
    
    # Key Features
    if key_features:
        description_parts.append("\n## Key Features\n")
        for feature in key_features:
            description_parts.append(f"- {feature}\n")
    
    # Documentation
    description_parts.append("\n## Documentation\n")
    description_parts.append(f"\nSee full details: `docs/slices/{slice_name}.md`\n")
    
    # Phase
    description_parts.append("\n## Phase\n")
    description_parts.append(f"\nPhase {phase} (INFRA_ONLY)\n")
    
    return ''.join(description_parts)


def build_files_array(
    files_created: List[str],
    files_modified: List[str]
) -> Tuple[List[Dict[str, str]], int]:
    """
    Build files array for PR spec
    
    Returns:
        (files_array, total_size_bytes)
    """
    files_array = []
    total_size = 0
    
    # Process created files
    for file_path in files_created:
        full_path = REPO_ROOT / file_path
        try:
            content = read_file_content(full_path)
            total_size += len(content.encode('utf-8'))
            
            files_array.append({
                "path": file_path,
                "content": content,
                "operation": "create"
            })
        except FileNotFoundError:
            print(f"[WARNING] File not found (skipping): {file_path}", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] Failed to read {file_path}: {e}", file=sys.stderr)
            raise
    
    # Process modified files
    for file_path in files_modified:
        full_path = REPO_ROOT / file_path
        try:
            content = read_file_content(full_path)
            total_size += len(content.encode('utf-8'))
            
            files_array.append({
                "path": file_path,
                "content": content,
                "operation": "update"
            })
        except FileNotFoundError:
            print(f"[WARNING] File not found (skipping): {file_path}", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] Failed to read {file_path}: {e}", file=sys.stderr)
            raise
    
    return files_array, total_size


def create_pr_intent(
    slice_name: str,
    title: str,
    description: str,
    files: List[Dict[str, str]],
    base_branch: str = "main"
) -> Dict[str, Any]:
    """Create PR Intent object"""
    intent_id = generate_intent_id(slice_name)
    now = datetime.utcnow().isoformat() + "Z"
    
    return {
        "intent_id": intent_id,
        "created_at": now,
        "created_by": "slice_to_pr_pipeline_v1",
        "status": "pending",
        "pr_spec": {
            "title": title,
            "description": description,
            "files": files,
            "base_branch": base_branch,
            "use_ai_generation": False
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


def log_event(slice_name: str, intent_id: str, files_count: int, pr_title: str) -> None:
    """Log SLICE_PR_INTENT_CREATED event"""
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": "SLICE_PR_INTENT_CREATED",
        "source": "slice_to_pr_pipeline_v1",
        "payload": {
            "slice_name": slice_name,
            "intent_id": intent_id,
            "files_count": files_count,
            "pr_title": pr_title
        }
    }
    
    TIMELINE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(TIMELINE_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(event, ensure_ascii=False) + '\n')


def format_size(bytes_size: int) -> str:
    """Format bytes as KB"""
    return f"{bytes_size / 1024:.1f} KB"


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Create PR Intent from completed slice",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python scripts/publish_slice_as_pr.py --slice-name SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1
  
  # Dry run (preview without creating)
  python scripts/publish_slice_as_pr.py --slice-name SLICE_X_V1 --dry-run
  
  # Custom title
  python scripts/publish_slice_as_pr.py --slice-name SLICE_X_V1 --title "Custom PR Title"
  
  # Different base branch
  python scripts/publish_slice_as_pr.py --slice-name SLICE_X_V1 --base-branch develop
        """
    )
    
    parser.add_argument(
        "--slice-name",
        required=True,
        help="Name of the slice (e.g., SLICE_CHAT_BOOTSTRAP_PROTOCOL_V1)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without modifying files"
    )
    
    parser.add_argument(
        "--title",
        help="Override PR title (default: auto-generated from slice)"
    )
    
    parser.add_argument(
        "--base-branch",
        default="main",
        help="Target branch for PR (default: main)"
    )
    
    args = parser.parse_args()
    
    slice_name = args.slice_name
    
    # Print header
    print("=" * 70)
    print("  Slice to PR Pipeline - Creating PR Intent")
    print("=" * 70)
    print()
    
    # Step 1: Validate
    print(f"[1/5] Validating slice: {slice_name}")
    
    slice_doc_path = SLICES_DIR / f"{slice_name}.md"
    if not slice_doc_path.exists():
        print(f"[ERROR] Slice doc not found: {slice_doc_path}")
        sys.exit(1)
    print(f"  ✓ Slice doc found: {slice_doc_path.relative_to(REPO_ROOT)}")
    
    # Find SLICE_COMPLETE event
    event_payload = find_slice_complete_event(slice_name)
    if not event_payload:
        print(f"[WARNING] SLICE_COMPLETE event not found in timeline")
        print(f"  Will use slice doc only")
    else:
        print(f"  ✓ SLICE_COMPLETE event found in timeline")
    
    # Step 2: Extract metadata
    print()
    print("[2/5] Extracting metadata")
    
    # Parse slice doc
    doc_metadata = parse_slice_doc(slice_doc_path)
    
    # Merge with event data (event takes precedence)
    if event_payload:
        files_created = event_payload.get("files_created", doc_metadata["files_created"])
        files_modified = event_payload.get("files_modified", doc_metadata.get("files_modified", []))
        summary = event_payload.get("description", doc_metadata["summary"])
        key_features = event_payload.get("key_features", doc_metadata.get("key_features", []))
    else:
        files_created = doc_metadata["files_created"]
        files_modified = doc_metadata.get("files_modified", [])
        summary = doc_metadata["summary"]
        key_features = doc_metadata.get("key_features", [])
    
    if not summary:
        summary = f"Implementation of {slice_name}"
    
    print(f"  Slice description: {summary}")
    print(f"  Files created: {len(files_created)}")
    print(f"  Files modified: {len(files_modified)}")
    
    # Validate files exist
    all_files = files_created + files_modified
    if not all_files:
        print(f"[ERROR] No files found for slice")
        print(f"  Check slice doc or SLICE_COMPLETE event")
        sys.exit(1)
    
    print(f"  ✓ Files exist on disk: {len(all_files)} files")
    
    # Step 3: Read file contents
    print()
    print("[3/5] Reading file contents")
    
    try:
        files_array, total_size = build_files_array(files_created, files_modified)
    except Exception as e:
        print(f"[ERROR] Failed to read files: {e}")
        sys.exit(1)
    
    for file_spec in files_array:
        file_size = len(file_spec["content"].encode('utf-8'))
        print(f"  Reading: {file_spec['path']} ({format_size(file_size)})")
    
    print(f"  Total content size: {format_size(total_size)}")
    
    # Step 4: Build PR spec
    print()
    print("[4/5] Building PR spec")
    
    # Generate title
    if args.title:
        pr_title = args.title
    else:
        # Auto-generate: "SLICE_NAME - Brief description"
        brief_desc = summary.split('.')[0]  # First sentence
        if len(brief_desc) > 80:
            brief_desc = brief_desc[:77] + "..."
        pr_title = f"{slice_name} - {brief_desc}"
    
    print(f"  Title: {pr_title}")
    
    # Generate description
    pr_description = build_pr_description(
        slice_name=slice_name,
        summary=summary,
        files_created=files_created,
        files_modified=files_modified,
        key_features=key_features
    )
    
    print(f"  Description: {len(pr_description.split(chr(10)))} lines")
    print(f"  Files: {len(files_array)} entries")
    
    # Create intent
    intent = create_pr_intent(
        slice_name=slice_name,
        title=pr_title,
        description=pr_description,
        files=files_array,
        base_branch=args.base_branch
    )
    
    # Step 5: Save (or dry-run)
    print()
    if args.dry_run:
        print("[5/5] DRY RUN - Not saving intent")
        print()
        print("Would create intent:")
        print(json.dumps(intent, indent=2, ensure_ascii=False)[:500] + "...")
    else:
        print("[5/5] Creating PR Intent")
        
        intent_id = intent["intent_id"]
        
        # Save intent
        save_intent(intent)
        print(f"  Intent ID: {intent_id}")
        print(f"  Saved to: {INTENTS_FILE.relative_to(REPO_ROOT)}")
        
        # Log event
        log_event(slice_name, intent_id, len(files_array), pr_title)
        print(f"  Logged event: SLICE_PR_INTENT_CREATED")
    
    # Final summary
    print()
    print("=" * 70)
    if args.dry_run:
        print("DRY RUN COMPLETE")
    else:
        print("✅ PR Intent Created Successfully")
    print("=" * 70)
    print()
    print(f"Intent ID: {intent['intent_id']}")
    print(f"Slice: {slice_name}")
    print(f"Files: {len(files_array)}")
    print(f"PR Title: {pr_title}")
    
    if not args.dry_run:
        print()
        print("Next step: Run pr_worker.py to create the PR on GitHub")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
