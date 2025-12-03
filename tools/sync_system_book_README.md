# sync_system_book.py

## Purpose
Automatically sync SYSTEM_BOOK.md from 01-active-context.md after every slice.

## How It Works

**Reads from:**
- `memory-bank/01-active-context.md` (ground truth)

**Updates in SYSTEM_BOOK.md:**
1. **Section 1: Quick Context Injection** → `Current State` (Phase + Progress)
2. **Section 6: System State (Live)** → `Phase Status` + `Recent Achievement`

## Usage

### Manual (for testing):
```bash
cd C:\Users\edri2\Desktop\AI\ai-os
python tools/sync_system_book.py
```

### Auto (via Protocol 1):
Add to end of every slice:
```bash
python tools/sync_system_book.py
git add SYSTEM_BOOK.md
git commit -m "chore(docs): Auto-sync SYSTEM_BOOK.md from 01-active-context"
```

## Research Support

**Living Documentation (Martraire 2024):**
> "It should be reliable, low effort, collaborative, and insightful"
- "Low effort" = automation

**Documentation as Code (DevOps 2024):**
> "CI/CD pipeline can automatically build and deploy the updated documentation"
- Auto-deployment standard

**Anthropic + Mintlify (2025):**
> "Platforms like Mintlify now generate both llms.txt and MCP servers automatically"
- Industry leaders use auto-generation

## Output Example

```
[INFO] Extracted from 01-active-context.md:
   Progress: 90%
   Phase: Phase 1 – Infrastructure Deployment
   Recent: SYSTEM_BOOK.md (LLM-optimized entry point...
[SUCCESS] SYSTEM_BOOK.md updated (2025-12-04 00:56)
   Phase: Phase 1 – Infrastructure Deployment (90%)
   Recent: SYSTEM_BOOK.md (LLM-optimized entry point...
```

## Files Modified

- `SYSTEM_BOOK.md` (3 sections updated)

## Error Handling

- If 01-active-context.md missing → Uses fallback values
- If regex fails → Logs error + raises exception
- Encoding: UTF-8 (handles Hebrew + emoji in files, ASCII in console)

---

**Created:** 2025-12-04  
**Research:** Living Documentation (Martraire), Docs as Code (DevOps), llms.txt (Anthropic/Mintlify)
