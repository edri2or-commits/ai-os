# Drift Report - Sample for Testing

**Generated:** 2025-12-01T12:00:00Z  
**Purpose:** Test data for Reconciler (Slice 2.4b)

---

## Git HEAD Drift

Observer detected mismatch between Truth Layer and actual git state.

- Last commit in SYSTEM_STATE_COMPACT.json: 29c328d
- Actual HEAD: fe2fd52
- Commits behind: 2

**Impact:** Truth Layer metadata is stale.

---

## Stale Timestamps

The following entities have timestamps older than 3 days:

- task-20251128-001: updated_at = 2025-11-28T14:00:00Z (3 days old)
- project-20251125-002: updated_at = 2025-11-25T10:30:00Z (6 days old)

**Impact:** Entity metadata doesn't reflect recent activity.

---

## Summary

- **Total Drift Findings:** 3
- **Risk Levels:**
  - LOW: 3 (git HEAD drift, stale timestamps)
  - MEDIUM: 0
  - HIGH: 0

**Recommended Action:** Generate Change Requests for all LOW risk drift items.
