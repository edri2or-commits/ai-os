"""
Auto-Sync API Key from SSOT

This script automatically syncs OPENAI_API_KEY from the SSOT location
to the AI-OS .env file, without requiring manual copy-paste.

SSOT Location: C:\Users\edri2\make-ops-clean\SECRETS\.env.local
Target: C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace\.env

Usage:
    python sync_api_key.py
"""

import sys
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("API Key Sync - From SSOT to AI-OS")
print("=" * 70)

# Paths
SSOT_PATH = Path("C:/Users/edri2/make-ops-clean/SECRETS/.env.local")
TARGET_PATH = Path(__file__).parent / ".env"

# Step 1: Read SSOT
print("\n📋 Step 1: Reading SSOT...")
print(f"   Location: {SSOT_PATH}")

if not SSOT_PATH.exists():
    print(f"❌ SSOT file not found!")
    print(f"\n💡 Expected at: {SSOT_PATH}")
    sys.exit(1)

ssot_content = SSOT_PATH.read_text(encoding='utf-8')
print("✅ SSOT loaded")

# Extract API key
api_key = None
for line in ssot_content.split('\n'):
    if line.strip().startswith('OPENAI_API_KEY='):
        api_key = line.split('=', 1)[1].strip()
        break

if not api_key:
    print("❌ OPENAI_API_KEY not found in SSOT")
    sys.exit(1)

if not api_key.startswith('sk-'):
    print("❌ Invalid API key format (should start with sk-)")
    sys.exit(1)

masked_key = f"{api_key[:7]}...{api_key[-4:]}"
print(f"✅ API Key found: {masked_key}")

# Step 2: Create/Update .env
print("\n📋 Step 2: Updating .env...")
print(f"   Location: {TARGET_PATH}")

env_content = f"""# AI-OS Environment Configuration
# Auto-synced from SSOT: {SSOT_PATH}
# Last sync: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Mode: Real GPT (API key synced from SSOT)
DEMO_MODE=false

# OpenAI API Key (from SSOT)
OPENAI_API_KEY={api_key}

# OpenAI Model
OPENAI_MODEL=gpt-4o-mini

# Server Port
SERVER_PORT=8000
"""

TARGET_PATH.write_text(env_content, encoding='utf-8')
print("✅ .env updated")

# Step 3: Verify
print("\n📋 Step 3: Verifying...")

from dotenv import load_dotenv
import os

load_dotenv(TARGET_PATH)

loaded_key = os.getenv('OPENAI_API_KEY', '')
demo_mode = os.getenv('DEMO_MODE', 'true').lower() == 'true'

if loaded_key == api_key:
    print("✅ API key verified in .env")
else:
    print("⚠️  API key mismatch")

if not demo_mode:
    print("✅ Demo mode: OFF")
else:
    print("⚠️  Demo mode still ON")

print("\n" + "=" * 70)
print("✅ API Key Sync Complete!")
print("=" * 70)

print("\n💡 Next steps:")
print("   1. Run: python test_real_gpt.py")
print("   2. Run: python start.py")
print("\n" + "=" * 70)
