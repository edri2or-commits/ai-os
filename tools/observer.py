#!/usr/bin/env python3
"""
Observer System - Drift Detection CLI

Detects drift in truth-layer YAML files by comparing working tree to last git commit.
Generates structured drift reports for human review and reconciliation.

Usage:
    python tools/observer.py [--verbose]

Exit Codes:
    0 - No drift detected (clean)
    1 - Drift detected (report generated)
    2 - Error (not in git repo, invalid YAML, etc.)
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ObserverError(Exception):
    """Base exception for Observer errors."""
    pass


class GitNotFoundError(ObserverError):
    """Raised when git is not available or repo is not initialized."""
    pass


class Observer:
    """Drift detection system for truth-layer YAML files."""
    
    VERSION = "0.1.0"
    TRUTH_LAYER_PATH = "truth-layer"
    DRIFT_REPORT_DIR = "truth-layer/drift"
    
    def __init__(self, repo_root: Path, verbose: bool = False):
        """
        Initialize Observer.
        
        Args:
            repo_root: Path to git repository root
            verbose: Enable verbose logging
        """
        self.repo_root = repo_root
        self.verbose = verbose
        self.truth_layer = repo_root / self.TRUTH_LAYER_PATH
        self.drift_dir = repo_root / self.DRIFT_REPORT_DIR
        
    def log(self, message: str, force: bool = False):
        """Log message if verbose mode enabled."""
        if self.verbose or force:
            print(f"[Observer] {message}")
    
    def check_git_available(self) -> bool:
        """Check if git is available and repo is initialized."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def get_yaml_files(self) -> List[str]:
        """Get list of YAML files in truth-layer (relative to repo root)."""
        if not self.truth_layer.exists():
            self.log(f"Truth layer directory does not exist: {self.truth_layer}")
            return []
        
        yaml_files = []
        for pattern in ["*.yaml", "*.yml"]:
            yaml_files.extend(self.truth_layer.rglob(pattern))
        
        # Convert to relative paths from repo root
        relative_paths = [
            str(f.relative_to(self.repo_root)).replace("\\", "/")
            for f in yaml_files
        ]
        
        self.log(f"Found {len(relative_paths)} YAML files in truth-layer")
        return relative_paths
    
    def detect_drift(self) -> Tuple[List[Dict], int]:
        """
        Detect drift in truth-layer YAML files.
        
        Returns:
            Tuple of (drift_list, files_scanned)
        """
        self.log("Detecting drift...")
        
        # Get all YAML files
        yaml_files = self.get_yaml_files()
        files_scanned = len(yaml_files)
        
        if files_scanned == 0:
            self.log("No YAML files found in truth-layer", force=True)
            return [], 0
        
        # Run git diff to detect changes
        result = subprocess.run(
            ["git", "diff", "HEAD", "--name-status", "--", self.TRUTH_LAYER_PATH],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            raise GitNotFoundError(f"Git diff failed: {result.stderr}")
        
        drift_list = []
        
        # Parse git diff output
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                continue
            
            status_code, filepath = parts
            
            # Only process YAML files
            if not (filepath.endswith(".yaml") or filepath.endswith(".yml")):
                continue
            
            # Map git status codes to drift types
            drift_type = self._map_status_to_type(status_code)
            
            if drift_type is None:
                continue
            
            # Get diff for modified files
            diff_content = None
            if drift_type == "modified":
                diff_content = self._get_file_diff(filepath)
            
            drift_entry = {
                "path": filepath,
                "type": drift_type,
                "diff": diff_content
            }
            
            drift_list.append(drift_entry)
            self.log(f"  {drift_type.upper()}: {filepath}")
        
        return drift_list, files_scanned
    
    def _map_status_to_type(self, status_code: str) -> Optional[str]:
        """Map git status code to drift type."""
        mapping = {
            "M": "modified",
            "A": "added",
            "D": "deleted",
            "R": "renamed",  # Treat as modified
            "C": "copied",   # Treat as added
        }
        
        # Handle complex status codes (e.g., "R100")
        first_char = status_code[0]
        drift_type = mapping.get(first_char)
        
        # Map renamed/copied to simpler types
        if drift_type == "renamed":
            return "modified"
        elif drift_type == "copied":
            return "added"
        
        return drift_type
    
    def _get_file_diff(self, filepath: str) -> str:
        """Get git diff for a specific file."""
        result = subprocess.run(
            ["git", "diff", "HEAD", "--", filepath],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            return f"Error getting diff: {result.stderr}"
        
        return result.stdout.strip()
    
    def generate_report(self, drift_list: List[Dict], files_scanned: int) -> Path:
        """
        Generate drift report YAML file.
        
        Args:
            drift_list: List of drift entries
            files_scanned: Total number of files scanned
        
        Returns:
            Path to generated report file
        """
        # Create drift directory if it doesn't exist
        self.drift_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate timestamp-based filename
        timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
        report_filename = f"{timestamp}-drift.yaml"
        report_path = self.drift_dir / report_filename
        
        # Build report structure
        report_data = {
            "metadata": {
                "detected_at": datetime.utcnow().isoformat() + "Z",
                "observer_version": self.VERSION,
                "files_scanned": files_scanned,
                "files_with_drift": len(drift_list)
            },
            "drift": drift_list
        }
        
        # Write YAML report (using manual formatting for cleaner output)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("metadata:\n")
            f.write(f'  detected_at: "{report_data["metadata"]["detected_at"]}"\n')
            f.write(f'  observer_version: "{report_data["metadata"]["observer_version"]}"\n')
            f.write(f'  files_scanned: {report_data["metadata"]["files_scanned"]}\n')
            f.write(f'  files_with_drift: {report_data["metadata"]["files_with_drift"]}\n')
            f.write("\n")
            f.write("drift:\n")
            
            for entry in drift_list:
                f.write(f'  - path: "{entry["path"]}"\n')
                f.write(f'    type: "{entry["type"]}"\n')
                
                if entry["diff"] is not None:
                    # Write diff with proper YAML multiline string formatting
                    f.write('    diff: |\n')
                    for line in entry["diff"].split("\n"):
                        f.write(f'      {line}\n')
                else:
                    f.write('    diff: null\n')
                
                f.write("\n")
        
        self.log(f"Report generated: {report_path}", force=True)
        return report_path
    
    def run(self) -> int:
        """
        Run observer drift detection.
        
        Returns:
            Exit code (0=clean, 1=drift, 2=error)
        """
        try:
            # Check git availability
            if not self.check_git_available():
                raise GitNotFoundError("Git repository not found or git not installed")
            
            self.log(f"Repository root: {self.repo_root}", force=True)
            
            # Detect drift
            drift_list, files_scanned = self.detect_drift()
            
            # Generate report if drift detected
            if drift_list:
                report_path = self.generate_report(drift_list, files_scanned)
                print(f"\n[!] Drift detected ({len(drift_list)} files)")
                print(f"Report: {report_path}")
                return 1
            else:
                print(f"\n[OK] No drift detected ({files_scanned} files scanned)")
                return 0
        
        except ObserverError as e:
            print(f"\n[ERROR] Observer error: {e}", file=sys.stderr)
            return 2
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}", file=sys.stderr)
            if self.verbose:
                import traceback
                traceback.print_exc()
            return 2


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Observer - Drift detection for truth-layer YAML files"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Detect repo root (assume script is in tools/ subdirectory)
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    
    # Run observer
    observer = Observer(repo_root, verbose=args.verbose)
    exit_code = observer.run()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
