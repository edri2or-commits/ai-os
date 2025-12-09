# Gmail Cleanup Tool

**Purpose:** Automatically clean up Gmail storage to resolve the "28-day warning" by archiving old emails and backing up large attachments to Google Drive.

## 📋 Strategy

### Tier 1: Safe Auto-Archive
- **Query:** `older_than:1y AND (category:promotions OR category:social)`
- **Action:** Archive only (remove from Inbox, NOT delete)
- **Risk:** ZERO (easily reversible)
- **Expected:** 100-500 emails

### Tier 2: Download & Delete
- **Query:** `larger:10M has:attachment`
- **Action:** Download → Upload to Drive → Delete from Gmail
- **Risk:** LOW (backup exists in Google Drive)
- **Expected:** 500MB-2GB freed

### Tier 3: Manual Review
- **Query:** `larger:5M is:important`
- **Action:** Show list → User decides
- **Risk:** ZERO (user approves each)

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd C:\Users\edri2\Desktop\AI\ai-os\tools
pip install -r gmail_cleanup_requirements.txt --break-system-packages
```

### Step 2: Get Google API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project (or use existing)
3. Enable Gmail API and Google Drive API
4. Create OAuth 2.0 Client ID:
   - Application type: **Desktop app**
   - Name: `Gmail Cleanup Tool`
5. Download the JSON file
6. Rename to `client_secrets.json`
7. Place in: `C:\Users\edri2\Desktop\AI\ai-os\tools\client_secrets.json`

### Step 3: Run Setup (First Time Only)

```bash
python gmail_cleanup_setup.py
```

This will:
- Open browser for OAuth authorization
- Save credentials to `~/.credentials/gmail_cleanup_token.json`

### Step 4: Run Cleanup

**Dry Run (Recommended First):**
```bash
python gmail_cleanup.py --dry-run
```

**Live Run:**
```bash
python gmail_cleanup.py
```

## 📊 Output

### Reports
- Location: `C:\Users\edri2\Desktop\AI\gmail-archive\YYYY-MM-DD\`
- Format: `cleanup_report_YYYYMMDD_HHMMSS.yaml`

### Backed Up Files
- Google Drive folder: `/Gmail Archive/`
- Each run creates timestamped subfolder

## 🔒 Safety Features

1. **HITL Approval Gates:** User must type 'yes' before each tier executes
2. **Dry Run Mode:** Test without making changes
3. **Pre-flight Checks:** Validates API access, disk space, directory creation
4. **Full Reversibility:**
   - Tier 1: Archived emails can be restored from All Mail
   - Tier 2: Attachments backed up to Drive before deletion
   - Tier 3: No auto-deletion of important messages

## ⚠️ Important Notes

- **Gmail quota:** 8.45GB (out of 2TB total)
- **Google One:** 2TB plan with ~1440GB free
- **First run:** Start with `--dry-run` to see what will be affected
- **Approval required:** Each tier requires user confirmation

## 🛠️ Troubleshooting

### "Authentication required"
Run `python gmail_cleanup_setup.py` again

### "Gmail API not working"
1. Check that Gmail API is enabled in Google Cloud Console
2. Verify client_secrets.json is in the correct location

### "Low disk space"
- Script requires min 2GB free space on C:\
- Temporary files are created during upload to Drive

## 📈 Expected Results

Based on initial scan:
- **Tier 1:** ~200-500 promotional emails
- **Tier 2:** 5-10 large messages (21MB, 7MB, 6.4MB attachments)
- **Total freed:** 500MB-2GB

## 🔄 Next Steps

After successful cleanup:
1. Check Gmail storage at [one.google.com/storage](https://one.google.com/storage)
2. Verify 28-day warning is resolved
3. Schedule monthly cleanup (optional)
4. Review Tier 3 important messages manually in Gmail
