# Memory Bank Access Protocol (MAP-001)
## Version 2.0 - Updated with Research Citations

## Purpose
Ensure Claude ALWAYS finds Memory Bank on first attempt, every session.

## The Problem
Previous instructions said "Read memory-bank/START_HERE.md" without absolute path.
Result: Claude guesses, fails, wastes time, starts blind.

## Research Context: Absolute vs Relative Paths

### Industry Standards
According to Stack Overflow (2024): "Normally, you should always use relative paths where possible. This is the best practice" [1].

RedHat (2022): "Relative paths use the same principle [as absolute]. Suppose you're in /var/log/foo and you want to view a file in /var/log/bar. There's no reason to 'travel' all the way back to /var" [2].

### Why This Protocol Deviates
**Standard practice:** Relative paths for code portability  
**This protocol:** Absolute paths for documentation clarity

**Rationale:**
1. **Single-machine setup** - Memory Bank location is fixed, not portable
2. **Documentation context** - Instructions, not application code
3. **Failure cost** - Wrong path = complete session failure
4. **Clarity over portability** - For this specific use case, explicit path prevents ambiguity

PhoenixNAP (2023): "The choice between the paths depends on the specific task and the need for portability in the given situation" [3].

**This protocol explicitly chooses:** Absolute paths for stability in fixed-location documentation.

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

## Citations & References
[1] Stack Overflow (2024). "Relative path vs absolute paths". https://stackoverflow.com/questions/38476592/relative-path-vs-absolute-paths  
[2] RedHat (2022). "What are the differences between absolute and relative paths?". https://www.redhat.com/en/blog/linux-path-absolute-relative  
[3] Phoenix NAP (2023). "Absolute Path vs. Relative Path Explained". https://phoenixnap.com/kb/absolute-path-vs-relative-path

## Implementation Status
- [x] Protocol created (2025-12-03)
- [x] Citations added (2025-12-03)
- [ ] Update project instructions (USER ACTION REQUIRED)
- [ ] Test with fresh Claude instance
- [ ] Document in Playbook

## Success Metrics
- Memory Bank found on first attempt: 100% (was ~30%)
- Sessions starting blind: 0%
- Time to context load: < 30 seconds

---
**Last Updated:** 2025-12-03  
**Version:** 2.0 (Research-backed)