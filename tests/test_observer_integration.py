"""
Observer Integration Tests - Full workflow testing

Tests the Observer system with real git operations and YAML validation:
- Complete Observer + Git workflow (commit, modify, detect, report)
- Observer + YAML schema validation integration
- Multiple files drift detection
- Real git repository operations

These are integration tests - they test Observer working with real git and file system.
"""

import sys
from pathlib import Path
import subprocess
import yaml

# Add tools/ to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from observer import Observer
import pytest


class TestObserverGitIntegration:
    """Test Observer with real git operations."""
    
    def test_full_drift_detection_workflow(self, truth_layer_dir):
        """
        Test complete Observer workflow: create → commit → modify → detect → report.
        
        This tests the full happy path:
        1. Create YAML files in truth-layer
        2. Commit them to git
        3. Modify one file
        4. Run Observer.detect_drift()
        5. Verify drift detected correctly
        6. Generate drift report
        7. Verify report structure
        """
        repo = truth_layer_dir.parent
        
        # Step 1: Create initial YAML files
        project_file = truth_layer_dir / "projects" / "test-project.yaml"
        project_file.write_text("""entity_type: project
id: proj-test-001
title: Test Project
status: active
created_at: '2025-12-02T12:00:00Z'
updated_at: '2025-12-02T12:00:00Z'
""")
        
        area_file = truth_layer_dir / "areas" / "test-area.yaml"
        area_file.write_text("""entity_type: area
id: area-test-001
title: Test Area
status: active
created_at: '2025-12-02T12:00:00Z'
updated_at: '2025-12-02T12:00:00Z'
""")
        
        # Step 2: Commit to git
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit with test entities"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Step 3: Modify project file (simulate drift)
        project_file.write_text("""entity_type: project
id: proj-test-001
title: Test Project - MODIFIED
status: completed
created_at: '2025-12-02T12:00:00Z'
updated_at: '2025-12-02T13:00:00Z'
""")
        
        # Step 4: Run Observer
        observer = Observer(repo, verbose=False)
        drift_list, files_scanned = observer.detect_drift()
        
        # Step 5: Verify drift detected
        assert files_scanned == 2, "Should scan 2 YAML files"
        assert len(drift_list) == 1, "Should detect 1 modified file"
        
        drift_entry = drift_list[0]
        assert drift_entry["type"] == "modified"
        assert "test-project.yaml" in drift_entry["path"]
        assert drift_entry["diff"] is not None
        assert "MODIFIED" in drift_entry["diff"]
        assert "completed" in drift_entry["diff"]
        
        # Step 6: Generate drift report
        report_path = observer.generate_report(drift_list, files_scanned)
        
        # Step 7: Verify report file exists and structure
        assert report_path.exists()
        assert report_path.suffix == ".yaml"
        
        # Load and verify report content
        with open(report_path, "r", encoding="utf-8") as f:
            report_data = yaml.safe_load(f)
        
        assert "metadata" in report_data
        assert "drift" in report_data
        
        metadata = report_data["metadata"]
        assert metadata["observer_version"] == Observer.VERSION
        assert metadata["files_scanned"] == 2
        assert metadata["files_with_drift"] == 1
        assert "detected_at" in metadata
        
        # Verify drift entry in report
        assert len(report_data["drift"]) == 1
        report_drift = report_data["drift"][0]
        assert report_drift["path"] == drift_entry["path"]
        assert report_drift["type"] == "modified"
        assert report_drift["diff"] is not None
    
    def test_observer_with_schema_validation(self, truth_layer_dir):
        """
        Test Observer with YAML schema validation integration.
        
        Tests that Observer can:
        1. Detect drift in YAML files
        2. Validate YAML structure is parseable
        3. Handle invalid YAML gracefully (no crash)
        """
        repo = truth_layer_dir.parent
        
        # Create valid YAML and commit
        valid_file = truth_layer_dir / "projects" / "valid.yaml"
        valid_file.write_text("""entity_type: project
id: proj-valid-001
title: Valid Project
status: active
""")
        
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add valid file"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Modify to create drift (still valid YAML)
        valid_file.write_text("""entity_type: project
id: proj-valid-001
title: Valid Project - Updated
status: completed
""")
        
        # Run Observer
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        
        # Verify drift detected
        assert len(drift_list) == 1
        assert drift_list[0]["type"] == "modified"
        
        # Verify YAML is parseable
        yaml_content = yaml.safe_load(valid_file.read_text())
        assert yaml_content["entity_type"] == "project"
        assert yaml_content["status"] == "completed"
        
        # Verify diff contains expected changes
        diff = drift_list[0]["diff"]
        assert "Updated" in diff
        assert "completed" in diff
    
    def test_multiple_files_drift_detection(self, truth_layer_dir):
        """
        Test Observer detecting drift in multiple files simultaneously.
        
        Scenarios:
        1. Multiple modified files
        2. Mix of modified + added files
        """
        repo = truth_layer_dir.parent
        
        # Create 3 files and commit
        files = {
            "projects/proj-001.yaml": "entity_type: project\nid: proj-001\ntitle: Project 1\n",
            "projects/proj-002.yaml": "entity_type: project\nid: proj-002\ntitle: Project 2\n",
            "areas/area-001.yaml": "entity_type: area\nid: area-001\ntitle: Area 1\n",
        }
        
        for path, content in files.items():
            file = truth_layer_dir / path
            file.write_text(content)
        
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add multiple files"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Modify 2 files
        (truth_layer_dir / "projects/proj-001.yaml").write_text(
            "entity_type: project\nid: proj-001\ntitle: Project 1 MODIFIED\n"
        )
        (truth_layer_dir / "areas/area-001.yaml").write_text(
            "entity_type: area\nid: area-001\ntitle: Area 1 UPDATED\n"
        )
        
        # Add new file and stage it
        new_file = truth_layer_dir / "projects/proj-003.yaml"
        new_file.write_text("entity_type: project\nid: proj-003\ntitle: New Project\n")
        subprocess.run(["git", "add", str(new_file)], cwd=repo, check=True)
        
        # Run Observer
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        
        # Verify multiple drifts detected
        assert files_scanned == 4, "Should scan 4 YAML files"
        assert len(drift_list) == 3, "Should detect 3 changes (2 modified + 1 added)"
        
        # Verify drift types
        types = {d["type"] for d in drift_list}
        assert "modified" in types
        assert "added" in types
        
        # Verify specific files
        paths = {d["path"] for d in drift_list}
        assert any("proj-001.yaml" in p for p in paths)
        assert any("area-001.yaml" in p for p in paths)
        assert any("proj-003.yaml" in p for p in paths)
        
        # Verify diffs exist for modified files
        modified_drifts = [d for d in drift_list if d["type"] == "modified"]
        assert all(d["diff"] is not None for d in modified_drifts)
        assert all(len(d["diff"]) > 0 for d in modified_drifts)


