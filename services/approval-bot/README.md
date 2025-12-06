# H3 Telegram Approval Bot

**HEADLESS_MIGRATION_ROADMAP Slice H3**

Async Human-in-the-Loop approvals via Telegram. No Claude Desktop required!

---

## 🎯 What It Does

```
Reconciler detects drift
    → Writes CR to truth-layer/drift/approvals/pending/
    → Backend watches directory
    → Sends Telegram notification
    → User clicks [✅ Approve] or [❌ Reject]
    → Backend writes approval file
    → Executor applies CR
    → Git commit
    → Telegram updated: "✅ Applied!"
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd services/approval-bot
pip install -r requirements.txt
```

### 2. Configure (Already done! Using existing .env)

Your `.env` already has:
- `TELEGRAM_BOT_TOKEN=8119131809:AAH...`
- `TELEGRAM_CHAT_ID=5786217215`

### 3. Run

```bash
python backend.py
```

**Output:**
```
✅ Telegram configured: 8119131809...
✅ Chat ID: 5786217215
✅ Database initialized
👁️ Watching: truth-layer/drift/approvals/pending
✅ Approval Bot Running!
```

---

## 🧪 Testing

### Manual Test (Create CR)

```bash
# Create test CR
cat > truth-layer/drift/approvals/pending/CR_TEST_001.yaml << EOF
cr_id: CR_TEST_001
type: TEST
risk: low
proposal:
  - op: test_operation
    description: "Test approval workflow"
EOF
```

**Expected:**
1. Backend detects file (< 1 sec)
2. Telegram message received (< 5 sec):
   ```
   🔔 Change Request Approval
   
   ID: CR_TEST_001
   Type: TEST
   Risk: low
   
   [✅ Approve] [❌ Reject] [📄 View Full]
   ```
3. Click ✅ Approve
4. File created: `truth-layer/drift/approvals/approved/CR_TEST_001_APPROVED.json`
5. Telegram message updated: "✅ Approved! Executor will process..."

---

## 📁 Directory Structure

```
truth-layer/drift/approvals/
├── pending/         ← Reconciler writes CRs here
├── approved/        ← Bot writes APPROVED files here (Executor reads)
└── rejected/        ← Bot writes REJECTED files here
```

---

## 🔒 Security

- **Chat ID Whitelist:** Only `TELEGRAM_CHAT_ID` can approve
- **Audit Trail:** All approvals logged in SQLite
- **Git History:** Approval files committed to Git
- **Privacy Mode:** Bot configured via @BotFather (Privacy: Enabled)

---

## 🐛 Troubleshooting

### Bot not receiving messages

```bash
# Check token
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('TELEGRAM_BOT_TOKEN'))"
```

### File watcher not triggering

```bash
# Check directory exists
ls truth-layer/drift/approvals/pending

# Check permissions
icacls truth-layer\drift\approvals\pending
```

### Database locked

```bash
# Stop backend
# Delete database
rm services/approval-bot/approvals.db
# Restart backend (will recreate)
```

---

## 🔗 Integration

### Reconciler Integration

Update Reconciler to write CRs to `pending/`:

```python
# In reconciler.py
cr_file = Path("truth-layer/drift/approvals/pending") / f"{cr_id}.yaml"
with open(cr_file, 'w') as f:
    yaml.dump(cr_data, f)
```

### Executor Integration

Add file watcher to Executor:

```python
# In executor.py
from watchdog.observers import Observer

def on_approval_file_created(event):
    if event.src_path.endswith('_APPROVED.json'):
        cr_id = Path(event.src_path).stem.replace('_APPROVED', '')
        apply_cr(cr_id)
```

---

## 📊 Database Schema

```sql
CREATE TABLE approvals (
    cr_id TEXT PRIMARY KEY,
    type TEXT,
    risk TEXT,
    proposal TEXT,           -- JSON array
    status TEXT,             -- PENDING, APPROVED, REJECTED
    created_at TEXT,
    updated_at TEXT,
    telegram_message_id INTEGER
)
```

---

## 🎉 Definition of Done

- [x] Backend watches pending/ directory
- [x] Telegram notifications sent
- [x] Inline buttons work (Approve/Reject/Diff)
- [x] Approval files written to approved/
- [ ] Executor integration (next step)
- [ ] E2E test (Observer → Reconciler → Telegram → Executor)

---

**Status:** Phase 2.1 Complete ✅  
**Next:** Phase 2.2 - Bot UI Adaptation (optional - backend is standalone)  
**Duration:** ~20 min  
**Git:** Pending commit
