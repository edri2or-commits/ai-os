"""
Snapshot tests using Syrupy

These tests capture the output of functions and save them as "snapshots".
On future runs, the output is compared to the snapshot to detect regressions.

When to use snapshots:
- Testing structured output (YAML, JSON, reports)
- Detecting unintended changes in output format
- Regression testing for complex transformations
"""

import sys
from pathlib import Path
import subprocess
import yaml

# Add tools/ to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from observer import Observer


class TestObserverSnapshots:
    """Snapshot tests for Observer output structures."""
    
    def test_drift_report_structure(self, truth_layer_dir, snapshot):
        """Drift report structure should remain stable across changes."""
        # Create a test scenario
        yaml_file = truth_layer_dir / "projects" / "test.yaml"
        yaml_file.write_text("id: test-001\ntitle: Original")
        
        repo = truth_layer_dir.parent
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Modify file
        yaml_file.write_text("id: test-001\ntitle: Modified")
        
        # Detect drift
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        
        # Snapshot the structure (not the exact diff content)
        drift_structure = {
            "files_scanned": files_scanned,
            "drift_count": len(drift_list),
            "drift_types": [d["type"] for d in drift_list],
            "has_diff": [d["diff"] is not None for d in drift_list]
        }
        
        assert drift_structure == snapshot
    
    def test_empty_drift_report(self, truth_layer_dir, snapshot):
        """Empty drift report structure should be consistent."""
        # Create and commit a file
        yaml_file = truth_layer_dir / "projects" / "test.yaml"
        yaml_file.write_text("id: test-001")
        
        repo = truth_layer_dir.parent
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # No changes - clean state
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        
        result = {
            "files_scanned": files_scanned,
            "drift_count": len(drift_list),
            "drift_list": drift_list
        }
        
        assert result == snapshot
    
    def test_multiple_files_drift(self, truth_layer_dir, snapshot):
        """Multiple files drift detection should have consistent structure."""
        # Create multiple files
        for i in range(3):
            yaml_file = truth_layer_dir / "projects" / f"test-{i}.yaml"
            yaml_file.write_text(f"id: test-{i:03d}\ntitle: Original {i}")
        
        repo = truth_layer_dir.parent
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Modify all files
        for i in range(3):
            yaml_file = truth_layer_dir / "projects" / f"test-{i}.yaml"
            yaml_file.write_text(f"id: test-{i:03d}\ntitle: Modified {i}")
        
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        
        # Snapshot summary (not full diffs)
        summary = {
            "files_scanned": files_scanned,
            "modified_count": sum(1 for d in drift_list if d["type"] == "modified"),
            "all_have_diffs": all(d["diff"] is not None for d in drift_list if d["type"] == "modified")
        }
        
        assert summary == snapshot


class TestValidationSnapshots:
    """Snapshot tests for validation error messages."""
    
    def test_cr_id_validation_messages(self, snapshot):
        """CR ID validation should produce consistent error behavior."""
        from input_validation import validate_cr_id
        
        test_cases = {
            "valid": "CR-20251202-120000-abcd",
            "missing_prefix": "20251202-120000-abcd",
            "wrong_date_length": "CR-2025120-120000-abcd",
            "uppercase_suffix": "CR-20251202-120000-ABCD",
            "empty": "",
            "too_short": "CR-2025",
        }
        
        results = {
            case_name: validate_cr_id(case_value)
            for case_name, case_value in test_cases.items()
        }
        
        assert results == snapshot
    
    def test_entity_status_validation_matrix(self, snapshot):
        """Entity status validation matrix should remain stable."""
        from input_validation import validate_status
        
        entities = ["area", "project", "task", "context", "identity", "log"]
        statuses = ["active", "paused", "completed", "todo", "done", "dormant", "archived"]
        
        # Build validation matrix
        matrix = {}
        for entity in entities:
            matrix[entity] = {
                status: validate_status(status, entity)
                for status in statuses
            }
        
        assert matrix == snapshot
