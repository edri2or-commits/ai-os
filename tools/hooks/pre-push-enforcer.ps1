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
$Editor = "code" # VS Code
$EditorWaitFlag = "--wait"

# Colors for output
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"
$ColorInfo = "Cyan"

# Get current branch name
function Get-CurrentBranch {
    try {
        $branch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($LASTEXITCODE -ne 0) {
            return "unknown"
        }
        return $branch.Trim()
    }
    catch {
        return "unknown"
    }
}

# Get today's date in ISO format
function Get-TodayDate {
    return (Get-Date).ToString("yyyy-MM-dd")
}

# Calculate reflection signature
function Get-ReflectionSignature {
    param(
        [string]$Branch,
        [string]$Date
    )
    return "## Reflection: $Branch - $Date"
}

# Check if reflection exists for today's branch
function Test-ReflectionExists {
    param(
        [string]$Signature
    )
    
    if (-not (Test-Path $ReflectionLog)) {
        return $false
    }
    
    $content = Get-Content $ReflectionLog -Raw
    return $content -match [regex]::Escape($Signature)
}

# Calculate current streak (consecutive days with reflections)
function Get-ReflectionStreak {
    if (-not (Test-Path $ReflectionLog)) {
        return 0
    }
    
    $content = Get-Content $ReflectionLog
    $dates = @()
    
    foreach ($line in $content) {
        if ($line -match '## Reflection: .+ - (\d{4}-\d{2}-\d{2})') {
            $dates += [DateTime]::ParseExact($matches[1], "yyyy-MM-dd", $null)
        }
    }
    
    if ($dates.Count -eq 0) {
        return 0
    }
    
    # Sort dates descending
    $sortedDates = $dates | Sort-Object -Descending -Unique
    
    # Count consecutive days from today
    $streak = 0
    $expectedDate = (Get-Date).Date
    
    foreach ($date in $sortedDates) {
        if ($date.Date -eq $expectedDate) {
            $streak++
            $expectedDate = $expectedDate.AddDays(-1)
        }
        else {
            break
        }
    }
    
    return $streak
}

# Append reflection template
function Add-ReflectionTemplate {
    param(
        [string]$Branch,
        [string]$Date
    )
    
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
    
    # Ensure file exists
    if (-not (Test-Path $ReflectionLog)) {
        "# Reflection Log`n`nMicro-level reflection entries (one per push).`nEnforced by pre-push Git hook.`n`nSee: memory-bank/protocols/PROTOCOL_1_pre-push-reflection.md`n" | Out-File -FilePath $ReflectionLog -Encoding UTF8
    }
    
    # Append template
    $template | Out-File -FilePath $ReflectionLog -Append -Encoding UTF8
    
    Write-Host "✏️  Reflection template added to $ReflectionLog" -ForegroundColor $ColorInfo
}

# Main execution
function Main {
    Write-Host ""
    Write-Host "🔍 Protocol 1 Pre-Push Reflection Check" -ForegroundColor $ColorInfo
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorInfo
    
    # Get context
    $branch = Get-CurrentBranch
    $date = Get-TodayDate
    $signature = Get-ReflectionSignature -Branch $branch -Date $date
    
    Write-Host "Branch: $branch" -ForegroundColor $ColorInfo
    Write-Host "Date: $date" -ForegroundColor $ColorInfo
    Write-Host ""
    
    # Check if reflection exists
    $reflectionExists = Test-ReflectionExists -Signature $signature
    
    if ($reflectionExists) {
        # Reflection already exists - allow push
        $streak = Get-ReflectionStreak
        $streakEmoji = if ($streak -ge 7) { "🔥" } elseif ($streak -ge 3) { "⚡" } else { "✅" }
        
        Write-Host "$streakEmoji Reflection found for today's session!" -ForegroundColor $ColorSuccess
        Write-Host "Streak: $streak day$(if ($streak -ne 1) { 's' })" -ForegroundColor $ColorSuccess
        Write-Host ""
        Write-Host "✅ Push allowed." -ForegroundColor $ColorSuccess
        Write-Host ""
        
        exit 0
    }
    
    # Reflection missing - block and prompt
    Write-Host "⚠️  No reflection entry found for:" -ForegroundColor $ColorWarning
    Write-Host "   $signature" -ForegroundColor $ColorWarning
    Write-Host ""
    Write-Host "📝 Protocol 1 requires micro-reflection before push." -ForegroundColor $ColorInfo
    Write-Host "   This takes ~2 minutes and helps close the cognitive loop." -ForegroundColor $ColorInfo
    Write-Host ""
    
    # Get content hash before editing
    $contentBefore = if (Test-Path $ReflectionLog) { 
        (Get-FileHash $ReflectionLog -Algorithm MD5).Hash 
    } else { 
        "" 
    }
    
    # Add template
    Add-ReflectionTemplate -Branch $branch -Date $date
    
    # Open editor
    Write-Host "🚀 Opening editor... (fill the reflection and save)" -ForegroundColor $ColorInfo
    Write-Host "   Editor will block until you close it." -ForegroundColor $ColorInfo
    Write-Host ""
    
    try {
        # Open VS Code and wait
        & $Editor $EditorWaitFlag $ReflectionLog
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Editor exited with error code $LASTEXITCODE" -ForegroundColor $ColorError
            Write-Host "   You can manually edit $ReflectionLog and try pushing again." -ForegroundColor $ColorError
            Write-Host ""
            exit 1
        }
    }
    catch {
        Write-Host "❌ Failed to open editor: $_" -ForegroundColor $ColorError
        Write-Host "   Please manually edit $ReflectionLog and add reflection." -ForegroundColor $ColorError
        Write-Host ""
        exit 1
    }
    
    # Validate that content changed
    $contentAfter = if (Test-Path $ReflectionLog) { 
        (Get-FileHash $ReflectionLog -Algorithm MD5).Hash 
    } else { 
        "" 
    }
    
    if ($contentBefore -eq $contentAfter) {
        Write-Host "❌ Reflection not modified. Push aborted." -ForegroundColor $ColorError
        Write-Host "   Please fill in the reflection template and try again." -ForegroundColor $ColorError
        Write-Host ""
        exit 1
    }
    
    # Verify reflection now exists
    $reflectionExists = Test-ReflectionExists -Signature $signature
    
    if (-not $reflectionExists) {
        Write-Host "❌ Reflection signature not found after editing." -ForegroundColor $ColorError
        Write-Host "   Expected: $signature" -ForegroundColor $ColorError
        Write-Host "   Please ensure the signature line is intact." -ForegroundColor $ColorError
        Write-Host ""
        exit 1
    }
    
    # Success!
    $streak = Get-ReflectionStreak
    $streakEmoji = if ($streak -ge 7) { "🔥" } elseif ($streak -ge 3) { "⚡" } else { "✅" }
    
    Write-Host ""
    Write-Host "$streakEmoji Reflection recorded successfully!" -ForegroundColor $ColorSuccess
    Write-Host "Streak: $streak day$(if ($streak -ne 1) { 's' })" -ForegroundColor $ColorSuccess
    Write-Host ""
    Write-Host "✅ Push allowed. Good work! 🎯" -ForegroundColor $ColorSuccess
    Write-Host ""
    
    exit 0
}

# Run
Main
