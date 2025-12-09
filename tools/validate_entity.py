#!/usr/bin/env python3
"""
Life Graph Entity Validator

Validates YAML frontmatter in Life Graph entity files.
Checks required fields, field types, and canonical field names.

Usage:
    python validate_entity.py <file_or_directory>
    python validate_entity.py --staged  # Validate staged files in git
"""

import sys
import yaml
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Entity schemas (required fields + types)
ENTITY_SCHEMAS = {
    'area': {
        'required': ['type', 'id', 'name', 'active'],
        'optional': ['vision', 'contexts', 'review_frequency'],
        'enums': {
            'review_frequency': ['daily', 'weekly', 'monthly', 'quarterly']
        }
    },
    'project': {
        'required': ['type', 'id', 'title', 'status', 'created', 'energy_profile', 'dopamine_level'],
        'optional': ['area', 'do_date', 'due_date', 'is_frog', 'contexts', 'blockers', 'review_cadence'],
        'enums': {
            'status': ['planning', 'active', 'blocked', 'completed', 'archived'],
            'dopamine_level': ['high', 'medium', 'low', 'negative'],
            'review_cadence': ['daily', 'weekly', 'monthly']
        }
    },
    'task': {
        'required': ['type', 'id', 'title', 'status', 'created', 'energy_profile', 'contexts'],
        'optional': ['project', 'area', 'do_date', 'duration_minutes', 'dopamine_level', 'is_frog', 'dependencies'],
        'enums': {
            'status': ['inbox', 'next', 'waiting', 'scheduled', 'completed'],
            'dopamine_level': ['high', 'medium', 'low', 'negative']
        }
    },
    'context': {
        'required': ['type', 'context_name'],
        'optional': ['created', 'energy_fit', 'tools_available'],
        'enums': {
            'energy_fit': ['high_focus', 'creative', 'admin', 'low_energy']
        }
    },
    'identity': {
        'required': ['type', 'id', 'title'],
        'optional': ['default_context', 'ideal_time_block', 'associated_areas'],
        'enums': {
            'ideal_time_block': ['Morning', 'Afternoon', 'Evening', 'Night']
        }
    },
    'log': {
        'required': ['type', 'id', 'timestamp'],
        'optional': ['tags', 'linked_entities', 'mood'],
        'enums': {
            'mood': ['high', 'neutral', 'low']
        }
    }
}

# Valid energy profile values
ENERGY_PROFILE_VALUES = ['high_focus', 'creative', 'admin', 'low_energy']

# Deprecated field names (old_name -> new_name)
DEPRECATED_FIELDS = {
    'dopamine_reward': 'dopamine_level',
    'scheduled': 'do_date',  # For Project entities
}


def extract_frontmatter(content: str) -> Optional[Dict]:
    """Extract YAML frontmatter from markdown file."""
    # Match YAML frontmatter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None
    
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return None


