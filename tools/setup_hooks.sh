#!/bin/bash
# Setup Script for Life Graph Validator
#
# Installs validator and git hooks for automatic validation.
#
# Usage: bash tools/setup_hooks.sh

set -e  # Exit on error

echo "🔧 Setting up Life Graph Validator..."
echo ""

# Get script directory (tools/)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TOOLS_DIR="$REPO_ROOT/tools"
GIT_HOOKS_DIR="$REPO_ROOT/.git/hooks"

# Check if git repo
if [ ! -d "$REPO_ROOT/.git" ]; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Check if validator exists
if [ ! -f "$TOOLS_DIR/validate_entity.py" ]; then
    echo "❌ Error: validate_entity.py not found in tools/"
    exit 1
fi

# Check if pre-commit template exists
if [ ! -f "$TOOLS_DIR/hooks/pre-commit" ]; then
    echo "❌ Error: pre-commit hook not found in tools/hooks/"
    exit 1
fi

# Make validator executable
chmod +x "$TOOLS_DIR/validate_entity.py"
echo "✅ Validator ready: tools/validate_entity.py"

# Install pre-commit hook to .git/hooks/
cp "$TOOLS_DIR/hooks/pre-commit" "$GIT_HOOKS_DIR/pre-commit"
chmod +x "$GIT_HOOKS_DIR/pre-commit"
echo "✅ Active hook: .git/hooks/pre-commit"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 What was installed:"
echo "   • tools/validate_entity.py - Entity validator"
echo "   • tools/hooks/pre-commit - Hook template"
echo "   • .git/hooks/pre-commit - Active git hook"
echo ""
echo "🔍 Validator will now run automatically on every commit"
echo "💡 To bypass validation (use carefully): git commit --no-verify"
echo ""
echo "🧪 Test the validator:"
echo "   python tools/validate_entity.py memory-bank/TEMPLATES/"
