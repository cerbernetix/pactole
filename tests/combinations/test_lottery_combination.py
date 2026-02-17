"""Unit tests for LotteryCombination class."""

import random
from math import ceil

import pytest

from pactole.combinations import (
    BoundCombination,
    LotteryCombination,
    comb,
    get_combination_from_rank,
    get_combination_rank,
)

NUMBER_COUNT = 5
NUMBER_START = 1
NUMBER_END = 50
NUMBER_COMBINATIONS = comb(NUMBER_END - NUMBER_START + 1, NUMBER_COUNT)

EXTRA_COUNT = 3
EXTRA_START = 1
EXTRA_END = 20
EXTRA_COMBINATIONS = comb(EXTRA_END - EXTRA_START + 1, EXTRA_COUNT)

WINNING_RANKS_NUMBERS = {
    (5,): 1,
    (4,): 2,
    (3,): 3,
    (2,): 4,
}

WINNING_RANKS_EXTRA = {
    (5, 3): 1,
    (5, 2): 2,
    (5, 1): 3,
    (5, 0): 4,
    (4, 3): 5,
    (4, 2): 6,
    (4, 1): 7,
    (4, 0): 8,
    (3, 3): 9,
    (3, 2): 10,
    (3, 1): 11,
    (3, 0): 12,
    (2, 3): 13,
    (2, 2): 14,
    (2, 1): 15,
    (2, 0): 16,
}


