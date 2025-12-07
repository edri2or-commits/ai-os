#!/usr/bin/env python3
"""
ADHD State Monitor - State Freshness & Hyperfocus Detection

Checks ADHD state file for:
1. Staleness (>24h without update)
2. Hyperfocus risk (>90 min since last break)

Called by Observer every 15 minutes.
"""

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Optional


class ADHDStateMonitor:
    """Monitor ADHD state for freshness and time-based signals."""
    
    VERSION = "1.0.0"
    STATE_FILE = "memory-bank/20_Areas/adhd-support/adhd_state.json"
    HISTORY_FILE = "memory-bank/20_Areas/adhd-support/state_history.jsonl"
    
    # Thresholds
    STALE_THRESHOLD_HOURS = 24
    HYPERFOCUS_THRESHOLD_MINUTES = 90
    
    def __init__(self, repo_root: Path, verbose: bool = False):
        """
        Initialize ADHD State Monitor.
        
        Args:
            repo_root: Path to repository root
            verbose: Enable verbose logging
        """
        self.repo_root = repo_root
        self.state_path = repo_root / self.STATE_FILE
        self.history_path = repo_root / self.HISTORY_FILE
        self.verbose = verbose
    
    def log(self, message: str, force: bool = False):
        """Log message if verbose enabled."""
        if self.verbose or force:
            print(f"[ADHD Monitor] {message}")
    
    def check_state(self) -> Dict:
        """
        Check ADHD state freshness and auto-update time-based signals.
        
        Returns:
            Dict with status, age_hours, minutes_since_break, issues
        """
        if not self.state_path.exists():
            self.log("State file not found - ADHD system not initialized", force=True)
            return {"status": "no_state", "initialized": False}
        
        try:
            # Read current state
            with open(self.state_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            now = datetime.now(timezone.utc)
            issues = []
            
            # Check 1: State staleness
            last_update_str = state["current_state"]["timestamp"]
            last_update = datetime.fromisoformat(last_update_str.replace('Z', '+00:00'))
            age_hours = (now - last_update).total_seconds() / 3600
            
            if age_hours > self.STALE_THRESHOLD_HOURS:
                issues.append({
                    "type": "STATE_STALE",
                    "severity": "warning",
                    "message": f"State not updated for {age_hours:.1f} hours (threshold: {self.STALE_THRESHOLD_HOURS}h)"
                })
                self.log(f"⚠️ Stale state detected: {age_hours:.1f}h old", force=True)
            
            # Check 2: Hyperfocus risk (time since last break)
            last_break_str = state["current_state"]["last_break_timestamp"]
            last_break = datetime.fromisoformat(last_break_str.replace('Z', '+00:00'))
            minutes_since_break = (now - last_break).total_seconds() / 60
            
            # Update hyperfocus_risk flag if needed
            if minutes_since_break > self.HYPERFOCUS_THRESHOLD_MINUTES:
                if not state["task_context"]["hyperfocus_risk"]:
                    # Set risk flag
                    state["task_context"]["hyperfocus_risk"] = True
                    state["meta"]["last_updated"] = now.isoformat()
                    
                    # Write back
                    with open(self.state_path, 'w', encoding='utf-8') as f:
                        json.dump(state, f, indent=2, ensure_ascii=False)
                    
                    issues.append({
                        "type": "HYPERFOCUS_RISK_DETECTED",
                        "severity": "alert",
                        "message": f"User working {minutes_since_break:.0f} minutes without break (threshold: {self.HYPERFOCUS_THRESHOLD_MINUTES}min)"
                    })
                    self.log(f"🔴 Hyperfocus risk: {minutes_since_break:.0f} min without break", force=True)
                
                    # Log to history
                    self._append_history_event("HYPERFOCUS_RISK", {
                        "minutes_since_break": minutes_since_break,
                        "current_focus": state["task_context"]["current_focus"]
                    })
            else:
                # Clear risk flag if under threshold
                if state["task_context"]["hyperfocus_risk"]:
                    state["task_context"]["hyperfocus_risk"] = False
                    state["meta"]["last_updated"] = now.isoformat()
                    
                    with open(self.state_path, 'w', encoding='utf-8') as f:
                        json.dump(state, f, indent=2, ensure_ascii=False)
                    
                    self.log(f"✅ Hyperfocus risk cleared (break detected)", force=True)
            
            # Build result
            result = {
                "status": "ok",
                "initialized": True,
                "age_hours": round(age_hours, 1),
                "minutes_since_break": round(minutes_since_break, 0),
                "current_mode": state["system_mode"]["current_mode"],
                "energy_spoons": state["current_state"]["energy_spoons"],
                "issues": issues
            }
            
            if not issues:
                self.log("✅ State healthy", force=False)
            
            return result
        
        except Exception as e:
            self.log(f"❌ Error checking state: {e}", force=True)
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _append_history_event(self, event_type: str, payload: Dict):
        """
        Append event to state_history.jsonl.
        
        Args:
            event_type: Type of event (e.g., "HYPERFOCUS_RISK")
            payload: Event data
        """
        try:
            event = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event_type": event_type,
                "payload": payload
            }
            
            # Ensure directory exists
            self.history_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Append to JSONL
            with open(self.history_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')
            
            self.log(f"Logged event: {event_type}")
        
        except Exception as e:
            self.log(f"Failed to log history event: {e}", force=True)


def main():
    """CLI entry point for standalone testing."""
    import sys
    
    # Detect repo root (assume script is in tools/)
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    
    print(f"ADHD State Monitor v{ADHDStateMonitor.VERSION}")
    print(f"Repo: {repo_root}\n")
    
    monitor = ADHDStateMonitor(repo_root, verbose=True)
    result = monitor.check_state()
    
    print("\n" + "="*50)
    print("RESULT:")
    print(json.dumps(result, indent=2))
    print("="*50)
    
    # Exit code: 0 if ok, 1 if issues detected
    if result.get("issues"):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
