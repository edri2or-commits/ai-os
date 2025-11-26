# BLOCK_POWERSHELL_STABILITY_AND_HEALTHCHECK_V1

**Status:** 📋 Open (Not Started)  
**Created:** 2025-11-26  
**Priority:** Medium  
**Related Incident:** EVT-2025-11-26-INCIDENT-001  
**Owner:** Claude Desktop  
**Phase:** 2.3 or 2.4

---

## 🎯 Purpose

Investigate and resolve PowerShell reliability issues in AI-OS infrastructure operations.

**Context:**  
PowerShell commands used for file operations, JSON updates, and system tasks frequently fail silently (Status Code: 1, no error message) during blocks. This creates friction, requires workarounds mid-block, and reduces confidence in PowerShell as an infrastructure tool.

---

## 📊 Current State

### Where PowerShell is Used Today

1. **File Operations:**
   - JSON file updates (SYSTEM_STATE_COMPACT, SERVICES_STATUS)
   - Text replacements in configuration files
   - Batch operations on multiple files

2. **System Operations:**
   - Service management (Docker, ngrok)
   - Process monitoring
   - Environment variable management

3. **Git Operations:**
   - Repository status checks
   - File staging and commits (via git CLI)

### Known Failure Patterns

| Incident | Date | Command Type | Failure Mode | Workaround |
|----------|------|--------------|--------------|------------|
| EVT-2025-11-26-INCIDENT-001 | 2025-11-26 | JSON string replacement | Status Code: 1, no error | Used Filesystem:edit_file |

---

## 🔍 Investigation Needed

### 1. Root Cause Analysis

**Questions to answer:**
- Why do PowerShell commands return Status Code: 1 without error messages?
- Is this an encoding issue (UTF-8 vs UTF-16)?
- Is this a path issue (Windows paths, backslashes, special chars)?
- Is this a permissions issue?
- Is this a PowerShell version issue (5.1 vs 7+)?

### 2. Environment Check

**What to verify:**
- PowerShell version in use (Windows PowerShell 5.1 vs PowerShell 7+)
- Default encoding settings
- Execution policy
- Available cmdlets and modules
- Error handling configuration ($ErrorActionPreference)

### 3. Tool Comparison

**Alternatives to test:**
- Filesystem MCP tools (already working well)
- bash_tool (available but less tested)
- autonomous-control:execute_command with CMD (proven to work)
- Direct Python scripts
- Git bash commands

---

## 🎯 Proposed Solution Phases

### Phase 1: Diagnosis (Quick Win)

**Goal:** Understand what's failing and why

**Tasks:**
- [ ] Run PowerShell diagnostics script
- [ ] Document current PowerShell environment
- [ ] Identify specific failure scenarios

**Output:** Diagnostic report with findings

### Phase 2: Quick Fixes (If Available)

**Possible fixes:**
- Switch to PowerShell 7 if on 5.1
- Set explicit encoding for all file operations
- Use `-ErrorAction Stop` to force proper error reporting
- Add try-catch blocks to all PowerShell operations

### Phase 3: Standardization

**Goal:** Create reliable patterns OR standardize on alternatives

**Decision Matrix:**
- **Use CMD (via autonomous-control) for:** Git operations, file system navigation
- **Use Filesystem tools for:** File read/write, JSON updates, text replacements
- **Use PowerShell for:** Windows-specific system operations (if reliable)

---

## 📋 Acceptance Criteria

1. ✅ PowerShell environment documented and understood
2. ✅ Root cause of silent failures identified
3. ✅ Decision made: Fix PowerShell OR standardize on alternative tools
4. ✅ Best practices documented
5. ✅ At least 3 consecutive infrastructure operations succeed without workarounds
6. ✅ No new `infra_incident` events with same failure mode for 1 week

---

## 🔗 Related

**Incidents:** EVT-2025-11-26-INCIDENT-001  
**GAPs:** GAP-005  
**Decisions:** (Future) DEC-008

---

**Last Updated:** 2025-11-26  
**Updated By:** Claude Desktop (NO-KOMBINOT policy implementation)
