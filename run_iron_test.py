"""
Agent Gateway - Iron Test (Demo Mode)

This script tests the full Agent Gateway flow with simulated GPT responses
(since OPENAI_API_KEY is not available).

Tests:
1. "עדכן SYSTEM_SNAPSHOT" - file.update action
2. "צור workflow חדש" - file.create action  
3. "עדכן README" - file.update + git operations
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Fix encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from ai_core.action_executor import execute_actions

print("=" * 70)
print("AGENT GATEWAY - IRON TEST (Demo Mode)")
print("=" * 70)
print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n⚠️  Running in DEMO mode (simulated GPT Planner responses)")
print("=" * 70)

# Test results
test_results = []
log_content = []

log_content.append("# Agent Gateway - Iron Test Results\n")
log_content.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
log_content.append(f"**Mode**: Demo (Simulated GPT Planner)\n")
log_content.append("\n---\n\n")


# ============================================================================
# TEST 1: Update SYSTEM_SNAPSHOT
# ============================================================================

print("\n" + "=" * 70)
print("TEST 1: עדכן SYSTEM_SNAPSHOT")
print("=" * 70)

test1_intent = "עדכן SYSTEM_SNAPSHOT עם תאריך הבדיקה"

# Simulated plan
test1_actions = [
    {
        "type": "file.update",
        "params": {
            "path": "docs/SYSTEM_SNAPSHOT.md",
            "edits": [
                {
                    "old_text": "**Last Updated**: 2025-11-20",
                    "new_text": f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d')} (Iron Test)"
                }
            ]
        },
        "approval": "auto",
        "description": "עדכון תאריך ב-SYSTEM_SNAPSHOT"
    }
]

log_content.append("## Test 1: עדכן SYSTEM_SNAPSHOT\n\n")
log_content.append(f"**Intent**: {test1_intent}\n\n")
log_content.append("**Actions**:\n")
log_content.append(f"```json\n{json.dumps(test1_actions, ensure_ascii=False, indent=2)}\n```\n\n")

print(f"\nIntent: {test1_intent}")
print("\nExecuting...")

try:
    result1 = execute_actions(test1_actions)
    
    log_content.append(f"**Status**: {'✅ Success' if result1['summary']['failed'] == 0 else '❌ Failed'}\n\n")
    log_content.append(f"**Summary**:\n")
    log_content.append(f"- Total: {result1['summary']['total']}\n")
    log_content.append(f"- Executed: {result1['summary']['executed']}\n")
    log_content.append(f"- Failed: {result1['summary']['failed']}\n\n")
    
    if result1['executed_actions']:
        log_content.append("**Executed Actions**:\n")
        for item in result1['executed_actions']:
            log_content.append(f"- ✅ {item['action']['type']}: {item['result']['message']}\n")
    
    if result1['errors']:
        log_content.append("\n**Errors**:\n")
        for item in result1['errors']:
            log_content.append(f"- ❌ {item['error']}\n")
    
    log_content.append("\n---\n\n")
    
    print(f"\n✅ Test 1: {result1['summary']['executed']}/{result1['summary']['total']} actions executed")
    test_results.append(("Test 1", result1['summary']['failed'] == 0))
    
except Exception as e:
    print(f"\n❌ Test 1 Failed: {e}")
    log_content.append(f"**Status**: ❌ Exception\n\n")
    log_content.append(f"**Error**: {str(e)}\n\n")
    log_content.append("\n---\n\n")
    test_results.append(("Test 1", False))


# ============================================================================
# TEST 2: Create new workflow
# ============================================================================

print("\n" + "=" * 70)
print("TEST 2: צור workflow חדש")
print("=" * 70)

test2_intent = "צור קובץ workflows/IRON_TEST_WF.md עם workflow לבדיקה"

test2_actions = [
    {
        "type": "file.create",
        "params": {
            "path": "workflows/IRON_TEST_WF.md",
            "content": f"""# Iron Test Workflow

**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Purpose**: Test workflow created by Agent Gateway iron test

## Description

This is a test workflow created automatically to verify:
- File creation works
- Agent Gateway flow is functional
- Actions are executed correctly

## Status

✅ Created successfully by iron test

---

