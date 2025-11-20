# Agents Inventory – מלאי סוכני המערכת

מסמך זה מפרט את כל הסוכנים שזוהו בריפו הישן `make-ops-clean` ומספק המלצות למיקום במערכת החדשה `ai-os`.

**תאריך יצירה**: 20 נובמבר 2025  
**מבוסס על**: `docs/REPO_AUDIT_make-ops-clean.md` + סקירה ישירה של הריפו הישן

---

## טבלת סוכנים

| AgentName | OldPath | Role | StatusFromAudit | SuggestedRoleInAIOS | Notes |
|-----------|---------|------|-----------------|---------------------|-------|
| **Local Execution Agent** | `agents/local_execution_agent.py` | ביצוע פעולות מקומיות על המחשב (קובץ placeholder בסיסי) | זהב | סוכן עזר / Archive | הקובץ מכיל רק הדפסת Hello World. דורש החלטה: האם זה היה מתוכנן לפיתוח עתידי או שרק placeholder? |
| **GPT GitHub Agent** | `gpt_agent/github_agent.py` | מתכנן משימות GitHub ומנתח אינטנט המשתמש לפי CAPABILITIES_MATRIX. פועל במצב DRY RUN. | זהב | סוכן ליבה | זהו סוכן מתוחכם שמתכנן פעולות על בסיס מסמכי DESIGN ו-CAPABILITIES_MATRIX. מומלץ לייבא ולפתח עוד. |
| **MCP Master Control Program** | `mcp/` (כל התיקייה) | הלב של המערכת: ניהול סוכנים, תזמון, אינטגרציות (GitHub, Google), ו-API server | זהב | Workflow Engine / סוכן ליבה | מכיל clients, servers ו-integrations. זהו ה"מוח" של מערכת הסוכנים. דורש פירוק לרכיבים: `mcp/server/` → workflows/, `mcp/clients/` → tools/ |
| **GitHub Executor API** | `mcp/server/worker/` + תיעוד ב-CAPABILITIES_MATRIX | API אוטומציה של GitHub (קוד מלא, deployment חסום) | זהב (מתוכנן) | כלי / API Wrapper | לפי CAPABILITIES_MATRIX זה קוד מוכן שמחכה ל-deployment. מומלץ להעביר ל-`tools/` עם תיעוד מלא. |
| **Autopilot / Self-Healing Agent** | `autopilot.py` + `autopilot-state.json` | סוכן החלמה עצמית (Self-Healing) - מנסה לשחזר גישה ל-Google Sheets | ניסוי/ישן | Archive / סוכן עזר | נראה כ-POC של מנגנון החלמה. דורש החלטה: האם רלוונטי עדיין? |
| **OPS Decision Manager** | `ops/decisions/` | ניהול החלטות תפעוליות (ADRs - Architectural Decision Records) | זהב | Workflow Component | מכיל קבצי החלטה כמו `2025-11-02-L2-approval.md`. מתאים ל-`workflows/` או `docs/decisions/` |
| **OPS Diagnostics** | `ops/diag/` | כלי אבחון ובדיקות מערכת | זהב | Workflow Component | מכיל `cloudshell_check.md`, `REMOTE_MCP_EVIDENCE.md` וכו'. מתאים ל-`workflows/diagnostics/` |
| **GitHub Executor Bootstrap** | `ops/TRIGGERS/github_executor_bootstrap.md` | מסמך bootstrap להפעלת GitHub Executor | זהב | Workflow Documentation | תיעוד טריגרים והפעלה - מתאים ל-`workflows/` |

---

## סיכום ממצאים

### סוכנים שזוהו בבירור:
1. **GPT GitHub Agent** – סוכן ליבה מתוחכם (מתכנן משימות)
2. **MCP** – תשתית/מנוע ניהול מרכזי (לא סוכן בודד אלא מערכת)
3. **GitHub Executor API** – כלי אוטומציה (API wrapper)
4. **Autopilot** – סוכן החלמה עצמית (נראה POC)
5. **Local Execution Agent** – placeholder / לא מפותח

### רכיבים תפעוליים (לא בהכרח "סוכנים" אלא תהליכים):
- **OPS/decisions** – מנהל החלטות
- **OPS/diag** – כלי אבחון
- **OPS/TRIGGERS** – מנגנוני הפעלה

---

## דברים שדורשים החלטה אנושית

1. **Local Execution Agent**: האם זה היה אמור להיות סוכן אמיתי או סתם placeholder? צריך להחליט אם לזרוק או לפתח.

2. **MCP Structure**: התיקייה `mcp/` ענקית ומכילה שרתים, לקוחות ואינטגרציות. צריך לפרק אותה לרכיבים:
   - `mcp/server/` → `workflows/mcp-server/`
   - `mcp/clients/` → `tools/mcp-clients/`
   - `mcp/github/`, `mcp/google/` → `tools/integrations/`

3. **Autopilot Status**: האם מנגנון ההחלמה העצמית עדיין רלוונטי? אם כן - צריך לשדרג ולתעד. אם לא - לארכב.

4. **OPS Components**: האם `ops/` הוא חלק ממערכת הסוכנים או רק כלי תפעול תומך? יש צורך בהבחנה ברורה.

5. **GitHub Executor API**: קוד מוכן שמחכה ל-deployment. צריך להחליט:
   - האם לייבא כמו שהוא?
   - האם לשלב במערכת MCP?
   - האם להפוך לכלי עצמאי ב-`tools/`?

---

## המלצות צעד הבא

1. **להתחיל עם GPT GitHub Agent**:
   - לייבא את `gpt_agent/github_agent.py` → `agents/gpt-github-agent/`
   - לייבא את מסמכי התיעוד הנלווים (AGENT_GPT_MASTER_DESIGN.md וכו')
   - ליצור README.md בתיקייה שמסביר תפקיד, dependencies והרצה

2. **לתעד את MCP כ-Workflow Engine**:
   - ליצור `workflows/MCP_OVERVIEW.md`
   - להחליט על פירוק לרכיבים

3. **להעביר את GitHub Executor API ל-tools/**:
   - ליצור `tools/github-executor-api/`
   - לתעד deployment requirements

4. **לארכב את Autopilot**:
   - להעביר ל-`archive/autopilot/` אלא אם יש החלטה אחרת

---

**סטטוס**: ✅ מיפוי ראשוני הושלם  
**צעד הבא**: אישור אנושי להמלצות + ייבוא הסוכן הראשון
