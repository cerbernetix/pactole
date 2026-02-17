"""Combination module for handling combinations of values and their lexicographic ranks."""

from __future__ import annotations

import random
from functools import cache, cached_property
from math import ceil
from math import comb as math_comb
from typing import Iterable, Iterator, TypedDict

DEFAULT_START = 1
DEFAULT_END = 50
DEFAULT_COUNT = 5

CombinationRank = int
CombinationNumber = int
CombinationNumbers = Iterable[CombinationNumber]
CombinationValues = list[CombinationNumber]


comb = cache(math_comb)
"""Cached version of math.comb to improve performance.

Args:
    n (int): The total number of items.
    k (int): The number of items to choose.

Returns:
    int: The number of combinations (n choose k).

Raises:
    ValueError: If n or k is negative, or if k is greater than n.

Examples:
    >>> comb(5, 2)
    10
    >>> comb(10, 3)
    120
"""


def get_combination_rank(combination: Iterable[int], offset: int = 0) -> int:
    """Get the lexicographic rank of a given combination.

    Args:
        combination (Iterable[int]): The combination to get the lexicographic rank for.
        offset (int, optional): An offset to apply to each value in the combination. Defaults to 0.

    Returns:
        int: The lexicographic rank of the combination.

    Examples:
        >>> get_combination_rank([0, 1, 2])
        0
        >>> get_combination_rank([0, 2, 3])
        2
        >>> get_combination_rank([1, 2, 3], offset=1)
        0
    """
    rank = 0
    for index, value in enumerate(sorted(combination)):
        value -= offset

        if value == index:
            continue

        rank += comb(value, index + 1)

    return rank


def get_combination_from_rank(rank: int, length: int = 2, offset: int = 0) -> list[int]:
    """Get the combination corresponding to a given lexicographic rank.

    Args:
        rank (int): The lexicographic rank of the combination.
        length (int, optional): The length of the combination. Defaults to 2.
        offset (int, optional): An offset to apply to each value in the combination. Defaults to 0.

    Returns:
        list[int]: The combination corresponding to the lexicographic rank.

    Raises:
        ValueError: If the rank or length is negative.

    Examples:
        >>> get_combination_from_rank(0, 3)
        [0, 1, 2]
        >>> get_combination_from_rank(2, 3)
        [0, 2, 3]
        >>> get_combination_from_rank(0, 3, offset=1)
        [1, 2, 3]
    """
    if rank < 0:
        raise ValueError("The rank must not be negative")

    if length < 0:
        raise ValueError("The length must not be negative")

    if length == 0:
        return []

    if length == 1:
        return [rank + offset]

    combination = [0] * length

    binomial = 0
    val = 0
    b = 1
    while b <= rank:
        val += 1
        binomial = b
        b = (b * (val + length)) // val

    for index in range(length - 1, 1, -1):
        rank -= binomial
        binomial = (binomial * (index + 1)) // (val + index)
        combination[index] = val + index + offset

        while binomial > rank:
            val -= 1
            binomial = (binomial * val) // (val + index)

    combination[1] = val + 1 + offset
    combination[0] = rank - binomial + offset

    return combination