class TestObserverReportGeneration:
    """Test drift report generation and structure."""
    
    def test_drift_report_metadata(self, truth_layer_dir):
        """
        Test that drift reports contain correct metadata.
        
        Metadata should include:
        - observer_version
        - detected_at (ISO 8601 format)
        - files_scanned (count)
        - files_with_drift (count)
        """
        repo = truth_layer_dir.parent
        
        # Create and commit a file
        test_file = truth_layer_dir / "projects" / "metadata-test.yaml"
        test_file.write_text("entity_type: project\nid: meta-001\n")
        
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add metadata test file"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Modify file
        test_file.write_text("entity_type: project\nid: meta-001\ntitle: Modified\n")
        
        # Generate report
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        report_path = observer.generate_report(drift_list, files_scanned)
        
        # Load and verify report
        with open(report_path, "r", encoding="utf-8") as f:
            report = yaml.safe_load(f)
        
        # Verify metadata structure
        assert "metadata" in report
        metadata = report["metadata"]
        
        assert "observer_version" in metadata
        assert metadata["observer_version"] == Observer.VERSION
        
        assert "detected_at" in metadata
        assert "T" in metadata["detected_at"]  # ISO 8601 format
        assert "Z" in metadata["detected_at"]  # UTC timezone
        
        assert "files_scanned" in metadata
        assert metadata["files_scanned"] == 1
        
        assert "files_with_drift" in metadata
        assert metadata["files_with_drift"] == 1
        
        assert "drift" in report
        assert isinstance(report["drift"], list)
        assert len(report["drift"]) == 1
    
    def test_drift_report_yaml_format(self, truth_layer_dir):
        """
        Test that drift reports can be saved and loaded as YAML.
        
        This ensures reports are human-readable and machine-parseable.
        """
        repo = truth_layer_dir.parent
        
        # Create drift scenario
        test_file = truth_layer_dir / "projects" / "yaml-test.yaml"
        test_file.write_text("entity_type: project\nid: yaml-001\n")
        
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add yaml test"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        test_file.write_text("entity_type: project\nid: yaml-001\ntitle: Test\n")
        
        # Generate report
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        report_path = observer.generate_report(drift_list, files_scanned)
        
        # Load report
        with open(report_path, "r", encoding="utf-8") as f:
            report = yaml.safe_load(f)
        
        # Convert to YAML and back (round-trip test)
        yaml_str = yaml.dump(report, default_flow_style=False)
        parsed_report = yaml.safe_load(yaml_str)
        
        # Verify round-trip preserves structure
        assert parsed_report["metadata"]["observer_version"] == report["metadata"]["observer_version"]
        assert parsed_report["metadata"]["files_scanned"] == report["metadata"]["files_scanned"]
        assert parsed_report["metadata"]["files_with_drift"] == report["metadata"]["files_with_drift"]
        assert len(parsed_report["drift"]) == len(report["drift"])


