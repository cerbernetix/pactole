"""Tests for the pactole main module."""

from pactole.main import pactole


def test_pactole_returns_greeting() -> None:
    """Test that the pactole function returns the expected text."""
    result = pactole()
    assert result == "Welcome to Pactole!"
    assert isinstance(result, str)
