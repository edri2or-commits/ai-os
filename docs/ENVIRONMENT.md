# AI Life OS - Environment Documentation

**Last Updated:** 2025-12-02  
**Status:** ✅ Stable & Operational

---

## System Overview

**Machine:** Windows 11 native (no WSL)  
**User:** edri2  
**Primary Workspace:** `C:\Users\edri2\Desktop\AI\ai-os`

---

## Core Components

### 1. Python Environment
- **Version:** Python 3.14.0
- **Location:** `C:\Program Files\Python314\`
- **Installed Packages:**
  - `jsonschema` (4.25.1)
  - `pyyaml`
  - `attrs` (25.4.0)
  - `referencing` (0.37.0)
  - `rpds-py` (0.30.0)

### 2. Git
- **Location:** `C:\Program Files\Git\cmd\git.exe`
- **Status:** ✅ Operational
- **Remote:** https://github.com/edri2or-commits/ai-os

### 3. Claude Desktop + MCP Servers
- **Desktop Commander:** v0.2.23 ✅ Fully Operational
  - Node version: 22.21.1
  - Default shell: `powershell.exe`
  - Blocked commands: 32 safety rules active
- **Filesystem MCP:** ✅ Active
- **Windows-MCP:** ✅ Active (UI automation)
- **Google MCP:** ✅ Available (edri2or@gmail.com)

---

## Key Paths

```
Main Repo:          C:\Users\edri2\Desktop\AI\ai-os
Claude Project:     C:\Users\edri2\Desktop\AI\ai-os\claude-project
Research Files:     C:\Users\edri2\Desktop\AI\ai-os\claude-project\research_claude
Memory Bank:        C:\Users\edri2\Desktop\AI\ai-os\memory-bank
Tools:              C:\Users\edri2\Desktop\AI\ai-os\tools
System State:       C:\Users\edri2\Desktop\AI\ai-os\docs\system_state
```

---

## Resolved Technical Issues

### TD-002: Windows MCP stdout Capture Failure
- **Status:** ✅ RESOLVED (2025-12-02)
- **Solution:** Desktop Commander MCP (v0.2.23)
- **Impact:** Full subprocess stdout/stderr capture now working
- **Details:** See `docs/technical_debt/TD-002-windows-mcp-stdout.md`

---

## Known Limitations

### Console Encoding (Non-Critical)
- **Issue:** Windows console (cp1255) doesn't support emoji rendering
- **Workaround:** Set `PYTHONIOENCODING=utf-8` when needed
- **Impact:** Cosmetic only - functionality unaffected
- **Status:** Not blocking development

### Pre-commit Hook
- **Issue:** `.git/hooks/pre-commit` is batch file (doesn't run with Git)
- **Status:** Using `git commit --no-verify` as workaround
- **Priority:** Low (safety checks happen in CI/reconciler)

---

## Testing & Validation

### Reconciler Tool (tools/reconciler.py)
- ✅ All commands operational: `generate`, `list`, `show`, `approve`, `reject`, `apply`
- ✅ Git safety rules validated (working tree checks)
- ✅ Schema validation working
- ✅ Dry-run mode tested

### Desktop Commander Validation
```powershell
# Verified commands:
DC:get_config          → Full system configuration retrieved
DC:start_process       → Python subprocess spawned successfully
DC:read_process_output → stdout/stderr captured completely
DC:list_directory      → Recursive directory listing working
DC:edit_block          → Surgical file edits successful
```

---

## Development Workflow

### Standard Command Pattern
```powershell
# Working directory
cd C:\Users\edri2\Desktop\AI\ai-os

# Python with UTF-8 (if emoji needed)
$env:PYTHONIOENCODING='utf-8' ; python tools\reconciler.py list

# Git operations
git status --short
git add .
git commit --no-verify -m "feat: description"
git push origin main
```

### MCP Tool Access
All operations go through Desktop Commander:
- File operations: `DC:read_file`, `DC:write_file`, `DC:edit_block`
- Process execution: `DC:start_process`, `DC:interact_with_process`
- System queries: `DC:get_config`, `DC:list_directory`

---

## Security & Safety

### Git Safety Rules (Reconciler)
1. ✅ Must be in git repository root
2. ✅ Working tree must be clean (no uncommitted changes)
3. ✅ Must not run if git status shows modifications
4. ✅ All changes are atomic and reversible

### Desktop Commander Blocked Commands
32 dangerous system commands blocked including:
- `mkfs`, `format`, `diskpart`
- `shutdown`, `reboot`
- `rm -rf /`, `del /f /s /q`
- Full list in DC config

---

## Next Steps

1. ✅ Desktop Commander operational
2. ✅ TD-002 resolved
3. ✅ Python environment stable
4. 🎯 Ready for Observer System (Slice 2.6)
5. 🎯 Ready for autonomous drift detection

---

**Maintainer:** Or (edri2or@gmail.com)  
**Architecture:** Personal AI Life OS - Phase 2 (Core Infrastructure)
