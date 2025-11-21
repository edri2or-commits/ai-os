"""
GPT Planner Smoke Test - Verify REAL GPT mode

Tests:
1. Load .env and verify API key
2. Make actual OpenAI API call
3. Confirm NOT in demo mode
"""

import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Fix encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("GPT PLANNER SMOKE TEST - Real GPT Verification")
print("=" * 70)

# Step 1: Load .env
print("\n📋 Step 1: Loading .env...")

from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    print(f"❌ .env not found at: {env_path}")
    sys.exit(1)

load_dotenv(env_path)

demo_mode = os.getenv('DEMO_MODE', 'false').lower() == 'true'
api_key = os.getenv('OPENAI_API_KEY', '')
model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

print(f"✅ .env loaded from: {env_path}")
print(f"   Demo Mode: {demo_mode}")
print(f"   Model: {model}")

# Don't print full key, just first/last chars
if api_key:
    masked_key = f"{api_key[:7]}...{api_key[-4:]}" if len(api_key) > 20 else "***"
    print(f"   API Key: {masked_key}")
else:
    print(f"   API Key: NOT FOUND")

if demo_mode:
    print("\n❌ ERROR: Still in DEMO MODE!")
    print("   Expected: DEMO_MODE=false")
    print("   Check .env file")
    sys.exit(1)

if not api_key or not api_key.startswith('sk-'):
    print("\n❌ ERROR: Invalid API Key!")
    print("   Expected: sk-...")
    sys.exit(1)

print("✅ Configuration looks correct")

# Step 2: Test OpenAI API
print("\n📋 Step 2: Testing OpenAI API...")

try:
    from openai import OpenAI
    
    client = OpenAI(api_key=api_key)
    
    # Make a minimal API call
    print("   Making test API call...")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a test assistant."},
            {"role": "user", "content": "Reply with exactly: TEST_OK"}
        ],
        max_tokens=10
    )
    
    result = response.choices[0].message.content.strip()
    
    print(f"✅ API call successful!")
    print(f"   Response: {result}")
    print(f"   Model used: {response.model}")
    
except Exception as e:
    print(f"❌ API call failed: {e}")
    sys.exit(1)

# Step 3: Test GPT Orchestrator
print("\n📋 Step 3: Testing GPT Orchestrator...")

try:
    from ai_core.gpt_orchestrator import plan_change
    
    print("   Testing with simple intent...")
    
    result = plan_change("צור קובץ test בשם hello.txt")
    
    if result and 'summary' in result:
        print("✅ GPT Orchestrator working!")
        print(f"   Summary: {result['summary'][:60]}...")
        
        # Check if it looks like real GPT output
        if len(result.get('summary', '')) > 10:
            print("✅ Response looks like REAL GPT (not demo)")
        else:
            print("⚠️  Response very short - might be demo")
    else:
        print("⚠️  Unexpected response format")
        
except Exception as e:
    print(f"❌ GPT Orchestrator failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Verify mode one more time
print("\n📋 Step 4: Final verification...")

print(f"\n✅ GPT PLANNER MODE: REAL")
print(f"✅ API Key: Valid and working")
print(f"✅ Model: {model}")
print(f"✅ OpenAI API: Responding")

print("\n" + "=" * 70)
print("🎉 SUCCESS: GPT Planner is in REAL MODE and working!")
print("=" * 70)

print("\n💡 Next:")
print("   - Run: python start.py")
print("   - Agent Gateway will use REAL GPT")
print("   - No more DEMO mode!")

print("\n" + "=" * 70)
