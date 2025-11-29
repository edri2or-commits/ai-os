# SLICE_BOOTSTRAP_VALIDATOR_V1

**Date:** 2025-11-28  
**Phase:** 2.3 (INFRA_ONLY)  
**Status:** ✅ COMPLETE  
**Type:** Validation Tool (Infrastructure)

---

## 🎯 Goal

Build a validation tool that checks if a chat's first reply (bootstrap handshake) follows `CHAT_BOOTSTRAP_PROTOCOL_V1`.

**Before This Slice:**
- Manual verification of handshakes
- No automated checking
- Inconsistent feedback when protocol violated

**After This Slice:**
- Automated validation script: `validate_bootstrap_response.py`
- Clear PASS/FAIL results with specific reasons
- Optional logging to EVENT_TIMELINE

---

## 📁 Files Created/Modified

### Created (4 files)

1. **`scripts/validate_bootstrap_response.py`** (~350 lines)
   - CLI validation tool
   - Loads COMPACT/GOVERNANCE for current phase/mode
   - Runs 6 validation checks (C1-C6)
   - Outputs text or JSON format
   - Optional timeline logging

2. **`test/bootstrap_responses/`** (NEW directory)
   - Test examples directory

3. **`test/bootstrap_responses/good_handshake.txt`**
   - Example of valid handshake
   - Passes all checks

4. **`test/bootstrap_responses/bad_handshake.txt`**
   - Example of invalid handshake
   - Claims disallowed capabilities

5. **`docs/slices/SLICE_BOOTSTRAP_VALIDATOR_V1.md`** (this file)
   - Slice documentation

### Modified (0 files)

No existing files modified in V1.

---

## 🔍 What The Validator Checks

### Check C1: ACK_CONTEXT_LOADED

**Requirement:** First non-empty line must be exactly `ACK_CONTEXT_LOADED`

**Passes if:**
- ✅ First line (ignoring empty lines) is `ACK_CONTEXT_LOADED`

**Fails if:**
- ❌ Missing entirely
- ❌ Appears later in response
- ❌ Misspelled or modified

---

### Check C2: SUMMARY Section

**Requirement:** Response must have a `SUMMARY:` section

**Passes if:**
- ✅ Contains `SUMMARY:` header (case-insensitive)

**Fails if:**
- ❌ Section missing entirely

---

### Check C3: Phase/Mode Match

**Requirement:** SUMMARY must include correct Phase and Mode from COMPACT

**Passes if:**
- ✅ Contains exact phase string (e.g., "Phase 2.3 – Stabilizing the Hands (Sync & State Alignment)")
- ✅ Contains exact mode string (e.g., "INFRA_ONLY")
- ✅ Mentions role (e.g., "AI_OS_OPERATOR_ASSISTANT")

**Fails if:**
- ❌ Wrong phase
- ❌ Wrong mode
- ❌ No role specified

---

### Check C4: CAPABILITIES Valid

**Requirement:** CAPABILITIES section lists only allowed operations

**Passes if:**
- ✅ Has CAPABILITIES section
- ✅ Mentions PR_CONTRACT_V1 (the only write contract in V1)
- ✅ Does NOT claim disallowed capabilities

**Fails if:**
- ❌ Missing CAPABILITIES section
- ❌ Claims ability to "send emails" / "Gmail"
- ❌ Claims ability to "create calendar events" / "Calendar"
- ❌ Claims ability to "create tasks" / "Tasks"
- ❌ Claims "live automations" / "real-world services"

**Disallowed Keywords:**
- "send email", "gmail send", "create email"
- "create calendar", "calendar event", "google calendar"
- "create task", "google tasks"
- "live automation", "real-world service", "production service"

---

### Check C5: HARD CONSTRAINTS

**Requirement:** Must have HARD CONSTRAINTS section mentioning INFRA_ONLY and Truth Protocol

**Passes if:**
- ✅ Has "HARD CONSTRAINTS:" section
- ✅ Mentions "INFRA_ONLY" (case-insensitive)
- ✅ Mentions "Truth Protocol" OR "repo files" (file-based state)

**Fails if:**
- ❌ Missing HARD CONSTRAINTS section
- ❌ Doesn't mention INFRA_ONLY
- ❌ Doesn't mention Truth Protocol / file-based approach

---

