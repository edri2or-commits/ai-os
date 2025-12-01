#!/usr/bin/env python3
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Set up paths
REPO_ROOT = Path(__file__).parent
CHANGE_REQUESTS_DIR = REPO_ROOT / "docs" / "system_state" / "change_requests"

print(f"REPO_ROOT: {REPO_ROOT}")
print(f"CHANGE_REQUESTS_DIR: {CHANGE_REQUESTS_DIR}")
print(f"DIR exists: {CHANGE_REQUESTS_DIR.exists()}")

# List CRs
crs = list(CHANGE_REQUESTS_DIR.glob("*.cr.yaml"))
print(f"Found {len(crs)} CR files")

for cr_file in crs:
    print(f"  - {cr_file.name}")
    
    # Try to read it
    import yaml
    with open(cr_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    print(f"    Status: {data.get('status')}")
    print(f"    Drift: {data.get('drift_type')}")
