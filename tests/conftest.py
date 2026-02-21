"""Shared pytest fixtures for tests."""

from typing import Generator
from unittest.mock import patch

import pytest

from pactole.utils import timeout as timeout_module


class FakeTime:
    """Simple controllable clock for tests."""

    def __init__(self, start: float = 0.0) -> None:
        self._now = start

    def time(self) -> float:
        """Return the current fake time."""
        return self._now

    def advance(self, seconds: float) -> None:
        """Advance the fake time forward."""
        self._now += seconds


@pytest.fixture
def fake_time() -> Generator[FakeTime, None, None]:
    """Provide a fake time source for time-based tests."""
    clock = FakeTime()
    with patch.object(timeout_module.time, "time", clock.time):
        yield clock
