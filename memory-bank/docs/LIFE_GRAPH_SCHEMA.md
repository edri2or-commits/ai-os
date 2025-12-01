# Life Graph Schema v1.0

**Status:** Active (Slice 2.2a)  
**Last Updated:** 2025-11-30  
**Purpose:** Canonical schema for all entities in the Memory Bank

---

## TL;DR (Read This First)

**What is this?** The Life Graph is a structured knowledge system for managing projects, tasks, and life domains, designed specifically for ADHD solopreneurs.

**Core Philosophy:**
- **Energy Management > Time Management** – Match work to your current state, not the clock
- **Dopamine as Design Constraint** – Track subjective reward to prevent low-motivation spirals
- **Object Permanence via Links** – Explicit relationships enable associative retrieval
- **Time Blindness Mitigation** – Separate "when to start" (`do_date`) from "when to finish" (`due_date`)

**6 Core Entities:**

*Structural (define your world):*
1. **Area** – Life domains with no deadline (Health, Career, Finance)
2. **Context** – Constraints on when/where work can happen (@laptop, @low_energy, @home)
3. **Identity** – Roles/modes you operate in (Writer, Developer, Parent)

*State-based (evolve over time):*
4. **Project** – Finite goals with deadlines (Launch Website, Plan Trip)
5. **Task** – Atomic work units (5-60 minutes, completable in one session)
6. **Log** – Time-stamped observations, notes, journal entries

**Critical ADHD Fields (appear in Project + Task):**
- **`energy_profile`** – [high_focus | creative | admin | low_energy] – What state this requires
- **`dopamine_level`** – [high | medium | low] – How fun/rewarding this feels
- **`is_frog`** – boolean – Is this the hardest/most dreaded task?
- **`do_date`** vs **`due_date`** – When to START vs when to FINISH
- **`contexts`** – array – Where/how this can be done (enables "what can I do NOW?" queries)

**Storage:** Markdown files with YAML frontmatter, git-backed, human-readable

**If you only remember one thing:** This schema exists to reduce cognitive load and match work to your neurobiology, not to impose rigid productivity theater.

---

## 1. Overview

### 1.1 Purpose

This schema defines the structure for all knowledge entities in the Memory Bank. Unlike generic productivity systems, every field is designed with ADHD neurobiology in mind:

- **Working Memory Deficits** → Explicit links replace mental tracking
- **Executive Dysfunction** → Energy/dopamine metadata enables state-matched task selection
- **Time Blindness** → Visual/spatial representations via contexts + do_date/due_date split
- **Object Permanence** → Graph relationships surface "forgotten" items via associative paths

### 1.2 Relationship to PARA

The Life Graph entities live within the PARA structure:

```
memory-bank/
├── 00_Inbox/          # Unprocessed captures (temporary)
├── 10_Projects/       # Project entities (finite goals)
├── 20_Areas/          # Area entities (ongoing domains)
├── 30_Resources/      # Reference materials
├── 99_Archive/        # Completed entities
└── TEMPLATES/         # Templates for creating new entities
```

**Projects** and **Tasks** are dynamic (status changes).  
**Areas** and **Contexts** are structural (rarely change).

### 1.3 Design Principles [EXPLICIT - 12.md, 18.md]

1. **Energy Management > Time Management** – ADHD brains struggle with "when" but can assess "what state am I in?"
2. **Dopamine as First-Class Metadata** – Track subjective reward to enable "dopamine menu" patterns
3. **Explicit Relationships** – Graph edges (HAS_PARENT, BLOCKS, REQUIRES_CONTEXT) enable non-linear retrieval
4. **Low Activation Energy** – Minimal required fields, defaults provided, AI can infer missing metadata
5. **Markdown + YAML = Truth** – Human-readable, git-diffable, LLM-friendly, tool-agnostic

---

## 2. Core Entities

### 2.1 Area (Life Domain) [EXPLICIT - 12.md section 3.1.1]

**Purpose:** High-level categories representing ongoing areas of responsibility with no end date.

**ADHD Rationale:** Provides broad context for projects and tasks. Enables questions like "What's working well in my Health area?" without requiring the user to manually categorize every item.

**Location:** `memory-bank/20_Areas/area-{shortname}.md`

#### Fields

