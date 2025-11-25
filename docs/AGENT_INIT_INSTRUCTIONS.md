# 🧭 System Initialization Instructions (AI-OS Family Protocol)

## 1. התחברות לריפו
קרא את הקבצים הקריטיים הבאים בריפו `edri2or-commits/ai-os`:
- `docs/CONSTITUTION.md`
- `docs/SYSTEM_SNAPSHOT.md`
- `docs/DECISIONS_AI_OS.md`
- `docs/SESSION_INIT_CHECKLIST.md`
- `docs/CONTROL_PLANE_SPEC.md`
- `docs/PHASE2_ROADMAP.md`
- כל קובץ בתיקייה `active_plans/` (אם קיימת)

## 2. הבנת המצב הנוכחי של המערכת
- קבע את ה־System Mode מתוך `CONTROL_PLANE_SPEC.md`
- בדוק את מצב הסוכנים: Claude, Chat1, Make, Google
- זהה אם קיימת תוכנית פעילה בתיקיית `active_plans/`. אם כן — טען אותה והגדר את ה־context שלך בהתאם.

## 3. חיול עצמי (Session Init)
- קרא ובצע את השלבים מתוך `SESSION_INIT_CHECKLIST.md`.
- אמת שאתה מסונכרן עם ה־branch `main`.
- ודא שכל שינוי עתידי יתועד כ־commit או כ־PR עם הודעה מפורטת.

## 4. מודעות לפאזות (Phases Awareness)
- בדוק את הקובץ `PHASE2_ROADMAP.md` או את הפאזת הנוכחית שמוגדרת ב־Control Plane.
- הכרז את עצמך כסוכן הפועל במסגרת הפאזה הזו, בהתאם לתפקיד שלך (Operator / Architect / Claude / Chat1 וכו’).

## 5. עקרונות חובה
- אין קוד תלוש: כל סקריפט חדש חייב להיות רשום ב־Control Plane ובתיעוד.
- Human-in-the-loop בלבד — אין אוטומציה לא מאושרת מראש.
- שקיפות מוחלטת: כל פעולה חייבת להופיע ב־commit log או ב־Timeline.

---

**Tech Summary:**
- Adds `docs/AGENT_INIT_INSTRUCTIONS.md`
- Defines unified boot protocol for all Agents
- Ensures every new Chat/Agent can fully initialize context automatically