<#
.SYNOPSIS
    AI-OS System Dashboard - Health monitoring for automated processes

.DESCRIPTION
    Displays status of:
    - 3 Scheduled Tasks (Observer, Watchdog, Email Watcher)
    - 2 Docker containers (n8n, Qdrant)
    - Recent drift reports
    
    Read-only, ADHD-friendly single-pane-of-glass view.

.EXAMPLE
    .\dashboard.ps1
    
.NOTES
    Author: AI-OS Project
    Created: 2025-12-03
    Phase: 1.8 Infrastructure Monitoring
#>

# Color helper functions
function Write-Success { param($text) Write-Host $text -ForegroundColor Green }
function Write-Warning { param($text) Write-Host $text -ForegroundColor Yellow }
function Write-Error { param($text) Write-Host $text -ForegroundColor Red }
function Write-Info { param($text) Write-Host $text -ForegroundColor Cyan }
function Write-Header { param($text) Write-Host $text -ForegroundColor White -BackgroundColor DarkBlue }

# Time helpers
function Get-TimeAgo {
    param([DateTime]$timestamp)
    
    if (-not $timestamp -or $timestamp -eq [DateTime]::MinValue) {
        return "Never"
    }
    
    $span = (Get-Date) - $timestamp
    
    if ($span.TotalMinutes -lt 1) { return "Just now" }
    if ($span.TotalMinutes -lt 60) { return "$([int]$span.TotalMinutes) min ago" }
    if ($span.TotalHours -lt 24) { return "$([int]$span.TotalHours) hours ago" }
    return "$([int]$span.TotalDays) days ago"
}

function Get-TimeUntil {
    param([DateTime]$timestamp)
    
    if (-not $timestamp -or $timestamp -eq [DateTime]::MinValue) {
        return "Unknown"
    }
    
    $span = $timestamp - (Get-Date)
    
    if ($span.TotalSeconds -lt 0) { return "Overdue" }
    if ($span.TotalMinutes -lt 60) { return "in $([int]$span.TotalMinutes) min" }
    if ($span.TotalHours -lt 24) { return "in $([int]$span.TotalHours) hours" }
    return "in $([int]$span.TotalDays) days"
}

# Main dashboard
Clear-Host

Write-Host ""
Write-Header "==================================================================="
Write-Header "                AI-OS System Dashboard                            "
Write-Header "==================================================================="
Write-Host ""

# ==========================
# SCHEDULED TASKS
# ==========================
Write-Info "[SCHEDULED TASKS]"
Write-Host "-------------------------------------------------------------------"

$taskNames = @(
    "Observer-Drift-Detection",
    "Watchdog-Memory-Bank-Ingestion", 
    "\AI-OS\Email Watcher"
)

$allTasksOk = $true

foreach ($taskName in $taskNames) {
    try {
        # Handle full paths (e.g., "\AI-OS\Email Watcher")
        if ($taskName -match "\\") {
            $allTasks = Get-ScheduledTask -ErrorAction Stop
            $task = $allTasks | Where-Object { "$($_.TaskPath)$($_.TaskName)" -eq $taskName }
            if (-not $task) { throw "Task not found" }
            $taskInfo = Get-ScheduledTaskInfo -InputObject $task -ErrorAction Stop
        } else {
            $task = Get-ScheduledTask -TaskName $taskName -ErrorAction Stop
            $taskInfo = Get-ScheduledTaskInfo -TaskName $taskName -ErrorAction Stop
        }
        
        # Determine status
        $statusIcon = "[OK]"
        $statusColor = "Green"
        
        if ($task.State -ne "Ready") {
            $statusIcon = "[WARN]"
            $statusColor = "Yellow"
            $allTasksOk = $false
        }
        
        if ($taskInfo.LastTaskResult -ne 0) {
            $statusIcon = "[FAIL]"
            $statusColor = "Red"
            $allTasksOk = $false
        }
        
        # Display
        Write-Host "$statusIcon " -NoNewline -ForegroundColor $statusColor
        Write-Host "$taskName" -ForegroundColor White
        
        $lastRun = if ($taskInfo.LastRunTime -eq [DateTime]::MinValue) { 
            "Never" 
        } else { 
            "$($taskInfo.LastRunTime.ToString('yyyy-MM-dd HH:mm:ss')) ($(Get-TimeAgo $taskInfo.LastRunTime))"
        }
        
        $nextRun = if ($taskInfo.NextRunTime -eq [DateTime]::MinValue) {
            "Not scheduled"
        } else {
            "$($taskInfo.NextRunTime.ToString('yyyy-MM-dd HH:mm:ss')) ($(Get-TimeUntil $taskInfo.NextRunTime))"
        }
        
        Write-Host "   Last Run: $lastRun" -ForegroundColor Gray
        Write-Host "   Next Run: $nextRun" -ForegroundColor Gray
        
        $exitCodeText = if ($taskInfo.LastTaskResult -eq 0) {
            "0 (Success)"
        } else {
            "0x$($taskInfo.LastTaskResult.ToString('X8')) (Failed)"
        }
        Write-Host "   Exit Code: $exitCodeText" -ForegroundColor Gray
        Write-Host ""
        
    } catch {
        Write-Error "[FAIL] $taskName"
        Write-Host "   Error: Task not found" -ForegroundColor Red
        Write-Host ""
        $allTasksOk = $false
    }
}