| Field | Type | Required? | Default | Description | ADHD Rationale |
|-------|------|-----------|---------|-------------|----------------|
| `type` | string | ✅ Yes | - | Always `"area"` | [EXPLICIT] Entity type identifier |
| `id` | string | ✅ Yes | - | Format: `area-{slug}` (e.g., `area-health`) | [EXPLICIT] Unique identifier for linking |
| `name` | string | ✅ Yes | - | Human-readable title | [EXPLICIT] Display name |
| `active` | boolean | ✅ Yes | `true` | Is this area currently active? | [EXPLICIT] Inactive areas hidden from default views |
| `vision` | string | ❌ No | `null` | Long-term aspiration for this area | [EXPLICIT] Provides "why" context, reduces drift |
| `contexts` | array | ❌ No | `[]` | Default contexts where this area's work happens (e.g., `["@home", "@gym"]`) | [EXPLICIT - 12.md] Enables spatial/constraint filtering |
| `review_frequency` | enum | ❌ No | `"weekly"` | How often to review (`daily`, `weekly`, `monthly`, `quarterly`) | [PROPOSAL] Prevents "out of sight, out of mind" |

#### Example YAML

```yaml
---
type: area
id: area-health
name: Health & Vitality
active: true
vision: "To maintain peak cognitive function and physical energy"
contexts: ["@home", "@gym", "@walking"]
review_frequency: weekly
---

# Health & Vitality

## Purpose
Maintain physical health, manage ADHD symptoms, optimize energy levels.

## Current Projects
- [[proj-2025-running-routine]]
- [[proj-2025-sleep-optimization]]

## Standards / Habits
- 7+ hours sleep per night
- 3x strength training per week
- Daily walk for dopamine reset

## Resources
- [Sleep hygiene guide](https://example.com)
- Workout tracker spreadsheet

## Review Notes
- 2025-11-28: Energy levels improved after fixing sleep schedule
```

#### Relationships

- **HAS_PROJECT** → Area can contain multiple Projects (one-to-many)
- **DEFINES_CONTEXT** → Area may specify default contexts for its work

---

### 2.2 Project (Finite Goal) [EXPLICIT - 12.md section 3.1.2]

**Purpose:** A collection of tasks with a defined outcome and (usually) a deadline.

**ADHD Rationale:** The `energy_profile` and `dopamine_level` fields allow the system to recommend projects only when the user is in the right state, preventing the "Wall of Awful" (emotional barrier to starting difficult work).

**Location:** `memory-bank/10_Projects/proj-{year}-{shortname}.md`

#### Fields

| Field | Type | Required? | Default | Description | ADHD Rationale |
|-------|------|-----------|---------|-------------|----------------|
| `type` | string | ✅ Yes | - | Always `"project"` | [EXPLICIT] Entity type |
| `id` | string | ✅ Yes | - | Format: `proj-{YYYY}-{slug}` (e.g., `proj-2025-website`) | [EXPLICIT] Unique ID + temporal context |
| `title` | string | ✅ Yes | - | Human-readable project name | [EXPLICIT] Display name |
| `status` | enum | ✅ Yes | `"planning"` | Current state: `planning`, `active`, `blocked`, `completed`, `archived` | [EXPLICIT] Lifecycle tracking |
| `area` | string | ❌ No | `null` | Link to parent Area ID (e.g., `area-professional`) | [EXPLICIT] Hierarchical containment |
| `created` | date | ✅ Yes | (auto) | ISO 8601 date when project was created | [PROPOSAL] Temporal context |
| **`do_date`** | date | ❌ No | `null` | When to START working on this (internal commitment) | **[EXPLICIT - 12.md]** Time blindness mitigation |
| **`due_date`** | date | ❌ No | `null` | When to FINISH (external deadline) | **[EXPLICIT - 12.md]** Distinguishes planning from deadline |
| **`energy_profile`** | array | ✅ Yes | `["high_focus"]` | What energy state(s) this requires: `high_focus`, `creative`, `admin`, `low_energy` | **[EXPLICIT - 12.md, 18.md]** Energy-matched selection |
| **`is_frog`** | boolean | ❌ No | `false` | "Eat the frog" – Is this the hardest/most important project? | **[EXPLICIT - 12.md, 18.md]** Prioritization signal |
| **`dopamine_level`** | enum | ❌ No | `"medium"` | Subjective fun/reward: `high`, `medium`, `low` | **[EXPLICIT - 12.md, 18.md]** Prevents low-dopamine spirals |
| **`contexts`** | array | ❌ No | `["@laptop"]` | Where/how this can be worked on (e.g., `["@laptop", "@home"]`) | **[EXPLICIT - 12.md]** Constraint-based filtering |
| `blockers` | array | ❌ No | `[]` | List of blocking issues or dependencies | [PROPOSAL] Makes friction explicit |
| `review_cadence` | enum | ❌ No | `"weekly"` | How often to review: `daily`, `weekly`, `monthly` | [PROPOSAL] Prevents drift |

#### Example YAML

