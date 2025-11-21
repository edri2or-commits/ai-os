"""
Intent Router v0.1 - High-level orchestration layer

This module provides the entry point for routing raw user intents
into structured plans via GPT Planner.

Status: IMPLEMENTED v0.1
- Basic wrapping of GPT Planner
- Returns raw plan text (no parsing yet)
- Foundation for future expansion
"""

from typing import Dict, Any
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
        
        Current format (v0.1):
        {
            "raw_plan": str,  # Full plan text from GPT Planner
            "intent": str,    # Original intent for reference
            "version": str    # Router version
        }
        
        Future format (v1.0+):
        {
            "summary": str,              # What GPT understood
            "context": str,              # Relevant SSOT context
            "steps": List[str],          # Step-by-step plan
            "actions_for_claude": List[str],  # Technical actions
            "decisions_for_or": List[str],    # What Or needs to approve
            "intent": str,               # Original intent
            "version": str               # Router version
        }
    
    Example:
        >>> result = route_intent("צור workflow חדש לגיבוי")
        >>> print(result["raw_plan"])
        [GPT Planner's full response...]
    """
    # Call GPT Planner to generate plan
    plan_text = plan_change(intent_text)
    
    # v0.1: Return raw plan with metadata
    # TODO (v1.0): Parse plan_text according to GPT_PLANNER_CONTRACT
    # and extract structured sections:
    # - "1. מה הבנתי מהכוונה:"
    # - "2. הקשר רלוונטי מתוך ה-SSOT:"
    # - "3. תכנית פעולה צעד-צעד:"
    # - "4. מה צריך Claude לעשות בפועל:"
    # - "5. מה אור צריך רק לאשר / להחליט:"
    
    return {
        "raw_plan": plan_text,
        "intent": intent_text,
        "version": "0.1"
    }


# Convenience aliases for different entry points
def process_intent(intent_text: str) -> Dict[str, Any]:
    """Alias for route_intent - same functionality"""
    return route_intent(intent_text)


def quick_plan(intent_text: str) -> str:
    """
    Quick access to just the plan text (no wrapping).
    
    Useful for simple CLI usage or direct inspection.
    
    Returns:
        str: The raw plan text from GPT Planner
    """
    result = route_intent(intent_text)
    return result["raw_plan"]


if __name__ == "__main__":
    import sys
    
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    
    # Simple smoke test
    print("Intent Router v0.1 - Smoke Test")
    print("=" * 50)
    
    test_intent = "אני רוצה ליצור workflow חדש לניהול טוקנים"
    print(f"\nIntent: {test_intent}")
    print("-" * 50)
    
    try:
        result = route_intent(test_intent)
        print(f"\n✅ Success!")
        print(f"Version: {result['version']}")
        print(f"\nPlan preview (first 200 chars):")
        print(result['raw_plan'][:200] + "...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
