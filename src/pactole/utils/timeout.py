"""Timeout utility class for managing timeouts in various operations."""

import time


class Timeout:
    """A class to represent a timeout duration.

    Args:
        seconds (float): The duration of the timeout in seconds.
        start (bool, optional): Whether to start the timeout immediately. Defaults to True.

    Examples:
        >>> timeout = Timeout(5)
        >>> timeout.seconds
        5
        >>> timeout.elapsed
        0.0
        >>> timeout.remaining
        5.0
        >>> timeout.expired
        False
        >>> time.sleep(6)
        >>> timeout.elapsed
        6.0
        >>> timeout.remaining
        0.0
        >>> timeout.expired
        True
        >>> timeout.reset()
        >>> timeout.elapsed
        0.0
        >>> timeout.remaining
        5.0
        >>> timeout.expired
        False
    """

    _seconds: float
    _timestamp: float
    _started: bool

    def __init__(self, seconds: float, start: bool = True) -> None:
        self._seconds = seconds
        self._started = start
        self._timestamp = time.time()

    @property
    def seconds(self) -> float:
        """Return the timeout duration in seconds.

        Returns:
            float: The timeout duration in seconds.

        Examples:
            >>> timeout = Timeout(5)
            >>> timeout.seconds
            5
        """
        return self._seconds

    @seconds.setter
    def seconds(self, value: float) -> None:
        """Set the timeout duration in seconds.

        Args:
            value (float): The new timeout duration in seconds.

        Examples:
            >>> timeout = Timeout(5)
            >>> timeout.seconds = 10
            >>> timeout.seconds
            10
        """
        self._seconds = value

    @property
    def started(self) -> bool:
        """Return whether the timeout has been started.

        Returns:
            bool: True if the timeout has been started, False otherwise.

        Examples:
            >>> timeout = Timeout(5, start=False)
            >>> timeout.started
            False
            >>> timeout.start()
            >>> timeout.started
            True
        """
        return self._started

    @property
    def elapsed(self) -> float:
        """Return the elapsed time since the timeout was started.

        Returns:
            float: The elapsed time in seconds.

        Examples:
            >>> timeout = Timeout(5)
            >>> timeout.elapsed
            0.0
            >>> time.sleep(2)
            >>> timeout.elapsed
            2.0
        """
        if not self._started:
            return 0.0
        return time.time() - self._timestamp

    @property
    def remaining(self) -> float:
        """Return the remaining time before the timeout expires.

        Returns:
            float: The remaining time in seconds.

        Examples:
            >>> timeout = Timeout(5)
            >>> timeout.remaining
            5.0
            >>> time.sleep(2)
            >>> timeout.remaining
            3.0
        """
        if not self._started:
            return self._seconds
        return max(0.0, self._seconds - self.elapsed)

    @property
    def expired(self) -> bool:
        """Return True if the timeout has expired, False otherwise.

        Returns:
            bool: True if the timeout has expired, False otherwise.

        Examples:
            >>> timeout = Timeout(5)
            >>> timeout.expired
            False
            >>> time.sleep(6)
            >>> timeout.expired
            True
        """
        return self.elapsed >= self._seconds

    def start(self) -> None:
        """Start the timeout.

        Examples:
            >>> timeout = Timeout(5, start=False)
            >>> timeout.expired
            False
            >>> timeout.start()
            >>> timeout.expired
            False
            >>> time.sleep(6)
            >>> timeout.expired
            True
        """
        self._started = True
        self.reset()

    def reset(self) -> None:
        """Reset the timeout to start counting from now.

        Examples:
            >>> timeout = Timeout(5)
            >>> time.sleep(3)
            >>> timeout.elapsed
            3.0
            >>> timeout.reset()
            >>> timeout.elapsed
            0.0
        """
        self._timestamp = time.time()

    def stop(self) -> None:
        """Stop the timeout.

        Examples:
            >>> timeout = Timeout(5)
            >>> time.sleep(2)
            >>> timeout.stop()
            >>> timeout.elapsed
            2.0
            >>> timeout.remaining
            3.0
            >>> timeout.expired
            False
        """
        self._started = False
