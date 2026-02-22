"""Unit tests for data models."""

from __future__ import annotations

import datetime

from pactole.combinations import BoundCombination, CombinationInputWithRank, LotteryCombination
from pactole.data import DrawRecord, WinningRank


class TestDrawRecord:
    """Tests for data model helpers."""

    def test_draw_record_to_dict_exports_fields(self) -> None:
        """Test to_dict returns all expected fields."""

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

        result = record.to_dict()

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

    def test_draw_record_from_dict_builds_components_and_ranks(self) -> None:
        """Test from_dict builds numbers and winning ranks with a factory."""

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

        record = DrawRecord.from_dict(data, factory)

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

    def test_draw_record_from_dict_defaults_combination(self) -> None:
        """Test from_dict falls back to an empty LotteryCombination."""

        data = {
            "period": "202403",
            "draw_date": "2024-03-10",
            "deadline_date": "2024-04-10",
            "main_1": 8,
            "main_2": 14,
            "rank_1_winners": 2,
            "rank_1_gain": 100.0,
        }

        record = DrawRecord.from_dict(data, object())

        assert isinstance(record.combination, LotteryCombination)
        assert not record.combination.components
        assert record.numbers == {"main": [8, 14]}
        assert record.winning_ranks == [WinningRank(rank=1, winners=2, gain=100.0)]
