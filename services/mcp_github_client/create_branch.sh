#!/bin/bash
# One-time script to create branch and commit MCP GitHub Client service
# This is a JUSTIFIED EXCEPTION - creating initial branch structure

set -e

REPO_PATH="C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace"
BRANCH_NAME="feature/mcp-github-client-init"

echo "🔄 Creating branch and committing MCP GitHub Client service..."

cd "$REPO_PATH"

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Create and checkout new branch
echo "Creating branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"

# Stage all new files
echo "Staging new files..."
git add services/mcp_github_client/

# Commit
echo "Committing..."
git commit -m "[L2] Create MCP GitHub Client - The Heart of AI-OS

This service provides HTTP endpoints for GitHub operations:
- read-file: Read files from repository
- list-tree: List repository tree
- open-pr: Create Pull Requests (PR-only workflow)

All responses follow standardized format with 'ok' field.
All changes to repo must go through PR workflow.

Thin Slice 1: Core service structure + FastAPI implementation"

echo "✅ Branch created and committed successfully!"
echo "Next step: Push branch and create PR"
