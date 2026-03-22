"""Unit tests for data models."""

from __future__ import annotations

import datetime

import pytest

from pactole.combinations import (
    BoundCombination,
    CombinationInputOrRank,
    CombinationInputWithRank,
    CompoundCombination,
    LotteryCombination,
)
from pactole.data import DrawRecord, FoundCombination, WinningRank


class TestDrawRecord:
    """Tests for data model helpers."""

    def test_draw_record_to_csv_exports_fields(self) -> None:
        """Test to_csv returns all expected fields."""

        draw_date = datetime.date(2024, 1, 15)
        deadline_date = datetime.date(2024, 2, 15)
        main = BoundCombination(values=[12, 5, 23], start=1, end=50, count=3)
        bonus = BoundCombination(values=[7], start=1, end=10, count=1)
        combination = LotteryCombination(main=main, bonus=bonus)
        record = DrawRecord(
            period="202401",
            draw_date=draw_date,
            deadline_date=deadline_date,
            combination=combination,
            numbers={"main": [12, 5, 23], "bonus": [7]},
            winning_ranks=[
                WinningRank(rank=1, winners=2, gain=1_000_000.0),
                WinningRank(rank=2, winners=10, gain=50_000.0),
            ],
        )

        result = record.to_csv()

        assert result == {
            "period": "202401",
            "draw_date": "2024-01-15",
            "deadline_date": "2024-02-15",
            "main_1": 12,
            "main_2": 5,
            "main_3": 23,
            "bonus_1": 7,
            "main_rank": main.rank,
            "bonus_rank": bonus.rank,
            "combination_rank": combination.rank,
            "rank_1_winners": 2,
            "rank_1_gain": 1_000_000.0,
            "rank_2_winners": 10,
            "rank_2_gain": 50_000.0,
        }

    def test_draw_record_from_csv_builds_components_and_ranks(self) -> None:
        """Test from_csv builds numbers and winning ranks with a factory."""

        def factory(
            main: CombinationInputWithRank,
            bonus: CombinationInputWithRank,
        ) -> LotteryCombination:
            """Build a LotteryCombination with fixed bounds for tests."""

            return LotteryCombination(
                main=BoundCombination(
                    values=main["values"],
                    rank=main["rank"],
                    start=1,
                    end=50,
                    count=3,
                ),
                bonus=BoundCombination(
                    values=bonus["values"],
                    rank=bonus["rank"],
                    start=1,
                    end=10,
                    count=1,
                ),
            )

        data = {
            "period": "202402",
            "draw_date": "2024-02-10",
            "deadline_date": "2024-03-10",
            "main_1": "3",
            "main_2": "11",
            "main_3": "5",
            "bonus_1": "9",
            "main_rank": "5",
            "bonus_rank": "1",
            "combination_rank": "123",
            "rank_2_winners": "4",
            "rank_1_winners": "1",
            "rank_1_gain": "250000.0",
            "dummy_field": "ignored",
        }

        record = DrawRecord.from_csv(data, factory)

        assert record.period == "202402"
        assert record.draw_date == datetime.date(2024, 2, 10)
        assert record.deadline_date == datetime.date(2024, 3, 10)
        assert record.numbers == {"main": [3, 11, 5], "bonus": [9]}
        assert record.combination.components["main"].values == [3, 5, 11]
        assert record.combination.components["bonus"].values == [9]
        assert record.winning_ranks == [
            WinningRank(rank=1, winners=1, gain=250_000.0),
            WinningRank(rank=2, winners=4, gain=0.0),
        ]

    def test_draw_record_from_csv_defaults_combination(self) -> None:
        """Test from_csv falls back to an empty LotteryCombination."""

        data = {
            "period": "202403",
            "draw_date": "2024-03-10",
            "deadline_date": "2024-04-10",
            "main_1": 8,
            "main_2": 14,
            "rank_1_winners": 2,
            "rank_1_gain": 100.0,
        }

        record = DrawRecord.from_csv(data, object())

        assert isinstance(record.combination, LotteryCombination)
        assert not record.combination.components
        assert record.numbers == {"main": [8, 14]}
        assert record.winning_ranks == [WinningRank(rank=1, winners=2, gain=100.0)]

    def test_draw_record_to_json_exports_all_fields(self) -> None:
        """Test to_json returns all expected JSON fields."""

        draw_date = datetime.date(2024, 1, 15)
        deadline_date = datetime.date(2024, 2, 15)
        main = BoundCombination(values=[5, 12, 23], start=1, end=50, count=3)
        bonus = BoundCombination(values=[7], start=1, end=10, count=1)
        combination = LotteryCombination(main=main, bonus=bonus)
        record = DrawRecord(
            period="202401",
            draw_date=draw_date,
            deadline_date=deadline_date,
            combination=combination,
            numbers={"main": [5, 12, 23], "bonus": [7]},
            winning_ranks=[
                WinningRank(rank=1, winners=2, gain=1_000_000.0),
                WinningRank(rank=2, winners=10, gain=50_000.0),
            ],
        )

        result = record.to_json()

        assert result == {
            "period": "202401",
            "draw_date": "2024-01-15",
            "deadline_date": "2024-02-15",
            "combination": combination.to_json(),
            "numbers": combination.values,
            "winning_ranks": [
                {"rank": 1, "winners": 2, "gain": 1_000_000.0},
                {"rank": 2, "winners": 10, "gain": 50_000.0},
            ],
        }

    def test_draw_record_from_json_with_factory(self) -> None:
        """Test from_json builds a DrawRecord using a combination factory."""

        def factory(main: list, bonus: list) -> LotteryCombination:
            """Build a LotteryCombination with fixed bounds for tests."""

            return LotteryCombination(
                main=BoundCombination(values=main, start=1, end=50, count=3),
                bonus=BoundCombination(values=bonus, start=1, end=10, count=1),
            )

        data = {
            "period": "202401",
            "draw_date": "2024-01-15",
            "deadline_date": "2024-02-15",
            "combination": {"main": [5, 12, 23], "bonus": [7]},
            "numbers": [5, 12, 23, 7],
            "winning_ranks": [
                {"rank": 1, "winners": 2, "gain": 1_000_000.0},
                {"rank": 2, "winners": 10, "gain": 50_000.0},
            ],
        }

        record = DrawRecord.from_json(data, factory)

        assert record.period == "202401"
        assert record.draw_date == datetime.date(2024, 1, 15)
        assert record.deadline_date == datetime.date(2024, 2, 15)
        assert record.combination.components["main"].values == [5, 12, 23]
        assert record.combination.components["bonus"].values == [7]
        assert record.numbers == {"main": [5, 12, 23], "bonus": [7]}
        assert record.winning_ranks == [
            WinningRank(rank=1, winners=2, gain=1_000_000.0),
            WinningRank(rank=2, winners=10, gain=50_000.0),
        ]

    def test_draw_record_from_json_without_factory(self) -> None:
        """Test from_json falls back to LotteryCombination.from_json when no factory provided."""

        main = BoundCombination(values=[5, 12, 23], start=1, end=50, count=3)
        bonus = BoundCombination(values=[7], start=1, end=10, count=1)
        combination = LotteryCombination(main=main, bonus=bonus)
        data = {
            "period": "202402",
            "draw_date": "2024-02-15",
            "deadline_date": "2024-03-15",
            "combination": combination.to_json(),
            "numbers": combination.values,
            "winning_ranks": [],
        }

        record = DrawRecord.from_json(data)

        assert isinstance(record.combination, LotteryCombination)
        assert record.combination.values == combination.values
        assert record.period == "202402"

    def test_draw_record_from_json_raises_on_numbers_mismatch(self) -> None:
        """Test from_json raises ValueError when JSON numbers don't match the combination."""

        main = BoundCombination(values=[5, 12, 23], start=1, end=50, count=3)
        combination = LotteryCombination(main=main)
        data = {
            "period": "202403",
            "draw_date": "2024-03-15",
            "deadline_date": "2024-04-15",
            "combination": combination.to_json(),
            "numbers": [99, 99, 99],
            "winning_ranks": [],
        }

        with pytest.raises(ValueError):
            DrawRecord.from_json(data)

    def test_draw_record_to_dict_exports_all_fields(self) -> None:
        """Test to_dict returns all expected JSON fields."""

        draw_date = datetime.date(2024, 1, 15)
        deadline_date = datetime.date(2024, 2, 15)
        main = BoundCombination(values=[5, 12, 23], start=1, end=50, count=3)
        bonus = BoundCombination(values=[7], start=1, end=10, count=1)
        combination = LotteryCombination(main=main, bonus=bonus)
        record = DrawRecord(
            period="202401",
            draw_date=draw_date,
            deadline_date=deadline_date,
            combination=combination,
            numbers={"main": [5, 12, 23], "bonus": [7]},
            winning_ranks=[
                WinningRank(rank=1, winners=2, gain=1_000_000.0),
                WinningRank(rank=2, winners=10, gain=50_000.0),
            ],
        )

        result = record.to_dict()

        assert result == {
            "period": "202401",
            "draw_date": "2024-01-15",
            "deadline_date": "2024-02-15",
            "combination": combination.to_dict(),
            "numbers": combination.values,
            "winning_ranks": [
                {"rank": 1, "winners": 2, "gain": 1_000_000.0},
                {"rank": 2, "winners": 10, "gain": 50_000.0},
            ],
        }

    def test_draw_record_from_dict_with_factory(self) -> None:
        """Test from_dict builds a DrawRecord using a combination factory."""

        def factory(main: list, bonus: list) -> LotteryCombination:
            """Build a LotteryCombination with fixed bounds for tests."""

            return LotteryCombination(
                main=BoundCombination(values=main, start=1, end=50, count=3),
                bonus=BoundCombination(values=bonus, start=1, end=10, count=1),
            )

        data = {
            "period": "202401",
            "draw_date": "2024-01-15",
            "deadline_date": "2024-02-15",
            "combination": {"main": [5, 12, 23], "bonus": [7]},
            "numbers": [5, 12, 23, 7],
            "winning_ranks": [
                {"rank": 1, "winners": 2, "gain": 1_000_000.0},
                {"rank": 2, "winners": 10, "gain": 50_000.0},
            ],
        }

        record = DrawRecord.from_dict(data, factory)

        assert record.period == "202401"
        assert record.draw_date == datetime.date(2024, 1, 15)
        assert record.deadline_date == datetime.date(2024, 2, 15)
        assert record.combination.components["main"].values == [5, 12, 23]
        assert record.combination.components["bonus"].values == [7]
        assert record.numbers == {"main": [5, 12, 23], "bonus": [7]}
        assert record.winning_ranks == [
            WinningRank(rank=1, winners=2, gain=1_000_000.0),
            WinningRank(rank=2, winners=10, gain=50_000.0),
        ]

    def test_draw_record_from_dict_without_factory(self) -> None:
        """Test from_dict falls back to LotteryCombination.from_dict when no factory provided."""

        main = BoundCombination(values=[5, 12, 23], start=1, end=50, count=3)
        bonus = BoundCombination(values=[7], start=1, end=10, count=1)
        combination = LotteryCombination(main=main, bonus=bonus)
        data = {
            "period": "202402",
            "draw_date": "2024-02-15",
            "deadline_date": "2024-03-15",
            "combination": combination.to_dict(),
            "numbers": combination.values,
            "winning_ranks": [],
        }

        record = DrawRecord.from_dict(data)

        assert isinstance(record.combination, LotteryCombination)
        assert record.combination.values == combination.values
        assert record.period == "202402"

    def test_draw_record_from_dict_raises_on_numbers_mismatch(self) -> None:
        """Test from_dict raises ValueError when JSON numbers don't match the combination."""

        main = BoundCombination(values=[5, 12, 23], start=1, end=50, count=3)
        combination = LotteryCombination(main=main)
        data = {
            "period": "202403",
            "draw_date": "2024-03-15",
            "deadline_date": "2024-04-15",
            "combination": combination.to_dict(),
            "numbers": [99, 99, 99],
            "winning_ranks": [],
        }

        with pytest.raises(ValueError):
            DrawRecord.from_dict(data)


