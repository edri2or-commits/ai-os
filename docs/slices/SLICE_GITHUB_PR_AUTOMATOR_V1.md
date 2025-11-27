# SLICE_GITHUB_PR_AUTOMATOR_V1

**Date:** 2025-11-27  
**Phase:** 2.3 (INFRA_ONLY)  
**Status:** 🚧 In Progress

---

## 🎯 Goal

Transform MCP GitHub Client into the **official PR gateway** of AI-OS, enabling automated Pull Request creation from completed slices without manual intervention.

**End State:**
- Claude Desktop can say: "Open PR for slice X" → PR created automatically
- GPT Operator can call `/github/open-pr` → PR created automatically
- Consistent, auditable PR workflow for all infrastructure slices

---

## 📊 Truth Layer - Current State

### GitHub Integration Status (as of 2025-11-27)

**1. Local Git:**
- ✅ Working: Read/write files, commit, push branches
- ❌ Missing: Cannot create PRs (no GitHub API access)
- Location: `C:\Users\edri2\Desktop\AI\ai-os`
- Remote: `https://github.com/edri2or-commits/ai-os.git`

**2. GitHub CLI (gh):**
- ✅ Installed: `gh version 2.83.1`
- ❌ Not authenticated: Requires `gh auth login`
- ❌ Cannot use: All PR operations blocked

**3. MCP GitHub Client:**
- ✅ Code exists: `services/mcp_github_client/`
- ✅ Has `/github/open-pr` endpoint (full PR workflow)
- ✅ FastAPI service on port 8081
- ❌ Not running: Service not started
- ❌ No PAT configured: Missing GitHub authentication

---

## 📦 Outputs - What This Slice Delivers

### 1. Configuration Layer

**Files:**
- `services/mcp_github_client/.env.template` - Template with required variables
- `services/mcp_github_client/README.md` - Updated with clear setup instructions
- `services/mcp_github_client/.gitignore` - Ensure `.env` is never committed

**Content:**
```env
# .env.template
GITHUB_TOKEN=ghp_your_token_here
GITHUB_OWNER=edri2or-commits
GITHUB_REPO=ai-os
GITHUB_DEFAULT_BASE=main
SERVICE_PORT=8081
```

### 2. Service Launcher

**File:** `services/mcp_github_client/run_service.bat` (Windows)

**Purpose:** One-click service startup

**Content:**
```batch
@echo off
echo Starting MCP GitHub Client...
python -m uvicorn services.mcp_github_client.main:app --port 8081 --reload
```

### 3. Smoke Test - PR Creation

**File:** `services/mcp_github_client/smoke_test_open_pr.py`

**Tests:**
1. ✅ Service health check (`GET /health`)
2. ✅ Read file capability (`POST /github/read-file` on `README.md`)
3. ✅ Create test PR (`POST /github/open-pr` with minimal change)

**Output:**
- Clear PASS/FAIL for each test
- PR URL if successful
- Error messages if failed

### 4. PR Automation Wrapper

**File:** `scripts/open_pr_for_branch.py`

**Purpose:** Simplified PR creation from slice branches

**Usage:**
```bash
python scripts/open_pr_for_branch.py \
  --branch feature/slice_governance_truth_bootstrap_v1 \
  --body-file governance_truth_pr_body.txt \
  --base main
```

**What it does:**
1. Validates branch exists and is pushed
2. Reads PR body from file
3. Calls MCP GitHub Client `/github/open-pr`
4. Returns PR URL

---

## 🔧 Implementation Plan

### Phase A: Configuration Setup (No Code Changes)