```yaml
---
type: project
id: proj-2025-website
title: Website Redesign
status: active
area: area-professional
created: 2025-11-15
do_date: 2025-12-01
due_date: 2026-03-15
energy_profile: [high_focus, creative]
is_frog: true
dopamine_level: medium
contexts: ["@laptop", "@home", "@cafe"]
blockers: []
review_cadence: weekly
---

# Website Redesign

## Goal
Launch new personal website with portfolio, blog, and contact form by Q1 2026.

## Why Now
Current site is outdated and doesn't reflect recent work. Need online presence for networking.

## Next Actions
- [ ] Sketch wireframes for homepage
- [ ] Choose CMS platform
- [ ] Write homepage copy

## Resources
- [Design inspiration board](https://example.com)
- [[resource-web-design-principles]]

## Notes
Considering WordPress vs. static site generator (Hugo/Jekyll).

## Log
- 2025-11-15: Project created, initial research done
- 2025-11-20: Decided on Hugo + Netlify for hosting
```

#### Relationships

- **HAS_PARENT** → Project belongs to an Area (many-to-one)
- **HAS_TASKS** → Project contains multiple Tasks (one-to-many)
- **BLOCKS** → Project A may block Project B (sequential dependency)

---

### 2.3 Task (Atomic Work Unit) [EXPLICIT - 12.md section 3.1.2]

**Purpose:** The smallest unit of work, completable in 5-60 minutes in a single session.

**ADHD Rationale:** Tasks are where ADHD-specific metadata matters most. The combination of `energy_profile`, `dopamine_level`, `is_frog`, and `do_date` vs `due_date` enables sophisticated energy-matched task selection ("What can I do RIGHT NOW in my current state?").

**Location:** `memory-bank/00_Inbox/task-{shortname}.md` (temporary) → `memory-bank/10_Projects/{project-folder}/task-{shortname}.md` (after processing)

#### Fields

| Field | Type | Required? | Default | Description | ADHD Rationale |
|-------|------|-----------|---------|-------------|----------------|
| `type` | string | ✅ Yes | - | Always `"task"` | [EXPLICIT] Entity type |
| `id` | string | ✅ Yes | - | Format: `task-{slug}` (e.g., `task-homepage-copy`) | [EXPLICIT] Unique ID |
| `title` | string | ✅ Yes | - | Verb-first action (e.g., "Draft homepage copy") | [EXPLICIT] Clarity on what to do |
| `status` | enum | ✅ Yes | `"inbox"` | Lifecycle: `inbox`, `next`, `waiting`, `scheduled`, `completed` | [EXPLICIT] Workflow state |
| `project` | string | ❌ No | `null` | Parent project ID (e.g., `proj-2025-website`) | [EXPLICIT] Hierarchical link |
| `area` | string | ❌ No | `null` | Parent area ID if not part of a project | [EXPLICIT] Alternative parent |
| `created` | date | ✅ Yes | (auto) | ISO 8601 date when task was created | [PROPOSAL] Temporal tracking |
| **`scheduled`** | date | ❌ No | `null` | When to do this (same as `do_date` in Project) | **[EXPLICIT - 12.md]** "When to start" vs deadline |
| `duration_minutes` | integer | ❌ No | `30` | Estimated time to complete (5-480 minutes) | [EXPLICIT - 12.md Appendix A] Time estimation |
| **`energy_profile`** | array | ✅ Yes | `["admin"]` | Required energy: `high_focus`, `creative`, `admin`, `low_energy` | **[EXPLICIT - 12.md, 18.md]** State-matched selection |
| **`contexts`** | array | ✅ Yes | `["@laptop"]` | Where/how this can be done | **[EXPLICIT - 12.md]** "What can I do NOW?" filtering |
| **`dopamine_reward`** | enum | ❌ No | `"medium"` | Subjective fun/satisfaction: `high`, `medium`, `low` | **[EXPLICIT - 12.md, 18.md]** Dopamine menu enabler |
| **`is_frog`** | boolean | ❌ No | `false` | Is this the hardest task today? | **[EXPLICIT - 12.md, 18.md]** "Eat the frog" prioritization |
| `dependencies` | array | ❌ No | `[]` | List of task IDs that must complete first | [EXPLICIT - 12.md Table 2] Sequential dependencies |

#### Example YAML

