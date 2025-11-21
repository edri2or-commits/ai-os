"""
AI-OS One-Command Startup

Smart startup script that:
1. Checks dependencies
2. Verifies configuration
3. Starts Agent Gateway Server
4. Shows clear status

Usage:
    python start.py
    
Or double-click: start.bat
"""

import sys
import subprocess
from pathlib import Path
import importlib.util

# Fix encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("AI-OS - One-Command Startup")
print("=" * 70)

project_root = Path(__file__).parent

# ============================================================================
# Step 1: Check Python Version
# ============================================================================

print("\n📋 Step 1: Checking Python version...")

python_version = sys.version_info
if python_version < (3, 10):
    print(f"❌ Python {python_version.major}.{python_version.minor} detected")
    print(f"✅ Required: Python 3.10+")
    print("\n💡 Please upgrade Python:")
    print("   https://www.python.org/downloads/")
    sys.exit(1)

print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")

# ============================================================================
# Step 2: Check Dependencies
# ============================================================================

print("\n📋 Step 2: Checking dependencies...")

required_packages = {
    'openai': 'openai',
    'fastapi': 'fastapi',
    'uvicorn': 'uvicorn',
    'dotenv': 'python-dotenv'
}

missing_packages = []

for import_name, package_name in required_packages.items():
    spec = importlib.util.find_spec(import_name)
    if spec is None:
        missing_packages.append(package_name)
        print(f"❌ {package_name} - NOT INSTALLED")
    else:
        print(f"✅ {package_name}")

if missing_packages:
    print(f"\n⚠️  Missing {len(missing_packages)} package(s)")
    print("\n💡 Installing missing packages...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install"] + missing_packages,
            check=True,
            capture_output=True
        )
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("\n💡 Try manually:")
        print(f"   pip install {' '.join(missing_packages)}")
        sys.exit(1)

# ============================================================================
# Step 3: Check Configuration
# ============================================================================

print("\n📋 Step 3: Checking configuration...")

env_file = project_root / ".env"
env_template = project_root / ".env.template"

if not env_file.exists():
    print("⚠️  No .env file found")
    
    if env_template.exists():
        print("\n💡 Run setup first:")
        print("   python setup_env.py")
        print("\n   Or use Demo Mode (no setup needed):")
        
        response = input("\n   Start in Demo Mode? (yes/no): ").strip().lower()
        
        if response in ['yes', 'y']:
            # Create temporary .env for demo mode
            demo_env = """# AI-OS Environment - Demo Mode (Auto-generated)
DEMO_MODE=true
OPENAI_API_KEY=demo-mode-no-key-needed
OPENAI_MODEL=gpt-4o-mini
SERVER_PORT=8000
"""
            env_file.write_text(demo_env, encoding='utf-8')
            print("✅ Demo Mode configured")
        else:
            print("\n   Exiting. Run 'python setup_env.py' first.")
            sys.exit(0)
    else:
        print("❌ .env.template not found")
        sys.exit(1)
else:
    print("✅ .env file exists")

# ============================================================================
# Step 4: Load and Verify Configuration
# ============================================================================

print("\n📋 Step 4: Loading configuration...")

try:
    from dotenv import load_dotenv
    load_dotenv(env_file)
    
    import os
    
    demo_mode = os.getenv('DEMO_MODE', 'false').lower() == 'true'
    api_key = os.getenv('OPENAI_API_KEY', '')
    model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    port = int(os.getenv('SERVER_PORT', '8000'))
    
    if demo_mode:
        print("✅ Mode: Demo (Simulated GPT)")
        print("   - No API key required")
        print("   - GPT Planner uses simulated responses")
    else:
        if api_key and api_key.startswith('sk-'):
            print("✅ Mode: Real GPT")
            print(f"   - Model: {model}")
            print(f"   - API Key: sk-...{api_key[-4:]}")
        else:
            print("⚠️  Mode: Demo (API key invalid)")
            print("   - Falling back to demo mode")
    
    print(f"✅ Port: {port}")
    
except Exception as e:
    print(f"❌ Configuration error: {e}")
    sys.exit(1)

# ============================================================================
# Step 5: Check Repository
# ============================================================================

print("\n📋 Step 5: Checking repository...")

critical_paths = [
    "ai_core/agent_gateway.py",
    "ai_core/agent_gateway_server.py",
    "ai_core/intent_router.py",
    "ai_core/action_executor.py",
]

for path_str in critical_paths:
    path = project_root / path_str
    if not path.exists():
        print(f"❌ Missing: {path_str}")
        print("\n💡 Repository may be corrupted. Try:")
        print("   git pull")
        sys.exit(1)

print("✅ All core files present")

# ============================================================================
# Step 6: Start Server
# ============================================================================

print("\n" + "=" * 70)
print("🚀 Starting Agent Gateway Server...")
print("=" * 70)

print(f"\n📍 Server will start on: http://localhost:{port}")
print(f"\n📖 API Documentation: http://localhost:{port}/docs")
print(f"\n🏥 Health Check: http://localhost:{port}/health")
print(f"\n⏸️  Press CTRL+C to stop")
print("\n" + "=" * 70)

try:
    # Start uvicorn server
    subprocess.run(
        [
            sys.executable, "-m", "uvicorn",
            "ai_core.agent_gateway_server:app",
            "--host", "0.0.0.0",
            "--port", str(port)
        ],
        cwd=project_root,
        check=True
    )
except KeyboardInterrupt:
    print("\n\n🛑 Server stopped by user")
    print("=" * 70)
except Exception as e:
    print(f"\n\n❌ Server error: {e}")
    print("\n💡 Try:")
    print("   1. Check if port is available")
    print("   2. Check error message above")
    print("   3. Run: python -m ai_core.agent_gateway_server")
    sys.exit(1)
