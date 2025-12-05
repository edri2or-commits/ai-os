# Keep-Awake Configuration - AI Life OS

Prevents Windows from sleeping while automation is running.

---

## 📊 Comparison Table

| Method | Setup Time | Power Usage | Flexibility | Best For |
|--------|-----------|-------------|-------------|----------|
| **GUI (Option A)** | 2 min | ⚠️ High (always on) | ❌ None | Quick test |
| **PowerShell (Option B)** | 5 min | ⚠️ High (always on) | ✅ Scriptable | 24/7 server |
| **Smart Keep-Awake (Option C)** | 10 min | ✅ Low (only when needed) | ✅✅ Intelligent | **RECOMMENDED** |

---

## 🎯 Option A: GUI (Quick & Simple)

**Use this for:** Quick testing (few hours/days)

**Steps:**
1. `Win + I` → System → Power & sleep
2. Set "Sleep" to **Never** (when plugged in)
3. Set "Screen" to **Never** (optional)

**Pros:**
- ✅ Fastest setup (2 minutes)
- ✅ No scripting needed

**Cons:**
- ❌ Computer always on (high power consumption)
- ❌ Screen stays on (unless manually configured)
- ❌ Not intelligent (can't adapt)

---

## 🔧 Option B: PowerShell (Professional)

**Use this for:** Dedicated server/workstation (24/7 operation)

**Setup:**
```powershell
# Run as Administrator
cd C:\Users\edri2\Desktop\AI\ai-os\tools
.\disable_sleep.ps1
```

**What it does:**
- Disables sleep when plugged in (AC power)
- Disables monitor timeout
- Disables hibernate
- Disables hybrid sleep
- Disables hard disk timeout

**To restore normal settings:**
```powershell
.\restore_sleep.ps1
```

**Pros:**
- ✅ Consistent behavior
- ✅ Scriptable (can integrate with other automation)
- ✅ Easy to revert

**Cons:**
- ❌ Always on (high power consumption ~150-300W 24/7)
- ❌ Not intelligent (wastes power when Docker isn't running)

**Cost estimation:**
- Power: ~200W × 24h × 30 days = 144 kWh/month
- Cost: 144 kWh × ₪0.50 = **~₪72/month** ($20/month)

---

## 🧠 Option C: Smart Keep-Awake (RECOMMENDED)

**Use this for:** Optimal balance (automation when needed, sleep when idle)

**Setup:**
```powershell
# 1. Setup Task Scheduler (run as Administrator)
cd C:\Users\edri2\Desktop\AI\ai-os\tools
.\setup_keep_awake_task.ps1

# 2. Start immediately (without reboot)
Start-ScheduledTask -TaskPath '\AI-OS\' -TaskName 'Smart Keep-Awake'

# 3. Verify it's running
Get-ScheduledTask -TaskPath '\AI-OS\' -TaskName 'Smart Keep-Awake'
```

**How it works:**
1. **Monitors Docker** every 5 minutes
2. **Critical containers checked:**
   - n8n-production
   - qdrant-production
   - langfuse-web-1
   - langfuse-worker-1
3. **If running:** Prevents system sleep ☕
4. **If stopped:** Allows normal sleep 💤

**Behavior:**
```
Docker running:
├─ System: AWAKE (automation working)
└─ Screen: Can turn off (saves power)

Docker stopped:
├─ System: Sleeps normally after 30 min
└─ Screen: Turns off after 15 min
```

**Pros:**
- ✅ **Intelligent** - only prevents sleep when needed
- ✅ **Low power** - sleeps when Docker is off
- ✅ **Auto-start** - runs on Windows startup
- ✅ **Silent** - hidden window (no distraction)
- ✅ **Safe** - allows screen to turn off

**Cons:**
- ⚠️ 5-minute detection lag (can tune with `-CheckIntervalMinutes`)
- ⚠️ Requires PowerShell to stay running (minimal overhead)

**Cost estimation:**
- Active time: ~12 hours/day (50% usage)
- Power: 200W × 12h × 30 days = 72 kWh/month
- Cost: 72 kWh × ₪0.50 = **~₪36/month** ($10/month)
- **Savings: ₪36/month vs Option B**

---

## 🔍 Manual Testing

Before setting up Task Scheduler, test manually:

```powershell
# Run in a PowerShell window (keep it open)
cd C:\Users\edri2\Desktop\AI\ai-os\tools
.\smart_keep_awake.ps1 -ShowWindow

# You'll see output like:
# [14:30:00] Docker automation active - PREVENTING SLEEP ☕
# [14:30:00] Running: 4/4 containers ✓
```

**To stop manual test:** Press `Ctrl+C`

---

## 🛠️ Task Scheduler Management

**Check status:**
```powershell
Get-ScheduledTask -TaskPath '\AI-OS\' -TaskName 'Smart Keep-Awake'
```

**Start manually:**
```powershell
Start-ScheduledTask -TaskPath '\AI-OS\' -TaskName 'Smart Keep-Awake'
```

**Stop manually:**
```powershell
Stop-ScheduledTask -TaskPath '\AI-OS\' -TaskName 'Smart Keep-Awake'
```

**View logs (if issues):**
```powershell
Get-ScheduledTaskInfo -TaskPath '\AI-OS\' -TaskName 'Smart Keep-Awake'
```

**Remove task:**
```powershell
Unregister-ScheduledTask -TaskPath '\AI-OS\' -TaskName 'Smart Keep-Awake' -Confirm:$false
```

---

## 🎯 Decision Tree

```
Do you need 24/7 uptime?
├─ YES, for production server
│  └─ Use Option B (disable_sleep.ps1)
│
└─ NO, only when I'm working
   ├─ Docker runs < 12 hours/day
   │  └─ Use Option C (smart_keep_awake.ps1) ✅ BEST
   │
   └─ Testing for few hours
      └─ Use Option A (GUI)
```

---

## ⚠️ Important Notes

**Battery Safety (Laptops):**
- All options only affect **AC power** (when plugged in)
- On battery: sleep after 30 minutes (unchanged)
- This protects battery life

**Screen Timeout:**
- Smart Keep-Awake allows screen to turn off
- Saves power and prolongs screen life
- System stays awake, only display sleeps

**Docker Dependency:**
- Smart Keep-Awake needs Docker Desktop installed
- If Docker is uninstalled, task will fail gracefully

---

## 🚀 Recommended Setup (Step-by-Step)

**For most users (Option C):**

1. **Install Smart Keep-Awake:**
   ```powershell
   # Run PowerShell as Administrator
   cd C:\Users\edri2\Desktop\AI\ai-os\tools
   .\setup_keep_awake_task.ps1
   ```

2. **Start immediately:**
   ```powershell
   Start-ScheduledTask -TaskPath '\AI-OS\' -TaskName 'Smart Keep-Awake'
   ```

3. **Verify Docker is detected:**
   ```powershell
   # Start Docker Desktop
   # Wait 2 minutes
   # Check if computer stays awake
   ```

4. **Done!** System now:
   - ✅ Stays awake when Docker runs
   - ✅ Sleeps normally when Docker stops
   - ✅ Auto-starts on Windows boot

---

## 📊 Monitoring & Verification

**Check if it's working:**
```powershell
# 1. Check task is running
Get-ScheduledTask -TaskPath '\AI-OS\' | Where-Object {$_.TaskName -eq 'Smart Keep-Awake'} | Select-Object TaskName, State

# 2. Check Docker containers
docker ps --format "{{.Names}}"

# 3. Check power plan
powercfg /requests
# Should show: EXECUTION:Smart Keep-Awake (if Docker running)
```

---

## 🆘 Troubleshooting

**Problem: Computer still sleeps**
- Check task status: `Get-ScheduledTask`
- Verify Docker is running: `docker ps`
- Check execution state: `powercfg /requests`

**Problem: Computer never sleeps**
- Check if script is stuck: `Stop-ScheduledTask`
- Verify Docker stopped: `docker ps` (should be empty)
- Manually allow sleep: `.\restore_sleep.ps1`

**Problem: Task fails to start**
- Check script path exists
- Run as Administrator
- Check PowerShell execution policy: `Get-ExecutionPolicy`

---

## 📝 Files Created

```
tools/
├─ disable_sleep.ps1              # Option B: Permanent disable
├─ restore_sleep.ps1              # Option B: Restore defaults
├─ smart_keep_awake.ps1           # Option C: Smart prevention
├─ setup_keep_awake_task.ps1      # Option C: Task installer
└─ README_keep_awake.md           # This file
```

---

**Last Updated:** 2025-12-05  
**Status:** Production Ready  
**Recommended:** Option C (Smart Keep-Awake)