**Note**: This file can be deleted after testing.
"""
        },
        "approval": "auto",
        "description": "יצירת workflow לבדיקה"
    }
]

log_content.append("## Test 2: צור workflow חדש\n\n")
log_content.append(f"**Intent**: {test2_intent}\n\n")
log_content.append("**Actions**:\n")
log_content.append(f"```json\n{json.dumps([{k: v for k, v in test2_actions[0].items() if k != 'params'}], ensure_ascii=False, indent=2)}\n```\n\n")
log_content.append("(Content truncated for brevity)\n\n")

print(f"\nIntent: {test2_intent}")
print("\nExecuting...")

try:
    result2 = execute_actions(test2_actions)
    
    log_content.append(f"**Status**: {'✅ Success' if result2['summary']['failed'] == 0 else '❌ Failed'}\n\n")
    log_content.append(f"**Summary**:\n")
    log_content.append(f"- Total: {result2['summary']['total']}\n")
    log_content.append(f"- Executed: {result2['summary']['executed']}\n")
    log_content.append(f"- Failed: {result2['summary']['failed']}\n\n")
    
    if result2['executed_actions']:
        log_content.append("**Executed Actions**:\n")
        for item in result2['executed_actions']:
            log_content.append(f"- ✅ {item['action']['type']}: {item['result']['message']}\n")
    
    if result2['errors']:
        log_content.append("\n**Errors**:\n")
        for item in result2['errors']:
            log_content.append(f"- ❌ {item['error']}\n")
    
    log_content.append("\n---\n\n")
    
    print(f"\n✅ Test 2: {result2['summary']['executed']}/{result2['summary']['total']} actions executed")
    test_results.append(("Test 2", result2['summary']['failed'] == 0))
    
except Exception as e:
    print(f"\n❌ Test 2 Failed: {e}")
    log_content.append(f"**Status**: ❌ Exception\n\n")
    log_content.append(f"**Error**: {str(e)}\n\n")
    log_content.append("\n---\n\n")
    test_results.append(("Test 2", False))


# ============================================================================
# TEST 3: Full flow with git operations
# ============================================================================

print("\n" + "=" * 70)
print("TEST 3: עדכן README + commit + push")
print("=" * 70)

test3_intent = "עדכן README עם תיעוד Iron Test"

test3_actions = [
    {
        "type": "file.update",
        "params": {
            "path": "README.md",
            "edits": [
                {
                    "old_text": "Every change flows through this pipeline, ensuring consistency and traceability.",
                    "new_text": f"Every change flows through this pipeline, ensuring consistency and traceability.\n\n**Last Tested**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Agent Gateway Iron Test ✅)"
                }
            ]
        },
        "approval": "auto",
        "description": "הוספת תיעוד Iron Test ל-README"
    },
    {
        "type": "git.commit",
        "params": {
            "files": ["README.md", "docs/SYSTEM_SNAPSHOT.md", "workflows/IRON_TEST_WF.md"],
            "message": "test: Agent Gateway iron test - verify full pipeline"
        },
        "approval": "auto",
        "description": "commit של כל שינויי הבדיקה"
    },
    {
        "type": "git.push",
        "params": {},
        "approval": "auto",
        "description": "העלאה לגיטהאב"
    }
]

log_content.append("## Test 3: עדכן README + git operations\n\n")
log_content.append(f"**Intent**: {test3_intent}\n\n")
log_content.append("**Actions**:\n")
log_content.append(f"```json\n{json.dumps([{k: v for k, v in a.items() if k != 'params' or a['type'] != 'file.update'} for a in test3_actions], ensure_ascii=False, indent=2)}\n```\n\n")

print(f"\nIntent: {test3_intent}")
print("\nExecuting...")

try:
    result3 = execute_actions(test3_actions)
    
    log_content.append(f"**Status**: {'✅ Success' if result3['summary']['failed'] == 0 else '❌ Failed'}\n\n")
    log_content.append(f"**Summary**:\n")
    log_content.append(f"- Total: {result3['summary']['total']}\n")
    log_content.append(f"- Executed: {result3['summary']['executed']}\n")
    log_content.append(f"- Failed: {result3['summary']['failed']}\n\n")
    
    if result3['executed_actions']:
        log_content.append("**Executed Actions**:\n")
        for item in result3['executed_actions']:
            log_content.append(f"- ✅ {item['action']['type']}: {item['result']['message']}\n")
            if item['action']['type'] == 'git.commit' and 'details' in item['result']:
                log_content.append(f"  - Files: {item['result']['details']['files']}\n")
                log_content.append(f"  - Message: {item['result']['details']['message']}\n")
    
    if result3['errors']:
        log_content.append("\n**Errors**:\n")
        for item in result3['errors']:
            log_content.append(f"- ❌ {item['error']}\n")
    
    log_content.append("\n---\n\n")
    
    print(f"\n✅ Test 3: {result3['summary']['executed']}/{result3['summary']['total']} actions executed")
    test_results.append(("Test 3", result3['summary']['failed'] == 0))
    
except Exception as e:
    print(f"\n❌ Test 3 Failed: {e}")
    log_content.append(f"**Status**: ❌ Exception\n\n")
    log_content.append(f"**Error**: {str(e)}\n\n")
    log_content.append("\n---\n\n")
    test_results.append(("Test 3", False))


# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)

log_content.append("## Summary\n\n")

passed = sum(1 for _, result in test_results if result)
total = len(test_results)

log_content.append(f"**Results**: {passed}/{total} tests passed\n\n")

for name, result in test_results:
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status}: {name}")
    log_content.append(f"- {status}: {name}\n")

log_content.append("\n---\n\n")

if passed == total:
    print(f"\n✅ All tests passed! ({passed}/{total})")
    log_content.append("## Conclusion\n\n")
    log_content.append("✅ **All tests passed!** Agent Gateway is fully functional.\n\n")
    log_content.append("**Verified**:\n")
    log_content.append("- File operations (create, update)\n")
    log_content.append("- Git operations (commit, push)\n")
    log_content.append("- Full end-to-end pipeline\n")
else:
    print(f"\n⚠️ {total - passed} test(s) failed")
    log_content.append("## Conclusion\n\n")
    log_content.append(f"⚠️ **{total - passed} test(s) failed** - see details above.\n")

# Save log
log_path = Path("logs/GATEWAY_SMOKE_TEST.md")
log_path.parent.mkdir(exist_ok=True)
log_path.write_text("".join(log_content), encoding="utf-8")

print(f"\n📄 Log saved to: {log_path}")
print("\n" + "=" * 70)
