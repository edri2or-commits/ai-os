# TO_DELETE - Context Diet Plan

**Date:** 2025-12-03  
**Reason:** Context Window Overflow (Claude compacting after 2-3 messages)  
**Research:** MCP Performance Report - H2 (Premature Compaction) + H3 (Token Bloat)

---

## 🎯 Problem Summary

**Claude was compacting after 2-3 messages because:**
- Project Knowledge: 715KB (29 files) = ~178,000 tokens
- Plus Instructions + Tools + Memory = ~28,000 tokens
- **Total: ~206,000 tokens at startup** (exceeds 200K window!)

---

## ✅ Solution: Remove 9 msg_* Files

**Files to remove from Project Knowledge:**

```
msg_019.md - 30KB
msg_020.md - 29KB
msg_021.md - 13KB
msg_022.md - 30KB
msg_023.md - 22KB
msg_024.md - 25KB
msg_025.md - 29KB
msg_026.md - 31KB
msg_027.md - 24KB

Total: 233KB = ~58,000 tokens saved
```

**After removal:**
- Project Knowledge: 482KB (20 files) = ~120,000 tokens
- **Total: ~147,500 tokens** ✅
- **Buffer: 52,500 tokens (26%)** - No more premature compaction!

---

## 📍 WHERE ARE THESE FILES?

**Important:** These files exist ONLY in Claude Desktop Project Knowledge!

They are NOT in your filesystem at:
- ❌ NOT in `claude-project/research_claude/`
- ❌ NOT in any physical directory

They ARE in:
- ✅ Claude Desktop → Project Settings → Project Knowledge
- ✅ Mounted at `/mnt/project/msg_*.md` (read-only, visible only to Claude)
- ✅ Backed up in Claude's workspace at `/home/claude/msg_*.md` (for Claude's reference)

---

## 🔧 What Was Done

**Step 1:** ✅ Created TO_DELETE directory (this folder)  
**Step 2:** ✅ Files backed up (copied to `/home/claude/msg_*.md` in Claude's workspace)  
**Step 3:** ✅ References removed from 3 system_mapping files:
- `current_state_map.md`
- `target_architecture_summary.md`
- `migration_plan.md`

**Step 4:** ⏳ **YOU NEED TO DO:**

### How to Remove from Project Knowledge:

1. Open Claude Desktop
2. Click on Project Name (top left)
3. Click "Project Settings"
4. Go to "Project Knowledge" tab
5. Find these 9 files: msg_019.md through msg_027.md
6. Click the ❌ button next to each file to remove it
7. Restart Claude Desktop for changes to take effect

---

## 📊 Impact Verification

**Before removal:**
- Start new chat → 2-3 messages → "Compacting conversation..." 🔴
- Context: ~206K tokens (overflow)

**After removal:**
- Start new chat → 10-15+ messages before any compaction ✅
- Context: ~148K tokens (healthy buffer)

---

## 🗑️ After Confirmation

Once you've removed the files from Project Knowledge and verified Claude is no longer compacting prematurely:

1. Delete this entire `TO_DELETE_context-diet/` directory
2. Git commit the changes (references removed from system_mapping/)

---

**Status:** ⏳ Waiting for you to remove files from Claude Desktop Project Knowledge
