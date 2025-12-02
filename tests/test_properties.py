"""
Property-based tests using Hypothesis

These tests generate thousands of random inputs automatically to find edge cases.
Instead of testing specific examples, we test properties that should ALWAYS be true.

Example: "Observer.log() should NEVER crash, regardless of input"
"""

import sys
from pathlib import Path

# Add tools/ to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from observer import Observer
from input_validation import (
    validate_cr_id,
    validate_file_path,
    validate_commit_message,
    validate_entity_type,
    validate_status
)

import pytest
from hypothesis import given, strategies as st, settings, example


class TestInputValidationProperties:
    """Property-based tests for input_validation.py functions."""
    
    @given(st.text())
    @settings(max_examples=200)
    def test_validate_cr_id_never_crashes(self, text_input):
        """validate_cr_id should never crash, regardless of input."""
        # Should return bool, never raise exception
        result = validate_cr_id(text_input)
        assert isinstance(result, bool)
    
    @given(st.text())
    @example("CR-20251202-120000-abcd")  # Valid example
    @example("INVALID")  # Invalid example
    @example("")  # Empty string
    @example("CR-99999999-999999-zzzz")  # Valid format, extreme values
    def test_validate_cr_id_format_strictness(self, text_input):
        """Valid CR IDs must match exact format: CR-YYYYMMDD-HHMMSS-xxxx"""
        result = validate_cr_id(text_input)
        
        if result is True:
            # If validation passed, must be exact format
            assert text_input.startswith("CR-")
            parts = text_input.split("-")
            assert len(parts) == 4
            assert len(parts[1]) == 8  # YYYYMMDD
            assert len(parts[2]) == 6  # HHMMSS
            assert len(parts[3]) == 4  # xxxx
            assert parts[3].isalnum() and parts[3].islower()
    
    @given(st.text(min_size=1))
    @settings(max_examples=200)
    def test_validate_file_path_never_crashes(self, path_input):
        """validate_file_path should never crash with any string input."""
        result = validate_file_path(path_input)
        assert isinstance(result, bool)
    
    @given(st.text())
    def test_validate_file_path_blocks_parent_refs(self, path_input):
        """Paths containing '..' should ALWAYS be rejected."""
        if ".." in path_input:
            result = validate_file_path(path_input)
            assert result is False, f"Path with '..' should be rejected: {path_input}"
    
    @given(st.text(max_size=500))
    @settings(max_examples=200)
    def test_validate_commit_message_never_crashes(self, message):
        """validate_commit_message should handle any text input."""
        result = validate_commit_message(message)
        assert isinstance(result, bool)
    
    @given(st.text())
    def test_validate_commit_message_blocks_shell_chars(self, message):
        """Messages with shell metacharacters should be rejected."""
        dangerous = ['|', '&', ';', '$', '`', '\n', '\r']
        
        has_dangerous = any(char in message for char in dangerous)
        result = validate_commit_message(message)
        
        if has_dangerous:
            assert result is False, f"Message with shell chars should be rejected"
    
    @given(st.text())
    def test_validate_entity_type_is_whitelist(self, entity_type):
        """Only exact valid entity types should pass."""
        valid_types = {'area', 'project', 'task', 'context', 'identity', 'log'}
        result = validate_entity_type(entity_type)
        
        if result is True:
            assert entity_type in valid_types
        else:
            assert entity_type not in valid_types


class TestObserverProperties:
    """Property-based tests for Observer class."""
    
    def test_observer_log_never_crashes_with_fixtures(self, temp_repo):
        """Observer.log() should handle various messages without crashing."""
        observer = Observer(temp_repo, verbose=True)
        
        # Test with a variety of strings
        test_messages = [
            "normal message",
            "",
            "a" * 10000,  # very long
            "\n\n\n",  # newlines
            "unicode: 你好 🎉",
            "special: |&;$`",
        ]
        
        for message in test_messages:
            try:
                observer.log(message)
            except Exception as e:
                pytest.fail(f"Observer.log() crashed with: {e}")
    
    def test_observer_handles_various_repo_paths(self, tmp_path):
        """Observer initialization should handle various paths."""
        test_cases = [
            "normal-repo",
            "repo with spaces",
            "repo_with_underscores",
            "123-numeric",
        ]
        
        for path_name in test_cases:
            test_path = tmp_path / path_name
            test_path.mkdir(exist_ok=True, parents=True)
            
            # Observer should not crash on initialization
            observer = Observer(test_path)
            assert observer.repo_root == test_path


class TestPropertyInvariants:
    """Test mathematical/logical properties that should always hold."""
    
    def test_yaml_file_count_never_negative(self, truth_layer_dir):
        """Number of YAML files detected should never be negative."""
        # Create various numbers of YAML files
        test_counts = [0, 1, 5, 10, 25]
        
        for count in test_counts:
            # Clean directory
            for f in truth_layer_dir.glob("**/*.yaml"):
                f.unlink()
            
            # Create specified number of YAML files
            for i in range(count):
                (truth_layer_dir / "projects" / f"test-{i}.yaml").write_text("id: test")
            
            observer = Observer(truth_layer_dir.parent)
            yaml_files = observer.get_yaml_files()
            
            assert len(yaml_files) >= 0, "File count cannot be negative"
            assert len(yaml_files) == count, f"Expected {count} files, got {len(yaml_files)}"
    
    @given(st.text(), st.text())
    def test_validate_status_consistency(self, status, entity_type):
        """Status validation should be consistent - same inputs give same result."""
        result1 = validate_status(status, entity_type)
        result2 = validate_status(status, entity_type)
        
        assert result1 == result2, "validate_status should be deterministic"
    
    @given(st.text(min_size=1, max_size=100))
    @example("feat: add feature")
    @example("fix: bug fix")
    def test_safe_commit_messages_always_pass(self, message):
        """Messages without dangerous chars and reasonable length should pass."""
        # Remove any dangerous characters
        safe_message = message
        for char in ['|', '&', ';', '$', '`', '\n', '\r', '$(', '${']:
            safe_message = safe_message.replace(char, '')
        
        if len(safe_message) <= 500 and safe_message:
            result = validate_commit_message(safe_message)
            assert result is True, f"Safe message rejected: {safe_message}"
    
    @given(st.text(alphabet='abcdefghijklmnopqrstuvwxyz0123456789', min_size=4, max_size=4))
    @example("abcd")
    @example("1234")
    @example("a1b2")
    def test_cr_id_with_valid_suffix(self, suffix):
        """CR IDs with valid lowercase alphanumeric suffix should pass."""
        cr_id = f"CR-20251202-120000-{suffix}"
        
        # All lowercase alphanumeric 4-char suffixes should be valid
        result = validate_cr_id(cr_id)
        assert result is True, f"Valid CR ID rejected: {cr_id}"
