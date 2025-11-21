"""
Intent Router v2.0 - High-level orchestration layer with Action validation

This module provides the entry point for routing raw user intents
into structured plans via GPT Planner, with full validation of structured Actions.

Status: IMPLEMENTED v2.0
- Structured Actions (JSON) from GPT Planner
- Full validation against ACTION_EXECUTION_SCHEMA
- Error flagging for invalid actions
"""

from typing import Dict, Any, List
from ai_core.gpt_orchestrator import plan_change


# Valid action types from ACTION_EXECUTION_SCHEMA.md
VALID_ACTION_TYPES = {
    "file.create",
    "file.update",
    "file.delete",
    "git.commit",
    "git.push",
    "workflow.run",
    "validation.check"
}

# Required params for each action type
ACTION_REQUIRED_PARAMS = {
    "file.create": ["path", "content"],
    "file.update": ["path", "edits"],
    "file.delete": ["path"],
    "git.commit": ["files", "message"],
    "git.push": [],
    "workflow.run": ["workflow_id"],
    "validation.check": ["check_type", "target"]
}


def validate_action(action: Dict[str, Any], index: int) -> Dict[str, Any]:
    """
    Validate a single action against ACTION_EXECUTION_SCHEMA.
    
    Returns:
        Dict with 'valid' (bool), 'errors' (List[str]), and original action
    """
    errors = []
    
    # Check required fields
    if "type" not in action:
        errors.append(f"Action #{index}: Missing required field 'type'")
    elif action["type"] not in VALID_ACTION_TYPES:
        errors.append(f"Action #{index}: Invalid type '{action['type']}'. Must be one of: {', '.join(VALID_ACTION_TYPES)}")
    
    if "params" not in action:
        errors.append(f"Action #{index}: Missing required field 'params'")
    
    if "approval" not in action:
        errors.append(f"Action #{index}: Missing required field 'approval'")
    elif action["approval"] not in ["auto", "manual"]:
        errors.append(f"Action #{index}: Invalid approval '{action['approval']}'. Must be 'auto' or 'manual'")
    
    if "description" not in action or not action["description"]:
        errors.append(f"Action #{index}: Missing or empty 'description'")
    
    # Check type-specific params
    if "type" in action and action["type"] in ACTION_REQUIRED_PARAMS:
        required_params = ACTION_REQUIRED_PARAMS[action["type"]]
        params = action.get("params", {})
        
        for param in required_params:
            if param not in params:
                errors.append(f"Action #{index}: Missing required param '{param}' for type '{action['type']}'")
    
    # Special rules
    if action.get("type") == "file.delete" and action.get("approval") != "manual":
        errors.append(f"Action #{index}: file.delete MUST have approval='manual' (security policy)")
    
    # Check for absolute paths (should be relative)
    if "params" in action and "path" in action["params"]:
        path = action["params"]["path"]
        if path.startswith("/") or ":" in path:  # Unix absolute or Windows absolute
            errors.append(f"Action #{index}: Path must be relative, not absolute: '{path}'")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "action": action
    }


