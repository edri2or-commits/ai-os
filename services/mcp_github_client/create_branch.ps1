# One-time script to create branch and commit MCP GitHub Client service
# This is a JUSTIFIED EXCEPTION - creating initial branch structure

$ErrorActionPreference = "Stop"

$REPO_PATH = "C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace"
$BRANCH_NAME = "feature/mcp-github-client-init"

Write-Host "🔄 Creating branch and committing MCP GitHub Client service..." -ForegroundColor Cyan

Set-Location $REPO_PATH

# Check current branch
$CURRENT_BRANCH = git branch --show-current
Write-Host "Current branch: $CURRENT_BRANCH" -ForegroundColor Yellow

# Create and checkout new branch
Write-Host "Creating branch: $BRANCH_NAME" -ForegroundColor Yellow
git checkout -b $BRANCH_NAME

# Stage all new files
Write-Host "Staging new files..." -ForegroundColor Yellow
git add services/mcp_github_client/

# Commit
Write-Host "Committing..." -ForegroundColor Yellow
$commitMessage = @"
[L2] Create MCP GitHub Client - The Heart of AI-OS

This service provides HTTP endpoints for GitHub operations:
- read-file: Read files from repository  
- list-tree: List repository tree
- open-pr: Create Pull Requests (PR-only workflow)

All responses follow standardized format with 'ok' field.
All changes to repo must go through PR workflow.

Thin Slice 1: Core service structure + FastAPI implementation
"@

git commit -m $commitMessage

Write-Host "✅ Branch created and committed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Push branch: git push -u origin $BRANCH_NAME" -ForegroundColor White
Write-Host "2. Claude will create the PR via GitHub API" -ForegroundColor White
