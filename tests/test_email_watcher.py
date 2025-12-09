"""
Tests for Email Watcher

Run with: pytest tests/test_email_watcher.py -v
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch
import sys

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.email_watcher import EmailWatcher


@pytest.fixture
def watcher():
    return EmailWatcher(verbose=False, dry_run=True)


class TestEmailExtraction:
    def test_extract_email_summary(self, watcher):
        email = {
            "id": "001",
            "payload": {
                "headers": [
                    {"name": "From", "value": "test@example.com"},
                    {"name": "Subject", "value": "Test"}
                ]
            },
            "snippet": "Test email"
        }
        
        summary = watcher.extract_email_summary(email)
        assert summary["id"] == "001"
        assert summary["from"] == "test@example.com"


class TestClaudeClassification:
    @patch('requests.post')
    def test_classify_success(self, mock_post, watcher):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": [{"text": '[{"id": "001", "category": "work"}]'}]
        }
        mock_post.return_value = mock_response
        
        result = watcher.classify_with_claude([{"id": "001"}])
        assert len(result) == 1
        assert result[0]["category"] == "work"
