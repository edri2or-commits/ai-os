# Task Scheduler Dashboard

**Quick health monitoring for AI-OS automated processes**

## Overview

PowerShell script that displays status of:
- 3 Scheduled Tasks (Observer, Watchdog, Email Watcher)
- 2 Docker containers (n8n, Qdrant)
- Recent drift reports

**Read-only, ADHD-friendly single-pane-of-glass view**

## Usage

### Quick Run
```powershell
cd C:\Users\edri2\Desktop\AI\ai-os\tools
.\dashboard.ps1
```

### Example Output
```
===================================================================
                AI-OS System Dashboard                            
===================================================================

[SCHEDULED TASKS]
-------------------------------------------------------------------
[OK] Observer-Drift-Detection
   Last Run: 2025-12-03 16:04:01 (6 hours ago)
   Next Run: 2025-12-03 22:19:00 (in 13 min)
   Exit Code: 0 (Success)

[OK] Watchdog-Memory-Bank-Ingestion
   Last Run: 2025-12-03 16:07:01 (6 hours ago)
   Next Run: 2025-12-03 22:07:00 (in 1 min)
   Exit Code: 0 (Success)

[OK] \AI-OS\Email Watcher
   Last Run: 2025-12-03 22:00:01 (6 min ago)
   Next Run: 2025-12-03 22:15:00 (in 9 min)
   Exit Code: 0 (Success)

[DOCKER SERVICES]
-------------------------------------------------------------------
[OK] n8n-production
   Status: UP (21 minutes)
   Port: :5678

[OK] qdrant-production
   Status: UP (21 minutes)
   Port: :6333

[DRIFT REPORTS]
-------------------------------------------------------------------
Total Reports: 5
Latest: email-drift-2025-12-03-043629.yaml (2 hours ago)
   Email drift reports: 3
   Other drift reports: 2

===================================================================
[STATUS] ALL SYSTEMS OPERATIONAL
===================================================================
```

## Status Indicators

- **[OK]** - Green - System operational
- **[WARN]** - Yellow - Warning state (task not Ready)
- **[FAIL]** - Red - Failed (non-zero exit code or not found)

## When to Run

**Daily:**
- At start of work session
- After Windows reboot
- If something feels "off"

**After Changes:**
- Deploying new automations
- Modifying Task Scheduler
- Docker restarts

**Troubleshooting:**
- Email Watcher not sending alerts
- Observer not detecting drift
- Watchdog not indexing Memory Bank

## Troubleshooting

### Task Shows [FAIL]
```
[FAIL] Observer-Drift-Detection
   Exit Code: 0x1 (Failed)
```

**Fix:**
1. Check logs: `C:\Users\edri2\Desktop\AI\ai-os\logs\`
2. Run manually: `python tools/observer.py`
3. Check Task Scheduler Event Viewer

### Docker Shows NOT RUNNING
```
[FAIL] Docker Desktop
   Status: NOT RUNNING or not accessible
```

**Fix:**
1. Start Docker Desktop manually
2. Check AutoStart: `Get-Content "$env:APPDATA\Docker\settings-store.json"`
3. Verify containers: `docker ps`

### Task Shows "Task not found"
```
[FAIL] Email Watcher
   Error: Task not found
```

**Fix:**
1. Verify task exists: `Get-ScheduledTask | Where-Object {$_.TaskName -like "*Email*"}`
2. Check task path (may be in `\AI-OS\` folder)
3. Re-create if needed: See `tools/email_watcher_task.xml`

## Technical Details

**Read-Only Operations:**
- `Get-ScheduledTask` (Task Scheduler)
- `Get-ScheduledTaskInfo` (Task details)
- `docker ps` (Container status)
- `Get-ChildItem` (Drift reports count)

**No Changes Made:**
- Does not modify tasks
- Does not start/stop services
- Does not write files

**Performance:**
- Runtime: ~5-10 seconds
- No network calls
- Minimal CPU/memory usage

## Integration

**Manual Monitoring:**
Run whenever you need system health overview

**Future (Optional):**
- Add to Task Scheduler (run every hour)
- Save output to log file
- Send Telegram alert if issues detected
- HTML dashboard version

## Files

- **dashboard.ps1** - Main script (264 lines)
- **README_dashboard.md** - This file

## Related

- **Observer:** `tools/observer.py` (drift detection)
- **Watchdog:** `tools/watchdog.py` (Memory Bank indexing)
- **Email Watcher:** `tools/email_watcher.py` (Gmail automation)
- **Incident Report:** `memory-bank/incidents/2025-12-03-docker-autostart-false.md`

## Created

- **Date:** 2025-12-03
- **Phase:** 1.8 Infrastructure Monitoring
- **Duration:** ~45 min
- **Slice:** Task Scheduler Dashboard

---

**Tip:** Bookmark this README for quick reference when troubleshooting!
