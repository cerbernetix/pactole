"""Module for compound combination representation and manipulation."""

from __future__ import annotations

import re
from functools import cached_property
from typing import Any, Iterator, Protocol

from .combination import (
    Combination,
    CombinationInput,
    CombinationInputOrRank,
    CombinationInputValues,
    CombinationNumber,
    CombinationRank,
    CombinationValues,
)

RE_NUMBER = re.compile(r"^(?P<component>\w+)_(?P<index>\d+)$")
RE_COMPONENT = re.compile(r"(?P<name>\w+):\s*\[?(?P<values>[\d,\s]*)\]?")

CombinationWinningPattern = tuple[int, ...]
CombinationWinningRanks = dict[CombinationWinningPattern, CombinationRank]
CombinationComponents = dict[str, Combination]


class CombinationFactory(Protocol):
    """Protocol for a combination factory."""

    def __call__(
        self,
        combination: CombinationInput | CompoundCombination | None = None,
        **components: Combination | CombinationInput | CompoundCombination,
    ) -> CompoundCombination:
        """Create a combination from the provided components.

        Args:
            combination (CombinationInput | CompoundCombination | None): The base combination to
                build from. If None, uses the provided components.
            **components (Combination | CombinationInput | CompoundCombination): The components to
                construct the combination. Can be Combination instances, values to convert to
                Combination, or CompoundCombination instances.

        Returns:
            CompoundCombination: An instance of CompoundCombination created from the provided
                components.
        """


