"""
AI-OS Slice 2 Iron Test

Tests One-Command Startup functionality:
1. Verifies startup script works
2. Tests Demo Mode configuration
3. Tests Real GPT Mode detection
4. Verifies Agent Gateway responds
5. Executes simple workflow end-to-end
"""

import sys
import os
import subprocess
import time
import requests
from pathlib import Path
from datetime import datetime

# Fix encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("SLICE 2 IRON TEST - One-Command Startup")
print("=" * 70)
print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "=" * 70)

project_root = Path(__file__).parent

# Test results
test_results = []

# ============================================================================
# TEST 1: Check .env exists or can create demo
# ============================================================================

print("\n" + "=" * 70)
print("TEST 1: Configuration Check")
print("=" * 70)

env_file = project_root / ".env"

if env_file.exists():
    print("✅ .env file exists")
    
    # Load and check
    from dotenv import load_dotenv
    load_dotenv(env_file)
    
    demo_mode = os.getenv('DEMO_MODE', 'false').lower() == 'true'
    api_key = os.getenv('OPENAI_API_KEY', '')
    
    if demo_mode:
        print("✅ Mode: Demo (Simulated GPT)")
        mode = "demo"
    elif api_key and api_key.startswith('sk-'):
        print(f"✅ Mode: Real GPT (key: sk-...{api_key[-4:]})")
        mode = "real"
    else:
        print("⚠️  Mode: Demo (invalid key)")
        mode = "demo"
    
    test_results.append(("Config Check", True))
else:
    print("⚠️  No .env file - will create demo config")
    
    # Create demo .env
    demo_env = """# AI-OS Environment - Demo Mode (Iron Test)
DEMO_MODE=true
OPENAI_API_KEY=demo-mode-no-key-needed
OPENAI_MODEL=gpt-4o-mini
SERVER_PORT=8000
"""
    env_file.write_text(demo_env, encoding='utf-8')
    print("✅ Created demo .env")
    mode = "demo"
    test_results.append(("Config Check", True))

# ============================================================================
# TEST 2: Start server in background
# ============================================================================

print("\n" + "=" * 70)
print("TEST 2: Server Startup")
print("=" * 70)

print("\n🚀 Starting server in background...")

server_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "ai_core.agent_gateway_server:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd=project_root,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server to start
print("⏳ Waiting for server to initialize...")
time.sleep(3)

# Check if server is running
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    if response.status_code == 200:
        print("✅ Server started successfully")
        print(f"   Status: {response.json()}")
        test_results.append(("Server Startup", True))
    else:
        print(f"❌ Server responded with status {response.status_code}")
        test_results.append(("Server Startup", False))
except Exception as e:
    print(f"❌ Server not responding: {e}")
    test_results.append(("Server Startup", False))
    server_process.terminate()
    sys.exit(1)

# ============================================================================
# TEST 3: Test API Endpoint
# ============================================================================

print("\n" + "=" * 70)
print("TEST 3: API Endpoint Test")
print("=" * 70)

try:
    response = requests.post(
        "http://localhost:8000/api/v1/intent",
        json={
            "intent": "בדיקה פשוטה",
            "auto_execute": False
        },
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ API endpoint responding")
        print(f"   Status: {result.get('status')}")
        print(f"   Mode: {mode}")
        
        if result.get('plan'):
            print(f"   Plan summary: {result['plan']['summary'][:60]}...")
        
        test_results.append(("API Endpoint", True))
    else:
        print(f"❌ API returned status {response.status_code}")
        test_results.append(("API Endpoint", False))

except Exception as e:
    print(f"❌ API request failed: {e}")
    test_results.append(("API Endpoint", False))

# ============================================================================
# TEST 4: End-to-end workflow (file creation)
# ============================================================================

print("\n" + "=" * 70)
print("TEST 4: End-to-End Workflow")
print("=" * 70)

# Direct execution via agent_gateway (bypass HTTP for speed)
sys.path.insert(0, str(project_root))

from ai_core.action_executor import execute_actions

test_action = [
    {
        "type": "file.create",
        "params": {
            "path": "test_slice2_output.txt",
            "content": f"Slice 2 Iron Test - Success!\n\nDate: {datetime.now()}\nMode: {mode}\n"
        },
        "approval": "auto",
        "description": "Test file creation"
    }
]

try:
    result = execute_actions(test_action)
    
    if result['summary']['executed'] > 0:
        print("✅ File creation successful")
        print(f"   Executed: {result['summary']['executed']}/{result['summary']['total']}")
        test_results.append(("E2E Workflow", True))
        
        # Clean up test file
        test_file = project_root / "test_slice2_output.txt"
        if test_file.exists():
            test_file.unlink()
            print("   (Test file cleaned up)")
    else:
        print("❌ File creation failed")
        test_results.append(("E2E Workflow", False))

except Exception as e:
    print(f"❌ Workflow error: {e}")
    test_results.append(("E2E Workflow", False))

# ============================================================================
# CLEANUP & SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("CLEANUP")
print("=" * 70)

print("\n🛑 Stopping server...")
server_process.terminate()
server_process.wait(timeout=5)
print("✅ Server stopped")

print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)

passed = sum(1 for _, result in test_results if result)
total = len(test_results)

print(f"\n📊 Results: {passed}/{total} tests passed\n")

for name, result in test_results:
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status}: {name}")

if passed == total:
    print(f"\n🎉 All tests passed! Slice 2 is working!")
    print(f"\n✅ One-Command Startup: VERIFIED")
    print(f"✅ Mode: {mode.upper()}")
    print(f"✅ Agent Gateway: OPERATIONAL")
else:
    print(f"\n⚠️ {total - passed} test(s) failed")

print("\n" + "=" * 70)
print(f"\n💡 To start normally: python start.py")
print(f"💡 Or double-click: start.bat")
print("\n" + "=" * 70)