```yaml
---
type: task
id: task-homepage-copy
title: Draft Homepage Copy
status: next
project: proj-2025-website
area: null
created: 2025-11-20
scheduled: 2025-12-01
duration_minutes: 45
energy_profile: [creative, high_focus]
contexts: ["@laptop", "@quiet"]
dopamine_reward: high
is_frog: true
dependencies: []
---

# Draft Homepage Copy

## Action
Write compelling hero section + 3 key value propositions for homepage.

## Success Criteria
- Hero headline (10 words max)
- 3 value props (2 sentences each)
- Call-to-action text
- Reviewed and edited once

## Notes
Reference competitor sites for inspiration. Keep tone professional but warm.
Aim for clarity over cleverness.
```

#### Relationships

- **HAS_PARENT** → Task belongs to a Project or Area (many-to-one)
- **BLOCKS** → Task A blocks Task B (in `dependencies` field)
- **REQUIRES_CONTEXT** → Task can only happen in certain Contexts

---

### 2.4 Context (Constraint) [EXPLICIT - 12.md section 3.1.1]

**Purpose:** Defines where or how work can be done, enabling constraint-based filtering.

**ADHD Rationale:** Contexts reduce decision fatigue by answering "What can I do RIGHT NOW with the tools/energy/location I have?" This is critical for ADHD users who struggle with working memory and executive function for on-the-fly decision-making.

**Location:** `memory-bank/30_Resources/context-{name}.md`

#### Fields

| Field | Type | Required? | Default | Description | ADHD Rationale |
|-------|------|-----------|---------|-------------|----------------|
| `type` | string | ✅ Yes | - | Always `"context"` | [EXPLICIT] Entity type |
| `context_name` | string | ✅ Yes | - | Format: `@{name}` (e.g., `@laptop`, `@low_energy`) | [EXPLICIT] Tag-style naming |
| `created` | date | ❌ No | (auto) | When this context was defined | [PROPOSAL] Historical tracking |
| `energy_fit` | enum | ❌ No | `null` | What energy level works here: `high_focus`, `creative`, `admin`, `low_energy` | [PROPOSAL] Energy-context matching |
| `tools_available` | array | ❌ No | `[]` | What tools/resources are available in this context | [PROPOSAL] Constraint clarity |

#### Example YAML

```yaml
---
type: context
context_name: "@low_energy"
created: 2025-11-01
energy_fit: low_energy
tools_available: ["@phone", "@couch", "audio_only"]
---

# @low_energy (Zombie Mode)

## When Available
Late afternoon crashes (14:00-16:00), post-lunch slumps, end of long workdays.

## Tools & Resources Available
- Phone (for light reading, audio, messages)
- Couch (comfortable, low-effort posture)
- Audio-only content (podcasts, audiobooks)

## Energy Fit
Perfect for admin tasks, passive reading, light email triage, or content consumption.
NOT suitable for creative work or high-focus tasks.

## Typical Tasks
- Sort inbox
- Listen to podcast
- Review calendar
- Light email responses
- Read saved articles
```

#### Relationships

- **ENABLES** → Context enables certain Tasks/Projects (via `contexts` field)
- **EXCLUDES** → Context may exclude tasks requiring different constraints

---

### 2.5 Identity (Role) [EXPLICIT - 12.md section 3.1.1]

**Purpose:** Represents roles or "modes" the user operates in, enabling mode-specific task filtering and reducing context-switching overhead.

**ADHD Rationale:** ADHD users struggle with mode-switching (context switching between different types of work). Explicit identities reduce cognitive load by grouping tasks/contexts/energy states by role. For example, "Writer mode" = quiet space + morning + creative work, while "Admin mode" = any time + low energy + bureaucracy.

**Location:** `memory-bank/30_Resources/role-{name}.md`

#### Fields

| Field | Type | Required? | Default | Description | ADHD Rationale |
|-------|------|-----------|---------|-------------|----------------|
| `type` | string | ✅ Yes | - | Always `"identity"` | [EXPLICIT] Entity type |
| `id` | string | ✅ Yes | - | Format: `role-{slug}` (e.g., `role-writer`) | [EXPLICIT] Unique identifier |
| `title` | string | ✅ Yes | - | Human-readable role name (e.g., "The Writer") | [EXPLICIT] Display name |
| `default_context` | string | ❌ No | `null` | Preferred context for this role (e.g., `@quiet`) | [PROPOSAL] Auto-filters tasks by role |
| `ideal_time_block` | enum | ❌ No | `null` | Best time of day: `Morning`, `Afternoon`, `Evening`, `Night` | [PROPOSAL] Circadian rhythm matching |
| `associated_areas` | array | ❌ No | `[]` | Area IDs linked to this role (e.g., `["area-professional"]`) | [PROPOSAL] Hierarchical grouping |

#### Example YAML