def validate_entity(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate a single Life Graph entity file.
    
    Returns:
        (is_valid, errors) - is_valid is True if no errors, errors is list of error messages
    """
    errors = []
    
    # Read file
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f"Failed to read file: {e}"]
    
    # Extract frontmatter
    frontmatter = extract_frontmatter(content)
    if frontmatter is None:
        return False, ["Missing or invalid YAML frontmatter"]
    
    # Check entity type
    entity_type = frontmatter.get('type')
    if not entity_type:
        return False, ["Missing required field: 'type'"]
    
    if entity_type not in ENTITY_SCHEMAS:
        return False, [f"Unknown entity type: '{entity_type}' (valid: {', '.join(ENTITY_SCHEMAS.keys())})"]
    
    schema = ENTITY_SCHEMAS[entity_type]
    
    # Check required fields (be lenient with templates that have None/null placeholders)
    for field in schema['required']:
        if field not in frontmatter:
            errors.append(f"Missing required field: '{field}'")
        elif frontmatter[field] is None or frontmatter[field] == 'None' or frontmatter[field] == 'null':
            # Allow None/null in templates for required fields
            pass
    
    # Check for deprecated field names
    for old_name, new_name in DEPRECATED_FIELDS.items():
        if old_name in frontmatter:
            errors.append(f"Deprecated field '{old_name}' - use '{new_name}' instead")
    
    # Validate energy_profile (if present)
    if 'energy_profile' in frontmatter:
        energy_profile = frontmatter['energy_profile']
        if not isinstance(energy_profile, list):
            errors.append(f"Field 'energy_profile' must be array, got {type(energy_profile).__name__}")
        else:
            for value in energy_profile:
                if value not in ENERGY_PROFILE_VALUES:
                    errors.append(f"Invalid energy_profile value: '{value}' (valid: {', '.join(ENERGY_PROFILE_VALUES)})")
    
    # Validate enum fields (skip if value is None/null for optional fields)
    if 'enums' in schema:
        for field, valid_values in schema['enums'].items():
            if field in frontmatter:
                value = frontmatter[field]
                # Skip validation if value is None (for optional fields in templates)
                if value is None or value == 'None' or value == 'null':
                    continue
                if value not in valid_values:
                    errors.append(f"Invalid {field}: '{value}' (valid: {', '.join(valid_values)})")
    
    # Validate ID format (if present)
    if 'id' in frontmatter:
        entity_id = frontmatter['id']
        expected_prefix = {
            'area': 'area-',
            'project': 'proj-',
            'task': 'task-',
            'identity': 'role-',
            'log': 'log-'
        }.get(entity_type)
        
        if expected_prefix and not entity_id.startswith(expected_prefix):
            errors.append(f"ID should start with '{expected_prefix}' (got: '{entity_id}')")
    
    return len(errors) == 0, errors


def validate_file(file_path: Path, verbose: bool = False) -> bool:
    """Validate a single file and print results."""
    is_valid, errors = validate_entity(file_path)
    
    if is_valid:
        print(f"✅ VALID: {file_path.name}")
        return True
    else:
        print(f"❌ INVALID: {file_path.name}")
        for error in errors:
            print(f"  - {error}")
        return False


def validate_directory(dir_path: Path, verbose: bool = False) -> Tuple[int, int]:
    """
    Validate all .md files in directory recursively.
    
    Returns:
        (valid_count, total_count)
    """
    md_files = list(dir_path.rglob('*.md'))
    
    if not md_files:
        print(f"No .md files found in {dir_path}")
        return 0, 0
    
    valid_count = 0
    for file_path in md_files:
        # Skip non-entity files (README, documentation, etc.)
        if file_path.name in ['README.md', 'LIFE_GRAPH_SCHEMA.md', 'START_HERE.md']:
            continue
        
        if validate_file(file_path, verbose):
            valid_count += 1
    
    total_count = len(md_files)
    print(f"\n📊 Results: {valid_count}/{total_count} files valid")
    
    return valid_count, total_count


def validate_staged_files() -> bool:
    """Validate git staged .md files in memory-bank/."""
    import subprocess
    
    try:
        # Get staged files
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True,
            text=True,
            check=True
        )
        
        staged_files = result.stdout.strip().split('\n')
        
        # Filter for .md files in memory-bank/
        entity_files = [
            Path(f) for f in staged_files 
            if f.endswith('.md') and 'memory-bank' in f and Path(f).exists()
        ]
        
        if not entity_files:
            print("No entity files staged for commit")
            return True
        
        print(f"🔍 Validating {len(entity_files)} staged file(s)...\n")
        
        all_valid = True
        for file_path in entity_files:
            # Skip non-entity files
            if file_path.name in ['README.md', 'LIFE_GRAPH_SCHEMA.md', 'START_HERE.md']:
                continue
            
            if not validate_file(file_path):
                all_valid = False
        
        return all_valid
        
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_entity.py <file_or_directory>")
        print("       python validate_entity.py --staged")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    # Handle --staged flag
    if arg == '--staged':
        success = validate_staged_files()
        sys.exit(0 if success else 1)
    
    # Handle file or directory
    path = Path(arg)
    
    if not path.exists():
        print(f"Error: Path does not exist: {path}")
        sys.exit(1)
    
    if path.is_file():
        success = validate_file(path, verbose=True)
        sys.exit(0 if success else 1)
    
    elif path.is_dir():
        valid_count, total_count = validate_directory(path, verbose=True)
        sys.exit(0 if valid_count == total_count else 1)
    
    else:
        print(f"Error: Path is neither file nor directory: {path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
