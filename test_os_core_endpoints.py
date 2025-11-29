"""
Test OS Core MCP endpoints
"""
import subprocess
import time
import requests
import sys

print("Starting OS Core MCP...")
server_process = subprocess.Popen(
    [sys.executable, "server.py"],
    cwd=r"C:\Users\edri2\Desktop\AI\ai-os\services\os_core_mcp",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print("Waiting 3 seconds...")
time.sleep(3)

try:
    # Test root
    print("\n1. GET /")
    response = requests.get("http://localhost:8083/", timeout=5)
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Endpoints: {list(data.get('endpoints', {}).keys())}")
    
    # Test if /state/update exists
    print("\n2. Checking if /state/update exists in docs...")
    response = requests.get("http://localhost:8083/docs", timeout=5)
    print(f"   Status: {response.status_code}")
    
    # Try to call /state/update
    print("\n3. POST /state/update (actual call)")
    try:
        response = requests.post(
            "http://localhost:8083/state/update",
            json={
                "patch": {"test": "value"},
                "source": "test"
            },
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
finally:
    print("\nStopping server...")
    server_process.terminate()
    server_process.wait(timeout=5)
    print("Done.")
