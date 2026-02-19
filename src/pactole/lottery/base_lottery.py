"""Base class for lottery implementations."""

from datetime import date
from typing import Iterable

from ..combinations import (
    CombinationFactory,
    CombinationInputOrRank,
    LotteryCombination,
)
from ..utils import Day, DrawDays, Weekday


class BaseLottery:
    """A base class for lottery implementations.


    Args:
        draw_days (DrawDays | Iterable[Day | Weekday], optional): An instance of DrawDays or an
            iterable of Day or Weekday representing the draw days of the lottery.
            Defaults to an empty tuple.
        combination_factory (CombinationFactory | None): A factory function or class to create a
            combination instance. If None, a default LotteryCombination instance will be used.
            Default is None.

    Examples:
        >>> lottery = BaseLottery(
        ...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
        ...     combination_factory=EuroMillionsCombination,
        ... )
        >>> lottery.draw_days
        DrawDays(days=[<Weekday.MONDAY: 0>, <Weekday.THURSDAY: 3>])
        >>> lottery.combination_factory
        <class 'pactole.combinations.EuroMillionsCombination'>
        >>> lottery.combination_factory(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
    """

    _draw_days: DrawDays
    _combination_factory: CombinationFactory

    def __init__(
        self,
        draw_days: DrawDays | Iterable[Day | Weekday] = (),
        combination_factory: CombinationFactory | None = None,
    ) -> None:
        if not callable(combination_factory):
            combination_factory = LotteryCombination().get_combination
        self._combination_factory = combination_factory

        if not isinstance(draw_days, DrawDays):
            draw_days = DrawDays(draw_days)
        self._draw_days = draw_days

    @property
    def draw_days(self) -> DrawDays:
        """Return the DrawDays instance associated with this lottery.

        Returns:
            DrawDays: The DrawDays instance associated with this lottery.

        Examples:
            >>> lottery = BaseLottery(draw_days=[Weekday.MONDAY, Weekday.THURSDAY])
            >>> lottery.draw_days
            DrawDays(days=[<Weekday.MONDAY: 0>, <Weekday.THURSDAY: 3>])
        """
        return self._draw_days

    @property
    def combination_factory(self) -> CombinationFactory:
        """Return the combination factory associated with this lottery.

        Returns:
            CombinationFactory: The combination factory associated with this lottery.

        Examples:
            >>> lottery = BaseLottery(combination_factory=EuroMillionsCombination)
            >>> lottery.combination_factory
            <class 'pactole.combinations.EuroMillionsCombination'>
            >>> lottery.combination_factory(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
            EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        """
        return self._combination_factory

    def get_last_draw_date(
        self,
        from_date: Day | Weekday | None = None,
        closest: bool = True,
    ) -> date:
        """Return the date of the last lottery draw.

        Args:
            from_date (Day | Weekday | None, optional): The starting date.

                A timestamp can be provided as an integer or float representing
                seconds since the epoch. When a string is provided, it must be in the ISO format
                'YYYY-MM-DD'. Finally, a date object can be provided directly.

                Defaults to None.

        Returns:
            date: The date of the last lottery draw.

        Raises:
            TypeError: If the provided date is not a string, timestamp, or date object.
            ValueError: If the string is not a valid date in ISO format.

        Examples:
            >>> lottery = BaseLottery(draw_days=[Weekday.MONDAY, Weekday.THURSDAY])
            >>> lottery.get_last_draw_date(date(2024, 6, 5))
            datetime.date(2024, 6, 3)
        """
        return self._draw_days.get_last_draw_date(from_date=from_date, closest=closest)

    def get_next_draw_date(
        self,
        from_date: Day | Weekday | None = None,
        closest: bool = True,
    ) -> date:
        """Return the date of the next lottery draw.

        Args:
            from_date (Day | Weekday | None, optional): The starting date.

                A timestamp can be provided as an integer or float representing
                seconds since the epoch. When a string is provided, it must be in the ISO format
                'YYYY-MM-DD'. Finally, a date object can be provided directly.

                Defaults to None.

        Returns:
            date: The date of the next lottery draw.

        Raises:
            TypeError: If the provided date is not a string, timestamp, or date object.
            ValueError: If the string is not a valid date in ISO format.

        Examples:
            >>> lottery = BaseLottery(draw_days=[Weekday.MONDAY, Weekday.THURSDAY])
            >>> lottery.get_next_draw_date(date(2024, 6, 5))
            datetime.date(2024, 6, 6)
        """
        return self._draw_days.get_next_draw_date(from_date=from_date, closest=closest)

    def generate(self, n: int = 1, partitions: int = 1) -> list[LotteryCombination]:
        """Generate a list of random lottery combinations.

        Args:
            n (int, optional): The number of combinations to generate. Defaults to 1.
            partitions (int, optional): The number of partitions to use when generating
                combinations. Defaults to 1.

        Returns:
            list[LotteryCombination]: A list of generated lottery combinations.

        Examples:
            >>> lottery = BaseLottery(combination_factory=EuroMillionsCombination)
            >>> lottery.generate(n=2)
            [EuroMillionsCombination(numbers=[...], stars=[...]),
             EuroMillionsCombination(numbers=[...], stars=[...])]
        """
        return self._combination_factory().generate(n=n, partitions=partitions)

    def get_combination(self, **components: CombinationInputOrRank) -> LotteryCombination:
        """Create a lottery combination from the provided components.

        Args:
            **components (CombinationInputOrRank): The components of the combination, provided as
                keyword arguments. The keys should correspond to the component names defined in the
                combination factory.

        Returns:
            LotteryCombination: A lottery combination created from the provided components.

        Examples:
            >>> lottery = BaseLottery(combination_factory=EuroMillionsCombination)
            >>> lottery.get_combination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
            EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        """
        return self._combination_factory(**components)
