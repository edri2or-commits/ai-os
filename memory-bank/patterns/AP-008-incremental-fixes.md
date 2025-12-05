# AP-008: Incremental Fixes (Whack-a-Mole)

**Status:** Validated  
**Severity:** Medium-High (40+ min waste typical)  
**Category:** Problem-Solving Anti-Pattern  
**Date Identified:** 2025-12-05  
**Context:** Langfuse V3 Setup (Slice 2.5.4)

---

## Description

**What:** Attempting to fix complex system failures by addressing errors one-at-a-time without understanding the complete architecture or consulting reference implementations.

**Symptoms:**
- Multiple sequential configuration attempts (6+ iterations)
- Each fix reveals a new error (cascading failures)
- Duration grows linearly with complexity (10+ min per iteration)
- Final state remains incomplete (3/6 services vs 6/6 required)
- Frustration increases, confidence decreases

**Pattern Recognition:**
```
Error 1: ClickHouse auth → Fix → Test → FAIL
Error 2: Missing CLICKHOUSE_USER → Fix → Test → FAIL  
Error 3: Empty password → Fix → Test → FAIL
Error 4: Wrong protocol → Fix → Test → FAIL
Error 5: Missing users.xml → Fix → Test → FAIL
Error 6: Still incomplete → Research → Discover missing 3 services!
```

---

## Why It's Bad

**Time Cost:**
- Langfuse DIY: 40 minutes (6 iterations, incomplete)
- Official config: 20 minutes (complete, working)
- **Net waste: 20 minutes (100% overhead)**

**Cognitive Cost:**
- Context switching between errors (ADHD-hostile)
- Decision fatigue ("What to try next?")
- Reduced confidence in system knowledge

**Quality Cost:**
- Incomplete solutions (3/6 services vs 6/6)
- Technical debt (partial configs left behind)
- Container conflicts (cleanup required later)

---

## Root Causes

1. **Assumption of Simplicity:** "I can figure this out incrementally"
2. **Missing Big Picture:** Didn't know Langfuse V3 requires 6 services
3. **Skipping Research:** Didn't check GitHub for official docker-compose first
4. **Sunk Cost Fallacy:** "I've already spent 30 min, let me try one more fix..."

---

## Correct Alternative: BP-007

**Reference Implementation First:**
1. Check official GitHub/docs for docker-compose.yml
2. Download complete reference implementation
3. Customize minimally (only secrets/ports)
4. Test complete system
5. Iterate only if needed

**Decision Tree:**
```
Need to deploy complex system?
├─ Is there an official docker-compose? 
│  ├─ YES → Download & use (15-30 min)
│  └─ NO → Continue to next check
├─ Is there community reference (awesome-x)? 
│  ├─ YES → Start from that (30-45 min)
│  └─ NO → DIY with research (60-90 min)
```

---

## Examples

### Langfuse V3 Setup (This Case)
- **Wrong:** DIY docker-compose → 40 min whack-a-mole → incomplete
- **Right:** GitHub official → 20 min setup → complete

### Future Prevention
- n8n: Used official docker-compose ✅ (Slice 1.1, zero issues)
- Qdrant: Used official docker-compose ✅ (Slice 1.2, zero issues)
- Langfuse (attempt 1): DIY ❌ (Slice 2.5.4, 40 min waste)
- Langfuse (attempt 2): Official ✅ (Slice 2.5.4, 20 min success)

---

## Detection

**During Work:**
- 3rd sequential error = STOP
- 15+ minutes troubleshooting same component = STOP
- "Let me try one more thing..." thought = RED FLAG

**After Work (5 Whys):**
- Why failed? → Incomplete config
- Why incomplete? → Didn't know full requirements
- Why didn't know? → Didn't check official source
- Why didn't check? → Assumed DIY would be faster
- Why assumed? → **Anti-Pattern: Whack-a-Mole**

---

## Prevention Protocol

**Before Starting:**
```bash
# Checklist:
☐ Searched "{project} docker-compose github official"
☐ Found reference implementation or confirmed none exists
☐ If exists: Downloaded and reviewed
☐ If not: Documented rationale for DIY approach
```

**During Work:**
```bash
# Circuit breakers:
IF error_count > 2 THEN
    STOP
    Research official sources
    Reassess approach
END IF
```

---

## Related

- **BP-007:** Reference Implementation Over DIY
- **TFP-001:** Truth-First Protocol (SEARCH FIRST, WRITE SECOND)
- **SVP-001:** Self-Validation Protocol (verify before claiming done)

---

## Metrics

**Occurrences:**
- 2025-12-05: Langfuse V3 Setup (40 min wasted, identified & corrected)

**Future Target:**
- Zero occurrences (catch at 3rd error, before 15 min mark)
