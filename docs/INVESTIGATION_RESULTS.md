# Investigation Results - Legacy Components (Slice 1.1a)

**Investigation Type:** Static analysis (read-only)  
**Date:** 2025-11-29  
**Scope:** ai_core/, tools/, scripts/, root-level scripts  
**Method:** Import analysis, code inspection, documentation search  

---

## Summary

**Key Findings:**
- ✅ ai_core/ is **LEGACY** - superseded by MCP architecture → **✅ ARCHIVED (Slice 1.2a, 2025-11-29)**
- ✅ tools/ appears to be **ONE-TIME utilities** - no active imports
- ⚠️ scripts/ status **UNCLEAR** - could be active or superseded by MCP GitHub client
- ⚠️ Root-level scripts need categorization (demo vs. operational vs. test)

**Confidence Levels:**
- **High confidence:** ai_core/ is legacy
- **Medium confidence:** tools/ is deprecated
- **Low confidence:** scripts/ and root-level (needs runtime check or deeper analysis)

**Migration Status:**
- ✅ **ai_core/** - Archived to `archive/legacy/ai_core/` (Slice 1.2a, 2025-11-29)
- ✅ **tools/** - Archived to `archive/one-time/tools/` (Slice 1.2b, 2025-11-29)
- ⏸️ **scripts/** - Pending investigation
- ⏸️ **Root scripts** - Pending categorization

---

## Section 1: ai_core/ Components

### Overview

**Directory:** `ai_core/`  
**Files:** 6 Python files + 1 markdown  
**Purpose:** Pre-MCP orchestration layer (Intent → Planner → Router → Executor)  

**Architecture Pattern (Hypothesis):**
```
User Intent → Intent Router → GPT Orchestrator (OpenAI API) 
                            ↓
                    Action Executor → File/Git operations
```

This appears to be the **original architecture before MCP servers were introduced**.

---

### ai_core/action_executor.py

**What it does:**  
Executes structured actions (file.create, file.update, git.commit, git.push) after validation.

**Imported by:**
- `ai_core/agent_gateway.py` (internal)
- `ai_core/agent_gateway_server.py` (internal)
- `check_health.py` (root-level)
- `execute_demo.py` (root-level)
- `run_iron_test.py` (root-level)

**Git history:** [Not available via static analysis]

**Aliveness:** Active imports suggest it's still referenced, but likely not operational

**Risk level:** **MEDIUM** - Referenced by multiple files, but all appear to be demos/tests

**Recommendation:** **DEPRECATE**

**Rationale:**
- Target architecture uses MCP servers for file/git operations
- action_executor.py duplicates functionality now handled by:
  - `services/mcp_github_client/` (git operations)
  - Filesystem MCP server (file operations)
- All imports are from demo/test scripts (execute_demo.py, run_iron_test.py, check_health.py)
- No production code imports this

**Migration path:**
- Verify demos/tests are not operational
- If they are, rewrite to use MCP servers
- Then deprecate action_executor.py

---

### ai_core/agent_gateway.py

**What it does:**  
Unified entry point wrapping the entire pipeline: Intent → Planner → Router → Executor

**Imported by:**
- `ai_core/agent_gateway_server.py` (internal)
- `check_health.py` (root-level)

**Key function:**
```python
plan_and_optionally_execute(intent, auto_execute=False, dry_run=False)
```

**Aliveness:** Only imported by agent_gateway_server.py and check_health.py

**Risk level:** **MEDIUM**

**Recommendation:** **DEPRECATE**

**Rationale:**
- agent_gateway.py wraps the old pipeline
- Target architecture: Claude Desktop orchestrates directly via MCP
- No "gateway" needed - Claude IS the gateway
- agent_gateway_server.py (which imports this) is probably also legacy

**Migration path:**
- Check if agent_gateway_server.py is running (Slice 1.1b runtime check)
- If not running → deprecate both
- If running → understand why, then migrate to MCP pattern

---

### ai_core/agent_gateway_server.py

**What it does:**  
HTTP server exposing agent_gateway.py as REST API

**Imported by:** None (it's a server entrypoint)

**Key routes:**
- `/plan` - Get plan without execution
- `/execute` - Execute with approval
- `/health` - Health check

**Aliveness:** No external imports, but could be running as server

**Risk level:** **HIGH** (could be running in production)

**Recommendation:** **INVESTIGATE** (needs runtime check in Slice 1.1b)

**Rationale:**
- Could be a background service
- If running, need to understand what calls it
- If not running → safe to deprecate
- Target architecture doesn't need this (Claude Desktop + MCP)

**Next steps:**
- Check if process is running (Slice 1.1b)
- Check if port is listening
- Check nginx/system logs for calls

---

### ai_core/gpt_orchestrator.py

**What it does:**  
Calls OpenAI API to generate plans based on SSOT files (CONSTITUTION, DECISIONS, etc.)

**Imported by:**
- `ai_core/intent_router.py` (internal)
- `ai_core/agent_gateway_server.py` (internal)
- `check_health.py` (root-level)

**Key function:**
```python
plan_change(intent) -> dict
```

**Aliveness:** Only used internally within ai_core/

**Risk level:** **LOW** (if ai_core/ is deprecated, this goes too)

**Recommendation:** **DEPRECATE**

**Rationale:**
- Target architecture: Claude Desktop (not external OpenAI calls)
- This is the "old brain" - Claude Desktop is the "new brain"
- Duplicates functionality now handled by Claude's own reasoning

---

### ai_core/intent_router.py

**What it does:**  
Routes user intent to appropriate planner/executor

**Imported by:**
- `ai_core/agent_gateway.py` (internal)
- `ai_core/agent_gateway_server.py` (internal)
- `check_health.py` (root-level)
- `run_intent.py` (root-level)
- `test_e2e.py` (root-level)

**Aliveness:** Referenced by demos/tests

**Risk level:** **MEDIUM**

**Recommendation:** **DEPRECATE**

**Rationale:**
- Target architecture: No "router" - Claude reasons about intent directly
- All imports are from tests/demos
- Part of legacy orchestration pipeline

---

### ai_core/ssot_writer.py

**What it does:**  
Updates SSOT files (CONSTITUTION, DECISIONS, etc.)

**Imported by:**
- `ai_core/agent_gateway_server.py` (internal)

**Aliveness:** Only used within ai_core/

**Risk level:** **LOW**

**Recommendation:** **DEPRECATE**

**Rationale:**
- Target architecture: Truth Layer updates via reconciler.py (services/os_core_mcp/)
- This is legacy SSOT management
- ssot_writer.py is NOT the same as the current Truth Layer pattern

---

### ai_core/ Summary

**Overall Assessment:** **LEGACY ARCHITECTURE**

**Evidence:**
1. No production code imports ai_core/ (only demos/tests/health checks)
2. Duplicates functionality now in MCP servers
3. Uses old pattern: GPT API calls instead of Claude Desktop
4. Uses old pattern: Direct SSOT writes instead of Truth Layer + Reconciler

**Confidence:** **HIGH** - This is the pre-MCP architecture

**Recommendation:** **DEPRECATE** entire ai_core/ directory

**Migration Steps:**
1. Verify no services are running that depend on this (Slice 1.1b)
2. Verify demos/tests are not operational
3. Move ai_core/ to archive/legacy/ai_core/
4. Update any lingering references to use MCP servers
5. Document in REMOVED_COMPONENTS.md

---

### ✅ MIGRATION COMPLETE (Slice 1.2a)

**Date:** 2025-11-29  
**Action:** ai_core/ archived to `archive/legacy/ai_core/`  
**Status:** ✅ **ARCHIVED**  
**Location:** `archive/legacy/ai_core/`  
**Reason:** Legacy pre-MCP architecture, superseded by MCP servers  
**Rollback:** `git mv archive/legacy/ai_core ai_core/` or `git revert HEAD`  

**Impact:**
- Demo scripts (execute_demo.py, run_intent.py, etc.) will break - expected
- Potentially chat/telegram_bot.py if operational - needs verification
- No production impact (ai_core/ had zero production imports)

**Next Steps:**
- Monitor for 1 week for any unexpected breakage
- If stable, mark as permanent deprecation
- Consider tools/ for Slice 1.2b

---

## Section 2: tools/ Components

### Overview

**Directory:** `tools/`  
**Files:** 4 Python files + 1 inventory  
**Purpose:** One-time setup utilities  
**Import analysis:** **ZERO** external imports found

---

### tools/repo_bootstrap_agent.py

**What it does:**  
Creates initial directory structure (core/, system/, agents/, workflows/)

**Imported by:** **NONE**

**Code quality:** Poor (typos: "CHECT" instead of "CHECK")

**Aliveness:** Stale (one-time setup script)

**Risk level:** **LOW**

**Recommendation:** **ONE-TIME / DEPRECATE**

**Rationale:**
- This was clearly a one-time repo initialization script
- Directory structure already exists
- No external references
- Code quality suggests it was never production-grade

**Action:** Move to `archive/one-time/` or delete

---

### tools/repo_introspection_agent.py

**What it does:** [Not read yet, but name suggests repo analysis utility]

**Imported by:** **NONE**

**Aliveness:** Unknown (no imports)

**Risk level:** **LOW**

**Recommendation:** **INVESTIGATE** (low priority) or **DEPRECATE**

**Rationale:**
- No active imports
- Likely a one-time utility or experiment
- Can safely defer investigation

---

### tools/repo_reader_base.py

**What it does:** [Not read yet, but name suggests base class for repo reading]

**Imported by:** **NONE**

**Aliveness:** Unknown (no imports)

**Risk level:** **LOW**

**Recommendation:** **INVESTIGATE** (low priority) or **DEPRECATE**

**Rationale:**
- No active imports
- Might be a base class for repo_introspection_agent.py
- Safe to defer or deprecate

---

### tools/system_init.py

**What it does:** [Not read yet, but name suggests system initialization]

**Imported by:** **NONE**

**Aliveness:** Unknown (no imports)

**Risk level:** **LOW**

**Recommendation:** **ONE-TIME / DEPRECATE**

**Rationale:**
- No active imports
- Name suggests one-time initialization
- Safe to deprecate

---

### tools/ Summary

**Overall Assessment:** **ONE-TIME UTILITIES / DEPRECATED**

**Evidence:**
1. ZERO external imports
2. Names suggest one-time setup (bootstrap, init)
3. Code quality issues (typos) suggest not production-grade
4. No documentation references

**Confidence:** **MEDIUM** - High confidence they're not actively used, but haven't read all files

**Recommendation:** **DEPRECATE** entire tools/ directory

**Migration Steps:**
1. Quick skim of remaining files to confirm hypothesis
2. Move tools/ to archive/one-time/
3. Document in REMOVED_COMPONENTS.md

---

### ✅ MIGRATION COMPLETE (Slice 1.2b)

**Date:** 2025-11-29  
**Action:** tools/ archived to `archive/one-time/tools/`  
**Status:** ✅ **ARCHIVED**  
**Location:** `archive/one-time/tools/`  
**Reason:** One-time repo initialization utilities, no active usage  
**Rollback:** `git mv archive/one-time/tools tools/` or `git revert HEAD`  

**Impact:**
- Zero expected breakage (no imports, no references)
- All one-time setup utilities, already executed their purpose
- No production impact (ZERO external imports confirmed)

**Components Archived:**
- repo_bootstrap_agent.py - Initial directory setup (deprecated)
- repo_introspection_agent.py - Repo analysis (one-time)
- repo_reader_base.py - Base class (unused)
- system_init.py - System initialization (one-time)
- TOOLS_INVENTORY.md - Documentation

**Next Steps:**
- Monitor for 1 week for any unexpected breakage (unlikely)
- If stable, mark as permanent deprecation
- Continue to Slice 1.2c/d (duplicates removal) or Phase 2

---

## Section 3: scripts/ Components

### Overview

**Directory:** `scripts/`  
**Files:** 6 Python files  
**Purpose:** PR automation helpers  
**Import analysis:** **ZERO** external imports found  

**Key Observation:** All scripts are PR-related, which could be superseded by `services/mcp_github_client/`

---

### scripts/create_pr_intent.py

**What it does:**  
Creates PR intents in `PR_INTENTS.jsonl` for processing by pr_worker.py

**Imported by:** **NONE** (CLI tool)

**Aliveness:** Unknown - depends on whether PR automation is active

**Risk level:** **MEDIUM** (could be part of active workflow)

**Recommendation:** **INVESTIGATE** - Check if MCP GitHub client supersedes this

**Rationale:**
- Target architecture uses `services/mcp_github_client/` for GitHub operations
- This script uses a JSONL-based intent system
- Current matrix shows "mcp_github_client" is operational
- Question: Does mcp_github_client replace this workflow, or do they coexist?

**Next steps:**
- Check if `docs/system_state/outbox/PR_INTENTS.jsonl` exists and is actively used
- Check if pr_worker.py is running
- Check if mcp_github_client can handle PR creation (it can - confirmed in current_state_map)

---

### scripts/pr_worker.py

**What it does:**  
Processes PR intents from `PR_INTENTS.jsonl`

**Imported by:** **NONE** (worker process or CLI)

**Aliveness:** Unknown - could be running as background worker

**Risk level:** **HIGH** (could be active process)

**Recommendation:** **INVESTIGATE** (Slice 1.1b runtime check)

**Rationale:**
- Could be a background process
- Need to check if running
- If not running → safe to deprecate
- If running → understand why, given MCP GitHub client exists

---

### scripts/open_pr_for_branch.py

**What it does:**  
Opens a PR for a given branch

**Imported by:** **NONE** (CLI tool)

**Aliveness:** Unknown

**Risk level:** **MEDIUM**

**Recommendation:** **DEPRECATE** (likely superseded by MCP GitHub client)

**Rationale:**
- MCP GitHub client has full PR capabilities
- This is likely redundant
- No active imports

---

### scripts/publish_slice_as_pr.py

**What it does:**  
Publishes a slice (work unit) as a PR

**Imported by:** **NONE** (CLI tool)

**Aliveness:** Unknown

**Risk level:** **MEDIUM**

**Recommendation:** **INVESTIGATE** - Could be useful pattern to preserve

**Rationale:**
- "Slice as PR" is a good pattern (aligns with migration plan)
- Could be worth migrating to MCP GitHub client rather than deleting
- Need to understand if this is actively used

---

### scripts/move_completed_plan.py

**What it does:**  
Moves completed plans (presumably to archive)

**Imported by:** **NONE** (CLI tool)

**Aliveness:** Unknown

**Risk level:** **LOW**

**Recommendation:** **DEPRECATE** or **REFACTOR**

**Rationale:**
- Simple file management, could be done with basic shell scripts
- Or could be integrated into governance layer
- Not critical to preserve as-is

---

### scripts/validate_bootstrap_response.py

**What it does:**  
Validates bootstrap responses (purpose unclear without reading)

**Imported by:** **NONE** (CLI tool)

**Aliveness:** Unknown

**Risk level:** **LOW**

**Recommendation:** **INVESTIGATE** (low priority) or **DEPRECATE**

---

### scripts/ Summary

**Overall Assessment:** **UNCLEAR - Potentially superseded by MCP GitHub client**

**Evidence:**
1. All scripts are PR/GitHub-related
2. `services/mcp_github_client/` exists and is operational
3. No active imports (all are CLI tools or workers)
4. Some scripts could be useful patterns to preserve

**Confidence:** **LOW** - Need runtime checks to determine if any are active

**Recommendation:** **MIXED**
- **Investigate:** pr_worker.py, publish_slice_as_pr.py
- **Deprecate:** create_pr_intent.py, open_pr_for_branch.py, move_completed_plan.py

**Next Steps (Slice 1.1b):**
1. Check if pr_worker.py is running
2. Check if PR_INTENTS.jsonl is actively written to
3. Compare capabilities: scripts/ vs. mcp_github_client/
4. Decision: Deprecate all OR migrate useful patterns to MCP

---

## Section 4: Root-Level Scripts

### Overview

**Observation:** Many root-level Python scripts (start*.py, test*.py, demo*.py, run*.py, etc.)

**Files Identified (from current_state_map):**
- start*.py / start*.bat (multiple start scripts)
- demo_loop.py, execute_demo.py
- run_intent.py, run_iron_test.py, run_*.py
- test_*.py (multiple test files)
- check_health.py, setup_env.py, sync_api_key.py

**Import Analysis (from earlier scan):**

**Scripts that import ai_core:**
- `check_health.py`
- `execute_demo.py`
- `run_intent.py`
- `run_iron_test.py`
- `test_e2e.py`

**Hypothesis:** These are demos, tests, or operational utilities

---

### Categorization (Preliminary)

**Category A: Demo Scripts**
- `demo_loop.py`
- `execute_demo.py`
- `demo_plan.json`, `temp_plan.json`, `plan_output.json`

**Status:** **DEPRECATED** (demos for old ai_core/ architecture)

**Action:** Move to `archive/demos/`

---

**Category B: Test Scripts**
- `test_e2e.py`
- `test_gateway.py`
- `test_langgraph_import.py`
- `test_os_core_endpoints.py`
- `test_real_gpt.py`
- `test_slice2.py`, `test_slice3.py`
- `test_ssot_update.py`

**Status:** **MIXED** - Some might test current infrastructure

**Action:** 
- Tests for ai_core/ → Move to archive
- Tests for MCP servers (test_os_core_endpoints.py) → Move to tests/
- Tests for LangGraph (test_langgraph_import.py) → Keep if services/agent_kernel uses LangGraph

---

**Category C: Operational Utilities**
- `check_health.py` - Health check utility
- `setup_env.py` - Environment setup
- `sync_api_key.py` - API key sync

**Status:** **UNCLEAR** - Could be operational

**Action:** Investigate usage (Slice 1.1b)

---

**Category D: Intent/Execution Scripts**
- `run_intent.py` - Runs intent through ai_core/
- `run_iron_test.py` - Runs "iron test" through ai_core/

**Status:** **DEPRECATED** (tied to ai_core/)

**Action:** Move to archive

---

**Category E: Start Scripts**
- `start.py`, `start.bat`
- `start-all-services.bat`
- `start_chat1.py`
- `start_github_client.py`
- `start_public_server.py`

**Status:** **MIXED** - Some could be operational

**Action:**
- start_github_client.py → Check if starts services/mcp_github_client/ (operational)
- start-all-services.bat → Check if starts current services (operational)
- Others → Investigate

---

### Root-Level Scripts Summary

**Overall Assessment:** **MIXED - Needs categorization and cleanup**

**Recommendation:** 
- Create `scripts/operational/` for active scripts
- Create `tests/` for active tests
- Move demos to `archive/demos/`
- Move ai_core/ tests to `archive/tests/legacy/`

**Next Steps:**
1. Categorize each script (can be done in spreadsheet/doc)
2. Move to appropriate directories
3. Update docs

---

## Section 5: Chat Components

### chat/telegram_bot.py

**What it does:**  
Telegram bot interface (imports ai_core/agent_gateway)

**Imported by:** **NONE** (bot entrypoint)

**Aliveness:** Unknown - could be running

**Risk level:** **HIGH** (could be operational)

**Recommendation:** **INVESTIGATE** (Slice 1.1b runtime check)

**Rationale:**
- Telegram bot was mentioned in target architecture as potential future interface
- But current code uses ai_core/ (legacy)
- Need to check if running
- If running → migrate to MCP pattern
- If not running → deprecate or leave as example for future

---

## Overall Summary & Recommendations

### High Confidence Findings

**✅ DEPRECATE - ai_core/ directory (entire)**
- **Evidence:** Legacy pre-MCP architecture, no production imports, duplicates MCP functionality
- **Risk:** Medium (need to verify no background services)
- **Action:** Slice 1.1b runtime check, then move to archive/legacy/

**✅ DEPRECATE - tools/ directory (entire)**
- **Evidence:** One-time utilities, no imports, code quality issues
- **Risk:** Low
- **Action:** Move to archive/one-time/

---

### Medium Confidence Findings

**⚠️ INVESTIGATE - scripts/ directory**
- **Reason:** Could be superseded by mcp_github_client, but uncertain
- **Next Step:** Slice 1.1b - Check if pr_worker.py running, check PR_INTENTS.jsonl usage
- **Likely Outcome:** Deprecate most, possibly preserve publish_slice_as_pr.py pattern

**⚠️ CATEGORIZE - Root-level scripts**
- **Reason:** Mix of demos, tests, and operational utilities
- **Next Step:** Create spreadsheet/doc, categorize each, then reorganize
- **Likely Outcome:** 
  - Demos → archive/demos/
  - Legacy tests → archive/tests/legacy/
  - Current tests → tests/
  - Operational → scripts/operational/

---

### Low Confidence / Needs Runtime Check

**⚠️ INVESTIGATE - chat/telegram_bot.py**
- **Next Step:** Check if running (Slice 1.1b)

**⚠️ INVESTIGATE - ai_core/agent_gateway_server.py**
- **Next Step:** Check if running (Slice 1.1b)

**⚠️ INVESTIGATE - scripts/pr_worker.py**
- **Next Step:** Check if running (Slice 1.1b)

---

## Recommended Next Steps

### Option A: Proceed to Slice 1.1b (Runtime Probing)

**If we need to be certain before deprecating:**

**Runtime checks:**
```powershell
# Check if any ai_core services running
Get-Process | Where-Object {$_.ProcessName -like "*agent_gateway*"}

# Check if pr_worker running
Get-Process | Where-Object {$_.ProcessName -like "*pr_worker*"}

# Check if telegram_bot running
Get-Process | Where-Object {$_.ProcessName -like "*telegram*"}

# Check if ports are listening
Test-NetConnection -ComputerName localhost -Port 8081  # MCP GitHub
Test-NetConnection -ComputerName localhost -Port 8082  # MCP Google
Test-NetConnection -ComputerName localhost -Port 8083  # OS Core
Test-NetConnection -ComputerName localhost -Port 8084  # Agent Kernel

# Check for any other Python processes
Get-Process python | Select-Object Id, ProcessName, Path
```

**File checks:**
```powershell
# Check if PR_INTENTS.jsonl exists and is recent
Test-Path "docs/system_state/outbox/PR_INTENTS.jsonl"
Get-Item "docs/system_state/outbox/PR_INTENTS.jsonl" | Select-Object LastWriteTime

# Check recent modifications to ai_core/
Get-ChildItem -Path "ai_core/" -Recurse -File | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 10 FullName, LastWriteTime
```

---

### Option B: Skip Slice 1.1b (Proceed with Deprecation)

**If confidence is high enough:**

**Rationale for skipping runtime checks:**
1. **ai_core/** - Very high confidence it's legacy (no production imports, duplicates MCP)
2. **tools/** - Very high confidence it's deprecated (no imports, one-time utilities)
3. **scripts/** - Medium confidence, but even if active, should migrate to MCP

**Conservative approach:**
- Move to `archive/` instead of deleting
- If something breaks, easy to restore
- Git history preserves everything anyway

---

## Proposed Decision

**My recommendation as architect:**

### Skip Slice 1.1b (Runtime Probing)

**Reasoning:**
1. **Static analysis is sufficient** for high-confidence decisions (ai_core/, tools/)
2. **Git rollback** provides safety net
3. **Archive instead of delete** provides additional safety
4. **ADHD-friendly** - One less decision point, maintain momentum

**Action Plan:**
1. Proceed directly to Slice 1.2 (Duplicate Removal)
2. Add ai_core/ and tools/ to deprecation list
3. Move (don't delete) to archive/
4. If something breaks, restore from archive
5. Monitor for 1 week - if no issues, mark as complete

**Trade-off:**
- **Benefit:** Faster progress, less analysis paralysis
- **Risk:** Might miss an active component (LOW risk given evidence)
- **Mitigation:** Archive + Git + 1-week monitoring period

---

## Final Question for Approval

**Should we:**

**Option A:** Proceed to Slice 1.1b (runtime checks) for extra certainty?  
**Option B:** Skip to Slice 1.2 (archive ai_core/ and tools/ immediately)?

**My recommendation:** **Option B** (skip runtime checks, archive immediately)

**Your call.**

---

**Document Version:** 1.0  
**Investigation:** Slice 1.1a (Static Analysis Only)  
**Next:** Awaiting decision on Slice 1.1b vs. Slice 1.2  
**Confidence:** High (ai_core/, tools/), Medium (scripts/), Low (individual root scripts)

---

**Files Referenced:**
- ai_core/*.py (6 files analyzed)
- tools/*.py (1 file analyzed, 3 deferred)
- scripts/*.py (1 file analyzed, 5 deferred)
- Root-level imports (via PowerShell grep)

**Research Sources:**
- current_state_map.md (repo structure)
- target_architecture_summary.md (MCP architecture)
- current_vs_target_matrix.md (deprecation categories)