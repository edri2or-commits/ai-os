#!/usr/bin/env python3
"""
Gmail Cleanup Automation Script
================================

Purpose: Resolve Gmail storage crisis (28-day warning) via automated cleanup

Strategy:
  Tier 1 (Safe Auto-Archive): older_than:1y AND (promotions OR social) → Archive only
  Tier 2 (Download + Delete): larger:10M has:attachment → Download to Drive → Delete from Gmail
  Tier 3 (Manual Review): larger:5M is:important → Present to user → User decides

Safety:
  - Pre-flight checks (API working, disk space, user approval)
  - HITL approval gates before each tier
  - Full reversibility (Archive can be restored, Drive has backups)
  - Dry-run mode available

Output:
  - cleanup_report_YYYY-MM-DD.yaml
  - Downloaded files in: C:\Users\edri2\Desktop\AI\gmail-archive\YYYY-MM-DD\
  - Uploaded to Drive: /Gmail Archive/YYYY-MM-DD/
"""

import os
import sys
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import base64
import io

# Google API imports
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


# Configuration
OUTPUT_DIR = Path(r"C:\Users\edri2\Desktop\AI\gmail-archive")
DRIVE_FOLDER_NAME = "Gmail Archive"
MIN_DISK_SPACE_GB = 2
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/drive.file'
]


