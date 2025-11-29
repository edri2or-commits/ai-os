#!/bin/bash
set -e
BRANCH="feature/mcp-github-client-init"

git checkout -b $BRANCH
git add services/mcp_github_client
git commit -m "Add ai-os-mcp-github-client service (MCP client for GitHub MCP Server + OpenAI PR flow)"
git push origin $BRANCH

gh pr create --base main --head $BRANCH --title "Add ai-os-mcp-github-client service" --body "Introduces ai-os-mcp-github-client service with FastAPI, MCP integration and OpenAI PR flow."
