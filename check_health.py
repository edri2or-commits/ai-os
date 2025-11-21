"""
System Health Check - Local Script

Runs comprehensive health checks on all AI-OS components.
Can be run locally without starting the server.

Usage:
    python check_health.py
"""

import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Fix encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("AI-OS SYSTEM HEALTH CHECK")
print("=" * 70)
print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "=" * 70)

# Results tracking
results = {}
overall_healthy = True

def check(name, status, message):
    """Record check result"""
    global overall_healthy
    results[name] = {
        "status": status,
        "message": message
    }
    
    icon = {"healthy": "✅", "warning": "⚠️", "error": "❌"}[status]
    print(f"{icon} {name}: {message}")
    
    if status == "error":
        overall_healthy = False

# ============================================================================
# Check 1: Python Version
# ============================================================================

print("\n📋 Check 1: Python Version")
try:
    version = sys.version_info
    if version >= (3, 10):
        check("Python", "healthy", f"Python {version.major}.{version.minor}.{version.micro}")
    else:
        check("Python", "warning", f"Python {version.major}.{version.minor} (3.10+ recommended)")
except Exception as e:
    check("Python", "error", str(e))

# ============================================================================
# Check 2: API Key Configuration
# ============================================================================

print("\n📋 Check 2: API Key Configuration")
try:
    from dotenv import load_dotenv
    
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        
        api_key = os.getenv('OPENAI_API_KEY', '')
        demo_mode = os.getenv('DEMO_MODE', 'false').lower() == 'true'
        
        if demo_mode:
            check("API Key", "warning", "Demo Mode (simulated GPT)")
        elif api_key and api_key.startswith('sk-'):
            masked = f"{api_key[:7]}...{api_key[-4:]}"
            check("API Key", "healthy", f"Real GPT configured ({masked})")
        else:
            check("API Key", "error", "No valid API key found")
    else:
        check("API Key", "error", ".env file not found")
except Exception as e:
    check("API Key", "error", str(e))

# ============================================================================
# Check 3: Dependencies
# ============================================================================

print("\n📋 Check 3: Dependencies")

required_deps = {
    'openai': 'OpenAI',
    'fastapi': 'FastAPI',
    'uvicorn': 'Uvicorn',
    'dotenv': 'python-dotenv',
    'requests': 'Requests'
}

missing = []

for import_name, package_name in required_deps.items():
    try:
        __import__(import_name)
    except ImportError:
        missing.append(package_name)

if not missing:
    check("Dependencies", "healthy", f"All {len(required_deps)} packages installed")
else:
    check("Dependencies", "error", f"Missing: {', '.join(missing)}")

# ============================================================================
# Check 4: Core Modules
# ============================================================================

print("\n📋 Check 4: Core Modules")

try:
    from ai_core.gpt_orchestrator import plan_change
    check("GPT Planner", "healthy", "Module loaded successfully")
except Exception as e:
    check("GPT Planner", "error", f"Failed to load: {str(e)}")

try:
    from ai_core.intent_router import route_intent
    check("Intent Router", "healthy", "Module loaded successfully")
except Exception as e:
    check("Intent Router", "error", f"Failed to load: {str(e)}")

try:
    from ai_core.action_executor import execute_actions
    check("Action Executor", "healthy", "Module loaded successfully")
except Exception as e:
    check("Action Executor", "error", f"Failed to load: {str(e)}")

try:
    from ai_core.agent_gateway import plan_and_optionally_execute
    check("Agent Gateway", "healthy", "Module loaded successfully")
except Exception as e:
    check("Agent Gateway", "error", f"Failed to load: {str(e)}")

# ============================================================================
# Check 5: Git
# ============================================================================

print("\n📋 Check 5: Git Operations")

try:
    result = subprocess.run(
        ["git", "--version"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode == 0:
        git_version = result.stdout.strip()
        check("Git", "healthy", git_version)
    else:
        check("Git", "error", "Git command failed")
except FileNotFoundError:
    check("Git", "error", "Git not found in PATH")
except Exception as e:
    check("Git", "error", str(e))

# ============================================================================
# Check 6: File System
# ============================================================================

print("\n📋 Check 6: File System Access")

try:
    project_root = Path(__file__).parent
    
    # Check read
    readme = project_root / "README.md"
    read_ok = readme.exists() and readme.is_file()
    
    # Check write
    test_file = project_root / ".health_check_test"
    try:
        test_file.write_text("test")
        write_ok = True
        test_file.unlink()
    except:
        write_ok = False
    
    if read_ok and write_ok:
        check("File System", "healthy", "Read and write access OK")
    elif read_ok:
        check("File System", "warning", "Read OK, write failed")
    else:
        check("File System", "error", "Access failed")
except Exception as e:
    check("File System", "error", str(e))

# ============================================================================
# Check 7: SSOT Files
# ============================================================================

print("\n📋 Check 7: SSOT Files")

try:
    from ai_core.gpt_orchestrator import SSOT_FILES
    
    missing_ssot = []
    for ssot_file in SSOT_FILES:
        if not ssot_file.exists():
            missing_ssot.append(ssot_file.name)
    
    if not missing_ssot:
        check("SSOT Files", "healthy", f"All {len(SSOT_FILES)} files present")
    else:
        check("SSOT Files", "warning", f"Missing: {', '.join(missing_ssot)}")
except Exception as e:
    check("SSOT Files", "error", str(e))

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("HEALTH CHECK SUMMARY")
print("=" * 70)

# Count statuses
healthy_count = sum(1 for r in results.values() if r["status"] == "healthy")
warning_count = sum(1 for r in results.values() if r["status"] == "warning")
error_count = sum(1 for r in results.values() if r["status"] == "error")
total_count = len(results)

print(f"\n📊 Results:")
print(f"   ✅ Healthy: {healthy_count}/{total_count}")
print(f"   ⚠️  Warning: {warning_count}/{total_count}")
print(f"   ❌ Error: {error_count}/{total_count}")

if overall_healthy and error_count == 0:
    print(f"\n✅ OVERALL STATUS: HEALTHY")
    print("\n💡 System is ready for use!")
    print("   Run: python start.py")
elif warning_count > 0 and error_count == 0:
    print(f"\n⚠️  OVERALL STATUS: WARNING")
    print("\n💡 System is functional but has warnings")
else:
    print(f"\n❌ OVERALL STATUS: DEGRADED")
    print(f"\n💡 Fix {error_count} error(s) before using")

print("\n" + "=" * 70)

# Exit code
sys.exit(0 if error_count == 0 else 1)
