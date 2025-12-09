# Setup Script for Life Graph Validator (PowerShell)
#
# Installs validator and git hooks for automatic validation.
#
# Usage: .\tools\setup_hooks.ps1

Write-Host "🔧 Setting up Life Graph Validator..." -ForegroundColor Cyan
Write-Host ""

# Get repo root directory
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$REPO_ROOT = Split-Path -Parent $SCRIPT_DIR
$TOOLS_DIR = Join-Path $REPO_ROOT "tools"
$GIT_HOOKS_DIR = Join-Path $REPO_ROOT ".git\hooks"

# Check if git repo
if (-not (Test-Path (Join-Path $REPO_ROOT ".git"))) {
    Write-Host "❌ Error: Not a git repository" -ForegroundColor Red
    exit 1
}

# Check if validator exists
$VALIDATOR_PATH = Join-Path $TOOLS_DIR "validate_entity.py"
if (-not (Test-Path $VALIDATOR_PATH)) {
    Write-Host "❌ Error: validate_entity.py not found in tools/" -ForegroundColor Red
    exit 1
}

# Check if pre-commit template exists
$HOOK_TEMPLATE = Join-Path $TOOLS_DIR "hooks\pre-commit"
if (-not (Test-Path $HOOK_TEMPLATE)) {
    Write-Host "❌ Error: pre-commit hook not found in tools/hooks/" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Validator ready: tools\validate_entity.py" -ForegroundColor Green

# Install pre-commit hook to .git/hooks/
$HOOK_DEST = Join-Path $GIT_HOOKS_DIR "pre-commit"

# For Windows, we need to create a batch file that calls Python
$BATCH_HOOK = @'
@echo off
echo 🔍 Validating Life Graph entities...

python tools\validate_entity.py --staged

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Validation failed. Fix errors above and try again.
    echo 💡 Tip: To bypass validation (use carefully): git commit --no-verify
    exit /b 1
)

echo ✅ All staged entities valid
exit /b 0
'@

# Write batch file
Set-Content -Path $HOOK_DEST -Value $BATCH_HOOK -Encoding ASCII
Write-Host "✅ Active hook: .git\hooks\pre-commit" -ForegroundColor Green

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 What was installed:" -ForegroundColor Yellow
Write-Host "   • tools\validate_entity.py - Entity validator"
Write-Host "   • tools\hooks\pre-commit - Hook template"
Write-Host "   • .git\hooks\pre-commit - Active git hook"
Write-Host ""
Write-Host "🔍 Validator will now run automatically on every commit" -ForegroundColor Cyan
Write-Host "💡 To bypass validation (use carefully): git commit --no-verify" -ForegroundColor Yellow
Write-Host ""
Write-Host "🧪 Test the validator:" -ForegroundColor Cyan
Write-Host "   python tools\validate_entity.py memory-bank\TEMPLATES\"