### Check C6: READY FOR INSTRUCTIONS

**Requirement:** Last non-empty line should contain "READY FOR INSTRUCTIONS"

**Passes if:**
- ✅ Last line contains "READY FOR INSTRUCTIONS" (case-insensitive)

**Fails if:**
- ❌ Missing entirely
- ❌ Appears earlier but not at end

---

## 🧪 Usage Examples

### Basic Usage (Text Output)

```bash
# Validate a handshake response
python scripts/validate_bootstrap_response.py --response-file handshake.txt

# Expected output for VALID response:
VALIDATION RESULT: ✅ VALID

  [x] C1: ACK_CONTEXT_LOADED present as first non-empty line
  [x] C2: SUMMARY section present
  [x] C3: Phase and Mode match current state
  [x] C4: CAPABILITIES section lists only allowed operations
  [x] C5: HARD CONSTRAINTS include INFRA_ONLY and Truth Protocol
  [x] C6: Ends with READY FOR INSTRUCTIONS

Overall: VALID - all checks passed
```

### JSON Output

```bash
# Get JSON output for programmatic use
python scripts/validate_bootstrap_response.py \
  --response-file handshake.txt \
  --format json

# Expected output:
{
  "valid": true,
  "checks": [
    {"id": "C1", "passed": true, "message": "ACK_CONTEXT_LOADED found as first line"},
    {"id": "C2", "passed": true, "message": "SUMMARY section found"},
    {"id": "C3", "passed": true, "message": "Phase 'Phase 2.3 – Stabilizing the Hands (Sync & State Alignment)', Mode 'INFRA_ONLY' found"},
    {"id": "C4", "passed": true, "message": "Only allowed capabilities listed (PR_CONTRACT_V1)"},
    {"id": "C5", "passed": true, "message": "INFRA_ONLY and Truth Protocol both mentioned"},
    {"id": "C6", "passed": true, "message": "READY FOR INSTRUCTIONS found at end"}
  ],
  "phase_expected": "Phase 2.3 – Stabilizing the Hands (Sync & State Alignment)",
  "mode_expected": "INFRA_ONLY",
  "compact_version": "1.2"
}
```

### With Timeline Logging

```bash
# Validate and log result to EVENT_TIMELINE.jsonl
python scripts/validate_bootstrap_response.py \
  --response-file handshake.txt \
  --log-timeline

# Logs event like:
{
  "timestamp": "2025-11-28T02:00:00Z",
  "event_type": "CHAT_BOOTSTRAP_VALIDATION_RUN",
  "source": "bootstrap_validator_v1",
  "payload": {
    "response_file": "handshake.txt",
    "valid": true,
    "failed_checks": []
  }
}
```

---

## 📊 Example Runs

### Example 1: Valid Handshake

**Input File:** `test/bootstrap_responses/good_handshake.txt`

```
ACK_CONTEXT_LOADED

SUMMARY:
- Phase: Phase 2.3 – Stabilizing the Hands (Sync & State Alignment)
- Mode: INFRA_ONLY
- Role: AI_OS_OPERATOR_ASSISTANT
- Truth Sources Loaded: SYSTEM_STATE_COMPACT (v1.2, 2025-11-27T22:40:00Z), GOVERNANCE_LATEST (2025-11-27T20:26:48Z), EVENT_TIMELINE (last 20 events)

CAPABILITIES:
- Read: Truth Layer (COMPACT, GOVERNANCE, TIMELINE), Architecture docs, Code
- Write: PR_CONTRACT_V1 (create PR intents in PR_INTENTS.jsonl, process via pr_worker.py)
- Blocked: Direct edits to state files, Gmail/Calendar/Tasks operations, live automations

HARD CONSTRAINTS:
- INFRA_ONLY: No actions on Or's real-world services (Gmail, Calendar, Tasks, etc.)
- Truth Protocol: All state derived from repo files, not previous chat memory
- All infrastructure changes via PR (using PR_CONTRACT_V1 intent + worker pattern)

CURRENT FOCUS:
- Stabilize Phase 2.3 Control Plane (reconciler, n8n, write contracts)
- Complete Sync Write Contracts (next: Email, Calendar, Tasks)

READY FOR INSTRUCTIONS.
```

**Command:**
```bash
python scripts/validate_bootstrap_response.py --response-file test/bootstrap_responses/good_handshake.txt
```

