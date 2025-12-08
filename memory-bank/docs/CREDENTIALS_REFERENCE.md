# Credentials Reference - DO NOT ASK USER

**Purpose:** This file exists to STOP Claude from asking about API keys repeatedly.

---

## 🔐 Credentials Location

**PRIMARY SOURCE (Always Use This):**
```
C:\Users\edri2\Desktop\AI\ai-os\vps.env
```

---

## 📋 Available API Keys

The following credentials are available in `vps.env`:

| Service | Environment Variable | Status |
|---------|---------------------|--------|
| OpenAI | `OPENAI_API_KEY` | ✅ Active |
| Anthropic (Claude) | `ANTHROPIC_API_KEY` | ✅ Active |
| Google (Gemini) | `GOOGLE_API_KEY`, `GEMINI_API_KEY` | ✅ Active |
| GitHub | `GITHUB_PAT` | ✅ Active |
| Telegram Bot | `TELEGRAM_BOT_TOKEN` | ✅ Active |
| n8n | `N8N_API_KEY` | ✅ Active |
| Qdrant | `QDRANT__SERVICE__API_KEY` | ✅ Active |
| Langfuse | `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` | ⏳ Pending setup |

---

## 🚨 CRITICAL RULE FOR ALL CLAUDE INSTANCES

**WHEN YOU NEED AN API KEY:**

1. ❌ **DO NOT** ask the user "Do you have an API key?"
2. ❌ **DO NOT** ask "Where is your API key stored?"
3. ✅ **DO** read from `C:\Users\edri2\Desktop\AI\ai-os\vps.env`
4. ✅ **DO** use Desktop Commander to read the file
5. ✅ **DO** extract the specific key you need

**Example (Correct Behavior):**
```
User: "Add LiteLLM to docker-compose"
Claude: [Reads vps.env] → [Uses OPENAI_API_KEY and ANTHROPIC_API_KEY] → [Creates config]
```

**Example (WRONG Behavior - NEVER DO THIS):**
```
User: "Add LiteLLM to docker-compose"
Claude: "Do you have OpenAI and Anthropic API keys? Where are they stored?"
❌ THIS CREATES FRICTION AND WASTES TIME
```

---

## 🎯 Why This File Exists

**ADHD-Aware Design Principle:**
- **Problem:** Repeatedly asking for API keys = unnecessary context switching
- **Solution:** Document location once, reference automatically
- **Result:** Frictionless development, no repeated questions

---

## 🔄 When to Update This File

- New API key added to `vps.env` → Update this table
- API key location changes → Update PRIMARY SOURCE path
- Never delete this file without creating a replacement

---

**Created:** 2025-12-08  
**Last Updated:** 2025-12-08  
**Maintenance:** Update when credentials change location
