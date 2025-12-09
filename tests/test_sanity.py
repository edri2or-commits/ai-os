"""
Sanity test - verify pytest is working

This is a minimal test to ensure the testing infrastructure is operational.
"""


def test_sanity():
    """Sanity check - pytest is working."""
    assert True


def test_basic_arithmetic():
    """Basic arithmetic works."""
    assert 1 + 1 == 2


def test_string_operations():
    """Basic string operations work."""
    assert "hello" + " " + "world" == "hello world"
