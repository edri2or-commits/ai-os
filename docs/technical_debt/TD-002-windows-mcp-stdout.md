# TD-002: Windows PowerShell MCP stdout/stderr Capture Failure

**Date Identified:** 2025-12-01  
**Severity:** HIGH (blocks validation of high-risk operations)  
**Component:** Windows-MCP / Powershell-Tool  
**Discovered During:** Slice 2.4c apply flow testing

---

## Problem

Windows PowerShell MCP tool fails to reliably capture stdout/stderr from Python subprocess executions:

**Symptoms:**
- Python commands execute (exit code 0)
- NO stdout/stderr visible in MCP response
- File redirects (e.g., `> output.txt 2>&1`) produce EMPTY files
- `Out-String`, `Tee-Object`, direct file writes all fail

**Impact:**
- **BLOCKS** validation of `reconciler.py apply` via MCP
- **BREAKS** HITL protocol observability requirements
- Forces manual CLI usage (defeats automation purpose)

---

## Examples

```powershell
# This returns exit code 0 but NO output visible:
& "C:\Program Files\Python314\python.exe" tools\reconciler.py apply --dry-run

# File redirect produces EMPTY file:
& "C:\Program Files\Python314\python.exe" tools\reconciler.py apply --dry-run > output.txt 2>&1
# output.txt exists but is 0 bytes

# Even basic Python print fails:
& "C:\Program Files\Python314\python.exe" -c "print('test')"
# Returns exit 0, but no "test" in output
```

---

## Root Cause (Hypothesis)

PowerShell MCP may be:
1. Running in a restricted execution context that suppresses subprocess stdout
2. Using wrong stream capture mechanism for Windows processes
3. Hitting encoding issues (Python outputs UTF-8, PowerShell expects different encoding)

---

## Workarounds Attempted (all failed)

- ❌ `Out-String`
- ❌ `Tee-Object`
- ❌ File redirects (`>`, `2>&1`)
- ❌ `$output = & python ...`
- ❌ Setting `$OutputEncoding`

---

## Impact on 2.4c

**Slice 2.4c Status:**
- ✅ Code implementation COMPLETE (280 lines, all 5 Safety Rules implemented)
- ✅ Spec documentation COMPLETE
- ❌ End-to-end validation BLOCKED (cannot observe dry-run/apply output)

**What works:**
- Code compiles
- Git operations work (we can verify git status)
- File reads work (can check CR files, entity files, apply.log)

**What's blocked:**
- Cannot see dry-run preview output
- Cannot see apply progress indicators
- Cannot observe safety rule violations in real-time
- Cannot validate commit messages without checking git log manually

---

## Required Fix

One of:
1. Fix Windows-MCP Powershell-Tool to properly capture subprocess stdout/stderr
2. Switch to different shell tool (bash via WSL?)
3. Implement file-based logging for all reconciler operations (workaround)

---

## Temporary Mitigation

Until fixed:
- `reconciler.py apply` is **available for manual use** in direct PowerShell
- User must run commands themselves with runbook/safety rules
- **DO NOT** attempt MCP-based apply operations
- Validation must be post-facto (check git log, apply.log, file contents)

---

## Next Steps

1. **Investigate** Windows-MCP source code for subprocess handling
2. **Test** alternative shell execution methods
3. **File issue** with Windows-MCP maintainers if confirmed bug
4. **Consider** adding comprehensive file-based logging to reconciler as workaround
