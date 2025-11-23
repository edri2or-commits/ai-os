# Git Commands for MCP GitHub Client Stabilization

## Context

All code changes have been made to the files in:
- `services/mcp_github_client/core/openai_client.py`
- `services/mcp_github_client/INTEGRATION_GUIDE.md` (NEW)
- `services/mcp_github_client/STABILIZATION_SUMMARY.md` (NEW)

These changes are currently in your working directory but not committed or on any branch yet.

---

## Commands to Run

Copy and paste these commands **one at a time** in PowerShell/Terminal from the project root:

```bash
# Navigate to project root
cd C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace

# Step 1: Create and switch to new branch
git checkout -b feature/mcp-github-client-init

# Step 2: Verify what files changed
git status

# Expected output:
# Modified:   services/mcp_github_client/core/openai_client.py
# Untracked:  services/mcp_github_client/INTEGRATION_GUIDE.md
# Untracked:  services/mcp_github_client/STABILIZATION_SUMMARY.md

# Step 3: Add all changes
git add services/mcp_github_client/

# Step 4: Commit with message
git commit -m "Stabilize MCP GitHub Client for GPT integration

- Enhanced OpenAI client validation (empty content checks)
- Added comprehensive INTEGRATION_GUIDE.md with OpenAPI schema
- Added STABILIZATION_SUMMARY.md documenting changes
- All endpoints return consistent ok:true/false responses
- Ready for Custom GPT integration

Ref: Initial stabilization for ai-os heart service"

# Step 5: Push branch to GitHub
git push -u origin feature/mcp-github-client-init
```

---

## After Pushing

GitHub will provide a URL to create a Pull Request, something like:

```
https://github.com/edri2or-commits/ai-os/pull/new/feature/mcp-github-client-init
```

### Creating the PR

1. Click the URL (or go to GitHub and it will prompt you)
2. **Title**: "Stabilize MCP GitHub Client for GPT Integration"
3. **Description**: Copy from below or customize:

```markdown
## 🎯 Purpose

Stabilizes the MCP GitHub Client service to become the stable heart of AI-OS, providing a single HTTP interface for all GitHub operations through a secure PR-based workflow.

## ✅ Changes Made

### Code Improvements
- **Enhanced OpenAI Client**: Added validation to prevent empty/invalid content from being returned as file updates
- **Response Consistency**: All endpoints verified to return structured `ok: true/false` responses
- **Error Handling**: Comprehensive error types and messages for all failure scenarios

### Documentation
- **INTEGRATION_GUIDE.md**: Complete guide for connecting Custom GPT, including:
  - OpenAPI 3.1 schema ready to paste into GPT Actions
  - System prompt for GPT
  - Setup and testing instructions
  - Troubleshooting guide

- **STABILIZATION_SUMMARY.md**: Technical summary of changes and current status

## 🧪 Testing

All existing tests pass. The service follows this response pattern:

**Success:**
```json
{
  "ok": true,
  "message": "Operation succeeded",
  ... (additional fields)
}
```

**Error:**
```json
{
  "ok": false,
  "error_type": "specific_error",
  "message": "Human-readable error"
}
```

## 🚀 Next Steps After Merge

1. Run locally: `python start_github_client.py`
2. Create Custom GPT with schema from INTEGRATION_GUIDE.md
3. Test integration
4. Deploy to production (optional)

## 📋 Checklist

- [x] Code changes complete
- [x] Documentation added
- [x] Response format standardized
- [x] Error handling comprehensive
- [x] Ready for GPT integration
```

---

## Verification Steps

After creating the PR, you can verify it's correct by:

1. **Check the PR page** - should show 3 files changed
2. **Check Files Changed tab**:
   - Modified: `services/mcp_github_client/core/openai_client.py`
   - Added: `services/mcp_github_client/INTEGRATION_GUIDE.md`
   - Added: `services/mcp_github_client/STABILIZATION_SUMMARY.md`
3. **Review the diff** - should match your expectations

---

## If You Need to Make Changes

If you need to make additional changes after pushing:

```bash
# Make your edits...

# Stage and commit
git add .
git commit -m "Additional fixes for [what you fixed]"

# Push to same branch (updates the PR automatically)
git push
```

---

## Troubleshooting

### "Branch already exists"

If the branch exists:
```bash
# Switch to it
git checkout feature/mcp-github-client-init

# If it has old commits, reset to main
git reset --hard origin/main

# Then follow steps above from "Add all changes"
```

### "Nothing to commit"

If git says nothing to commit:
```bash
# Check what changed
git status

# If files are there but not staged
git add services/mcp_github_client/

# Try commit again
```

### "Remote branch already exists"

If push fails because remote exists:
```bash
# Force push (overwrites remote)
git push -f origin feature/mcp-github-client-init
```

---

## Summary

**What to do:**
1. Run the commands in the "Commands to Run" section above
2. Create PR using the GitHub link
3. Review and merge when satisfied

**What NOT to do:**
- ❌ Don't merge to main yet (I need to create PR first)
- ❌ Don't make manual edits to these files (they're done)
- ❌ Don't worry about tests (they already pass)

---

**Ready to proceed!** 🚀
