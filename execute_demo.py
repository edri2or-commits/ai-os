"""
Execute approved actions for README update
"""

import sys
import json

sys.path.insert(0, '.')

from ai_core.action_executor import execute_actions

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Load the approved plan
with open("demo_plan.json", "r", encoding="utf-8") as f:
    plan = json.load(f)

print("=" * 70)
print("EXECUTING APPROVED ACTIONS")
print("=" * 70)

actions = plan["actions_for_claude"]

print(f"\n📋 Executing {len(actions)} actions...")

# Execute!
result = execute_actions(actions)

print("\n" + "=" * 70)
print("EXECUTION COMPLETE")
print("=" * 70)

print(f"\n📊 Summary:")
print(f"   Total: {result['summary']['total']}")
print(f"   Executed: {result['summary']['executed']}")
print(f"   Pending: {result['summary']['pending']}")
print(f"   Failed: {result['summary']['failed']}")

if result['executed_actions']:
    print(f"\n✅ Executed actions:")
    for item in result['executed_actions']:
        action = item['action']
        res = item['result']
        print(f"   ✅ {action['type']}: {res['message']}")

if result['pending_approval']:
    print(f"\n⏳ Pending approval:")
    for item in result['pending_approval']:
        action = item['action']
        print(f"   ⏸️ {action['type']}: {item['reason']}")

if result['errors']:
    print(f"\n❌ Errors:")
    for item in result['errors']:
        print(f"   ❌ {item['error']}")

print(f"\n📄 Full result:")
print(json.dumps(result, ensure_ascii=False, indent=2))
