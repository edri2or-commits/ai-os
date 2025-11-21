"""
End-to-End Test: Intent → Router → Executor

This script demonstrates the complete flow from user intent to execution.
"""

import sys
import json

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from ai_core.intent_router import route_intent
from ai_core.action_executor import execute_actions

print("=" * 70)
print("END-TO-END TEST: Intent → Router → Executor")
print("=" * 70)

# Test intent
test_intent = "צור קובץ docs/E2E_TEST.md עם הסבר קצר על Action Executor"

print(f"\n📝 Intent: {test_intent}")
print("-" * 70)

# Step 1: Route intent
print("\n🔄 Step 1: Routing intent through GPT Planner...")
try:
    plan = route_intent(test_intent)
    
    print(f"✅ Plan received!")
    print(f"   Summary: {plan['summary'][:80]}...")
    print(f"   Actions: {len(plan['actions_for_claude'])}")
    print(f"   Valid: {plan['actions_validation']['valid']}")
    
    if not plan['actions_validation']['valid']:
        print(f"\n⚠️ Validation errors:")
        for error in plan['actions_validation']['errors']:
            print(f"   - {error}")
        sys.exit(1)
    
except Exception as e:
    print(f"❌ Failed to route intent: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 2: Execute actions
print("\n🚀 Step 2: Executing actions...")
try:
    result = execute_actions(plan['actions_for_claude'])
    
    print(f"\n✅ Execution complete!")
    print(f"   Total: {result['summary']['total']}")
    print(f"   Executed: {result['summary']['executed']}")
    print(f"   Pending: {result['summary']['pending']}")
    print(f"   Failed: {result['summary']['failed']}")
    
    if result['executed_actions']:
        print(f"\n📋 Executed actions:")
        for item in result['executed_actions']:
            action = item['action']
            print(f"   ✅ {action['type']}: {action['description']}")
    
    if result['pending_approval']:
        print(f"\n⏳ Pending approval:")
        for item in result['pending_approval']:
            action = item['action']
            print(f"   ⏸️ {action['type']}: {action['description']}")
    
    if result['errors']:
        print(f"\n❌ Errors:")
        for item in result['errors']:
            print(f"   ❌ {item['error']}")
    
    print(f"\n📊 Full result:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
except Exception as e:
    print(f"❌ Failed to execute: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ END-TO-END TEST COMPLETE!")
print("=" * 70)