```yaml
---
type: identity
id: role-writer
title: The Writer
default_context: "@quiet"
ideal_time_block: Morning
associated_areas: ["area-professional", "area-creative"]
---

# The Writer

## Purpose
Deep, focused writing work – articles, essays, documentation, creative fiction.

## Typical Activities
- Draft blog posts
- Write technical documentation
- Edit manuscripts
- Research and outline

## Context & Energy
**Best conditions:**
- Early morning (6am-10am)
- Quiet space (@home office or @library)
- High-focus energy state
- Coffee + instrumental music

**Avoid:**
- Afternoons (energy crashes)
- Noisy environments
- After meetings (context-switching overhead)

## Projects & Tasks
- [[proj-2025-blog-reboot]]
- [[task-article-ai-ethics]]
- [[task-novel-chapter-3]]

## Notes
This mode requires 90+ minutes of uninterrupted time. Don't schedule back-to-back with other roles.
```

#### Relationships

- **OPERATES_IN** → Identity works best in specific Context (via `default_context`)
- **OWNS** → Identity is responsible for certain Areas (via `associated_areas`)
- **PERFORMS** → Tasks/Projects can be tagged with identity (future enhancement)

---

### 2.6 Log (Ephemeral Stream) [EXPLICIT - 12.md section 3.1.2]

**Purpose:** Time-stamped, freeform capture of thoughts, observations, meeting notes, journal entries. Acts as external memory and raw material for later processing.

**ADHD Rationale:** ADHD users experience "object impermanence" – if it's not written down, it didn't happen. Logs provide a low-friction capture mechanism (no structure required) that surfaces forgotten insights during review. The timestamp + optional tagging enable retrieval without imposing activation energy barriers.

**Location:** `memory-bank/00_Inbox/log-{timestamp}.md`

#### Fields

| Field | Type | Required? | Default | Description | ADHD Rationale |
|-------|------|-----------|---------|-------------|----------------|
| `type` | string | ✅ Yes | - | Always `"log"` | [EXPLICIT] Entity type |
| `id` | string | ✅ Yes | - | Format: `log-YYYY-MM-DD-HHMM` (e.g., `log-2025-11-30-1430`) | [EXPLICIT] Sortable timestamp ID |
| `timestamp` | datetime | ✅ Yes | (auto) | ISO 8601 timestamp when log was created | [EXPLICIT] Temporal anchor |
| `tags` | array | ❌ No | `[]` | Optional tags for filtering (e.g., `["#meeting", "#energy/low", "#idea"]`) | [PROPOSAL] Enables retrieval |
| `linked_entities` | array | ❌ No | `[]` | Optional links to related entities (e.g., `["proj-2025-website", "task-homepage"]`) | [PROPOSAL] Graph integration |
| `mood` | enum | ❌ No | `null` | Subjective mood at capture time: `high`, `neutral`, `low` | [PROPOSAL] Energy pattern tracking |

#### Example YAML

```yaml
---
type: log
id: log-2025-11-30-1430
timestamp: 2025-11-30T14:30:00
tags: ["#meeting", "#idea", "#website"]
linked_entities: ["proj-2025-website"]
mood: high
---

# Meeting Notes: Website Redesign Kickoff

## Key Decisions
- Decided on Hugo static site generator (fast, markdown-native)
- Hosting: Netlify (free tier, CI/CD built-in)
- Timeline: Launch by March 15, 2026

## Action Items
- [ ] Sketch wireframes (me, by Dec 5)
- [ ] Research Hugo themes (me, this week)
- [ ] Set up GitHub repo (me, today)

## Ideas
- Maybe add a "now" page (what I'm currently working on)
- Could integrate blog with RSS for discoverability
- Consider dark mode toggle (nice-to-have, not MVP)

## Observations
- Felt energized after this meeting (unusual for afternoon)
- Hugo's speed advantage matters for iteration velocity
- Need to timebox theme research (rabbit hole risk)

## Follow-up
Schedule design review session for Dec 10.
```

#### Relationships

- **MENTIONS** → Log can reference any entity via `linked_entities` or `[[wikilinks]]`
- **TEMPORAL_SEQUENCE** → Logs are ordered by `timestamp` (chronological stream)
- **AGGREGATES_TO** → Logs can be processed into Projects/Tasks/Areas during weekly review

---

## 3. ADHD-Specific Metadata (Deep Dive)

### 3.1 energy_profile [EXPLICIT - 12.md, 18.md section 2.1-2.2]

**Type:** Array of enum  
**Values:** `["high_focus", "creative", "admin", "low_energy"]`  
**Used in:** Project, Task

**Why This Matters:**

ADHD brains have **variable executive function** – the same person may have vastly different capabilities at 9am vs 3pm. Traditional productivity systems ask "when is this due?" but ADHD users need "what state am I in RIGHT NOW?"

