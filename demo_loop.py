"""
Demo: Full LOOP - Intent → Router → Executor → Git

This demonstrates what the complete flow WOULD look like
with a simulated GPT Planner response.
"""

import sys
import json

sys.path.insert(0, '.')

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("DEMO: Full LOOP - Intent → Router → Executor → Git")
print("=" * 70)

# Original intent
intent = """הוסף ל-README סעיף קצר שמסביר שיש עכשיו Intent Router, GPT Planner ו-Action Executor, ושכל שינוי עובר דרכם לפני ביצוע בפועל."""

print(f"\n📝 Intent:\n{intent}")
print("\n" + "-" * 70)

# Simulated plan (this is what GPT Planner WOULD return)
actions = [
    {
        "type": "file.update",
        "params": {
            "path": "README.md",
            "edits": [
                {
                    "old_text": "# AI-OS",
                    "new_text": """# AI-OS

## 🏗️ Architecture

AI-OS operates through a structured pipeline:

1. **Intent Router** - Entry point for user intents (natural language)
2. **GPT Planner** - Converts intents into structured action plans
3. **Action Executor** - Executes validated actions automatically
4. **Git Integration** - Commits and pushes changes to GitHub

Every change flows through this pipeline, ensuring consistency and traceability."""
                }
            ]
        },
        "approval": "auto",
        "description": "הוספת סעיף Architecture ל-README"
    },
    {
        "type": "git.commit",
        "params": {
            "files": ["README.md"],
            "message": "docs: add Architecture section explaining Intent Router flow"
        },
        "approval": "auto",
        "description": "commit של עדכון README"
    },
    {
        "type": "git.push",
        "params": {},
        "approval": "auto",
        "description": "העלאה לגיטהאב"
    }
]

simulated_plan = {
    "intent": intent,
    "summary": "אור רוצה להוסיף סעיף ל-README שמתעד את הארכיטקטורה החדשה: Intent Router, GPT Planner, Action Executor.",
    "context": "README.md קיים. המערכת החדשה כוללת 3 רכיבים מרכזיים שעובדים בתיאום. צריך להוסיף הסבר קצר על התהליך.",
    "steps": [
        "קרא את README.md הנוכחי",
        "הוסף סעיף 'Architecture' או עדכן אותו",
        "הסבר את התהליך: Intent → GPT Planner → Router → Executor",
        "commit עם הודעה תיאורית",
        "push לגיטהאב"
    ],
    "actions_for_claude": actions,
    "decisions_for_or": [
        "האם התוכן של סעיף Architecture מתאים",
        "האם המיקום בתחילת README נכון"
    ],
    "actions_validation": {
        "valid": True,
        "total": 3,
        "valid_count": 3,
        "invalid_count": 0,
        "errors": []
    },
    "version": "2.0"
}

print("\n✅ Plan generated (simulated)")
print(f"\n📋 Summary:\n{simulated_plan['summary']}")
print(f"\n📝 Steps:")
for i, step in enumerate(simulated_plan['steps'], 1):
    print(f"   {i}. {step}")

print(f"\n🔧 Actions for Claude:")
for i, action in enumerate(simulated_plan['actions_for_claude'], 1):
    print(f"   {i}. {action['type']}: {action['description']}")

print(f"\n✅ Validation: {simulated_plan['actions_validation']['valid']}")
print(f"   Valid: {simulated_plan['actions_validation']['valid_count']}/{simulated_plan['actions_validation']['total']}")
print(f"   Errors: {len(simulated_plan['actions_validation']['errors'])}")

# Save plan
with open("demo_plan.json", "w", encoding="utf-8") as f:
    json.dump(simulated_plan, f, ensure_ascii=False, indent=2)

print(f"\n💾 Plan saved to: demo_plan.json")
