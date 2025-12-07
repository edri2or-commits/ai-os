# ADHD Support System (NAES)
## Neuro-Adaptive Executive Scaffold - הפיגום הניוירו-אדפטיבי

**Area Type:** 20_Areas (Ongoing concern, not time-bound)  
**Created:** 2025-12-07  
**Version:** 1.0  
**Status:** Active  

---

## Purpose

This Area contains the **ADHD State Management Layer** - a system that tracks the user's executive function capacity and adapts AI behavior accordingly.

## Components

### Runtime State
- **adhd_state.json** - Current user state (energy, clarity, mode)
- **state_history.jsonl** - Historical log of state changes

### System Prompts
- **mode_prompts/** - 4 system prompts for different modes:
  - `crisis_recovery.md` - Red zone (energy ≤3)
  - `paralysis_breaker.md` - Stuck/foggy state
  - `body_double.md` - Emotional support mode
  - `flow_support.md` - Standard operation

### Automation
- **workflows/** - n8n automation workflows:
  - Morning check-in (9am)
  - Hyperfocus break enforcer (>90 min)
  - Evening wind-down (8pm)

## Core Concepts

### State Signals (6)
1. **Energy (Spoons):** 1-10 scale of executive capacity
2. **Cognitive Clarity:** Clear / Foggy / Mud
3. **Emotional Valence:** Negative / Neutral / Positive
4. **Sensory Load:** Low / Medium / High
5. **Task Urgency:** Low / Medium / High / Critical
6. **Time Since Break:** Minutes since last reset

### System Modes (4)
1. **CRISIS_RECOVERY** - Stop pushing, rest is work
2. **PARALYSIS_BREAKER** - Micro-steps only
3. **BODY_DOUBLE** - Emotional validation + presence
4. **FLOW_SUPPORT** - Standard helpful operation

## Usage

### For Claude (AI)
1. **At session start:** Read `adhd_state.json`
2. **Select mode:** Based on state signals (see protocol AEP-002)
3. **Load prompt:** Read corresponding file from `mode_prompts/`
4. **Adapt behavior:** Follow mode rules

### For User (Or)
1. **Update state:** "6 spoons, clear" → Claude updates JSON
2. **Manual override:** "Switch to crisis mode"
3. **Check state:** "What's my current state?"

## Integration

- **Observer** (every 15 min): Checks hyperfocus risk, state staleness
- **Watchdog**: Indexes state_history.jsonl → Qdrant
- **n8n**: Runs proactive check-ins and nudges
- **Protocol AEP-002**: Defines state management rules

## References

- **Research:** `/mnt/user-data/uploads/note_20251207_172948.md` (NAEP design)
- **Protocol:** `memory-bank/protocols/AEP-002_state-management.md`
- **Architecture:** `memory-bank/docs/ADHD_STATE_ARCHITECTURE.md`
- **Spec:** Slice 2025-12-07 (NAES v1)

---

**Last Updated:** 2025-12-07