class TestFoundCombination:
    """Tests for FoundCombination model."""

    def _make_record(self) -> DrawRecord:
        """Build a simple DrawRecord for use in tests."""

        main = BoundCombination(values=[5, 12, 23], start=1, end=50, count=3)
        combination = LotteryCombination(main=main)
        return DrawRecord(
            period="202401",
            draw_date=datetime.date(2024, 1, 15),
            deadline_date=datetime.date(2024, 2, 15),
            combination=combination,
            numbers={"main": [5, 12, 23]},
            winning_ranks=[WinningRank(rank=1, winners=1, gain=500_000.0)],
        )

    def _make_match(self) -> CompoundCombination:
        """Build a simple CompoundCombination for use in tests."""

        return CompoundCombination(main=[5, 12], bonus=[])

    def test_found_combination_to_csv(self) -> None:
        """Test to_csv merges DrawRecord CSV data with the found rank."""

        record = self._make_record()
        match = self._make_match()
        found = FoundCombination(record=record, rank=7, match=match)

        result = found.to_csv()

        assert result == {**record.to_csv(), "rank": 7, "match": match.to_string()}

    def test_found_combination_to_json(self) -> None:
        """Test to_json returns the same payload as to_dict."""

        record = self._make_record()
        match = self._make_match()
        found = FoundCombination(record=record, rank=42, match=match)

        assert found.to_json() == found.to_dict()

    def test_found_combination_to_dict(self) -> None:
        """Test to_dict returns record as JSON dict and rank."""

        record = self._make_record()
        match = self._make_match()
        found = FoundCombination(record=record, rank=42, match=match)

        result = found.to_dict()

        assert result == {"record": record.to_dict(), "rank": 42, "match": match.dump()}

    def test_found_combination_from_csv_with_factory(self) -> None:
        """Test from_csv builds the record with the provided combination factory."""

        def factory(
            main: CombinationInputOrRank,
            bonus: CombinationInputOrRank,
        ) -> LotteryCombination:
            """Build a LotteryCombination with fixed bounds for tests."""

            if isinstance(main, list):
                main = {"values": main, "rank": None}
            if isinstance(bonus, list):
                bonus = {"values": bonus, "rank": None}

            return LotteryCombination(
                main=BoundCombination(
                    values=main["values"],
                    rank=main["rank"],
                    start=1,
                    end=50,
                    count=3,
                ),
                bonus=BoundCombination(
                    values=bonus["values"],
                    rank=bonus["rank"],
                    start=1,
                    end=10,
                    count=1,
                ),
            )

        data = {
            "period": "202402",
            "draw_date": "2024-02-10",
            "deadline_date": "2024-03-10",
            "main_1": "3",
            "main_2": "11",
            "main_3": "5",
            "bonus_1": "9",
            "main_rank": "5",
            "bonus_rank": "1",
            "rank_1_winners": "2",
            "rank_1_gain": "1234.5",
            "rank": "9",
            "match": "main: [3, 11, 5]  bonus: [9]",
        }

        found = FoundCombination.from_csv(data, combination_factory=factory)

        assert found.rank == 9
        assert found.match == CompoundCombination(main=[3, 11, 5], bonus=[9])
        assert found.record.numbers == {"main": [3, 11, 5], "bonus": [9]}
        assert found.record.combination.components["main"].values == [3, 5, 11]
        assert found.record.combination.components["main"].rank == 5
        assert found.record.combination.components["bonus"].rank == 1
        assert found.record.winning_ranks == [WinningRank(rank=1, winners=2, gain=1234.5)]

    def test_found_combination_from_csv_without_factory(self) -> None:
        """Test from_csv falls back to DrawRecord.from_csv when no factory provided."""

        data = {
            "period": "202403",
            "draw_date": "2024-03-10",
            "deadline_date": "2024-04-10",
            "main_1": 8,
            "main_2": 14,
            "rank_1_winners": 2,
            "rank_1_gain": 100.0,
            "rank": 5,
            "match": "main: [8, 14]",
        }

        found = FoundCombination.from_csv(data)

        assert found.rank == 5
        assert found.match == CompoundCombination(main=[8, 14], bonus=[])
        assert found.record.numbers == {"main": [8, 14]}
        assert isinstance(found.record.combination, LotteryCombination)
        assert found.record.combination.components == {}
        assert found.record.winning_ranks == [WinningRank(rank=1, winners=2, gain=100.0)]

    def test_found_combination_from_json_with_factory(self) -> None:
        """Test from_json forwards combination_factory to DrawRecord.from_dict."""

        def factory(main: list[int], bonus: list[int]) -> LotteryCombination:
            """Build a LotteryCombination with fixed bounds for tests."""

            return LotteryCombination(
                main=BoundCombination(values=main, start=1, end=50, count=3),
                bonus=BoundCombination(values=bonus, start=1, end=10, count=1),
            )

        data = {
            "record": {
                "period": "202405",
                "draw_date": "2024-05-03",
                "deadline_date": "2024-06-03",
                "combination": {"main": [1, 2, 3], "bonus": [4]},
                "numbers": [1, 2, 3, 4],
                "winning_ranks": [{"winners": 1, "gain": 10.0}],
            },
            "rank": 3,
            "match": {"main": [5, 12], "bonus": []},
        }

        found = FoundCombination.from_json(data, combination_factory=factory)

        assert found.rank == 3
        assert found.match == CompoundCombination(main=[5, 12], bonus=[])
        assert found.record.period == "202405"
        assert found.record.combination.values == [1, 2, 3, 4]
        assert found.record.winning_ranks == [WinningRank(rank=1, winners=1, gain=10.0)]

    def test_found_combination_from_dict_with_factory(self) -> None:
        """Test from_dict forwards combination_factory to DrawRecord.from_dict."""

        def factory(main: list[int], bonus: list[int]) -> LotteryCombination:
            """Build a LotteryCombination with fixed bounds for tests."""

            return LotteryCombination(
                main=BoundCombination(values=main, start=1, end=50, count=3),
                bonus=BoundCombination(values=bonus, start=1, end=10, count=1),
            )

        data = {
            "record": {
                "period": "202401",
                "draw_date": "2024-01-15",
                "deadline_date": "2024-02-15",
                "combination": {"main": [5, 12, 23], "bonus": [7]},
                "numbers": [5, 12, 23, 7],
                "winning_ranks": [{"rank": 1, "winners": 2, "gain": 1_000_000.0}],
            },
            "rank": 8,
            "match": {"main": [5, 12], "bonus": []},
        }

        found = FoundCombination.from_dict(data, combination_factory=factory)

        assert found.rank == 8
        assert found.match == CompoundCombination(main=[5, 12], bonus=[])
        assert found.record.combination.components["main"].values == [5, 12, 23]
        assert found.record.combination.components["bonus"].values == [7]
        assert found.record.winning_ranks == [WinningRank(rank=1, winners=2, gain=1_000_000.0)]

    def test_found_combination_from_dict(self) -> None:
        """Test from_dict restores the FoundCombination from a dictionary."""

        record = self._make_record()
        match = self._make_match()
        data = {"record": record.to_json(), "rank": 42, "match": {"main": [5, 12], "bonus": []}}

        found = FoundCombination.from_dict(data)

        assert found.rank == 42
        assert found.match == match
        assert found.record.period == record.period
        assert found.record.draw_date == record.draw_date
        assert found.record.combination.values == record.combination.values
        assert found.record.winning_ranks == record.winning_ranks

    def test_found_combination_serialization_roundtrip(self) -> None:
        """Test to_dict / from_dict roundtrip preserves all fields."""

        record = self._make_record()
        match = self._make_match()
        original = FoundCombination(record=record, rank=7, match=match)

        restored = FoundCombination.from_dict(original.to_dict())

        assert restored.rank == original.rank
        assert restored.match == original.match
        assert restored.record.period == original.record.period
        assert restored.record.draw_date == original.record.draw_date
        assert restored.record.deadline_date == original.record.deadline_date
        assert restored.record.combination.values == original.record.combination.values
        assert restored.record.winning_ranks == original.record.winning_ranks
