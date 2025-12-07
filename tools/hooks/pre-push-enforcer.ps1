<#
.SYNOPSIS
    Protocol 1 LEVEL 1 - Micro Reflection Gate (Pre-Push Hook)

.DESCRIPTION
    Enforces micro-level reflection before every git push.
    This is ADHD-aware "good friction" - blocks push until reflection exists.
    
    This hook enforces MICRO-level reflection (every push).
    It does NOT replace MACRO-level documentation:
      - 02-progress.md (still manual for milestones)
      - 01-active-context.md (still manual for phase updates)
    
    Purpose: Close cognitive loop after each push session.
    Scope: Quick bullets (what/why/next).
    Duration: ~2 minutes per push.
    
    Research basis:
    - Gawande: Active checklists prevent ineptitude
    - ADHD: Blocking > nagging, immediate feedback critical
    - Aviation: Pre-flight checklist as quality gate

.NOTES
    See: memory-bank/protocols/PROTOCOL_1_pre-push-reflection.md
#>

# Configuration
$RepoRoot = "C:\Users\edri2\Desktop\AI\ai-os"
$ReflectionLog = Join-Path $RepoRoot "REFLECTION_LOG.md"
$Editor = "code"
$EditorWaitFlag = "--wait"

# Colors
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"
$ColorInfo = "Cyan"

function Get-CurrentBranch {
    try {
        $branch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($LASTEXITCODE -ne 0) { return "unknown" }
        return $branch.Trim()
    }
    catch { return "unknown" }
}

function Get-TodayDate {
    return (Get-Date).ToString("yyyy-MM-dd")
}

function Get-ReflectionSignature {
    param([string]$Branch, [string]$Date)
    return "## Reflection: $Branch - $Date"
}

function Test-ReflectionExists {
    param([string]$Signature)
    if (-not (Test-Path $ReflectionLog)) { return $false }
    $content = Get-Content $ReflectionLog -Raw
    return $content -match [regex]::Escape($Signature)
}

function Get-ReflectionStreak {
    if (-not (Test-Path $ReflectionLog)) { return 0 }
    $content = Get-Content $ReflectionLog
    $dates = @()
    
    foreach ($line in $content) {
        if ($line -match '## Reflection: .+ - (\d{4}-\d{2}-\d{2})') {
            $dates += [DateTime]::ParseExact($matches[1], "yyyy-MM-dd", $null)
        }
    }
    
    if ($dates.Count -eq 0) { return 0 }
    $sortedDates = $dates | Sort-Object -Descending -Unique
    $streak = 0
    $expectedDate = (Get-Date).Date
    
    foreach ($date in $sortedDates) {
        if ($date.Date -eq $expectedDate) {
            $streak++
            $expectedDate = $expectedDate.AddDays(-1)
        }
        else { break }
    }
    
    return $streak
}

function Add-ReflectionTemplate {
    param([string]$Branch, [string]$Date)
    $signature = Get-ReflectionSignature -Branch $Branch -Date $Date
    
    $template = @"

---

$signature

**Branch:** $Branch  
**Date:** $Date

**What was done:**
- [Describe what you accomplished in this push]

**Why:**
- [Why was this needed? What problem does it solve?]

**Next:**
- [What's the immediate next step?]

**Context/Notes:**
- [Any additional context, blockers, or observations]

"@
    
    if (-not (Test-Path $ReflectionLog)) {
        "# Reflection Log`n`nMicro-level reflection entries (one per push).`nEnforced by pre-push Git hook.`n`nSee: memory-bank/protocols/PROTOCOL_1_pre-push-reflection.md`n" | Out-File -FilePath $ReflectionLog -Encoding UTF8
    }
    
    $template | Out-File -FilePath $ReflectionLog -Append -Encoding UTF8
    Write-Host "[+] Template added to $ReflectionLog" -ForegroundColor $ColorInfo
}

function Main {
    Write-Host ""
    Write-Host "=== Protocol 1 Pre-Push Reflection Check ===" -ForegroundColor $ColorInfo
    Write-Host ""
    
    $branch = Get-CurrentBranch
    $date = Get-TodayDate
    $signature = Get-ReflectionSignature -Branch $branch -Date $date
    
    Write-Host "Branch: $branch" -ForegroundColor $ColorInfo
    Write-Host "Date: $date" -ForegroundColor $ColorInfo
    Write-Host ""
    
    if (Test-ReflectionExists -Signature $signature) {
        $streak = Get-ReflectionStreak
        $label = if ($streak -ge 7) { "FIRE" } elseif ($streak -ge 3) { "BOLT" } else { "OK" }
        
        Write-Host "[$label] Reflection found! Streak: $streak day$(if ($streak -ne 1) { 's' })" -ForegroundColor $ColorSuccess
        Write-Host "[OK] Push allowed." -ForegroundColor $ColorSuccess
        Write-Host ""
        exit 0
    }
    
    Write-Host "[!] No reflection found for: $signature" -ForegroundColor $ColorWarning
    Write-Host "[i] Protocol 1 requires micro-reflection (~2 min)" -ForegroundColor $ColorInfo
    Write-Host ""
    
    $hashBefore = if (Test-Path $ReflectionLog) { (Get-FileHash $ReflectionLog -Algorithm MD5).Hash } else { "" }
    
    Add-ReflectionTemplate -Branch $branch -Date $date
    
    Write-Host "[>] Opening editor (fill and save)..." -ForegroundColor $ColorInfo
    Write-Host ""
    
    try {
        & $Editor $EditorWaitFlag $ReflectionLog
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[X] Editor error. Edit manually and retry." -ForegroundColor $ColorError
            exit 1
        }
    }
    catch {
        Write-Host "[X] Failed to open editor. Edit manually." -ForegroundColor $ColorError
        exit 1
    }
    
    $hashAfter = if (Test-Path $ReflectionLog) { (Get-FileHash $ReflectionLog -Algorithm MD5).Hash } else { "" }
    
    if ($hashBefore -eq $hashAfter) {
        Write-Host "[X] Not modified. Push aborted." -ForegroundColor $ColorError
        exit 1
    }
    
    if (-not (Test-ReflectionExists -Signature $signature)) {
        Write-Host "[X] Signature missing after edit." -ForegroundColor $ColorError
        exit 1
    }
    
    $streak = Get-ReflectionStreak
    $label = if ($streak -ge 7) { "FIRE" } elseif ($streak -ge 3) { "BOLT" } else { "OK" }
    
    Write-Host ""
    Write-Host "[$label] Recorded! Streak: $streak day$(if ($streak -ne 1) { 's' })" -ForegroundColor $ColorSuccess
    Write-Host "[OK] Push allowed. Good work!" -ForegroundColor $ColorSuccess
    Write-Host ""
    exit 0
}

Main
