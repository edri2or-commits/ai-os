#!/usr/bin/env python3
"""
Smoke Test: MCP GitHub Client - PR Creation

Tests that the MCP GitHub Client service can:
1. Start and respond to health checks
2. Read files from the repository
3. Create Pull Requests automatically

This test creates a real test PR on a temporary branch.
"""

import sys
import json
import time
import requests
from datetime import datetime
from typing import Dict, Any


# Service configuration
SERVICE_URL = "http://localhost:8081"
HEALTH_ENDPOINT = f"{SERVICE_URL}/health"
READ_FILE_ENDPOINT = f"{SERVICE_URL}/github/read-file"
OPEN_PR_ENDPOINT = f"{SERVICE_URL}/github/open-pr"

# Test configuration
TEST_FILE_PATH = "README.md"
TEST_BRANCH_PREFIX = "test/pr-automator"


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_health_check() -> bool:
    """Test 1: Service Health Check"""
    print("\n[1/3] Testing service health...")
    
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                print("   [PASS] Service is running")
                print(f"   Service: {data.get('service', 'Unknown')}")
                print(f"   GitHub configured: {data.get('github_configured', False)}")
                print(f"   Repository: {data.get('repository', 'Unknown')}")
                return True
            else:
                print("   [FAIL] Service returned ok=false")
                return False
        else:
            print(f"   [FAIL] Service returned status code {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   [FAIL] Cannot connect to service")
        print("   Is the service running? Start it with: run_service.bat")
        return False
    except Exception as e:
        print(f"   [FAIL] Unexpected error: {e}")
        return False


def test_read_file() -> bool:
    """Test 2: Read File Capability"""
    print("\n[2/3] Testing file read capability...")
    
    try:
        payload = {
            "path": TEST_FILE_PATH,
            "ref": "main"
        }
        
        response = requests.post(
            READ_FILE_ENDPOINT,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                content = data.get("content", "")
                content_preview = content[:100] + "..." if len(content) > 100 else content
                
                print("   [PASS] Successfully read file")
                print(f"   Path: {data.get('path')}")
                print(f"   Size: {len(content)} characters")
                print(f"   Preview: {content_preview[:50]}...")
                return True
            else:
                print("   [FAIL] Service returned ok=false")
                print(f"   Error: {data.get('message')}")
                return False
        else:
            print(f"   [FAIL] Service returned status code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   [FAIL] Unexpected error: {e}")
        return False


def test_create_pr() -> Dict[str, Any]:
    """Test 3: Create Pull Request"""
    print("\n[3/3] Testing PR creation...")
    
    # Generate unique branch name
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    branch_name = f"{TEST_BRANCH_PREFIX}-{timestamp}"
    
    # Create test PR with minimal change
    test_file_path = "services/mcp_github_client/TESTING.md"
    test_content = f"""# MCP GitHub Client - Smoke Test

This file was created by the smoke test at {datetime.now().isoformat()}

## Purpose

This is a test PR created by `smoke_test_open_pr.py` to verify that the MCP GitHub Client
can successfully create Pull Requests.

## Test Details

- Branch: {branch_name}
- Timestamp: {timestamp}
- Test: SLICE_GITHUB_PR_AUTOMATOR_V1

This PR can be safely closed after verification.
"""
    
    try:
        payload = {
            "title": f"[TEST] MCP GitHub Client - Smoke Test {timestamp}",
            "description": f"""# Test PR - MCP GitHub Client

This is an automated test PR created by `smoke_test_open_pr.py`.

**Purpose:** Verify that MCP GitHub Client can create Pull Requests automatically.

**Branch:** `{branch_name}`  
**Test:** SLICE_GITHUB_PR_AUTOMATOR_V1  
**Created:** {datetime.now().isoformat()}

## What Changed

- Added `services/mcp_github_client/TESTING.md` (test file)

## Next Steps

1. Verify PR was created successfully
2. Check that all metadata is correct
3. Close this PR (no need to merge)

---

**Note:** This is a test PR and can be safely closed.
""",
            "files": [
                {
                    "path": test_file_path,
                    "content": test_content,
                    "operation": "create"
                }
            ],
            "base_branch": "main",
            "use_ai_generation": False
        }
        
        print(f"   Creating test PR on branch: {branch_name}")
        print(f"   Test file: {test_file_path}")
        
        response = requests.post(
            OPEN_PR_ENDPOINT,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                pr_url = data.get("pr_url", "Unknown")
                pr_number = data.get("pr_number", "Unknown")
                
                print("   [PASS] PR created successfully!")
                print(f"   PR #{pr_number}: {pr_url}")
                print(f"   Branch: {data.get('branch_name')}")
                
                return {
                    "success": True,
                    "pr_url": pr_url,
                    "pr_number": pr_number,
                    "branch_name": data.get("branch_name")
                }
            else:
                print("   [FAIL] Service returned ok=false")
                print(f"   Error type: {data.get('error_type')}")
                print(f"   Message: {data.get('message')}")
                return {"success": False}
        else:
            print(f"   [FAIL] Service returned status code {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('message', 'Unknown error')}")
            except:
                print(f"   Response: {response.text[:200]}")
            return {"success": False}
            
    except Exception as e:
        print(f"   [FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False}


def main():
    """Run all smoke tests"""
    print_section("MCP GitHub Client - Smoke Test Suite")
    print("\nThis test will:")
    print("  1. Check if the service is running")
    print("  2. Test file read capability")
    print("  3. Create a test Pull Request")
    print("\nPress Ctrl+C to cancel...")
    time.sleep(2)
    
    # Run tests
    results = {
        "health": False,
        "read": False,
        "pr": False
    }
    
    results["health"] = test_health_check()
    if not results["health"]:
        print("\n[ABORT] Service health check failed")
        print("Please start the service with: run_service.bat")
        sys.exit(1)
    
    results["read"] = test_read_file()
    if not results["read"]:
        print("\n[ABORT] File read test failed")
        print("Check your GitHub PAT configuration in .env")
        sys.exit(1)
    
    pr_result = test_create_pr()
    results["pr"] = pr_result.get("success", False)
    
    # Summary
    print_section("Test Summary")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ [SUCCESS] All tests passed!")
        print("\nPR Details:")
        print(f"  URL: {pr_result.get('pr_url')}")
        print(f"  Number: #{pr_result.get('pr_number')}")
        print(f"  Branch: {pr_result.get('branch_name')}")
        print("\nNext steps:")
        print("  1. Visit the PR URL to verify it was created correctly")
        print("  2. Close the test PR (no need to merge)")
        print("  3. MCP GitHub Client is ready for use!")
    else:
        print("\n❌ [FAILED] Some tests failed")
        print("\nFailed tests:")
        for test_name, passed in results.items():
            if not passed:
                print(f"  - {test_name}")
    
    print("=" * 60)
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
