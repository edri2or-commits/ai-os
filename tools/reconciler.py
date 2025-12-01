#!/usr/bin/env python3
"""
Reconciler - Change Request (CR) Management System
Phase 2, Slice 2.4b - CR lifecycle management (no apply logic yet)

Handles:
- Reading drift reports from Observer
- Generating Change Request (CR) files
- Listing CRs by status
- Approving/Rejecting CRs (updates CR file only, no entity modifications)

NOT in this slice:
- Applying CRs to entities (deferred to Slice 2.4c)
- Git commits from reconciler
- Entity file modifications
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Paths (relative to repo root)
REPO_ROOT = Path(__file__).parent.parent
DRIFT_REPORTS_DIR = REPO_ROOT / "docs" / "system_state" / "drift"
CHANGE_REQUESTS_DIR = REPO_ROOT / "docs" / "system_state" / "change_requests"
CR_SCHEMA_PATH = REPO_ROOT / "docs" / "schemas" / "change_request.schema.json"


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class DriftFinding:
    """Parsed drift finding from Observer report"""
    drift_type: str  # git_head_drift, stale_timestamp, etc.
    affected_entity: Dict[str, Any]  # {type, id, path}
    current_value: Any
    proposed_value: Any
    rationale: str = ""


@dataclass
class ChangeRequest:
    """Change Request (CR) wrapper"""
    cr_id: str
    timestamp: str
    generator: str
    status: str
    drift_type: str
    affected_entity: Dict[str, Any]
    proposed_changes: Dict[str, Any]
    rationale: str
    risk_level: str
    requires_approval: bool
    reversible: bool
    created_by: str
    drift_report_id: Optional[str] = None
    backup_path: Optional[str] = None
    reviewed_by: Optional[str] = None
    applied_at: Optional[str] = None
    git_commit: Optional[str] = None
    rejection_reason: Optional[str] = None

    @staticmethod
    def load(cr_path: Path) -> "ChangeRequest":
        """Load CR from YAML file"""
        with open(cr_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return ChangeRequest(**data)

    def save(self, cr_path: Path):
        """Save CR to YAML file"""
        # Convert to dict, remove None values for cleaner YAML
        data = {k: v for k, v in asdict(self).items() if v is not None}
        
        with open(cr_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def validate_schema(self) -> bool:
        """Validate CR against JSON Schema"""
        try:
            import jsonschema
            with open(CR_SCHEMA_PATH, "r", encoding="utf-8") as f:
                schema = json.load(f)
            
            cr_dict = asdict(self)
            jsonschema.validate(cr_dict, schema)
            return True
        except jsonschema.ValidationError as e:
            print(f"❌ Schema validation failed: {e.message}")
            return False
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False


# ============================================================================
# Reconciler Logic
# ============================================================================

class Reconciler:
    """Main reconciler logic - CR management only (no apply)"""

    def __init__(self):
        self.cr_dir = CHANGE_REQUESTS_DIR
        self.cr_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------------
    # Drift Report Parsing
    # ------------------------------------------------------------------------

    def parse_drift_report(self, report_path: Path) -> List[DriftFinding]:
        """
        Parse Markdown drift report and extract findings.
        
        Expected format:
        # Drift Report
        
        ## Git HEAD Drift
        - Last commit: 43b308a
        - Actual HEAD: eefc5d3
        
        ## Stale Timestamps
        - task-20251128-001: updated_at = 2025-11-28T14:00:00Z (3 days old)
        """
        findings = []
        
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Parse Git HEAD Drift
        git_drift = self._parse_git_head_drift(content)
        if git_drift:
            findings.append(git_drift)
        
        # Parse Stale Timestamps
        stale_timestamps = self._parse_stale_timestamps(content)
        findings.extend(stale_timestamps)
        
        return findings

    def _parse_git_head_drift(self, content: str) -> Optional[DriftFinding]:
        """Parse Git HEAD Drift section"""
        # Pattern: ## Git HEAD Drift followed by lines with "Last commit" and "Actual HEAD"
        git_section = re.search(
            r"## Git HEAD Drift.*?(?=##|\Z)",
            content,
            re.DOTALL | re.IGNORECASE
        )
        
        if not git_section:
            return None
        
        section_text = git_section.group(0)
        
        # Extract commit hashes
        last_commit_match = re.search(r"Last commit.*?:\s*([a-f0-9]{7,40})", section_text, re.IGNORECASE)
        actual_head_match = re.search(r"Actual HEAD.*?:\s*([a-f0-9]{7,40})", section_text, re.IGNORECASE)
        
        if not (last_commit_match and actual_head_match):
            return None
        
        last_commit = last_commit_match.group(1)
        actual_head = actual_head_match.group(1)
        
        return DriftFinding(
            drift_type="git_head_drift",
            affected_entity={
                "type": "system",
                "id": "SYSTEM_STATE_COMPACT.json",
                "path": "docs/system_state/SYSTEM_STATE_COMPACT.json"
            },
            current_value=last_commit,
            proposed_value=actual_head,
            rationale=f"Observer detected git HEAD drift. SYSTEM_STATE_COMPACT.json shows last_commit: {last_commit}, but actual HEAD is {actual_head}."
        )

    def _parse_stale_timestamps(self, content: str) -> List[DriftFinding]:
        """Parse Stale Timestamps section"""
        findings = []
        
        # Pattern: ## Stale Timestamps followed by lines with entity IDs
        stale_section = re.search(
            r"## Stale Timestamps.*?(?=##|\Z)",
            content,
            re.DOTALL | re.IGNORECASE
        )
        
        if not stale_section:
            return findings
        
        section_text = stale_section.group(0)
        
        # Pattern: - task-20251128-001: updated_at = 2025-11-28T14:00:00Z (3 days old)
        # Or: - task-20251128-001: path/to/file.md: updated_at = 2025-11-28T14:00:00Z
        timestamp_pattern = re.compile(
            r"-\s+([a-z]+-\d{8}-\d{3})(?:\s*:\s*([^\s:]+))?.*?updated_at\s*=\s*([^\s]+)",
            re.IGNORECASE
        )
        
        for match in timestamp_pattern.finditer(section_text):
            entity_id = match.group(1)
            entity_path = match.group(2) if match.group(2) else f"memory-bank/10_Projects/unknown/{entity_id}.md"
            old_timestamp = match.group(3)
            
            # Determine entity type from ID
            entity_type = entity_id.split("-")[0]  # e.g., "task" from "task-20251128-001"
            
            findings.append(DriftFinding(
                drift_type="stale_timestamp",
                affected_entity={
                    "type": entity_type,
                    "id": entity_id,
                    "path": entity_path
                },
                current_value=old_timestamp,
                proposed_value=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                rationale=f"Entity timestamp is stale (old value: {old_timestamp}). Proposing update to current time."
            ))
        
        return findings

    # ------------------------------------------------------------------------
    # CR Generation
    # ------------------------------------------------------------------------

    def generate_cr_from_drift(self, finding: DriftFinding, report_id: Optional[str] = None) -> ChangeRequest:
        """Generate a Change Request from a drift finding"""
        cr_id = self._generate_cr_id()
        now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Build proposed_changes based on drift type
        if finding.drift_type == "git_head_drift":
            field = "last_commit"
            operation = "update"
        elif finding.drift_type == "stale_timestamp":
            field = "updated_at"
            operation = "update"
        else:
            # Generic fallback
            field = "unknown"
            operation = "update"
        
        cr = ChangeRequest(
            cr_id=cr_id,
            timestamp=now,
            generator="reconciler.py",
            status="proposed",
            drift_type=finding.drift_type,
            drift_report_id=report_id,
            affected_entity=finding.affected_entity,
            proposed_changes={
                "field": field,
                "current_value": finding.current_value,
                "proposed_value": finding.proposed_value,
                "operation": operation
            },
            rationale=finding.rationale,
            risk_level="low",  # Only LOW risk in Slice 2.4b
            requires_approval=True,
            reversible=True,
            created_by="reconciler.py",
            backup_path=None
        )
        
        return cr

    def _generate_cr_id(self) -> str:
        """Generate unique CR ID: CR-YYYYMMDD-NNN"""
        today = datetime.utcnow().strftime("%Y%m%d")
        
        # Find existing CRs for today
        existing_crs = list(self.cr_dir.glob(f"CR-{today}-*.cr.yaml"))
        
        # Extract sequence numbers
        seq_numbers = []
        for cr_file in existing_crs:
            match = re.search(r"CR-\d{8}-(\d{3})", cr_file.name)
            if match:
                seq_numbers.append(int(match.group(1)))
        
        # Next sequence number
        next_seq = max(seq_numbers, default=0) + 1
        
        return f"CR-{today}-{next_seq:03d}"

    # ------------------------------------------------------------------------
    # CR Listing & Display
    # ------------------------------------------------------------------------

    def list_crs(self, status: Optional[str] = None) -> List[ChangeRequest]:
        """List CRs, optionally filtered by status"""
        crs = []
        
        for cr_file in sorted(self.cr_dir.glob("*.cr.yaml")):
            try:
                cr = ChangeRequest.load(cr_file)
                if status is None or cr.status == status:
                    crs.append(cr)
            except Exception as e:
                print(f"⚠️  Warning: Could not load {cr_file.name}: {e}")
        
        return crs

    def show_cr(self, cr_id: str) -> Optional[ChangeRequest]:
        """Load and return a specific CR"""
        cr_path = self.cr_dir / f"{cr_id}.cr.yaml"
        
        if not cr_path.exists():
            print(f"❌ CR not found: {cr_id}")
            return None
        
        try:
            return ChangeRequest.load(cr_path)
        except Exception as e:
            print(f"❌ Error loading CR: {e}")
            return None

    # ------------------------------------------------------------------------
    # CR Approval / Rejection (File updates only, no entity changes)
    # ------------------------------------------------------------------------

    def approve_cr(self, cr_id: str, reviewed_by: str = "user") -> bool:
        """
        Approve a CR by updating its status.
        NOTE: This only updates the CR file, does NOT apply changes to entities.
        """
        cr_path = self.cr_dir / f"{cr_id}.cr.yaml"
        
        if not cr_path.exists():
            print(f"❌ CR not found: {cr_id}")
            return False
        
        try:
            cr = ChangeRequest.load(cr_path)
            
            if cr.status != "proposed":
                print(f"⚠️  CR {cr_id} is not in 'proposed' state (current: {cr.status})")
                return False
            
            # Update status
            cr.status = "approved"
            cr.reviewed_by = reviewed_by
            
            # Validate and save
            if not cr.validate_schema():
                print(f"❌ CR validation failed after approval")
                return False
            
            cr.save(cr_path)
            print(f"✅ Approved {cr_id}")
            print(f"   Status: proposed → approved")
            print(f"   Reviewed by: {reviewed_by}")
            return True
            
        except Exception as e:
            print(f"❌ Error approving CR: {e}")
            return False

    def reject_cr(self, cr_id: str, reason: str, reviewed_by: str = "user") -> bool:
        """
        Reject a CR by updating its status and recording the reason.
        NOTE: This only updates the CR file, does NOT apply changes to entities.
        """
        cr_path = self.cr_dir / f"{cr_id}.cr.yaml"
        
        if not cr_path.exists():
            print(f"❌ CR not found: {cr_id}")
            return False
        
        try:
            cr = ChangeRequest.load(cr_path)
            
            if cr.status != "proposed":
                print(f"⚠️  CR {cr_id} is not in 'proposed' state (current: {cr.status})")
                return False
            
            # Update status
            cr.status = "rejected"
            cr.reviewed_by = reviewed_by
            cr.rejection_reason = reason
            
            # Validate and save
            if not cr.validate_schema():
                print(f"❌ CR validation failed after rejection")
                return False
            
            cr.save(cr_path)
            print(f"❌ Rejected {cr_id}")
            print(f"   Reason: {reason}")
            return True
            
        except Exception as e:
            print(f"❌ Error rejecting CR: {e}")
            return False


# ============================================================================
# CLI Commands
# ============================================================================

def cmd_generate(args):
    """Generate CRs from drift report"""
    reconciler = Reconciler()
    
    # Determine report path
    if args.report:
        report_path = Path(args.report)
    else:
        # Find latest drift report
        reports = sorted(DRIFT_REPORTS_DIR.glob("*.md"))
        if not reports:
            print("❌ No drift reports found in", DRIFT_REPORTS_DIR)
            print("   Create a sample report or run Observer first")
            return
        report_path = reports[-1]
    
    if not report_path.exists():
        print(f"❌ Report not found: {report_path}")
        return
    
    print(f"📄 Reading drift report: {report_path.name}")
    
    # Parse drift report
    try:
        findings = reconciler.parse_drift_report(report_path)
    except Exception as e:
        print(f"❌ Error parsing drift report: {e}")
        return
    
    if not findings:
        print("ℹ️  No drift findings in report")
        return
    
    print(f"   Found {len(findings)} drift finding(s)")
    
    # Generate CRs
    generated = []
    for finding in findings:
        try:
            cr = reconciler.generate_cr_from_drift(finding)
            
            # Validate
            if not cr.validate_schema():
                print(f"⚠️  Skipping invalid CR for {finding.drift_type}")
                continue
            
            # Save
            cr_path = CHANGE_REQUESTS_DIR / f"{cr.cr_id}.cr.yaml"
            cr.save(cr_path)
            generated.append(cr.cr_id)
            print(f"✅ Generated {cr.cr_id} ({finding.drift_type})")
            
        except Exception as e:
            print(f"❌ Error generating CR for {finding.drift_type}: {e}")
    
    print(f"\n📋 Generated {len(generated)} CR(s)")


def cmd_list(args):
    """List CRs"""
    reconciler = Reconciler()
    crs = reconciler.list_crs(status=args.status)
    
    if not crs:
        status_msg = f"with status='{args.status}'" if args.status else ""
        print(f"ℹ️  No CRs found {status_msg}")
        return
    
    # Print table header
    print(f"\n{'CR ID':<20} | {'Drift Type':<20} | {'Risk':<6} | {'Status':<10}")
    print("-" * 70)
    
    # Print CRs
    for cr in crs:
        print(f"{cr.cr_id:<20} | {cr.drift_type:<20} | {cr.risk_level:<6} | {cr.status:<10}")
    
    print(f"\nTotal: {len(crs)} CR(s)")


def cmd_show(args):
    """Show specific CR"""
    reconciler = Reconciler()
    cr = reconciler.show_cr(args.cr_id)
    
    if not cr:
        return
    
    # Pretty-print CR as YAML
    print(f"\n{'='*70}")
    print(f"CR: {cr.cr_id}")
    print(f"{'='*70}\n")
    
    print(yaml.dump(asdict(cr), default_flow_style=False, sort_keys=False))


def cmd_approve(args):
    """Approve a CR"""
    reconciler = Reconciler()
    reconciler.approve_cr(args.cr_id, reviewed_by=args.reviewed_by)


def cmd_reject(args):
    """Reject a CR"""
    reconciler = Reconciler()
    if not args.reason:
        print("❌ Rejection reason required (use --reason)")
        return
    reconciler.reject_cr(args.cr_id, reason=args.reason, reviewed_by=args.reviewed_by)


# ============================================================================
# Main CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Reconciler - Change Request (CR) Management System (Slice 2.4b)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate CRs from latest drift report
  python tools/reconciler.py generate

  # Generate from specific report
  python tools/reconciler.py generate --report drift-20251201.md

  # List all CRs
  python tools/reconciler.py list

  # List by status
  python tools/reconciler.py list --status proposed
  python tools/reconciler.py list --status approved

  # Show specific CR
  python tools/reconciler.py show CR-20251201-001

  # Approve CR
  python tools/reconciler.py approve CR-20251201-001

  # Reject CR
  python tools/reconciler.py reject CR-20251201-001 --reason "Not needed"
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Generate command
    parser_gen = subparsers.add_parser("generate", help="Generate CRs from drift report")
    parser_gen.add_argument("--report", help="Path to drift report (default: latest in drift/)")
    
    # List command
    parser_list = subparsers.add_parser("list", help="List CRs")
    parser_list.add_argument("--status", choices=["proposed", "approved", "rejected", "applied"],
                             help="Filter by status")
    
    # Show command
    parser_show = subparsers.add_parser("show", help="Show specific CR")
    parser_show.add_argument("cr_id", help="CR ID (e.g., CR-20251201-001)")
    
    # Approve command
    parser_approve = subparsers.add_parser("approve", help="Approve a CR")
    parser_approve.add_argument("cr_id", help="CR ID to approve")
    parser_approve.add_argument("--reviewed-by", default="user", help="Reviewer name")
    
    # Reject command
    parser_reject = subparsers.add_parser("reject", help="Reject a CR")
    parser_reject.add_argument("cr_id", help="CR ID to reject")
    parser_reject.add_argument("--reason", required=True, help="Reason for rejection")
    parser_reject.add_argument("--reviewed-by", default="user", help="Reviewer name")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Dispatch to command handler
    {
        "generate": cmd_generate,
        "list": cmd_list,
        "show": cmd_show,
        "approve": cmd_approve,
        "reject": cmd_reject
    }[args.command](args)


if __name__ == "__main__":
    main()
