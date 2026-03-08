"""Tests for type checking utilities."""

import pytest

from pactole.utils import assert_non_negative_integer, get_float, get_int


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("42", 42),
        (7, 7),
        (3.5, 3),
        (True, 1),
    ],
)
def test_get_int_converts_values(value, expected):
    """Test get_int converts valid values to int."""

    assert get_int(value) == expected


@pytest.mark.parametrize(
    ("value", "default"),
    [
        ("abc", 10),
        (None, 5),
        ({"value": 1}, 2),
    ],
)
def test_get_int_returns_default(value, default):
    """Test get_int returns default on conversion errors."""

    assert get_int(value, default=default) == default


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("3.14", 3.14),
        ("3,14", 3.14),
        (7, 7.0),
        (2.5, 2.5),
        (True, 1.0),
    ],
)
def test_get_float_converts_values(value, expected):
    """Test get_float converts valid values to float."""

    assert get_float(value) == expected


@pytest.mark.parametrize(
    ("value", "default"),
    [
        ("abc", 1.0),
        (None, 2.5),
        ({"value": 1}, 3.0),
    ],
)
def test_get_float_returns_default(value, default):
    """Test get_float returns default on conversion errors."""

    assert get_float(value, default=default) == default


@pytest.mark.parametrize(
    ("value", "name"),
    [
        (-1, "value"),
        (-5, "length"),
        (3.14, "value"),
        ("abc", "length"),
    ],
)
def test_assert_non_negative_integer_raises(value, name):
    """Test assert_non_negative_integer raises ValueError for negative integers."""

    with pytest.raises(ValueError, match=f"{name} must be a non-negative integer, got {value}"):
        assert_non_negative_integer(value, name=name)


@pytest.mark.parametrize(
    ("value", "name"),
    [
        (0, "value"),
        (5, "length"),
    ],
)
def test_assert_non_negative_integer_passes(value, name):
    """Test assert_non_negative_integer does not raise for non-negative integers."""

    try:
        assert_non_negative_integer(value, name=name)
    except ValueError:
        pytest.fail(f"assert_non_negative_integer raised ValueError for {name}={value}")
