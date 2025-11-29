#!/usr/bin/env python3
"""
State Layer Reconciler V1
Generates SYSTEM_STATE_COMPACT.json from Truth Sources and detects/fixes drift.

Truth Sources (Priority Order):
1. governance/snapshots/GOVERNANCE_LATEST.json - system state, services, fitness
2. docs/DECISIONS_AI_OS.md - decisions status (authoritative)
3. docs/system_state/timeline/EVENT_TIMELINE.jsonl - events, recent work
4. docs/system_state/registries/SERVICES_STATUS.json - services list
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Tuple
import re


class StateReconciler:
    """Reconciles SYSTEM_STATE_COMPACT.json from Truth Sources"""
    
    def __init__(self, repo_root: str = None):
        """
        Initialize reconciler with repo root path.
        
        Args:
            repo_root: Path to ai-os repo root. If None, auto-detect from this file.
        """
        if repo_root is None:
            # Auto-detect: services/os_core_mcp/reconciler.py → repo root is 2 levels up
            current_file = Path(__file__).resolve()
            self.repo_root = current_file.parent.parent.parent
        else:
            self.repo_root = Path(repo_root)
        
        # Define paths to truth sources
        self.paths = {
            'governance': self.repo_root / 'governance' / 'snapshots' / 'GOVERNANCE_LATEST.json',
            'decisions': self.repo_root / 'docs' / 'DECISIONS_AI_OS.md',
            'timeline': self.repo_root / 'docs' / 'system_state' / 'timeline' / 'EVENT_TIMELINE.jsonl',
            'services': self.repo_root / 'docs' / 'system_state' / 'registries' / 'SERVICES_STATUS.json',
            'compact': self.repo_root / 'docs' / 'system_state' / 'SYSTEM_STATE_COMPACT.json'
        }
    
    def verify_truth_sources(self) -> Dict[str, bool]:
        """Check which truth sources exist"""
        return {
            name: path.exists()
            for name, path in self.paths.items()
        }
    
    def read_governance_snapshot(self) -> Dict[str, Any]:
        """Read GOVERNANCE_LATEST.json"""
        with open(self.paths['governance'], 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def read_services_registry(self) -> Dict[str, Any]:
        """Read SERVICES_STATUS.json"""
        with open(self.paths['services'], 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def read_event_timeline(self, last_n: int = 100) -> List[Dict[str, Any]]:
        """Read last N events from EVENT_TIMELINE.jsonl"""
        events = []
        with open(self.paths['timeline'], 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('{"_schema"'):  # Skip schema line
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        return events[-last_n:] if len(events) > last_n else events
    
    def parse_decisions(self) -> Tuple[List[Dict], List[Dict]]:
        """
        Parse DECISIONS_AI_OS.md to extract pending and recent decisions.
        
        Returns:
            (pending_decisions, recent_decisions)
        """
        with open(self.paths['decisions'], 'r', encoding='utf-8') as f:
            content = f.read()
        
        pending = []
        recent = []
        
        # Find the decisions table (starts after "| # | נושא | החלטה | סטטוס |")
        table_pattern = r'\|\s*#\s*\|\s*נושא\s*\|\s*החלטה\s*\|\s*סטטוס\s*\|(.*?)(?=\n##|\Z)'
        match = re.search(table_pattern, content, re.DOTALL)
        
        if match:
            table_content = match.group(1)
            
            # Parse each row
            for line in table_content.split('\n'):
                line = line.strip()
                if not line or line.startswith('|---') or not line.startswith('|'):
                    continue
                
                # Split by | and clean
                parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove empty first/last
                
                if len(parts) < 4:
                    continue
                
                dec_id = parts[0]
                title = parts[1]
                decision = parts[2]
                status = parts[3]
                
                # Extract DEC-XXX if it's in the ID column
                dec_match = re.search(r'(DEC-\d+)', dec_id)
                if not dec_match:
                    continue
                
                dec_id = dec_match.group(1)
                
                decision_obj = {
                    'id': dec_id,
                    'title': title,
                    'decision': decision,
                    'status': status
                }
                
                # Categorize by status
                if '✅' in status or 'Approved' in status or 'Complete' in status:
                    recent.append(decision_obj)
                elif '📋' in status or 'in_progress' in status.lower() or 'pending' in status.lower():
                    pending.append(decision_obj)
        
        # Take last 5 recent decisions
        recent = recent[-5:] if len(recent) > 5 else recent
        
        return pending, recent
    
    def extract_recent_work(self, events: List[Dict]) -> List[Dict]:
        """Extract recent work blocks/slices from events"""
        recent_work = []
        
        for event in reversed(events):  # Most recent first
            event_type = event.get('event_type', '')
            
            if any(t in event_type for t in ['block_complete', 'SLICE', 'COMPLETE']):
                work_item = {
                    'timestamp': event.get('timestamp'),
                    'event_type': event_type,
                    'event_id': event.get('event_id', ''),
                    'summary': event.get('summary', event.get('action', ''))
                }
                
                # Add slice/block specific fields
                if 'slice_id' in event:
                    work_item['slice_id'] = event['slice_id']
                if 'block_id' in event:
                    work_item['block_id'] = event['block_id']
                if 'pr_number' in event.get('payload', {}):
                    work_item['pr_number'] = event['payload']['pr_number']
                if 'pr_url' in event.get('payload', {}):
                    work_item['pr_url'] = event['payload']['pr_url']
                
                recent_work.append(work_item)
            
            if len(recent_work) >= 10:  # Limit to 10 most recent
                break
        
        return recent_work
    
    def build_compact_from_truth(self) -> Dict[str, Any]:
        """
        Build new SYSTEM_STATE_COMPACT.json from Truth Sources.
        
        Returns:
            New COMPACT dict
        """
        # Read all truth sources
        governance = self.read_governance_snapshot()
        services_reg = self.read_services_registry()
        events = self.read_event_timeline()
        pending_decs, recent_decs = self.parse_decisions()
        
        # Extract data from governance (authoritative for system state)
        gov_system = governance.get('system_state', {})
        gov_git = governance.get('git', {})
        gov_services = governance.get('services_summary', {})
        gov_fitness = governance.get('fitness_metrics', {})
        
        # Build new COMPACT
        new_compact = {
            "_schema": "SYSTEM_STATE_COMPACT_V1",
            "_description": "Compact JSON representation of AI-OS current state - single source for external agents",
            "_version": "1.2",  # Bump from 1.1
            "_generated": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "_generated_by": "reconciler_v1",
            
            "system": {
                "name": "AI-OS",
                "description": "Personal AI operating system with integrated GitHub and Google Workspace services",
                "repo": "edri2or-commits/ai-os",
                "branch": gov_git.get('branch', 'main'),
                "phase": gov_system.get('phase', 'Phase 2.3'),
                "mode": gov_system.get('mode', 'INFRA_ONLY'),
                "automations_enabled": gov_system.get('automations_enabled', False),
                "sandbox_only": True
            },
            
            "services_summary": gov_services,
            
            "fitness_metrics": gov_fitness,
            
            "recent_work": self.extract_recent_work(events),
            
            "pending_decisions": [
                {
                    "id": d['id'],
                    "title": d['title'],
                    "status": d['status']
                }
                for d in pending_decs
            ],
            
            "recent_decisions": [
                {
                    "id": d['id'],
                    "title": d['title'],
                    "decision": d['decision'],
                    "status": d['status']
                }
                for d in recent_decs
            ],
            
            "git_status": {
                "branch": gov_git.get('branch', 'main'),
                "last_commit": gov_git.get('last_commit', 'unknown')
            },
            
            "last_daily_context_sync_utc": gov_system.get('last_daily_context_sync_utc', '')
        }
        
        return new_compact
    
    def detect_drift(self, old_compact: Dict, new_compact: Dict) -> Dict[str, Any]:
        """
        Compare old and new COMPACT to detect drift.
        
        Returns:
            Dict with drift details
        """
        drift = {
            'decisions': [],
            'services_count': None,
            'timestamp_gap_hours': None,
            'phase_mismatch': None,
            'version_bump': None,
            'fitness_metrics': None
        }
        
        # Check timestamp staleness
        old_ts = old_compact.get('_generated', '')
        new_ts = new_compact.get('_generated', '')
        if old_ts and new_ts:
            try:
                old_dt = datetime.fromisoformat(old_ts.replace('Z', '+00:00'))
                new_dt = datetime.fromisoformat(new_ts.replace('Z', '+00:00'))
                gap = (new_dt - old_dt).total_seconds() / 3600
                drift['timestamp_gap_hours'] = round(gap, 1)
            except:
                pass
        
        # Check version
        old_v = old_compact.get('_version', '')
        new_v = new_compact.get('_version', '')
        if old_v != new_v:
            drift['version_bump'] = f"{old_v} → {new_v}"
        
        # Check phase
        old_phase = old_compact.get('system', {}).get('phase', '')
        new_phase = new_compact.get('system', {}).get('phase', '')
        if old_phase != new_phase:
            drift['phase_mismatch'] = f"{old_phase} → {new_phase}"
        
        # Check services count
        old_count = old_compact.get('services_summary', {}).get('total', 0)
        new_count = new_compact.get('services_summary', {}).get('total', 0)
        if old_count != new_count:
            drift['services_count'] = f"{old_count} → {new_count}"
        
        # Check decisions (compare pending lists)
        old_pending_ids = {d['id'] for d in old_compact.get('pending_decisions', [])}
        new_pending_ids = {d['id'] for d in new_compact.get('pending_decisions', [])}
        
        moved_to_approved = old_pending_ids - new_pending_ids
        if moved_to_approved:
            drift['decisions'] = [f"{dec_id}: pending → approved" for dec_id in moved_to_approved]
        
        # Check fitness metrics
        old_fitness = old_compact.get('fitness_metrics', {})
        new_fitness = new_compact.get('fitness_metrics', {})
        if old_fitness != new_fitness and new_fitness:
            drift['fitness_metrics'] = 'Updated from GOVERNANCE snapshot'
        
        return drift
    
    def generate_reconciliation_report(self, drift: Dict) -> List[str]:
        """Convert drift dict to human-readable reconciliation actions"""
        actions = []
        
        if drift.get('timestamp_gap_hours'):
            actions.append(f"Updated timestamp (was {drift['timestamp_gap_hours']}h old)")
        
        if drift.get('version_bump'):
            actions.append(f"Bumped version: {drift['version_bump']}")
        
        if drift.get('phase_mismatch'):
            actions.append(f"Fixed phase: {drift['phase_mismatch']}")
        
        if drift.get('services_count'):
            actions.append(f"Fixed services count: {drift['services_count']}")
        
        if drift.get('decisions'):
            for dec in drift['decisions']:
                actions.append(f"Moved decision: {dec}")
        
        if drift.get('fitness_metrics'):
            actions.append(drift['fitness_metrics'])
        
        return actions
    
    def reconcile(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        Main reconciliation function.
        
        Args:
            dry_run: If True, don't write files, just return diff
        
        Returns:
            Reconciliation result with drift and actions
        """
        # Verify truth sources exist
        sources_status = self.verify_truth_sources()
        missing = [name for name, exists in sources_status.items() if not exists and name != 'compact']
        
        if missing:
            return {
                'status': 'error',
                'error': f"Missing truth sources: {', '.join(missing)}",
                'sources_status': sources_status
            }
        
        # Read old COMPACT if exists
        old_compact = {}
        if self.paths['compact'].exists():
            with open(self.paths['compact'], 'r', encoding='utf-8') as f:
                old_compact = json.load(f)
        
        # Build new COMPACT from truth
        new_compact = self.build_compact_from_truth()
        
        # Detect drift
        drift = self.detect_drift(old_compact, new_compact)
        reconciliation_applied = self.generate_reconciliation_report(drift)
        
        result = {
            'status': 'success',
            'timestamp': new_compact['_generated'],
            'previous_generated': old_compact.get('_generated', 'N/A'),
            'drift_detected': {k: v for k, v in drift.items() if v},
            'reconciliation_applied': reconciliation_applied,
            'dry_run': dry_run
        }
        
        # Write new COMPACT (unless dry_run)
        if not dry_run:
            with open(self.paths['compact'], 'w', encoding='utf-8') as f:
                json.dump(new_compact, f, indent=2, ensure_ascii=False)
            result['file_written'] = str(self.paths['compact'])
            
            # Append reconciliation event to timeline
            self._append_reconciliation_event(drift, reconciliation_applied)
        
        return result
    
    def _append_reconciliation_event(self, drift: Dict, actions: List[str]):
        """Append STATE_RECONCILIATION event to EVENT_TIMELINE.jsonl"""
        event = {
            'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'event_type': 'STATE_RECONCILIATION',
            'source': 'reconciler_v1',
            'payload': {
                'drift_detected': {k: v for k, v in drift.items() if v},
                'reconciliation_applied': actions
            }
        }
        
        with open(self.paths['timeline'], 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')


# Standalone execution
if __name__ == '__main__':
    reconciler = StateReconciler()
    result = reconciler.reconcile(dry_run=False)
    
    print("=" * 60)
    print("STATE LAYER RECONCILIATION V1")
    print("=" * 60)
    print(f"Status: {result['status']}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"Previous: {result['previous_generated']}")
    print()
    
    if result.get('drift_detected'):
        print("Drift Detected:")
        for key, value in result['drift_detected'].items():
            print(f"  - {key}: {value}")
        print()
    
    if result.get('reconciliation_applied'):
        print("Reconciliation Applied:")
        for action in result['reconciliation_applied']:
            print(f"  ✓ {action}")
        print()
    
    if result.get('file_written'):
        print(f"File written: {result['file_written']}")
    
    print("=" * 60)