**Energy Profiles:**

- **`high_focus`** – Deep work, complex problem-solving, requires sustained attention (programming, writing, analysis)
- **`creative`** – Idea generation, brainstorming, design, low structure (sketching, outlining, conceptualizing)
- **`admin`** – Low-stakes bureaucracy, requires willpower but not creativity (email, scheduling, filing, data entry)
- **`low_energy`** – Minimal executive function, passive consumption (reading, listening, light sorting)

**Usage Pattern:**

```yaml
# User reports current state: "I'm brain-fried but restless"
# System queries: energy_profile contains "low_energy" AND dopamine_reward = "high"
# Returns: Light tasks with high subjective reward (e.g., "Browse design inspiration")
```

**Research Grounding:**
- 18.md section 2.1 (Executive Dysfunction) – explains why time management fails for ADHD
- 12.md section 3.1.2 (Project schema) – `energy_profile` field prevents "Wall of Awful"

---

### 3.2 dopamine_level / dopamine_reward [EXPLICIT - 12.md, 18.md section 2.3]

**Type:** Enum  
**Values:** `high`, `medium`, `low` (optionally `negative` for actively aversive tasks)  
**Field Name:** `dopamine_level` (Project), `dopamine_reward` (Task) – **[PROPOSAL: Standardize to one name in 2.2b]**  
**Used in:** Project, Task

**Why This Matters:**

ADHD is neurochemically linked to **dopamine dysregulation**. Tasks with low subjective reward are **physiologically difficult to initiate**, not just "boring." The brain literally doesn't produce enough dopamine to sustain motivation.

**Dopamine Levels:**

- **`high`** – Fun, interesting, novel, immediately rewarding (creative work, learning new skills, favorite hobbies)
- **`medium`** – Neutral, neither exciting nor dreaded (routine work, familiar tasks)
- **`low`** – Boring, tedious, high activation barrier (taxes, admin, repetitive data entry)
- **`negative`** – Actively aversive, past failures attached (tasks with shame/anxiety)

**Usage Pattern (Dopamine Menu):**

```yaml
# User reports: "I'm bored and unmotivated"
# System queries: dopamine_reward = "high" AND energy_profile contains "low_energy"
# Returns: 3 high-dopamine, low-effort tasks to build momentum
# Example: "Sketch logo idea", "Order that book", "Reply to fun email"
```

**Research Grounding:**
- 18.md section 2.3 (Dopamine and Feedback Loops) – explains reward prediction deficits
- 12.md Playbook 2 (Dopamine Menu Activation) – clinical validation of this pattern

---

### 3.3 is_frog [EXPLICIT - 12.md, 18.md section 4.1]

**Type:** Boolean  
**Values:** `true` or `false`  
**Default:** `false`  
**Used in:** Project, Task

**Why This Matters:**

"Eat the Frog" is the practice of doing the hardest/most dreaded task first thing in the morning when willpower is highest. For ADHD users, the `is_frog` field makes this **explicit and trackable** rather than relying on working memory to identify "the hard thing."

**Usage Pattern:**

```yaml
# Morning routine query: is_frog = true AND status = "next"
# System returns: "Your frog today is: Draft homepage copy"
# Surfaces the task WITHOUT requiring user to remember or decide
```

**Research Grounding:**
- 18.md section 4.1 (Goblin Decomposer) – Task Paralysis mitigation
- 12.md section 3.1.2 (Task schema) – `is_frog` field as prioritization signal

---

### 3.4 do_date vs due_date [EXPLICIT - 12.md section 3.1.2, 18.md section 4.3]

**Fields:**
- **`do_date`** (Project) / **`scheduled`** (Task) – When to START
- **`due_date`** (Project/Task) – When to FINISH

**Why This Matters:**

ADHD users experience **time blindness** – deadlines feel abstract and distant until they're suddenly "today." The split between `do_date` and `due_date` creates an **internal commitment** (when to start) separate from the **external deadline** (when it's due).

**Example:**

```yaml
# Project: Website Redesign
do_date: 2025-12-01      # "I will start working on this December 1st"
due_date: 2026-03-15     # "Final launch deadline is March 15th"

# Benefit: Creates a planning buffer (3.5 months) instead of last-minute panic
```

**Usage Pattern:**

```yaml
# Daily planning: do_date <= today AND status != "completed"
# Returns: Tasks that were SUPPOSED to start today or earlier (accountability)
```

**Research Grounding:**
- 12.md section 3.1.2 (Task schema) – explicit do_date/due_date distinction
- 18.md section 4.3 (Visual Time Transformation) – time blindness mitigation via spatial representation