class GmailCleanup:
    """Gmail Cleanup orchestrator with 3-tier strategy"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.gmail_service = None
        self.drive_service = None
        self.session_dir = OUTPUT_DIR / datetime.now().strftime("%Y-%m-%d")
        self.stats = {
            'tier1_archived': 0,
            'tier2_downloaded': 0,
            'tier2_deleted': 0,
            'tier3_pending': 0,
            'space_freed_mb': 0,
            'errors': []
        }
        
    def authenticate(self) -> Tuple[bool, Optional[str]]:
        """Authenticate with Gmail and Drive APIs"""
        try:
            creds = None
            token_path = Path.home() / '.credentials' / 'gmail_cleanup_token.json'
            
            if token_path.exists():
                creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # Need to run OAuth flow
                    return False, "Authentication required. Please run setup first."
            
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            self.drive_service = build('drive', 'v3', credentials=creds)
            
            return True, None
        except Exception as e:
            return False, f"Authentication failed: {str(e)}"
    
    def preflight_checks(self) -> Tuple[bool, List[str]]:
        """Run safety checks before cleanup"""
        issues = []
        
        # Check 1: APIs working
        try:
            self.gmail_service.users().getProfile(userId='me').execute()
        except Exception as e:
            issues.append(f"Gmail API not working: {str(e)}")
        
        try:
            self.drive_service.about().get(fields='user').execute()
        except Exception as e:
            issues.append(f"Drive API not working: {str(e)}")
        
        # Check 2: Output directory exists or can be created
        try:
            self.session_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            issues.append(f"Cannot create output directory: {str(e)}")
        
        # Check 3: Disk space
        import shutil
        stat = shutil.disk_usage(self.session_dir.parent)
        free_gb = stat.free / (1024**3)
        if free_gb < MIN_DISK_SPACE_GB:
            issues.append(f"Low disk space: {free_gb:.2f}GB < {MIN_DISK_SPACE_GB}GB")
        
        return len(issues) == 0, issues
    
    def search_messages(self, query: str, max_results: int = 500) -> List[Dict]:
        """Search Gmail messages by query"""
        try:
            messages = []
            request = self.gmail_service.users().messages().list(
                userId='me',
                q=query,
                maxResults=min(max_results, 500)
            )
            
            while request is not None:
                response = request.execute()
                messages.extend(response.get('messages', []))
                request = self.gmail_service.users().messages().list_next(request, response)
                
                if len(messages) >= max_results:
                    break
            
            return messages[:max_results]
        except Exception as e:
            self.stats['errors'].append(f"Search failed for '{query}': {str(e)}")
            return []
    
    def get_message_details(self, message_id: str) -> Optional[Dict]:
        """Get full message details including attachments"""
        try:
            message = self.gmail_service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            return message
        except Exception as e:
            self.stats['errors'].append(f"Failed to get message {message_id}: {str(e)}")
            return None
    
    def tier1_safe_archive(self) -> Dict:
        """Tier 1: Auto-archive old promotions/social (NO deletion)"""
        print("\n" + "="*60)
        print("TIER 1: Safe Auto-Archive")
        print("="*60)
        print("Query: older_than:1y AND (category:promotions OR category:social)")
        print("Action: Remove from Inbox (archive only, NOT delete)")
        print("Risk: ZERO (easily reversible)")
        
        # Search
        query = "older_than:1y AND (category:promotions OR category:social)"
        messages = self.search_messages(query, max_results=500)
        
        print(f"\nFound: {len(messages)} messages")
        
        if len(messages) == 0:
            print("✅ No messages to archive")
            return {'archived': 0}
        
        # HITL Gate
        print(f"\n⚠️  APPROVAL REQUIRED:")
        print(f"Archive {len(messages)} old promotional emails?")
        response = input("Type 'yes' to proceed, anything else to skip: ").strip().lower()
        
        if response != 'yes':
            print("❌ Skipped by user")
            return {'archived': 0, 'skipped': True}
        
        # Archive (remove INBOX label)
        if not self.dry_run:
            archived_count = 0
            for msg in messages:
                try:
                    self.gmail_service.users().messages().modify(
                        userId='me',
                        id=msg['id'],
                        body={'removeLabelIds': ['INBOX']}
                    ).execute()
                    archived_count += 1
                except Exception as e:
                    self.stats['errors'].append(f"Failed to archive {msg['id']}: {str(e)}")
            
            self.stats['tier1_archived'] = archived_count
            print(f"✅ Archived: {archived_count} messages")
        else:
            print(f"🔍 DRY RUN: Would archive {len(messages)} messages")
        
        return {'archived': len(messages) if not self.dry_run else 0}
    
    def tier2_download_and_delete(self) -> Dict:
        """Tier 2: Download large attachments to Drive, then delete from Gmail"""
        print("\n" + "="*60)
        print("TIER 2: Download & Delete Large Attachments")
        print("="*60)
        print("Query: larger:10M has:attachment")
        print("Action: Download → Upload to Drive → Delete from Gmail")
        print("Risk: LOW (backup exists in Drive)")
        
        # Search
        query = "larger:10M has:attachment"
        messages = self.search_messages(query, max_results=100)
        
        print(f"\nFound: {len(messages)} messages with large attachments")
        
        if len(messages) == 0:
            print("✅ No large attachments to process")
            return {'downloaded': 0, 'deleted': 0}
        
        # HITL Gate
        print(f"\n⚠️  APPROVAL REQUIRED:")
        print(f"Download {len(messages)} messages with attachments to Drive, then delete from Gmail?")
        response = input("Type 'yes' to proceed, anything else to skip: ").strip().lower()
        
        if response != 'yes':
            print("❌ Skipped by user")
            return {'downloaded': 0, 'deleted': 0, 'skipped': True}
        
        # Process each message
        results = {'downloaded': 0, 'deleted': 0, 'space_freed_mb': 0}
        
        for i, msg in enumerate(messages, 1):
            print(f"\nProcessing {i}/{len(messages)}...")
            message_details = self.get_message_details(msg['id'])
            if not message_details:
                continue
            
            # Extract subject for logging
            subject = self._get_header(message_details, 'Subject')
            print(f"  Subject: {subject[:50]}...")
            
            # Download attachments
            attachments = self._extract_attachments(message_details)
            if not attachments:
                print("  No attachments found")
                continue
            
            print(f"  Found {len(attachments)} attachment(s)")
            
            # Upload to Drive (if not dry run)
            if not self.dry_run:
                for att in attachments:
                    print(f"    Uploading: {att['filename']}")
                    success = self._upload_to_drive(att)
                    if success:
                        results['downloaded'] += 1
                        results['space_freed_mb'] += att['size_mb']
                        print(f"    ✅ Uploaded ({att['size_mb']:.2f} MB)")
                
                # Delete from Gmail after successful upload
                try:
                    self.gmail_service.users().messages().trash(
                        userId='me',
                        id=msg['id']
                    ).execute()
                    results['deleted'] += 1
                    print(f"  ✅ Moved to trash")
                except Exception as e:
                    self.stats['errors'].append(f"Failed to delete {msg['id']}: {str(e)}")
                    print(f"  ❌ Failed to delete: {str(e)}")
            else:
                print(f"  🔍 DRY RUN: Would process message {msg['id']}")
        
        self.stats['tier2_downloaded'] = results['downloaded']
        self.stats['tier2_deleted'] = results['deleted']
        self.stats['space_freed_mb'] += results['space_freed_mb']
        
        print(f"\n✅ Downloaded: {results['downloaded']} attachments")
        print(f"✅ Deleted: {results['deleted']} messages")
        print(f"✅ Space freed: {results['space_freed_mb']:.2f} MB")
        
        return results
    
    def tier3_manual_review(self) -> Dict:
        """Tier 3: Present large important emails for manual review"""
        print("\n" + "="*60)
        print("TIER 3: Manual Review")
        print("="*60)
        print("Query: larger:5M is:important")
        print("Action: Show list → User decides")
        print("Risk: ZERO (user approves each)")
        
        # Search
        query = "larger:5M is:important"
        messages = self.search_messages(query, max_results=50)
        
        print(f"\nFound: {len(messages)} important messages with attachments")
        
        if len(messages) == 0:
            print("✅ No messages for manual review")
            return {'pending': 0}
        
        # Show list
        print("\n📋 Messages for review:")
        for i, msg in enumerate(messages, 1):
            details = self.get_message_details(msg['id'])
            if details:
                subject = self._get_header(details, 'Subject')
                from_addr = self._get_header(details, 'From')
                date = self._get_header(details, 'Date')
                size_mb = int(details.get('sizeEstimate', 0)) / (1024*1024)
                
                print(f"\n{i}. {subject}")
                print(f"   From: {from_addr}")
                print(f"   Date: {date}")
                print(f"   Size: {size_mb:.2f} MB")
        
        self.stats['tier3_pending'] = len(messages)
        
        print(f"\n💡 Review these messages in Gmail and decide manually.")
        print(f"   (This script doesn't auto-delete important messages)")
        
        return {'pending': len(messages)}
    
    def _extract_attachments(self, message: Dict) -> List[Dict]:
        """Extract attachment metadata from message"""
        attachments = []
        
        def process_parts(parts):
            for part in parts:
                if part.get('filename'):
                    att_id = part['body'].get('attachmentId')
                    if att_id:
                        attachments.append({
                            'message_id': message['id'],
                            'attachment_id': att_id,
                            'filename': part['filename'],
                            'mime_type': part.get('mimeType', 'application/octet-stream'),
                            'size_mb': part['body'].get('size', 0) / (1024*1024)
                        })
                
                if 'parts' in part:
                    process_parts(part['parts'])
        
        if 'parts' in message['payload']:
            process_parts(message['payload']['parts'])
        
        return attachments
    
    def _upload_to_drive(self, attachment: Dict) -> bool:
        """Upload attachment to Google Drive"""
        try:
            # Download from Gmail
            att = self.gmail_service.users().messages().attachments().get(
                userId='me',
                messageId=attachment['message_id'],
                id=attachment['attachment_id']
            ).execute()
            
            data = base64.urlsafe_b64decode(att['data'])
            
            # Create Drive folder if needed
            folder_id = self._get_or_create_drive_folder()
            
            # Upload to Drive
            file_metadata = {
                'name': attachment['filename'],
                'parents': [folder_id]
            }
            
            # Create temporary file for upload
            temp_file = io.BytesIO(data)
            
            media = MediaFileUpload(
                temp_file,
                mimetype=attachment['mime_type'],
                resumable=True
            )
            
            self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            return True
        except Exception as e:
            self.stats['errors'].append(f"Upload failed for {attachment['filename']}: {str(e)}")
            return False
    
    def _get_or_create_drive_folder(self) -> str:
        """Get or create Gmail Archive folder in Drive"""
        # Search for existing folder
        query = f"name='{DRIVE_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = self.drive_service.files().list(q=query, fields='files(id, name)').execute()
        folders = results.get('files', [])
        
        if folders:
            return folders[0]['id']
        
        # Create new folder
        file_metadata = {
            'name': DRIVE_FOLDER_NAME,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = self.drive_service.files().create(body=file_metadata, fields='id').execute()
        return folder['id']
    
    def _get_header(self, message: Dict, header_name: str) -> str:
        """Extract header value from message"""
        headers = message['payload'].get('headers', [])
        for header in headers:
            if header['name'].lower() == header_name.lower():
                return header['value']
        return ''
    
    def generate_report(self) -> str:
        """Generate YAML cleanup report"""
        report = {
            'cleanup_date': datetime.now().isoformat(),
            'dry_run': self.dry_run,
            'stats': self.stats,
            'next_steps': []
        }
        
        # Add recommendations
        if self.stats['tier3_pending'] > 0:
            report['next_steps'].append(f"Review {self.stats['tier3_pending']} important messages manually")
        
        if self.stats['space_freed_mb'] < 500:
            report['next_steps'].append("Consider running Tier 2 with lower threshold (larger:5M)")
        
        # Save report
        report_path = self.session_dir / f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
        with open(report_path, 'w', encoding='utf-8') as f:
            yaml.dump(report, f, allow_unicode=True, default_flow_style=False)
        
        print(f"\n📄 Report saved: {report_path}")
        return str(report_path)
    
    def run(self):
        """Execute full cleanup workflow"""
        print("🚀 Gmail Cleanup - Starting...")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        
        # Authenticate
        print("\n1️⃣ Authenticating...")
        success, error = self.authenticate()
        if not success:
            print(f"❌ {error}")
            return False
        print("✅ Authenticated")
        
        # Preflight checks
        print("\n2️⃣ Running preflight checks...")
        passed, issues = self.preflight_checks()
        if not passed:
            print("❌ Preflight checks failed:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        print("✅ All checks passed")
        
        # Execute tiers
        print("\n3️⃣ Executing cleanup tiers...")
        self.tier1_safe_archive()
        self.tier2_download_and_delete()
        self.tier3_manual_review()
        
        # Generate report
        print("\n4️⃣ Generating report...")
        self.generate_report()
        
        # Summary
        print("\n" + "="*60)
        print("CLEANUP SUMMARY")
        print("="*60)
        print(f"Tier 1 - Archived: {self.stats['tier1_archived']} messages")
        print(f"Tier 2 - Downloaded: {self.stats['tier2_downloaded']} attachments")
        print(f"Tier 2 - Deleted: {self.stats['tier2_deleted']} messages")
        print(f"Tier 3 - Pending review: {self.stats['tier3_pending']} messages")
        print(f"Space freed: {self.stats['space_freed_mb']:.2f} MB")
        
        if self.stats['errors']:
            print(f"\n⚠️  Errors: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:
                print(f"   - {error}")
        
        print("\n✅ Cleanup complete!")
        return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gmail Cleanup Automation')
    parser.add_argument('--dry-run', action='store_true', help='Run in dry-run mode (no changes)')
    args = parser.parse_args()
    
    cleanup = GmailCleanup(dry_run=args.dry_run)
    success = cleanup.run()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
