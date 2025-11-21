"""
API Key Sync - From SSOT to AI-OS

This script automatically syncs OPENAI_API_KEY and TELEGRAM_BOT_TOKEN
from the SSOT location to the AI-OS .env file.

SSOT Location: C:/Users/edri2/make-ops-clean/SECRETS/.env.local
Target: C:/Users/edri2/Work/AI-Projects/ai-os-claude-workspace/.env

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
print(f"✅ OPENAI_API_KEY found: {masked_key}")

# Extract Telegram token (optional)
telegram_token = None
for line in ssot_content.split('\n'):
    if line.strip().startswith('TELEGRAM_BOT_TOKEN='):
        telegram_token = line.split('=', 1)[1].strip()
        break

if telegram_token:
    # Mask token (format: 123456:ABC-DEF...)
    if ':' in telegram_token:
        parts = telegram_token.split(':')
        masked_token = f"{parts[0][:3]}...:{parts[1][:3]}...{parts[1][-4:]}"
    else:
        masked_token = f"{telegram_token[:6]}...{telegram_token[-4:]}"
    print(f"✅ TELEGRAM_BOT_TOKEN found: {masked_token}")
else:
    print("⚠️  TELEGRAM_BOT_TOKEN not found (Chat1 will be disabled)")

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

# Telegram Bot Token (from SSOT)
TELEGRAM_BOT_TOKEN={telegram_token if telegram_token else ''}

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
loaded_telegram = os.getenv('TELEGRAM_BOT_TOKEN', '')
demo_mode = os.getenv('DEMO_MODE', 'true').lower() == 'true'

if loaded_key == api_key:
    print("✅ OPENAI_API_KEY verified in .env")
else:
    print("⚠️  OPENAI_API_KEY mismatch")

if telegram_token and loaded_telegram == telegram_token:
    print("✅ TELEGRAM_BOT_TOKEN verified in .env")
elif telegram_token:
    print("⚠️  TELEGRAM_BOT_TOKEN mismatch")

if not demo_mode:
    print("✅ Demo mode: OFF")
else:
    print("⚠️  Demo mode still ON")

print("\n" + "=" * 70)
print("✅ API Key Sync Complete!")
print("=" * 70)

print("\n💡 Next steps:")
if not telegram_token:
    print("   1. Get Telegram Bot Token from @BotFather")
    print("   2. Add to SSOT: TELEGRAM_BOT_TOKEN=your_token")
    print("   3. Run sync again: python sync_api_key.py")
    print("   4. Start system: python start.py")
else:
    print("   1. Run: python start.py")
    print("   2. Chat1 (Telegram) will start automatically!")
print("\n" + "=" * 70)
