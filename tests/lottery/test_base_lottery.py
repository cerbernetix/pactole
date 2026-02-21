"""Unit tests for BaseLottery."""

from __future__ import annotations

from datetime import date
from typing import Callable, Iterable

from pactole.combinations import BoundCombination, LotteryCombination
from pactole.data import DrawRecord, FoundCombination, WinningRank
from pactole.lottery import BaseLottery
from pactole.utils import DrawDays, Weekday


class DummyProvider:
    """Minimal provider stub for BaseLottery tests."""

    def __init__(
        self,
        draw_days: DrawDays,
        combination_factory: Callable[..., LotteryCombination],
        records: Iterable[DrawRecord],
    ) -> None:
        self.draw_days = draw_days
        self.combination_factory = combination_factory
        self._records = list(records)
        self.load_calls: list[bool] = []

    def load(self, force: bool = False) -> list[DrawRecord]:
        """Return the cached records."""
        self.load_calls.append(force)
        return list(self._records)


def build_combination_factory() -> tuple[Callable[..., LotteryCombination], LotteryCombination]:
    """Return a combination factory with a predictable template."""
    template = LotteryCombination(
        main=BoundCombination(start=1, end=10, count=2),
        winning_ranks={(2,): 1, (1,): 2},
    )
    return template.get_combination, template


def build_record(period: str, draw_date: date, combination: LotteryCombination) -> DrawRecord:
    """Build a DrawRecord with predictable values for tests."""
    return DrawRecord(
        period=period,
        draw_date=draw_date,
        deadline_date=draw_date,
        combination=combination,
        numbers={"main": combination.get_component_values("main")},
        winning_ranks=[WinningRank(rank=1, winners=1, gain=1.0)],
    )


