#!/usr/bin/env python3
"""
Observer System - Drift Detection for Truth Layer

Detects uncommitted changes in truth-layer/*.yaml files by comparing
working tree state to last git commit (HEAD).

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
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class Observer:
    """Drift detection system for Truth Layer YAML files."""
    
    VERSION = "0.1.0"
    TRUTH_LAYER_PATH = "truth-layer"
    DRIFT_REPORTS_PATH = "truth-layer/drift"
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.repo_root = self._find_repo_root()
        if not self.repo_root:
            raise RuntimeError("Not in a git repository")
    
    def _find_repo_root(self) -> Optional[Path]:
        """Find git repository root directory."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True
            )
            return Path(result.stdout.strip())
        except subprocess.CalledProcessError:
            return None
    
    def _log(self, message: str):
        """Log message if verbose mode enabled."""
        if self.verbose:
            print(f"[Observer] {message}")
    
    def _run_git_command(self, args: List[str]) -> Tuple[str, str, int]:
        """Run git command and return (stdout, stderr, returncode)."""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1
    
    def detect_drift(self) -> Dict:
        """
        Detect drift in truth-layer YAML files.
        
        Returns:
            Dict with metadata and drift findings.
        """
        self._log("Starting drift detection...")
        
        # Get changed files in truth-layer/
        self._log("Running git diff to detect changes...")
        stdout, stderr, returncode = self._run_git_command([
            "diff", "HEAD", "--name-status", "--", "truth-layer/*.yaml"
        ])
        
        if returncode != 0:
            raise RuntimeError(f"Git diff failed: {stderr}")
        
        # Parse git diff output
        drift_findings = []
        lines = stdout.strip().split("\n") if stdout.strip() else []
        
        self._log(f"Found {len(lines)} changed files")
        
        for line in lines:
            if not line.strip():
                continue
            
            parts = line.split("\t", 1)
            if len(parts) != 2:
                continue
            
            status, filepath = parts[0], parts[1]
            
            # Map git status codes
            change_type = self._map_status_code(status)
            
            self._log(f"Processing {filepath} (type: {change_type})")
            
            # Get diff for modified files
            diff_content = None
            if change_type == "modified":
                diff_content = self._get_file_diff(filepath)
            
            drift_findings.append({
                "path": filepath,
                "type": change_type,
                "diff": diff_content
            })
        
        # Build report metadata
        metadata = {
            "detected_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "observer_version": self.VERSION,
            "files_scanned": self._count_yaml_files(),
            "files_with_drift": len(drift_findings)
        }
        
        return {
            "metadata": metadata,
            "drift": drift_findings
        }
    
    def _map_status_code(self, status: str) -> str:
        """Map git status code to drift type."""
        if status.startswith("M"):
            return "modified"
        elif status.startswith("A"):
            return "added"
        elif status.startswith("D"):
            return "deleted"
        elif status.startswith("R"):
            return "renamed"
        else:
            return "unknown"
    
    def _get_file_diff(self, filepath: str) -> Optional[str]:
        """Get diff content for a file."""
        stdout, stderr, returncode = self._run_git_command([
            "diff", "HEAD", "--", filepath
        ])
        
        if returncode != 0:
            self._log(f"Warning: Could not get diff for {filepath}")
            return None
        
        return stdout if stdout.strip() else None
    
    def _count_yaml_files(self) -> int:
        """Count total YAML files in truth-layer."""
        truth_layer_dir = self.repo_root / self.TRUTH_LAYER_PATH
        
        if not truth_layer_dir.exists():
            return 0
        
        # Count .yaml and .yml files
        yaml_files = list(truth_layer_dir.rglob("*.yaml")) + list(truth_layer_dir.rglob("*.yml"))
        return len(yaml_files)
    
    def generate_report(self, drift_data: Dict) -> Path:
        """
        Generate drift report YAML file.
        
        Args:
            drift_data: Drift detection results
            
        Returns:
            Path to generated report file
        """
        # Create drift reports directory
        drift_dir = self.repo_root / self.DRIFT_REPORTS_PATH
        drift_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate timestamp-based filename
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        report_path = drift_dir / f"{timestamp}-drift.yaml"
        
        self._log(f"Generating report: {report_path}")
        
        # Convert to YAML format (manual, simple format)
        yaml_content = self._dict_to_yaml(drift_data)
        
        # Write report
        report_path.write_text(yaml_content, encoding="utf-8")
        
        return report_path
    
    def _dict_to_yaml(self, data: Dict, indent: int = 0) -> str:
        """Convert dict to YAML format (simple implementation)."""
        lines = []
        prefix = "  " * indent
        
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(self._dict_to_yaml(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        lines.append(f"{prefix}  -")
                        for k, v in item.items():
                            if k == "diff" and v:
                                lines.append(f"{prefix}    {k}: |")
                                for diff_line in v.split("\n"):
                                    lines.append(f"{prefix}      {diff_line}")
                            elif v is None:
                                lines.append(f"{prefix}    {k}: null")
                            else:
                                lines.append(f"{prefix}    {k}: \"{v}\"")
                    else:
                        lines.append(f"{prefix}  - {item}")
            elif value is None:
                lines.append(f"{prefix}{key}: null")
            elif isinstance(value, str):
                lines.append(f"{prefix}{key}: \"{value}\"")
            else:
                lines.append(f"{prefix}{key}: {value}")
        
        return "\n".join(lines)



def main():
    """Main entry point for Observer CLI."""
    parser = argparse.ArgumentParser(
        description="Observer System - Drift Detection for Truth Layer"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize observer
        observer = Observer(verbose=args.verbose)
        
        # Detect drift
        drift_data = observer.detect_drift()
        
        # Check if drift detected
        drift_count = drift_data["metadata"]["files_with_drift"]
        
        if drift_count == 0:
            print("[OK] No drift detected. Truth layer is clean.")
            return 0
        
        # Generate report
        report_path = observer.generate_report(drift_data)
        
        # Display results
        print(f"[DRIFT] Drift detected in {drift_count} file(s).")
        print(f"[REPORT] Report generated: {report_path}")
        print()
        print("Files with drift:")
        for finding in drift_data["drift"]:
            print(f"  - {finding['path']} ({finding['type']})")
        
        return 1
        
    except RuntimeError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())
