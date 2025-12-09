# Panic Button - Emergency State Preservation
# Hotkey: Ctrl+Alt+P
# Purpose: Pause all automation, commit WIP, dump state

param(
    [switch]$Test
)

$ErrorActionPreference = "Continue"
$PanicDir = "C:\Users\edri2\Desktop\AI\ai-os\panic"
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$PanicLog = "$PanicDir\panic_$Timestamp.log"

# Ensure panic directory exists
New-Item -ItemType Directory -Path $PanicDir -Force | Out-Null

function Write-PanicLog {
    param([string]$Message)
    $LogEntry = "[$(Get-Date -Format 'HH:mm:ss')] $Message"
    Write-Host $LogEntry -ForegroundColor Yellow
    Add-Content -Path $PanicLog -Value $LogEntry
}

Write-PanicLog "=== PANIC BUTTON ACTIVATED ==="
Write-PanicLog "Timestamp: $Timestamp"

# Step 1: Pause Docker containers (n8n)
Write-PanicLog "Step 1: Pausing Docker containers..."
try {
    $DockerContainers = docker ps --format "{{.Names}}" 2>$null
    if ($DockerContainers) {
        foreach ($Container in $DockerContainers) {
            Write-PanicLog "  Pausing container: $Container"
            docker pause $Container 2>&1 | Out-Null
        }
        Write-PanicLog "  [OK] Docker containers paused"
    } else {
        Write-PanicLog "  [SKIP] No running Docker containers"
    }
} catch {
    Write-PanicLog "  [ERROR] Failed to pause Docker: $_"
}

# Step 2: Git WIP commit
Write-PanicLog "Step 2: Creating Git WIP commit..."
try {
    $GitRoot = "C:\Users\edri2\Desktop\AI\ai-os"
    Set-Location $GitRoot
    
    # Check if there are changes
    $GitStatus = & "C:\Program Files\Git\cmd\git.exe" status --porcelain 2>&1
    
    if ($GitStatus) {
        Write-PanicLog "  Detected uncommitted changes"
        
        # Stage all changes
        & "C:\Program Files\Git\cmd\git.exe" add -A
        
        # Create WIP commit
        $CommitMsg = "WIP: Panic button save - $Timestamp"
        & "C:\Program Files\Git\cmd\git.exe" commit -m $CommitMsg --no-verify
        
        $CommitHash = & "C:\Program Files\Git\cmd\git.exe" rev-parse --short HEAD
        Write-PanicLog "  [OK] WIP commit created: $CommitHash"
    } else {
        Write-PanicLog "  [SKIP] No uncommitted changes"
    }
} catch {
    Write-PanicLog "  [ERROR] Git WIP commit failed: $_"
}

# Step 3: Dump system state
Write-PanicLog "Step 3: Dumping system state..."
try {
    $StateFile = "$PanicDir\state_$Timestamp.json"
    
    $State = @{
        timestamp = $Timestamp
        git_branch = & "C:\Program Files\Git\cmd\git.exe" branch --show-current 2>$null
        git_status = & "C:\Program Files\Git\cmd\git.exe" status --short 2>$null
        docker_containers = docker ps --format "{{.Names}}: {{.Status}}" 2>$null
        running_processes = Get-Process | Where-Object {
            $_.ProcessName -match "python|node|docker|claude"
        } | Select-Object ProcessName, Id, WorkingSet
        memory_mb = [math]::Round((Get-Process -Id $PID).WorkingSet / 1MB, 2)
    }
    
    $State | ConvertTo-Json -Depth 3 | Out-File -FilePath $StateFile -Encoding UTF8
    Write-PanicLog "  [OK] State dumped to: $StateFile"
} catch {
    Write-PanicLog "  [ERROR] State dump failed: $_"
}

# Step 4: Copy recent logs
Write-PanicLog "Step 4: Archiving recent logs..."
try {
    $LogsDir = "C:\Users\edri2\Desktop\AI\ai-os\logs"
    if (Test-Path $LogsDir) {
        $PanicLogsDir = "$PanicDir\logs_$Timestamp"
        New-Item -ItemType Directory -Path $PanicLogsDir -Force | Out-Null
        
        # Copy JSONL logs
        Get-ChildItem -Path $LogsDir -Filter "*.jsonl" | ForEach-Object {
            Copy-Item $_.FullName -Destination $PanicLogsDir
            Write-PanicLog "  Archived: $($_.Name)"
        }
        Write-PanicLog "  [OK] Logs archived"
    } else {
        Write-PanicLog "  [SKIP] No logs directory found"
    }
} catch {
    Write-PanicLog "  [ERROR] Log archiving failed: $_"
}

# Step 5: Summary
Write-PanicLog ""
Write-PanicLog "=== PANIC SEQUENCE COMPLETE ==="
Write-PanicLog "All automated processes paused"
Write-PanicLog "Current state saved to: $PanicDir"
Write-PanicLog "Git WIP commit created (if changes existed)"
Write-PanicLog ""
Write-PanicLog "TO RESUME:"
Write-PanicLog "  1. Review panic log: $PanicLog"
Write-PanicLog "  2. Unpause Docker: docker unpause <container-name>"
Write-PanicLog "  3. Reset WIP commit: git reset HEAD~1 (if desired)"
Write-PanicLog ""

# Display notification
if (-not $Test) {
    Add-Type -AssemblyName System.Windows.Forms
    $notification = New-Object System.Windows.Forms.NotifyIcon
    $notification.Icon = [System.Drawing.SystemIcons]::Warning
    $notification.BalloonTipTitle = "Panic Button Activated"
    $notification.BalloonTipText = "System paused. Check panic log for details."
    $notification.Visible = $true
    $notification.ShowBalloonTip(5000)
    Start-Sleep -Seconds 2
    $notification.Dispose()
}

Write-PanicLog "Panic button script completed"
