import re

filepath = 'ai-life-os-claude-project-playbook.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match Section 5.1 (using DOTALL to match across newlines)
pattern = r'(### 5\.1 On Every New Session in This Project\s+)Claude \*\*must\*\*:.*?(Claude should \*\*not\*\* start heavy editing before these steps are done\.)'

replacement = r'''\1🔴 **CRITICAL - ALWAYS DO THIS FIRST!** 🔴

Claude **must** follow the 4-step Memory Bank onboarding BEFORE starting any work:

1. **Read START_HERE.md immediately**
   - Path: `memory-bank/START_HERE.md`
   - This is your navigation hub - it tells you what to read and in what order

2. **Follow the 4-step onboarding** (< 5 minutes total):
   - **Step 1:** `AI_LIFE_OS_STORY.md` → Read Section "📖 2 Minutes (What/Why/How)" for context
   - **Step 2:** `01-active-context.md` → **GROUND TRUTH** for current state (Phase, %, recent work, next steps)
   - **Step 3:** `TOOLS_INVENTORY.md` → Quick reference: "Can I do X?" (capability map)
   - **Step 4:** `WRITE_LOCATIONS.md` → Quick reference: "Event → Files to Update" (Protocol 1 guide)

3. **Summarize to user in Hebrew** before starting work:
   ```
   היי! קראתי את Memory Bank.

   📍 **איפה אנחנו:**
   - Phase X: [name] (~Y% complete)
   - סיימנו לאחרונה: [from 01-active-context Recent Changes]
   - הבא: [from Next Steps]

   🛠️ **כלים זמינים:**
   - [top 3-4 from TOOLS_INVENTORY]

   🎯 **אפשרויות להמשך:**
   1. [Option A from Next Steps]
   2. [Option B from Next Steps]
   3. [Option C from Next Steps]

   מה תרצה לעשות?
   ```

4. **WAIT for user to choose direction** - don't start work without approval!

**Why This Matters:**
- Prevents "artificial amnesia" - every Claude instance starts with full context
- Eliminates 90-minute onboarding confusion (now: 5 minutes)
- Provides canonical answers to "where are we?" and "what can we do?"
- Ensures continuity across sessions, days, and Claude instances

**DO NOT:**
- Skip Memory Bank and go straight to editing files
- Assume you know the state from previous conversations (you don't)
- Start with "what would you like to work on?" without context
- Read old system_state files (SYSTEM_STATE_COMPACT.json is deprecated)

\2'''

result = re.sub(pattern, replacement, content, flags=re.DOTALL)

if result != content:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)
    print('✅ Section 5.1 updated successfully')
else:
    print('❌ Pattern not found - no changes made')
