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

See templates in `TEMPLATES/` for examples.

## Examples

- `10_Projects/example-website-redesign.md` - Example project
- `20_Areas/example-health.md` - Example area
- `00_Inbox/example-idea-task-prioritizer.md` - Example inbox item

## Integration with AI Life OS

- **Core (Truth Layer):** All PARA files are git-tracked, single source of truth
- **Ports (MCP):** Access via filesystem MCP server
- **Adapters:** Any AI model (Claude, ChatGPT, Gemini) can read/write PARA files

See `claude project/system_mapping/CANONICAL_ARCHITECTURE.md` for architectural details.

## Model-Agnostic Design

This Memory Bank works with **any AI model or interface:**
- **Claude Desktop** (current primary adapter)
- **ChatGPT** (future)
- **Gemini** (future)
- **Telegram bot** (future)
- **CLI tools** (future)

All adapters read/write the same PARA structure via filesystem access. The Memory Bank is adapter-agnostic by design.
