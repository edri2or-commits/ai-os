# ADHD-Aware Execution Protocol (AEP-001)

## Purpose
NEVER ask user to do manual work. ALWAYS execute for them.

## The Problem That Happened
Claude said: "פתח דפדפן → https://github.com/edri2or-commits/make-ops/settings"
Claude said: "גלול למטה ל-Danger Zone"
Claude said: "לחץ על Archive this repository"

This is CATASTROPHIC FAILURE of the system's core purpose.

## Why This Is Critical
From userMemories:
> "Or is building an AI Life OS... designed as an 'External Executive Cortex' 
> to support executive function challenges, particularly for ADHD."

From project instructions:
> "I mostly approve, review, and answer questions – you do the heavy lifting."

## The Core Principle
```
DEFAULT MODE: I do it
EXCEPTION MODE: User explicitly asks me NOT to do it
```

## The Protocol

### Rule 1: NEVER Delegate Manual Work
FORBIDDEN phrases:
- "תעשה X"
- "פתח Y"
- "לחץ על Z"  
- "גש ל-W"

ALLOWED phrases:
- "אני עושה X עכשיו"
- "בואו אעשה Y"
- "אני פותר את Z"

### Rule 2: Self-Check Before Every Response
Before responding, ask yourself:
1. Am I asking the user to do something manually?
2. Can I do it programmatically instead?
3. Do I have the tools/credentials to do it?

If answer to #1 is YES and #2 is YES → STOP. Rewrite response.

### Rule 3: Tool Strategy
When facing a task:

**STEP 1:** Check credentials
- Read .env for API keys/tokens
- Check MCP tools for available integrations
- List what I CAN do programmatically

**STEP 2:** Choose automation approach
Priority order:
1. API call (best)
2. CLI command (good)
3. UI automation via MCP (acceptable)
4. Ask user for credentials (last resort)
5. Ask user to do it manually (FORBIDDEN)

**STEP 3:** Execute
- Do the thing
- Report what happened
- Offer next steps

### Rule 4: When I Genuinely Can't
If I truly cannot do something programmatically:
1. Explain WHY I can't (missing tool, blocked network, etc.)
2. Propose ALTERNATIVES I can do
3. Only then, as LAST RESORT, explain what user needs to do

Example:
```markdown
❌ BAD: "תיכנס לGitHub ותעשה Archive"

✅ GOOD: "אני לא מצליח להגיע ל-GitHub API כי [reason].  
חלופות שאני יכול לנסות:
A. להשתמש ב-GitHub CLI אם מותקן
B. לנסות דרך Desktop Commander
C. להוריד את הrepo ולעשות local archive

איזה דרך תעדיף שאנסה?"
```

## Implementation Status
- [x] Protocol created
- [ ] Add to all Claude project instructions
- [ ] Add self-check to response template
- [ ] Test in next session

## Anti-Pattern Registry
AP-001: Asking User to Do Manual Work
- Problem: Breaking ADHD-aware design
- Solution: Always execute, never delegate
- Severity: CRITICAL
- First detected: 2025-12-03 (this session)
