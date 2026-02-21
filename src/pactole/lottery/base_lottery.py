"""Base class for lottery implementations."""

from datetime import date
from typing import Iterator

from ..combinations import (
    CombinationFactory,
    CombinationInput,
    CombinationInputOrRank,
    CombinationRank,
    LotteryCombination,
)
from ..data import BaseProvider, DrawRecord, FoundCombination
from ..utils import Day, DrawDays, Weekday


class BaseLottery:
    """A base class for lottery implementations.


    Args:
        provider (BaseProvider): The data provider to use for fetching lottery results.

    Examples:
        >>> provider = BaseProvider(
        ...     resolver=MyResolver(),
        ...     parser=MyParser(),
        ...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
        ...     combination_factory=EuroMillionsCombination,
        ... )
        >>> lottery = BaseLottery(provider)
        >>> lottery.draw_days
        DrawDays(days=[<Weekday.MONDAY: 0>, <Weekday.THURSDAY: 3>])
        >>> lottery.combination_factory
        <class 'pactole.combinations.EuroMillionsCombination'>
        >>> lottery.combination_factory(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        >>> lottery.get_next_draw_date(date(2024, 6, 5))
        datetime.date(2024, 6, 6)
        >>> combination = EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9])
        >>> list(lottery.find_records(combination))
        [DrawRecord(
            period='202001',
            draw_date=date(2020, 1, 1),
            deadline_date=date(2020, 1, 15),
            combination=EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9]),
            numbers={'number': [5, 12, 23, 34, 45], 'star': [2, 9]},
             winning_ranks=[WinningRank(rank=1, winners=1, gain=1000000.0), ...]
        ), ...]
    """

    _provider: BaseProvider

    def __init__(self, provider: BaseProvider) -> None:
        self._provider = provider

    @property
    def draw_days(self) -> DrawDays:
        """Return the DrawDays instance associated with this lottery.

        Returns:
            DrawDays: The DrawDays instance associated with this lottery.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
            ... )
            >>> lottery = BaseLottery(provider)
            >>> lottery.draw_days
            DrawDays(days=[<Weekday.MONDAY: 0>, <Weekday.THURSDAY: 3>])
        """
        return self._provider.draw_days

    @property
    def combination_factory(self) -> CombinationFactory:
        """Return the combination factory associated with this lottery.

        Returns:
            CombinationFactory: The combination factory associated with this lottery.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
            ...     combination_factory=EuroMillionsCombination,
            ... )
            >>> lottery = BaseLottery(provider)
            >>> lottery.combination_factory
            <class 'pactole.combinations.EuroMillionsCombination'>
            >>> lottery.combination_factory(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
            EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        """
        return self._provider.combination_factory

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
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
            ... )
            >>> lottery = BaseLottery(provider)
            >>> lottery.get_last_draw_date(date(2024, 6, 5))
            datetime.date(2024, 6, 3)
        """
        return self._provider.draw_days.get_last_draw_date(from_date=from_date, closest=closest)

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
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
            ... )
            >>> lottery = BaseLottery(provider)
            >>> lottery.get_next_draw_date(date(2024, 6, 5))
            datetime.date(2024, 6, 6)
        """
        return self._provider.draw_days.get_next_draw_date(from_date=from_date, closest=closest)

    def generate(self, n: int = 1, partitions: int = 1) -> list[LotteryCombination]:
        """Generate a list of random lottery combinations.

        Args:
            n (int, optional): The number of combinations to generate. Defaults to 1.
            partitions (int, optional): The number of partitions to use when generating
                combinations. Defaults to 1.

        Returns:
            list[LotteryCombination]: A list of generated lottery combinations.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
            ...     combination_factory=EuroMillionsCombination,
            ... )
            >>> lottery = BaseLottery(provider)
            >>> lottery.generate(n=2)
            [EuroMillionsCombination(numbers=[...], stars=[...]),
             EuroMillionsCombination(numbers=[...], stars=[...])]
        """
        return self._provider.combination_factory().generate(n=n, partitions=partitions)

    def get_combination(self, **components: CombinationInputOrRank) -> LotteryCombination:
        """Create a lottery combination from the provided components.

        Args:
            **components (CombinationInputOrRank): The components of the combination, provided as
                keyword arguments. The keys should correspond to the component names defined in the
                combination factory.

        Returns:
            LotteryCombination: A lottery combination created from the provided components.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
            ...     combination_factory=EuroMillionsCombination,
            ... )
            >>> lottery = BaseLottery(provider)
            >>> lottery.get_combination(numbers=[5, 12, 23, 34, 45], stars=[2, 9])
            EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9])
        """
        return self._provider.combination_factory(**components)

    def count(self) -> int:
        """Return the total number of lottery records available in the cache.

        Returns:
            int: The total number of lottery records.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
            ...     combination_factory=EuroMillionsCombination,
            ... )
            >>> lottery = BaseLottery(provider)
            >>> lottery.count()
            1234
        """
        return len(self._provider.load())

    def dump(self, force: bool = False) -> list[dict]:
        """Dump the cached data as a list of dictionaries.

        Args:
            force (bool, optional): If True, forces a refresh of the cache before dumping.
                Defaults to False.

        Returns:
            list[dict]: A list of dictionaries representing the cached data.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
            ...     combination_factory=EuroMillionsCombination,
            ... )
            >>> lottery = BaseLottery(provider)
            >>> lottery.dump()
            [
                {
                    'period': '202201',
                    'draw_date': '2022-01-15',
                    'deadline_date': '2022-02-15',
                    'numbers_1': 12,
                    'numbers_2': 5,
                    'numbers_3': 23,
                    'numbers_4': 34,
                    'numbers_5': 45,
                    'stars_1': 7,
                    'stars_2': 9,
                    'numbers_rank': 1128527,
                    'stars_rank': 34,
                    'rank_1_winners': 2,
                    'rank_1_gain': 1000000.0,
                    'rank_2_winners': 10,
                    'rank_2_gain': 50000.0
                },
                ...
            ]
        """
        return [record.to_dict() for record in self._provider.load(force=force)]

    def get_records(self, force: bool = False) -> Iterator[DrawRecord]:
        """Get the cached data as an iterator of DrawRecord instances.

        If the cache is missing or outdated, it will be refreshed before returning the data.

        Args:
            force (bool, optional): If True, forces a refresh of the cache before getting the data.
                Defaults to False.

        Returns:
            Iterator[DrawRecord]: An iterator of DrawRecord instances representing the cached data.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
            ...     combination_factory=EuroMillionsCombination,
            ...     cache_name="euromillions"
            ... )
            >>> lottery = BaseLottery(provider)
            >>> list(lottery.get_records())
            [DrawRecord(
                period='202001',
                draw_date=date(2020, 1, 1),
                deadline_date=date(2020, 1, 15),
                combination=EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9]),
                numbers={'number': [5, 12, 23, 34, 45], 'star': [2, 9]},
                winning_ranks=[WinningRank(rank=1, winners=1, gain=1000000.0), ...]
            ), ...]
        """
        yield from self._provider.load(force=force)

    def find_records(
        self,
        combination: CombinationInput | LotteryCombination | None = None,
        target_rank: CombinationRank | None = None,
        strict: bool = False,
        force: bool = False,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> Iterator[FoundCombination]:
        """Find lottery results based on a query.

        Args:
            combination (CombinationInput | LotteryCombination | None, optional): A combination to
                search for. Defaults to None.
            target_rank (CombinationRank | None, optional): If provided, only results with the
                specified winning rank will be returned. Defaults to None.
            strict (bool, optional): If True, the search will be strict, meaning that only
                records that exactly match the provided combination and target rank will be
                returned. If False, the search will be more flexible, allowing for partial matches
                as long as a winning rank is found. Defaults to False.
            force (bool, optional): If True, forces a refresh of the cache before searching for
                results. Defaults to False.
            **components (CombinationInputOrRank | LotteryCombination): Additional
                components of the combination to search for, provided as keyword arguments.
                The keys should correspond to the component names defined in the combination
                factory.

        Returns:
            Iterator[FoundCombination]: An iterator of FoundCombination instances matching the
                search criteria.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
            ...     combination_factory=EuroMillionsCombination,
            ...     cache_name="euromillions",
            ... )
            >>> combination = EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9])
            >>> lottery = BaseLottery(provider)
            >>> list(lottery.find_records(combination))
            [FoundCombination(
                record=DrawRecord(
                    period='202001',
                    draw_date=date(2020, 1, 1),
                    deadline_date=date(2020, 1, 15),
                    combination=EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9]),
                    numbers={'number': [5, 12, 23, 34, 45], 'star': [2, 9]},
                    winning_ranks=[WinningRank(rank=1, winners=1, gain=1000000.0), ...]
                ),
                rank=1
            ), ...]
        """
        combination = self._provider.combination_factory(combination, **components)
        if target_rank is None and not strict:
            target_rank = combination.min_winning_rank
        if target_rank is not None:
            return self._find_records_by_winning_rank(
                combination,
                target_rank,
                strict=strict,
                force=force,
            )
        return self._find_records_by_combination(combination, force=force)

    def _find_records_by_combination(
        self,
        combination: LotteryCombination,
        force: bool = False,
    ) -> Iterator[FoundCombination]:
        """Find lottery results based on a combination."""
        record: DrawRecord
        for record in self._provider.load(force=force):
            if record.combination.includes(combination):
                winning_rank = record.combination.get_winning_rank(combination)
                yield FoundCombination(record=record, rank=winning_rank)

    def _find_records_by_winning_rank(
        self,
        combination: LotteryCombination,
        target_rank: CombinationRank,
        strict: bool = False,
        force: bool = False,
    ) -> Iterator[FoundCombination]:
        """Find lottery results based on a combination and an optional target rank."""
        record: DrawRecord
        if strict:

            def matches(winning_rank: CombinationRank) -> bool:
                return winning_rank == target_rank
        else:

            def matches(winning_rank: CombinationRank) -> bool:
                return winning_rank is not None and winning_rank >= target_rank

        for record in self._provider.load(force=force):
            winning_rank = record.combination.get_winning_rank(combination)
            if matches(winning_rank):
                yield FoundCombination(record=record, rank=winning_rank)
