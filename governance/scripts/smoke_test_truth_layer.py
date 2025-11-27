#!/usr/bin/env python3
"""
Smoke Test: Governance Truth Layer V1

Tests that generate_snapshot.py works correctly and produces valid output.
"""

import json
import subprocess
import sys
from pathlib import Path


# Paths
SCRIPT_DIR = Path(__file__).parent
GOVERNANCE_ROOT = SCRIPT_DIR.parent
SNAPSHOTS_DIR = GOVERNANCE_ROOT / "snapshots"


def test_generate_snapshot():
    """Run generate_snapshot.py and verify output"""
    print("=" * 60)
    print("Smoke Test: Governance Truth Layer V1")
    print("=" * 60)
    print()
    
    # Step 1: Run generate_snapshot.py
    print("[1/4] Running generate_snapshot.py...")
    try:
        result = subprocess.run(
            [sys.executable, "generate_snapshot.py"],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"   [FAIL] Script failed with return code {result.returncode}")
            print(f"   STDERR: {result.stderr}")
            return False
        
        print("   [PASS] Script executed successfully")
    except subprocess.TimeoutExpired:
        print("   [FAIL] Script timed out after 10 seconds")
        return False
    except Exception as e:
        print(f"   [FAIL] Error running script: {e}")
        return False
    
    # Step 2: Check GOVERNANCE_LATEST.json exists
    print("\n[2/4] Checking GOVERNANCE_LATEST.json exists...")
    latest_path = SNAPSHOTS_DIR / "GOVERNANCE_LATEST.json"
    if not latest_path.exists():
        print(f"   [FAIL] File not found: {latest_path}")
        return False
    print(f"   [PASS] File exists: {latest_path}")
    
    # Step 3: Parse and validate JSON structure
    print("\n[3/4] Validating JSON structure...")
    try:
        with open(latest_path, 'r', encoding='utf-8') as f:
            snapshot = json.load(f)
    except json.JSONDecodeError as e:
        print(f"   [FAIL] Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"   [FAIL] Error reading file: {e}")
        return False
    
    # Check required keys
    required_keys = [
        "snapshot_id",
        "created_at",
        "source",
        "git",
        "system_state",
        "services_summary",
        "event_log_summary",
        "fitness_metrics"
    ]
    
    missing_keys = [key for key in required_keys if key not in snapshot]
    if missing_keys:
        print(f"   [FAIL] Missing required keys: {missing_keys}")
        return False
    
    print(f"   [PASS] All required keys present: {', '.join(required_keys)}")
    
    # Step 4: Validate fitness_metrics structure
    print("\n[4/4] Validating fitness_metrics...")
    fitness = snapshot.get("fitness_metrics", {})
    
    if "FITNESS_001_FRICTION" not in fitness:
        print("   [FAIL] Missing FITNESS_001_FRICTION")
        return False
    
    if "FITNESS_002_CCI" not in fitness:
        print("   [FAIL] Missing FITNESS_002_CCI")
        return False
    
    friction = fitness["FITNESS_001_FRICTION"]
    cci = fitness["FITNESS_002_CCI"]
    
    # Check that metrics have values (not None)
    friction_keys = list(friction.keys())
    cci_keys = list(cci.keys())
    
    if not friction_keys:
        print("   [FAIL] FITNESS_001_FRICTION is empty")
        return False
    
    if not cci_keys:
        print("   [FAIL] FITNESS_002_CCI is empty")
        return False
    
    print(f"   [PASS] FITNESS_001_FRICTION: {', '.join(friction_keys)}")
    print(f"   [PASS] FITNESS_002_CCI: {', '.join(cci_keys)}")
    
    # Success!
    print("\n" + "=" * 60)
    print("[SUCCESS] All smoke tests passed!")
    print(f"Snapshot ID: {snapshot['snapshot_id']}")
    print(f"Created: {snapshot['created_at']}")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_generate_snapshot()
    sys.exit(0 if success else 1)
