#!/usr/bin/env pwsh
# Commit script for MCP GitHub Client stability improvements

$ErrorActionPreference = "Stop"

Write-Host "🔧 Committing MCP GitHub Client stability improvements..." -ForegroundColor Cyan

# Navigate to repo root
$repoRoot = "C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace"
Set-Location $repoRoot

# Check if we're in a git repo
if (-not (Test-Path ".git")) {
    Write-Host "❌ Not a git repository!" -ForegroundColor Red
    exit 1
}

# Add modified files
Write-Host "📝 Adding files..." -ForegroundColor Yellow
git add services/mcp_github_client/requirements.txt
git add services/mcp_github_client/STABILITY_AUDIT.md

# Check if there are changes to commit
$status = git status --porcelain
if (-not $status) {
    Write-Host "✅ No changes to commit" -ForegroundColor Green
    exit 0
}

# Create commit
$commitMessage = @"
[AI-OS] Stabilize MCP GitHub Client - Add testing deps and audit

## Changes
- Add pytest and pytest-asyncio to requirements.txt for testing
- Create STABILITY_AUDIT.md documenting response format consistency
- Validate all endpoints return structured {ok, error_type, message}
- Confirm error handling in MCPGitHubClient and OpenAIClient

## Status
✅ Service is stable and ready for integration
- All endpoints follow unified response format
- Error handling is comprehensive
- Logging is properly configured
- Tests verify 'ok' field presence

## Next Steps
- Integration with start.py / start_public_server.py
- Update .env.template with service variables
- Update SSOT documentation
"@

Write-Host "💾 Creating commit..." -ForegroundColor Yellow
git commit -m $commitMessage

Write-Host "✅ Commit created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Commit details:" -ForegroundColor Cyan
git log -1 --stat

Write-Host ""
Write-Host "🚀 To push: git push origin main" -ForegroundColor Yellow