**Output:**
```
VALIDATION RESULT: ✅ VALID

  [x] C1: ACK_CONTEXT_LOADED present as first non-empty line
  [x] C2: SUMMARY section present
  [x] C3: Phase and Mode match current state
  [x] C4: CAPABILITIES section lists only allowed operations
  [x] C5: HARD CONSTRAINTS include INFRA_ONLY and Truth Protocol
  [x] C6: Ends with READY FOR INSTRUCTIONS

Overall: VALID - all checks passed
```

**Exit Code:** 0

---

### Example 2: Invalid Handshake (Disallowed Capabilities)

**Input File:** `test/bootstrap_responses/bad_handshake.txt`

```
ACK_CONTEXT_LOADED

I'm ready to help! I can:
- Read all system files
- Send emails via Gmail
- Create calendar events
- Create Google Tasks
- Open PRs on GitHub

Current phase: Phase 2.3 (INFRA mode)
Services: 10 up, 3 partial

What should I work on?
```

**Command:**
```bash
python scripts/validate_bootstrap_response.py --response-file test/bootstrap_responses/bad_handshake.txt
```

**Output:**
```
VALIDATION RESULT: ❌ INVALID

  [x] C1: ACK_CONTEXT_LOADED present as first non-empty line
  [ ] C2: SUMMARY section present
      ⮕ SUMMARY section not found
  [x] C3: Phase and Mode match current state
  [ ] C4: CAPABILITIES section lists only allowed operations
      ⮕ Claims disallowed capabilities: send email, create calendar, create task
  [ ] C5: HARD CONSTRAINTS include INFRA_ONLY and Truth Protocol
      ⮕ HARD CONSTRAINTS section not found
  [ ] C6: Ends with READY FOR INSTRUCTIONS
      ⮕ Expected 'READY FOR INSTRUCTIONS' at end, got: 'What should I work on?'

Overall: INVALID due to failing checks: C2, C4, C5, C6
```

**Exit Code:** 1

**Why It Failed:**
- ❌ Missing SUMMARY section (not properly formatted)
- ❌ Claims ability to send emails (disallowed)
- ❌ Claims ability to create calendar events (disallowed)
- ❌ Claims ability to create tasks (disallowed)
- ❌ Missing HARD CONSTRAINTS section
- ❌ Doesn't end with READY FOR INSTRUCTIONS

---

## ⚠️ Known Limitations (V1)

### What V1 Does NOT Check:

❌ **Truth Source Timestamps**
- V1 doesn't verify timestamps are included or recent
- V2: Parse timestamps, check freshness

❌ **Semantic Validation**
- V1 uses keyword matching, not deep understanding
- Could miss paraphrased violations
- V2: LLM-based semantic validation

❌ **CURRENT FOCUS Content**
- V1 doesn't verify content makes sense
- V2: Cross-check against COMPACT's recent_work

❌ **Complete Contract List**
- V1 hardcodes PR_CONTRACT_V1
- V2: Auto-discover contracts from `docs/sync_contracts/`

❌ **Multi-Language Support**
- V1 expects English responses
- V2: Support Hebrew, multilingual

❌ **Detailed Role Validation**
- V1 just checks for "operator" or "assistant"
- V2: Validate against specific role definitions

❌ **Cross-File Consistency**
- V1 doesn't check if phase/mode in COMPACT matches GOVERNANCE
- V2: Deep consistency checks

---

## 🔮 Next Steps (V2+)

### Immediate Improvements

1. **Timestamp Validation:**
   ```python
   # Check truth source timestamps are:
   # - Present
   # - Recent (< 24h for COMPACT)
   # - Correctly formatted (ISO 8601)
   ```

2. **Semantic Validation:**
   ```python
   # Use LLM to check:
   # - Does CAPABILITIES contradict HARD CONSTRAINTS?
   # - Is CURRENT FOCUS aligned with system state?
   # - Are claims semantically valid?
   ```

3. **Auto-Discovery:**
   ```python
   # Scan docs/sync_contracts/ for available contracts
   # Validate agent only claims contracts that exist
   ```

### Future Enhancements

4. **n8n Integration:**
   - Workflow: `BOOTSTRAP_VALIDATOR_WORKFLOW_V1`
   - Trigger: Webhook or file watch
   - Auto-validate on new chat session