class TestObserverEdgeCases:
    """Test Observer behavior in edge cases."""
    
    def test_observer_with_empty_truth_layer(self, truth_layer_dir):
        """
        Test Observer when truth-layer exists but contains no YAML files.
        
        Should return:
        - drift_list: []
        - files_scanned: 0
        """
        repo = truth_layer_dir.parent
        
        # Commit empty truth-layer (with .gitkeep to make git track it)
        gitkeep = truth_layer_dir / ".gitkeep"
        gitkeep.write_text("")
        
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Empty truth-layer"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Run Observer
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        
        assert drift_list == []
        assert files_scanned == 0


class TestObserverErrorHandling:
    """Test Observer error handling and resilience."""
    
    def test_observer_with_corrupt_yaml(self, truth_layer_dir):
        """
        Test Observer gracefully handles corrupt YAML files.
        
        Observer should either:
        - Skip corrupt files and continue processing valid ones
        - Log error but not crash
        """
        repo = truth_layer_dir.parent
        
        # Create valid YAML
        valid_file = truth_layer_dir / "projects" / "valid.yaml"
        valid_file.write_text("entity_type: project\nid: proj-valid\ntitle: Valid\n")
        
        # Create corrupt YAML (invalid syntax)
        corrupt_file = truth_layer_dir / "projects" / "corrupt.yaml"
        corrupt_file.write_text("entity_type: project\n{bad: [syntax\nunclosed brackets")
        
        # Commit both
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add valid and corrupt YAML"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Modify valid file to create drift
        valid_file.write_text("entity_type: project\nid: proj-valid\ntitle: Valid MODIFIED\n")
        
        # Modify corrupt file too
        corrupt_file.write_text("entity_type: project\n{still: bad syntax")
        
        # Observer should handle gracefully (not crash)
        observer = Observer(repo, verbose=False)
        drift_list, files_scanned = observer.detect_drift()
        
        # Should process at least the valid file
        assert files_scanned >= 1, "Should scan at least 1 file"
        
        # Should detect drift in valid file
        valid_drifts = [d for d in drift_list if "valid.yaml" in d["path"]]
        assert len(valid_drifts) == 1, "Should detect drift in valid file"
        assert "MODIFIED" in valid_drifts[0]["diff"]
    
    def test_observer_with_missing_truth_layer(self, truth_layer_dir):
        """
        Test Observer behavior when truth-layer directory is missing.
        
        Expected: Observer should detect absence and return empty results or error.
        """
        repo = truth_layer_dir.parent
        
        # Initialize git repo (truth_layer_dir fixture already does this)
        # Delete truth-layer directory after Observer init would need it
        import shutil
        
        # Create and commit something first
        test_file = truth_layer_dir / "projects" / "test.yaml"
        test_file.write_text("entity_type: project\nid: test-001\n")
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Now delete truth-layer
        shutil.rmtree(truth_layer_dir)
        
        # Observer should handle missing directory
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        
        # Should return empty results (no files to scan)
        assert files_scanned == 0
        # Drift list might contain deleted files or be empty
        # Either is acceptable - just don't crash
        assert isinstance(drift_list, list)
    
    def test_observer_with_non_git_repo(self, tmp_path):
        """
        Test Observer on a directory that is NOT a git repository.
        
        Expected: Observer should raise GitNotFoundError when git is not available.
        """
        # Import the exception class
        from observer import GitNotFoundError
        
        # Create non-git directory
        non_git_dir = tmp_path / "non-git"
        non_git_dir.mkdir()
        
        # Create truth-layer structure
        truth_layer = non_git_dir / "truth-layer"
        truth_layer.mkdir()
        (truth_layer / "projects").mkdir()
        
        test_file = truth_layer / "projects" / "test.yaml"
        test_file.write_text("entity_type: project\nid: test\n")
        
        # Observer should detect git is not available
        observer = Observer(non_git_dir)
        
        # check_git_available should return False
        git_available = observer.check_git_available()
        assert git_available is False, "Should detect git is not available"
        
        # detect_drift should raise GitNotFoundError in non-git repo
        with pytest.raises(GitNotFoundError):
            observer.detect_drift()
    
    def test_observer_with_mixed_valid_invalid_files(self, truth_layer_dir):
        """
        Test Observer with mix of valid and invalid YAML files.
        
        Observer should:
        - Process all valid files successfully
        - Handle invalid files without stopping entire scan
        """
        repo = truth_layer_dir.parent
        
        # Create 2 valid files
        valid1 = truth_layer_dir / "projects" / "valid-1.yaml"
        valid1.write_text("entity_type: project\nid: proj-001\ntitle: Project 1\n")
        
        valid2 = truth_layer_dir / "areas" / "valid-2.yaml"
        valid2.write_text("entity_type: area\nid: area-001\ntitle: Area 1\n")
        
        # Create 1 invalid file
        invalid = truth_layer_dir / "projects" / "invalid.yaml"
        invalid.write_text("!!this is not yaml at all!!\n{{{{broken}}}}\n")
        
        # Commit all
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add mixed valid/invalid files"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Modify all 3 files
        valid1.write_text("entity_type: project\nid: proj-001\ntitle: Project 1 UPDATED\n")
        valid2.write_text("entity_type: area\nid: area-001\ntitle: Area 1 UPDATED\n")
        invalid.write_text("!!still not yaml!!\n{{more broken}}\n")
        
        # Observer should process successfully
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        
        # Should scan all 3 files
        assert files_scanned == 3, "Should scan all 3 YAML files"
        
        # Should detect drift in all 3 files (git diff doesn't care about YAML validity)
        assert len(drift_list) == 3, "Should detect drift in all modified files"
        
        # Verify valid files are in drift list
        paths = [d["path"] for d in drift_list]
        assert any("valid-1.yaml" in p for p in paths)
        assert any("valid-2.yaml" in p for p in paths)
        assert any("invalid.yaml" in p for p in paths)


