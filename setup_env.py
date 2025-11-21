"""
AI-OS Environment Setup

Interactive script to help set up .env file for AI-OS.
Run once to configure your environment.
"""

import sys
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stdin = codecs.getreader('utf-8')(sys.stdin.buffer, 'strict')

print("=" * 70)
print("AI-OS Environment Setup")
print("=" * 70)

project_root = Path(__file__).parent
env_file = project_root / ".env"
template_file = project_root / ".env.template"

# Check if .env already exists
if env_file.exists():
    print("\n⚠️  .env file already exists!")
    response = input("Do you want to overwrite it? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("\n✅ Keeping existing .env file")
        print("=" * 70)
        sys.exit(0)

print("\n📝 Let's set up your environment...")
print("\nYou have two options:")
print("1. Demo Mode - Use simulated GPT responses (no API key needed)")
print("2. Real GPT - Use OpenAI's GPT-4 (requires API key)")

while True:
    choice = input("\nWhich mode do you want? (1/2): ").strip()
    if choice in ['1', '2']:
        break
    print("❌ Please enter 1 or 2")

if choice == '1':
    # Demo Mode
    print("\n✅ Setting up Demo Mode...")
    print("   - No API key required")
    print("   - GPT Planner will use simulated responses")
    print("   - Everything else works normally")
    
    env_content = """# AI-OS Environment Configuration
# Mode: Demo (Simulated GPT)

# Demo Mode - Using simulated GPT responses
DEMO_MODE=true

# OpenAI API Key (not required in demo mode)
OPENAI_API_KEY=demo-mode-no-key-needed

# OpenAI Model
OPENAI_MODEL=gpt-4o-mini

# Server Port
SERVER_PORT=8000
"""
    
else:
    # Real GPT Mode
    print("\n🔑 Setting up Real GPT Mode...")
    print("\n📍 To get your OpenAI API key:")
    print("   1. Go to: https://platform.openai.com/api-keys")
    print("   2. Sign in or create account")
    print("   3. Click 'Create new secret key'")
    print("   4. Copy the key (starts with 'sk-')")
    
    while True:
        api_key = input("\n🔑 Paste your OpenAI API key: ").strip()
        if api_key.startswith('sk-') and len(api_key) > 20:
            break
        elif api_key == '':
            print("❌ API key cannot be empty")
        elif not api_key.startswith('sk-'):
            print("❌ OpenAI API keys start with 'sk-'")
        else:
            print("❌ API key seems too short")
    
    print("\n📊 Choose model:")
    print("   1. gpt-4o-mini (Recommended - Fast & Cheap)")
    print("   2. gpt-4o (More capable, more expensive)")
    print("   3. gpt-4-turbo (Previous generation)")
    
    model_choices = {
        '1': 'gpt-4o-mini',
        '2': 'gpt-4o',
        '3': 'gpt-4-turbo'
    }
    
    while True:
        model_choice = input("\nModel (1/2/3): ").strip()
        if model_choice in model_choices:
            break
        print("❌ Please enter 1, 2, or 3")
    
    selected_model = model_choices[model_choice]
    
    env_content = f"""# AI-OS Environment Configuration
# Mode: Real GPT

# Demo Mode
DEMO_MODE=false

# OpenAI API Key
OPENAI_API_KEY={api_key}

# OpenAI Model
OPENAI_MODEL={selected_model}

# Server Port
SERVER_PORT=8000
"""

# Write .env file
env_file.write_text(env_content, encoding='utf-8')

print("\n" + "=" * 70)
print("✅ Setup Complete!")
print("=" * 70)
print(f"\n📄 Created: {env_file}")

if choice == '1':
    print("\n🎭 Demo Mode Active:")
    print("   - GPT Planner uses simulated responses")
    print("   - No API costs")
    print("   - Everything else works normally")
else:
    print("\n🚀 Real GPT Mode Active:")
    print(f"   - Model: {selected_model}")
    print("   - GPT Planner will use OpenAI API")
    print("   - API costs apply")

print("\n▶️  Next Steps:")
print("   1. Run: python start.py")
print("   2. Or: python -m ai_core.agent_gateway_server")

print("\n💡 Tip: You can edit .env file manually anytime")
print("=" * 70)
