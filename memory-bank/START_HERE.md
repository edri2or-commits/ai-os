# START HERE - AI Life OS Entry Point

**🔴 NEW CLAUDE INSTANCE? READ THIS FIRST! 🔴**

**If you are a new AI instance, this is your navigation hub.**

---

## 🎯 Quick Start (< 5 minutes)

Follow these 4 steps IN ORDER:

### Step 1: Get the Story (2 min)
📖 **File:** `memory-bank/AI_LIFE_OS_STORY.md`

**Read:** Section "📖 2 Minutes (What/Why/How)"

**What you'll learn:**
- What is AI Life OS? (Personal AI OS for ADHD)
- Why does it exist? (Prosthetic Executive Cortex)
- 4 Core Principles (Sovereignty, Attention, Prosthesis, Gardener)
- Current state (Phase 2, 78%)

---

### Step 2: Get Current State (2 min) ⭐ MOST IMPORTANT
📊 **File:** `memory-bank/01-active-context.md`

**What you'll learn:**
- Current Phase and % completion
- Recent changes (last 5-8 slices)
- Next steps (2-3 proposed options)
- **This is your ground truth!**

---

### Step 3: Know Your Tools (1 min)
🛠️ **File:** `memory-bank/TOOLS_INVENTORY.md`

**Read:** Quick Reference table ("Can I...?")

**What you'll learn:**
- MCP servers (Google, n8n, Desktop Commander)
- REST APIs (H1 Gmail, H2 Memory Bank, H3 Telegram)
- Docker services (n8n, Qdrant, Langfuse)
- Windows automations (Observer, Email Watcher)
- What you CAN do vs CANNOT do

---

### Step 4: Know Where to Write (< 1 min)
📝 **File:** `memory-bank/WRITE_LOCATIONS.md`

**Read:** Quick Reference table ("Event → Files to Update")

**What you'll learn:**
- After slice: Update 01-active-context + 02-progress (ALWAYS)
- After tool deployed: Update TOOLS_INVENTORY
- After pattern: Create AP-XXX or BP-XXX
- Git commit rules

---

## ✅ After Reading - Summarize to User (Hebrew)

Before doing ANY work, tell the user in Hebrew:

```
היי! קראתי את Memory Bank.

📍 **איפה אנחנו:**
- Phase X: [name] (~Y% complete)
- סיימנו לאחרונה: [from Recent Changes]
- הבא: [from Next Steps]

🛠️ **כלים זמינים:**
- [top 3-4 tools from TOOLS_INVENTORY]

🎯 **אפשרויות להמשך:**
1. [Option A from 01-active-context]
2. [Option B from 01-active-context]
3. [Option C from 01-active-context]

מה תרצה לעשות?
```

**Then WAIT for user to choose direction!**

---

## 🤖 For External LLMs (GPT, Gemini, o1, etc.)

**You have 2 options:**

### Option A: Fast (30 seconds) - API
```bash
curl http://localhost:8081/api/context/current-state
```

Returns JSON with:
- Phase, progress %
- Recent work
- Next steps
- Architecture summary

### Option B: Complete (5 minutes) - File
Read: `memory-bank/AI_LIFE_OS_STORY.md`

**Sections:**
- 30 seconds: Elevator pitch
- 2 minutes: What/Why/How ⭐ START HERE
- 5 minutes: Current state + wins
- 10 minutes: Architecture + vision
- 30+ minutes: Complete deep dive

---

## 📚 Deep Dives (Optional - Read as Needed)

### If You Need Philosophy/WHY:
📖 **File:** `memory-bank/00_The_Sovereign_AI_Manifesto_v2.md`

- 4 Core Principles with ADHD justifications
- Historical context (written before ADR-001)
- Journey Map to all documentation
- ⚠️ Note: Uses deprecated terms (updated since)

### If You Need Architecture/HOW:
🏛️ **Files:** `memory-bank/docs/`

