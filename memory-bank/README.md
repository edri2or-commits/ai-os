# Memory Bank

Personal knowledge management system using **PARA** (Projects, Areas, Resources, Archive) methodology.

## Structure

```
memory-bank/
├── 00_Inbox/          # Quick capture for unsorted notes and ideas
├── 10_Projects/       # Time-bound initiatives with clear end state
├── 20_Areas/          # Ongoing areas of responsibility (no end date)
├── 30_Resources/      # Reference material, templates, reusable knowledge
├── 99_Archive/        # Completed projects or inactive items
├── TEMPLATES/         # Templates for creating new items
├── project-brief.md   # Project overview (Vision, Constraints, TL;DR)
├── 01-active-context.md  # Current state (Focus, Recent, Next)
└── 02-progress.md     # Chronological log of completed slices
```

## Quick Start

### For New Chats (Any AI Model)

**10-second load:**
1. Read `project-brief.md` (TL;DR section)
2. Read `01-active-context.md` (Quick Status)

**20-second load:**
1. Read `project-brief.md` (full Vision + Requirements)
2. Read `01-active-context.md` (Current Focus + Recent Changes)

**5-minute deep load:**
1. Read all three: `project-brief.md`, `01-active-context.md`, `02-progress.md`
2. Scan `CANONICAL_ARCHITECTURE.md` (if making architectural decisions)

### PARA Methodology

**Projects** = Time-bound, multi-step initiatives with clear success criteria  
Examples: "Launch website redesign", "Complete Q1 tax filing"

**Areas** = Ongoing responsibilities with standards to maintain  
Examples: "Health & Wellness", "Professional Development"

**Resources** = Reference material, templates, knowledge to reuse  
Examples: "Design inspiration", "Code snippets", "Research papers"

**Archive** = Completed or inactive items (moved from Projects/Areas)

### Usage Flow

1. **Capture:** Quickly add to `00_Inbox/`
2. **Clarify:** Process inbox items into Projects/Areas/Resources (use templates)
3. **Organize:** Use YAML frontmatter for Life Graph integration (Slice 2.2)
4. **Review:** Weekly review of active Projects and Areas
5. **Archive:** Move completed/inactive items to `99_Archive/`

## YAML Frontmatter

All items use YAML frontmatter for structured metadata. This enables:
- Life Graph integration (Slice 2.2)
- Observer queries (Phase 2)
- Context-aware task suggestions (future)

**Schema Reference:** See [`docs/LIFE_GRAPH_SCHEMA.md`](docs/LIFE_GRAPH_SCHEMA.md) for the canonical definition of all entities (Area, Project, Task, Context) and ADHD-specific metadata fields.

See templates in `TEMPLATES/` for examples.

## Examples

- `10_Projects/example-website-redesign.md` - Example project
- `20_Areas/example-health.md` - Example area
- `00_Inbox/example-idea-task-prioritizer.md` - Example inbox item

## Integration with AI Life OS

- **Truth Layer:** All PARA files are git-tracked, single source of truth
- **Nerves (MCP):** Access via filesystem MCP server
- **Heads:** Any AI model (Claude, ChatGPT, Gemini) can read/write PARA files

See `docs/ARCHITECTURE_METAPHOR.md` for architectural details.

## Model-Agnostic Design

This Memory Bank works with **any AI model or interface:**
- **Claude Desktop** (current primary Head)
- **ChatGPT** (future)
- **Gemini** (future)
- **Telegram bot** (future)
- **CLI tools** (future)

All Heads read/write the same PARA structure via filesystem access. The Memory Bank is Head-agnostic by design.

## For Side Architect Assistants

If you're a side architect (chat-based thinking partner, not executor):

1. Read `docs/side-architect-research-digest.md` (~10 min) – Architecture overview and research summary
2. Read `docs/side-architect-bridge.md` (~2 min) – Current state snapshot
3. Read `01-active-context.md` (~2 min) – What's happening NOW

These 3 files replace the need to reload all research docs on every new chat. They provide a curated map to the canonical sources.

**For history / "how did we get here?" questions:**
- Ask the user for relevant entries from `02-progress.md` and/or `migration_plan.md` instead of guessing from chat
- Side architects have no persistent memory, so asking the user to provide excerpts is faster and more accurate than reconstructing from conversation

**To start a new side-architect assistant chat:**
- See `docs/side-architect-onboarding.md` for the complete onboarding flow (instruction block + opening message template + checklist)
