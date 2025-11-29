# Legacy Components Archive

**Purpose:** This directory contains deprecated legacy code that has been superseded by newer architecture.

**Status:** ARCHIVED - Not for active use

**Reason:** These components were part of earlier architectural iterations and have been replaced by modern equivalents.

---

## Contents

### archive/legacy/ai_core/

**Archived:** 2025-11-29 (Slice 1.2a)  
**Reason:** Legacy pre-MCP orchestration layer  
**Superseded by:** MCP servers (services/mcp_github_client/, filesystem MCP, etc.) + Claude Desktop orchestration  

**Components:**
- `action_executor.py` - Legacy file/git operations → MCP servers
- `agent_gateway.py` - Legacy unified entry point → Claude Desktop
- `agent_gateway_server.py` - Legacy HTTP server → No longer needed
- `gpt_orchestrator.py` - Legacy OpenAI planner → Claude Desktop reasoning
- `intent_router.py` - Legacy intent router → Claude Desktop direct orchestration
- `ssot_writer.py` - Legacy SSOT updater → Truth Layer + Reconciler pattern

**Old Architecture:**
```
User Intent → Intent Router → GPT Orchestrator (OpenAI API) → Action Executor → File/Git ops
```

**New Architecture:**
```
User → Claude Desktop → MCP Servers → File/Git/etc. ops
```

**Documentation:**
- Investigation: `docs/INVESTIGATION_RESULTS.md`
- Migration: `claude project/system_mapping/migration_plan.md`
- Commit: `COMMIT_MSG_SLICE_1_2a.txt`

**Rollback:**
```bash
# If needed, restore with:
git mv archive/legacy/ai_core ai_core/
# Or:
git revert <commit-hash>
```

---

## Why Archive Instead of Delete?

1. **Git History:** Preserve code for historical reference
2. **Safety:** Easy to restore if needed
3. **Learning:** Understand past architectural decisions
4. **Documentation:** Reference for migration context

---

## Maintenance

- **DO NOT** modify files in this directory
- **DO NOT** import from archived components
- **DO** refer to this archive for historical context
- **DO** remove after confirming stable migration (1-4 weeks)

---

**Last Updated:** 2025-11-29  
**Migration Phase:** Phase 1 (Investigation & Cleanup)  
**Next Review:** 2025-12-06 (1 week monitoring period)
