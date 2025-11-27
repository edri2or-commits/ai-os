#!/usr/bin/env python3
"""
Governance Script: Generate Snapshot (Truth Layer V1)

Purpose:
  Generate a comprehensive governance snapshot of AI-OS state.
  
  Combines:
  - System State (SYSTEM_STATE_COMPACT.json)
  - Services Status (SERVICES_STATUS.json)
  - Recent Events (EVENT_TIMELINE.jsonl)
  - Git metadata (branch, commit)
  - Fitness Metrics (FITNESS_001_FRICTION, FITNESS_002_CCI)
  
  Outputs to: governance/snapshots/

Status: IMPLEMENTED - Bootstrap V1
"""

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List


# Paths relative to this script
SCRIPT_DIR = Path(__file__).parent
GOVERNANCE_ROOT = SCRIPT_DIR.parent
REPO_ROOT = GOVERNANCE_ROOT.parent
SNAPSHOTS_DIR = GOVERNANCE_ROOT / "snapshots"
DOCS_ROOT = REPO_ROOT / "docs"
STATE_ROOT = DOCS_ROOT / "system_state"


def read_json_file(file_path: Path) -> Dict[str, Any]:
    """Read and parse a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"WARNING: File not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"WARNING: Invalid JSON in {file_path}: {e}")
        return {}


def read_jsonl_tail(file_path: Path, n: int = 20) -> List[Dict[str, Any]]:
    """Read last N lines from JSONL file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Take last N lines
        tail_lines = lines[-n:] if len(lines) > n else lines
        
        # Parse each line as JSON
        events = []
        for line in tail_lines:
            line = line.strip()
            if not line:
                continue
            try:
                # Skip schema/comment lines
                obj = json.loads(line)
                if not obj.get("_schema"):  # Skip schema definition line
                    events.append(obj)
            except json.JSONDecodeError:
                continue
        
        return events
    except FileNotFoundError:
        print(f"WARNING: File not found: {file_path}")
        return []


def get_git_metadata() -> Dict[str, str]:
    """Get current git branch and commit"""
    try:
        # Get branch name
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=REPO_ROOT,
            text=True
        ).strip()
        
        # Get short commit hash
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            text=True
        ).strip()
        
        return {
            "branch": branch,
            "last_commit": commit
        }
    except subprocess.CalledProcessError as e:
        print(f"WARNING: Failed to get git metadata: {e}")
        return {
            "branch": "unknown",
            "last_commit": "unknown"
        }


