# n8n Observer Workflow - Import Guide

## 📋 Observer Drift Detection Workflow

This workflow automatically runs the Observer every 15 minutes to detect drift in the truth-layer.

---

## 🚀 How to Import

### Step 1: Open n8n UI
1. Open your browser
2. Navigate to: http://localhost:5678
3. If this is your first time:
   - n8n will ask you to create an account (local only, no internet required)
   - Create a username/password (stored locally)

### Step 2: Import Workflow
1. Click on **"Workflows"** in the left sidebar
2. Click the **"+"** button (top right) → **"Import from File"**
3. Select the file: `C:\Users\edri2\Desktop\AI\ai-os\n8n-workflows\observer-drift-detection.json`
4. Click **"Import"**

### Step 3: Activate Workflow
1. The workflow should open automatically after import
2. Click the **"Inactive"** toggle (top right) → It will turn to **"Active"**
3. The workflow will now run every 15 minutes automatically!

---

## 📊 Workflow Structure

```
Schedule Trigger (every 15 min)
    ↓
Run Observer (python observer.py)
    ↓
Check for Drift (exit code == 1?)
    ↓ YES                    ↓ NO
Log Drift Alert       Log Clean State
```

### Nodes:
1. **Schedule Trigger**: Runs every 15 minutes (cron: */15 * * * *)
2. **Run Observer**: Executes `python observer.py` in ai-os directory
3. **Check for Drift**: Checks if Observer exit code is 1 (drift detected)
4. **Log Drift Alert**: Logs message when drift is found
5. **Log Clean State**: Logs message when no drift

---

## ✅ Validation

After activating the workflow:

1. **Check Executions**:
   - Click on **"Executions"** in left sidebar
   - You should see runs appearing every 15 minutes
   - Green = success, Red = error

2. **Manual Test** (optional):
   - Open the workflow
   - Click **"Test Workflow"** (top right)
   - This runs it immediately (doesn't wait 15 minutes)
   - Check the output to see if Observer ran successfully

3. **Check Drift Reports**:
   - If drift is detected, reports appear in: `C:\Users\edri2\Desktop\AI\ai-os\truth-layer\drift\`
   - File format: `YYYY-MM-DD-HHMMSS-drift.yaml`

---

## 🔧 Troubleshooting

### Issue: "Command not found: python"
**Solution:** Edit the "Run Observer" node:
- Change command to: `python3` or full path: `C:\Python314\python.exe`

### Issue: "File not found: observer.py"
**Solution:** Check the working directory (cwd) is set to: `C:\Users\edri2\Desktop\AI\ai-os`

### Issue: Workflow not running automatically
**Solution:** 
- Make sure workflow is **Active** (toggle is green)
- Check n8n container is running: `docker ps | findstr n8n`

---

## 📝 Next Steps (Future Enhancements)

After this works, we can add:
1. **Slack/Discord Notification** - Alert when drift detected
2. **Email Notification** - Send drift report via email
3. **Auto-Reconciler Trigger** - Automatically generate Change Requests
4. **Dashboard Webhook** - Send metrics to monitoring dashboard

---

## 🎯 Success Criteria

✅ Workflow imported successfully  
✅ Workflow is **Active** (green toggle)  
✅ Executions appear every 15 minutes  
✅ Observer runs successfully (green status)  
✅ Drift detection working (exit codes: 0 or 1)  

**Result:** Critical Gap #1 ("Observer Not Scheduled") is now **CLOSED**! 🎉

---

**File:** `n8n-workflows/observer-drift-detection.json`  
**Created:** 2025-12-03  
**AI Life OS Phase 1:** Infrastructure Deployment