**Steps:**
1. Create `.env.template` with all required variables
2. Update `services/mcp_github_client/README.md` with setup instructions
3. Add `.env` to `.gitignore` (verify it's there)
4. Document PAT requirements (scopes: `repo`, `workflow`)

**Validation:**
- [ ] `.env.template` exists
- [ ] README has clear "Quick Start" section
- [ ] `.gitignore` includes `.env`

### Phase B: Service Launcher

**Steps:**
1. Create `run_service.bat` for Windows
2. Test service starts correctly
3. Verify `/health` endpoint responds

**Validation:**
- [ ] `run_service.bat` executes without errors
- [ ] Service accessible at `http://localhost:8081`
- [ ] `/health` returns 200 OK

### Phase C: Smoke Test

**Steps:**
1. Create `smoke_test_open_pr.py`
2. Implement 3 test stages (health → read → PR)
3. Use test branch: `feature/test_pr_automator`
4. Make minimal change (e.g., add comment to `services/mcp_github_client/TESTING.md`)

**Validation:**
- [ ] All 3 tests pass
- [ ] Test PR created successfully
- [ ] PR URL returned and accessible

### Phase D: PR Automation Wrapper

**Steps:**
1. Create `scripts/open_pr_for_branch.py`
2. Implement argument parsing (branch, body-file, base)
3. Add validation (branch exists, pushed, etc.)
4. Call MCP GitHub Client API
5. Handle errors gracefully

**Validation:**
- [ ] Script runs without errors
- [ ] Creates PR from existing branch
- [ ] Returns PR URL

---

## 🧪 Testing Strategy

### Manual Testing (Or performs)

**Step 1: Setup PAT**
1. Create GitHub PAT with `repo` scope
2. Add to `.env`: `GITHUB_TOKEN=ghp_...`

**Step 2: Start Service**
```bash
cd services/mcp_github_client
run_service.bat
```

**Step 3: Run Smoke Test**
```bash
python smoke_test_open_pr.py
```

**Expected Output:**
```
[1/3] Testing service health...
   [PASS] Service is running

[2/3] Testing file read...
   [PASS] Successfully read README.md

[3/3] Testing PR creation...
   [PASS] PR created: https://github.com/edri2or-commits/ai-os/pull/X

[SUCCESS] All tests passed!
```

**Step 4: Test Wrapper**
```bash
python scripts/open_pr_for_branch.py \
  --branch feature/slice_governance_truth_bootstrap_v1 \
  --body-file governance_truth_pr_body.txt
```

**Expected Output:**
```
✅ Branch exists: feature/slice_governance_truth_bootstrap_v1
✅ Branch pushed to origin
✅ PR body read: 5847 characters
✅ Calling MCP GitHub Client...
✅ PR created: https://github.com/edri2or-commits/ai-os/pull/Y

PR Details:
  Number: Y
  URL: https://github.com/edri2or-commits/ai-os/pull/Y
  Branch: feature/slice_governance_truth_bootstrap_v1 → main
```

---

## 🔒 Security Notes

### PAT Management

**Never commit:**
- `.env` file with actual PAT
- PAT in any script or config
- PAT in commit messages or logs

**Safe practices:**
- `.env` in `.gitignore` ✅
- `.env.example` with dummy values only ✅
- PAT with minimal required scopes (`repo` only) ✅
- PAT rotation every 90 days (future: add reminder)

### Service Security

**Current scope:** Local development only
- Service runs on `localhost:8081`
- No external access
- No CORS restrictions (local only)

**Future hardening (Phase 3+):**
- API key authentication
- Rate limiting
- Request validation
- Audit logging

---

## 📝 Success Criteria

### Must Have ✅

- [ ] MCP GitHub Client starts successfully with `run_service.bat`
- [ ] `smoke_test_open_pr.py` passes all tests
- [ ] Test PR created automatically
- [ ] `scripts/open_pr_for_branch.py` works for existing branches
- [ ] No PAT committed to repo
- [ ] Clear documentation in README

### Nice to Have 🎯

- [ ] Error messages are helpful
- [ ] Logs show what's happening
- [ ] Can handle branch name with special characters
- [ ] Validates PR body file exists

### Out of Scope ❌

- GitHub CLI (`gh`) authentication (separate slice if needed)
- Merging PRs automatically (requires approval workflow)
- Multi-repo support (AI-OS only for now)
- Deployed service (local development only)

---

## 🔗 Related

**Decisions:**
- DEC-003: Safe Git Policy (PR-first approach)
- DEC-010: Governance Truth Layer (snapshot automation foundation)

**Prerequisites:**
- GitHub PAT with `repo` scope (Or creates manually)
- Python 3.10+ with FastAPI, httpx, PyGithub

**Enables:**
- Automated PR creation from slices
- GPT Custom Actions integration (Phase 3)
- Consistent PR workflow across all agents

---

## 🎬 Next Steps (After This Slice)

1. **SLICE_GPT_ACTIONS_INTEGRATION_V1**
   - Connect GPT Custom Actions to MCP GitHub Client
   - Enable "Open PR" from ChatGPT

2. **SLICE_PR_APPROVAL_WORKFLOW_V1**
   - Add approval checklist
   - Human-in-the-loop confirmation
   - Auto-merge with approval

3. **SLICE_MULTI_SERVICE_ORCHESTRATION_V1**
   - Combine n8n + Agent Kernel + MCP GitHub Client
   - Scheduled snapshot + auto-PR workflow

---

**Status:** 🚧 In Progress  
**Created:** 2025-11-27  
**Last Updated:** 2025-11-27
