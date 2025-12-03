"""
Email Watcher - Production Grade Gmail Automation

Monitors Gmail for unread emails, classifies them with Claude,
and generates drift reports for reconciliation.

Architecture:
    - Reuses Google MCP OAuth tokens (no re-authentication needed)
    - Anthropic API for classification
    - Structured JSONL logging (compatible with MCP Logger)
    - YAML drift reports (compatible with Observer/Reconciler)
    - Windows Task Scheduler integration

Usage:
    python tools/email_watcher.py [--dry-run] [--verbose]
    
Integration:
    - Observer detects drift reports
    - Reconciler generates Change Requests
    - User approves via HITL
"""

import sys
import json
import yaml
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
import argparse

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment
from dotenv import load_dotenv
import os
load_dotenv(PROJECT_ROOT / ".env")

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_TOKEN_PATH = Path.home() / ".google-mcp-tokens.json"
DRIFT_DIR = PROJECT_ROOT / "memory-bank" / "drift"
LOG_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
DRIFT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


class EmailWatcher:
    """Email monitoring and classification system"""
    
    def __init__(self, verbose: bool = False, dry_run: bool = False):
        self.verbose = verbose
        self.dry_run = dry_run
        self.log_file = LOG_DIR / "email_watcher.jsonl"
        
    def log(self, event_type: str, message: str, metadata: Optional[Dict] = None):
        """Structured logging (JSONL format like MCP Logger)"""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "message": message,
            "metadata": metadata or {}
        }
        
        # Write to JSONL
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Console output
        if self.verbose:
            print(f"[{event_type.upper()}] {message}")
    
    def load_google_token(self) -> Optional[str]:
        """Load OAuth token from Google MCP tokens file"""
        try:
            with open(GOOGLE_TOKEN_PATH, 'r') as f:
                tokens = json.load(f)
                return tokens.get("access_token")
        except FileNotFoundError:
            self.log("error", "Google MCP tokens not found", 
                    {"path": str(GOOGLE_TOKEN_PATH)})
            return None
        except Exception as e:
            self.log("error", f"Failed to load Google token: {e}")
            return None
    
    def search_unread_emails(self, access_token: str, max_results: int = 50) -> List[Dict]:
        """Search Gmail for unread emails using Gmail API"""
        try:
            # Get message IDs
            response = requests.get(
                "https://gmail.googleapis.com/gmail/v1/users/me/messages",
                headers={"Authorization": f"Bearer {access_token}"},
                params={"q": "is:unread", "maxResults": max_results}
            )
            
            if response.status_code != 200:
                self.log("error", f"Gmail API failed: {response.status_code}",
                        {"response": response.text})
                return []
            
            message_ids = response.json().get("messages", [])
            self.log("info", f"Found {len(message_ids)} unread emails")
            
            # Fetch full messages (batch first 10 for performance)
            emails = []
            for msg in message_ids[:10]:  # Limit to 10 for Claude API
                msg_response = requests.get(
                    f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg['id']}",
                    headers={"Authorization": f"Bearer {access_token}"},
                    params={"format": "metadata"}
                )
                
                if msg_response.status_code == 200:
                    emails.append(msg_response.json())
            
            return emails
            
        except Exception as e:
            self.log("error", f"Failed to search emails: {e}")
            return []
    
    def extract_email_summary(self, email: Dict) -> Dict:
        """Extract relevant fields from Gmail API response"""
        headers = {h["name"]: h["value"] 
                  for h in email.get("payload", {}).get("headers", [])}
        
        return {
            "id": email.get("id"),
            "from": headers.get("From", "Unknown"),
            "to": headers.get("To", "Unknown"),
            "subject": headers.get("Subject", "No Subject"),
            "date": headers.get("Date", "Unknown"),
            "snippet": email.get("snippet", "")
        }
    
    def classify_with_claude(self, email_summaries: List[Dict]) -> List[Dict]:
        """Classify emails using Claude API"""
        try:
            prompt = f"""Classify these emails into categories: bureaucracy, personal, work.
For each email, determine:
- category: bureaucracy/personal/work
- priority: low/medium/high
- action_needed: true/false
- suggested_action: brief description if action needed

Return ONLY a JSON array with this exact format:
[{{"id": "...", "category": "...", "priority": "...", "action_needed": false, "suggested_action": ""}}]

Emails to classify:
{json.dumps(email_summaries, indent=2)}"""

            self.log("info", "Calling Claude API for classification")
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 2048,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30
            )
            
            if response.status_code != 200:
                self.log("error", f"Claude API failed: {response.status_code}",
                        {"response": response.text})
                return []
            
            claude_response = response.json()
            classification_text = claude_response["content"][0]["text"]
            
            # Parse JSON from response
            try:
                # Try direct parse
                classifications = json.loads(classification_text)
            except:
                # Extract from markdown code block
                import re
                json_match = re.search(r'```json\s*(\[.*?\])\s*```', 
                                     classification_text, re.DOTALL)
                if json_match:
                    classifications = json.loads(json_match.group(1))
                else:
                    self.log("error", "Failed to parse Claude response as JSON",
                            {"response": classification_text[:200]})
                    return []
            
            self.log("info", f"Classified {len(classifications)} emails")
            return classifications
            
        except Exception as e:
            self.log("error", f"Classification failed: {e}")
            return []
    
    def generate_drift_report(self, emails: List[Dict], 
                            classifications: List[Dict]) -> Dict:
        """Generate YAML drift report compatible with Observer"""
        timestamp = datetime.now(timezone.utc)
        
        # Merge email data with classifications
        classified_emails = []
        for email in emails:
            email_id = email["id"]
            classification = next((c for c in classifications 
                                 if c.get("id") == email_id), {})
            
            classified_emails.append({
                **email,
                **classification
            })
        
        report = {
            "timestamp": timestamp.isoformat(),
            "type": "email_drift",
            "unread_count": len(emails),
            "classified_count": len(classifications),
            "classified_emails": classified_emails
        }
        
        return report
    
    def save_drift_report(self, report: Dict) -> Path:
        """Save drift report to YAML file"""
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        filename = f"email-drift-{timestamp}.yaml"
        filepath = DRIFT_DIR / filename
        
        if self.dry_run:
            self.log("info", f"[DRY RUN] Would save: {filepath}")
            # Skip printing YAML to avoid Windows console encoding issues
            print(f"[DRY RUN] Report preview: {len(report['classified_emails'])} emails classified")
            return filepath
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(report, f, allow_unicode=True, default_flow_style=False)
        
        self.log("info", f"Drift report saved: {filepath}")
        return filepath
    
    def run(self):
        """Main execution flow"""
        self.log("start", "Email Watcher starting")
        
        # Step 1: Load OAuth token
        access_token = self.load_google_token()
        if not access_token:
            self.log("error", "Cannot proceed without Google OAuth token")
            return 1
        
        # Step 2: Search unread emails
        emails = self.search_unread_emails(access_token)
        if not emails:
            self.log("info", "No unread emails found")
            return 0
        
        # Step 3: Extract summaries
        email_summaries = [self.extract_email_summary(e) for e in emails]
        
        # Step 4: Classify with Claude
        classifications = self.classify_with_claude(email_summaries)
        if not classifications:
            self.log("warning", "Classification failed, skipping report")
            return 1
        
        # Step 5: Generate drift report
        report = self.generate_drift_report(email_summaries, classifications)
        
        # Step 6: Save report
        self.save_drift_report(report)
        
        self.log("complete", "Email Watcher completed successfully",
                {"emails_processed": len(emails)})
        
        return 0


def main():
    parser = argparse.ArgumentParser(description="Email Watcher - Gmail Automation")
    parser.add_argument("--dry-run", action="store_true",
                       help="Preview without saving")
    parser.add_argument("--verbose", action="store_true",
                       help="Verbose console output")
    
    args = parser.parse_args()
    
    watcher = EmailWatcher(verbose=args.verbose, dry_run=args.dry_run)
    
    try:
        exit_code = watcher.run()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[CANCELLED] Email Watcher interrupted by user")
        sys.exit(130)
    except Exception as e:
        watcher.log("fatal", f"Unexpected error: {e}")
        print(f"[FATAL] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
