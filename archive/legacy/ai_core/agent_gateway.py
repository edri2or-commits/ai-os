"""
Agent Gateway v1.0 - Unified entry point for AI-OS

This module provides a single, clean interface for all external agents:
- Custom GPTs
- Telegram bots
- Web UIs
- CLI tools

It wraps the entire pipeline: Intent → Planner → Router → Executor
"""

from typing import Dict, Any, List, Optional
from ai_core.intent_router import route_intent
from ai_core.action_executor import execute_actions


def plan_and_optionally_execute(
    intent: str,
    auto_execute: bool = False,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Main entry point: takes user intent, plans, and optionally executes.
    
    This is the ONLY function external agents need to call.
    
    Args:
        intent: User's intent in natural language (Hebrew/English)
                Example: "צור workflow חדש לניהול טוקנים"
        
        auto_execute: If True, automatically execute all 'auto' approval actions
                     If False, return plan without executing
        
        dry_run: If True, simulate execution without making real changes
                 (not fully implemented yet - placeholder for future)
    
    Returns:
        {
            "status": "success" | "validation_failed" | "execution_failed",
            "intent": str,              # Original intent
            "plan": {                   # Full plan from Router
                "summary": str,
                "context": str,
                "steps": List[str],
                "actions_for_claude": List[Action],
                "decisions_for_or": List[str],
                "version": str
            },
            "validation": {             # Validation results
                "valid": bool,
                "total": int,
                "valid_count": int,
                "invalid_count": int,
                "errors": List[str]
            },
            "execution": {              # Execution results (if auto_execute=True)
                "executed": bool,       # Was execution attempted?
                "executed_actions": List[Dict],
                "pending_approval": List[Dict],
                "errors": List[Dict],
                "summary": {
                    "total": int,
                    "executed": int,
                    "pending": int,
                    "failed": int
                }
            } | None,                   # None if auto_execute=False
            "message": str              # Human-readable status message
        }
    
    Example (planning only):
        >>> result = plan_and_optionally_execute("צור workflow", auto_execute=False)
        >>> print(result["plan"]["summary"])
        "אור רוצה workflow חדש..."
        >>> print(result["execution"])
        None  # Because auto_execute=False
    
    Example (plan + execute):
        >>> result = plan_and_optionally_execute("עדכן README", auto_execute=True)
        >>> print(result["execution"]["summary"])
        {"total": 3, "executed": 3, "pending": 0, "failed": 0}
    """
    
    # Step 1: Route intent through planner
    try:
        plan = route_intent(intent)
    except Exception as e:
        return {
            "status": "planning_failed",
            "intent": intent,
            "plan": None,
            "validation": None,
            "execution": None,
            "message": f"Failed to plan: {str(e)}",
            "error": str(e)
        }
    
    # Step 2: Check validation
    validation = plan["actions_validation"]
    
    if not validation["valid"]:
        return {
            "status": "validation_failed",
            "intent": intent,
            "plan": {
                "summary": plan["summary"],
                "context": plan["context"],
                "steps": plan["steps"],
                "actions_for_claude": plan["actions_for_claude"],
                "decisions_for_or": plan["decisions_for_or"],
                "version": plan["version"]
            },
            "validation": {
                "valid": validation["valid"],
                "total": validation["total"],
                "valid_count": validation["valid_count"],
                "invalid_count": validation["invalid_count"],
                "errors": validation["errors"]
            },
            "execution": None,
            "message": f"Validation failed: {validation['invalid_count']} invalid actions"
        }
    
    # Step 3: Execute if requested
    execution_result = None
    
    if auto_execute:
        try:
            actions = plan["actions_for_claude"]
            execution_result = execute_actions(actions)
            
            # Check for execution errors
            if execution_result["summary"]["failed"] > 0:
                status = "execution_partial"
                message = f"Executed {execution_result['summary']['executed']}/{execution_result['summary']['total']} actions. {execution_result['summary']['failed']} failed."
            else:
                status = "success"
                message = f"Successfully executed {execution_result['summary']['executed']} actions"
        
        except Exception as e:
            return {
                "status": "execution_failed",
                "intent": intent,
                "plan": {
                    "summary": plan["summary"],
                    "context": plan["context"],
                    "steps": plan["steps"],
                    "actions_for_claude": plan["actions_for_claude"],
                    "decisions_for_or": plan["decisions_for_or"],
                    "version": plan["version"]
                },
                "validation": {
                    "valid": validation["valid"],
                    "total": validation["total"],
                    "valid_count": validation["valid_count"],
                    "invalid_count": validation["invalid_count"],
                    "errors": validation["errors"]
                },
                "execution": None,
                "message": f"Execution failed: {str(e)}",
                "error": str(e)
            }
    else:
        status = "plan_ready"
        message = f"Plan ready with {validation['total']} actions. Set auto_execute=True to execute."
    
    # Return full result
    return {
        "status": status,
        "intent": intent,
        "plan": {
            "summary": plan["summary"],
            "context": plan["context"],
            "steps": plan["steps"],
            "actions_for_claude": plan["actions_for_claude"],
            "decisions_for_or": plan["decisions_for_or"],
            "version": plan["version"]
        },
        "validation": {
            "valid": validation["valid"],
            "total": validation["total"],
            "valid_count": validation["valid_count"],
            "invalid_count": validation["invalid_count"],
            "errors": validation["errors"]
        },
        "execution": {
            "executed": auto_execute,
            "executed_actions": execution_result["executed_actions"] if execution_result else [],
            "pending_approval": execution_result["pending_approval"] if execution_result else [],
            "errors": execution_result["errors"] if execution_result else [],
            "summary": execution_result["summary"] if execution_result else None
        } if auto_execute else None,
        "message": message
    }


# Convenience functions for common use cases

def quick_plan(intent: str) -> str:
    """
    Get just the plan summary for quick feedback.
    
    Example:
        >>> summary = quick_plan("צור workflow")
        >>> print(summary)
        "אור רוצה workflow חדש..."
    """
    result = plan_and_optionally_execute(intent, auto_execute=False)
    if result["status"] == "planning_failed":
        return f"Error: {result['message']}"
    return result["plan"]["summary"]


def plan_and_execute(intent: str) -> Dict[str, Any]:
    """
    Plan + execute in one call (convenience wrapper).
    
    Example:
        >>> result = plan_and_execute("עדכן README")
        >>> print(result["execution"]["summary"])
        {"total": 3, "executed": 3, "pending": 0, "failed": 0}
    """
    return plan_and_optionally_execute(intent, auto_execute=True)


def validate_only(intent: str) -> Dict[str, Any]:
    """
    Just validate the plan without executing.
    Returns validation details.
    
    Example:
        >>> result = validate_only("צור workflow")
        >>> print(result["validation"]["valid"])
        True
    """
    result = plan_and_optionally_execute(intent, auto_execute=False)
    return {
        "intent": intent,
        "valid": result["validation"]["valid"] if result["validation"] else False,
        "validation": result["validation"],
        "actions_count": result["validation"]["total"] if result["validation"] else 0,
        "message": result["message"]
    }


if __name__ == "__main__":
    import sys
    import json
    
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    
    # Smoke test
    print("Agent Gateway v1.0 - Smoke Test")
    print("=" * 70)
    
    test_intent = "צור קובץ docs/GATEWAY_TEST.md עם הסבר על Agent Gateway"
    
    print(f"\n📝 Intent: {test_intent}")
    print("-" * 70)
    
    # Test 1: Plan only
    print("\n🔍 Test 1: Plan only (auto_execute=False)")
    result1 = plan_and_optionally_execute(test_intent, auto_execute=False)
    
    print(f"Status: {result1['status']}")
    print(f"Message: {result1['message']}")
    if result1['plan']:
        print(f"Summary: {result1['plan']['summary'][:80]}...")
        print(f"Actions: {result1['validation']['total']}")
    
    # Test 2: Quick plan
    print("\n🔍 Test 2: Quick plan")
    summary = quick_plan(test_intent)
    print(f"Summary: {summary[:100]}...")
    
    # Test 3: Validate only
    print("\n🔍 Test 3: Validate only")
    validation = validate_only(test_intent)
    print(f"Valid: {validation['valid']}")
    print(f"Actions: {validation['actions_count']}")
    
    print("\n" + "=" * 70)
    print("✅ Smoke test complete!")