---

### 3.5 contexts [EXPLICIT - 12.md section 3.1.1, 18.md]

**Type:** Array of strings  
**Format:** `["@location", "@tool", "@energy_state"]`  
**Used in:** Area, Project, Task, Context

**Why This Matters:**

Contexts enable **constraint-based filtering** – "What can I do RIGHT NOW?" This reduces the cognitive load of manually scanning a task list and deciding feasibility.

**Context Naming Convention [PROPOSAL]:**

- **Location:** `@home`, `@office`, `@cafe`, `@car`
- **Tool:** `@laptop`, `@phone`, `@pen_paper`
- **Energy:** `@low_energy`, `@high_focus`, `@creative_mode`
- **Social:** `@alone`, `@with_people`

**Usage Pattern:**

```yaml
# User's current state: At home, laptop available, low energy
# Query: contexts contains "@home" AND contexts contains "@laptop" AND energy_profile contains "low_energy"
# Returns: Tasks that match ALL constraints (e.g., "Sort email", "Read saved articles")
```

**Research Grounding:**
- 12.md section 3.1.1 (Context entity) – constraint matching
- 18.md section 2.2 (Cognitive Load Theory) – reducing extraneous load via filtering

---

## 4. Relationships & Graph Structure [EXPLICIT - 12.md section 3.2]

### 4.1 Relationship Types

The Life Graph uses **semantic edges** to create a navigable knowledge graph. Relationships are defined either:
- **Implicitly** via YAML fields (e.g., `project: proj-2025-website` creates HAS_PARENT edge)
- **Explicitly** via Markdown links (e.g., `[[area-health]]` creates MENTIONS edge)

| Relationship | Source | Target | Meaning | Implementation |
|--------------|--------|--------|---------|----------------|
| **HAS_PARENT** | Task/Project | Area | Hierarchical containment | `area: area-health` field |
| **HAS_PROJECT** | Area | Project | Area contains projects | Reverse of HAS_PARENT |
| **HAS_TASKS** | Project | Task | Project contains tasks | `project: proj-id` field in Task |
| **BLOCKS** | Task A | Task B | Sequential dependency | `dependencies: [task-a]` in Task B |
| **REQUIRES_CONTEXT** | Task/Project | Context | Constraint matching | `contexts: ["@laptop"]` field |
| **OPERATES_IN** | Identity | Context | Role works best in specific context | `default_context: "@quiet"` in Identity |
| **OWNS** | Identity | Area | Role responsible for area | `associated_areas: ["area-X"]` in Identity |
| **PERFORMS** | Identity | Task/Project | Role performs work (future) | Tag tasks with identity |
| **TEMPORAL_SEQUENCE** | Log | Log | Chronological ordering | Sorted by `timestamp` |
| **AGGREGATES_TO** | Log | Project/Task/Area | Raw notes become structured entities | Weekly review process |
| **MENTIONS** | Any | Any | Reference (via `[[link]]`) | Markdown wikilink |

### 4.2 Graph Traversal Examples

**Example 1: Find all tasks in Health area**
```
Query: area = "area-health"
Returns: All Projects with area=area-health + all Tasks with area=area-health
```

**Example 2: Find tasks I can do NOW (at home, low energy, laptop)**
```
Query: contexts contains "@home" AND contexts contains "@laptop" AND energy_profile contains "low_energy"
Returns: Filtered task list matching constraints
```

**Example 3: Find blocking tasks (critical path)**
```
Query: dependencies is not empty AND status != "completed"
Returns: Tasks that are blocking other work
```

---

## 5. Field Naming Conventions [PROPOSAL]

**Current Issue:** Templates use inconsistent naming (e.g., `dopamine_level` vs `dopamine_reward`, `scheduled` vs `do_date`)

**Proposed Canonical Names (for 2.2b):**

| Concept | Current Names | Canonical Name | Rationale |
|---------|---------------|----------------|-----------|
| Dopamine/Reward | `dopamine_level`, `dopamine_reward` | **`dopamine_level`** | Matches 12.md Appendix A |
| Start Date | `do_date`, `scheduled` | **`do_date`** | Clearer intent (Project uses this) |
| Finish Date | `due_date`, `deadline` | **`due_date`** | Matches 12.md schema |
| Energy | `energy_profile`, `energy_fit` | **`energy_profile`** | Matches 12.md + allows arrays |

**ID Format Convention [EXPLICIT - 12.md]:**
- Area: `area-{slug}` (e.g., `area-health`)
- Project: `proj-{YYYY}-{slug}` (e.g., `proj-2025-website`)
- Task: `task-{slug}` (e.g., `task-homepage-copy`)
- Context: Use `context_name` field with `@{name}` format (e.g., `@laptop`)

