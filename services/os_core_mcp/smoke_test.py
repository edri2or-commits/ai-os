"""
Smoke test for OS Core MCP
"""
import subprocess
import time
import requests
import sys
import json

def run_smoke_test():
    print("=== OS Core MCP Smoke Test ===\n")
    
    # Start server
    print("1. Starting server...")
    server_process = subprocess.Popen(
        [sys.executable, "server.py"],
        cwd=r"C:\Users\edri2\Desktop\AI\ai-os\services\os_core_mcp",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    print("   Waiting 3 seconds for server to start...")
    time.sleep(3)
    
    base_url = "http://localhost:8083"
    results = []
    
    try:
        # Test 1: GET /health
        print("\n2. Testing GET /health")
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
            results.append(("GET /health", response.status_code, "OK"))
        except Exception as e:
            print(f"   ERROR: {e}")
            results.append(("GET /health", "ERROR", str(e)))
        
        # Test 2: GET /state
        print("\n3. Testing GET /state")
        try:
            response = requests.get(f"{base_url}/state", timeout=5)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   System Phase: {data.get('system', {}).get('phase', 'N/A')}")
                print(f"   Mode: {data.get('system', {}).get('mode', 'N/A')}")
            else:
                print(f"   Response: {response.text[:200]}")
            results.append(("GET /state", response.status_code, "OK"))
        except Exception as e:
            print(f"   ERROR: {e}")
            results.append(("GET /state", "ERROR", str(e)))
        
        # Test 3: GET /services
        print("\n4. Testing GET /services")
        try:
            response = requests.get(f"{base_url}/services", timeout=5)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Services count: {len(data.get('services', []))}")
            else:
                print(f"   Response: {response.text[:200]}")
            results.append(("GET /services", response.status_code, "OK"))
        except Exception as e:
            print(f"   ERROR: {e}")
            results.append(("GET /services", "ERROR", str(e)))
        
        # Test 4: POST /events
        print("\n5. Testing POST /events")
        try:
            payload = {
                "event_type": "test_os_core_mcp",
                "payload": {"note": "smoke test"},
                "source": "os-core-mcp-smoketest"
            }
            response = requests.post(f"{base_url}/events", json=payload, timeout=5)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Event written: {data.get('event', {}).get('timestamp', 'N/A')}")
            else:
                print(f"   Response: {response.text[:200]}")
            results.append(("POST /events", response.status_code, "OK"))
        except Exception as e:
            print(f"   ERROR: {e}")
            results.append(("POST /events", "ERROR", str(e)))
        
    finally:
        # Stop server
        print("\n6. Stopping server...")
        server_process.terminate()
        server_process.wait(timeout=5)
        print("   Server stopped.")
    
    # Summary
    print("\n=== Test Summary ===")
    for endpoint, status, result in results:
        print(f"{endpoint}: {status} - {result}")
    
    print("\n=== Smoke Test Complete ===")

if __name__ == "__main__":
    run_smoke_test()
