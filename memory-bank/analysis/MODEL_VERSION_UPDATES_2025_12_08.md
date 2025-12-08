# Model Version Updates - Dec 2025

**Date:** 2025-12-08  
**Context:** Correct model versions for end of 2025

---

## ✅ CORRECTED MODEL VERSIONS

### Old (Wrong)
- ❌ Claude 3.5 Sonnet (`anthropic/claude-3-5-sonnet-20241022`)
- ❌ GPT-4 Turbo (`openai/gpt-4-turbo`)
- ❌ Gemini 2.0 Flash (`gemini/gemini-2.0-flash-exp`)

### New (Correct - December 2025)
- ✅ **Claude 4.5 Sonnet** (`anthropic/claude-sonnet-4-5-20250929`)
- ✅ **GPT-5.1** (`openai/gpt-5.1`)
- ✅ **Gemini 3 Pro** (`gemini/gemini-3-pro`)

---

## 📋 FILES UPDATED

### 1. H2_PHASE_2.6_MULTI_MODEL_PLAN.md
- ✅ Header: Added model versions note
- ✅ Vision diagram: Updated model names
- ✅ Slice 1: Updated model_list configuration

**Changes:**
```yaml
# OLD
model_list:
  - model_name: gpt-4
    litellm_params:
      model: openai/gpt-4-turbo
  - model_name: claude-3
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20241022
  - model_name: gemini-2
    litellm_params:
      model: gemini/gemini-2.0-flash-exp

# NEW
model_list:
  - model_name: gpt-5.1
    litellm_params:
      model: openai/gpt-5.1
  - model_name: claude-4.5
    litellm_params:
      model: anthropic/claude-sonnet-4-5-20250929
  - model_name: gemini-3-pro
    litellm_params:
      model: gemini/gemini-3-pro
```

### 2. H3_BOT_ANALYSIS_2025_12_08.md
- ✅ Created new analysis document
- ✅ Documented model version corrections
- ✅ H3 bot reuse strategy

### 3. CREDENTIALS_REFERENCE.md
- ⏳ TODO: Update with correct model strings

---

## 🔧 REMAINING UPDATES NEEDED

### High Priority (Before Slice 1)
1. **Search entire H2_PHASE_2.6_MULTI_MODEL_PLAN.md for:**
   - `gpt-4` → replace with `gpt-5.1`
   - `claude-3` → replace with `claude-4.5`
   - `gemini-2` → replace with `gemini-3-pro`
   - `3-5-sonnet` → replace with `4-5 sonnet`
   - `4-turbo` → replace with `5.1`
   - `2.0-flash` → replace with `3-pro`

2. **Update cost calculations:**
   - GPT-5.1 pricing (check OpenAI pricing page)
   - Claude 4.5 pricing (check Anthropic pricing page)
   - Gemini 3 Pro pricing (check Google AI pricing page)

3. **Verify model capabilities:**
   - Claude 4.5: Context window size
   - GPT-5.1: New features/improvements
   - Gemini 3 Pro: Performance benchmarks

### Medium Priority (During Slice 6)
4. **Update Telegram bot commands:**
   - `/status` should show correct model versions
   - `/costs` should use correct pricing

### Low Priority (Documentation)
5. **Update README files:**
   - services/approval-bot/README.md
   - Any other docs mentioning model versions

---

## 📊 MODEL COMPARISON (End of 2025)

| Model | Context Window | Cost (1M in/out) | Best For |
|-------|---------------|------------------|----------|
| GPT-5.1 | 128K | $3/$12 (est) | Complex reasoning, coding |
| Claude 4.5 | 200K | $3/$15 | Long documents, analysis |
| Gemini 3 Pro | 32K | $0.15/$0.60 | Speed, cost efficiency |

**Notes:**
- Prices are estimates (verify with provider)
- Context windows are approximate
- Claude 4.5 introduced multimodal capabilities
- GPT-5.1 has improved math/coding
- Gemini 3 Pro has better multilingual support

---

## ✅ VERIFICATION CHECKLIST

Before starting Slice 1:
- [ ] All model strings updated in plan
- [ ] Cost calculations verified
- [ ] Model capabilities documented
- [ ] H3 bot integration confirmed
- [ ] API keys tested with new models

---

**Status:** IN PROGRESS  
**Next:** Complete remaining search/replace operations