# ==========================
# DOCKER SERVICES
# ==========================
Write-Info "[DOCKER SERVICES]"
Write-Host "-------------------------------------------------------------------"

try {
    $dockerOutput = docker ps --format "{{.Names}}\t{{.Status}}\t{{.Ports}}" 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not running"
    }
    
    $expectedContainers = @("n8n-production", "qdrant-production")
    $runningContainers = @()
    
    foreach ($line in $dockerOutput) {
        $parts = $line -split "`t"
        if ($parts.Count -ge 2) {
            $name = $parts[0]
            $status = $parts[1]
            $ports = if ($parts.Count -ge 3) { $parts[2] } else { "No ports" }
            
            if ($name -in $expectedContainers) {
                $runningContainers += $name
                
                # Parse uptime
                if ($status -match "Up (.+)") {
                    $uptime = $matches[1]
                } else {
                    $uptime = "Unknown"
                }
                
                # Parse port
                $portDisplay = "Unknown"
                if ($ports -match ":(\d+)->") {
                    $portDisplay = ":$($matches[1])"
                }
                
                Write-Success "[OK] $name"
                Write-Host "   Status: UP ($uptime)" -ForegroundColor Gray
                Write-Host "   Port: $portDisplay" -ForegroundColor Gray
                Write-Host ""
            }
        }
    }
    
    # Check for missing containers
    $allDockerOk = $true
    foreach ($expected in $expectedContainers) {
        if ($expected -notin $runningContainers) {
            Write-Error "[FAIL] $expected"
            Write-Host "   Status: NOT RUNNING" -ForegroundColor Red
            Write-Host ""
            $allDockerOk = $false
        }
    }
    
} catch {
    Write-Error "[FAIL] Docker Desktop"
    Write-Host "   Status: NOT RUNNING or not accessible" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    $allDockerOk = $false
}

# ==========================
# DRIFT REPORTS
# ==========================
Write-Info "[DRIFT REPORTS]"
Write-Host "-------------------------------------------------------------------"

$driftDir = Join-Path $PSScriptRoot "..\truth-layer\drift"

if (Test-Path $driftDir) {
    $reports = Get-ChildItem -Path $driftDir -Filter "*.yaml" | Sort-Object LastWriteTime -Descending
    
    if ($reports.Count -gt 0) {
        Write-Host "Total Reports: $($reports.Count)" -ForegroundColor White
        
        $latest = $reports[0]
        $latestAge = Get-TimeAgo $latest.LastWriteTime
        Write-Host "Latest: $($latest.Name) ($latestAge)" -ForegroundColor Gray
        
        # Count by type
        $emailReports = ($reports | Where-Object { $_.Name -like "email-*" }).Count
        $otherReports = $reports.Count - $emailReports
        
        if ($emailReports -gt 0) {
            Write-Host "   Email drift reports: $emailReports" -ForegroundColor Gray
        }
        if ($otherReports -gt 0) {
            Write-Host "   Other drift reports: $otherReports" -ForegroundColor Gray
        }
    } else {
        Write-Warning "[WARN] No drift reports found"
    }
} else {
    Write-Warning "[WARN] Drift directory not found: $driftDir"
}

Write-Host ""

# ==========================
# OVERALL STATUS
# ==========================
Write-Host "==================================================================="

if ($allTasksOk -and $allDockerOk) {
    Write-Success "[STATUS] ALL SYSTEMS OPERATIONAL"
} else {
    $issues = @()
    if (-not $allTasksOk) { $issues += "Scheduled Tasks" }
    if (-not $allDockerOk) { $issues += "Docker Services" }
    
    Write-Warning "[STATUS] ISSUES DETECTED: $($issues -join ', ')"
}

Write-Host "==================================================================="
Write-Host ""

# Footer
Write-Host "Tip: Run this script anytime to check system health" -ForegroundColor DarkGray
Write-Host "Docs: tools/README_dashboard.md" -ForegroundColor DarkGray
Write-Host ""
