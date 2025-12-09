# Truth-First Protocol (TFP-001)
## Version 1.0 - Search Before Claim

## Purpose
**NEVER make claims without evidence. ALWAYS search first, cite sources, label clearly.**

## The Problem This Solves

### What Happened
In session 2025-12-03, Claude wrote 4 protocols claiming they were "best practices":
- MAP-001: "Always use absolute paths"
- AEP-001: "Never delegate manual work"  
- TSP-001: "API-first approach"
- SVP-001: "Validation checklists"

**Without searching for sources first.**

Result: User demanded proof. Claude had to search retroactively.

Finding: 4/5 claims were correct, but **the process was backwards**.

### Why This Is Dangerous
1. **False authority** - Presenting synthesis as established fact
2. **User trust** - User may act on unverified claims
3. **No validation** - Can't distinguish correct from incorrect without checking
4. **Undermines credibility** - Even correct claims look like "making things up"

## The Core Principle

> **SEARCH FIRST, WRITE SECOND**

If you're about to call something a "best practice," "industry standard," or "research shows" → STOP. Search first.

## The Protocol

### Rule 1: Trigger Detection
Call this protocol when writing content that includes:

**Trigger phrases:**
- "Best practice"
- "Industry standard"
- "Research shows"
- "Studies indicate"
- "It is recommended"
- "According to [vague authority]"
- "The standard approach"
- "Professional developers do X"

**If you use these phrases WITHOUT citations → VIOLATION**

### Rule 2: Search-Then-Write Workflow

```
User asks for protocol/guidance
    ↓
Do I need to make claims about standards/practices?
    ↓ YES
STOP writing
    ↓
Use web_search tool
    ↓
Find 2-3 authoritative sources
    ↓
Read sources with web_fetch if needed
    ↓
THEN write protocol WITH inline citations
    ↓
Continue
```

### Rule 3: Citation Standards

**Format:**
```markdown
According to [Source Name] ([Year]): "Quote or paraphrase" [N].

...

## Citations & References
[N] Organization (Year). "Title". URL
```

**Good citation example:**
```markdown
Stack Overflow (2024): "Normally, you should always use relative paths 
where possible. This is the best practice" [1].

[1] Stack Overflow (2024). "Relative path vs absolute paths". 
https://stackoverflow.com/questions/38476592/
```

**Bad citation example:**
```markdown
It's well known that relative paths are better. ← NO SOURCE
```

### Rule 4: Labeling Claims

**When writing protocols/guidance, ALWAYS label:**

✅ **"Best Practice (Cited)"** - Has research backing
```markdown
**Best Practice (Cited):** API-first approach
Source: Postman (2024) - 74% developer adoption
```

⚠️ **"Proposed Approach (Experimental)"** - No sources yet
```markdown
**Proposed Approach:** Use absolute paths for this specific case
Rationale: [explain reasoning]
Note: Deviates from standard practice [cite standard]
```

❓ **"Hypothesis (Unverified)"** - Needs testing
```markdown
**Hypothesis:** Protocol X will reduce errors by Y%
Status: Unverified, requires measurement
Next: Run experiment to validate
```

### Rule 5: Update Cycle

When better sources found:
1. Update protocol with new citations
2. Increment version number
3. Add "Last Updated" timestamp
4. Document what changed in git commit

## Implementation Checklist

When writing ANY protocol/technical guidance:

```markdown
□ Searched for industry sources BEFORE writing?
□ Found at least 2 authoritative sources?
□ Included inline citations in text?
□ Added References section at end?
□ Labeled claims appropriately (Best Practice vs Proposed)?
□ Noted any deviations from standard practice?
□ Provided rationale for deviations?
```

## What Counts as "Authoritative Source"?

### ✅ HIGH QUALITY
- Academic journals / research papers
- Official documentation (Microsoft, GitHub, etc.)
- Industry reports (Postman State of API, Stack Overflow Survey)
- Recognized authorities (OSHA, CHADD for ADHD)
- Technical publishers (O'Reilly, InfoQ, Martin Fowler)
- Professional organizations (ACM, IEEE)

### ⚠️ MEDIUM QUALITY
- Technical blogs from established companies
- Stack Overflow (high-vote answers)
- Medium articles by verified experts
- Conference talks (QCon, Strange Loop)

### ❌ LOW QUALITY
- Random blogs without credentials
- Unsourced claims
- "I think..." or "In my experience..."
- Marketing materials
- Your own synthesis (without sources)

## Examples: Before & After

### ❌ BEFORE (Version 1.0)
```markdown
# MAP-001
Always use absolute paths for Memory Bank.
```

### ✅ AFTER (Version 2.0)
```markdown
# MAP-001
## Research Context
Stack Overflow (2024): "Normally, you should always use relative 
paths where possible. This is the best practice" [1].

## This Protocol's Approach
**Proposed Approach (Deviates from Standard):** Use absolute paths 
for Memory Bank documentation.

**Rationale:** 
- Fixed single-machine setup (no portability needed)
- Documentation context (not application code)
- Clarity over portability for this use case

[1] Stack Overflow (2024). "Relative path vs absolute paths"...
```

## Integration with Other Protocols

**SVP-001 (Self-Validation) now includes:**
```markdown
□ TRUTH-FIRST CHECK
  - Am I making claims about "best practices"?
  - Did I search for sources BEFORE writing?
  - Are all claims cited or labeled as experimental?
```

## Success Metrics
- Protocols with citations: 100%
- Claims labeled correctly: 100%
- Retroactive searches needed: 0
- User trust incidents: 0

## Anti-Patterns

### AP-005: Synthesis Without Citations
**Problem:** Presenting understanding as fact
**Example:** "It's best practice to use X" (no source)
**Fix:** Search first, then write with citations
**Severity:** HIGH

### AP-006: Vague Authority  
**Problem:** "Research shows" without naming research
**Example:** "Studies indicate..." (which studies?)
**Fix:** Name specific source with year and link
**Severity:** HIGH

### AP-007: Retroactive Justification
**Problem:** Writing first, searching later when challenged
**Example:** This session - wrote protocols, then searched
**Fix:** Reverse the order - search first
**Severity:** CRITICAL

## Implementation Status
- [x] Protocol created (2025-12-03)
- [x] Applied to all existing protocols (2025-12-03)
- [x] Integrated with SVP-001 checklist
- [ ] Add to project instructions (USER ACTION)
- [ ] Test with next protocol creation

## The Meta-Lesson

**Even when synthesis is correct, the process matters.**

4/5 protocols were research-backed, but:
- User couldn't trust them without proof
- Had to spend time searching retroactively
- Created doubt about other claims
- Looked like "making things up"

**Professional system = verifiable claims from the start.**

## Warning to Future Claude Instances

**NEVER SKIP THIS STEP.**

If you think "I know this is right, I don't need to search":
1. You might be wrong
2. Even if right, user needs proof
3. Shortcuts destroy credibility
4. Search takes 2 minutes, losing trust takes seconds

**The user's protocol was explicit:**
> "לא להמציא, מקורות שקופים, איסורים מוחלטים על המצאת 
> עובדות/ציטוטים/מקורות מזויפים"

Honor that. Search first. Cite always.

---
**Last Updated:** 2025-12-03  
**Version:** 1.0 (Founding protocol)

## Citations & References
[1] This protocol synthesizes lessons from the 2025-12-03 incident where protocols were written without prior research, requiring retroactive verification.