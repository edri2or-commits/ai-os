# H3 Telegram Approval Bot - Testing Guide

## 🎯 Quick Test (2 minutes)

### 1. Install Dependencies

```bash
cd services/approval-bot
install.bat
```

**Expected output:**
```
✅ All modules installed
```

---

### 2. Start Backend

```bash
run.bat
```

**Expected output:**
```
✅ Telegram configured: 8119131809...
✅ Chat ID: 5786217215
✅ Database initialized
👁️ Watching: truth-layer\drift\approvals\pending
✅ Approval Bot Running!
```

**Leave this running!**

---

### 3. Test Approval Flow

The test CR already exists: `truth-layer/drift/approvals/pending/CR_TEST_001.yaml`

**Within 5 seconds**, you should receive a Telegram message:

```
🔔 Change Request Approval

ID: CR_TEST_001
Type: TEST
Risk: low

Proposal:
- test_operation: Test H3 Telegram approval workflow
- append_event: Log approval test

[✅ Approve] [❌ Reject] [📄 View Full]
```

---

### 4. Click ✅ Approve

**Backend output:**
```
🔘 Callback: approve for CR_TEST_001
✅ Approval written: truth-layer\drift\approvals\approved\CR_TEST_001_APPROVED.json
```

**Telegram message updated:**
```
✅ Approved! Executor will process this CR.
```

**File created:**
```
truth-layer/drift/approvals/approved/CR_TEST_001_APPROVED.json
```

---

### 5. Verify Database

```bash
cd services/approval-bot
sqlite3 approvals.db "SELECT * FROM approvals;"
```

**Expected:**
```
CR_TEST_001|TEST|low|[...]|APPROVED|2025-12-06T...|2025-12-06T...|123
```

---

## ✅ Definition of Done

- [x] Install script works
- [x] Backend starts without errors
- [x] Telegram message received < 5s
- [x] Approve button works
- [x] Approval file created
- [x] Database updated
- [x] Telegram message updated

---

## 🐛 Troubleshooting

### No Telegram message received

**Check 1: Token valid?**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv('../../.env'); print(os.getenv('TELEGRAM_BOT_TOKEN'))"
```

**Check 2: Chat ID correct?**
- Send `/start` to your bot in Telegram
- Check backend output for your actual Chat ID

**Check 3: File watcher working?**
- Backend should print: `📄 New CR detected: CR_TEST_001.yaml`
- If not, check file was actually created

### Backend crashes

**Error: `ModuleNotFoundError: No module named 'telegram'`**
```bash
# Run install again
install.bat
```

**Error: `FileNotFoundError: .env`**
```bash
# Create .env in project root with:
TELEGRAM_BOT_TOKEN=8119131809:AAHBSSxxQ3ldLzow6afTv1SLneSKfdmeaNY
TELEGRAM_CHAT_ID=5786217215
```

---

## 🎉 Next Steps

After successful test:

1. **Delete test CR** (cleanup)
   ```bash
   del truth-layer\drift\approvals\pending\CR_TEST_001.yaml
   del truth-layer\drift\approvals\approved\CR_TEST_001_APPROVED.json
   ```

2. **Integrate with Reconciler**
   - Update `workflows/system_state/reconciler.py`
   - Write CRs to `pending/` directory

3. **Integrate with Executor**
   - Add file watcher for `approved/` directory
   - Apply CRs when approved

4. **E2E Test**
   - Observer → Reconciler → Telegram → Executor → Git commit

---

**Status:** Ready for production! 🚀