class TestBaseLottery:
    """Tests for BaseLottery in pactole.data."""

    def test_draw_days_returns_provider_draw_days(self) -> None:
        """Expose the provider draw days."""

        draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])
        factory, _ = build_combination_factory()
        provider = DummyProvider(draw_days, factory, [])
        lottery = BaseLottery(provider)

        result = lottery.draw_days

        assert result is draw_days

    def test_combination_factory_returns_provider_factory(self) -> None:
        """Expose the provider combination factory."""

        draw_days = DrawDays([Weekday.MONDAY])
        factory, _ = build_combination_factory()
        provider = DummyProvider(draw_days, factory, [])
        lottery = BaseLottery(provider)

        result = lottery.combination_factory

        assert result is factory

    def test_get_last_draw_date_delegates_to_draw_days(self) -> None:
        """Return the last draw date from the provider draw days."""

        draw_days = DrawDays([Weekday.TUESDAY, Weekday.FRIDAY])
        factory, _ = build_combination_factory()
        provider = DummyProvider(draw_days, factory, [])
        lottery = BaseLottery(provider)

        result = lottery.get_last_draw_date(from_date=date(2024, 6, 5), closest=True)

        assert result == date(2024, 6, 4)

    def test_get_next_draw_date_delegates_to_draw_days(self) -> None:
        """Return the next draw date from the provider draw days."""

        draw_days = DrawDays([Weekday.TUESDAY, Weekday.FRIDAY])
        factory, _ = build_combination_factory()
        provider = DummyProvider(draw_days, factory, [])
        lottery = BaseLottery(provider)

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
        provider = DummyProvider(draw_days, DummyCombination, [])
        lottery = BaseLottery(provider)

        result = lottery.generate(n=2, partitions=3)

        assert result == ["generated:2:3"]

    def test_get_combination_uses_combination_factory(self) -> None:
        """Create a combination from the provider factory with forwarded components."""

        factory, template = build_combination_factory()
        provider = DummyProvider(DrawDays([Weekday.TUESDAY]), factory, [])
        lottery = BaseLottery(provider)

        result = lottery.get_combination(main=[1, 2])

        assert result == template.get_combination(main=[1, 2])

    def test_count_returns_number_of_records(self) -> None:
        """Return the count of cached records."""

        factory, template = build_combination_factory()
        record = build_record("202401", date(2024, 1, 2), template.get_combination([1, 2]))
        provider = DummyProvider(DrawDays([Weekday.TUESDAY]), factory, [record])
        lottery = BaseLottery(provider)

        result = lottery.count()

        assert result == 1

    def test_dump_returns_serialized_records(self) -> None:
        """Dump cached records as dictionaries and pass the force flag."""

        factory, template = build_combination_factory()
        record = build_record("202401", date(2024, 1, 2), template.get_combination([1, 2]))
        provider = DummyProvider(DrawDays([Weekday.TUESDAY]), factory, [record])
        lottery = BaseLottery(provider)

        result = lottery.dump(force=True)

        assert result == [record.to_dict()]
        assert provider.load_calls == [True]

    def test_get_records_yields_cached_records(self) -> None:
        """Yield cached records and pass the force flag."""

        factory, template = build_combination_factory()
        record = build_record("202401", date(2024, 1, 2), template.get_combination([1, 2]))
        provider = DummyProvider(DrawDays([Weekday.TUESDAY]), factory, [record])
        lottery = BaseLottery(provider)

        records = list(lottery.get_records(force=True))

        assert records == [record]
        assert provider.load_calls == [True]

    def test_find_records_filters_by_combination(self) -> None:
        """Filter records using the combination includes check."""

        factory, template = build_combination_factory()
        record_match = build_record("202401", date(2024, 1, 2), template.get_combination([1, 2]))
        record_other = build_record("202402", date(2024, 1, 9), template.get_combination([5, 6]))
        provider = DummyProvider(DrawDays([Weekday.TUESDAY]), factory, [record_match, record_other])
        lottery = BaseLottery(provider)

        records = list(lottery.find_records(combination=[1], force=True))

        assert records == [FoundCombination(record=record_match, rank=2)]
        assert provider.load_calls == [True]

    def test_find_records_filters_by_winning_rank(self) -> None:
        """Filter records using the target winning rank."""

        factory, template = build_combination_factory()
        record_match = build_record("202401", date(2024, 1, 2), template.get_combination([1, 2]))
        record_other = build_record("202402", date(2024, 1, 9), template.get_combination([5, 6]))
        provider = DummyProvider(DrawDays([Weekday.TUESDAY]), factory, [record_match, record_other])
        lottery = BaseLottery(provider)

        records = list(lottery.find_records(combination=[1], target_rank=2))

        assert records == [FoundCombination(record=record_match, rank=2)]

    def test_find_records_defaults_to_min_winning_rank(self) -> None:
        """Use the minimum winning rank when no target rank is provided."""

        factory, template = build_combination_factory()
        record_rank1 = build_record("202401", date(2024, 1, 2), template.get_combination([1, 2]))
        record_rank2 = build_record("202402", date(2024, 1, 9), template.get_combination([1, 3]))
        record_none = build_record("202403", date(2024, 1, 16), template.get_combination([5, 6]))
        provider = DummyProvider(
            DrawDays([Weekday.TUESDAY]),
            factory,
            [record_rank1, record_rank2, record_none],
        )
        lottery = BaseLottery(provider)

        records = list(lottery.find_records(combination=[1]))

        assert records == [
            FoundCombination(record=record_rank1, rank=2),
            FoundCombination(record=record_rank2, rank=2),
        ]

    def test_find_records_allows_non_strict_pattern(self) -> None:
        """Return records matching higher winning ranks when non-strict."""

        factory, template = build_combination_factory()
        record_rank1 = build_record("202401", date(2024, 1, 2), template.get_combination([1, 2]))
        record_rank2 = build_record("202402", date(2024, 1, 9), template.get_combination([1, 3]))
        provider = DummyProvider(DrawDays([Weekday.TUESDAY]), factory, [record_rank1, record_rank2])
        lottery = BaseLottery(provider)

        records = list(lottery.find_records(combination=[1, 2], target_rank=1, strict=False))

        assert records == [
            FoundCombination(record=record_rank1, rank=1),
            FoundCombination(record=record_rank2, rank=2),
        ]

    def test_find_records_strict_pattern_requires_exact_rank(self) -> None:
        """Return only exact winning ranks when strict."""

        factory, template = build_combination_factory()
        record_rank1 = build_record("202401", date(2024, 1, 2), template.get_combination([1, 2]))
        record_rank2 = build_record("202402", date(2024, 1, 9), template.get_combination([1, 3]))
        provider = DummyProvider(DrawDays([Weekday.TUESDAY]), factory, [record_rank1, record_rank2])
        lottery = BaseLottery(provider)

        records = list(lottery.find_records(combination=[1, 2], target_rank=1, strict=True))

        assert records == [FoundCombination(record=record_rank1, rank=1)]

    def test_find_records_strict_without_target_rank_uses_combination_includes(self) -> None:
        """Filter records by combination inclusion when strict without a rank."""

        factory, template = build_combination_factory()
        record_match = build_record("202401", date(2024, 1, 2), template.get_combination([1, 2]))
        record_other = build_record("202402", date(2024, 1, 9), template.get_combination([5, 6]))
        provider = DummyProvider(DrawDays([Weekday.TUESDAY]), factory, [record_match, record_other])
        lottery = BaseLottery(provider)

        records = list(lottery.find_records(combination=[1], strict=True))

        assert records == [FoundCombination(record=record_match, rank=2)]
