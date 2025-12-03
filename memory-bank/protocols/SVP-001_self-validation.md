# Self-Validation Protocol (SVP-001)

## Purpose
Claude validates its own behavior against protocols in real-time.

## The Meta-Problem
Protocols exist but aren't applied to current behavior.
Result: Same mistakes repeat because no self-checking mechanism.

## The Solution: Real-Time Self-Validation

### Validation Checklist (Run BEFORE every response)

```markdown
□ MEMORY BANK CHECK
  - Did I read Memory Bank this session?
  - Do I have current context from 01-active-context.md?
  - Am I working with latest information?

□ EXECUTION MODE CHECK  
  - Am I asking user to do something manually?
  - Can I do it programmatically instead?
  - Did I check .env for credentials?

□ TOOL STRATEGY CHECK
  - Did I try API before UI?
  - Did I read relevant documentation?
  - Am I using professional approach?

□ PROTOCOL COMPLIANCE CHECK
  - Am I following Chat→Spec→Change?
  - Am I respecting ADHD-aware design?
  - Am I minimizing cognitive load?
```

### Implementation: Thought Process Template

Every response should follow:

```markdown
<thinking>
VALIDATION:
✓ Memory Bank: Loaded, context current
✓ Execution Mode: I will do X, not ask user
✓ Tool Strategy: Checked .env, using API
✓ Protocol Compliance: Following AEP-001, TSP-001

PLAN:
1. [Action I will take]
2. [Tool I will use]
3. [Expected result]

PROCEED: Yes/No
</thinking>

<response in Hebrew>
...actual work...
</response>
```

### Trigger Points (When to Self-Validate)

**A. Session Start:**
- Validate Memory Bank access
- Load current protocols
- Confirm tool availability

**B. Before Technical Task:**
- Check credentials (.env)
- Verify API availability
- Plan tool strategy

**C. Before Asking User Anything:**
- Can I do this instead?
- Have I exhausted all options?
- Is this truly necessary?

**D. After Completing Task:**
- Did I follow protocols?
- What worked/didn't work?
- What to improve next time?

## Meta-Learning Integration

### Trigger E Detection (from Playbook)
When I notice:
- Repeated manual steps → propose automation
- Missing credentials → add to checklist
- Tool failure → document workaround

→ CREATE: AP-XXX (anti-pattern) or BP-XXX (best practice)
→ UPDATE: Relevant protocol
→ DOCUMENT: In Memory Bank

### Example Meta-Learning Flow

```
Observed: I asked user to do X manually
↓
Self-Check: Could I have done X programmatically?
↓ YES
Trigger: AEP-001 violation detected
↓
Action: 
1. Stop current approach
2. Read .env for credentials
3. Use API/automation instead
4. Document as AP-XXX if new pattern
```

## Protocol Application Matrix

| Protocol | When | How | Tool |
|----------|------|-----|------|
| MAP-001 | Session start | Read absolute path | Filesystem |
| AEP-001 | Any user request | Never delegate | Self-check |
| TSP-001 | Technical task | API-first | .env + docs |
| SVP-001 | Every response | Run checklist | This protocol |

## Success Metrics
- Protocol violations per session: 0
- Self-corrections before response: > 0 (means I'm catching issues)
- User pointing out mistakes: 0 (means I caught them first)

## Implementation Status
- [x] Protocol created
- [x] Self-activation rule applied (creating this IS validation)
- [ ] Add to response template
- [ ] Test in next session
- [ ] Measure violation rate

## The Deeper Issue: Why Protocols Weren't Applied

This session revealed:
1. Protocols existed (in project knowledge)
2. But weren't actively checked
3. No mechanism forced compliance
4. Result: Theoretical protocols, practical failures

This protocol (SVP-001) IS the fix:
- Mandatory checklist before responding
- Explicit validation steps
- Meta-learning when violations detected
- Self-correction mechanism

## Warning to Future Claude Instances

If you're reading this:
- These protocols exist for a reason (painful experience)
- Ignoring them = repeating same mistakes
- User will notice and lose trust
- System credibility depends on consistency

RUN THE CHECKLIST. EVERY TIME.
No exceptions. No shortcuts.

Professional system = disciplined execution.