**Date Format [PROPOSAL]:**
- ISO 8601: `YYYY-MM-DD` for dates (e.g., `2025-12-01`)
- ISO 8601 with time: `YYYY-MM-DDTHH:MM:SS` for timestamps (e.g., `2025-12-01T14:30:00`)

---

## 6. Usage Guide

### 6.1 Creating New Entities

**Use templates from `memory-bank/TEMPLATES/`:**
1. Copy the appropriate template file
2. Fill in required fields (marked ✅ in tables above)
3. Add optional fields as needed
4. Save to appropriate PARA folder

**Quick Reference:**
- **Area** → `20_Areas/area-{name}.md`
- **Project** → `10_Projects/proj-{year}-{name}.md`
- **Task** → `00_Inbox/task-{name}.md` (temporary) → move after processing
- **Context** → `30_Resources/context-{name}.md`
- **Identity** → `30_Resources/role-{name}.md`
- **Log** → `00_Inbox/log-{timestamp}.md`

### 6.2 Common Queries (for AI Agents)

**"What can I do NOW?"**
```yaml
Filter:
  - contexts contains current_context
  - energy_profile contains current_energy
  - status in ["inbox", "next", "scheduled"]
```

**"What's my frog today?"**
```yaml
Filter:
  - is_frog = true
  - status = "next"
  - do_date <= today
```

**"Show me high-dopamine, low-effort tasks" (Dopamine Menu)**
```yaml
Filter:
  - dopamine_level = "high"
  - energy_profile contains "low_energy"
  - duration_minutes <= 30
```

---

## 7. Migration & Validation (Coming in Slice 2.2b)

**Scope for 2.2a:**
- Schema definition ✅ (this document)
- Example entities ✅ (in templates)

**Coming in 2.2b:**
- Field name standardization (resolve `dopamine_level` vs `dopamine_reward`)
- JSON Schema validator (Appendix A pattern from 12.md)
- Template alignment (update all templates to canonical field names)
- Migration guide (old templates → new schema)

---

## 8. Research Grounding

This schema is grounded in the following research:

**Primary Sources:**
- **12.md** (The Neuro-Symbolic Life Graph) – Sections 3.1, 3.2, 3.3, Appendix A
  - Entity definitions (Area, Project, Task, Context)
  - Relationship types (HAS_PARENT, BLOCKS, REQUIRES_CONTEXT)
  - JSON Schema validation pattern
- **18.md** (Neuroadaptive Agentic Systems) – Sections 2.1-2.3, 4.1-4.4
  - ADHD cognitive profile (executive dysfunction, working memory, time blindness)
  - Energy management rationale
  - Dopamine regulation + feedback loops
  - Interaction design patterns (Goblin Decomposer, Dopamine Menu, Visual Time Transformation)

**Supporting Sources:**
- **CANONICAL_ARCHITECTURE.md** – INV-001 (Git as Core), INV-003 (model-agnostic design)
- **ai-life-os-claude-project-playbook.md** – Chat→Spec→Change workflow, ADHD-aware collaboration

**Research Families:**
- **#6: Memory / Life Graph / RAG / Truth Layer** (primary)
- **#3: ADHD / Cognitive Ergonomics / Governance** (ADHD-specific fields)
- **#1: Architecture / Kernel** (Core/Ports/Adapters alignment)

---

## 9. Version History

**v1.1 (2025-11-30) – Slice 2.2c:**
- Added 2 structural entities: Identity (Role), Log (Ephemeral Stream)
- Schema now complete: 6/6 core entities from 12.md
  - Structural: Area, Context, Identity (define your world)
  - State-based: Project, Task, Log (evolve over time)
- Updated TL;DR section (4→6 entities)
- Added Section 2.5: Identity with mode-switching ADHD rationale
- Added Section 2.6: Log with object permanence rationale
- Updated relationships table (4.1): OPERATES_IN, OWNS, PERFORMS, TEMPORAL_SEQUENCE, AGGREGATES_TO
- Updated quick reference (6.1): Added Identity, Log file locations
- Research grounding: 12.md sections 3.1.1, 3.1.2 (Identity/Log entities), 18.md (ADHD patterns)

**v1.0 (2025-11-30) – Slice 2.2a:**
- Initial schema definition
- 4 core entities: Area, Project, Task, Context
- ADHD-specific metadata documented
- [EXPLICIT]/[PROPOSAL] tagging throughout
- Foundation for validator (coming in 2.2b)

---

**Next Steps:** See Slice 2.2b for field name standardization, validator, and template alignment.