def calculate_fitness_001_friction(
    system_state: Dict[str, Any],
    services_status: Dict[str, Any],
    recent_events: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Calculate FITNESS_001_FRICTION metrics
    
    Measures operational friction:
    - Open gaps count
    - Time since last daily context sync
    - Failed events (if any)
    """
    friction = {}
    
    # Count open gaps
    open_gaps = system_state.get("open_gaps", [])
    open_gap_count = len([g for g in open_gaps if g.get("status") != "closed_resolved"])
    friction["open_gaps_count"] = open_gap_count
    
    # Time since last daily context sync
    last_sync = system_state.get("last_daily_context_sync_utc")
    if last_sync:
        try:
            last_sync_dt = datetime.fromisoformat(last_sync.replace("Z", "+00:00"))
            now_dt = datetime.now(timezone.utc)
            delta = now_dt - last_sync_dt
            friction["time_since_last_daily_context_sync_minutes"] = int(delta.total_seconds() / 60)
        except (ValueError, AttributeError):
            friction["time_since_last_daily_context_sync_minutes"] = None
    else:
        friction["time_since_last_daily_context_sync_minutes"] = None
    
    # Count error/incident events in recent history
    error_events = [
        e for e in recent_events 
        if "error" in e.get("event_type", "").lower() or "incident" in e.get("event_type", "").lower()
    ]
    friction["recent_error_events_count"] = len(error_events)
    
    return friction


def calculate_fitness_002_cci(
    system_state: Dict[str, Any],
    services_status: Dict[str, Any],
    recent_events: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Calculate FITNESS_002_CCI (Cognitive Capacity Index) metrics
    
    Measures system cognitive capacity:
    - Active services count
    - Unique event types (diversity of activity)
    - Recent work blocks count
    """
    cci = {}
    
    # Count active services
    services = services_status.get("services", [])
    active_services = [s for s in services if s.get("status") == "up"]
    cci["active_services_count"] = len(active_services)
    cci["total_services_count"] = len(services)
    
    # Count unique event types in recent history
    unique_event_types = set(e.get("event_type", "") for e in recent_events if e.get("event_type"))
    cci["recent_event_types_count"] = len(unique_event_types)
    
    # Count recent work blocks
    recent_work = system_state.get("recent_work", [])
    cci["recent_work_blocks_count"] = len(recent_work)
    
    # Count pending decisions
    pending_decisions = system_state.get("pending_decisions", [])
    cci["pending_decisions_count"] = len(pending_decisions)
    
    return cci


def generate_snapshot() -> Dict[str, Any]:
    """
    Generate comprehensive governance snapshot
    
    Returns:
        dict: Complete snapshot with metadata, state, and metrics
    """
    # Create snapshots directory if it doesn't exist
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp
    now_utc = datetime.now(timezone.utc)
    timestamp = now_utc.isoformat().replace("+00:00", "Z")
    snapshot_id = f"GOVERNANCE_SNAPSHOT_{timestamp}"
    
    print(f"Generating snapshot: {snapshot_id}")
    
    # Read source files
    print("Reading source files...")
    system_state = read_json_file(STATE_ROOT / "SYSTEM_STATE_COMPACT.json")
    services_status = read_json_file(STATE_ROOT / "registries" / "SERVICES_STATUS.json")
    recent_events = read_jsonl_tail(STATE_ROOT / "timeline" / "EVENT_TIMELINE.jsonl", n=20)
    
    # Get git metadata
    print("Collecting git metadata...")
    git_metadata = get_git_metadata()
    
    # Calculate fitness metrics
    print("Calculating fitness metrics...")
    fitness_001 = calculate_fitness_001_friction(system_state, services_status, recent_events)
    fitness_002 = calculate_fitness_002_cci(system_state, services_status, recent_events)
    
    # Build services summary
    services_summary = services_status.get("summary", {})
    
    # Build event log summary
    event_log_summary = {}
    if recent_events:
        event_log_summary["last_event_timestamp"] = recent_events[-1].get("timestamp", "unknown")
        event_log_summary["last_event_type"] = recent_events[-1].get("event_type", "unknown")
        event_log_summary["recent_events_sampled"] = len(recent_events)
    
    # Build snapshot
    snapshot = {
        "snapshot_id": snapshot_id,
        "created_at": timestamp,
        "source": "governance/scripts/generate_snapshot.py",
        "git": git_metadata,
        "system_state": {
            "phase": system_state.get("system", {}).get("phase", "unknown"),
            "mode": system_state.get("system", {}).get("mode", "unknown"),
            "automations_enabled": system_state.get("system", {}).get("automations_enabled", False),
            "last_daily_context_sync_utc": system_state.get("last_daily_context_sync_utc")
        },
        "services_summary": services_summary,
        "event_log_summary": event_log_summary,
        "fitness_metrics": {
            "FITNESS_001_FRICTION": fitness_001,
            "FITNESS_002_CCI": fitness_002
        }
    }
    
    # Save snapshot with timestamp
    snapshot_filename = f"SNAPSHOT_{now_utc.strftime('%Y%m%d_%H%M%S')}.json"
    snapshot_path = SNAPSHOTS_DIR / snapshot_filename
    
    print(f"Writing snapshot to: {snapshot_path}")
    with open(snapshot_path, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    
    # Update GOVERNANCE_LATEST.json (symlink-like behavior)
    latest_path = SNAPSHOTS_DIR / "GOVERNANCE_LATEST.json"
    print(f"Updating latest snapshot: {latest_path}")
    with open(latest_path, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    
    print(f"\n[SUCCESS] Snapshot generated successfully!")
    print(f"   ID: {snapshot_id}")
    print(f"   Path: {snapshot_path}")
    print(f"   Latest: {latest_path}")
    
    return {
        "status": "success",
        "snapshot_id": snapshot_id,
        "snapshot_path": str(snapshot_path),
        "latest_path": str(latest_path),
        "snapshot": snapshot
    }


if __name__ == "__main__":
    print("=" * 60)
    print("AI-OS Governance Layer - Snapshot Generation V1")
    print("=" * 60)
    print()
    
    try:
        result = generate_snapshot()
        print()
        print("=" * 60)
        print("Summary:")
        print(f"  Status: {result['status']}")
        print(f"  Snapshot ID: {result['snapshot_id']}")
        print(f"  File: {result['snapshot_path']}")
        print("=" * 60)
    except Exception as e:
        print(f"\n[ERROR] Failed to generate snapshot")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