def route_intent(intent_text: str) -> Dict[str, Any]:
    """
    High-level entry point for routing a raw intent string
    into a structured GPT plan with validated Actions.
    
    Args:
        intent_text: Raw user intent (Hebrew/English)
                    Example: "אני רוצה ליצור workflow חדש לניהול טוקנים"
    
    Returns:
        Structured plan as a Python dict.
        
        Format (v2.0):
        {
            "intent": str,                     # Original intent
            "summary": str,                    # What GPT understood
            "context": str,                    # Relevant SSOT context
            "steps": List[str],                # Step-by-step plan
            "actions_for_claude": List[Action], # Structured actions (JSON)
            "actions_validation": {            # Validation results
                "valid": bool,                 # All actions valid?
                "total": int,                  # Total actions
                "valid_count": int,            # Valid actions
                "invalid_count": int,          # Invalid actions
                "errors": List[str]            # All errors
            },
            "decisions_for_or": List[str],     # What Or needs to approve
            "version": str                     # Router version
        }
    
    Example:
        >>> result = route_intent("צור workflow חדש לגיבוי")
        >>> if result["actions_validation"]["valid"]:
        >>>     print("All actions valid!")
        >>> else:
        >>>     print("Errors:", result["actions_validation"]["errors"])
    """
    # Call GPT Planner to generate structured plan
    plan_dict = plan_change(intent_text)
    
    # Validate required keys exist
    required_keys = ["summary", "context", "steps", "actions_for_claude", "decisions_for_or"]
    for key in required_keys:
        if key not in plan_dict:
            plan_dict[key] = f"[Missing {key}]" if key not in ["actions_for_claude"] else []
    
    # Ensure lists are lists
    if not isinstance(plan_dict.get("steps"), list):
        plan_dict["steps"] = [str(plan_dict.get("steps", ""))]
    if not isinstance(plan_dict.get("actions_for_claude"), list):
        plan_dict["actions_for_claude"] = []
    if not isinstance(plan_dict.get("decisions_for_or"), list):
        plan_dict["decisions_for_or"] = [str(plan_dict.get("decisions_for_or", ""))]
    
    # Validate actions
    actions = plan_dict["actions_for_claude"]
    validation_results = []
    all_errors = []
    
    for i, action in enumerate(actions, 1):
        if not isinstance(action, dict):
            # Action is not structured JSON - this is an error
            error = f"Action #{i}: Must be JSON object, got {type(action).__name__}: {action}"
            all_errors.append(error)
            validation_results.append({
                "valid": False,
                "errors": [error],
                "action": action
            })
        else:
            result = validate_action(action, i)
            validation_results.append(result)
            all_errors.extend(result["errors"])
    
    # Add validation summary
    valid_count = sum(1 for r in validation_results if r["valid"])
    plan_dict["actions_validation"] = {
        "valid": len(all_errors) == 0,
        "total": len(actions),
        "valid_count": valid_count,
        "invalid_count": len(actions) - valid_count,
        "errors": all_errors,
        "details": validation_results  # Full validation details per action
    }
    
    # Add metadata
    plan_dict["intent"] = intent_text
    plan_dict["version"] = "2.0"
    
    return plan_dict


# Convenience aliases for different entry points
def process_intent(intent_text: str) -> Dict[str, Any]:
    """Alias for route_intent - same functionality"""
    return route_intent(intent_text)


def quick_summary(intent_text: str) -> str:
    """
    Quick access to just the summary (what GPT understood).
    
    Returns:
        str: The summary from GPT Planner
    """
    result = route_intent(intent_text)
    return result["summary"]


def get_claude_actions(intent_text: str) -> List[Dict[str, Any]]:
    """
    Quick access to Claude's action list (structured).
    
    Returns:
        List[Action]: Structured actions for Claude to execute
    """
    result = route_intent(intent_text)
    return result["actions_for_claude"]


def get_validation_report(intent_text: str) -> str:
    """
    Get a human-readable validation report.
    
    Returns:
        str: Formatted validation report
    """
    result = route_intent(intent_text)
    validation = result["actions_validation"]
    
    if validation["valid"]:
        return f"✅ All {validation['total']} actions are valid!"
    else:
        report = [f"⚠️ {validation['invalid_count']}/{validation['total']} actions have errors:\n"]
        for error in validation["errors"]:
            report.append(f"  - {error}")
        return "\n".join(report)


if __name__ == "__main__":
    import sys
    import json
    
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    
    # Simple smoke test
    print("Intent Router v2.0 - Smoke Test")
    print("=" * 50)
    
    test_intent = "צור קובץ README.md פשוט"
    print(f"\nIntent: {test_intent}")
    print("-" * 50)
    
    try:
        result = route_intent(test_intent)
        print(f"\n✅ Success! Version: {result['version']}")
        print(f"\nValidation: {result['actions_validation']['valid']}")
        print(f"Valid: {result['actions_validation']['valid_count']}/{result['actions_validation']['total']}")
        
        if not result['actions_validation']['valid']:
            print("\n⚠️ Errors found:")
            for error in result['actions_validation']['errors']:
                print(f"  - {error}")
        
        print(f"\nStructured Output (first 500 chars):")
        output = json.dumps(result, ensure_ascii=False, indent=2)
        print(output[:500] + "...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
