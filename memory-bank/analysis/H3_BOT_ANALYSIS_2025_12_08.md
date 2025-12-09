# Multi-Model + Telegram Bot Integration Analysis

**Date:** 2025-12-08  
**Context:** Review existing H3 Telegram Bot before Phase 2.6 implementation

---

## 🔍 FINDINGS

### ✅ H3 Telegram Approval Bot - EXISTS AND IS GOOD!

**Location:** `services/approval-bot/`

**What It Does:**
- ✅ Async approval workflow (Change Requests via Telegram)
- ✅ File-based system (watches `truth-layer/drift/approvals/pending/`)
- ✅ FastAPI backend (356 lines, clean code)
- ✅ SQLite queue management
- ✅ Inline buttons (Approve/Reject)
- ✅ Already tested and working

**Architecture:**
```
Reconciler → CR YAML → Backend (watchdog) → Telegram notification
    ↓
User clicks ✅/❌
    ↓
Backend writes approval file → Executor applies → Git commit
```

**Status:** ✅ PRODUCTION READY (from H3 phase)

---

## 💡 DECISION: Reuse H3 Bot + Extend for Multi-Model

**Why NOT start from scratch:**
1. ✅ Code quality is good (clean, async, tested)
2. ✅ Architecture fits Multi-Model needs perfectly
3. ✅ Already integrated with `.env` (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
4. ✅ File-based workflow = easy to extend
5. ✅ No "legacy debt" - this was built recently with best practices

**What We'll Add to H3 Bot:**
- `/status` - Show system status (LiteLLM, n8n, models health)
- `/costs` - Daily/monthly API spending per model
- `/switch` - Manually switch model priority
- `/logs` - Recent LLM calls from Langfuse
- Multi-model Change Requests (when Observer detects multi-model conflicts)

**What Stays the Same:**
- ✅ Core approval workflow (CR → Telegram → approve → execute)
- ✅ Database structure
- ✅ File watching mechanism
- ✅ Authentication (CHAT_ID whitelist)

---

## 📋 UPDATED PLAN: H2 Phase 2.6 with H3 Bot Integration

### Modified Slice 6: Telegram Bot Extension (was: "End-to-End Test")

**Old Goal:** Test Telegram → n8n → LiteLLM  
**New Goal:** Extend H3 bot with multi-model commands + keep approval workflow

**Changes to services/approval-bot/backend.py:**

1. Add command handlers:
   ```python
   @app.command("status")
   async def status_command(update, context):
       # Check LiteLLM health, n8n, models
       # Return: "✅ GPT-4: OK, Claude: OK, Gemini: OK"
   
   @app.command("costs")
   async def costs_command(update, context):
       # Query Langfuse for today's spending
       # Return: "GPT-4: $2.50, Claude: $1.20, Gemini: $0.05"
   ```

2. Extend CR types to include multi-model conflicts:
   ```python
   # New CR type: MULTI_MODEL_CONFLICT
   # When GPT and Claude both modify same resource
   ```

**Duration:** 90 min → 120 min (added 30 min for new commands)

---

## 🔧 REQUIRED UPDATES (Critical!)

### 1. Model Versions (End of 2025)

**WRONG (in current plan):**
- ❌ Claude 3.5 Sonnet
- ❌ GPT-4 Turbo
- ❌ Gemini 2.0 Flash

**CORRECT (December 2025):**
- ✅ **Claude 4.5 Sonnet** (`anthropic/claude-sonnet-4-5-20250929`)
- ✅ **GPT-5.1** (`openai/gpt-5.1`)
- ✅ **Gemini 3 Pro** (`gemini/gemini-3-pro`)

**Files to Update:**
- `memory-bank/plans/H2_PHASE_2.6_MULTI_MODEL_PLAN.md` (all model references)
- `litellm-config.yaml` (when we create it)
- `memory-bank/docs/CREDENTIALS_REFERENCE.md` (documentation)

---

## 🎯 INTEGRATION STRATEGY

### Phase 2.6 Slice Order (Modified)

**Slices 1-5:** As planned (LiteLLM setup, n8n routing, fallbacks)  
**Slice 6 (NEW):** Extend H3 bot for multi-model  
**Slices 7-12:** As planned (Event Sourcing, production hardening)

---

## 📊 H3 Bot Current State

**Pros:**
- ✅ Clean codebase
- ✅ Production-tested
- ✅ Async architecture (aiogram)
- ✅ File-based workflow (easy to extend)
- ✅ SQLite state management
- ✅ Inline keyboard UX

**Cons (Minor):**
- ⚠️ No command handlers yet (only approval callbacks)
- ⚠️ Not deployed to VPS (still local, but that's H4)
- ⚠️ No cost tracking integration

**Risk Assessment:** ✅ LOW RISK to reuse and extend

---

## 🚀 RECOMMENDATION

**DO NOT start from scratch.**  
**EXTEND H3 bot with multi-model features.**

**Rationale:**
1. Saves 3-4 hours of bot setup work
2. Maintains code quality (H3 bot is well-architected)
3. Unified approval system (one bot for all HITL needs)
4. Natural evolution (Phase 2.6 builds on H3, not replaces it)

**Updated Timeline:**
- Slice 6: 90 min → 120 min (added multi-model commands)
- Total: 10.5 hours → 11 hours (30 min increase)

---

## ✅ ACTION ITEMS

**Before starting Slice 1:**
1. ✅ Update H2_PHASE_2.6_MULTI_MODEL_PLAN.md (model versions)
2. ✅ Update Slice 6 description (Telegram bot extension)
3. ✅ Document H3 bot structure (for future reference)
4. ✅ Verify H3 bot still runs locally (quick test)

**During Slice 6:**
1. Add `/status` command (LiteLLM + models health)
2. Add `/costs` command (Langfuse query)
3. Extend CR types (MULTI_MODEL_CONFLICT)
4. Test: Send command → bot responds

---

## 📝 NOTES

- H3 bot token: `8119131809:AAH...` (in vps.env)
- Chat ID: `5786217215` (Or's Telegram)
- Database: `services/approval-bot/approvals.db` (SQLite)
- Backend: `services/approval-bot/backend.py` (356 lines)

**Last H3 Commit:** e0f8f17 on feature/h2-memory-bank-api  
**Last H3 Test:** ✅ PASSED (manual CR → Telegram → approval → DB update)

---

**Conclusion:** H3 bot is a solid foundation. Extend it, don't replace it.