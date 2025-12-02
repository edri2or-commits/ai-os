# Testing Infrastructure - AI Life OS

**Status:** Operational (VAL-1a complete - Part 1/4)  
**Framework:** pytest 8.3.3 + hypothesis + syrupy  
**Coverage:** Foundation setup complete, tests coming in VAL-1b-1d

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
├── __init__.py              # Package marker
├── conftest.py              # Shared fixtures
├── test_sanity.py           # Sanity checks (3 tests)
└── (coming in VAL-1b-1d)
    ├── test_observer.py     # Observer drift detection tests
    ├── test_reconciler.py   # Reconciler CR management tests
    └── test_validation.py   # Input validation tests
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

### ✅ Passing (3/3)
- `test_sanity()` - Basic pytest sanity
- `test_basic_arithmetic()` - Arithmetic works
- `test_string_operations()` - String ops work

### 🚧 Coming Soon (VAL-1b-1d)
- Observer drift detection tests
- Reconciler CR generation tests
- Input validation tests
- Integration tests

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

**VAL-1b (Part 2/4):** First real test - `test_observer_basic.py`  
**VAL-1c (Part 3/4):** Property-based tests with Hypothesis  
**VAL-1d (Part 4/4):** Snapshot tests with Syrupy + CI setup

---

**Created:** 2025-12-02  
**Part of:** VAL-1 (pytest foundation)  
**Dependencies:** Python 3.14, requirements-dev.txt