class TestLotteryCombination:
    """Test suite for LotteryCombination class."""

    def test_combination_empty(self):
        """Test empty LotteryCombination."""

        combination = LotteryCombination()
        assert combination.components == {}
        assert combination.winning_ranks == {}
        assert combination.nb_winning_ranks == 0
        assert combination.min_winning_rank is None
        assert combination.max_winning_rank is None
        assert combination.values == []
        assert combination.rank == 0
        assert combination.length == 0
        assert combination.count == 0
        assert combination.combinations == 0

        combination = LotteryCombination(winning_ranks=WINNING_RANKS_NUMBERS)
        assert combination.components == {}
        assert combination.winning_ranks == WINNING_RANKS_NUMBERS
        assert combination.winning_ranks is not WINNING_RANKS_NUMBERS
        assert combination.nb_winning_ranks == 4
        assert combination.min_winning_rank == 1
        assert combination.max_winning_rank == 4
        assert combination.values == []
        assert combination.rank == 0
        assert combination.length == 0
        assert combination.count == 0
        assert combination.combinations == 0

    def test_combination_from_components(self):
        """Test LotteryCombination construction with components input."""

        numbers = BoundCombination(
            values=[5, 4, 3, 2, 1],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[10, 9, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination = LotteryCombination(numbers=numbers, winning_ranks=WINNING_RANKS_NUMBERS)
        assert combination.components == {"numbers": numbers}
        assert combination.numbers == numbers
        assert combination.winning_ranks == WINNING_RANKS_NUMBERS
        assert combination.winning_ranks is not WINNING_RANKS_NUMBERS
        assert combination.nb_winning_ranks == 4
        assert combination.values == [1, 2, 3, 4, 5]
        assert combination.rank == get_combination_rank([1, 2, 3, 4, 5], offset=1)
        assert combination.length == 5
        assert combination.count == 5
        assert combination.combinations == NUMBER_COMBINATIONS

        combination = LotteryCombination(numbers=numbers, extra=extra)
        assert list(combination.components.keys()) == ["numbers", "extra"]
        assert combination.components == {"numbers": numbers, "extra": extra}
        assert combination.numbers == numbers
        assert combination.extra == extra
        assert combination.winning_ranks == {}
        assert combination.nb_winning_ranks == 0
        assert combination.values == [1, 2, 3, 4, 5, 8, 9, 10]
        assert combination.rank == get_combination_rank(
            [1, 2, 3, 4, 5], offset=1
        ) * EXTRA_COMBINATIONS + get_combination_rank([8, 9, 10], offset=1)
        assert combination.length == 8
        assert combination.count == 8
        assert combination.combinations == NUMBER_COMBINATIONS * EXTRA_COMBINATIONS

        combination = LotteryCombination(extra=extra, numbers=numbers)
        assert list(combination.components.keys()) == ["extra", "numbers"]
        assert combination.components == {"extra": extra, "numbers": numbers}
        assert combination.extra == extra
        assert combination.numbers == numbers
        assert combination.winning_ranks == {}
        assert combination.nb_winning_ranks == 0
        assert combination.values == [8, 9, 10, 1, 2, 3, 4, 5]
        assert combination.rank == get_combination_rank(
            [8, 9, 10], offset=1
        ) * NUMBER_COMBINATIONS + get_combination_rank([1, 2, 3, 4, 5], offset=1)
        assert combination.length == 8
        assert combination.count == 8
        assert combination.combinations == NUMBER_COMBINATIONS * EXTRA_COMBINATIONS

        numbers_exceeded = BoundCombination(
            values=[5, 4, 3, 2, 1, 7, 8, 9],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        combination = LotteryCombination(numbers=numbers_exceeded)
        assert combination.components == {"numbers": numbers}
        assert combination.numbers == numbers
        assert combination.winning_ranks == {}
        assert combination.values == [1, 2, 3, 4, 5]
        assert combination.rank == get_combination_rank([1, 2, 3, 4, 5], offset=1)
        assert combination.length == 5
        assert combination.count == 5
        assert combination.combinations == NUMBER_COMBINATIONS

    def test_combination_from_combination(self):
        """Test LotteryCombination construction with LotteryCombination input."""

        numbers = BoundCombination(
            values=[5, 4, 3, 2, 1],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[10, 9, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        original = LotteryCombination(numbers=numbers, winning_ranks=WINNING_RANKS_NUMBERS)
        assert original.winning_ranks == WINNING_RANKS_NUMBERS

        combination = LotteryCombination(original)
        assert combination.components == {"numbers": numbers}
        assert combination.numbers == numbers
        assert combination.winning_ranks == WINNING_RANKS_NUMBERS
        assert combination.winning_ranks is not WINNING_RANKS_NUMBERS
        assert combination.values == [1, 2, 3, 4, 5]
        assert combination.rank == get_combination_rank([1, 2, 3, 4, 5], offset=1)
        assert combination.length == 5

        combination = LotteryCombination(original, extra=extra)
        assert combination.components == {"numbers": numbers, "extra": extra}
        assert combination.numbers == numbers
        assert combination.extra == extra
        assert combination.winning_ranks == WINNING_RANKS_NUMBERS
        assert combination.winning_ranks is not WINNING_RANKS_NUMBERS
        assert combination.values == [1, 2, 3, 4, 5, 8, 9, 10]
        assert combination.rank == get_combination_rank(
            [1, 2, 3, 4, 5], offset=1
        ) * EXTRA_COMBINATIONS + get_combination_rank([8, 9, 10], offset=1)
        assert combination.length == 8

        original = LotteryCombination(numbers=numbers, extra=extra)
        assert original.winning_ranks == {}

        combination = LotteryCombination(original, winning_ranks=WINNING_RANKS_NUMBERS)
        assert combination.components == {"numbers": numbers, "extra": extra}
        assert combination.numbers == numbers
        assert combination.extra == extra
        assert combination.winning_ranks == WINNING_RANKS_NUMBERS
        assert combination.winning_ranks is not WINNING_RANKS_NUMBERS
        assert combination.values == [1, 2, 3, 4, 5, 8, 9, 10]
        assert combination.rank == get_combination_rank(
            [1, 2, 3, 4, 5], offset=1
        ) * EXTRA_COMBINATIONS + get_combination_rank([8, 9, 10], offset=1)
        assert combination.length == 8

    def test_combination_raise_on_invalid_component(self):
        """Test LotteryCombination raises TypeError on invalid component."""

        with pytest.raises(TypeError):
            _ = LotteryCombination(numbers="invalid_component")

        with pytest.raises(TypeError):
            _ = LotteryCombination(numbers={"values": []})

        with pytest.raises(AttributeError):
            _ = LotteryCombination().numbers

    def test_combination_generate(self):
        """Test the generate method of LotteryCombination."""

        numbers = BoundCombination(
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )
        extra = BoundCombination(
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination = LotteryCombination(numbers=numbers, extra=extra)

        partition1 = combination.combinations
        partition2 = ceil(combination.combinations / 2)
        partition3 = ceil(combination.combinations / 3)
        combinations = set()

        random.seed(42)
        ranks = (
            # generated1
            random.randint(0, partition1 - 1),
            # generated2
            random.randint(0, partition1 - 1),
            random.randint(0, partition1 - 1),
            # generated3
            random.randint(partition3 * 0, partition3 * 1 - 1),
            random.randint(partition3 * 1, partition3 * 2 - 1),
            random.randint(partition3 * 2, partition3 * 3 - 1),
            # generated4
            random.randint(partition2 * 0, partition2 * 1 - 1),
            random.randint(partition2 * 1, partition2 * 2 - 1),
            random.randint(partition2 * 0, partition2 * 1 - 1),
            random.randint(partition2 * 1, partition2 * 2 - 1),
        )
        random.seed(42)

        generated1 = combination.generate()
        for c in generated1:
            combinations.add(c.rank)

        assert len(generated1) == 1
        assert generated1[0].values == get_combination_from_rank(
            ranks[0] // EXTRA_COMBINATIONS, length=5, offset=1
        ) + get_combination_from_rank(ranks[0] % EXTRA_COMBINATIONS, length=3, offset=1)

        generated2 = combination.generate(2)
        for c in generated2:
            combinations.add(c.rank)

        assert len(generated2) == 2
        assert generated2[0].values == get_combination_from_rank(
            ranks[1] // EXTRA_COMBINATIONS, length=5, offset=1
        ) + get_combination_from_rank(ranks[1] % EXTRA_COMBINATIONS, length=3, offset=1)
        assert generated2[1].values == get_combination_from_rank(
            ranks[2] // EXTRA_COMBINATIONS, length=5, offset=1
        ) + get_combination_from_rank(ranks[2] % EXTRA_COMBINATIONS, length=3, offset=1)

        generated3 = combination.generate(3, partitions=3)
        for c in generated3:
            combinations.add(c.rank)

        assert len(generated3) == 3
        assert generated3[0].values == get_combination_from_rank(
            ranks[3] // EXTRA_COMBINATIONS, length=5, offset=1
        ) + get_combination_from_rank(ranks[3] % EXTRA_COMBINATIONS, length=3, offset=1)
        assert generated3[1].values == get_combination_from_rank(
            ranks[4] // EXTRA_COMBINATIONS, length=5, offset=1
        ) + get_combination_from_rank(ranks[4] % EXTRA_COMBINATIONS, length=3, offset=1)
        assert generated3[2].values == get_combination_from_rank(
            ranks[5] // EXTRA_COMBINATIONS, length=5, offset=1
        ) + get_combination_from_rank(ranks[5] % EXTRA_COMBINATIONS, length=3, offset=1)

        generated4 = combination.generate(4, partitions=2)
        for c in generated4:
            combinations.add(c.rank)

        assert len(generated4) == 4
        assert generated4[0].values == get_combination_from_rank(
            ranks[6] // EXTRA_COMBINATIONS, length=5, offset=1
        ) + get_combination_from_rank(ranks[6] % EXTRA_COMBINATIONS, length=3, offset=1)
        assert generated4[1].values == get_combination_from_rank(
            ranks[7] // EXTRA_COMBINATIONS, length=5, offset=1
        ) + get_combination_from_rank(ranks[7] % EXTRA_COMBINATIONS, length=3, offset=1)
        assert generated4[2].values == get_combination_from_rank(
            ranks[8] // EXTRA_COMBINATIONS, length=5, offset=1
        ) + get_combination_from_rank(ranks[8] % EXTRA_COMBINATIONS, length=3, offset=1)
        assert generated4[3].values == get_combination_from_rank(
            ranks[9] // EXTRA_COMBINATIONS, length=5, offset=1
        ) + get_combination_from_rank(ranks[9] % EXTRA_COMBINATIONS, length=3, offset=1)

        for c in combination.generate(5):
            combinations.add(c.rank)

        assert len(combinations) == 15

    def test_combination_copy(self):
        """Test LotteryCombination copy method."""

        numbers = BoundCombination(
            values=[3, 5, 18, 29, 42],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )
        numbers2 = BoundCombination(
            values=[6, 9, 12],
            count=3,
            start=1,
            end=10,
        )

        extra = BoundCombination(
            values=[10, 9, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination = LotteryCombination(
            numbers=numbers, extra=extra, winning_ranks=WINNING_RANKS_NUMBERS
        )

        combination2 = combination.copy()
        assert isinstance(combination2, LotteryCombination)
        assert combination2 is not combination
        assert combination2.components == combination.components
        assert combination2.numbers == combination.numbers
        assert combination2.extra == combination.extra
        assert combination2.winning_ranks == combination.winning_ranks
        assert combination2.values == combination.values
        assert combination2.rank == combination.rank
        assert combination2.length == combination.length
        assert combination2.count == combination.count
        assert combination2.combinations == combination.combinations

        combination2 = combination.copy(winning_ranks=WINNING_RANKS_EXTRA)
        assert isinstance(combination2, LotteryCombination)
        assert combination2 is not combination
        assert combination2.components == combination.components
        assert combination2.numbers == combination.numbers
        assert combination2.extra == combination.extra
        assert combination2.winning_ranks == WINNING_RANKS_EXTRA
        assert combination2.values == combination.values
        assert combination2.rank == combination.rank
        assert combination2.length == combination.length
        assert combination2.count == combination.count
        assert combination2.combinations == combination.combinations

        combination2 = combination.copy(numbers=numbers2)
        assert isinstance(combination2, LotteryCombination)
        assert combination2 is not combination
        assert combination2.components == {"numbers": numbers2, "extra": extra}
        assert combination2.numbers == numbers2
        assert combination2.extra == combination.extra
        assert combination2.winning_ranks == combination.winning_ranks
        assert combination2.values == numbers2.get_values() + extra.get_values()
        assert combination2.rank == numbers2.rank * extra.combinations + extra.rank
        assert combination2.length == extra.count + numbers2.count
        assert combination2.count == extra.count + numbers2.count
        assert combination2.combinations == extra.combinations * numbers2.combinations

    def test_combination_get_combination(self):
        """Test LotteryCombination get_combination method."""

        numbers = BoundCombination(
            values=[5, 4, 3, 2, 1],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[10, 9, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination = LotteryCombination(
            numbers=numbers, extra=extra, winning_ranks=WINNING_RANKS_NUMBERS
        )

        combination2 = combination.get_combination([2, 3, 4, 5, 6, 7, 8])
        assert isinstance(combination2, LotteryCombination)
        assert combination2.values == [2, 3, 4, 5, 6, 7, 8]
        assert combination2.get_component_values("numbers") == [2, 3, 4, 5, 6]
        assert combination2.get_component_values("extra") == [7, 8]
        assert combination2.winning_ranks == WINNING_RANKS_NUMBERS

        new_combination = combination.get_combination([2, 3, 4, 5, 6, 7, 8], extra=[12, 17])
        assert isinstance(new_combination, LotteryCombination)
        assert new_combination.values == [2, 3, 4, 5, 6, 12, 17]
        assert new_combination.get_component_values("numbers") == [2, 3, 4, 5, 6]
        assert new_combination.get_component_values("extra") == [12, 17]
        assert new_combination.winning_ranks == WINNING_RANKS_NUMBERS

        new_combination = combination.get_combination(extra=[12, 17])
        assert isinstance(new_combination, LotteryCombination)
        assert new_combination.values == [12, 17]
        assert new_combination.get_component_values("extra") == [12, 17]
        assert new_combination.winning_ranks == WINNING_RANKS_NUMBERS

        new_combination = combination.get_combination(combination2)
        assert isinstance(new_combination, LotteryCombination)
        assert new_combination.values == [2, 3, 4, 5, 6, 7, 8]
        assert new_combination.winning_ranks == WINNING_RANKS_NUMBERS

        new_combination = combination.get_combination(combination2, extra=[12, 17])
        assert isinstance(new_combination, LotteryCombination)
        assert new_combination.values == [2, 3, 4, 5, 6, 12, 17]
        assert new_combination.winning_ranks == WINNING_RANKS_NUMBERS

        new_combination = combination.get_combination(
            combination2, winning_ranks=WINNING_RANKS_EXTRA
        )
        assert isinstance(new_combination, LotteryCombination)
        assert new_combination.values == [2, 3, 4, 5, 6, 7, 8]
        assert new_combination.winning_ranks == WINNING_RANKS_EXTRA

        new_combination = combination.get_combination(numbers=[6, 7, 8, 9, 10])
        assert isinstance(new_combination, LotteryCombination)
        assert new_combination.values == [6, 7, 8, 9, 10]
        assert new_combination.winning_ranks == WINNING_RANKS_NUMBERS

        new_combination = combination.get_combination(
            numbers=[6, 7, 8, 9, 10], extra=[15, 16, 17], winning_ranks=WINNING_RANKS_EXTRA
        )
        assert isinstance(new_combination, LotteryCombination)
        assert new_combination.values == [6, 7, 8, 9, 10, 15, 16, 17]
        assert new_combination.winning_ranks == WINNING_RANKS_EXTRA

        new_combination = new_combination.get_combination(combination.rank)
        assert isinstance(new_combination, LotteryCombination)
        assert new_combination.values == [1, 2, 3, 4, 5, 8, 9, 10]
        assert new_combination.winning_ranks == WINNING_RANKS_EXTRA

        with pytest.raises(KeyError):
            _ = combination.get_combination(numbers=[6, 7, 8, 9, 10], stars=[3, 4])

    def test_combination_getting_components(self):
        """Test LotteryCombination getting components."""

        numbers = BoundCombination(
            values=[5, 4, 3, 2, 1],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[10, 9, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination = LotteryCombination(numbers=numbers, extra=extra)

        components = combination.get_components()
        assert components == {}

        components = combination.get_components(numbers=[4, 5, 6, 7, 8])
        assert components == {
            "numbers": numbers.copy(values=[4, 5, 6, 7, 8]),
        }

        components = combination.get_components(extra=[18, 19, 20])
        assert components == {
            "extra": extra.copy(values=[18, 19, 20]),
        }

        components = combination.get_components(numbers=[4, 5, 6, 7, 8], extra=[18, 19, 20])
        assert components == {
            "numbers": numbers.copy(values=[4, 5, 6, 7, 8]),
            "extra": extra.copy(values=[18, 19, 20]),
        }

        retrieved_numbers = combination.get_component("numbers")
        assert retrieved_numbers == numbers

        retrieved_extra = combination.get_component("extra")
        assert retrieved_extra == extra

        retrieved_none = combination.get_component("nonexistent")
        assert retrieved_none is None

    def test_combination_getting_values(self):
        """Test LotteryCombination getting values."""

        numbers = BoundCombination(
            values=[5, 4, 3, 2, 1],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[10, 9, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination = LotteryCombination(numbers=numbers, extra=extra)

        assert combination.get_component_values("numbers") == [1, 2, 3, 4, 5]
        assert combination.get_component_values("extra") == [8, 9, 10]
        assert combination.get_component_values("nonexistent") == []

    def test_combination_get_winning_rank(self):
        """Test LotteryCombination winning rank calculation."""

        numbers = BoundCombination(
            values=[1, 2, 3, 4, 5],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[6, 7, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination = LotteryCombination(numbers=numbers, winning_ranks=WINNING_RANKS_NUMBERS)

        assert combination.get_winning_rank() is None

        assert combination.get_winning_rank(numbers=[1, 2, 3, 4, 5]) == 1

        assert combination.get_winning_rank(numbers=[1, 2, 3, 4, 6]) == 2
        assert combination.get_winning_rank(numbers=[1, 2, 3, 4]) == 2

        assert combination.get_winning_rank(numbers=[1, 2, 3, 6, 7]) == 3
        assert combination.get_winning_rank(numbers=[1, 2, 3]) == 3

        assert combination.get_winning_rank(numbers=[1, 2, 7, 8, 9]) == 4
        assert combination.get_winning_rank(numbers=[1, 2]) == 4

        assert combination.get_winning_rank(numbers=[1, 6, 7, 8, 9]) is None
        assert combination.get_winning_rank(numbers=[1]) is None
        assert combination.get_winning_rank(numbers=[6, 7, 8, 9, 10]) is None

        combination = LotteryCombination(
            numbers=numbers, extra=extra, winning_ranks=WINNING_RANKS_EXTRA
        )

        assert combination.get_winning_rank(numbers=[1, 2, 3, 4, 5], extra=[6, 7, 8]) == 1
        assert combination.get_winning_rank(numbers=[1, 2, 3, 4, 5], extra=[6, 7, 9]) == 2
        assert combination.get_winning_rank(numbers=[1, 2, 3, 4, 5], extra=[6, 9, 10]) == 3
        assert combination.get_winning_rank(numbers=[1, 2, 3, 4, 5], extra=[9, 10, 11]) == 4

        assert combination.get_winning_rank(numbers=[1, 2, 3, 4, 6], extra=[6, 7, 8]) == 5
        assert combination.get_winning_rank(numbers=[1, 2, 3, 4, 6], extra=[6, 7, 9]) == 6
        assert combination.get_winning_rank(numbers=[1, 2, 3, 4, 6], extra=[6, 9, 10]) == 7
        assert combination.get_winning_rank(numbers=[1, 2, 3, 4, 6], extra=[9, 10, 11]) == 8

        assert combination.get_winning_rank(numbers=[1, 2, 3, 6, 7], extra=[6, 7, 8]) == 9
        assert combination.get_winning_rank(numbers=[1, 2, 3, 6, 7], extra=[6, 7, 9]) == 10
        assert combination.get_winning_rank(numbers=[1, 2, 3, 6, 7], extra=[6, 9, 10]) == 11
        assert combination.get_winning_rank(numbers=[1, 2, 3, 6, 7], extra=[9, 10, 11]) == 12

        assert combination.get_winning_rank(numbers=[1, 2, 6, 7, 8], extra=[6, 7, 8]) == 13
        assert combination.get_winning_rank(numbers=[1, 2, 6, 7, 8], extra=[6, 7, 9]) == 14
        assert combination.get_winning_rank(numbers=[1, 2, 6, 7, 8], extra=[6, 9, 10]) == 15
        assert combination.get_winning_rank(numbers=[1, 2, 6, 7, 8], extra=[9, 10, 11]) == 16

        assert combination.get_winning_rank(numbers=[1, 6, 7, 8, 9], extra=[6, 7, 8]) is None
        assert combination.get_winning_rank() is None

        with pytest.raises(KeyError):
            _ = combination.get_winning_rank(numbers=[1, 2, 3, 4, 5], stars=[1, 2])

    def test_combination_equality(self):
        """Test LotteryCombination equality comparisons."""

        numbers = BoundCombination(
            values=[1, 2, 3, 4, 5],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[6, 7, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        numbers_rank = get_combination_rank([1, 2, 3, 4, 5], offset=1)
        extra_rank = get_combination_rank([6, 7, 8], offset=1)

        combination = LotteryCombination(numbers=numbers, extra=extra)

        combination1 = combination.get_combination(numbers=[1, 2, 3, 4, 5], extra=[6, 7, 8])
        combination2 = combination.get_combination(numbers=[1, 2, 3, 4, 5], extra=[6, 7, 8])
        combination3 = combination.get_combination(numbers=[1, 2, 4, 5, 7], extra=[6, 7, 8])

        assert LotteryCombination() == LotteryCombination()
        assert LotteryCombination().equals()

        assert combination1
        assert not combination1.equals()

        assert combination1 == combination2
        assert combination1 != combination3

        assert combination1.equals(combination1)
        assert combination1.equals(combination2)
        assert not combination1.equals(combination3)

        assert combination1.equals([1, 2, 3, 4, 5, 6, 7, 8])
        assert combination1.equals(numbers=[1, 2, 3, 4, 5], extra=[6, 7, 8])
        assert not combination1.equals(numbers=[1, 2, 4, 5, 7], extra=[6, 7, 8])
        assert not combination1.equals(numbers=[1, 2, 3, 4, 5], extra=[6, 7, 9])
        assert not combination1.equals(numbers=[1, 2, 3, 4, 5])
        assert not combination1.equals(extra=[6, 7, 8])

        assert combination1.equals(numbers=numbers_rank, extra=extra_rank)
        assert not combination1.equals(numbers=numbers_rank + 1, extra=extra_rank)

        assert combination1.equals(numbers_rank * EXTRA_COMBINATIONS + extra_rank)

        with pytest.raises(KeyError):
            _ = combination1.equals(numbers=[1, 2, 3, 4, 5], dummy=[6, 7, 8])

    def test_combination_includes(self):
        """Test LotteryCombination includes method."""

        numbers = BoundCombination(
            values=[1, 2, 3, 4, 5],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[6, 7, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination1 = LotteryCombination(numbers=numbers, extra=extra)
        combination2 = LotteryCombination(numbers=numbers.copy(values=[1, 2]))
        combination3 = LotteryCombination(numbers=numbers.copy(values=[2, 6]))

        assert combination1.includes([])
        assert combination1.includes([2])
        assert combination1.includes([2, 4])

        assert not combination1.includes([2, 6])
        assert not combination1.includes([6])

        assert combination1.includes(combination2)
        assert not combination1.includes(combination3)

        assert combination1.includes([1, 2, 3, 4, 5, 6, 7, 8])
        assert combination1.includes(numbers=[1, 2, 3, 4, 5])
        assert combination1.includes(numbers=[3, 4])
        assert not combination1.includes(numbers=[1, 2, 3, 4, 8])
        assert not combination1.includes(numbers=[5, 6])

        assert combination1.includes(extra=[6, 7, 8])
        assert combination1.includes(extra=[6, 7])
        assert not combination1.includes([6, 7, 8])
        assert not combination1.includes(extra=[6, 7, 9])
        assert not combination1.includes(extra=[5, 8])

        with pytest.raises(KeyError):
            _ = combination1.includes(dummy=[1, 2])

        assert 4 in combination1
        assert 9 not in combination1

        assert [2, 4] in combination1
        assert [2, 6] not in combination1

        assert combination2 in combination1
        assert combination3 not in combination1

    def test_combination_intersects(self):
        """Test LotteryCombination intersects method."""

        numbers = BoundCombination(
            values=[1, 2, 3, 4, 5],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )
        extra = BoundCombination(
            values=[6, 7, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination1 = LotteryCombination(numbers=numbers, extra=extra)
        combination2 = LotteryCombination(numbers=numbers.copy(values=[1, 3, 5, 6, 7]))
        combination3 = LotteryCombination(numbers=numbers.copy(values=[6, 7, 8, 9, 10]))

        assert combination1.intersects([3])
        assert combination1.intersects([3, 4])
        assert combination1.intersects([3, 4, 5])
        assert combination1.intersects(numbers=[1, 2, 3, 4, 5])
        assert combination1.intersects(extra=[6, 7, 8])
        assert combination1.intersects(numbers=[5])
        assert combination1.intersects(extra=[6])

        assert not combination1.intersects(numbers=[6])
        assert not combination1.intersects(extra=[5])
        assert not combination1.intersects([6, 7, 8])
        assert not combination1.intersects([6, 7])
        assert not combination1.intersects([6])
        assert not combination1.intersects([])
        assert not combination1.get_combination().intersects([1, 2, 3, 4, 5])

        assert combination1.intersects(combination2)
        assert not combination1.intersects(combination3)

        with pytest.raises(KeyError):
            _ = combination1.intersects(dummy=[1, 2])

    def test_combination_intersection(self):
        """Test LotteryCombination intersection method."""

        numbers = BoundCombination(
            values=[1, 2, 3, 4, 5],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )
        extra = BoundCombination(
            values=[6, 7, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination1 = LotteryCombination(numbers=numbers, extra=extra)
        combination2 = LotteryCombination(numbers=numbers.copy(values=[1, 3, 5, 6, 7]))
        combination3 = LotteryCombination(numbers=numbers.copy(values=[1, 3, 5, 6, 7]), extra=extra)
        combination4 = LotteryCombination(numbers=numbers.copy(values=[6, 7, 8, 9, 10]))

        intersection1 = combination1.intersection([1, 3, 5, 6, 7])
        intersection2 = combination1.intersection([6, 7, 8, 9, 10])

        assert isinstance(intersection1, LotteryCombination)
        assert isinstance(intersection2, LotteryCombination)

        assert intersection1.values == [1, 3, 5]
        assert intersection1.length == 3
        assert intersection1.count == 8

        assert not intersection2.values
        assert intersection2.length == 0
        assert intersection2.count == 8

        assert combination1.intersection(combination2).values == [1, 3, 5]
        assert combination1.intersection(combination3).values == [1, 3, 5, 6, 7, 8]
        assert not combination1.intersection(combination4).values

        assert combination1.intersection([1, 2, 5, 6, 7, 3, 5]).values == [1, 2, 5]
        assert combination1.intersection([6, 7, 8, 9, 10, 3, 6, 7]).values == [6, 7]
        assert combination1.intersection(numbers=[1, 2, 5, 6, 7]).values == [1, 2, 5]
        assert combination1.intersection(extra=[3, 6, 7]).values == [6, 7]

        with pytest.raises(KeyError):
            _ = combination1.intersection(dummy=[1, 2])

    def test_combination_compares(self):
        """Test LotteryCombination compares method."""

        numbers = BoundCombination(
            values=[1, 2, 3, 4, 5],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )
        extra = BoundCombination(
            values=[6, 7, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination1 = LotteryCombination(numbers=numbers, extra=extra)
        combination2 = LotteryCombination(numbers=numbers.copy(values=[1, 3, 5, 6, 7]))
        combination3 = LotteryCombination(combination1)

        assert combination1.compares() == 1
        assert LotteryCombination().compares(combination1) == -1
        assert LotteryCombination().compares() == 0

        assert combination1.compares([1, 3, 5, 6, 7]) == -1
        assert combination2.compares([1, 2, 3, 4, 5]) == 1
        assert combination1.compares([1, 2, 3, 4, 5, 6, 7, 8]) == 0

        assert combination1.compares(numbers=[1, 2, 3, 4, 5], extra=[6, 7, 8]) == 0
        assert combination1.compares(numbers=[1, 2, 3, 4, 5], extra=[5, 7, 8]) == 1
        assert combination1.compares(numbers=[1, 2, 3, 4, 6], extra=[6, 7, 8]) == -1

        assert combination1.compares(numbers=[1, 2, 3, 4, 5]) == 0
        assert combination1.compares(numbers=[1, 2, 3, 4, 6]) == -1
        assert combination1.compares(extra=[6, 7, 8]) == 0
        assert combination1.compares(extra=[5, 7, 8]) == 1

        assert combination1.compares([1, 3, 5, 6, 7]) == -1
        assert combination2.compares([1, 2, 3, 4, 5]) == 1

        assert combination1.compares(combination2) == -1
        assert combination2.compares(combination1) == 1
        assert combination1.compares(combination1) == 0
        assert combination1.compares(combination3) == 0

        with pytest.raises(KeyError):
            _ = combination1.compares(numbers=[1, 2, 3, 4, 5], dummy=[6, 7, 8])

        assert combination1 < combination2
        assert combination1 <= combination2
        assert combination1 == combination3
        assert combination2 > combination1
        assert combination2 >= combination1

    def test_combination_similarity(self):
        """Test LotteryCombination similarity method."""

        numbers = BoundCombination(
            values=[1, 2, 3, 4, 5],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )
        extra = BoundCombination(
            values=[6, 7, 8],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination1 = LotteryCombination(numbers=numbers, extra=extra)
        combination2 = LotteryCombination(numbers=numbers.copy(values=[1, 3, 5, 6, 7]))
        combination3 = LotteryCombination(
            numbers=BoundCombination(
                values=[6, 7, 8, 9, 10],
                count=NUMBER_COUNT,
                start=NUMBER_START,
                end=NUMBER_END,
                combinations=NUMBER_COMBINATIONS,
            ),
            extra=extra,
        )

        assert LotteryCombination().similarity() == 1
        assert LotteryCombination().similarity([1, 2, 3, 4, 5]) == 1

        assert combination1.similarity() == 0

        assert combination1.similarity([1, 2, 3, 4, 5, 6, 7, 8]) == 1
        assert combination1.similarity([1, 2, 3, 4, 5]) == 5 / 8
        assert combination1.similarity([1, 3, 5, 6, 7]) == 3 / 8
        assert combination1.similarity([6, 7, 8, 9, 10]) == 0
        assert combination1.similarity([1, 3, 5, 6, 7]) == 3 / 8
        assert combination1.similarity([6, 7, 8, 9, 10]) == 0

        assert combination1.similarity(numbers=[1, 2, 3, 4, 5], extra=[6, 7, 8]) == 1
        assert combination1.similarity(numbers=[1, 2, 3, 4, 5], extra=[6, 7, 9]) == 7 / 8
        assert combination1.similarity(numbers=[1, 2, 3, 4, 6], extra=[6, 7, 9]) == 6 / 8
        assert combination1.similarity(numbers=[1, 2, 3, 4, 6]) == 4 / 8
        assert combination1.similarity(extra=[6, 7, 9]) == 2 / 8

        assert combination1.similarity(combination1) == 1
        assert combination1.similarity(combination2) == 3 / 8
        assert combination1.similarity(combination3) == 3 / 8
        assert combination1.similarity(combination3, extra=[1, 2, 3]) == 0

        with pytest.raises(KeyError):
            _ = combination1.similarity(dummy=[1, 2, 3, 4, 5])

    def test_combination_iteration(self):
        """Test LotteryCombination iteration."""

        numbers = BoundCombination(
            values=[5, 4, 3, 2, 1],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[8, 7, 6],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination = LotteryCombination(numbers=numbers, extra=extra)
        assert list(combination) == [1, 2, 3, 4, 5, 6, 7, 8]

    def test_combination_access(self):
        """Test LotteryCombination item access."""

        numbers = BoundCombination(
            values=[5, 4, 3, 2, 1],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[8, 7, 6],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination = LotteryCombination(numbers=numbers, extra=extra)

        assert combination[0] == 1
        assert combination[1] == 2
        assert combination[2] == 3
        assert combination[3] == 4
        assert combination[4] == 5
        assert combination[5] == 6
        assert combination[6] == 7
        assert combination[7] == 8

        with pytest.raises(IndexError):
            _ = combination[8]

    def test_combination_length(self):
        """Test LotteryCombination length method."""

        numbers = BoundCombination(
            values=[5, 4, 3, 2, 1],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[8, 7, 6],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination = LotteryCombination(numbers=numbers, extra=extra)

        assert len(combination) == 8
        assert combination.length == 8

    def test_combination_string(self):
        """Test LotteryCombination string representation."""

        numbers = BoundCombination(
            values=[3, 6, 12, 33, 42],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[6, 7, 12],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination = LotteryCombination(numbers=numbers, extra=extra)

        assert str(combination) == "numbers: [ 3,  6, 12, 33, 42] extra: [ 6,  7, 12]"

        combination = combination.get_combination(numbers=[3, 6, 12], extra=[7, 12])

        assert str(combination) == "numbers: [         3,  6, 12] extra: [     7, 12]"

    def test_combination_repr(self):
        """Test LotteryCombination repr representation."""

        numbers = BoundCombination(
            values=[5, 4, 3, 2, 1],
            rank=12345,
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[8, 7, 6],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination = LotteryCombination(numbers=numbers, extra=extra)

        numbers_repr = (
            "BoundCombination("
            "values=[1, 2, 3, 4, 5], "
            "rank=12345, "
            f"start={NUMBER_START}, "
            f"end={NUMBER_END}, "
            f"count={NUMBER_COUNT}, "
            f"combinations={NUMBER_COMBINATIONS}"
            ")"
        )

        extra_repr = (
            "BoundCombination("
            "values=[6, 7, 8], "
            "rank=None, "
            f"start={EXTRA_START}, "
            f"end={EXTRA_END}, "
            f"count={EXTRA_COUNT}, "
            f"combinations={EXTRA_COMBINATIONS}"
            ")"
        )

        winning_ranks_repr = "{}"

        assert repr(combination) == (
            f"LotteryCombination(numbers={numbers_repr}, "
            f"extra={extra_repr}, "
            f"winning_ranks={winning_ranks_repr})"
        )

        assert repr(LotteryCombination()) == (
            f"LotteryCombination(winning_ranks={winning_ranks_repr})"
        )

    def test_combination_hash(self):
        """Test LotteryCombination hash method."""

        numbers = BoundCombination(
            values=[5, 4, 3, 2, 1],
            count=NUMBER_COUNT,
            start=NUMBER_START,
            end=NUMBER_END,
            combinations=NUMBER_COMBINATIONS,
        )

        extra = BoundCombination(
            values=[8, 7, 6],
            count=EXTRA_COUNT,
            start=EXTRA_START,
            end=EXTRA_END,
            combinations=EXTRA_COMBINATIONS,
        )

        combination1 = LotteryCombination(numbers=numbers)
        combination2 = LotteryCombination(numbers=numbers)
        combination3 = LotteryCombination(numbers=numbers, extra=extra)

        assert hash(combination1) == hash(combination2)
        assert hash(combination1) != hash(combination3)
        assert hash(combination1) == combination1.rank
