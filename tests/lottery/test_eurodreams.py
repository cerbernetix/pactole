"""Unit tests for EuroDreams lottery."""

from __future__ import annotations

from datetime import date

from pactole.combinations import EuroDreamsCombination
from pactole.lottery import EuroDreams
from pactole.utils import Weekday


class TestEuroDreams:
    """Tests for EuroDreams initialization."""

    def test_init_sets_expected_draw_days(self) -> None:
        """Expose Monday and Thursday as draw days."""

        lottery = EuroDreams()

        assert lottery.draw_days.days == (Weekday.MONDAY, Weekday.THURSDAY)

    def test_init_sets_expected_combination_factory(self) -> None:
        """Expose EuroDreamsCombination as combination factory."""

        lottery = EuroDreams()

        assert lottery.combination_factory is EuroDreamsCombination

    def test_get_last_and_next_draw_date(self) -> None:
        """Compute previous and next draw dates using configured draw days."""

        lottery = EuroDreams()

        assert lottery.get_last_draw_date(from_date=date(2024, 6, 5), closest=True) == date(
            2024, 6, 3
        )
        assert lottery.get_next_draw_date(from_date=date(2024, 6, 5), closest=True) == date(
            2024, 6, 6
        )

    def test_get_combination_uses_eurodreams_factory(self) -> None:
        """Create a EuroDreamsCombination from forwarded components."""

        lottery = EuroDreams()

        result = lottery.get_combination(numbers=[1, 2, 3, 4, 5, 6], dream=[2])

        assert isinstance(result, EuroDreamsCombination)
        assert result.numbers == [1, 2, 3, 4, 5, 6]
        assert result.dream == [2]
