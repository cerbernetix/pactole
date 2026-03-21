"""Module for Lottery combination representation and manipulation."""

from __future__ import annotations

from functools import cached_property
from math import prod
from typing import Any

from .combination import (
    BoundCombination,
    CombinationInput,
    CombinationInputOrRank,
    CombinationRank,
    generate,
)
from .compound_combination import (
    RE_COMPONENT,
    RE_NUMBER,
    CombinationFactory,
    CombinationWinningRanks,
    CompoundCombination,
)

__all__ = ["LotteryCombination", "CombinationWinningRanks"]


class LotteryCombination(CompoundCombination):
    """Class representing a Lottery combination.

    A Lottery combination is a compound combination that can consist of multiple components
    (e.g., main numbers, bonus numbers). Components are built from BoundCombination instances,
    which provide capacity and rank information.

    Args:
        combination (LotteryCombination | None): The combination to copy from.
        winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
            initializes an empty mapping.
        **components (BoundCombination): The components of the combination.

    Raises:
        TypeError: If any component is not an instance of BoundCombination.

    Examples:
        >>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
        >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
        >>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
        >>> lottery_comb = LotteryCombination(
        ...     main=main_numbers,
        ...     bonus=bonus_number,
        ...     winning_ranks=winning_ranks
        ... )
        >>> lottery_comb.components
        {'main': BoundCombination(...), 'bonus': BoundCombination(...)}
        >>> lottery_comb.values
        [1, 2, 3, 4, 5, 6]
    """

    def __init__(
        self,
        combination: LotteryCombination | None = None,
        *,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: BoundCombination,
    ) -> None:
        for component in components.values():
            if not isinstance(component, BoundCombination):
                raise TypeError("All components must be instances of BoundCombination.")
        super().__init__(combination, winning_ranks=winning_ranks, **components)

    @cached_property
    def rank(self) -> CombinationRank:
        """Get the lexicographic rank of the combination.

        The rank is computed as a cross-product encoding of component ranks: each component's
        rank is weighted by the product of the total combinations of all subsequent components.

        Returns:
            CombinationRank: The lexicographic rank of the combination.

        Examples:
            >>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb = LotteryCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> lottery_comb.rank
            1234567
        """
        rank = 0
        multiplier = 1
        for component in reversed(self._components.values()):
            rank += component.rank * multiplier
            multiplier *= component.combinations
        return rank

    @cached_property
    def count(self) -> int:
        """Return the total capacity (count) of the combination.

        Unlike length (which counts actual values), count sums each component's max capacity
        (its count attribute), giving the total number of slots available.

        Returns:
            int: The total count.

        Examples:
            >>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb = LotteryCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> lottery_comb.count
            6
        """
        return sum(component.count for component in self._components.values())

    @property
    def combinations(self) -> int:
        """Return the total number of possible combinations.

        Returns:
            int: The total number of combinations, or 0 if empty.

        Examples:
            >>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb = LotteryCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> lottery_comb.combinations
            21187600
        """
        if not self._components:
            return 0
        return prod(component.combinations for component in self._components.values())

    @staticmethod
    def get_combination_factory(
        combination_factory: CombinationFactory | LotteryCombination | Any,
    ) -> CombinationFactory:
        """Get the combination factory.

        It checks that the provided combination_factory is a callable, and if not, it returns a
        default factory from LotteryCombination, which will produce combinations with no
        components and no winning ranks.

        An instance of a LotteryCombination can be used to produce a factory.

        Args:
            combination_factory (CombinationFactory | LotteryCombination | Any): A factory
                function or class to create a combination instance. If not callable,
                a default LotteryCombination instance will be used.

        Returns:
            CombinationFactory: The combination factory.

        Examples:
            >>> factory = LotteryCombination.get_combination_factory(None)
            factory(main=[1, 2, 3, 4, 5], bonus=[6])
            LotteryCombination()
            >>> factory = LotteryCombination.get_combination_factory(LotteryCombination(
            ...     main=BoundCombination(start=1, end=50, count=5)
            ... ))
            factory(main=[1, 2, 3, 4, 5])
            LotteryCombination(main=BoundCombination(...))
        """
        if isinstance(combination_factory, CompoundCombination):
            return combination_factory.get_combination
        if not callable(combination_factory):
            return LotteryCombination().get_combination
        return combination_factory

    def generate(self, n: int = 1, partitions: int = 1) -> list[LotteryCombination]:
        """Generate a list of random LotteryCombination instances with similar components.

        Args:
            n (int): The number of combinations to generate. Defaults to 1.
            partitions (int): The number of partitions to divide the generation into.
                Defaults to 1.

        Returns:
            list[LotteryCombination]: A list of generated LotteryCombination instances.

        Examples:
            >>> main_numbers = BoundCombination(start=1, end=50, count=5)
            >>> bonus_number = BoundCombination(start=1, end=10, count=1)
            >>> lottery_comb = LotteryCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> random_combs = lottery_comb.generate(n=3)
            >>> len(random_combs)
            3
        """
        return [
            self.get_combination(rank)
            for rank in generate(self.combinations, n=n, partitions=partitions)
        ]

    def get_combination(
        self,
        combination: CombinationInput | LotteryCombination | None = None,
        *,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> LotteryCombination:
        """Get a LotteryCombination based on provided components.

        Supports integer rank input to decode a rank into component values. For a flat list
        of values, each component receives values based on its count (max capacity) rather than
        its current length.

        Args:
            combination (CombinationInput | LotteryCombination | None): The base combination to
                build from. If None, uses the provided components. An integer rank decodes into
                each component's values using the cross-product encoding.
            winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
                uses the current instance's winning ranks.
            **components (CombinationInputOrRank | LotteryCombination): The components to
                construct the combination.

        Returns:
            LotteryCombination: The constructed LotteryCombination.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb = LotteryCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> new_comb = lottery_comb.get_combination(main=[1, 2, 3, 6, 7])
            >>> new_comb.components
            {'main': BoundCombination(...), 'bonus': BoundCombination(...)}
        """
        components = self.get_components(**components)

        if isinstance(combination, CompoundCombination):
            elevated = {}
            for name, comp in combination.components.items():
                if isinstance(comp, BoundCombination):
                    elevated[name] = comp
                elif name in self._components:
                    elevated[name] = self._components[name].copy(values=comp.values)
            components = {**elevated, **components}
            if winning_ranks is None:
                winning_ranks = combination._winning_ranks
        elif combination is not None:
            components_ = {}
            if isinstance(combination, int):
                for name, component in reversed(self._components.items()):
                    components_[name] = component.copy(values=combination % component.combinations)
                    combination = combination // component.combinations
                components_ = dict(reversed(components_.items()))
            else:
                values = list(combination)
                for name, component in self._components.items():
                    components_[name] = component.copy(values=values[: component.count])
                    if len(values) > component.count:
                        values = values[component.count :]
                    else:
                        values = []
            components = {**components_, **components}

        return self._create_combination(
            **components,
            winning_ranks=self._winning_ranks if winning_ranks is None else winning_ranks,
        )

    def _create_combination(
        self,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> LotteryCombination:
        """Create a correct class instance from the given components and winning ranks."""
        return LotteryCombination(**components, winning_ranks=winning_ranks)

    @staticmethod
    def from_string(data: str) -> dict:
        """Parse a string representation into lottery component values.

        LotteryCombination cannot build BoundCombination components from string data alone,
        because bounds and counts are game-specific. This parser therefore returns raw
        component values for subclasses or callers that have the required metadata.

        Args:
            data (str): A string representation of a LotteryCombination.

        Returns:
            dict: Parsed component values keyed by component name.

        Examples:
            >>> data = 'numbers: [1, 2, 3, 4, 5]  extra: [6, 7, 8]'
            >>> LotteryCombination.from_string(data)
            {'numbers': [1, 2, 3, 4, 5], 'extra': [6, 7, 8]}
        """
        return {
            name: [int(value.strip()) for value in values.split(",") if value.strip()]
            for name, values in RE_COMPONENT.findall(data)
        }

    @staticmethod
    def from_csv(data: dict) -> dict:
        """Parse a CSV-compatible dictionary into lottery component values.

        LotteryCombination cannot build BoundCombination components from CSV data alone,
        because bounds and counts are game-specific. This parser therefore returns raw
        component values for subclasses or callers that have the required metadata.

        Args:
            data (dict): A CSV-compatible dictionary representation of a LotteryCombination.

        Returns:
            dict: Parsed component values keyed by component name.

        Examples:
            >>> data = {'numbers_1': 1, 'numbers_2': 2, 'extra_1': 6}
            >>> LotteryCombination.from_csv(data)
            {'numbers': [1, 2], 'extra': [6]}
        """
        components = {}
        for key, value in data.items():
            match = RE_NUMBER.match(key)
            if not match:
                continue
            name = match.group("component")
            if name not in components:
                components[name] = []
            components[name].append(value)

        return components

    @classmethod
    def from_dict(cls, data: dict) -> LotteryCombination:
        """Create a LotteryCombination from a dictionary.

        Args:
            data (dict): A dictionary representation of a LotteryCombination.

        Returns:
            LotteryCombination: The created LotteryCombination instance.

        Examples:
            >>> data = {
            ...     'components': {
            ...         'main': {'values': [1, 2, 3, 4, 5], 'start': 1, 'end': 50, 'count': 5},
            ...         'bonus': {'values': [6], 'start': 1, 'end': 10, 'count': 1}
            ...     },
            ...     'winning_ranks': {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            ... }
            >>> lottery_comb = LotteryCombination.from_dict(data)
            >>> lottery_comb.components
            {'main': BoundCombination(...), 'bonus': BoundCombination(...)}
            >>> lottery_comb.winning_ranks
            {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
        """
        return cls(
            **{
                name: BoundCombination.from_dict(component_data)
                for name, component_data in data.get("components", {}).items()
            },
            winning_ranks=data.get("winning_ranks", {}),
        )

    def __repr__(self) -> str:
        params = ", ".join(
            f"{name}={repr(component)}" for name, component in self._components.items()
        )
        if params:
            params = params + ", "
        return f"LotteryCombination({params}winning_ranks={self._winning_ranks})"

    def __hash__(self) -> int:
        return self.rank
