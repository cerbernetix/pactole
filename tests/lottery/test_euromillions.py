"""Unit tests for EuroMillions lottery."""

from __future__ import annotations

from datetime import date

from pactole.combinations import EuroMillionsCombination
from pactole.lottery import EuroMillions
from pactole.utils import Weekday


class TestEuroMillions:
    """Tests for EuroMillions initialization."""

    def test_init_sets_expected_draw_days(self) -> None:
        """Expose Tuesday and Friday as draw days."""

        lottery = EuroMillions()

        assert lottery.draw_days.days == (Weekday.TUESDAY, Weekday.FRIDAY)

    def test_init_sets_expected_combination_factory(self) -> None:
        """Expose EuroMillionsCombination as combination factory."""

        lottery = EuroMillions()

        assert lottery.combination_factory is EuroMillionsCombination

    def test_get_last_and_next_draw_date(self) -> None:
        """Compute previous and next draw dates using configured draw days."""

        lottery = EuroMillions()

        assert lottery.get_last_draw_date(from_date=date(2024, 6, 5), closest=True) == date(
            2024, 6, 4
        )
        assert lottery.get_next_draw_date(from_date=date(2024, 6, 5), closest=True) == date(
            2024, 6, 7
        )

    def test_get_combination_uses_euromillions_factory(self) -> None:
        """Create a EuroMillionsCombination from forwarded components."""

        lottery = EuroMillions()

        result = lottery.get_combination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])

        assert isinstance(result, EuroMillionsCombination)
        assert result.numbers == [1, 2, 3, 4, 5]
        assert result.stars == [1, 2]
