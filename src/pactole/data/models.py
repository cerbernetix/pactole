"""Data models for lottery draw records and winning ranks."""

from __future__ import annotations

import datetime
import re
from dataclasses import dataclass

from ..combinations import CombinationFactory, CombinationInputWithRank, LotteryCombination
from ..utils import get_float, get_int

RE_NUMBER = re.compile(r"^(?P<component>\w+)_(?P<index>\d+)$")
RE_RANK = re.compile(r"^(?P<component>\w+)_rank$")
RE_WINNERS = re.compile(r"^rank_(?P<rank>\d+)_winners$")
RE_GAIN = re.compile(r"^rank_(?P<rank>\d+)_gain$")


@dataclass
class WinningRank:
    """A class representing a winning rank in a lottery draw."""

    rank: int
    """Rank of the winning combination (1 for jackpot, 2 for second prize, etc.)."""

    winners: int
    """Number of winners for this rank."""

    gain: float
    """Gain amount for this rank (can be zero for non-winning ranks)."""


@dataclass
class DrawRecord:
    """A class representing a record of a lottery draw."""

    period: str
    """Period identifier of the draw (e.g., '202201' for a lottery started in January 2022)."""

    draw_date: datetime.date
    """Date of the draw."""

    deadline_date: datetime.date
    """Deadline date for gain collection."""

    combination: LotteryCombination
    """The winning combination of the draw."""

    numbers: dict[str, list[int]]
    """A dictionary of number components and their corresponding lists of values in the draw."""

    winning_ranks: list[WinningRank]
    """A list of winning ranks for the draw, ordered by rank."""

    def to_dict(self) -> dict:
        """Convert the DrawRecord instance to a dictionary.

        Returns:
            dict: A dictionary representation of the DrawRecord instance.

        Example:
            >>> record = DrawRecord(
            ...     period="202201",
            ...     draw_date=datetime.date(2022, 1, 15),
            ...     deadline_date=datetime.date(2022, 2, 15),
            ...     combination=LotteryCombination(components={"main": ..., "bonus": ...}),
            ...     numbers={"main": [12, 5, 23], "bonus": [7]},
            ...     winning_ranks=[
            ...         WinningRank(rank=1, winners=2, gain=1000000.0),
            ...         WinningRank(rank=2, winners=10, gain=50000.0)],
            ...     ]
            ... )
            >>> record.to_dict()
            {'period': '202201',
             'draw_date': '2022-01-15',
             'deadline_date': '2022-02-15',
             'main_1': 12,
             'main_2': 5,
             'main_3': 23,
             'bonus_1': 7,
             'main_rank': 1,
             'bonus_rank': 2,
             'combination_rank': 1,
             'rank_1_winners': 2,
             'rank_1_gain': 1000000.0,
             'rank_2_winners': 10,
             'rank_2_gain': 50000.0}
        """
        data = {
            "period": self.period,
            "draw_date": self.draw_date.isoformat(),
            "deadline_date": self.deadline_date.isoformat(),
        }

        for key, values in self.numbers.items():
            for i, value in enumerate(values, start=1):
                data[f"{key}_{i}"] = value

        for key, component in self.combination.components.items():
            data[f"{key}_rank"] = component.rank
        data["combination_rank"] = self.combination.rank

        for winning_rank in self.winning_ranks:
            data[f"rank_{winning_rank.rank}_winners"] = winning_rank.winners
            data[f"rank_{winning_rank.rank}_gain"] = winning_rank.gain

        return data

    @staticmethod
    def from_dict(data: dict, combination_factory: CombinationFactory | None = None) -> DrawRecord:
        """Create a DrawRecord instance from a dictionary.

        Args:
            data (dict): A dictionary containing the draw record data.
            combination_factory (CombinationFactory | None): A factory function or class to create a
                combination instance. If None, a default LotteryCombination instance will be used.
                Default is None.

        Returns:
            DrawRecord: An instance of DrawRecord created from the input dictionary.

        Example:
            >>> data = {
            ...     "period": "202201",
            ...     "draw_date": "2022-01-15",
            ...     "deadline_date": "2022-02-15",
            ...     "main_1": 12,
            ...     "main_2": 5,
            ...     "main_3": 23,
            ...     "bonus_1": 7,
            ...     "main_rank": 1,
            ...     "bonus_rank": 2,
            ...     "combination_rank": 1,
            ...     "rank_1_winners": 2,
            ...     "rank_1_gain": 1000000.0,
            ...     "rank_2_winners": 10,
            ...     "rank_2_gain": 50000.0,
            ... }
            >>> record = DrawRecord.from_dict(data)
            >>> print(record)
            DrawRecord(
                period='202201',
                draw_date=datetime.date(2022, 1, 15),
                deadline_date=datetime.date(2022, 2, 15),
                combination=LotteryCombination(components={'main': ..., 'bonus': ...}),
                numbers={'main': [12, 5, 23], 'bonus': [7]},
                winning_ranks=[
                    WinningRank(rank=1, winners=2, gain=1000000.0),
                    WinningRank(rank=2, winners=10, gain=50000.0)
                ]
            )
        """
        period = data.get("period", "")
        draw_date = datetime.date.fromisoformat(data.get("draw_date", "1970-01-01"))
        deadline_date = datetime.date.fromisoformat(data.get("deadline_date", "1970-01-01"))

        numbers = {}
        ranks = {}
        winners = {}
        gains = {}

        known = set(["period", "draw_date", "deadline_date"])
        for key, value in data.items():
            if key in known:
                continue

            if match := RE_NUMBER.match(key):
                component_name = match.group("component")
                numbers.setdefault(component_name, []).append(get_int(value))
                continue

            if match := RE_RANK.match(key):
                component_name = match.group("component")
                ranks[component_name] = get_int(value)
                continue

            if match := RE_WINNERS.match(key):
                rank_number = get_int(match.group("rank"))
                winners[rank_number] = get_int(value)
                continue

            if match := RE_GAIN.match(key):
                rank_number = get_int(match.group("rank"))
                gains[rank_number] = get_float(value)
                continue

        if callable(combination_factory):
            combination = combination_factory(
                **{
                    component_name: CombinationInputWithRank(
                        values=values, rank=ranks.get(component_name)
                    )
                    for component_name, values in numbers.items()
                }
            )
        else:
            combination = LotteryCombination()

        winning_ranks = []
        for rank in sorted(winners.keys()):
            winning_ranks.append(
                WinningRank(rank=rank, winners=winners[rank], gain=gains.get(rank, 0.0))
            )

        return DrawRecord(
            period=period,
            draw_date=draw_date,
            deadline_date=deadline_date,
            combination=combination,
            numbers=numbers,
            winning_ranks=winning_ranks,
        )
