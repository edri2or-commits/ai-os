#!/usr/bin/env python3
"""
Life Graph Entity Validator

Validates YAML frontmatter in Markdown files against JSON schemas.
Designed for ADHD-friendly output: clear success/error messages.

Usage:
    python validate_entity.py path/to/file.md
    python validate_entity.py path/to/folder/*.md
"""

import sys
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

try:
    from jsonschema import validate, ValidationError, Draft7Validator
except ImportError:
    print("❌ Error: jsonschema library not installed")
    print("   Install with: pip install jsonschema")
    sys.exit(1)


# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def extract_frontmatter(file_path: Path) -> Optional[Dict]:
    """Extract YAML frontmatter from a Markdown file."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return None
    
    # Match YAML frontmatter between --- delimiters
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None
    
    try:
        frontmatter = yaml.safe_load(match.group(1))
        return frontmatter
    except yaml.YAMLError as e:
        return None


def load_schema(entity_type: str) -> Optional[Dict]:
    """Load JSON schema for a given entity type."""
    schema_dir = Path(__file__).parent / "schemas"
    schema_file = schema_dir / f"{entity_type}.schema.json"
    
    if not schema_file.exists():
        return None
    
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def validate_entity(file_path: Path) -> Tuple[bool, str, List[str]]:
    """
    Validate a single entity file.
    
    Returns:
        (success: bool, entity_type: str, errors: List[str])
    """
    # Extract frontmatter
    frontmatter = extract_frontmatter(file_path)
    if frontmatter is None:
        return False, "unknown", ["Could not extract YAML frontmatter (check --- delimiters)"]
    
    # Get entity type
    entity_type = frontmatter.get('type', 'unknown')
    if entity_type == 'unknown':
        return False, "unknown", ["Missing 'type' field in frontmatter"]
    
    # Load schema
    schema = load_schema(entity_type)
    if schema is None:
        return False, entity_type, [f"No schema found for type '{entity_type}'"]
    
    # Validate
    validator = Draft7Validator(schema)
    errors_list = list(validator.iter_errors(frontmatter))
    
    if not errors_list:
        return True, entity_type, []
    
    # Format errors for ADHD-friendly output
    formatted_errors = []
    for error in errors_list:
        path = " → ".join(str(p) for p in error.path) if error.path else "root"
        formatted_errors.append(f"Field '{path}': {error.message}")
    
    return False, entity_type, formatted_errors


def print_validation_result(file_path: Path, success: bool, entity_type: str, errors: List[str]):
    """Print validation result with ADHD-friendly formatting."""
    file_name = file_path.name
    
    if success:
        # ✅ Clear success message
        print(f"{Colors.GREEN}✅ Valid{Colors.END}: {Colors.BOLD}{entity_type}{Colors.END} → {file_name}")
    else:
        # ❌ Clear error message with numbered list
        print(f"{Colors.RED}❌ Invalid{Colors.END}: {Colors.BOLD}{entity_type}{Colors.END} → {file_name}")
        print(f"{Colors.YELLOW}   Errors found:{Colors.END}")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
        print()  # Extra spacing for readability


def main():
    if len(sys.argv) < 2:
        print(f"{Colors.BOLD}Usage:{Colors.END} python validate_entity.py <file.md> [file2.md ...]")
        print(f"{Colors.BOLD}Example:{Colors.END} python validate_entity.py memory-bank/10_Projects/proj-2025-website.md")
        sys.exit(1)
    
    files = [Path(arg) for arg in sys.argv[1:]]
    
    # Validate all files
    results = []
    for file_path in files:
        if not file_path.exists():
            print(f"{Colors.RED}❌ File not found:{Colors.END} {file_path}")
            continue
        
        if not file_path.suffix == '.md':
            print(f"{Colors.YELLOW}⚠️  Skipping non-Markdown file:{Colors.END} {file_path.name}")
            continue
        
        success, entity_type, errors = validate_entity(file_path)
        results.append((file_path, success, entity_type, errors))
        print_validation_result(file_path, success, entity_type, errors)
    
    # Summary
    total = len(results)
    valid = sum(1 for _, success, _, _ in results if success)
    invalid = total - valid
    
    print(f"{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    if invalid == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ All {total} file(s) valid!{Colors.END}")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}Summary:{Colors.END} {Colors.GREEN}{valid} valid{Colors.END}, {Colors.RED}{invalid} invalid{Colors.END} (out of {total} total)")
        sys.exit(1)  # Exit with error code if any validation failed


if __name__ == "__main__":
    main()
