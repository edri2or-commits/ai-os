"""
Start MCP GitHub Client Service

Simple startup script for the MCP GitHub Client HTTP service.
This service provides HTTP endpoints for GitHub operations via MCP.

Usage:
    python start_github_client.py
    
Or with custom port:
    python start_github_client.py --port 8081
"""

import sys
import subprocess
import argparse
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("AI-OS MCP GitHub Client - HTTP Service")
print("=" * 70)

# Parse arguments
parser = argparse.ArgumentParser(description='Start MCP GitHub Client Service')
parser.add_argument('--port', type=int, default=8081, help='Port to run on (default: 8081)')
args = parser.parse_args()

project_root = Path(__file__).parent
port = args.port

# ============================================================================
# Step 1: Check Dependencies
# ============================================================================

print("\n📋 Step 1: Checking dependencies...")

try:
    import importlib.util
    
    required_packages = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'httpx': 'httpx',
        'pydantic': 'pydantic',
        'pydantic_settings': 'pydantic-settings',
        'dotenv': 'python-dotenv',
        'openai': 'openai'
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
        print("\n💡 Installing from requirements.txt...")
        
        requirements_file = project_root / "services" / "mcp_github_client" / "requirements.txt"
        
        if requirements_file.exists():
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                check=True
            )
            print("✅ Dependencies installed successfully!")
        else:
            print(f"❌ Requirements file not found: {requirements_file}")
            sys.exit(1)

except Exception as e:
    print(f"❌ Dependency check failed: {e}")
    sys.exit(1)

# ============================================================================
# Step 2: Check Configuration
# ============================================================================

print("\n📋 Step 2: Checking configuration...")

import os
from dotenv import load_dotenv

# Load .env from project root
env_file = project_root / ".env"

if env_file.exists():
    load_dotenv(env_file)
    print("✅ .env file loaded")
else:
    print("⚠️  No .env file found (will use defaults)")

# Check required env vars
github_pat = os.getenv('GITHUB_PAT')
github_owner = os.getenv('GITHUB_OWNER', 'edri2or-commits')
github_repo = os.getenv('GITHUB_REPO', 'ai-os')
openai_key = os.getenv('OPENAI_API_KEY')

print(f"\n📊 Configuration:")
print(f"   GitHub Owner: {github_owner}")
print(f"   GitHub Repo: {github_repo}")

if github_pat:
    print(f"   GitHub PAT: ***{github_pat[-4:]}")
else:
    print("   ⚠️  GitHub PAT: Not configured (read-only access)")
    print("      💡 Set GITHUB_PAT in .env for write operations")

if openai_key:
    print(f"   OpenAI Key: sk-...{openai_key[-4:]}")
else:
    print("   ⚠️  OpenAI Key: Not configured (AI features disabled)")
    print("      💡 Set OPENAI_API_KEY in .env for AI-powered PRs")

# ============================================================================
# Step 3: Start Service
# ============================================================================

print("\n" + "=" * 70)
print("🚀 Starting MCP GitHub Client Service...")
print("=" * 70)

print(f"\n📍 Service URL: http://localhost:{port}")
print(f"\n📖 API Documentation: http://localhost:{port}/docs")
print(f"\n🏥 Health Check: http://localhost:{port}/health")
print(f"\n📚 Endpoints:")
print(f"   POST /github/read-file   - Read a file from GitHub")
print(f"   POST /github/list-tree   - List repository tree")
print(f"   POST /github/open-pr     - Open a Pull Request")
print(f"\n⏸️  Press CTRL+C to stop")
print("\n" + "=" * 70)

try:
    # Start uvicorn server
    subprocess.run(
        [
            sys.executable, "-m", "uvicorn",
            "services.mcp_github_client.main:app",
            "--host", "0.0.0.0",
            "--port", str(port),
            "--reload"  # Auto-reload on code changes during development
        ],
        cwd=project_root,
        check=True
    )
except KeyboardInterrupt:
    print("\n\n🛑 Service stopped by user")
    print("=" * 70)
except Exception as e:
    print(f"\n\n❌ Service error: {e}")
    print("\n💡 Try:")
    print("   1. Check if port is available")
    print("   2. Verify all dependencies are installed")
    print("   3. Check error message above")
    sys.exit(1)
