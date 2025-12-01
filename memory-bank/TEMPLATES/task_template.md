---
id: task-shortname
type: task
title: null  # TODO: Add task title
project: null  # proj-id if part of project
area: null  # area-id if part of area
status: inbox  # inbox | next | waiting | scheduled | completed
created: YYYY-MM-DD
do_date: null  # YYYY-MM-DD when to START this task
duration_minutes: 30
energy_profile: [admin]  # high_focus | creative | admin | low_energy
contexts: ["@laptop"]
dopamine_level: medium  # high | medium | low - how rewarding/fun this feels
is_frog: false  # Is this your hardest task today?
dependencies: []  # List of task IDs that must complete first
---

# [Task Title]

## Action
[Concrete, verb-first action - what exactly needs to be done?]

## Success Criteria
[How do you know it's complete?]

## Notes
[Any context, blockers, or dependencies]

---
**ADHD Tips:**
- Set `is_frog: true` if this is the hardest/most dreaded task today
- Use `do_date` for "when to start", not the deadline
- Match `energy_profile` to what this task requires (not what you have now)
- `dopamine_level: low` tasks pair well with rewards or "dopamine menus"
