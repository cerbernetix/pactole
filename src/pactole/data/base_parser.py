"""Base classes for data parsers."""

from typing import Any

from ..combinations import CombinationFactory, LotteryCombination
from .models import DrawRecord


class BaseParser:
    """A base class for data parsers.

    Args:
        combination_factory (CombinationFactory | LotteryCombination | Any): A factory function
            or class to create a combination instance. If None, a default LotteryCombination
            instance will be used. Default is None.

    Examples:
        >>> class MyParser(BaseParser):
        ...     def __call__(self, data: dict) -> DrawRecord:
        ...         # Implement parsing logic here
        ...         return DrawRecord(...)
        >>> parser = MyParser()
        >>> record = parser({
        ...     "date": "2022-01-15",
        ...     "deadline": "2022-02-15",
        ...     "main_1": 12,
        ...     "main_2": 5,
        ...     "main_3": 23,
        ...     "bonus_1": 7,
        ... })
        >>> print(record)
        DrawRecord(
            period='202201',
            draw_date=datetime.date(2022, 1, 15),
            deadline_date=datetime.date(2022, 2, 15),
            combination=...,
            numbers=...,
            winning_ranks=...)
    """

    _combination_factory: CombinationFactory

    def __init__(
        self,
        combination_factory: CombinationFactory | LotteryCombination | Any = None,
    ) -> None:
        self._combination_factory = LotteryCombination.get_combination_factory(combination_factory)

    def __call__(self, data: dict) -> DrawRecord:
        """Parse a line of data and return a DrawRecord.

        Args:
            data (dict): A dictionary representing a line of data.

        Returns:
            DrawRecord: The record parsed from the line of data.

        Example:
            >>> class SimpleParser(BaseParser):
            ...     def __call__(self, data: dict) -> DrawRecord:
            ...         return DrawRecord(
            ...             period=data["date"][:7].replace("-", ""),
            ...             draw_date=datetime.date.fromisoformat(data["date"]),
            ...             deadline_date=datetime.date.fromisoformat(data["deadline"]),
            ...             combination=None,
            ...             numbers={},
            ...             winning_ranks=[],
            ...         )
            >>> parser = SimpleParser()
            >>> record = parser({"date": "2022-01-15", "deadline": "2022-02-15", ... }, factory)
            >>> print(record)
            DrawRecord(
                period='202201',
                draw_date=datetime.date(2022, 1, 15),
                deadline_date=datetime.date(2022, 2, 15),
                combination=None,
                numbers={},
                winning_ranks=[])
        """
        raise NotImplementedError("Subclasses must implement method __call__.")

    @property
    def combination_factory(self) -> CombinationFactory:
        """Get the combination factory.

        Returns:
            CombinationFactory: The combination factory used by this parser.

        Example:
            >>> parser = BaseParser()
            >>> factory = parser.combination_factory
            >>> print(factory)
            <function LotteryCombination.get_combination at 0x...>
        """
        return self._combination_factory
