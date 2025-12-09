# BP-007: Reference Implementation Over DIY

**Status:** Validated  
**Confidence:** High  
**Category:** Problem-Solving Best Practice  
**Date Identified:** 2025-12-05  
**Context:** Langfuse V3 Setup (Slice 2.5.4)

---

## Description

**What:** Always check for official or well-maintained reference implementations (docker-compose.yml, terraform modules, helm charts) before creating your own configuration from scratch.

**Why It Works:**
- **Time Savings:** 50-70% faster (20 min vs 40+ min)
- **Completeness:** All required services included (6/6 vs 3/6)
- **Best Practices:** Security, performance, networking already optimized
- **Maintenance:** Easier to update (pull new version vs manual sync)

---

## The Pattern

### Step 1: Search Strategy

**Primary Sources (in order):**
1. **Official GitHub:** `{project}/docker-compose.yml` or `/deploy/` folder
2. **Official Docs:** "Docker Deployment" or "Self-Hosting" sections
3. **Awesome Lists:** `awesome-{topic}` repos (curated references)
4. **Community:** Stack Overflow, Reddit (validated by upvotes/acceptance)

**Search Queries:**
```
"{project} docker-compose github official"
"{project} official deployment docker"
"{project} production docker setup"
```

### Step 2: Validation Checklist

Before using a reference implementation:
```bash
☐ Source is official org or well-known maintainer (1K+ stars)
☐ Recent activity (last commit < 6 months)
☐ Complete documentation (README with setup steps)
☐ Includes all services (not minimal example)
☐ Has .env.example or clear environment variables
☐ Uses production-grade settings (restart policies, health checks)
```

### Step 3: Minimal Customization

**DO customize:**
- Secrets (passwords, API keys, encryption keys)
- Ports (if conflicts with existing services)
- Volumes (paths to local storage)
- Environment (timezone, language, feature flags)

**DON'T customize (initially):**
- Service topology (which containers, how many)
- Networking (unless required for your infra)
- Resource limits (start with defaults, tune later)
- Image versions (use what's specified, update later)

### Step 4: Test → Customize → Document

1. **Test as-is:** Verify reference works (5-10 min)
2. **Customize minimally:** Change only what's needed (5 min)
3. **Document changes:** Comment why each change was made
4. **Test again:** Ensure customizations didn't break anything (5 min)

---

## Evidence

### Case Study: Langfuse V3 Setup

**DIY Approach (Failed):**
- Duration: 40 minutes
- Iterations: 6 configuration attempts
- Outcome: Incomplete (3/6 services running)
- Services Missing: Redis, MinIO, Worker
- Errors Fixed: 6 (ClickHouse auth, env vars, protocol, users.xml...)
- Final State: langfuse-web in restart loop

**Reference Implementation (Success):**
- Duration: 20 minutes
- Iterations: 1 (found old containers, cleaned, restarted)
- Outcome: Complete (6/6 services healthy)
- Services: PostgreSQL, ClickHouse, Redis, MinIO, Web, Worker
- Errors: 0 (all config correct from start)
- Final State: "Ready in 23.8s" ✅

**Time Saved:** 20 minutes (50% faster)  
**Quality Improvement:** Complete vs Incomplete

### Historical Success Rate

**Using Reference Implementations:**
- n8n (Slice 1.1): Official docker-compose → 30 min → ✅ Zero issues
- Qdrant (Slice 1.2): Official docker-compose → 30 min → ✅ Zero issues
- Langfuse (attempt 2): Official docker-compose → 20 min → ✅ Zero issues

**DIY Approach:**
- Langfuse (attempt 1): Custom docker-compose → 40 min → ❌ Incomplete

**Success Rate:** 100% (3/3) vs 0% (0/1)

---

## When DIY Is Acceptable

**Valid Reasons for Custom Configuration:**
1. **No official reference exists** (verified via exhaustive search)
2. **Official reference is outdated** (>1 year old, deprecated)
3. **Unique requirements** (specialized networking, air-gapped, specific compliance)
4. **Educational purpose** (learning by building, not production)

**Even Then:**
- Start from community examples (awesome-{topic})
- Document rationale for DIY approach
- Expect 2-3x longer setup time
- Plan for maintenance burden

---

## Implementation Protocol

**Before Starting Any Infrastructure Deployment:**

```markdown
# Pre-Deployment Checklist

## Reference Search (15 min max)
- [ ] Searched official GitHub: {result}
- [ ] Checked official docs: {result}
- [ ] Reviewed awesome-{topic}: {result}
- [ ] Decision: Using {official|community|DIY}

## If Using Reference:
- [ ] Downloaded: {url}
- [ ] Validated checklist (stars, activity, docs)
- [ ] Identified customizations needed: {list}

## If DIY Required:
- [ ] Documented why no reference works: {reason}
- [ ] Estimated time: {X hours} (2-3x reference)
- [ ] Risk assessment: {low|medium|high}
```

---

## ROI Analysis

**Time Investment:**
- Reference search: 5-15 minutes
- Reference validation: 5 minutes
- Reference deployment: 15-30 minutes
- **Total: 25-50 minutes**

vs

- DIY research: 30-60 minutes
- DIY implementation: 30-90 minutes
- DIY debugging: 20-60 minutes
- **Total: 80-210 minutes**

**ROI: 60-320% time savings** (2-4x faster)

**Quality Gains:**
- Completeness: 100% vs 50-70%
- Best practices: Included vs Missing
- Security: Hardened vs Basic
- Maintainability: Easy vs Hard

---

## Integration with Other Protocols

**TFP-001 (Truth-First):** SEARCH FIRST, WRITE SECOND
- Reference Implementation = already searched & validated by community
- Using reference = following TFP-001 automatically

**SVP-001 (Self-Validation):**
- Reference implementations are pre-validated
- Reduces validation burden (focus on customizations only)

**AEP-001 (ADHD-Aware):**
- Reference = lower cognitive load (no decisions needed)
- Clear starting point = easier to maintain focus
- Faster = better for attention span

---

## Exceptions & Nuance

**When Official Might Be Wrong:**
- **Minimal Examples:** Official may be "getting started" not "production"
  - Solution: Look for `/deploy/` or `/examples/production/`
- **Version Skew:** Official may target latest (you need older)
  - Solution: Git tag/branch for your version
- **Cloud-Specific:** Official may assume AWS/GCP (you're on-prem)
  - Solution: Adapt networking/storage, keep service topology

---

## Metrics

**Adoption:**
- 2025-12-05: Applied to Langfuse (success after DIY failure)
- Target: 100% adoption for future deployments

**Success Criteria:**
- Time to first working deployment: < 30 minutes
- Configuration completeness: 100% (all services)
- Post-deployment issues: Zero critical

---

## Related Patterns

- **AP-008:** Incremental Fixes (Whack-a-Mole) - what happens when you skip this
- **TFP-001:** Truth-First Protocol - search before writing
- **SVP-001:** Self-Validation Protocol - verify completeness

---

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│  BP-007: Reference Implementation First │
├─────────────────────────────────────────┤
│                                         │
│  1. Search official GitHub (5 min)     │
│  2. Validate source (5 min)            │
│  3. Download & test (10 min)           │
│  4. Customize minimally (5 min)        │
│  5. Document changes (5 min)           │
│                                         │
│  Total: ~30 min vs ~80+ min DIY        │
│                                         │
│  ✅ 100% complete                       │
│  ✅ Best practices included             │
│  ✅ Easy to maintain                    │
└─────────────────────────────────────────┘
```
