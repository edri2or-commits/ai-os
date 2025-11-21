import os
from pathlib import Path
from openai import OpenAI

# הגדרה: היכן הריפו יושב
REPO_ROOT = Path(__file__).resolve().parents[1]

# מסמכי SSOT שנקרא מהם
SSOT_FILES = [
    REPO_ROOT / "docs" / "CONSTITUTION.md",
    REPO_ROOT / "docs" / "SYSTEM_SNAPSHOT.md",
    REPO_ROOT / "docs" / "CAPABILITIES_MATRIX.md",
    REPO_ROOT / "docs" / "DECISIONS_AI_OS.md",
    REPO_ROOT / "docs" / "AGENT_ONBOARDING.md",
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

def plan_change(intent: str) -> str:
    """
    לוקח כוונה טקסטואלית (intent) ומחזיר תכנית פעולה מילולית,
    לפי ה-SSOT והמדיניות (אור לא עושה טכני).
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

    פורמט תשובה:
    1. מה הבנתי מהכוונה
    2. הקשר רלוונטי מתוך ה-SSOT (בקצרה)
    3. תכנית פעולה צעד-צעד (ללא קוד ריצה, רק תיאור)
    4. מה צריך Claude לעשות בפועל (פעולות טכניות)
    5. מה אור צריך רק לאשר / להחליט
    """

    user_prompt = f"""
    intent (כוונה של אור):
    {intent}

    יש לך גישה לתמצית המסמכים הבאים (SSOT):
    {', '.join(str(p.relative_to(REPO_ROOT)) for p in SSOT_FILES if p.exists())}

    אל תמציא דברים שלא קיימים ב-SSOT.
    הקפד שכל פעולה טכנית משויכת ל-Claude / סוכנים אחרים, לא לאור.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "user", "content": f"SSOT snapshot:\n\n{context}"},
        ],
    )

    # פענוח פשוט של הטקסט מהתשובה
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    import sys
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    
    # דוגמת הרצה בסיסית
    example_intent = "לעדכן את SYSTEM_SNAPSHOT כך שישקף את המדיניות HUMAN_TECH_INTERACTION_POLICY החדשה."
    plan = plan_change(example_intent)
    print(plan)
