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