class TestObserverPerformance:
    """Test Observer performance with large datasets."""
    
    def test_observer_with_many_files(self, truth_layer_dir):
        """
        Test Observer performance with many YAML files.
        
        Creates 100 YAML files, modifies 50 of them, and verifies:
        - Observer completes in reasonable time (<5 seconds)
        - All files are scanned
        - Drift detection is accurate
        """
        import time
        
        repo = truth_layer_dir.parent
        
        # Create 100 YAML files
        for i in range(100):
            entity_type = "project" if i % 2 == 0 else "area"
            subdir = "projects" if entity_type == "project" else "areas"
            
            file = truth_layer_dir / subdir / f"{entity_type}-{i:03d}.yaml"
            file.write_text(f"""entity_type: {entity_type}
id: {entity_type}-{i:03d}
title: Test {entity_type.capitalize()} {i}
status: active
""")
        
        # Commit all files
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add 100 test files"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Modify 50 files (every other file)
        for i in range(0, 100, 2):
            entity_type = "project" if i % 2 == 0 else "area"
            subdir = "projects" if entity_type == "project" else "areas"
            
            file = truth_layer_dir / subdir / f"{entity_type}-{i:03d}.yaml"
            file.write_text(f"""entity_type: {entity_type}
id: {entity_type}-{i:03d}
title: Test {entity_type.capitalize()} {i} MODIFIED
status: completed
""")
        
        # Run Observer and measure time
        start_time = time.time()
        observer = Observer(repo, verbose=False)
        drift_list, files_scanned = observer.detect_drift()
        elapsed_time = time.time() - start_time
        
        # Performance assertions
        assert elapsed_time < 5.0, f"Observer took too long: {elapsed_time:.2f}s (expected <5s)"
        
        # Correctness assertions
        assert files_scanned == 100, "Should scan all 100 files"
        assert len(drift_list) == 50, "Should detect 50 modified files"
        
        # Verify all drifts are 'modified' type
        assert all(d["type"] == "modified" for d in drift_list)
    
    def test_observer_with_large_diffs(self, truth_layer_dir):
        """
        Test Observer with large file diffs (500+ lines).
        
        Verifies Observer can handle:
        - Large diff output from git
        - Files with many changes
        - No timeout or memory issues
        """
        repo = truth_layer_dir.parent
        
        # Create large YAML file with 500 lines
        large_file = truth_layer_dir / "projects" / "large-project.yaml"
        
        # Initial content: 500 lines
        content_lines = ["entity_type: project", "id: large-001", "title: Large Project"]
        content_lines += [f"field_{i:03d}: value_{i:03d}" for i in range(500)]
        
        large_file.write_text("\n".join(content_lines))
        
        # Commit
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add large file"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Modify most lines (change "value_XXX" to "modified_XXX")
        modified_lines = content_lines[:3]  # Keep header
        modified_lines += [f"field_{i:03d}: modified_{i:03d}" for i in range(500)]
        
        large_file.write_text("\n".join(modified_lines))
        
        # Run Observer
        observer = Observer(repo)
        drift_list, files_scanned = observer.detect_drift()
        
        # Should detect the large diff
        assert files_scanned == 1
        assert len(drift_list) == 1
        
        drift = drift_list[0]
        assert drift["type"] == "modified"
        assert "large-project.yaml" in drift["path"]
        
        # Diff should be large (many lines changed)
        diff_text = drift["diff"]
        assert diff_text is not None
        assert len(diff_text) > 1000, "Diff should be substantial"
        
        # Should contain evidence of modifications
        assert "modified_" in diff_text
    
    def test_observer_performance_benchmark(self, truth_layer_dir):
        """
        Benchmark Observer with realistic dataset.
        
        Creates:
        - 20 projects
        - 10 areas
        - 5 tasks
        Modifies 10 files
        
        Measures and reports performance metrics.
        """
        import time
        
        repo = truth_layer_dir.parent
        
        # Create realistic dataset
        # 20 projects
        for i in range(20):
            file = truth_layer_dir / "projects" / f"proj-{i:02d}.yaml"
            file.write_text(f"""entity_type: project
id: proj-{i:02d}
title: Project {i}
status: active
priority: {'high' if i % 3 == 0 else 'medium'}
""")
        
        # 10 areas
        for i in range(10):
            file = truth_layer_dir / "areas" / f"area-{i:02d}.yaml"
            file.write_text(f"""entity_type: area
id: area-{i:02d}
title: Area {i}
status: active
""")
        
        # 5 tasks
        for i in range(5):
            file = truth_layer_dir / "tasks" / f"task-{i:02d}.yaml"
            file.write_text(f"""entity_type: task
id: task-{i:02d}
title: Task {i}
status: todo
""")
        
        # Commit
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add realistic dataset"],
            cwd=repo,
            check=True,
            capture_output=True
        )
        
        # Modify 10 files (mix of types)
        for i in range(5):
            # Modify projects
            file = truth_layer_dir / "projects" / f"proj-{i:02d}.yaml"
            file.write_text(f"""entity_type: project
id: proj-{i:02d}
title: Project {i} UPDATED
status: completed
""")
        
        for i in range(3):
            # Modify areas
            file = truth_layer_dir / "areas" / f"area-{i:02d}.yaml"
            file.write_text(f"""entity_type: area
id: area-{i:02d}
title: Area {i} UPDATED
status: archived
""")
        
        for i in range(2):
            # Modify tasks
            file = truth_layer_dir / "tasks" / f"task-{i:02d}.yaml"
            file.write_text(f"""entity_type: task
id: task-{i:02d}
title: Task {i} DONE
status: completed
""")
        
        # Benchmark Observer
        start_time = time.time()
        observer = Observer(repo, verbose=False)
        drift_list, files_scanned = observer.detect_drift()
        elapsed_time = time.time() - start_time
        
        # Performance check
        assert elapsed_time < 2.0, f"Observer too slow for realistic dataset: {elapsed_time:.2f}s"
        
        # Correctness check
        assert files_scanned == 35, "Should scan 35 files (20+10+5)"
        assert len(drift_list) == 10, "Should detect 10 modified files"
        
        # Report performance (visible in test output with -v)
        print(f"\nPerformance: {files_scanned} files scanned in {elapsed_time:.3f}s")
        print(f"Throughput: {files_scanned / elapsed_time:.1f} files/second")
