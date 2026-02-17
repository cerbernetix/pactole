"""Module for Lottery combination representation and manipulation."""

from __future__ import annotations

import random
from functools import cached_property
from math import ceil, prod
from typing import Iterator, Protocol

from .combination import (
    BoundCombination,
    CombinationInput,
    CombinationInputOrRank,
    CombinationInputValues,
    CombinationNumber,
    CombinationRank,
    CombinationValues,
)

CombinationWinningPattern = tuple[int, ...]
CombinationWinningRanks = dict[CombinationWinningPattern, CombinationRank]
CombinationComponents = dict[str, BoundCombination]


class CombinationFactory(Protocol):
    """Protocol for a combination factory."""

    def __call__(
        self,
        combination: CombinationInput | LotteryCombination | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> LotteryCombination:
        """Create a combination from the provided components.

        Args:
            combination (CombinationInput | LotteryCombination | None): The base combination to
                build from. If None, uses the provided components.
            **components (CombinationInputOrRank | LotteryCombination): The components to construct
                the combination.

        Returns:
            LotteryCombination: An instance of LotteryCombination created from the provided
                components.
        """


class LotteryCombination:
    """Class representing a Lottery combination.

    A Lottery combination is a compound combination that can consist of multiple components
    (e.g., main numbers, bonus numbers).

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

    _components: CombinationComponents
    _winning_ranks: CombinationWinningRanks

    def __init__(
        self,
        combination: LotteryCombination | None = None,
        *,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: BoundCombination,
    ) -> None:
        if isinstance(combination, LotteryCombination):
            components = {**combination._components, **components}
            if winning_ranks is None:
                winning_ranks = combination._winning_ranks.copy()

        if winning_ranks is None:
            winning_ranks = {}

        for component in components.values():
            if not isinstance(component, BoundCombination):
                raise TypeError("All components must be instances of BoundCombination.")

        self._components = components
        self._winning_ranks = winning_ranks

    @property
    def components(self) -> CombinationComponents:
        """Get the components of the combination.

        Returns:
            CombinationComponents: The components of the combination.

        Examples:
            >>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb = LotteryCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> lottery_comb.components
            {'main': BoundCombination(...), 'bonus': BoundCombination(...)}
        """
        return self._components.copy()

    @cached_property
    def values(self) -> CombinationValues:
        """Get all numbers in the combination.

        Returns:
            CombinationValues: The list of all numbers in the combination.

        Examples:
            >>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb = LotteryCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> lottery_comb.values
            [1, 2, 3, 4, 5, 6]
        """
        return [value for component in self._components.values() for value in component.values]

    @cached_property
    def rank(self) -> CombinationRank:
        """Get the lexicographic rank of the combination.

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
    def length(self) -> int:
        """Get the total length of the combination.

        Returns:
            int: The total length of the combination.

        Examples:
            >>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb = LotteryCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> lottery_comb.length
            6
        """
        return sum(component.length for component in self._components.values())

    @cached_property
    def count(self) -> int:
        """Return the count of numbers in the combination.

        Returns:
            int: The count of numbers.

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
            int: The total number of combinations.

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

    @property
    def winning_ranks(self) -> CombinationWinningRanks:
        """Get the winning ranks mapping.

        Returns:
            CombinationWinningRanks: The winning ranks mapping.

        Examples:
            >>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            >>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
            >>> lottery_comb.winning_ranks
            {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
        """
        return self._winning_ranks.copy()

    @property
    def nb_winning_ranks(self) -> int:
        """Get the number of winning ranks.

        Returns:
            int: The number of winning ranks.

        Examples:
            >>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            >>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
            >>> lottery_comb.nb_winning_ranks
            4
        """
        if not self._winning_ranks:
            return 0
        min_rank = min(self._winning_ranks.values())
        max_rank = max(self._winning_ranks.values())
        return max_rank - min_rank + 1

    @property
    def min_winning_rank(self) -> int | None:
        """Get the minimum winning rank.

        Returns:
            int | None: The minimum winning rank, or None if there are no winning ranks.

        Examples:
            >>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            >>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
            >>> lottery_comb.min_winning_rank
            1
            >>> lottery_comb_empty = LotteryCombination()
            >>> lottery_comb_empty.min_winning_rank
            None
        """
        if not self._winning_ranks:
            return None
        return min(self._winning_ranks.values())

    @property
    def max_winning_rank(self) -> int | None:
        """Get the maximum winning rank.

        Returns:
            int | None: The maximum winning rank, or None if there are no winning ranks.

        Examples:
            >>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            >>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
            >>> lottery_comb.max_winning_rank
            4
            >>> lottery_comb_empty = LotteryCombination()
            >>> lottery_comb_empty.max_winning_rank
            None
        """
        if not self._winning_ranks:
            return None
        return max(self._winning_ranks.values())

    def generate(self, n: int = 1, partitions: int = 1) -> list[LotteryCombination]:
        """Generate a list of random LotteryCombination with similar components.

        Args:
            n (int): The number of combinations to generate. Defaults to 1.
            partitions (int): The number of partitions to divide the generation into. Defaults to 1.

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
            >>> random_combs[0].values
            [3, 15, 22, 34, 45, 7]
        """
        n = max(1, n)
        partitions = max(1, partitions)
        combinations = self.combinations
        partition = ceil(combinations / partitions)

        return [
            self.get_combination(
                random.randint(
                    partition * (i % partitions),
                    min(partition * (i % partitions + 1) - 1, combinations - 1),
                )
            )
            for i in range(n)
        ]

    def copy(
        self,
        *,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> LotteryCombination:
        """Create a copy of the LotteryCombination with optional modifications.

        Args:
            winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
                uses the current instance's winning ranks.
            **components (CombinationInputOrRank | LotteryCombination): The components to modify in
                the copy. If not provided, the original component is used.

        Returns:
            LotteryCombination: A new LotteryCombination instance with the specified modifications.
        """
        if winning_ranks is None:
            winning_ranks = self._winning_ranks

        components = {
            name: components.get(name) or values for name, values in self._components.items()
        }

        return self._create_combination(**components, winning_ranks=winning_ranks)

    def get_combination(
        self,
        combination: CombinationInput | LotteryCombination | None = None,
        *,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> LotteryCombination:
        """Get a LotteryCombination based on provided components.

        Args:
            combination (CombinationInput | LotteryCombination | None): The base combination to
                build from. If None, uses the provided components.
            winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
                uses the current instance's winning ranks.
            **components (CombinationInputOrRank | LotteryCombination): The components to construct
                the combination.

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

        if isinstance(combination, LotteryCombination):
            components = {**combination._components, **components}
            if winning_ranks is None:
                winning_ranks = combination._winning_ranks.copy()
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

        if winning_ranks is None:
            winning_ranks = self._winning_ranks

        return self._create_combination(**components, winning_ranks=winning_ranks)

    def _create_combination(
        self,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> LotteryCombination:
        """Create a correct class instance from the given components and winning ranks."""
        return LotteryCombination(**components, winning_ranks=winning_ranks)

    def get_components(
        self,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> CombinationComponents:
        """Get the parameters for multiple components of the combination.

        Args:
            **components (CombinationInputOrRank | LotteryCombination): The names and values of the
                components.

        Returns:
            CombinationComponents: The parameters for the specified components.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb = LotteryCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> lottery_comb.get_components(main=[1, 2, 3, 4, 5], bonus=[6])
            {'main': BoundCombination(...), 'bonus': BoundCombination(...)}
            >>> lottery_comb.get_components(main=[1, 2, 3])
            {'main': BoundCombination(...)}
            >>> lottery_comb.get_components(bonus=[7])
            {'bonus': BoundCombination(...)}
            >>> lottery_comb.get_components(extra=[8])
            KeyError: 'Component "extra" does not exist in the combination.'
        """
        return {
            name: self._components[name].copy(values=values) for name, values in components.items()
        }

    def get_component(self, name: str) -> BoundCombination | None:
        """Get the parameters for a specific component of the combination.

        Args:
            name (str): The name of the component.

        Returns:
            BoundCombination | None: The parameters for the specified component,
                or None if not found.

        Examples:
            >>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb = LotteryCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> lottery_comb.get_component('main')
            BoundCombination(...)
            >>> lottery_comb.get_component('bonus')
            BoundCombination(...)
            >>> lottery_comb.get_component('extra')
            None
        """
        return self._components.get(name)

    def get_component_values(self, name: str) -> CombinationValues:
        """Get the values for a specific component of the combination.

        Args:
            name (str): The name of the component.

        Returns:
            CombinationValues: The values for the specified component.

        Examples:
            >>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb = LotteryCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> lottery_comb.get_component_values('main')
            [1, 2, 3, 4, 5]
            >>> lottery_comb.get_component_values('bonus')
            [6]
            >>> lottery_comb.get_component_values('extra')
            []
        """
        component = self._components.get(name)
        if component is None:
            return []

        return component.values

    def get_winning_rank(
        self,
        combination: CombinationInput | LotteryCombination | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> int | None:
        """Get the winning rank of the combination against a winning combination.

        Args:
            combination (CombinationInput | LotteryCombination | None): The winning combination to
                compare against.
            **components (CombinationInputOrRank | LotteryCombination): The components of the
                winning combination.

        Returns:
            int | None: The winning rank, or None if not a winning combination.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            >>> lottery_comb = LotteryCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number,
            ...     winning_ranks=winning_ranks
            ... )
            >>> winning_comb = lottery_comb.get_combination(main=[1, 2, 3, 4, 5], bonus=[6])
            >>> lottery_comb.get_winning_rank(winning_comb)
            1
            >>> winning_comb = lottery_comb.get_combination(main=[1, 2, 3, 4, 5], bonus=[7])
            >>> lottery_comb.get_winning_rank(winning_comb)
            2
            >>> winning_comb = lottery_comb.get_combination(main=[1, 2, 3, 4, 6], bonus=[6])
            >>> lottery_comb.get_winning_rank(winning_comb)
            3
            >>> winning_comb = lottery_comb.get_combination(main=[1, 2, 3, 4, 6], bonus=[7])
            >>> lottery_comb.get_winning_rank(winning_comb)
            4
            >>> winning_comb = lottery_comb.get_combination(main=[10, 11, 12, 13, 14], bonus=[15])
            >>> lottery_comb.get_winning_rank(winning_comb)
            None
        """
        winning_combination = self.intersection(combination, **components)
        return self._winning_ranks.get(
            tuple(component.length for component in winning_combination.components.values())
        )

    def equals(
        self,
        combination: CombinationInput | LotteryCombination | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> bool:
        """Check if the combination is equal to another combination.

        Args:
            combination (CombinationInput | LotteryCombination | None): The other combination to
                compare against.
            **components (CombinationInputOrRank | LotteryCombination): The components of the other
                combination.

        Returns:
            bool: True if equal, False otherwise.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number1 = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb1 = LotteryCombination(
            ...     main=main_numbers1,
            ...     bonus=bonus_number1
            ... )
            >>> main_numbers2 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number2 = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb2 = LotteryCombination(
            ...     main=main_numbers2,
            ...     bonus=bonus_number2
            ... )
            >>> lottery_comb1.equals(lottery_comb2)
            True
        """
        combination = self.get_combination(combination, **components)

        if combination.length != self.length:
            return False

        if not combination.length and not self.length:
            return True

        return all(
            self_name == other_name and self_comp == other_comp
            for (self_name, self_comp), (other_name, other_comp) in zip(
                self.components.items(), combination.components.items()
            )
        )

    def includes(
        self,
        combination: CombinationInput | LotteryCombination | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> bool:
        """Check if the combination includes another combination.

        Args:
            combination (CombinationInput | LotteryCombination | None): The other combination to
                compare against.
            **components (CombinationInputOrRank | LotteryCombination): The components of the other
                combination.

        Returns:
            bool: True if includes, False otherwise.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number1 = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb1 = LotteryCombination(
            ...     main=main_numbers1,
            ...     bonus=bonus_number1
            ... )
            >>> main_numbers2 = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)
            >>> bonus_number2 = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb2 = LotteryCombination(
            ...     main=main_numbers2,
            ...     bonus=bonus_number2
            ... )
            >>> lottery_comb1.includes(lottery_comb2)
            True
            >>> main_numbers3 = BoundCombination(values=[1, 2, 6], start=1, end=50, count=5)
            >>> lottery_comb3 = LotteryCombination(
            ...     main=main_numbers3,
            ...     bonus=bonus_number2
            ... )
            >>> lottery_comb1.includes(lottery_comb3)
            False
        """
        combination = self.get_combination(combination, **components)

        if not combination.length:
            return True

        return all(
            self._components[other_name].includes(other_comp)
            for other_name, other_comp in combination.components.items()
        )

    def intersects(
        self,
        combination: CombinationInput | LotteryCombination | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> bool:
        """Check if the combination intersects with another combination.

        Args:
            combination (CombinationInput | LotteryCombination | None): The other combination to
                compare against.
            **components (CombinationInputOrRank | LotteryCombination): The components of the other
                combination.

        Returns:
            bool: True if intersects, False otherwise.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number1 = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb1 = LotteryCombination(
            ...     main=main_numbers1,
            ...     bonus=bonus_number1
            ... )
            >>> main_numbers2 = BoundCombination(values=[4, 5, 6], start=1, end=50, count=5)
            >>> bonus_number2 = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb2 = LotteryCombination(
            ...     main=main_numbers2,
            ...     bonus=bonus_number2
            ... )
            >>> lottery_comb1.intersects(lottery_comb2)
            True
            >>> main_numbers3 = BoundCombination(values=[7, 8, 9], start=1, end=50, count=5)
            >>> lottery_comb3 = LotteryCombination(
            ...     main=main_numbers3,
            ...     bonus=bonus_number2
            ... )
            >>> lottery_comb1.intersects(lottery_comb3)
            False
        """
        combination = self.get_combination(combination, **components)

        if not combination.length or not self.length:
            return False

        return all(
            self._components[other_name].intersects(other_comp)
            for other_name, other_comp in combination.components.items()
            if other_comp.length > 0
        )

    def intersection(
        self,
        combination: CombinationInput | LotteryCombination | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> LotteryCombination:
        """Get the intersection with another combination.

        Args:
            combination (CombinationInput | LotteryCombination | None): The other combination to
                compare against.
            **components (CombinationInputOrRank | LotteryCombination): The components of the other
                combination.

        Returns:
            LotteryCombination: The intersection combination.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number1 = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb1 = LotteryCombination(
            ...     main=main_numbers1,
            ...     bonus=bonus_number1
            ... )
            >>> main_numbers2 = BoundCombination(values=[4, 5, 6], start=1, end=50, count=5)
            >>> bonus_number2 = BoundCombination(values=[7], start=1, end=10, count=1)
            >>> lottery_comb2 = LotteryCombination(
            ...     main=main_numbers2,
            ...     bonus=bonus_number2
            ... )
            >>> intersection_comb = lottery_comb1.intersection(lottery_comb2)
            >>> intersection_comb.components
            {'main': BoundCombination(...), 'bonus': BoundCombination(...)}
            >>> intersection_comb.values
            [4, 5]
        """
        combination = self.get_combination(combination, **components)

        return self.get_combination(
            **{
                other_name: self._components[other_name].intersection(other_comp)
                for other_name, other_comp in combination.components.items()
            }
        )

    def compares(
        self,
        combination: CombinationInput | LotteryCombination | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> int:
        """Compare the combination with another combination.

        Args:
            combination (CombinationInput | LotteryCombination | None): The other combination to
                compare against.
            **components (CombinationInputOrRank | LotteryCombination): The components of the other
                combination.

        Returns:
            int: -1 if self < combination, 0 if self == combination, 1 if self > combination.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number1 = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb1 = LotteryCombination(
            ...     main=main_numbers1,
            ...     bonus=bonus_number1
            ... )
            >>> main_numbers2 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number2 = BoundCombination(values=[7], start=1, end=10, count=1)
            >>> lottery_comb2 = LotteryCombination(
            ...     main=main_numbers2,
            ...     bonus=bonus_number2
            ... )
            >>> lottery_comb1.compares(lottery_comb2)
            -1
        """
        combination = self.get_combination(combination, **components)

        if not combination.length and not self.length:
            return 0

        if not combination.length or not self.length:
            return -1 if self.length < combination.length else 1

        for other_name, other_comp in combination.components.items():
            self_comp = self._components[other_name]
            if self_comp < other_comp:
                return -1
            if self_comp > other_comp:
                return 1
        return 0

    def similarity(
        self,
        combination: CombinationInput | LotteryCombination | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> float:
        """Calculate the similarity with another combination.

        Args:
            combination (CombinationInput | LotteryCombination | None): The other combination to
                compare against.
            **components (CombinationInputOrRank | LotteryCombination): The components of the other
                combination.

        Returns:
            float: Similarity ratio between 0 and 1.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
            >>> bonus_number1 = BoundCombination(values=[6], start=1, end=10, count=1)
            >>> lottery_comb1 = LotteryCombination(
            ...     main=main_numbers1,
            ...     bonus=bonus_number1
            ... )
            >>> main_numbers2 = BoundCombination(values=[1, 2, 3, 6, 7], start=1, end=50, count=5)
            >>> bonus_number2 = BoundCombination(values=[8], start=1, end=10, count=1)
            >>> lottery_comb2 = LotteryCombination(
            ...     main=main_numbers2,
            ...     bonus=bonus_number2
            ... )
            >>> lottery_comb1.similarity(lottery_comb2)
            0.375
        """
        combination = self.get_combination(combination, **components)

        if not combination.length and not self.length:
            return 1.0

        if not combination.length or not self.length:
            return 0.0

        if all(
            self_name == other_name and self_comp == other_comp
            for (self_name, self_comp), (other_name, other_comp) in zip(
                self.components.items(), combination.components.items()
            )
        ):
            return 1.0

        return (
            self.get_combination(
                **{
                    other_name: self._components[other_name].intersection(other_comp)
                    for other_name, other_comp in combination.components.items()
                }
            ).length
            / self.length
        )

    def __eq__(self, combination: object) -> bool:
        return self.equals(combination)

    def __ne__(self, combination: object) -> bool:
        return not self.equals(combination)

    def __lt__(self, combination: CombinationInputOrRank | LotteryCombination) -> bool:
        return self.compares(combination) == -1

    def __gt__(self, combination: CombinationInputOrRank | LotteryCombination) -> bool:
        return self.compares(combination) == 1

    def __le__(self, combination: CombinationInputOrRank | LotteryCombination) -> bool:
        return self.compares(combination) != 1

    def __ge__(self, combination: CombinationInputOrRank | LotteryCombination) -> bool:
        return self.compares(combination) != -1

    def __contains__(
        self, item: CombinationNumber | CombinationInputValues | LotteryCombination
    ) -> bool:
        if isinstance(item, CombinationNumber):
            return item in self.values

        return self.includes(item)

    def __iter__(self) -> Iterator[CombinationNumber]:
        yield from self.values

    def __getitem__(self, index: int) -> CombinationNumber:
        return self.values[index]

    def __getattr__(self, name: str) -> BoundCombination:
        if name in self._components:
            return self._components[name]

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        return " ".join([f"{name}: {component}" for name, component in self._components.items()])

    def __repr__(self) -> str:
        params = ", ".join(
            [f"{name}={repr(component)}" for name, component in self._components.items()]
        )
        if params:
            params = params + ", "
        return f"LotteryCombination({params}winning_ranks={self._winning_ranks})"

    def __hash__(self) -> int:
        return self.rank
