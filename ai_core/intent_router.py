"""
Intent Router v1.0 - High-level orchestration layer

This module provides the entry point for routing raw user intents
into structured plans via GPT Planner.

Status: IMPLEMENTED v1.0
- Structured output from GPT Planner (JSON)
- Parses into clean dict with all required fields
- Foundation for future execution
"""

from typing import Dict, Any, List
from ai_core.gpt_orchestrator import plan_change


def route_intent(intent_text: str) -> Dict[str, Any]:
    """
    High-level entry point for routing a raw intent string
    into a structured GPT plan.
    
    Args:
        intent_text: Raw user intent (Hebrew/English)
                    Example: "אני רוצה ליצור workflow חדש לניהול טוקנים"
    
    Returns:
        Structured plan as a Python dict.
        
        Format (v1.0):
        {
            "intent": str,                # Original intent
            "summary": str,               # What GPT understood (1-3 sentences)
            "context": str,               # Relevant SSOT context (2-4 sentences)
            "steps": List[str],           # Step-by-step plan
            "actions_for_claude": List[str],  # Technical actions
            "decisions_for_or": List[str],    # What Or needs to approve
            "version": str                # Router version
        }
    
    Example:
        >>> result = route_intent("צור workflow חדש לגיבוי")
        >>> print(result["summary"])
        "אור רוצה workflow חדש (WF-004) לגיבוי אוטומטי של הריפו."
        >>> print(result["steps"])
        ["צור קובץ workflows/BACKUP_AUTOMATION.md", ...]
    """
    # Call GPT Planner to generate structured plan
    plan_dict = plan_change(intent_text)
    
    # Validate required keys exist
    required_keys = ["summary", "context", "steps", "actions_for_claude", "decisions_for_or"]
    for key in required_keys:
        if key not in plan_dict:
            plan_dict[key] = f"[Missing {key}]"
    
    # Ensure lists are lists
    if not isinstance(plan_dict.get("steps"), list):
        plan_dict["steps"] = [str(plan_dict.get("steps", ""))]
    if not isinstance(plan_dict.get("actions_for_claude"), list):
        plan_dict["actions_for_claude"] = [str(plan_dict.get("actions_for_claude", ""))]
    if not isinstance(plan_dict.get("decisions_for_or"), list):
        plan_dict["decisions_for_or"] = [str(plan_dict.get("decisions_for_or", ""))]
    
    # Add metadata
    plan_dict["intent"] = intent_text
    plan_dict["version"] = "1.0"
    
    return plan_dict


# Convenience aliases for different entry points
def process_intent(intent_text: str) -> Dict[str, Any]:
    """Alias for route_intent - same functionality"""
    return route_intent(intent_text)


def quick_summary(intent_text: str) -> str:
    """
    Quick access to just the summary (what GPT understood).
    
    Useful for debugging or quick checks.
    
    Returns:
        str: The summary from GPT Planner
    """
    result = route_intent(intent_text)
    return result["summary"]


def get_claude_actions(intent_text: str) -> List[str]:
    """
    Quick access to Claude's action list.
    
    Useful for execution planning.
    
    Returns:
        List[str]: Actions for Claude to execute
    """
    result = route_intent(intent_text)
    return result["actions_for_claude"]


if __name__ == "__main__":
    import sys
    import json
    
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    
    # Simple smoke test
    print("Intent Router v1.0 - Smoke Test")
    print("=" * 50)
    
    test_intent = "אני רוצה ליצור workflow חדש לניהול טוקנים"
    print(f"\nIntent: {test_intent}")
    print("-" * 50)
    
    try:
        result = route_intent(test_intent)
        print(f"\n✅ Success! Version: {result['version']}")
        print(f"\nStructured Output:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
