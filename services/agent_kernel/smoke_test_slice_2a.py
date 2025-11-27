"""
Slice 2A Smoke Test - OS Core MCP + Agent Kernel
"""
import subprocess
import time
import requests
import sys
import json
from pathlib import Path

def run_slice_2a_smoke_test():
    print("=" * 70)
    print("SLICE 2A SMOKE TEST - OS Core MCP + Agent Kernel + LangGraph")
    print("=" * 70)
    
    base_dir = Path(r"C:\Users\edri2\Desktop\AI\ai-os")
    
    # Start OS Core MCP
    print("\n1. Starting OS Core MCP (port 8083)...")
    os_core_process = subprocess.Popen(
        [sys.executable, "server.py"],
        cwd=base_dir / "services" / "os_core_mcp",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Start Agent Kernel
    print("2. Starting Agent Kernel (port 8084)...")
    kernel_process = subprocess.Popen(
        [sys.executable, "kernel_server.py"],
        cwd=base_dir / "services" / "agent_kernel",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print("   Waiting 5 seconds for servers to start...")
    time.sleep(5)
    
    results = []
    
    try:
        # Test 1: OS Core MCP health
        print("\n3. Testing OS Core MCP - GET /health")
        try:
            response = requests.get("http://localhost:8083/health", timeout=5)
            print(f"   Status: {response.status_code}")
            results.append(("OS Core /health", response.status_code, "OK"))
        except Exception as e:
            print(f"   ERROR: {e}")
            results.append(("OS Core /health", "ERROR", str(e)))
        
        # Test 2: Agent Kernel health
        print("\n4. Testing Agent Kernel - GET /health")
        try:
            response = requests.get("http://localhost:8084/health", timeout=5)
            print(f"   Status: {response.status_code}")
            results.append(("Kernel /health", response.status_code, "OK"))
        except Exception as e:
            print(f"   ERROR: {e}")
            results.append(("Kernel /health", "ERROR", str(e)))
        
        # Test 3: Daily Context Sync - THE MAIN TEST
        print("\n5. Testing POST /daily-context-sync/run")
        try:
            response = requests.post(
                "http://localhost:8084/daily-context-sync/run",
                timeout=30
            )
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Result: {json.dumps(data, indent=2)}")
                
                if data.get("status") == "ok":
                    sync_time = data.get("last_sync_time")
                    print(f"   ✅ Sync completed: {sync_time}")
                    results.append(("Daily Context Sync", 200, f"OK - {sync_time}"))
                else:
                    print(f"   ❌ Sync failed: {data.get('error')}")
                    results.append(("Daily Context Sync", 200, f"FAILED - {data.get('error')}"))
            else:
                print(f"   Response: {response.text[:200]}")
                results.append(("Daily Context Sync", response.status_code, "ERROR"))
                
        except Exception as e:
            print(f"   ERROR: {e}")
            results.append(("Daily Context Sync", "ERROR", str(e)))
        
        # Test 4: Verify SYSTEM_STATE_COMPACT.json updated
        print("\n6. Verifying SYSTEM_STATE_COMPACT.json updated")
        try:
            state_file = base_dir / "docs" / "system_state" / "SYSTEM_STATE_COMPACT.json"
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            sync_time = state.get("last_daily_context_sync_utc")
            if sync_time:
                print(f"   ✅ State updated: last_daily_context_sync_utc = {sync_time}")
                results.append(("State Updated", "OK", sync_time))
            else:
                print(f"   ❌ State NOT updated: field not found")
                results.append(("State Updated", "MISSING", "Field not in state"))
                
        except Exception as e:
            print(f"   ERROR: {e}")
            results.append(("State Updated", "ERROR", str(e)))
        
        # Test 5: Verify EVENT_TIMELINE.jsonl has new events
        print("\n7. Verifying EVENT_TIMELINE.jsonl has new events")
        try:
            timeline_file = base_dir / "docs" / "system_state" / "timeline" / "EVENT_TIMELINE.jsonl"
            with open(timeline_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Check last 3 events for DAILY_CONTEXT_SYNC
            recent_events = [json.loads(line) for line in lines[-3:]]
            
            started_found = any(
                e.get("event_type") == "DAILY_CONTEXT_SYNC_STARTED" 
                for e in recent_events
            )
            completed_found = any(
                e.get("event_type") == "DAILY_CONTEXT_SYNC_COMPLETED"
                for e in recent_events
            )
            
            if started_found and completed_found:
                print(f"   ✅ Both events found: STARTED + COMPLETED")
                results.append(("Events Logged", "OK", "Both events present"))
            elif started_found:
                print(f"   ⚠️  Only STARTED event found")
                results.append(("Events Logged", "PARTIAL", "Only STARTED"))
            elif completed_found:
                print(f"   ⚠️  Only COMPLETED event found")
                results.append(("Events Logged", "PARTIAL", "Only COMPLETED"))
            else:
                print(f"   ❌ Neither event found")
                results.append(("Events Logged", "MISSING", "No events"))
                
        except Exception as e:
            print(f"   ERROR: {e}")
            results.append(("Events Logged", "ERROR", str(e)))
        
    finally:
        # Stop servers
        print("\n8. Stopping servers...")
        kernel_process.terminate()
        os_core_process.terminate()
        kernel_process.wait(timeout=5)
        os_core_process.wait(timeout=5)
        print("   Servers stopped.")
    
    # Summary
    print("\n" + "=" * 70)
    print("SMOKE TEST SUMMARY")
    print("=" * 70)
    for test_name, status, result in results:
        print(f"{test_name:30s}: {str(status):10s} - {result}")
    
    print("\n" + "=" * 70)
    print("SLICE 2A SMOKE TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    run_slice_2a_smoke_test()
