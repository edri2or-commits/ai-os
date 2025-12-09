"""
Basic Observer tests - drift detection functionality

Tests the core Observer functionality:
- Initialization
- Git availability check
- YAML file detection
- Drift detection (clean state)
- Drift detection (with changes)
"""

import sys
from pathlib import Path
import subprocess

# Add tools/ to path so we can import observer
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from observer import Observer, GitNotFoundError
import pytest


class TestObserverBasics:
    """Test basic Observer initialization and setup."""
    
    def test_observer_initialization(self, temp_repo):
        """Observer initializes correctly with valid repo."""
        observer = Observer(temp_repo, verbose=False)
        
        assert observer.repo_root == temp_repo
        assert observer.verbose is False
        assert observer.truth_layer == temp_repo / "truth-layer"
        assert observer.drift_dir == temp_repo / "truth-layer" / "drift"
    
    def test_observer_verbose_mode(self, temp_repo):
        """Observer respects verbose flag."""
        observer = Observer(temp_repo, verbose=True)
        assert observer.verbose is True
    
    def test_check_git_available_in_repo(self, temp_repo):
        """check_git_available returns True in git repo."""
        observer = Observer(temp_repo)
        assert observer.check_git_available() is True
    
    def test_check_git_available_outside_repo(self, tmp_path):
        """check_git_available returns False outside git repo."""
        non_repo = tmp_path / "not-a-repo"
        non_repo.mkdir()
        
        observer = Observer(non_repo)
        assert observer.check_git_available() is False


class TestYAMLFileDetection:
    """Test YAML file detection in truth-layer."""
    
    def test_get_yaml_files_empty_truth_layer(self, temp_repo):
        """get_yaml_files returns empty list when no YAML files exist."""
        # Create truth-layer but no files
        truth_layer = temp_repo / "truth-layer"
        truth_layer.mkdir()
        
        observer = Observer(temp_repo)
        yaml_files = observer.get_yaml_files()
        
        assert yaml_files == []
    
    def test_get_yaml_files_with_yaml_files(self, truth_layer_dir):
        """get_yaml_files finds YAML files in truth-layer."""
        # Create some YAML files
        (truth_layer_dir / "projects" / "test-project.yaml").write_text("id: test-001")
        (truth_layer_dir / "areas" / "test-area.yml").write_text("id: area-001")
        
        observer = Observer(truth_layer_dir.parent)
        yaml_files = observer.get_yaml_files()
        
        assert len(yaml_files) == 2
        assert any("test-project.yaml" in f for f in yaml_files)
        assert any("test-area.yml" in f for f in yaml_files)
    
    def test_get_yaml_files_ignores_non_yaml(self, truth_layer_dir):
        """get_yaml_files ignores non-YAML files."""
        # Create YAML and non-YAML files
        (truth_layer_dir / "projects" / "test.yaml").write_text("id: test")
        (truth_layer_dir / "projects" / "readme.txt").write_text("not yaml")
        (truth_layer_dir / "projects" / "config.json").write_text("{}")
        
        observer = Observer(truth_layer_dir.parent)
        yaml_files = observer.get_yaml_files()
        
        assert len(yaml_files) == 1
        assert "test.yaml" in yaml_files[0]


class TestDriftDetection:
    """Test drift detection functionality."""
    
    def test_detect_drift_clean_state(self, truth_layer_dir):
        """detect_drift returns empty list when no changes."""
        # Create a file and commit it
        yaml_file = truth_layer_dir / "projects" / "test.yaml"
        yaml_file.write_text("id: test-001\ntitle: Test Project")
        
        repo = truth_layer_dir.parent
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add test file"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        
        assert drift_list == []
        assert files_scanned == 1
    
    def test_detect_drift_with_modified_file(self, truth_layer_dir):
        """detect_drift detects modified files."""
        # Create and commit a file
        yaml_file = truth_layer_dir / "projects" / "test.yaml"
        yaml_file.write_text("id: test-001\ntitle: Original")
        
        repo = truth_layer_dir.parent
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Modify the file
        yaml_file.write_text("id: test-001\ntitle: Modified")
        
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        
        assert len(drift_list) == 1
        assert drift_list[0]["type"] == "modified"
        assert "test.yaml" in drift_list[0]["path"]
        assert drift_list[0]["diff"] is not None
    
    def test_detect_drift_with_new_file(self, truth_layer_dir):
        """detect_drift detects new files in staging area."""
        # Create a placeholder file and commit it (git won't commit empty dirs)
        placeholder = truth_layer_dir / ".gitkeep"
        placeholder.write_text("")
        
        repo = truth_layer_dir.parent
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial empty"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Add new file and stage it (Observer detects staged files, not untracked)
        new_file = truth_layer_dir / "projects" / "new.yaml"
        new_file.write_text("id: new-001")
        subprocess.run(["git", "add", str(new_file)], cwd=repo, check=True)
        
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        
        assert len(drift_list) == 1
        assert drift_list[0]["type"] == "added"
        assert "new.yaml" in drift_list[0]["path"]
