#!/usr/bin/env python3
"""
Bootstrap Response Validator - Validates chat bootstrap handshakes

Checks if a chat session's first reply follows CHAT_BOOTSTRAP_PROTOCOL_V1.

Usage:
    python scripts/validate_bootstrap_response.py --response-file response.txt
    python scripts/validate_bootstrap_response.py --response-file response.txt --format json
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple


# Paths
REPO_ROOT = Path(__file__).parent.parent
COMPACT_PATH = REPO_ROOT / "docs" / "system_state" / "SYSTEM_STATE_COMPACT.json"
GOVERNANCE_PATH = REPO_ROOT / "governance" / "snapshots" / "GOVERNANCE_LATEST.json"
TIMELINE_PATH = REPO_ROOT / "docs" / "system_state" / "timeline" / "EVENT_TIMELINE.jsonl"

# Disallowed capability keywords (auto-fail if found)
DISALLOWED_CAPABILITIES = [
    "send email", "gmail send", "create email",
    "create calendar", "calendar event", "google calendar",
    "create task", "google tasks",
    "live automation", "real-world service", "production service"
]


class ValidationCheck:
    """Represents a single validation check"""
    def __init__(self, check_id: str, description: str):
        self.id = check_id
        self.description = description
        self.passed = False
        self.message = ""
    
    def pass_check(self, message: str = ""):
        self.passed = True
        self.message = message or f"{self.description}: OK"
    
    def fail_check(self, message: str):
        self.passed = False
        self.message = message
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "passed": self.passed,
            "message": self.message
        }


class BootstrapValidator:
    """Validates bootstrap handshake responses"""
    
    def __init__(self):
        self.checks: List[ValidationCheck] = []
        self.phase = None
        self.mode = None
        self.compact_version = None
    
    def load_truth_sources(self) -> bool:
        """Load COMPACT and GOVERNANCE to get current phase/mode"""
        try:
            # Load COMPACT
            with open(COMPACT_PATH, 'r', encoding='utf-8') as f:
                compact = json.load(f)
                self.phase = compact["system"]["phase"]
                self.mode = compact["system"]["mode"]
                self.compact_version = compact.get("_version", "unknown")
            
            # Load GOVERNANCE (for cross-verification)
            with open(GOVERNANCE_PATH, 'r', encoding='utf-8') as f:
                governance = json.load(f)
                gov_phase = governance["system_state"]["phase"]
                gov_mode = governance["system_state"]["mode"]
                
                # Verify consistency
                if gov_phase != self.phase or gov_mode != self.mode:
                    print(f"[WARNING] Phase/mode mismatch between COMPACT and GOVERNANCE", file=sys.stderr)
            
            return True
        
        except Exception as e:
            print(f"[ERROR] Failed to load truth sources: {e}", file=sys.stderr)
            return False
    
    def validate_response(self, response_text: str) -> bool:
        """
        Run all validation checks on the response
        
        Returns:
            True if all checks pass, False otherwise
        """
        lines = response_text.strip().split('\n')
        response_lower = response_text.lower()
        
        # C1: ACK_CONTEXT_LOADED on first line
        c1 = ValidationCheck("C1", "ACK_CONTEXT_LOADED present as first non-empty line")
        first_nonempty = next((line.strip() for line in lines if line.strip()), "")
        if first_nonempty == "ACK_CONTEXT_LOADED":
            c1.pass_check("ACK_CONTEXT_LOADED found as first line")
        else:
            c1.fail_check(f"Expected 'ACK_CONTEXT_LOADED' as first line, got: '{first_nonempty[:50]}'")
        self.checks.append(c1)
        
        # C2: SUMMARY section exists
        c2 = ValidationCheck("C2", "SUMMARY section present")
        if re.search(r'SUMMARY\s*:', response_text, re.IGNORECASE):
            c2.pass_check("SUMMARY section found")
        else:
            c2.fail_check("SUMMARY section not found")
        self.checks.append(c2)
        
        # C3: Phase and Mode match
        c3 = ValidationCheck("C3", "Phase and Mode match current state")
        issues = []
        
        # Check phase
        if self.phase not in response_text:
            issues.append(f"Phase mismatch: expected '{self.phase}' not found in response")
        
        # Check mode
        if self.mode not in response_text:
            issues.append(f"Mode mismatch: expected '{self.mode}' not found in response")
        
        # Check role (should be some variant of OPERATOR or ASSISTANT)
        if not re.search(r'role.*operator|role.*assistant', response_lower):
            issues.append("Role not clearly specified (expected AI_OS_OPERATOR_ASSISTANT or similar)")
        
        if issues:
            c3.fail_check("; ".join(issues))
        else:
            c3.pass_check(f"Phase '{self.phase}', Mode '{self.mode}' found")
        self.checks.append(c3)
        
        # C4: CAPABILITIES section valid
        c4 = ValidationCheck("C4", "CAPABILITIES section lists only allowed operations")
        if not re.search(r'CAPABILITIES\s*:', response_text, re.IGNORECASE):
            c4.fail_check("CAPABILITIES section not found")
        else:
            # Check for disallowed capabilities
            disallowed_found = []
            for disallowed in DISALLOWED_CAPABILITIES:
                if disallowed.lower() in response_lower:
                    disallowed_found.append(disallowed)
            
            if disallowed_found:
                c4.fail_check(f"Claims disallowed capabilities: {', '.join(disallowed_found)}")
            else:
                # Check that PR_CONTRACT_V1 is mentioned
                if "pr_contract" in response_lower or "pr intent" in response_lower:
                    c4.pass_check("Only allowed capabilities listed (PR_CONTRACT_V1)")
                else:
                    c4.fail_check("CAPABILITIES section found but PR_CONTRACT_V1 not clearly mentioned")
        self.checks.append(c4)
        
        # C5: HARD CONSTRAINTS section
        c5 = ValidationCheck("C5", "HARD CONSTRAINTS include INFRA_ONLY and Truth Protocol")
        if not re.search(r'HARD\s+CONSTRAINTS?\s*:', response_text, re.IGNORECASE):
            c5.fail_check("HARD CONSTRAINTS section not found")
        else:
            issues = []
            
            # Check for INFRA_ONLY
            if "infra_only" not in response_lower and "infra only" not in response_lower:
                issues.append("INFRA_ONLY not mentioned")
            
            # Check for Truth Protocol
            if "truth protocol" not in response_lower and "repo files" not in response_lower:
                issues.append("Truth Protocol / file-based state not mentioned")
            
            if issues:
                c5.fail_check("; ".join(issues))
            else:
                c5.pass_check("INFRA_ONLY and Truth Protocol both mentioned")
        self.checks.append(c5)
        
        # C6: READY FOR INSTRUCTIONS
        c6 = ValidationCheck("C6", "Ends with READY FOR INSTRUCTIONS")
        last_nonempty = next((line.strip() for line in reversed(lines) if line.strip()), "")
        if "READY FOR INSTRUCTIONS" in last_nonempty.upper():
            c6.pass_check("READY FOR INSTRUCTIONS found at end")
        else:
            c6.fail_check(f"Expected 'READY FOR INSTRUCTIONS' at end, got: '{last_nonempty[:50]}'")
        self.checks.append(c6)
        
        # Return overall result
        return all(check.passed for check in self.checks)
    
    def get_failed_checks(self) -> List[ValidationCheck]:
        """Get list of failed checks"""
        return [check for check in self.checks if not check.passed]
    
    def print_text_report(self):
        """Print human-readable validation report"""
        all_passed = all(check.passed for check in self.checks)
        
        if all_passed:
            print("VALIDATION RESULT: ✅ VALID\n")
        else:
            print("VALIDATION RESULT: ❌ INVALID\n")
        
        # Print individual checks
        for check in self.checks:
            status = "[x]" if check.passed else "[ ]"
            print(f"  {status} {check.id}: {check.description}")
            if not check.passed:
                print(f"      ⮕ {check.message}")
        
        print()
        
        # Summary
        failed = self.get_failed_checks()
        if failed:
            print(f"Overall: INVALID due to failing checks: {', '.join(c.id for c in failed)}")
        else:
            print("Overall: VALID - all checks passed")
    
    def get_json_report(self) -> Dict[str, Any]:
        """Get JSON validation report"""
        all_passed = all(check.passed for check in self.checks)
        
        return {
            "valid": all_passed,
            "checks": [check.to_dict() for check in self.checks],
            "phase_expected": self.phase,
            "mode_expected": self.mode,
            "compact_version": self.compact_version
        }
    
    def log_to_timeline(self, response_file: str, valid: bool):
        """Log validation run to EVENT_TIMELINE.jsonl"""
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": "CHAT_BOOTSTRAP_VALIDATION_RUN",
            "source": "bootstrap_validator_v1",
            "payload": {
                "response_file": str(response_file),
                "valid": valid,
                "failed_checks": [c.id for c in self.get_failed_checks()]
            }
        }
        
        try:
            with open(TIMELINE_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to log to timeline: {e}", file=sys.stderr)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Validate a chat bootstrap handshake response against CHAT_BOOTSTRAP_PROTOCOL_V1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate response (text output)
  python scripts/validate_bootstrap_response.py --response-file handshake.txt
  
  # Validate response (JSON output)
  python scripts/validate_bootstrap_response.py --response-file handshake.txt --format json
  
  # Validate and log to timeline
  python scripts/validate_bootstrap_response.py --response-file handshake.txt --log-timeline
        """
    )
    
    parser.add_argument(
        "--response-file",
        required=True,
        type=Path,
        help="Path to file containing the bootstrap handshake response"
    )
    
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--log-timeline",
        action="store_true",
        help="Log validation result to EVENT_TIMELINE.jsonl"
    )
    
    args = parser.parse_args()
    
    # Check response file exists
    if not args.response_file.exists():
        print(f"[ERROR] Response file not found: {args.response_file}", file=sys.stderr)
        sys.exit(1)
    
    # Create validator
    validator = BootstrapValidator()
    
    # Load truth sources
    if not validator.load_truth_sources():
        sys.exit(1)
    
    # Read response file
    try:
        with open(args.response_file, 'r', encoding='utf-8') as f:
            response_text = f.read()
    except Exception as e:
        print(f"[ERROR] Failed to read response file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Validate
    is_valid = validator.validate_response(response_text)
    
    # Output
    if args.format == "text":
        validator.print_text_report()
    else:  # json
        report = validator.get_json_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # Log to timeline if requested
    if args.log_timeline:
        validator.log_to_timeline(args.response_file, is_valid)
        print(f"\n[INFO] Logged validation result to {TIMELINE_PATH}", file=sys.stderr)
    
    # Exit code
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
