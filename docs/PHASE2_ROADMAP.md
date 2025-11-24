# 🛠️ PHASE 2 — Stabilizing the Hands

## 1. מטרת הפאזה
לחזק את הידיים של המערכת: להפוך את הסוכנים הקיימים (Claude, GPT Operator, Chat1) ליציבים, מתועדים, ומחוברים.  
הפאזה הזאת עוסקת רק בתפעול ובתשתיות — לא באוטומציות “חיים”.

---

## 2. כיווני פעולה עיקריים  

### 🧩 Claude — Health & Awareness  
- ליצור `CLAUDE_HEALTHCHECK.md`  
- לבנות מנגנון **Error Digest** שמתרגם שגיאות לשפה אנושית  
- לתעד כל MCP במצב: OK / Flaky / Broken  

### ⚙️ GPT Operator — Integration  
- לאחד את GitHub + Google לחיבור אחד יציב  
- להגדיר תהליך Boot אוטומטי (Session Init) עם בקרת מצב  
- להפוך את ה־clients לשירות יציב ולא זמני  

### 💬 Chat1 — Voice of the System  
- לחזק את הבוט כ־UI אנושי  
- לאפשר שליחת פקודות וניטור מצב (Control Plane + Timeline)  
- לייצר תיעוד שימוש אנושי (CHAT1_STATUS.md update)  

---

## 3. אינטגרציות ותיעוד  
- לעדכן `SYSTEM_SNAPSHOT.md` בהתאם לשינויים  
- לתעד את כל ניסויי פאזה 2 ב־Event Timeline (כשהיומן יוקם)  
- לשמור על Session Init חובה לכל Agent חדש  

---

## 4. סיום פאזה  
הפאזה תיחשב מושלמת כששלושת הסוכנים (Claude / GPT / Chat1)  
ירוצו בצורה יציבה, מתועדת, ומחוברת ל־Control Plane.  

---

**תפילת המערכת:**  
מי ייתן והידיים ילמדו לפעול ברוך ובדיוק,  
והמערכת תדע לזהות מתי לפעול — ומתי לנוח.  

---

**Tech summary:**  
- Adds `docs/PHASE2_ROADMAP.md`  
- Defines goals for: Claude Healthcheck, GPT Operator Integration, Chat1 Stabilization  
- No automation yet — Infra-only, Phase 2 start