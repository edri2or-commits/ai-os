"""
Test Agent Gateway
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_core.agent_gateway import plan_and_optionally_execute, quick_plan, validate_only
import json

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("Agent Gateway v1.0 - Smoke Test")
print("=" * 70)

test_intent = "צור קובץ docs/GATEWAY_TEST.md עם הסבר על Agent Gateway"

print(f"\n📝 Intent: {test_intent}")
print("-" * 70)

# Test 1: Quick plan
print("\n🔍 Test 1: Quick plan")
try:
    summary = quick_plan(test_intent)
    print(f"Summary: {summary[:100]}...")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Validate only
print("\n🔍 Test 2: Validate only")
try:
    validation = validate_only(test_intent)
    print(f"Valid: {validation['valid']}")
    print(f"Actions: {validation['actions_count']}")
    print(f"Message: {validation['message']}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Plan only (full response)
print("\n🔍 Test 3: Plan only (full response)")
try:
    result = plan_and_optionally_execute(test_intent, auto_execute=False)
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    if result['plan']:
        print(f"Summary: {result['plan']['summary'][:80]}...")
        print(f"Actions: {result['validation']['total']}")
        print(f"Valid: {result['validation']['valid']}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("✅ Smoke test complete!")