1. **ADR-001-architectural-alignment.md** - Canonical architecture decision
2. **CANONICAL_TERMINOLOGY.md** - Official terms (MANDATORY)
3. **ARCHITECTURE_REFERENCE.md** - Technical deep dive
4. **METAPHOR_GUIDE.md** - Communication guide

### If You Need Full History:
📜 **File:** `memory-bank/02-progress.md`

- Chronological log of all slices
- Detailed outcomes and lessons

### If You Need Protocols/Patterns:
📋 **Files:**
- `claude-project/ai-life-os-claude-project-playbook.md` - Phases, protocols
- `memory-bank/patterns/` - AP-XXX (anti-patterns), BP-XXX (best practices)
- `memory-bank/incidents/` - Post-mortems with 5 Whys

### If You Need Research:
🔬 **Files:** `claude-project/research_claude/`

- 18 research documents (350 pages)
- 7 families: architecture, MCP, ADHD, safety, infra, memory, meta
- 95% empirical confidence backing all decisions

---

## ⚠️ Critical Rules

### ✅ DO:
- Read these 4 files FIRST: STORY (2 min) + 01-active-context + TOOLS_INVENTORY + WRITE_LOCATIONS
- Summarize current state to user in Hebrew
- Wait for user to choose direction before starting work
- Follow Chat→Spec→Change pattern
- Auto-update Memory Bank after every slice (Protocol 1)

### ❌ DON'T:
- Start working without reading Memory Bank
- Skip the summary step
- Read all files randomly - follow the order above
- Guess current state - check 01-active-context.md
- Ask "should I update Memory Bank?" - just do it automatically (Protocol 1)
- Use deprecated terms - check CANONICAL_TERMINOLOGY.md

---

## 🔍 Self-Check Before Starting Work

**Ask yourself:**
- ✅ Did I read AI_LIFE_OS_STORY.md (2 min section)?
- ✅ Did I read 01-active-context.md completely?
- ✅ Did I check TOOLS_INVENTORY.md (what tools I have)?
- ✅ Did I check WRITE_LOCATIONS.md (where to update)?
- ✅ Did I summarize to user: Phase, %, recent work, tools, 2-3 options?
- ✅ Did I wait for user to choose direction?

**If any answer is NO → STOP and complete that step first!**

---

## 🎯 Why This Matters

**Without this context load:**
- ❌ You might redo work that's already done
- ❌ You might use wrong/missing tools (capability amnesia)
- ❌ You might update wrong files (drift)
- ❌ You might use deprecated terms (ADR violations)

**With this context load:**
- ✅ You continue smoothly from where we left off
- ✅ You know exactly what tools are available
- ✅ You update Memory Bank in the right places
- ✅ You use canonical terminology
- ✅ You work efficiently with ADHD-aware workflows

---

## 📖 File Reference Summary

| Purpose | File | Read When |
|---------|------|-----------|
| **Quick story** | AI_LIFE_OS_STORY.md (2 min) | ALWAYS FIRST |
| **Current state** | 01-active-context.md | ALWAYS |
| **Available tools** | TOOLS_INVENTORY.md | ALWAYS |
| **Where to write** | WRITE_LOCATIONS.md | ALWAYS |
| **Philosophy** | Manifesto_v2.md | If confused about WHY |
| **Architecture** | docs/ARCHITECTURE_REFERENCE.md | If technical work |
| **Terms** | docs/CANONICAL_TERMINOLOGY.md | If writing docs |
| **Full history** | 02-progress.md | If need context |
| **Protocols** | Playbook | If process question |
| **Research** | research_claude/ | If need sources |

---

**Now go read the 4 essential files (< 5 min total):** 🚀
1. AI_LIFE_OS_STORY.md (2 min section)
2. 01-active-context.md
3. TOOLS_INVENTORY.md (quick ref table)
4. WRITE_LOCATIONS.md (quick ref table)
