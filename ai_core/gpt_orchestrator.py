import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# הגדרה: היכן הריפו יושב
REPO_ROOT = Path(__file__).resolve().parents[1]

# מסמכי SSOT שנקרא מהם
SSOT_FILES = [
    REPO_ROOT / "docs" / "CONSTITUTION.md",
    REPO_ROOT / "docs" / "SYSTEM_SNAPSHOT.md",
    REPO_ROOT / "docs" / "CAPABILITIES_MATRIX.md",
    REPO_ROOT / "docs" / "DECISIONS_AI_OS.md",
    REPO_ROOT / "docs" / "AGENT_ONBOARDING.md",
    REPO_ROOT / "docs" / "ACTION_EXECUTION_SCHEMA.md",
    REPO_ROOT / "policies" / "HUMAN_TECH_INTERACTION_POLICY.md",
    REPO_ROOT / "policies" / "SECURITY_SECRETS_POLICY.md",
]

def load_ssot_context(max_chars: int = 24000) -> str:
    """קורא את מסמכי ה-SSOT ומחזיר אותם כמחרוזת אחת (חתוכה אם צריך)."""
    parts = []
    for path in SSOT_FILES:
        if path.exists():
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            parts.append(f"# FILE: {path.relative_to(REPO_ROOT)}\n\n{text}\n\n")
    full = "\n\n".join(parts)
    if len(full) > max_chars:
        return full[:max_chars] + "\n\n[TRUNCATED...]"
    return full

def get_client() -> "OpenAI":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in environment")
    return OpenAI(api_key=api_key)

def plan_change(intent: str) -> dict:
    """
    לוקח כוונה טקסטואלית (intent) ומחזיר תכנית פעולה מובנית,
    לפי ה-SSOT והמדיניות (אור לא עושה טכני).
    
    Returns:
        dict with keys:
        - summary: str (מה הבנתי מהכוונה)
        - context: str (הקשר מ-SSOT)
        - steps: List[str] (תכנית צעד-צעד)
        - actions_for_claude: List[Action] (פעולות טכניות מובנות)
        - decisions_for_or: List[str] (מה אור מאשר)
    """
    client = get_client()
    context = load_ssot_context()

    system_prompt = """
    אתה פועל בתור GPT Orchestrator עבור פרויקט בשם ai-os.

    חוקים מרכזיים:
    - אור (המשתמש) לא מבצע עבודה טכנית.
    - אתה רק מתכנן ומשיב, לא מריץ קוד.
    - תכבד את המדיניות ב-HUMAN_TECH_INTERACTION_POLICY.md ו-SECURITY_SECRETS_POLICY.md.
    - אם משהו דורש פעולה טכנית, הצע כיצד Claude / סוכנים אחרים יבצעו זאת, לא אור.

    CRITICAL: You MUST respond with valid JSON only. No markdown, no code blocks, just pure JSON.
    
    JSON Format (REQUIRED):
    {
      "summary": "מה הבנתי מהכוונה (1-3 משפטים)",
      "context": "הקשר רלוונטי מתוך ה-SSOT (2-4 משפטים)",
      "steps": [
        "צעד 1: תיאור",
        "צעד 2: תיאור"
      ],
      "actions_for_claude": [
        {
          "type": "file.create | file.update | file.delete | git.commit | git.push | workflow.run | validation.check",
          "params": {
            // Parameters specific to action type (see ACTION_EXECUTION_SCHEMA.md)
          },
          "approval": "auto | manual",
          "description": "תיאור קצר למה הפעולה"
        }
      ],
      "decisions_for_or": [
        "החלטה 1",
        "החלטה 2"
      ]
    }
    
    IMPORTANT: actions_for_claude MUST be structured JSON objects, NOT free text!
    
    Action Types (from ACTION_EXECUTION_SCHEMA.md):
    1. file.create: {"path": "...", "content": "..."}
    2. file.update: {"path": "...", "edits": [{"old_text": "...", "new_text": "..."}]}
    3. file.delete: {"path": "..."} - ALWAYS approval: "manual"
    4. git.commit: {"files": ["..."], "message": "..."}
    5. git.push: {} - no params
    6. workflow.run: {"workflow_id": "WF-00X", "inputs": {...}}
    7. validation.check: {"check_type": "...", "target": "..."}
    
    Approval Rules:
    - "auto": Safe, repeatable operations (create, update, commit, push)
    - "manual": Destructive or critical operations (delete, workflow.run, secrets)
    
    DO NOT include anything except valid JSON in your response.
    DO NOT wrap JSON in markdown code blocks.
    DO NOT use free text for actions_for_claude - ONLY structured JSON objects.
    """

    user_prompt = f"""
    intent (כוונה של אור):
    {intent}

    יש לך גישה לתמצית המסמכים הבאים (SSOT):
    {', '.join(str(p.relative_to(REPO_ROOT)) for p in SSOT_FILES if p.exists())}

    אל תמציא דברים שלא קיימים ב-SSOT.
    הקפד שכל פעולה טכנית משויכת ל-Claude / סוכנים אחרים, לא לאור.
    
    CRITICAL: actions_for_claude MUST be structured JSON (type, params, approval, description).
    See ACTION_EXECUTION_SCHEMA.md for exact format.
    
    RESPOND WITH VALID JSON ONLY.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "user", "content": f"SSOT snapshot:\n\n{context}"},
        ],
    )

    # Parse JSON response
    import json
    response_text = response.choices[0].message.content.strip()
    
    # Remove markdown code blocks if present (safety fallback)
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1])  # Remove first and last line
    
    try:
        plan_dict = json.loads(response_text)
        return plan_dict
    except json.JSONDecodeError as e:
        # Fallback: return error in structured format
        return {
            "summary": f"שגיאה בפרסור: {str(e)}",
            "context": "GPT לא החזיר JSON תקין",
            "steps": [response_text],
            "actions_for_claude": [],
            "decisions_for_or": ["בדוק את התשובה ידנית"]
        }

if __name__ == "__main__":
    import sys
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    
    # דוגמת הרצה בסיסית
    example_intent = "צור קובץ README.md פשוט עם הסבר על הפרויקט"
    plan = plan_change(example_intent)
    import json
    print(json.dumps(plan, ensure_ascii=False, indent=2))
