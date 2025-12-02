"""
pytest configuration and shared fixtures for AI Life OS tests

This file contains:
- Common fixtures (temp dirs, mock data, etc.)
- Test configuration
- Reusable test utilities
"""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_repo(tmp_path):
    """
    Create a temporary git repository for testing.
    
    Returns:
        Path: Path to temporary repo root
    """
    repo_dir = tmp_path / "test-repo"
    repo_dir.mkdir()
    
    # Initialize git repo
    import subprocess
    subprocess.run(
        ["git", "init"],
        cwd=repo_dir,
        check=True,
        capture_output=True
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_dir,
        check=True,
        capture_output=True
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo_dir,
        check=True,
        capture_output=True
    )
    
    return repo_dir


@pytest.fixture
def truth_layer_dir(temp_repo):
    """
    Create truth-layer directory structure.
    
    Returns:
        Path: Path to truth-layer directory
    """
    truth_layer = temp_repo / "truth-layer"
    truth_layer.mkdir()
    
    # Create subdirectories
    (truth_layer / "areas").mkdir()
    (truth_layer / "projects").mkdir()
    (truth_layer / "tasks").mkdir()
    (truth_layer / "contexts").mkdir()
    (truth_layer / "identities").mkdir()
    (truth_layer / "logs").mkdir()
    
    return truth_layer


@pytest.fixture
def sample_yaml_entity():
    """
    Return sample YAML entity for testing.
    
    Returns:
        dict: Sample entity data
    """
    return {
        "entity_type": "project",
        "id": "proj-test-001",
        "title": "Test Project",
        "status": "active",
        "created_at": "2025-12-02T12:00:00Z",
        "updated_at": "2025-12-02T12:00:00Z"
    }


@pytest.fixture
def sample_cr():
    """
    Return sample Change Request for testing.
    
    Returns:
        dict: Sample CR data
    """
    return {
        "cr_id": "CR-20251202-120000-abcd",
        "created_at": "2025-12-02T12:00:00Z",
        "status": "pending",
        "drift_report": "drift/2025-12-02-120000-drift.yaml",
        "changes": [
            {
                "entity_id": "proj-test-001",
                "field": "status",
                "old_value": "active",
                "new_value": "completed",
                "rationale": "Test completion"
            }
        ]
    }
