# Memory Bank Access Protocol (MAP-001)

## Purpose
Ensure Claude ALWAYS finds Memory Bank on first attempt, every session.

## The Problem
Previous instructions said "Read memory-bank/START_HERE.md" without absolute path.
Result: Claude guesses, fails, wastes time, starts blind.

## The Solution

### A. Instructions Update (IMMEDIATE)
Add to TOP of project instructions (before everything else):

```markdown
🔴 MEMORY BANK - ABSOLUTE PATH 🔴
Memory Bank location: C:\Users\edri2\Desktop\AI\ai-os\memory-bank\

FIRST ACTION in every session:
1. Read: C:\Users\edri2\Desktop\AI\ai-os\memory-bank\START_HERE.md
2. Follow the file's instructions
3. Confirm Memory Bank is accessible

IF Memory Bank not found → STOP and ask user for correct path.
DO NOT proceed without Memory Bank context.
```

### B. Validation Step (MANDATORY)
Every session starts with:

```python
# Pseudo-code for validation
try:
    read("C:\Users\edri2\Desktop\AI\ai-os\memory-bank\START_HERE.md")
    print("✅ Memory Bank accessible")
except:
    print("🔴 CRITICAL: Memory Bank not found at expected location")
    print("Path tried: C:\Users\edri2\Desktop\AI\ai-os\memory-bank\")
    print("Please provide correct path")
    STOP_SESSION()
```

### C. Fallback Mechanism
If primary path fails:
1. Search for memory-bank/ in known locations:
   - C:\Users\edri2\Desktop\AI\ai-os\memory-bank\
   - /mnt/user-data/uploads/ (if uploaded)
   - Current directory
2. Report all attempts to user
3. Request explicit path

## Implementation Status
- [ ] Update project instructions (USER ACTION REQUIRED)
- [ ] Add validation to onboarding checklist  
- [ ] Test with fresh Claude instance
- [ ] Document in Playbook

## Success Metrics
- Memory Bank found on first attempt: 100%
- Sessions starting blind: 0%
- Time to context load: < 30 seconds
