# Testing Infrastructure - AI Life OS

**Status:** ✅ Operational - 44/44 tests passing (VAL-1 + VAL-8 complete)  
**Framework:** pytest 8.3.3 + hypothesis 6.115.6 + syrupy 4.7.2  
**Coverage:** Observer fully validated (basic, integration, error handling, performance)  
**Runtime:** ~13s full suite | Zero warnings | Python 3.14 compliant

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_sanity.py -v

# Run with coverage report
python -m pytest --cov=tools --cov-report=term-missing
```

---

## Structure

```
tests/
├── __init__.py                        # Package marker
├── conftest.py                        # Shared fixtures (~115 lines)
├── test_sanity.py                     # Sanity checks (3 tests)
├── test_observer_basic.py             # Observer unit tests (10 tests)
├── test_observer_integration.py       # Observer integration tests (13 tests)
│   ├── TestObserverGitIntegration     # Git workflow (3 tests)
│   ├── TestObserverReportGeneration   # Report structure (2 tests)
│   ├── TestObserverEdgeCases          # Edge cases (1 test)
│   ├── TestObserverErrorHandling      # Error resilience (4 tests)
│   └── TestObserverPerformance        # Performance (3 tests)
├── test_properties.py                 # Property-based tests (13 tests)
│   ├── TestInputValidationProperties  # Input validation (7 tests)
│   ├── TestObserverProperties         # Observer properties (2 tests)
│   └── TestPropertyInvariants         # Invariants (4 tests)
└── test_snapshots.py                  # Snapshot tests (5 tests)
    ├── TestObserverSnapshots          # Observer output (3 tests)
    └── TestValidationSnapshots        # Validation matrix (2 tests)

Total: 44 tests across 6 files
```

---

## Available Fixtures (conftest.py)

### `temp_repo`
Creates temporary git repository for testing.
- Initializes git
- Sets test user (test@example.com)
- Returns: `Path` to repo root

**Usage:**
```python
def test_git_operations(temp_repo):
    # temp_repo is a Path object to initialized git repo
    (temp_repo / "test.txt").write_text("hello")
    subprocess.run(["git", "add", "."], cwd=temp_repo)
```

### `truth_layer_dir`
Creates truth-layer directory structure with all subdirectories.
- Depends on: `temp_repo`
- Creates: areas/, projects/, tasks/, contexts/, identities/, logs/
- Returns: `Path` to truth-layer directory

**Usage:**
```python
def test_truth_layer_structure(truth_layer_dir):
    # truth_layer_dir has full PARA structure
    project_file = truth_layer_dir / "projects" / "test-project.yaml"
    project_file.write_text("entity_type: project\nid: test-001")
```

### `sample_yaml_entity`
Returns sample YAML entity dict for testing.
- Type: project
- Contains: entity_type, id, title, status, timestamps

**Usage:**
```python
def test_entity_parsing(sample_yaml_entity):
    assert sample_yaml_entity["entity_type"] == "project"
    assert sample_yaml_entity["status"] == "active"
```

### `sample_cr`
Returns sample Change Request dict for testing.
- Contains: cr_id, status, drift_report, changes array

**Usage:**
```python
def test_cr_structure(sample_cr):
    assert sample_cr["status"] == "pending"
    assert len(sample_cr["changes"]) == 1
```

---

## Testing Strategies

### 1. Unit Tests (Standard)
Test individual functions in isolation.

```python
def test_validate_cr_id():
    from input_validation import validate_cr_id
    
    assert validate_cr_id("CR-20251202-120000-abcd") == True
    assert validate_cr_id("INVALID") == False
```

### 2. Property-Based Tests (Hypothesis)
Generate random inputs to find edge cases.

```python
from hypothesis import given, strategies as st

@given(st.text())
def test_function_never_crashes(input_text):
    result = my_function(input_text)
    # Just verify it doesn't crash
    assert result is not None or result is None
```

### 3. Snapshot Tests (Syrupy)
Compare output against saved snapshots.

```python
def test_output_matches_snapshot(snapshot):
    result = generate_report()
    assert result == snapshot
```

### 4. Integration Tests
Test multiple components together.

```python
def test_observer_to_reconciler_flow(temp_repo, truth_layer_dir):
    # 1. Create drift
    # 2. Run observer
    # 3. Run reconciler
    # 4. Verify CR generated
```

---

## Tools Installed

### Core Testing
- **pytest 8.3.3** - Test framework
- **pytest-cov 5.0.0** - Coverage reports
- **pytest-xdist 3.6.1** - Parallel test execution

### Advanced Testing
- **hypothesis 6.115.6** - Property-based testing (find edge cases)
- **syrupy 4.7.2** - Snapshot testing (regression tests)

### Utilities
- **pytest-mock 3.14.0** - Better mocking
- **freezegun 1.5.1** - Time travel for tests

### Code Quality
- **ruff 0.7.4** - Fast linter (replaces flake8, black, isort)
- **mypy 1.13.0** - Type checking

---

## Current Test Status

### ✅ All Passing (44/44)

**Sanity (3 tests)**
- Basic pytest functionality
- Arithmetic and string operations

**Observer Basic (10 tests)**
- Initialization and configuration
- YAML file detection
- Basic drift detection

**Observer Integration (13 tests)**
- Full Git workflow (commit → modify → detect → report)
- Schema validation integration
- Multi-file drift detection
- Report generation and structure
- Empty truth-layer handling
- **Error Handling (4 tests):** corrupt YAML, missing directories, non-git repos, mixed files
- **Performance (3 tests):** 100 files (<5s), large diffs (500+ lines), realistic benchmarks

**Property-Based (13 tests)**
- Input validation (~1,500 auto-generated test cases)
- Observer properties (unicode, paths, messages)
- Invariants (determinism, safety)

**Snapshot (5 tests)**
- Drift report structure (regression detection)
- Validation matrices

**Test Runtime:** ~13 seconds (full suite)  
**Warnings:** Zero (Python 3.14 compliant)  
**Coverage:** Observer fully validated end-to-end

---

## Why This Matters (ADHD Context)

**Without tests:**
- ❌ Manual verification every time (high friction)
- ❌ Fear of breaking things (paralysis)
- ❌ Unclear if changes work (anxiety)

**With tests:**
- ✅ One command to verify everything (`pytest`)
- ✅ Confidence to refactor (safety net)
- ✅ Clear pass/fail (reduces cognitive load)

Tests are the "undo button" for code changes - they tell you immediately if you broke something.

---

## Next Steps

**✅ VAL-1 COMPLETE:** pytest foundation + property-based + snapshots + CI  
**✅ VAL-8 COMPLETE:** Observer validation (basic + integration + error + performance)

**Remaining:**
- **VAL-9:** Reconciler integration tests (CR lifecycle, apply logic)
- **VAL-2:** MCP-specific validation tools
- **VAL-3:** Chaos engineering approaches

---

**Last Updated:** 2025-12-02 (post VAL-8 Slice 2)  
**Part of:** Validation Sprint (Phase 2: Core Infrastructure)  
**Dependencies:** Python 3.14, requirements-dev.txt
