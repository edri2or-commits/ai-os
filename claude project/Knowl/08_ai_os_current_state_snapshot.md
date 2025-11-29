בגדול: **לא מחליפים Truth Layer סטטי ב”דינמי” — בונים “Dual Truth”**. הסטטי נשאר *חוק/כוונה/מדיניות* (Audit + Git), והדינמי הוא *Observed Reality* (probe אמיתי). ביניהם יש **Reconciliation Loop** שמייצר *Change Requests* ורק אז (ובגבולות בטיחות) עושה שינוי.

### למה זה חשוב אצלך *עכשיו* (לפי תמונת המצב)
- אתה כבר חי את הכאב: יש **drift בין Git HEAD (d12cd61) לבין truth last_commit (43b308a)**. זה בדיוק “Split Brain”.
- המערכת ב־**INFRA_ONLY + sandbox_only + automations_enabled=false** ⇒ זה זמן מושלם להתחיל **Observer Read-Only** בלי לסכן כלום.

---

## מודל מוצע: 3 שכבות אמת (הכי פרקטי, הכי “ADHD-friendly”)
1) **Truth/Policy (סטטי, בגיט)**  
   DEC, governance, “מה מותר/אסור”, תצורת שירותים רצויה.
2) **Observed State (דינמי, נמדד)**  
   מה באמת רץ עכשיו (Git HEAD אמיתי, פורטים, זמינות שירותים, ngrok URL, n8n health…).
3) **Reconciliation Ledger (אירועים + CRs)**  
   “מצאתי פער X → הצעה לתיקון Y → אושר/נדחה → יושם/נכשל”.

התוצר: אתה מפסיק “לזכור” דברים בראש. אתה רק מאשר/דוחה CRs.

---

## תוצר קטן שאפשר להדביק: סכמת Observed + ChangeRequest
```json
// docs/system_state/observed/OBSERVED_STATE.json
{
  "observed_at_utc": "2025-11-29T12:00:00Z",
  "git": { "head_short": "d12cd61", "branch": "main" },
  "services": [
    { "name": "n8n", "expected": "up", "observed": "up", "endpoint": "http://localhost:5678" },
    { "name": "mcp_github_client", "expected": "up", "observed": "partial", "port": 8081 }
  ],
  "invariants": [
    { "id": "INV_GIT_TRUTH_MATCH", "status": "FAIL", "details": "truth=43b308a observed=d12cd61" }
  ]
}
```

```json
// docs/system_state/changes/CR_*.json
{
  "cr_id": "CR_2025-11-29_001",
  "created_at_utc": "2025-11-29T12:02:00Z",
  "type": "TRUTH_RECONCILIATION",
  "risk": "low",
  "proposal": [
    { "op": "update_json", "path": "docs/system_state/SYSTEM_STATE_COMPACT.json", "json_path": "$.git_status.last_commit", "value": "d12cd61" },
    { "op": "append_event", "path": "docs/system_state/timeline/EVENT_TIMELINE.jsonl", "event_type": "DRIFT_RECONCILED" }
  ],
  "requires_human_approval": true
}
```

---

## “Phase 2.4” שאתה יכול לעשות מחר בבוקר (בלי להפוך את העולם)
### 1) Read-Only Observer (0 סיכון)
מטרה: כל 10–30 דקות לכתוב **OBSERVED_STATE.json + EVT_DRIFT_DETECTED** אם יש פערים.

Probe מינימלי שמחזיר הכי הרבה ערך:
- Git: HEAD short + branch
- Services: n8n health, ports 8081/8082/5678, ngrok url (אם יש)
- Truth: last_commit מה־SYSTEM_STATE_COMPACT + GOVERNANCE_LATEST
- פערים: Git/Truth mismatch, service expected≠observed

### 2) Fitness Metric חדש: `FITNESS_003_DRIFT`
- `drift_git_truth = 0/1`
- `drift_services_count`
- `time_since_last_observed_probe_minutes`

### 3) Reconciliation רק כ-CR (לא Auto-Fix)
בשלב הזה אתה עדיין “הבוס”: המערכת *מציעה* שינוי, לא עושה.

---

## קוד שלד קצר (Python) ל־drift detector + כתיבת EVT
```python
import json, time, pathlib
from datetime import datetime, timezone

ROOT = pathlib.Path(".")
STATE = ROOT / "docs/system_state/SYSTEM_STATE_COMPACT.json"
GOV = ROOT / "governance/snapshots/GOVERNANCE_LATEST.json"
OBS = ROOT / "docs/system_state/observed/OBSERVED_STATE.json"
EVT = ROOT / "docs/system_state/timeline/EVENT_TIMELINE.jsonl"

def read_json(p): return json.loads(p.read_text(encoding="utf-8"))

def get_git_head_short():
    # fallback שמסתמך על קריאת קבצי .git (כמו שאתה כבר עושה)
    head = (ROOT / ".git/HEAD").read_text().strip()
    if head.startswith("ref:"):
        ref = head.split(" ", 1)[1].strip()
        sha = (ROOT / ".git" / ref).read_text().strip()
    else:
        sha = head
    return sha[:7]

def append_event(event_type, payload):
    evt = {"ts_utc": datetime.now(timezone.utc).isoformat(), "type": event_type, "payload": payload}
    EVT.parent.mkdir(parents=True, exist_ok=True)
    with EVT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(evt, ensure_ascii=False) + "\n")

def main():
    sys_state = read_json(STATE)
    gov = read_json(GOV)
    observed_head = get_git_head_short()
    truth_commit = sys_state.get("git_status", {}).get("last_commit") or gov.get("git", {}).get("last_commit")

    invariants = []
    if truth_commit and truth_commit[:7] != observed_head:
        invariants.append({"id":"INV_GIT_TRUTH_MATCH","status":"FAIL","details":f"truth={truth_commit} observed={observed_head}"})
    else:
        invariants.append({"id":"INV_GIT_TRUTH_MATCH","status":"PASS","details":"ok"})

    observed = {
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "git": {"head_short": observed_head, "branch": sys_state.get("branch","unknown")},
        "services": [],
        "invariants": invariants
    }
    OBS.parent.mkdir(parents=True, exist_ok=True)
    OBS.write_text(json.dumps(observed, ensure_ascii=False, indent=2), encoding="utf-8")

    if any(x["status"] == "FAIL" for x in invariants):
        append_event("DRIFT_DETECTED", {"invariants": invariants})

if __name__ == "__main__":
    main()
```

---

## ההחלטה האדריכלית בשורה אחת
**Static Truth = חוזה/מדיניות. Dynamic Truth = מדידה. Reconciliation = CR מאושר.**  
זה נותן לך *Offload אמיתי* בלי להפוך את המערכת למסוכנת.

אם תרצה, אני יכול להפוך את זה ל־**ADR קצר** בסגנון repo שלך (DEC/ADR), כולל “Accept/Reject Criteria” ל־Phase 2.4—אבל גם בלי זה, שלושת הקבצים למעלה (Observed/CR/Event) כבר נותנים לך “Autonomic בסיסי” עם 0 כתיבה אוטומטית.