class Combination:
    """A class representing a combination of values.

    Args:
        values (CombinationInputValues | CombinationInputWithRank | None, optional): The values of
            the combination. Defaults to None.
        rank (CombinationRank | None, optional): The lexicographic rank of the combination.
            If not provided, it will be calculated on demand from the values. Defaults to None.
        start (int, optional): The starting offset for the combination values.
            Defaults to DEFAULT_START.

    Examples:
        >>> combination = Combination([12, 3, 42, 6, 22])
        >>> combination.values
        [3, 6, 12, 22, 42]
        >>> combination.rank
        755560
        >>> combination.length
        5
        >>> combination.start
        1
    """

    _values: set[CombinationNumber]
    _rank: CombinationRank | None
    _start: int

    def __init__(
        self,
        values: CombinationInputValues | CombinationInputWithRank | None = None,
        rank: CombinationRank | None = None,
        start: int | None = None,
    ) -> None:
        if isinstance(values, dict):
            rank = values.get("rank") if rank is None else rank
            values = values.get("values")

        if isinstance(values, Combination):
            if start is None:
                start = values._start
            rank = values._rank if rank is None else rank
            values = values.get_values(start)

        if not values:
            values = []
            rank = None

        if start is None:
            start = DEFAULT_START

        self._values = set(values)
        self._rank = rank
        self._start = start

    @cached_property
    def values(self) -> CombinationValues:
        """Get the values of the combination as a sorted list.

        Returns:
            CombinationValues: The sorted list of values in the combination.

        Examples:
            >>> combination = Combination([3, 1, 2])
            >>> combination.values
            [1, 2, 3]
        """
        return sorted(self._values)

    @property
    def rank(self) -> CombinationRank:
        """Get the lexicographic rank of the combination.

        Returns:
            CombinationRank: The lexicographic rank of the combination.

        Examples:
            >>> combination = Combination([3, 1, 2])
            >>> combination.rank
            0
        """
        if self._rank is None:
            self._rank = get_combination_rank(self._values, offset=self._start)
        return self._rank

    @cached_property
    def length(self) -> int:
        """Get the length of the combination.

        Returns:
            int: The length of the combination.

        Examples:
            >>> combination = Combination([3, 1, 2])
            >>> combination.length
            3
        """
        return len(self._values)

    @property
    def start(self) -> int:
        """Get the starting offset of the combination.

        Returns:
            int: The starting offset of the combination.

        Examples:
            >>> combination = Combination([3, 1, 2], start=0)
            >>> combination.start
            0
            >>> combination = Combination([3, 1, 2])
            >>> combination.start
            1
        """
        return self._start

    def copy(
        self,
        values: CombinationInputOrRank | None = None,
        rank: CombinationRank | None = None,
        start: int | None = None,
    ) -> Combination:
        """Return a copy of the Combination with optional modifications.

        Args:
            values (CombinationInputOrRank | None): The values of the combination.
                If an integer is provided, it is treated as the lexicographic rank of the
                combination. If None, the current values are used. Defaults to None.
            rank (CombinationRank | None, optional): The lexicographic rank of the combination.
                If not provided, it will be calculated on demand from the values.
                Defaults to None.
            start (int | None): The starting offset for the combination values.
                If None, the current start is used. Defaults to None.

        Returns:
            Combination: A new Combination instance with the specified modifications.

        Examples:
            >>> combination = Combination([4, 5, 6], start=1)
            >>> new_comb = combination.copy(values=[2, 3, 4])
            >>> new_comb.values
            [2, 3, 4]
            >>> new_comb.start
            1
            >>> new_comb = combination.copy(start=2)
            >>> new_comb.values
            [5, 6, 7]
            >>> new_comb.start
            2
        """
        if start is None:
            start = self._start
        if values is None:
            values = self.get_values(start)
            rank = self._rank if self._rank is not None else rank
        return Combination(values=values, rank=rank, start=start)

    def get_values(self, start: int | None = None) -> CombinationValues:
        """Get the values of the combination as a sorted list with an optional new start offset.

        Args:
            start (int, optional): The new starting offset for the values. Defaults to None.

        Returns:
            CombinationValues: The sorted list of combination values with the new offset.
        """
        if start is None or start == self._start:
            return self.values

        offset = start - self._start
        return [value + offset for value in self.values]

    def equals(self, combination: CombinationInput) -> bool:
        """Check if the combination is equal to another combination or lexicographic rank.

        Args:
            combination (CombinationInput): The combination or lexicographic rank to compare with.

        Returns:
            bool: True if the combinations are equal, False otherwise.

        Examples:
            >>> combination1 = Combination([1, 2, 3])
            >>> combination2 = Combination([3, 2, 1])
            >>> combination1.equals(combination2)
            True
            >>> combination1.equals([1, 2, 4])
            False
            >>> rank = get_combination_rank([1, 2, 3], offset=1)
            >>> combination1.equals(rank)
            True
            >>> combination1.equals(rank + 1)
            False
        """
        if isinstance(combination, Combination):
            return self.values == combination.get_values(self._start)

        if isinstance(combination, int):
            return self.rank == combination

        if not combination:
            combination = []

        return self._values == set(combination)

    def includes(self, combination: CombinationNumber | CombinationInputValues) -> bool:
        """Check if the combination includes another combination.

        Args:
            combination (CombinationNumber | CombinationInputValues): The combination to check for
                inclusion, or a single number.

        Returns:
            bool: True if the combination includes the other combination, False otherwise.

        Examples:
            >>> combination1 = Combination([2, 4, 6])
            >>> combination2 = Combination([2, 4])
            >>> combination1.includes(combination2)
            True
            >>> combination1.includes([2, 5])
            False
        """
        if isinstance(combination, CombinationNumber):
            return combination in self._values

        if isinstance(combination, Combination):
            combination = combination.get_values(self._start)

        if not combination:
            combination = []

        return self._values.issuperset(combination)

    def intersects(self, combination: CombinationInputValues | Combination) -> bool:
        """Check if the combination intersects with another combination.

        Args:
            combination (CombinationInputValues | Combination): The combination to check for
                intersection.

        Returns:
            bool: True if the combination intersects with the other combination, False otherwise.

        Examples:
            >>> combination1 = Combination([1, 2, 3])
            >>> combination2 = Combination([3, 4, 5])
            >>> combination1.intersects(combination2)
            True
            >>> combination1.intersects([4, 5, 6])
            False
        """
        if isinstance(combination, Combination):
            combination = combination.get_values(self._start)

        if not combination:
            combination = []

        return not self._values.isdisjoint(combination)

    def intersection(self, combination: CombinationInputValues) -> Combination:
        """Get the intersection of the combination with another combination.

        Args:
            combination (CombinationInputValues | Combination): The combination to intersect with.

        Returns:
            Combination: The intersection of the two combinations.

        Examples:
            >>> combination1 = Combination([1, 2, 3])
            >>> combination2 = Combination([3, 4, 5])
            >>> intersection = combination1.intersection(combination2)
            >>> intersection.values
            [3]
            >>> intersection2 = combination1.intersection([4, 5, 6])
            >>> intersection2.values
            []
        """
        if isinstance(combination, Combination):
            combination = combination.get_values(self._start)

        if not combination:
            combination = []

        return Combination(self._values.intersection(combination), self._start)

    def compares(self, combination: CombinationInput) -> int:
        """Compare the combination with another combination or lexicographic rank.

        Args:
            combination (CombinationInput): The combination or lexicographic rank to compare with.

        Returns:
            int: -1 if self < combination, 0 if self == combination, 1 if self > combination.

        Examples:
            >>> combination1 = Combination([1, 2, 3])
            >>> combination2 = Combination([1, 2, 4])
            >>> combination1.compares(combination2)
            -1
            >>> combination2.compares(combination1)
            1
            >>> combination1.compares([1, 2, 3])
            0
        """
        if isinstance(combination, int):
            if self.rank == combination:
                return 0
            if self.rank > combination:
                return 1
            return -1

        if not isinstance(combination, Combination):
            combination = Combination(combination, start=self._start)

        if self.values == combination.get_values(self._start):
            return 0

        if self.rank - combination.rank > 0:
            return 1

        return -1

    def similarity(self, combination: CombinationInputValues) -> float:
        """Calculate the similarity between the combination and another combination.

        Args:
            combination (CombinationInputValues): The combination to compare with.

        Returns:
            float: The similarity ratio between the two combinations.

        Examples:
            >>> combination1 = Combination([1, 2, 3])
            >>> combination2 = Combination([2, 3, 4])
            >>> combination1.similarity(combination2)
            0.6666666666666666
            >>> combination1.similarity([4, 5, 6])
            0.0
        """
        if self.equals(combination):
            return 1.0

        if self.length == 0:
            return 0.0

        return self.intersection(combination).length / self.length

    def __eq__(self, combination: object) -> bool:
        return self.equals(combination)

    def __ne__(self, combination: object) -> bool:
        return not self.equals(combination)

    def __lt__(self, combination: CombinationInput) -> bool:
        return self.compares(combination) == -1

    def __gt__(self, combination: CombinationInput) -> bool:
        return self.compares(combination) == 1

    def __le__(self, combination: CombinationInput) -> bool:
        return self.compares(combination) != 1

    def __ge__(self, combination: CombinationInput) -> bool:
        return self.compares(combination) != -1

    def __contains__(self, item: CombinationInput) -> bool:
        return self.includes(item)

    def __iter__(self) -> Iterator[CombinationNumber]:
        yield from sorted(self._values)

    def __getitem__(self, index: int) -> CombinationNumber:
        return self.values[index]

    def __len__(self) -> int:
        return len(self._values)

    def __str__(self) -> str:
        return str(self.values)

    def __repr__(self) -> str:
        return f"Combination(values={self.values}, rank={self._rank}, start={self._start})"

    def __hash__(self) -> int:
        return self.rank


