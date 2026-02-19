"""Unit tests for BaseLottery."""

from __future__ import annotations

from datetime import date
from typing import Callable

from pactole.combinations import BoundCombination, LotteryCombination
from pactole.lottery import BaseLottery
from pactole.utils import DrawDays, Weekday


def build_combination_factory() -> tuple[Callable[..., LotteryCombination], LotteryCombination]:
    """Return a combination factory with a predictable template."""
    template = LotteryCombination(
        main=BoundCombination(start=1, end=10, count=2),
        winning_ranks={(2,): 1, (1,): 2},
    )
    return template.get_combination, template


class TestBaseLottery:
    """Tests for BaseLottery in pactole.data."""

    def test_init_uses_default_factory_when_not_callable(self) -> None:
        """Fallback to LotteryCombination.get_combination when factory is not callable."""

        lottery = BaseLottery()

        result = lottery.get_combination()

        assert callable(lottery.combination_factory)
        assert lottery.draw_days.days == ()
        assert isinstance(result, LotteryCombination)

    def test_draw_days_returns_provider_draw_days(self) -> None:
        """Expose the provider draw days."""

        draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])
        factory, _ = build_combination_factory()
        lottery = BaseLottery(draw_days, factory)

        result = lottery.draw_days

        assert result is draw_days

    def test_combination_factory_returns_provider_factory(self) -> None:
        """Expose the provider combination factory."""

        draw_days = DrawDays([Weekday.MONDAY])
        factory, _ = build_combination_factory()
        lottery = BaseLottery(draw_days, factory)

        result = lottery.combination_factory

        assert result is factory

    def test_get_last_draw_date_delegates_to_draw_days(self) -> None:
        """Return the last draw date from the provider draw days."""

        draw_days = DrawDays([Weekday.TUESDAY, Weekday.FRIDAY])
        factory, _ = build_combination_factory()
        lottery = BaseLottery(draw_days, factory)

        result = lottery.get_last_draw_date(from_date=date(2024, 6, 5), closest=True)

        assert result == date(2024, 6, 4)

    def test_get_next_draw_date_delegates_to_draw_days(self) -> None:
        """Return the next draw date from the provider draw days."""

        draw_days = DrawDays([Weekday.TUESDAY, Weekday.FRIDAY])
        factory, _ = build_combination_factory()
        lottery = BaseLottery(draw_days, factory)

        result = lottery.get_next_draw_date(from_date=date(2024, 6, 5), closest=True)

        assert result == date(2024, 6, 7)

    def test_generate_uses_combination_factory(self) -> None:
        """Generate combinations from the provider factory."""

        class DummyCombination:
            """Combination stub with a predictable generate output."""

            def generate(self, n: int = 1, partitions: int = 1) -> list[str]:
                """Return predictable strings for tests."""
                return [f"generated:{n}:{partitions}"]

        draw_days = DrawDays([Weekday.TUESDAY])
        lottery = BaseLottery(draw_days, DummyCombination)

        result = lottery.generate(n=2, partitions=3)

        assert result == ["generated:2:3"]

    def test_get_combination_uses_combination_factory(self) -> None:
        """Create a combination from the provider factory with forwarded components."""

        factory, template = build_combination_factory()
        draw_days = DrawDays([Weekday.TUESDAY])
        lottery = BaseLottery(draw_days, factory)

        result = lottery.get_combination(main=[1, 2])

        assert result == template.get_combination(main=[1, 2])
