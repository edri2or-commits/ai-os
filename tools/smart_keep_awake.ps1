# Smart Keep-Awake - Prevent sleep only when Docker containers are running
# This script runs in background and keeps Windows awake while automation is active

param(
    [int]$CheckIntervalMinutes = 5,
    [switch]$ShowWindow = $false
)

Write-Host "Smart Keep-Awake - AI Life OS" -ForegroundColor Cyan
Write-Host "Monitoring Docker containers every $CheckIntervalMinutes minutes..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Gray

# Load Windows API for preventing sleep
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class PowerManagement {
    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern uint SetThreadExecutionState(uint esFlags);
    
    public const uint ES_CONTINUOUS = 0x80000000;
    public const uint ES_SYSTEM_REQUIRED = 0x00000001;
    public const uint ES_DISPLAY_REQUIRED = 0x00000002;
}
"@

$keepAwake = $false

while ($true) {
    # Check if critical Docker containers are running
    $criticalContainers = @(
        "n8n-production",
        "qdrant-production", 
        "langfuse-web-1",
        "langfuse-worker-1"
    )
    
    $runningContainers = docker ps --format "{{.Names}}" 2>$null
    $criticalRunning = $criticalContainers | Where-Object { $runningContainers -contains $_ }
    
    if ($criticalRunning.Count -gt 0) {
        # Docker is running automation - prevent sleep
        if (-not $keepAwake) {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] " -NoNewline -ForegroundColor Gray
            Write-Host "Docker automation active - " -NoNewline -ForegroundColor Green
            Write-Host "PREVENTING SLEEP ☕" -ForegroundColor Yellow
            
            # Prevent system sleep (but allow screen to turn off)
            [PowerManagement]::SetThreadExecutionState(
                [PowerManagement]::ES_CONTINUOUS -bor 
                [PowerManagement]::ES_SYSTEM_REQUIRED
            ) | Out-Null
            
            $keepAwake = $true
        }
        
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Running: $($criticalRunning.Count)/$($criticalContainers.Count) containers ✓" -ForegroundColor DarkGray
        
    } else {
        # No automation running - allow sleep
        if ($keepAwake) {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] " -NoNewline -ForegroundColor Gray
            Write-Host "Docker stopped - " -NoNewline -ForegroundColor Yellow
            Write-Host "ALLOWING SLEEP 💤" -ForegroundColor Cyan
            
            # Allow system to sleep normally
            [PowerManagement]::SetThreadExecutionState(
                [PowerManagement]::ES_CONTINUOUS
            ) | Out-Null
            
            $keepAwake = $false
        }
        
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] No automation running (sleep allowed)" -ForegroundColor DarkGray
    }
    
    # Wait before next check
    Start-Sleep -Seconds ($CheckIntervalMinutes * 60)
}
