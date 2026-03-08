"""Type checking utilities."""


def get_int(value, default: int = 0) -> int:
    """Convert a value to an integer, if possible.

    Args:
        value: The value to convert.
        default: The default value to return if conversion fails. Defaults to 0.

    Returns:
        int: The converted integer value, or the default if conversion fails.

    Example:
        >>> get_int("42")
        42
        >>> get_int("abc", default=10)
        10
        >>> get_int(None, default=5)
        5
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def get_float(value, default: float = 0.0) -> float:
    """Convert a value to a float, if possible.

    Args:
        value: The value to convert.
        default: The default value to return if conversion fails. Defaults to 0.0.

    Returns:
        float: The converted float value, or the default if conversion fails.

    Example:
        >>> get_float("3.14")
        3.14
        >>> get_float("abc", default=1.0)
        1.0
        >>> get_float(None, default=2.5)
        2.5
    """
    if isinstance(value, str):
        value = value.replace(",", ".")
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def assert_non_negative_integer(value: int, name: str = "value") -> None:
    """Assert that a value is a non-negative integer.

    Args:
        value: The value to check.
        name: The name of the value for error messages. Defaults to "value".

    Raises:
        ValueError: If the value is not a non-negative integer.

    Example:
        >>> assert_non_negative_integer(5)
        >>> assert_non_negative_integer(-1)
        Traceback (most recent call last):
            ...
        ValueError: value must be a non-negative integer, got -1
    """
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer, got {value}")
