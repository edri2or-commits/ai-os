# Test SSOT Update Service

Simple test to verify /ssot/update endpoint works

import requests
import json

# Test configuration
API_URL = "http://localhost:8000/ssot/update"

# Test content - small update to SYSTEM_SNAPSHOT
test_content = """# System Snapshot – Test Update

This is a test update from SSOT Update Service.
Testing automated git commit + push functionality.

Timestamp: 2025-11-23 Test Run
"""

# Prepare request
payload = {
    "target": "system_snapshot",
    "mode": "replace_full",
    "content": test_content,
    "commit_message": "test: SSOT update service verification"
}

print("=" * 60)
print("Testing SSOT Update Service")
print("=" * 60)
print(f"\nEndpoint: {API_URL}")
print(f"Target: {payload['target']}")
print(f"Content length: {len(test_content)} chars")
print("\nSending request...")

try:
    response = requests.post(API_URL, json=payload)
    
    print(f"\nStatus Code: {response.status_code}")
    print("\nResponse:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        result = response.json()
        if result.get("ok"):
            print("\n✅ SUCCESS!")
            print(f"Commit SHA: {result['commit_sha']}")
            print(f"Commit Message: {result['commit_message']}")
        else:
            print("\n❌ FAILED!")
            print(f"Error: {result.get('error')}")
    else:
        print("\n❌ HTTP ERROR!")
        
except requests.exceptions.ConnectionError:
    print("\n❌ Cannot connect to server!")
    print("Make sure the server is running:")
    print("  python start.py")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "=" * 60)
