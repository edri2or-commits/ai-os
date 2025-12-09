#!/usr/bin/env python3
"""
Input Validation - Security layer for AI Life OS tools

Provides validation functions to prevent:
- Path traversal attacks
- Command injection
- Format violations
- YAML schema violations

Usage:
    from input_validation import validate_cr_id, validate_file_path
    
    cr_id = "CR-20251202-123456-abcd"
    if not validate_cr_id(cr_id):
        raise ValueError(f"Invalid CR ID: {cr_id}")
"""

import re
from pathlib import Path
from typing import Optional, Dict, Any
import os


def validate_cr_id(cr_id: str) -> bool:
    """
    Validate Change Request ID format.
    
    Expected format: CR-YYYYMMDD-HHMMSS-xxxx
    Example: CR-20251202-123456-abcd
    
    Args:
        cr_id: Change Request ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not cr_id or not isinstance(cr_id, str):
        return False
    
    # Pattern: CR-YYYYMMDD-HHMMSS-xxxx
    pattern = r'^CR-\d{8}-\d{6}-[a-z0-9]{4}$'
    return bool(re.match(pattern, cr_id))


def validate_file_path(file_path: str, allowed_base: Optional[str] = None) -> bool:
    """
    Validate file path to prevent path traversal attacks.
    
    Checks:
    - No parent directory references (..)
    - No absolute paths to sensitive directories
    - Path is within allowed_base if specified
    
    Args:
        file_path: Path to validate
        allowed_base: Optional base directory (must be within this)
        
    Returns:
        True if valid, False otherwise
    """
    if not file_path or not isinstance(file_path, str):
        return False
    
    # Check for parent directory references (BEFORE normalization)
    if '..' in file_path:
        return False
    
    # Normalize path
    try:
        normalized = Path(file_path).resolve()
    except (ValueError, OSError):
        return False
    
    # Check if within allowed_base
    if allowed_base:
        try:
            base = Path(allowed_base).resolve()
            if not str(normalized).startswith(str(base)):
                return False
        except (ValueError, OSError):
            return False
    
    # Block access to sensitive directories
    sensitive_dirs = [
        '/etc',
        '/sys',
        '/proc',
        '/dev',
        'C:\\Windows\\System32',
        'C:\\Program Files',
    ]
    
    path_str = str(normalized)
    for sensitive in sensitive_dirs:
        if path_str.startswith(sensitive):
            return False
    
    return True


def validate_yaml_schema(data: Dict[str, Any], required_fields: list) -> bool:
    """
    Validate YAML content has required fields.
    
    Args:
        data: Parsed YAML data (dict)
        required_fields: List of required field names
        
    Returns:
        True if all required fields present, False otherwise
    """
    if not isinstance(data, dict):
        return False
    
    for field in required_fields:
        if field not in data:
            return False
    
    return True


def validate_commit_message(message: str, max_length: int = 500) -> bool:
    """
    Validate git commit message to prevent command injection.
    
    Checks:
    - No shell metacharacters (|, &, ;, $, `, etc.)
    - No newlines (prevents multi-line injection)
    - Reasonable length
    
    Args:
        message: Commit message to validate
        max_length: Maximum allowed length
        
    Returns:
        True if valid, False otherwise
    """
    if not message or not isinstance(message, str):
        return False
    
    # Check length
    if len(message) > max_length:
        return False
    
    # Block shell metacharacters
    dangerous_chars = ['|', '&', ';', '$', '`', '\n', '\r', '$(', '${']
    for char in dangerous_chars:
        if char in message:
            return False
    
    return True


def validate_entity_type(entity_type: str) -> bool:
    """
    Validate Life Graph entity type.
    
    Args:
        entity_type: Entity type to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_types = ['area', 'project', 'task', 'context', 'identity', 'log']
    return entity_type in valid_types


def validate_status(status: str, entity_type: str) -> bool:
    """
    Validate status field based on entity type.
    
    Args:
        status: Status value to validate
        entity_type: Entity type (determines allowed statuses)
        
    Returns:
        True if valid, False otherwise
    """
    valid_statuses = {
        'area': ['active', 'dormant', 'archived'],
        'project': ['active', 'paused', 'completed', 'cancelled', 'archived'],
        'task': ['todo', 'in_progress', 'blocked', 'done', 'cancelled'],
        'context': ['active', 'dormant', 'archived'],
        'identity': ['active', 'exploring', 'dormant'],
        'log': ['N/A']  # Logs don't have status
    }
    
    if entity_type not in valid_statuses:
        return False
    
    return status in valid_statuses[entity_type]


# Convenience function for common validation
def validate_truth_layer_path(file_path: str) -> bool:
    """
    Validate path is within truth-layer directory.
    
    Args:
        file_path: Path to validate
        
    Returns:
        True if within truth-layer, False otherwise
    """
    # Determine truth-layer base path
    # This assumes script runs from repo root or has REPO_ROOT env var
    repo_root = os.environ.get('REPO_ROOT', os.getcwd())
    truth_layer = Path(repo_root) / 'truth-layer'
    
    return validate_file_path(file_path, str(truth_layer))


if __name__ == "__main__":
    # Self-test
    print("Running input_validation self-tests...")
    
    # Test CR ID validation
    assert validate_cr_id("CR-20251202-123456-abcd") == True
    assert validate_cr_id("CR-20251202-123456-ABCD") == False  # uppercase
    assert validate_cr_id("INVALID") == False
    print("[OK] CR ID validation")
    
    # Test file path validation
    assert validate_file_path("C:\\Users\\user\\file.txt") == True
    assert validate_file_path("C:\\Windows\\System32\\config\\SAM") == False
    assert validate_file_path("..\\..\\..\\Windows\\System32\\config\\SAM") == False
    print("[OK] File path validation")
    
    # Test commit message validation
    assert validate_commit_message("feat: add validation") == True
    assert validate_commit_message("feat: add | rm -rf /") == False
    assert validate_commit_message("a" * 501) == False
    print("[OK] Commit message validation")
    
    # Test entity type validation
    assert validate_entity_type("project") == True
    assert validate_entity_type("invalid") == False
    print("[OK] Entity type validation")
    
    # Test status validation
    assert validate_status("active", "project") == True
    assert validate_status("invalid", "project") == False
    assert validate_status("done", "area") == False  # wrong entity type
    print("[OK] Status validation")
    
    print("\n[OK] All self-tests passed!")
