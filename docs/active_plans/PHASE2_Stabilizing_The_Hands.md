# 🤖 Phase 2 – Stabilizing the Hands

**Status:** Active
**Scope:** Core Infrastructure & Execution Reliability
**Owner:** Or (System Architect & Human Supervisor)
**Agents Involved:** GPT Operator, Claude Desktop, Chat1 (Telegram), Make (later phase)

---

## 🎯 Objective
לאחד ולייצב את שכבת ה"ידיים" של המערכת – כל הסוכנים המבצעים (Claude, GPT Operator, Chat1) צריכים לפעול באופן מתואם, מתועד, ומבוקר.

מטרת הפאזה היא להבטיח שכל פעולה שמתבצעת בריפו, בגוגל, או דרך Chat1 – תהיה:
- מתועדת ב־Source of Truth (GitHub)
- מאושרת מראש על ידי Or
- שקופה ומובנת לכל הסוכנים האחרים

---

## 🧩 Sub-Phases & Tasks

### Phase 2.1 – Full Agent Sync (✅ Completed)
- עדכון כל הקבצים שקשורים להרשאות, אחריות, וחיבור בין סוכנים.
- חיבור סקריפטים (hooks) לתוך Control Plane.
- הבטחת סנכרון בין Claude ↔ GPT ↔ Chat1.

### Phase 2.2 – Claude Healthcheck & Error Digest (🚧 In Progress)
**מטרה:** להפוך את קלוד לכלי שמבצע ניטור עצמי ומדווח במבנה ברור.

**משימות:**
- ליצור `docs/CLAUDE_HEALTHCHECK_SPEC.md` – תיאור מבנה הדוח (OK / Flaky / Broken).
- להוסיף סעיף ב־`SESSION_INIT_CHECKLIST.md` שמזכיר להריץ Healthcheck בתחילת סשן.
- לעדכן את `CONTROL_PLANE_SPEC.md` עם שדה מצב בריאות (`claude_status`).

### Phase 2.3 – Chat1 Stabilization (🔜 Next)
- לוודא יציבות של Chat1 (טלגרם) עם webhook קבוע או ngrok יציב.
- לתעד בתיקייה `docs/chat1/` את כל הגדרות ה־env וההרצה.
- להוסיף ב־Control Plane מעקב אחר מצב Chat1 (`chat1_status`).

---

## 🧠 Notes
- הפאזה הזו היא חלק מ־Route Recalculation.
- כל פעולה בה נעשית תחת עקרונות: DRY, SSOT, Human-in-the-loop.
- אחרי השלמת Phase 2, המערכת תעבור ל־Phase 3 – Google Stabilization.

---

**Tech Summary:**
- Adds `docs/active_plans/PHASE2_Stabilizing_The_Hands.md` (active plan)
- Defines current scope, tasks, and responsible agents
- Status: `Phase 2.2 – In Progress`