# Patterns Directory

This directory contains documented **Best Practices (BP-XXX)** and **Anti-Patterns (AP-XXX)** discovered during AI Life OS development.

---

## Purpose

**Meta-Learning:** Capture lessons learned to prevent repeated mistakes and reinforce successful approaches.

**Format:**
- **AP-XXX:** Anti-Patterns (what NOT to do) - mistakes, pitfalls, waste
- **BP-XXX:** Best Practices (what TO do) - proven solutions, time-savers, quality boosters

---

## Current Patterns

### Anti-Patterns (Avoid These)

- **[AP-008: Incremental Fixes (Whack-a-Mole)](AP-008-incremental-fixes.md)**
  - **What:** Fixing errors one-at-a-time without understanding full architecture
  - **Cost:** 40+ min wasted, incomplete results
  - **Alternative:** BP-007 (Reference Implementation First)

### Best Practices (Follow These)

- **[BP-007: Reference Implementation Over DIY](BP-007-reference-implementation.md)**
  - **What:** Always check for official docker-compose/configs before building from scratch
  - **Benefit:** 50-70% time savings (20 min vs 40+ min), 100% completeness
  - **Evidence:** Langfuse V3, n8n, Qdrant (all successful with official configs)

---

## When to Create a Pattern

**Protocol 1 Triggers (Playbook Section 9):**

**Auto-Create AP-XXX:**
- **Trigger A:** Repetition (2nd+ occurrence of same mistake)
- **Trigger B:** Workaround used (temporary fix applied)
- **Trigger C:** User surprise/frustration (unexpected behavior)

**Auto-Create BP-XXX:**
- **Validation:** Pattern successfully applied 2+ times
- **ROI:** Measurable time/quality improvement (>30% gain)
- **Repeatability:** Can be documented as checklist/protocol

**Auto-Create TD-XXX (Technical Debt):**
- **Trigger B:** Workaround created (not root cause fix)
- **Impact:** Known gap in system (documented but not fixed)

---

## Pattern Template

### Anti-Pattern (AP-XXX)

```markdown
# AP-XXX: {Pattern Name}

**Status:** Validated | Suspected  
**Severity:** Low | Medium | High | Critical  
**Category:** Problem-Solving | Process | Technical | Cognitive  
**Date Identified:** YYYY-MM-DD  
**Context:** {Where discovered}

---

## Description
What + Symptoms + Pattern Recognition

## Why It's Bad
Time Cost + Cognitive Cost + Quality Cost

## Root Causes
5 Whys analysis

## Correct Alternative
Link to BP-XXX

## Examples
Specific cases

## Detection
How to recognize during/after work

## Prevention Protocol
Checklist + circuit breakers

## Related
Other patterns

## Metrics
Occurrences + future target
```

### Best Practice (BP-XXX)

```markdown
# BP-XXX: {Pattern Name}

**Status:** Validated | Experimental  
**Confidence:** Low | Medium | High  
**Category:** Problem-Solving | Process | Technical | Cognitive  
**Date Identified:** YYYY-MM-DD  
**Context:** {Where discovered}

---

## Description
What + Why It Works

## The Pattern
Step-by-step implementation

## Evidence
Case studies + data + success rate

## When to Use
Valid scenarios + exceptions

## Implementation Protocol
Checklist + decision tree

## ROI Analysis
Time + quality gains

## Integration with Other Protocols
How it fits with existing patterns

## Quick Reference Card
One-page summary
```

---

## Maintenance

**Auto-Update:** Pattern files updated when:
- New occurrence detected (AP-XXX metrics section)
- New evidence gathered (BP-XXX success cases)
- Protocol refined (implementation improvements)

**Review Cycle:** Monthly retrospective
- Which patterns need validation?
- Which patterns need refinement?
- Which patterns can be retired?

---

## Related Documents

- **Playbook Section 9:** Meta-Learning Triggers (when to create patterns)
- **Playbook Section 15:** Post-Slice Reflection Checklist (Protocol 1)
- **Memory Bank incidents/:** Incident reports (source of AP-XXX patterns)
- **Memory Bank docs/:** Plans and specifications (source of BP-XXX patterns)

---

**Last Updated:** 2025-12-05  
**Total Patterns:** 2 (1 AP, 1 BP)