class CompoundCombination:
    """Class representing a compound combination.

    A compound combination can consist of multiple components (e.g., main numbers, bonus numbers).
    Components are built from Combination instances.

    Args:
        combination (CompoundCombination | None): The combination to copy from.
        winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
            initializes an empty mapping.
        **components (Combination | CombinationInput): The components of the combination. Each
            can be either a Combination instance or a value/list that will be converted to a
            Combination.

    Raises:
        ValueError: If a component cannot be converted to a Combination instance.

    Examples:
        >>> main_numbers = Combination([1, 2, 3, 4, 5])
        >>> bonus_number = Combination([6])
        >>> compound_comb = CompoundCombination(
        ...     main=main_numbers,
        ...     bonus=bonus_number
        ... )
        >>> compound_comb.components
        {'main': Combination([1, 2, 3, 4, 5]), 'bonus': Combination([6])}

        You can also use lists directly:

        >>> compound_comb = CompoundCombination(
        ...     main=[1, 2, 3, 4, 5],
        ...     bonus=[6]
        ... )
        >>> compound_comb.values
        [1, 2, 3, 4, 5, 6]
    """

    _components: CombinationComponents
    _winning_ranks: CombinationWinningRanks

    def __init__(
        self,
        combination: CompoundCombination | None = None,
        *,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: Combination | CombinationInput,
    ) -> None:
        if isinstance(combination, CompoundCombination):
            components = {**combination._components, **components}
            if winning_ranks is None:
                winning_ranks = combination._winning_ranks

        self._components = {
            name: component if isinstance(component, Combination) else Combination(component)
            for name, component in components.items()
        }
        self._winning_ranks = winning_ranks.copy() if winning_ranks else {}

    @property
    def components(self) -> CombinationComponents:
        """Get the components of the combination.

        Returns:
            CombinationComponents: The components of the combination.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> compound_comb.components
            {'main': Combination([1, 2, 3, 4, 5]), 'bonus': Combination([6])}
        """
        return self._components.copy()

    @cached_property
    def values(self) -> CombinationValues:
        """Get all numbers in the combination.

        Returns:
            CombinationValues: The list of all numbers in the combination.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> compound_comb.values
            [1, 2, 3, 4, 5, 6]
        """
        return [value for component in self._components.values() for value in component.values]

    @cached_property
    def length(self) -> int:
        """Get the total length of the combination.

        Returns:
            int: The total length of the combination.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> compound_comb.length
            6
        """
        return sum(component.length for component in self._components.values())

    @property
    def winning_ranks(self) -> CombinationWinningRanks:
        """Get the winning ranks mapping.

        Returns:
            CombinationWinningRanks: The winning ranks mapping.

        Examples:
            >>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            >>> compound_comb = CompoundCombination(winning_ranks=winning_ranks)
            >>> compound_comb.winning_ranks
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
            >>> compound_comb = CompoundCombination(winning_ranks=winning_ranks)
            >>> compound_comb.nb_winning_ranks
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
            >>> compound_comb = CompoundCombination(winning_ranks=winning_ranks)
            >>> compound_comb.min_winning_rank
            1
            >>> CompoundCombination().min_winning_rank
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
            >>> compound_comb = CompoundCombination(winning_ranks=winning_ranks)
            >>> compound_comb.max_winning_rank
            4
            >>> CompoundCombination().max_winning_rank
            None
        """
        if not self._winning_ranks:
            return None
        return max(self._winning_ranks.values())

    @staticmethod
    def get_combination_factory(
        combination_factory: CombinationFactory | CompoundCombination | Any,
    ) -> CombinationFactory:
        """Get the combination factory.

        It checks that the provided combination_factory is a callable, and if not, it returns a
        default factory from CompoundCombination, which in this case will produce combinations
        with no winning ranks since the default CompoundCombination has no winning ranks.

        An instance of a CompoundCombination can be used to produce a factory.

        Args:
            combination_factory (CombinationFactory | CompoundCombination | Any): A factory
                function or class to create a combination instance. If not callable,
                a default CompoundCombination instance will be used.

        Returns:
            CombinationFactory: The combination factory.

        Examples:
            >>> factory = CompoundCombination.get_combination_factory(None)
            >>> factory(main=[1, 2, 3, 4, 5], bonus=[6])
            CompoundCombination(main=Combination([1, 2, 3, 4, 5]), bonus=Combination([6]))
            >>> factory = CompoundCombination.get_combination_factory(CompoundCombination(
            ...     main=Combination([1, 2, 3, 4, 5])
            ... ))
            >>> factory(main=[3, 4, 5, 6, 7])
            CompoundCombination(main=Combination([3, 4, 5, 6, 7]), bonus=Combination([]))
        """
        if isinstance(combination_factory, CompoundCombination):
            return combination_factory.get_combination
        if not callable(combination_factory):
            return CompoundCombination
        return combination_factory

    def copy(
        self,
        *,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: Combination | CombinationInput,
    ) -> CompoundCombination:
        """Create a copy of the CompoundCombination with optional modifications.

        Args:
            winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
                uses the current instance's winning ranks.
            **components (Combination | CombinationInput): The components to modify in the copy.
                Can be Combination instances or values that will be converted to Combination.
                If not provided, the original component is used.

        Returns:
            CompoundCombination: A new CompoundCombination instance with the specified
                modifications.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number,
            ...     winning_ranks=winning_ranks
            ... )
            >>> new_comb = compound_comb.copy(main=[1, 2, 3, 6, 7])
            >>> new_comb.components
            {'main': Combination([1, 2, 3, 6, 7]), 'bonus': Combination([6])}
        """
        if winning_ranks is None:
            winning_ranks = self._winning_ranks

        components = {
            name: components.get(name) or component for name, component in self._components.items()
        }

        return self._create_combination(**components, winning_ranks=winning_ranks)

    def get_combination(
        self,
        combination: CombinationInput | CompoundCombination | None = None,
        *,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: Combination | CombinationInput | CompoundCombination,
    ) -> CompoundCombination:
        """Get a CompoundCombination based on provided components.

        When a flat list of values is provided, it is split among the components in order by the
        current length of each component. This means the flat-list input works correctly only when
        all components have at least one value.

        Args:
            combination (CombinationInput | CompoundCombination | None): The base combination to
                build from. If None, uses the provided components. Integer rank input is not
                supported; use a subclass that provides rank-based retrieval.
            winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
                uses the current instance's winning ranks.
            **components (Combination | CombinationInput | CompoundCombination): The components to
                construct the combination. Can be Combination instances, values to convert to
                Combination, or CompoundCombination instances.

        Returns:
            CompoundCombination: The constructed CompoundCombination.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> new_comb = compound_comb.get_combination(main=[1, 2, 3, 6, 7])
            >>> new_comb.components
            {'main': Combination([1, 2, 3, 6, 7]), 'bonus': Combination([6])}
        """
        components = self.get_components(**components)

        if isinstance(combination, CompoundCombination):
            components = {**combination._components, **components}
            if winning_ranks is None:
                winning_ranks = combination._winning_ranks.copy()
        elif combination is not None:
            values = list(combination)
            components_ = {}
            for name, component in self._components.items():
                components_[name] = component.copy(values=values[: component.length])
                if len(values) > component.length:
                    values = values[component.length :]
                else:
                    values = []
            components = {**components_, **components}

        if winning_ranks is None:
            winning_ranks = self._winning_ranks

        return self._create_combination(**components, winning_ranks=winning_ranks)

    def _create_combination(
        self,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: Combination | CombinationInput,
    ) -> CompoundCombination:
        """Create a correct class instance from the given components and winning ranks."""
        return CompoundCombination(**components, winning_ranks=winning_ranks)

    def get_components(
        self,
        **components: Combination | CombinationInput | CompoundCombination,
    ) -> CombinationComponents:
        """Get the parameters for multiple components of the combination.

        Args:
            **components (Combination | CombinationInput | CompoundCombination): The names and
                values of the components. Can be Combination instances, values to convert to
                Combination, or CompoundCombination instances.

        Returns:
            CombinationComponents: The parameters for the specified components.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> compound_comb.get_components(main=[1, 2, 3, 4, 5], bonus=[6])
            {'main': Combination([1, 2, 3, 4, 5]), 'bonus': Combination([6])}
            >>> compound_comb.get_components(main=[1, 2, 3])
            {'main': Combination([1, 2, 3])}
            >>> compound_comb.get_components(bonus=[7])
            {'bonus': Combination([7])}
            >>> compound_comb.get_components(extra=[8])
            KeyError: 'extra'
        """
        return {
            name: self._components[name].copy(values=values) for name, values in components.items()
        }

    def get(self, name: str) -> Combination | None:
        """Get the parameters for a specific component of the combination.

        Args:
            name (str): The name of the component.

        Returns:
            Combination | None: The parameters for the specified component, or None if not found.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> compound_comb.get('main')
            Combination([1, 2, 3, 4, 5])
            >>> compound_comb.get('bonus')
            Combination([6])
            >>> compound_comb.get('extra')
            None
        """
        return self._components.get(name)

    def get_values(self, name: str) -> CombinationValues:
        """Get the values for a specific component of the combination.

        Args:
            name (str): The name of the component.

        Returns:
            CombinationValues: The values for the specified component.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> compound_comb.get_values('main')
            [1, 2, 3, 4, 5]
            >>> compound_comb.get_values('bonus')
            [6]
            >>> compound_comb.get_values('extra')
            []
        """
        component = self._components.get(name)
        if component is None:
            return []

        return component.values

    def get_winning_rank(
        self,
        combination: CombinationInput | CompoundCombination | None = None,
        **components: CombinationInputOrRank | CompoundCombination,
    ) -> int | None:
        """Get the winning rank of the combination against a winning combination.

        Args:
            combination (CombinationInput | CompoundCombination | None): The winning combination
                to compare against.
            **components (CombinationInputOrRank | CompoundCombination): The components of the
                winning combination.

        Returns:
            int | None: The winning rank, or None if not a winning combination.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number,
            ...     winning_ranks=winning_ranks
            ... )
            >>> winning_comb = compound_comb.get_combination(main=[1, 2, 3, 4, 5], bonus=[6])
            >>> compound_comb.get_winning_rank(winning_comb)
            1
            >>> winning_comb = compound_comb.get_combination(main=[1, 2, 3, 4, 5], bonus=[7])
            >>> compound_comb.get_winning_rank(winning_comb)
            2
        """
        winning_combination = self.intersection(combination, **components)
        return self._winning_ranks.get(
            tuple(component.length for component in winning_combination.components.values())
        )

    def equals(
        self,
        combination: CombinationInput | CompoundCombination | None = None,
        **components: CombinationInputOrRank | CompoundCombination,
    ) -> bool:
        """Check if the combination is equal to another combination.

        Args:
            combination (CombinationInput | CompoundCombination | None): The other combination to
                compare against.
            **components (CombinationInputOrRank | CompoundCombination): The components of the
                other combination.

        Returns:
            bool: True if equal, False otherwise.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers1 = Combination([1, 2, 3, 4, 5])
            >>> bonus_number1 = Combination([6])
            >>> compound_comb1 = CompoundCombination(
            ...     main=main_numbers1,
            ...     bonus=bonus_number1
            ... )
            >>> main_numbers2 = Combination([1, 2, 3, 4, 5])
            >>> bonus_number2 = Combination([6])
            >>> compound_comb2 = CompoundCombination(
            ...     main=main_numbers2,
            ...     bonus=bonus_number2
            ... )
            >>> compound_comb1.equals(compound_comb2)
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
        combination: CombinationInput | CompoundCombination | None = None,
        **components: CombinationInputOrRank | CompoundCombination,
    ) -> bool:
        """Check if the combination includes another combination.

        Args:
            combination (CombinationInput | CompoundCombination | None): The other combination to
                compare against.
            **components (CombinationInputOrRank | CompoundCombination): The components of the
                other combination.

        Returns:
            bool: True if includes, False otherwise.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers1 = Combination([1, 2, 3, 4, 5])
            >>> bonus_number1 = Combination([6])
            >>> compound_comb1 = CompoundCombination(
            ...     main=main_numbers1,
            ...     bonus=bonus_number1
            ... )
            >>> main_numbers2 = Combination([1, 2, 3])
            >>> bonus_number2 = Combination([6])
            >>> compound_comb2 = CompoundCombination(
            ...     main=main_numbers2,
            ...     bonus=bonus_number2
            ... )
            >>> compound_comb1.includes(compound_comb2)
            True
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
        combination: CombinationInput | CompoundCombination | None = None,
        **components: CombinationInputOrRank | CompoundCombination,
    ) -> bool:
        """Check if the combination intersects with another combination.

        Args:
            combination (CombinationInput | CompoundCombination | None): The other combination to
                compare against.
            **components (CombinationInputOrRank | CompoundCombination): The components of the
                other combination.

        Returns:
            bool: True if intersects, False otherwise.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers1 = Combination([1, 2, 3, 4, 5])
            >>> bonus_number1 = Combination([6])
            >>> compound_comb1 = CompoundCombination(
            ...     main=main_numbers1,
            ...     bonus=bonus_number1
            ... )
            >>> main_numbers2 = Combination([4, 5, 6])
            >>> bonus_number2 = Combination([6])
            >>> compound_comb2 = CompoundCombination(
            ...     main=main_numbers2,
            ...     bonus=bonus_number2
            ... )
            >>> compound_comb1.intersects(compound_comb2)
            True
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
        combination: CombinationInput | CompoundCombination | None = None,
        **components: CombinationInputOrRank | CompoundCombination,
    ) -> CompoundCombination:
        """Get the intersection with another combination.

        Args:
            combination (CombinationInput | CompoundCombination | None): The other combination to
                compare against.
            **components (CombinationInputOrRank | CompoundCombination): The components of the
                other combination.

        Returns:
            CompoundCombination: The intersection combination.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers1 = Combination([1, 2, 3, 4, 5])
            >>> bonus_number1 = Combination([6])
            >>> compound_comb1 = CompoundCombination(
            ...     main=main_numbers1,
            ...     bonus=bonus_number1
            ... )
            >>> main_numbers2 = Combination([4, 5, 6])
            >>> bonus_number2 = Combination([7])
            >>> compound_comb2 = CompoundCombination(
            ...     main=main_numbers2,
            ...     bonus=bonus_number2
            ... )
            >>> intersection_comb = compound_comb1.intersection(compound_comb2)
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
        combination: CombinationInput | CompoundCombination | None = None,
        **components: CombinationInputOrRank | CompoundCombination,
    ) -> int:
        """Compare the combination with another combination.

        Args:
            combination (CombinationInput | CompoundCombination | None): The other combination to
                compare against.
            **components (CombinationInputOrRank | CompoundCombination): The components of the
                other combination.

        Returns:
            int: -1 if self < combination, 0 if self == combination, 1 if self > combination.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers1 = Combination([1, 2, 3, 4, 5])
            >>> bonus_number1 = Combination([6])
            >>> compound_comb1 = CompoundCombination(
            ...     main=main_numbers1,
            ...     bonus=bonus_number1
            ... )
            >>> main_numbers2 = Combination([1, 2, 3, 4, 5])
            >>> bonus_number2 = Combination([7])
            >>> compound_comb2 = CompoundCombination(
            ...     main=main_numbers2,
            ...     bonus=bonus_number2
            ... )
            >>> compound_comb1.compares(compound_comb2)
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
        combination: CombinationInput | CompoundCombination | None = None,
        **components: CombinationInputOrRank | CompoundCombination,
    ) -> float:
        """Calculate the similarity with another combination.

        Args:
            combination (CombinationInput | CompoundCombination | None): The other combination to
                compare against.
            **components (CombinationInputOrRank | CompoundCombination): The components of the
                other combination.

        Returns:
            float: Similarity ratio between 0 and 1.

        Raises:
            KeyError: If a component name does not exist in the current combination.

        Examples:
            >>> main_numbers1 = Combination([1, 2, 3, 4, 5])
            >>> bonus_number1 = Combination([6])
            >>> compound_comb1 = CompoundCombination(
            ...     main=main_numbers1,
            ...     bonus=bonus_number1
            ... )
            >>> main_numbers2 = Combination([1, 2, 3, 6, 7])
            >>> bonus_number2 = Combination([8])
            >>> compound_comb2 = CompoundCombination(
            ...     main=main_numbers2,
            ...     bonus=bonus_number2
            ... )
            >>> compound_comb1.similarity(compound_comb2)
            0.5
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

    def dump(self) -> dict:
        """Dump the CompoundCombination to a dictionary.

        Returns:
            dict: A dictionary representation of the CompoundCombination.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number,
            ...     winning_ranks=winning_ranks
            ... )
            >>> compound_comb.dump()
            {
                'main': [1, 2, 3, 4, 5],
                'bonus': [6],
            }
        """
        return {name: component.values for name, component in self._components.items()}

    def to_string(self) -> str:
        """Convert the CompoundCombination to a string representation.

        Returns:
            str: A string representation of the CompoundCombination.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> compound_comb.to_string()
            'main: [1, 2, 3, 4, 5]  bonus: [6]'
        """
        return str(self)

    def to_csv(self) -> dict:
        """Convert the CompoundCombination to a CSV-serializable dictionary.

        Returns:
            dict: A CSV-serializable dictionary representation of the CompoundCombination.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number
            ... )
            >>> compound_comb.to_csv()
            {'main_1': 1, 'main_2': 2, 'main_3': 3, 'main_4': 4, 'main_5': 5, 'bonus_1': 6}
        """
        data = {}

        for name, component in self._components.items():
            for i, value in enumerate(component.values, start=1):
                data[f"{name}_{i}"] = value

        return data

    def to_json(self) -> dict:
        """Convert the CompoundCombination to a JSON-serializable dictionary.

        Returns:
            dict: A JSON-serializable dictionary representation of the CompoundCombination.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number,
            ...     winning_ranks=winning_ranks
            ... )
            >>> compound_comb.to_json()
            {
                'components': {
                    'main': {'values': [1, 2, 3, 4, 5], 'rank': None, 'start': 1},
                    'bonus': {'values': [6], 'rank': None, 'start': 1}
                },
                'winning_ranks': {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            }
        """
        return self.to_dict()

    def to_dict(self) -> dict:
        """Convert the CompoundCombination to a dictionary.

        Returns:
            dict: A dictionary representation of the CompoundCombination.

        Examples:
            >>> main_numbers = Combination([1, 2, 3, 4, 5])
            >>> bonus_number = Combination([6])
            >>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            >>> compound_comb = CompoundCombination(
            ...     main=main_numbers,
            ...     bonus=bonus_number,
            ...     winning_ranks=winning_ranks
            ... )
            >>> compound_comb.to_dict()
            {
                'components': {
                    'main': {'values': [1, 2, 3, 4, 5], 'rank': None, 'start': 1},
                    'bonus': {'values': [6], 'rank': None, 'start': 1}
                },
                'winning_ranks': {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
            }
        """
        return {
            "components": {
                name: component.to_dict() for name, component in self._components.items()
            },
            "winning_ranks": self._winning_ranks.copy(),
        }

    @classmethod
    def from_string(cls, data: str) -> CompoundCombination:
        """Create a CompoundCombination from a string representation.

        Args:
            data (str): A string representation of a CompoundCombination.

        Returns:
            CompoundCombination: The created CompoundCombination instance.

        Examples:
            >>> data = 'main: [1, 2, 3, 4, 5]  bonus: [6]'
            >>> combination = CompoundCombination.from_string(data)
            >>> combination.components['main'].values
            [1, 2, 3, 4, 5]
            >>> combination.components['bonus'].values
            [6]
        """
        return cls(
            **{
                name: [int(value.strip()) for value in values.split(",") if value.strip()]
                for name, values in RE_COMPONENT.findall(data)
            }
        )

    @classmethod
    def from_csv(cls, data: dict) -> CompoundCombination:
        """Create a CompoundCombination from a CSV-serializable dictionary.

        Args:
            data (dict): A CSV-serializable dictionary representation of a CompoundCombination.

        Returns:
            CompoundCombination: The created CompoundCombination instance.

        Examples:
            >>> data = {'main_1': 1, 'main_2': 2, 'main_3': 3, 'main_4': 4, 'main_5': 5,
            ...         'bonus_1': 6}
            >>> combination = CompoundCombination.from_csv(data)
            >>> combination.components['main'].values
            [1, 2, 3, 4, 5]
            >>> combination.components['bonus'].values
            [6]
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

        return cls(**components)

    @classmethod
    def from_json(cls, data: dict) -> CompoundCombination:
        """Create a CompoundCombination from a JSON-serializable dictionary.

        Args:
            data (dict): A JSON-serializable dictionary representation of a CompoundCombination.

        Returns:
            CompoundCombination: The created CompoundCombination instance.

        Examples:
            >>> data = {
            ...     'components': {
            ...         'main': {'values': [1, 2, 3, 4, 5], 'rank': None, 'start': 1},
            ...         'bonus': {'values': [6], 'rank': None, 'start': 1}
            ...     },
            ...     'winning_ranks': {(5, 1): 1}
            ... }
            >>> compound_comb = CompoundCombination.from_json(data)
            >>> compound_comb.components
            {'main': Combination([1, 2, 3, 4, 5]), 'bonus': Combination([6])}
        """
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> CompoundCombination:
        """Create a CompoundCombination from a dictionary.

        Args:
            data (dict): A dictionary representation of a CompoundCombination.

        Returns:
            CompoundCombination: The created CompoundCombination instance.

        Examples:
            >>> data = {
            ...     'components': {
            ...         'main': {'values': [1, 2, 3, 4, 5], 'rank': None, 'start': 1},
            ...         'bonus': {'values': [6], 'rank': None, 'start': 1}
            ...     },
            ...     'winning_ranks': {(5, 1): 1}
            ... }
            >>> compound_comb = CompoundCombination.from_dict(data)
            >>> compound_comb.components
            {'main': Combination([1, 2, 3, 4, 5]), 'bonus': Combination([6])}
            >>> compound_comb.winning_ranks
            {(5, 1): 1}
        """
        return cls(
            **{
                name: Combination.from_dict(component_data)
                for name, component_data in data.get("components", {}).items()
            },
            winning_ranks=data.get("winning_ranks", {}),
        )

    def __eq__(self, combination: object) -> bool:
        return self.equals(combination)

    def __ne__(self, combination: object) -> bool:
        return not self.equals(combination)

    def __lt__(self, combination: CombinationInputOrRank | CompoundCombination) -> bool:
        return self.compares(combination) == -1

    def __gt__(self, combination: CombinationInputOrRank | CompoundCombination) -> bool:
        return self.compares(combination) == 1

    def __le__(self, combination: CombinationInputOrRank | CompoundCombination) -> bool:
        return self.compares(combination) != 1

    def __ge__(self, combination: CombinationInputOrRank | CompoundCombination) -> bool:
        return self.compares(combination) != -1

    def __contains__(
        self, item: CombinationNumber | CombinationInputValues | CompoundCombination
    ) -> bool:
        if isinstance(item, CombinationNumber):
            return item in self.values

        return self.includes(item)

    def __iter__(self) -> Iterator[CombinationNumber]:
        yield from self.values

    def __getitem__(self, index: int | str) -> CombinationNumber:
        if isinstance(index, str):
            component = self._components.get(index)
            if component is None:
                raise KeyError(f"Component '{index}' not found in the combination.")
            return component

        return self.values[index]

    def __getattr__(self, name: str) -> Combination:
        if name in self._components:
            return self._components[name]

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        return "  ".join(f"{name}: {component}" for name, component in self._components.items())

    def __repr__(self) -> str:
        params = ", ".join(
            f"{name}={repr(component)}" for name, component in self._components.items()
        )
        if params:
            params = params + ", "
        return f"CompoundCombination({params}winning_ranks={self._winning_ranks})"
