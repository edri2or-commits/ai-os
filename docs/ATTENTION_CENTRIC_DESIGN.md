# Attention-Centric Design Guide
## Building the Prosthetic Interface for ADHD

---

**Version:** 1.0  
**Last Updated:** 2025-12-01  
**Status:** Active Design Guide  

---

## Table of Contents

1. [Philosophy: The Interface as Exocortex](#philosophy)
2. [Core Design Patterns](#core-patterns)
3. [Visual Grammar (Cognitive Accessibility)](#visual-grammar)
4. [Implementation Checklist](#implementation-checklist)
5. [Heuristic Evaluation for ADHD-Friendly AI](#heuristic-evaluation)
6. [References & Research Grounding](#references)

---

<a name="philosophy"></a>
## 1. Philosophy: The Interface as Exocortex

### The Problem with Standard UX

Standard UX design optimizes for **engagement**:
- Variable rewards (dopamine loops)
- Infinite scrolls (prevent closure)
- Notification loops (hijack attention)

For the ADHD solopreneur, the "Engagement Economy" is **hostile**. It exploits executive dysfunction to harvest attention.

### Our Philosophy: Attention-Centric Design

**Goal:** Optimize for focus, completion, and mental quiet.

The interface is **"Calm Technology"** (Weiser & Brown):
- Moves between center and periphery of attention
- Informs without overburdening
- Amplifies the best of technology
- Respects human limits

### The Prosthetic Metaphor

The AI Life OS interface is not just a UI—it is a **prosthetic extension of the executive cortex**.

**What this means:**
- The system performs executive functions the brain struggles with
- Working memory → externalized (persistent context)
- Time perception → materialized (visual timers)
- Inhibition → scaffolded (context switch friction)
- Planning → decomposed (generative scaffolding)

**Every pixel must justify its existence** by either:
1. Clarifying intent, OR
2. Facilitating action

If it doesn't do either, it's **cognitive noise**.

---

<a name="core-patterns"></a>
## 2. Core Design Patterns

These patterns are grounded in:
- Russell Barkley's ADHD theory (performance deficit at point of performance)
- Cognitive Load Theory (Sweller)
- Humane Technology principles
- ADHD accessibility research

---

### Pattern A: The "North Star" (Persistent Context)

#### Problem: ADHD Working Memory Failure

**Symptom:** Forgetting what I was doing because of an interruption.

**Cognitive Science:**
- ADHD working memory is "leaky" (Barkley)
- Information decays within 20-30 seconds
- Context switching cost: 20+ minutes to recover focus

#### Solution: Persistent, Un-closable Context Display

**Implementation:**

```
┌─────────────────────────────────────────┐
│ 🎯 Current Focus: Draft Quarterly Report │  ← ALWAYS VISIBLE
├─────────────────────────────────────────┤
│                                         │
│   [Main Content Area]                   │
│                                         │
│   Even if user navigates to Settings,  │
│   the North Star remains visible        │
│                                         │
└─────────────────────────────────────────┘
```

**Rules:**
1. **Single Objective Only:** Never show multiple "current focuses"
2. **Global State:** Persists across all views (settings, chat, browser)
3. **User-Controlled:** User explicitly sets/updates it (not automatic)
4. **Visual Anchor:** High contrast, top of screen, emoji icon

**Why It Works:**
- Externalizes working memory (offloads biological burden)
- Reduces "what was I doing?" anxiety
- Provides instant context reinstatement after distractions

---

### Pattern B: Time Materialization

#### Problem: Time Blindness

**Symptom:** Unable to sense passage of time or estimate duration.

**Cognitive Science:**
- ADHD = impaired temporal processing (Barkley)
- Digital clocks are meaningless numbers (abstract)
- "5 minutes" feels the same as "50 minutes"

#### Solution: Visual, Analog Time Representations

**Implementation:**

**1. Visual Timers (Time Timer Style)**

```
┌───────────────┐
│   ◐◐◐◐◐◑      │  ← Red disk "vanishing"
│  ◐     ◑      │     (spatial, not numeric)
│ ◐       ◑     │
│ ◑       ◑     │     "This much time left"
│  ◑     ◐      │     (pre-attentive processing)
│   ◑◐◐◐◐       │
└───────────────┘
   12 min left
```

**NOT** digital countdown: `00:12:34` (meaningless numbers)

**2. Time Horizons (Now vs Not Now)**

```yaml
Tasks:
  NOW (Today):
    - Task A (due in 2 hours) 🔴
    - Task B (due tonight)   🟡
  
  NOT NOW (>48 hours):
    [Hidden by default]
    - Task C (due next week)
    - Task D (due next month)
```

**Why:** "Later" is not processable. Only "Now" vs "Not Now" matters.

**3. Estimated vs Actual (Time Calibration)**

Before task:
```
🤔 How long will this take?
   → User estimates: "30 minutes"
   → System starts timer
```

After task:
```
✅ Task complete!
   You estimated: 30 min
   It actually took: 75 min
   
   [Your estimates tend to be 2.5x too optimistic]
```

**Why:** Builds internal time calibration through feedback.

---

### Pattern C: The "Bouncer" (Interruption Management)

#### Problem: Poor Inhibition (Responding to Every Stimulus)

**Symptom:** Clicking every notification, switching contexts impulsively.

**Cognitive Science:**
- ADHD = weak response inhibition (Barkley)
- Immediate stimuli override long-term goals
- Each interruption costs 20+ minutes of focus recovery

#### Solution: Intelligent Friction + Batching

**Implementation:**

**1. Notification Batching (Not Real-Time)**

```
❌ BAD:
   [11:34] Email from Boss
   [11:37] Slack ping
   [11:42] Calendar reminder
   → 3 interruptions in 8 minutes

✅ GOOD:
   [12:00 PM] Notification Digest
   ──────────────────────────
   • 3 emails (1 from boss)
   • 2 Slack messages
   • 1 calendar reminder
   
   [Process batch at designated time]
```

**Batch Times:** User-configurable (e.g., 12:00 PM, 5:00 PM)

**2. Context Switch Friction Modal**

When user tries to switch from "Writing Mode" to "Browser":

```
┌─────────────────────────────────────┐
│ ⚠️  Context Switch Detected          │
│                                     │
│ You are currently in:               │
│ 📝 Writing Mode                     │
│                                     │
│ Switching to Browser will break     │
│ your flow state.                    │
│                                     │
│ [ No, Stay Focused ]  [ Yes, Switch ]│
└─────────────────────────────────────┘
```

**Why:** Introduces 3-second pause (allows executive function to engage)

**3. The "Notification Inbox" (Passive Queue)**

```
Critical decisions (HITL):
  → Route to passive "Inbox"
  → User processes during "Admin" time
  → NOT real-time interruptions

Examples:
  • Agent needs approval for change
  • System wants to run expensive task
  • Drift detected, propose fix
```

**Why:** Respects burst cognition (process in batch, not constant ping-pong)

---

### Pattern D: Conversational Scaffolding

#### Problem: Analysis Paralysis / Task Initiation Failure

**Symptom:** Staring at blank screen, unable to start.

**Cognitive Science:**
- ADHD = impaired task decomposition (can't break big into small)
- "Wall of Awful" (overwhelming complexity perception)
- Open-ended interfaces trigger freeze response

#### Solution: Progressive Disclosure + Next Action Suggestions

**Implementation:**

**1. Progressive Disclosure (Not All at Once)**

```
❌ BAD:
   [500-word wall of text]
   → Overwhelming, skip

✅ GOOD:
   Summary: The report shows...
   
   [📖 Read More] [⏭️ Next Action]
```

**Rule:** Default to TL;DR. Expand only on request.

**2. Chunky Mode (Bite-Sized Blocks)**

```
AI Output:

Block 1:
  Here's the first point...
  [Click to Continue]

Block 2:
  Here's the second point...
  [Click to Continue]
```

**Why:** Prevents scrolling paralysis, maintains engagement.

**3. Next Action Suggestions (Bridge Thinking → Doing)**

Every AI response ends with:

```
🎯 Next Actions:
   1. [✏️ Edit this draft]
   2. [📤 Send to team]
   3. [🗑️ Discard and start over]
```

**Why:** Bridges gap between "I read it" and "I act on it"

**4. Generative Scaffolding (Task Decomposition Wizards)**

User input:
```
Goal: "Launch podcast"
```

AI immediately offers:
```
🪄 I can break this into:
   1. 🎙️ Record intro episode
   2. ✂️ Edit audio (remove ums)
   3. 📤 Upload to hosting
   4. 📱 Submit to Apple Podcasts
   
   Shall I create these as tasks?
   [Yes, Create Tasks] [No, Just Show Plan]
```

**Why:** Eliminates initiation paralysis, provides structure.

---

### Pattern E: The "Panic Button" (Reset State)

#### Problem: Overwhelm / "Tab Explosion"

**Symptom:** 47 browser tabs, 12 half-finished tasks, mental paralysis.

**Cognitive Science:**
- Visual clutter triggers sensory overload
- "Too many options" = decision paralysis
- Fear of losing open tabs prevents cleanup

#### Solution: Safe State Reset

**Implementation:**

```
┌─────────────────────────────────────┐
│ 🆘 PANIC BUTTON                     │
│                                     │
│ Feeling overwhelmed?                │
│                                     │
│ This will:                          │
│ 1. Save ALL open tabs/tasks        │
│    → "Review Later" folder          │
│ 2. Reset environment to clean slate│
│ 3. Show ONLY: North Star + 1 action│
│                                     │
│ [ Reset Now ]                       │
└─────────────────────────────────────┘
```

**Guarantees:**
- ✅ Nothing is lost (saved to Review Later)
- ✅ Can retrieve anytime
- ✅ Instant clean slate

**Why:**
- Reduces anxiety of "losing" things
- Provides escape hatch from overwhelm
- Safe to press (fully reversible)

---

<a name="visual-grammar"></a>
## 3. Visual Grammar (Cognitive Accessibility)

These rules apply to ALL interfaces in the AI Life OS.

### 3.1 Typography

**Font:**
- Sans-serif, high x-height (Verdana, OpenDyslexic)
- Avoid: Serif fonts (visual noise for dyslexia)

**Size:**
- Body text: 16px minimum
- Headers: 24px minimum
- Never below 14px (cognitive strain)

**Line Spacing:**
- 1.5x minimum (reduces crowding)
- Paragraph spacing: 2x line height

**Line Length:**
- 60-80 characters per line (optimal readability)
- Avoid: Full-width text on large screens

---

### 3.2 Color (Semantic, Not Decorative)

**Use color ONLY to convey meaning:**

| Color | Meaning | Usage |
|-------|---------|-------|
| 🔴 Red | Stop / Urgent / Error | Due now, failed task, blocked |
| 🟡 Yellow | Caution / Warning | Due soon, needs attention |
| 🟢 Green | Go / Success / Safe | Completed, approved, ready |
| 🔵 Blue | Information / Neutral | General info, links |
| ⚫ Gray | Disabled / Inactive | Archived, not applicable |

**Avoid:**
- Decorative color (adds sensory noise)
- Color as sole indicator (use icons + text too)

**High Contrast Mode:**
- Black text on white background
- Or: White text on black background
- No gradients, no subtle grays

---

### 3.3 Whitespace (Aggressive Use)

**Problem:** Visual crowding triggers overwhelm.

**Solution:** Generous whitespace separates "chunks"

```
✅ GOOD:

Section 1
  - Item A
  - Item B

[Large gap]

Section 2
  - Item C
  - Item D
```

```
❌ BAD:

Section 1
- Item A
- Item B
Section 2
- Item C
- Item D
```

**Rule:** Whitespace is NOT wasted space. It's cognitive breathing room.

---

### 3.4 Lists and Menus (Miller's Law: 7±2)

**Miller's Law:** Working memory holds ~7 items.

**Rule:** Never show more than 7 items at once without chunking.

```
✅ GOOD:

Main Actions (3)
  1. Create
  2. Review
  3. Archive

Advanced (collapsed)
  [▶ Show 5 more options]
```

```
❌ BAD:

Actions (15 items shown)
  1. Create
  2. Edit
  3. Review
  4. Archive
  5. Duplicate
  ...
  15. Export
```

---

### 3.5 Animations (Minimal or None)

**Problem:** Motion triggers hyperfocus on wrong thing.

**Rule:** Animations ONLY for:
1. Progress indicators (loading)
2. State transitions (smooth collapse/expand)

**Never:**
- Decorative animations
- Auto-playing videos
- Attention-grabbing motion

**Settings:**
- Respect `prefers-reduced-motion` (CSS/OS)
- Provide "Disable All Animations" toggle

---

<a name="implementation-checklist"></a>
## 4. Implementation Checklist

Use this when building ANY interface for the AI Life OS:

### Planning Phase

- [ ] **Identified executive function being supported?**
  - Which: Working Memory / Inhibition / Planning / Time Perception
  
- [ ] **Cognitive load assessed?**
  - Intrinsic (task difficulty): Can't reduce
  - Extraneous (UI clutter): MUST minimize
  - Germane (learning): Support with scaffolding

- [ ] **Failure mode identified?**
  - What happens if user gets distracted mid-flow?
  - How does system help recover context?

### Design Phase

- [ ] **North Star present?** (persistent context visible)
- [ ] **Time visualized?** (if task involves time)
- [ ] **Context switch friction added?** (if switching modes)
- [ ] **Next actions suggested?** (every response ends with options)
- [ ] **Panic button available?** (safe reset option)

### Visual Design Phase

- [ ] **Typography:** Sans-serif, 16px+, 1.5x line spacing
- [ ] **Color:** Semantic only (red/yellow/green/blue/gray)
- [ ] **Whitespace:** Generous, separates chunks
- [ ] **Lists:** ≤7 items visible (Miller's Law)
- [ ] **Animations:** Minimal (respects `prefers-reduced-motion`)

### Code Review Phase

- [ ] **Latency:** Sub-200ms response time (Local-First principle)
- [ ] **Offline:** Works without network (no spinners)
- [ ] **State persistence:** User's work auto-saved (never lost)
- [ ] **Undo/Redo:** Available for all destructive actions
- [ ] **Keyboard shortcuts:** All actions keyboard-accessible

---

<a name="heuristic-evaluation"></a>
## 5. Heuristic Evaluation for ADHD-Friendly AI

When evaluating tools for the AI Life OS, use this checklist:

### Nielsen's Heuristics + ADHD Layer

| Heuristic | ADHD-Specific Criterion | ✅/❌ |
|-----------|-------------------------|------|
| **Visibility of System Status** | Confirms actions instantly (Optimistic UI) to prevent "did I click it?" doubt? | |
| **Match with Real World** | Uses concrete time visualizations (visual disks) rather than abstract dates/times? | |
| **User Control & Freedom** | Can I "Undo" massive AI action? (Git Revert capability essential for impulsive mistakes) | |
| **Consistency & Standards** | Follows established patterns (North Star, Bouncer, etc.)? | |
| **Error Prevention** | Does HITL catch destructive actions (delete, publish) before execution? | |
| **Recognition Rather Than Recall** | Does system auto-suggest next logical step so I don't have to remember process? | |
| **Flexibility & Efficiency** | Supports both burst cognition (batch mode) AND immediate actions? | |
| **Aesthetic & Minimalist Design** | Is interface "Calm"? Non-essential animations disabled? Contrast managed to avoid sensory overload? | |
| **Help Users Recognize, Diagnose, and Recover from Errors** | If Agent fails, does it explain why in plain language and offer "Retry with Modification" button? | |
| **Help & Documentation** | Context-sensitive help at point of action (not buried in separate docs)? | |
| **ADHD-SPECIFIC: Burst Compatibility** | Can I dump "brain dump" of messy text and have AI structure it later, or does it force structure upfront? | |
| **ADHD-SPECIFIC: Externalizes Working Memory** | Is my current goal/context always visible (North Star pattern)? | |
| **ADHD-SPECIFIC: Time Materialization** | Can I SEE time (visual timer) vs just read numbers? | |
| **ADHD-SPECIFIC: Interruption Protection** | Are notifications batched (not real-time)? | |
| **ADHD-SPECIFIC: Safe Experimentation** | Can I try things without fear (Git undo, Panic Button)? | |

---

<a name="references"></a>
## 6. References & Research Grounding

This design guide synthesizes insights from:

### Core Research

1. **Barkley, R. A. (2015).** *Attention-Deficit Hyperactivity Disorder: A Handbook for Diagnosis and Treatment.*
   - ADHD = performance deficit at point of performance
   - Working memory deficits require external scaffolding
   - Inhibition weakness requires proactive friction

2. **Sweller, J. (1988).** *Cognitive Load Theory.*
   - Intrinsic vs Extraneous vs Germane load
   - Minimize extraneous load (UI clutter)
   - Support germane load (learning)

3. **Miller, G. A. (1956).** *"The Magical Number Seven, Plus or Minus Two."*
   - Working memory capacity: 7±2 items
   - Chunking as strategy for exceeding limits

4. **Weiser, M., & Brown, J. S. (1997).** *"The Coming Age of Calm Technology."*
   - Technology should move between center and periphery of attention
   - Inform without overburdening

### Applied Research

5. **Center for Humane Technology.** *Attention Sovereignty Principles.*
   - Persuasive technology hijacks attention
   - Design for user agency, not engagement

6. **Hallowell, E. M. & Ratey, J. J.** *ADHD-Friendly App Design.*
   - Visual cues over text
   - Minimal steps per action
   - Immediate feedback
   - Structured daily routines
   - Avoid feature bloat

7. **MDPI (2023).** *"Systematic Review: Cognitive Scaffolding for ADHD."*
   - External structure compensates for executive dysfunction
   - Task chunking ("task snacking") improves completion
   - Visual boards and timers reduce time blindness

### Design Resources

8. **Time Timer® Visual Timer Research**
   - Analog disks more effective than digital for ADHD
   - Spatial representation processed pre-attentively

9. **OpenDyslexic Font Research**
   - High x-height improves readability for neurodivergent users
   - Sans-serif reduces visual noise

10. **W3C Cognitive Accessibility Guidelines (COGA)**
    - Use clear language (avoid jargon)
    - Provide context (don't assume recall)
    - Support errors (clear feedback + recovery)

---

## Integration Points

This design guide connects to:

- **Manifesto Section III:** Executive Prosthesis (externalize, point of performance, transparent reasoning)
- **ADR Pattern:** Every UI decision should have ADR with ADHD Relevance section
- **Life Graph Entities:** UI should render ADHD-specific metadata (energy_profile, dopamine_level, is_frog)
- **Memory Bank:** All designs should support rapid context reinstatement

---

## Living Document

This guide will evolve as we:
1. Build actual interfaces (validate patterns)
2. User test with ADHD individuals (iterate based on feedback)
3. Discover new research (update based on science)

**Version History:**
- v1.0 (2025-12-01): Initial design guide based on academic research synthesis

---

**Questions? Problems? New Patterns?**

→ File an issue or propose ADR for new design decisions  
→ All patterns should be justified with cognitive science  
→ "Because it looks cool" is NOT a valid reason

**Remember:** Every pixel must earn its place by serving cognition, not decoration.
