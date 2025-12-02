# Input Validation

Security layer for AI Life OS tools - prevents injection attacks and format violations.

## Purpose

Protects critical tools (reconciler, observer, validator) from:
- Path traversal attacks (`../../etc/passwd`)
- Command injection (`; rm -rf /`)
- Format violations (invalid CR IDs)
- Schema violations (missing required fields)

## Functions

### `validate_cr_id(cr_id: str) -> bool`
Validates Change Request ID format.
- Format: `CR-YYYYMMDD-HHMMSS-xxxx`
- Example: `CR-20251202-123456-abcd`

### `validate_file_path(file_path: str, allowed_base: Optional[str]) -> bool`
Prevents path traversal attacks.
- Blocks `..` references
- Blocks sensitive directories (System32, /etc, /sys, etc.)
- Optional: restricts to allowed_base directory

### `validate_commit_message(message: str, max_length: int = 500) -> bool`
Prevents command injection in git commits.
- Blocks shell metacharacters: `|, &, ;, $, \`
- Blocks newlines (multi-line injection)
- Enforces length limit (default: 500 chars)

### `validate_yaml_schema(data: Dict, required_fields: list) -> bool`
Validates YAML content has required fields.

### `validate_entity_type(entity_type: str) -> bool`
Validates Life Graph entity types.
- Valid: `area, project, task, context, identity, log`

### `validate_status(status: str, entity_type: str) -> bool`
Validates status field based on entity type.
- Different valid statuses per entity type

### `validate_truth_layer_path(file_path: str) -> bool`
Convenience function - validates path is within truth-layer directory.

## Usage Example

```python
from input_validation import validate_cr_id, validate_file_path, validate_commit_message

# Validate CR ID
cr_id = "CR-20251202-123456-abcd"
if not validate_cr_id(cr_id):
    raise ValueError(f"Invalid CR ID: {cr_id}")

# Validate file path (prevent path traversal)
file_path = "truth-layer/projects/my-project.yaml"
truth_layer = "C:\\Users\\user\\ai-os\\truth-layer"
if not validate_file_path(file_path, truth_layer):
    raise ValueError(f"Invalid path: {file_path}")

# Validate commit message (prevent injection)
message = "feat: add validation"
if not validate_commit_message(message):
    raise ValueError(f"Unsafe commit message: {message}")
```

## Integration

This module should be imported and used in:
- **reconciler.py** - validate CR IDs, file paths, commit messages
- **observer.py** - validate file paths
- **validator.py** - validate entity types, statuses, YAML schemas

## Testing

Run self-tests:
```bash
python tools/input_validation.py
```

Expected output:
```
[OK] CR ID validation
[OK] File path validation
[OK] Commit message validation
[OK] Entity type validation
[OK] Status validation

[OK] All self-tests passed!
```

## Security Notes

- All validations happen BEFORE operations (fail-safe)
- Whitelist approach (explicit valid values)
- No dependencies (stdlib only)
- Cross-platform (Windows + Linux)

## Why This Matters (ADHD Safety)

Input validation protects Git Safety Rules from exploitation:
- **Rule 1:** No `git add -A` - validation ensures targeted staging
- **Rule 3:** One commit per CR - validation enforces CR ID format
- **Rule 5:** --limit flag - validation prevents batch overflow

This is the "immune system" for the Truth Layer - prevents mistakes from becoming disasters.

---

**Created:** 2025-12-02  
**Part of:** VAL-6 validation slice  
**Dependencies:** None (stdlib only)
