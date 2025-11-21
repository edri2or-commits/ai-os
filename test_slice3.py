"""
Slice 3 Iron Test - System Health Dashboard

Tests:
1. /system/health endpoint
2. /system/dashboard HTML
3. check_health.py script
4. All components report correctly
"""

import sys
import time
import subprocess
import requests
from pathlib import Path
from datetime import datetime

# Fix encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("SLICE 3 IRON TEST - System Health Dashboard")
print("=" * 70)
print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "=" * 70)

project_root = Path(__file__).parent
test_results = []

# ============================================================================
# TEST 1: check_health.py script
# ============================================================================

print("\n" + "=" * 70)
print("TEST 1: check_health.py Script")
print("=" * 70)

try:
    result = subprocess.run(
        [sys.executable, "check_health.py"],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0:
        print("✅ check_health.py executed successfully")
        print(f"   Exit code: {result.returncode}")
        
        # Check for key phrases
        if "OVERALL STATUS: HEALTHY" in result.stdout:
            print("✅ Overall status: HEALTHY")
            test_results.append(("check_health.py", True))
        else:
            print("⚠️  Status not healthy")
            print(result.stdout[-200:])
            test_results.append(("check_health.py", False))
    else:
        print(f"❌ check_health.py failed with exit code {result.returncode}")
        print(result.stdout[-200:])
        test_results.append(("check_health.py", False))

except Exception as e:
    print(f"❌ Failed to run check_health.py: {e}")
    test_results.append(("check_health.py", False))

# ============================================================================
# TEST 2: Start server and test endpoints
# ============================================================================

print("\n" + "=" * 70)
print("TEST 2: Server Health Endpoints")
print("=" * 70)

print("\n🚀 Starting server in background...")

server_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "ai_core.agent_gateway_server:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd=project_root,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print("⏳ Waiting for server to initialize...")
time.sleep(3)

# Test /system/health endpoint
print("\n📋 Testing /system/health endpoint...")

try:
    response = requests.get("http://localhost:8000/system/health", timeout=10)
    
    if response.status_code == 200:
        health_data = response.json()
        
        print("✅ /system/health responding")
        print(f"   Overall status: {health_data.get('overall_status')}")
        print(f"   Components: {len(health_data.get('components', {}))}")
        
        # Check key components
        components = health_data.get('components', {})
        
        required_components = [
            'api_key', 'gpt_planner', 'intent_router',
            'action_executor', 'git', 'filesystem', 'agent_gateway'
        ]
        
        missing = [c for c in required_components if c not in components]
        
        if not missing:
            print(f"✅ All {len(required_components)} required components present")
            test_results.append(("/system/health", True))
        else:
            print(f"❌ Missing components: {missing}")
            test_results.append(("/system/health", False))
    else:
        print(f"❌ /system/health returned {response.status_code}")
        test_results.append(("/system/health", False))

except Exception as e:
    print(f"❌ Failed to call /system/health: {e}")
    test_results.append(("/system/health", False))

# Test /system/dashboard endpoint
print("\n📋 Testing /system/dashboard endpoint...")

try:
    response = requests.get("http://localhost:8000/system/dashboard", timeout=10)
    
    if response.status_code == 200:
        html_content = response.text
        
        # Check for key HTML elements
        if "AI-OS System Health Dashboard" in html_content:
            print("✅ /system/dashboard returning HTML")
            print("   ✅ Title present")
        
        if "loadHealth()" in html_content:
            print("   ✅ JavaScript present")
        
        if "component-card" in html_content:
            print("   ✅ Component cards styled")
        
        test_results.append(("/system/dashboard", True))
    else:
        print(f"❌ /system/dashboard returned {response.status_code}")
        test_results.append(("/system/dashboard", False))

except Exception as e:
    print(f"❌ Failed to call /system/dashboard: {e}")
    test_results.append(("/system/dashboard", False))

# ============================================================================
# TEST 3: Component Status Verification
# ============================================================================

print("\n" + "=" * 70)
print("TEST 3: Component Status Verification")
print("=" * 70)

try:
    response = requests.get("http://localhost:8000/system/health", timeout=10)
    health_data = response.json()
    components = health_data.get('components', {})
    
    all_healthy = True
    
    for name, component in components.items():
        status = component.get('status')
        message = component.get('message', '')[:50]
        
        icon = {"healthy": "✅", "warning": "⚠️", "error": "❌"}.get(status, "❓")
        print(f"{icon} {name}: {status} - {message}...")
        
        if status == "error":
            all_healthy = False
    
    if all_healthy:
        print("\n✅ All components healthy or warning")
        test_results.append(("Component Status", True))
    else:
        print("\n❌ Some components have errors")
        test_results.append(("Component Status", False))

except Exception as e:
    print(f"❌ Failed to verify components: {e}")
    test_results.append(("Component Status", False))

# ============================================================================
# CLEANUP
# ============================================================================

print("\n" + "=" * 70)
print("CLEANUP")
print("=" * 70)

print("\n🛑 Stopping server...")
server_process.terminate()
server_process.wait(timeout=5)
print("✅ Server stopped")

# ============================================================================
# SUMMARY
# ============================================================================

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
    print(f"\n🎉 All tests passed! Slice 3 is working!")
    print(f"\n✅ Health Dashboard: OPERATIONAL")
    print(f"✅ System Monitoring: ENABLED")
else:
    print(f"\n⚠️ {total - passed} test(s) failed")

print("\n" + "=" * 70)
print(f"\n💡 To view dashboard: http://localhost:8000/system/dashboard")
print(f"💡 To check health: python check_health.py")
print("\n" + "=" * 70)
