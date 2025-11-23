import sys
import json

sys.path.insert(0, '.')

from ai_core.intent_router import route_intent

intent = """הוסף ל-README סעיף קצר שמסביר שיש עכשיו Intent Router, GPT Planner ו-Action Executor, ושכל שינוי עובר דרכם לפני ביצוע בפועל."""

result = route_intent(intent)

print(json.dumps(result, ensure_ascii=False, indent=2))
