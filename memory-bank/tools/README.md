# Memory Bank Tools

Validation and maintenance tools for the Life Graph entities.

## Validator

### What It Does

Validates YAML frontmatter in Markdown files against JSON schemas to ensure:
- Required fields are present
- Field types are correct (string, boolean, enum, etc.)
- Values match allowed options (e.g., `status` must be one of: inbox, next, waiting, scheduled, completed)
- ID formats are correct (e.g., `task-{slug}`, `proj-{YYYY}-{slug}`)

### Why It Matters (ADHD Context)

The validator prevents:
- **Data corruption** from AI hallucinations (wrong field names, invalid values)
- **Broken queries** (if `energy_profile` has a typo, energy-matched task selection fails)
- **Cognitive load** from manually checking every field

### Quick Start

**Validate a single file:**
```bash
python memory-bank/tools/validate_entity.py memory-bank/10_Projects/proj-2025-website.md
```

**Validate multiple files:**
```bash
python memory-bank/tools/validate_entity.py memory-bank/10_Projects/*.md
```

**Validate templates (recommended after editing):**
```bash
python memory-bank/tools/validate_entity.py memory-bank/TEMPLATES/*.md
```

### Output Format

**✅ Success (clear, one-line):**
```
✅ Valid: task → task-example.md
```

**❌ Error (numbered list of issues):**
```
❌ Invalid: task → task-broken.md
   Errors found:
   1. Field 'dopamine_level': 'super-high' is not one of ['high', 'medium', 'low']
   2. Field 'energy_profile': [] is too short (minimum 1 item)
```

### Requirements

**Python 3.7+** with `jsonschema` and `pyyaml`:
```bash
pip install jsonschema pyyaml
```

### Schemas

JSON schemas are in `tools/schemas/`:
- `area.schema.json` - Life domains (Health, Career, etc.)
- `project.schema.json` - Finite goals with deadlines
- `task.schema.json` - Atomic work units
- `context.schema.json` - Constraints (where/how work can be done)
- `identity.schema.json` - Roles/modes (Writer, Developer, Parent)
- `log.schema.json` - Time-stamped notes, observations, journal entries

Each schema enforces:
- Required fields (e.g., `type`, `id`, `title`)
- Field types and formats
- Enum values (e.g., `status`, `energy_profile`)
- ID patterns (e.g., `task-[a-z0-9-]+`)

### Integration Ideas (Not Implemented Yet)

**Pre-commit Hook:**
Automatically validate changed files before git commit:
```bash
# .git/hooks/pre-commit
python memory-bank/tools/validate_entity.py $(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')
```

**n8n Workflow:**
Validate entities before writing to git in automated captures.

**CI/CD:**
Run validator on all entities in GitHub Actions on every push.

---

## Future Tools (Roadmap)

- **Migration script** - Update existing files to canonical field names
- **Template generator** - Interactive CLI for creating new entities
- **Query helpers** - Common Life Graph queries (e.g., "What can I do now?")

---

**See also:** [`docs/LIFE_GRAPH_SCHEMA.md`](../docs/LIFE_GRAPH_SCHEMA.md) for complete schema documentation.