class CombinationInputWithRank(TypedDict):
    """Type representing a combination input along with its lexicographic rank."""

    values: CombinationInput
    rank: CombinationRank


CombinationInputValues = CombinationNumbers | Combination
CombinationInput = CombinationRank | CombinationInputValues
CombinationInputOrRank = CombinationInput | CombinationInputWithRank


class BoundCombination(Combination):
    """A class representing a bound combination of values.

    Args:
        values (CombinationInputOrRank | None): The values of the combination.
            If an integer is provided, it is treated as the lexicographic rank of the combination.
        rank (CombinationRank | None, optional): The lexicographic rank of the combination.
            If not provided, it will be calculated on demand from the values. Defaults to None.
        start (int | None): The start value of the combination range. Defaults to DEFAULT_START.
        end (int | None): The end value of the combination range. Defaults to DEFAULT_END.
        count (int | None): The count of numbers in the combination. Defaults to DEFAULT_COUNT.
        combinations (int | None): The total number of possible combinations. If not provided,
            it is calculated based on the start, end, and count.

    Examples:
        >>> bound_comb = BoundCombination(values=10, start=1, end=50, count=5)
        >>> bound_comb.values
        [2, 3, 4, 5, 7]
        >>> bound_comb.end
        50
        >>> bound_comb.count
        5
        >>> bound_comb.combinations
        2118760
    """

    _end: int
    _count: int
    _combinations: int

    def __init__(
        self,
        values: CombinationInputOrRank | None = None,
        rank: CombinationRank | None = None,
        start: int | None = None,
        end: int | None = None,
        count: int | None = None,
        combinations: int | None = None,
    ) -> None:
        if start is None:
            start = DEFAULT_START
        if end is None:
            end = DEFAULT_END
        if count is None:
            count = DEFAULT_COUNT
        if combinations is None:
            combinations = comb(end - start + 1, count)

        if isinstance(values, dict):
            rank = values.get("rank") if rank is None else rank
            values = values.get("values")

        if isinstance(values, Combination):
            rank = values._rank if rank is None else rank
            values = values.get_values(start)
        elif isinstance(values, int):
            rank = rank if rank is not None else values
            values = get_combination_from_rank(values, length=count, offset=start)
        elif not values:
            if rank is not None:
                values = get_combination_from_rank(rank, length=count, offset=start)
            else:
                values = []
                rank = None
        values = [min(max(value, start), end) for value in list(values)[:count]]

        super().__init__(values=values, rank=rank, start=start)
        self._end = end
        self._count = count
        self._combinations = combinations

    @property
    def end(self) -> int:
        """Return the end value of the combination range.

        Returns:
            int: The end value.

        Examples:
            >>> bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)
            >>> bound_comb.end
            50
        """
        return self._end

    @property
    def count(self) -> int:
        """Return the count of numbers in the combination.

        Returns:
            int: The count of numbers.

        Examples:
            >>> bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)
            >>> bound_comb.count
            5
        """
        return self._count

    @property
    def combinations(self) -> int:
        """Return the total number of possible combinations.

        Returns:
            int: The total number of combinations.

        Examples:
            >>> bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)
            >>> bound_comb.combinations
            2118760
        """
        return self._combinations

    def generate(self, n: int = 1, partitions: int = 1) -> list[BoundCombination]:
        """Generate a list of random combinations within the bounds.

        Args:
            n (int): The number of combinations to generate. Defaults to 1.
            partitions (int): The number of partitions to divide the range into for generation.
                Defaults to 1.

        Returns:
            list[BoundCombination]: A list of randomly generated combinations.

        Examples:
            >>> bound_comb = BoundCombination(start=1, end=50, count=5)
            >>> random_combs = bound_comb.generate()
            >>> len(random_combs)
            1
            >>> random_combs[0].values
            [3, 15, 22, 34, 45]
        """
        n = max(1, n)
        partitions = max(1, partitions)
        combinations = self.combinations
        partition = ceil(combinations / partitions)

        return [
            self.copy(
                values=random.randint(
                    partition * (i % partitions),
                    min(partition * (i % partitions + 1) - 1, combinations - 1),
                )
            )
            for i in range(n)
        ]

    def copy(
        self,
        values: CombinationInputOrRank | None = None,
        rank: CombinationRank | None = None,
        start: int | None = None,
        end: int | None = None,
        count: int | None = None,
        combinations: int | None = None,
    ) -> BoundCombination:
        """Return a copy of the BoundCombination with optional modifications.

        Args:
            values (CombinationInputOrRank | None): The values of the combination.
                If an integer is provided, it is treated as the lexicographic rank of the
                combination. If None, the current values are used. Defaults to None.
            rank (CombinationRank | None, optional): The lexicographic rank of the combination. If
                not provided, it will be calculated on demand from the values. Defaults to None.
            start (int | None): The start value of the combination range. If None, the current start
                is used. Defaults to None.
            end (int | None): The end value of the combination range. If None, the current end is
                used. Defaults to None.
            count (int | None): The count of numbers in the combination. If None, the current count
                is used. Defaults to None.
            combinations (int | None): The total number of possible combinations. If None, the
                current combinations are used. Defaults to None.

        Returns:
            BoundCombination: A new BoundCombination instance with the specified modifications.

        Examples:
            >>> bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)
            >>> new_comb = bound_comb.copy(values=15)
            >>> new_comb.values
             [1, 2, 5, 6, 7]
        """
        if start is None:
            start = self._start
        if end is None:
            end = self._end
        if count is None:
            count = self._count
        if (
            combinations is None
            and start == self._start
            and end == self._end
            and count == self._count
        ):
            combinations = self._combinations
        if values is None:
            values = self.get_values(start)
            rank = self._rank if self._rank is not None else rank

        return BoundCombination(
            values=values,
            rank=rank,
            start=start,
            end=end,
            count=count,
            combinations=combinations,
        )

    def __str__(self) -> str:
        n = len(str(self._end))
        sep = ", "
        width = n * self.count + (self.count - 1) * len(sep)
        return f"[{sep.join(f'{value:>{n}}' for value in self.values).rjust(width)}]"

    def __repr__(self) -> str:
        return (
            "BoundCombination("
            f"values={self.values}, "
            f"rank={self._rank}, "
            f"start={self._start}, "
            f"end={self._end}, "
            f"count={self._count}, "
            f"combinations={self._combinations}"
            ")"
        )