5. **Interactive Mode:**
   ```bash
   python scripts/validate_bootstrap_response.py --interactive
   # Paste response, get immediate feedback
   ```

6. **Batch Validation:**
   ```bash
   python scripts/validate_bootstrap_response.py --batch sessions/*.txt
   # Validate multiple sessions at once
   ```

7. **Strict Mode:**
   ```bash
   python scripts/validate_bootstrap_response.py --strict
   # Additional checks: timestamp freshness, semantic consistency
   ```

---

## 📝 Protocol Ambiguities Found & Resolutions

During implementation, I identified and resolved these ambiguities:

### 1. Case Sensitivity

**Ambiguity:** Should section headers be case-sensitive?

**Resolution:**
- Headers are case-insensitive (SUMMARY, summary, Summary all OK)
- `ACK_CONTEXT_LOADED` must be exact case (all caps)
- `READY FOR INSTRUCTIONS` is case-insensitive

**Rationale:** Headers are structural, ACK is a signal (precision matters)

---

### 2. Role Name Variations

**Ambiguity:** What role names are valid?

**Resolution:**
- Accepts: "AI_OS_OPERATOR_ASSISTANT", "OPERATOR", "ASSISTANT", "INFRA_OPERATOR"
- Rejects: No role specified, completely different roles

**Rationale:** Allow flexibility but require operator/assistant concept

---

### 3. Disallowed Capability Phrasing

**Ambiguity:** What exact phrasings count as "claiming email capability"?

**Resolution:**
- Disallowed keywords list (see C4 documentation)
- Matches case-insensitive
- Partial matches (e.g., "send email" catches "I can send emails")

**Rationale:** Conservative approach - better false positive than false negative

---

### 4. HARD CONSTRAINTS Flexibility

**Ambiguity:** Must "Truth Protocol" be mentioned verbatim?

**Resolution:**
- Accepts: "Truth Protocol" OR "repo files" OR "file-based state"
- All indicate understanding of file-based approach

**Rationale:** Concept matters more than exact phrasing

---

## 🎯 Success Criteria

✅ **Validator Script Complete**
- Runs without errors
- Validates against COMPACT/GOVERNANCE

✅ **6 Checks Implemented**
- C1: ACK_CONTEXT_LOADED
- C2: SUMMARY section
- C3: Phase/Mode match
- C4: CAPABILITIES valid
- C5: HARD CONSTRAINTS
- C6: READY FOR INSTRUCTIONS

✅ **Text and JSON Output**
- Human-readable text format
- Machine-parseable JSON format

✅ **Test Examples**
- Good handshake passes all checks
- Bad handshake fails with clear reasons

✅ **Documentation Complete**
- Usage examples
- Check descriptions
- Known limitations

---

## 🎓 Key Learnings

### What Worked Well

✅ **Keyword-Based Validation**
- Simple, fast, reliable
- Catches most violations

✅ **Structured Checks**
- Clear pass/fail per check
- Easy to debug failures

✅ **Truth Source Integration**
- Validates against actual system state
- Not hardcoded expectations

### Challenges

⚠️ **Semantic Understanding**
- Keywords can miss paraphrased violations
- "I'll help with your Gmail" vs "I can send emails"

⚠️ **False Positives**
- "We can't send emails" might trigger disallowed keyword
- Context matters

⚠️ **Maintenance**
- Disallowed keywords need updating as system evolves
- New contracts need manual addition

---

## 📚 Related Documentation

- **Protocol:** `docs/protocols/CHAT_BOOTSTRAP_PROTOCOL_V1.md`
- **Prompt Template:** `docs/protocols/CHAT_BOOTSTRAP_PROMPT_TEMPLATE_V1.md`
- **Manifest Template:** `docs/session/SESSION_MANIFEST_TEMPLATE_V1.json`
- **Truth Sources:**
  - `docs/system_state/SYSTEM_STATE_COMPACT.json`
  - `governance/snapshots/GOVERNANCE_LATEST.json`

---

**Slice Completed:** 2025-11-28  
**Next Slice:** TBD (possibly Email Contract or Session Manifest Generator)  
**Status:** ✅ COMPLETE  
**Pattern Established:** Automated validation for chat bootstrap handshakes
