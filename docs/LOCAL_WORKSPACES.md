# LOCAL_WORKSPACES.md – Local AI-OS and Make-Ops Workspace Inventory

**Created:** 2025-11-24  
**Created by:** Claude Desktop  
**Purpose:** Map all local ai-os and make-ops workspaces on Or's machine to address the "multiple sources of truth" choke point

---

## Overview

This document provides a complete inventory of all local folders that appear to be clones or workspaces of:
- `ai-os` — the current AI-OS system repo
- `make-ops-clean` — the legacy/historical system repo

**Why this matters:**
- Multiple clones of the same repo create confusion about which is "real"
- Agents (Claude, future GPT) might accidentally work in the wrong folder
- Stale clones can lead to lost work or conflicting changes
- This inventory supports future cleanup and workspace hygiene decisions

**Scan scope:** `C:\Users\edri2` (recursive)  
**Scan date:** 2025-11-24

---

## Classification Key

| Classification | Meaning |
|----------------|---------|
| **CANONICAL** | The ONE official working directory for this repo |
| **DUPLICATE** | Another clone of the same repo (potentially stale) |
| **LEGACY** | Clone of the old `make-ops-clean` repo (historical, not active) |
| **UNKNOWN** | Needs manual review to determine purpose |

---

## Workspace Inventory

| Path | IsGitRepo | Remote | CurrentBranch | Classification | Notes |
|------|-----------|--------|---------------|----------------|-------|
| `C:\Users\edri2\Desktop\AI\ai-os` | Yes | `https://github.com/edri2or-commits/ai-os.git` | `main` | **CANONICAL** | Official ai-os working directory per project instructions |
| `C:\Users\edri2\Downloads\ai-os` | Yes | `https://github.com/edri2or-commits/ai-os.git` | `main` | DUPLICATE | Likely a temporary download; should be reviewed for deletion |
| `C:\Users\edri2\Work\AI-Projects\ai-os-workspace` | Yes | `https://github.com/edri2or-commits/ai-os` | `main` | DUPLICATE | Older workspace; URL missing `.git` suffix but same repo |
| `C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace` | Yes | `https://github.com/edri2or-commits/ai-os.git` | `main` | DUPLICATE | Named for Claude; may have been an experimental workspace |
| `C:\Users\edri2\make-ops-clean` | Yes | `https://github.com/edri2or-commits/make-ops-clean.git` | `gpt-agent-playground` | LEGACY | Root-level legacy clone; on non-main branch |
| `C:\Users\edri2\Documents\GitHub\make-ops-clean` | Yes | `https://github.com/edri2or-commits/make-ops-clean.git` | `main` | LEGACY | GitHub Desktop default location; legacy repo |
| `C:\Users\edri2\Downloads\make-ops-clean` | Yes | `https://github.com/edri2or-commits/make-ops-clean.git` | `main` | LEGACY | Likely a temporary download; legacy repo |
| `C:\Users\edri2\Work\AI-Projects\make-ops-clean` | Yes | `https://github.com/edri2or-commits/make-ops-clean.git` | `main` | LEGACY | Work folder legacy clone |
| `C:\Users\edri2\Work\AI-Projects\make-ops-clean-workspace` | Yes | `https://github.com/edri2or-commits/make-ops-clean` | `main` | LEGACY | Another legacy workspace; URL missing `.git` suffix |
| `C:\Users\edri2\Work\AI-Projects\Claude-Ops\MCP\make-ops-clean` | Yes | `https://github.com/edri2or-commits/make-ops-clean.git` | `main` | LEGACY | Deeply nested legacy clone; possibly for MCP experiments |

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total folders scanned** | 10 |
| **ai-os clones** | 4 |
| **make-ops-clean clones** | 6 |
| **CANONICAL** | 1 |
| **DUPLICATE** | 3 |
| **LEGACY** | 6 |
| **UNKNOWN** | 0 |

---

## Observations

### ai-os Clones (4 total)

1. **Canonical:** `C:\Users\edri2\Desktop\AI\ai-os`
   - This is the designated working directory
   - Currently on `main`, synced with remote

2. **Duplicates (3):**
   - `Downloads\ai-os` — likely a zip download extraction; safe to delete
   - `Work\AI-Projects\ai-os-workspace` — older workspace; likely stale
   - `Work\AI-Projects\ai-os-claude-workspace` — named for Claude; unclear if still needed

### make-ops-clean Clones (6 total)

All are classified as **LEGACY** since `make-ops-clean` is the old system repo that has been superseded by `ai-os`.

Notable:
- `C:\Users\edri2\make-ops-clean` is on branch `gpt-agent-playground` (not `main`)
- The others are all on `main`
- Multiple locations suggest historical experimentation

---

## Recommendations (For Or's Decision)

### Immediate (Low Risk)

1. **Downloads folders:** Both `Downloads\ai-os` and `Downloads\make-ops-clean` are likely temporary and can be deleted after confirming no uncommitted work.

### Short-Term (Requires Review)

2. **Consolidate ai-os duplicates:** Review `ai-os-workspace` and `ai-os-claude-workspace` for any uncommitted work, then consider deleting them.

3. **Archive or delete legacy clones:** The 6 `make-ops-clean` folders are taking up space and creating confusion. Options:
   - Delete all but one reference copy
   - Or keep one clearly labeled as "archive" if needed for historical reference

### Long-Term (Part of System Map)

4. **Establish workspace hygiene policy:** Define rules for:
   - Where new clones should live
   - How to name workspaces
   - When to clean up old workspaces

---

## Open Questions

1. Is there any uncommitted work in any of the duplicate/legacy folders that needs to be preserved?
2. Should we keep one `make-ops-clean` clone as a historical archive, or is the remote repo sufficient?
3. Should `ai-os-claude-workspace` be repurposed or deleted?

---

## Changelog

| Date | Author | Changes |
|------|--------|---------|
| 2025-11-24 | Claude Desktop | Initial inventory created |

