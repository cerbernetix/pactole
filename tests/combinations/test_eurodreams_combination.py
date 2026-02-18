"""Unit tests for EuroDreamsCombination class."""

import random
from math import ceil

import pytest

from pactole.combinations import (
    CombinationInputWithRank,
    EuroDreamsCombination,
    get_combination_from_rank,
    get_combination_rank,
)


class TestEuroDreamsCombination:
    """Test suite for EuroDreamsCombination class."""

    def test_combination_empty(self):
        """Test empty EuroDreamsCombination."""

        combination = EuroDreamsCombination()
        assert combination.numbers == []
        assert combination.dream == []
        assert combination.nb_winning_ranks == 6
        assert combination.min_winning_rank == 1
        assert combination.max_winning_rank == 6
        assert combination.values == []
        assert combination.rank == 0
        assert combination.length == 0

    def test_combination_from_values(self):
        """Test EuroDreamsCombination construction with number inputs."""

        combination = EuroDreamsCombination(numbers=[3, 2, 1])
        assert combination.numbers == [1, 2, 3]
        assert combination.dream == []
        assert combination.values == [1, 2, 3]
        assert combination.rank == get_combination_rank([1, 2, 3], offset=1)
        assert combination.length == 3

        combination = EuroDreamsCombination(numbers=[3, 2, 1], dream=[3])
        assert combination.numbers == [1, 2, 3]
        assert combination.dream == [3]
        assert combination.values == [1, 2, 3, 3]
        assert combination.rank == get_combination_rank(
            [1, 2, 3], offset=1
        ) * 5 + get_combination_rank([3], offset=1)
        assert combination.length == 4

        combination = EuroDreamsCombination(dream=[3])
        assert combination.numbers == []
        assert combination.dream == [3]
        assert combination.values == [3]
        assert combination.rank == get_combination_rank([3], offset=1)
        assert combination.length == 1

        combination = EuroDreamsCombination([3, 5, 2, 4, 1, 6, 7, 8])
        assert combination.numbers == [1, 2, 3, 4, 5, 6]
        assert combination.dream == [5]
        assert combination.values == [1, 2, 3, 4, 5, 6, 5]
        assert combination.rank == get_combination_rank(
            [1, 2, 3, 4, 5, 6], offset=1
        ) * 5 + get_combination_rank([5], offset=1)
        assert combination.length == 7

    def test_combination_from_combination(self):
        """Test EuroDreamsCombination construction with EuroDreamsCombination input."""

        original = EuroDreamsCombination(numbers=[1, 2, 3, 4, 5, 6], dream=[3])
        combination = EuroDreamsCombination(original)
        assert combination.numbers == original.numbers
        assert combination.dream == original.dream
        assert combination.values == original.values
        assert combination.rank == original.rank
        assert combination.length == original.length

        combination = EuroDreamsCombination(original, dream=[2])
        assert combination.numbers == original.numbers
        assert combination.dream == [2]
        assert combination.values == original.numbers.values + [2]
        assert combination.rank == original.numbers.rank * 5 + +get_combination_rank([2], offset=1)
        assert combination.length == original.length

    def test_combination_from_ranks(self):
        """Test EuroDreamsCombination construction with rank inputs."""

        number_rank = get_combination_rank([1, 2, 3, 4, 5, 6], offset=1)
        dream_rank = get_combination_rank([3], offset=1)
        total_rank = number_rank * 5 + dream_rank

        combination = EuroDreamsCombination(numbers=number_rank, dream=dream_rank)
        assert combination.numbers == [1, 2, 3, 4, 5, 6]
        assert combination.dream == [3]
        assert combination.values == [1, 2, 3, 4, 5, 6, 3]
        assert combination.rank == total_rank
        assert combination.length == 7

    def test_combination_from_component_ranks(self):
        """Test EuroDreamsCombination construction with component rank dictionaries."""

        numbers_rank = get_combination_rank([1, 2, 3, 4, 5, 6], offset=1)
        dream_rank = get_combination_rank([3], offset=1)

        combination = EuroDreamsCombination(
            numbers=CombinationInputWithRank(values=[6, 2, 1, 4, 5, 3], rank=numbers_rank),
            dream=CombinationInputWithRank(values=[3], rank=dream_rank),
        )

        assert combination.numbers == [1, 2, 3, 4, 5, 6]
        assert combination.dream == [3]
        assert combination.values == [1, 2, 3, 4, 5, 6, 3]
        assert combination.numbers.rank == numbers_rank
        assert combination.dream.rank == dream_rank
        assert combination.rank == numbers_rank * 5 + dream_rank
        assert combination.length == 7

    def test_combination_generate(self):
        """Test the generate method of EuroDreamsCombination."""

        combination = EuroDreamsCombination()

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
            ranks[0] // combination.dream.combinations, length=6, offset=1
        ) + get_combination_from_rank(ranks[0] % combination.dream.combinations, length=1, offset=1)

        generated2 = combination.generate(2)
        for c in generated2:
            combinations.add(c.rank)

        assert len(generated2) == 2
        assert generated2[0].values == get_combination_from_rank(
            ranks[1] // combination.dream.combinations, length=6, offset=1
        ) + get_combination_from_rank(ranks[1] % combination.dream.combinations, length=1, offset=1)
        assert generated2[1].values == get_combination_from_rank(
            ranks[2] // combination.dream.combinations, length=6, offset=1
        ) + get_combination_from_rank(ranks[2] % combination.dream.combinations, length=1, offset=1)

        generated3 = combination.generate(3, partitions=3)
        for c in generated3:
            combinations.add(c.rank)

        assert len(generated3) == 3
        assert generated3[0].values == get_combination_from_rank(
            ranks[3] // combination.dream.combinations, length=6, offset=1
        ) + get_combination_from_rank(ranks[3] % combination.dream.combinations, length=1, offset=1)
        assert generated3[1].values == get_combination_from_rank(
            ranks[4] // combination.dream.combinations, length=6, offset=1
        ) + get_combination_from_rank(ranks[4] % combination.dream.combinations, length=1, offset=1)
        assert generated3[2].values == get_combination_from_rank(
            ranks[5] // combination.dream.combinations, length=6, offset=1
        ) + get_combination_from_rank(ranks[5] % combination.dream.combinations, length=1, offset=1)

        generated4 = combination.generate(4, partitions=2)
        for c in generated4:
            combinations.add(c.rank)

        assert len(generated4) == 4
        assert generated4[0].values == get_combination_from_rank(
            ranks[6] // combination.dream.combinations, length=6, offset=1
        ) + get_combination_from_rank(ranks[6] % combination.dream.combinations, length=1, offset=1)
        assert generated4[1].values == get_combination_from_rank(
            ranks[7] // combination.dream.combinations, length=6, offset=1
        ) + get_combination_from_rank(ranks[7] % combination.dream.combinations, length=1, offset=1)
        assert generated4[2].values == get_combination_from_rank(
            ranks[8] // combination.dream.combinations, length=6, offset=1
        ) + get_combination_from_rank(ranks[8] % combination.dream.combinations, length=1, offset=1)
        assert generated4[3].values == get_combination_from_rank(
            ranks[9] // combination.dream.combinations, length=6, offset=1
        ) + get_combination_from_rank(ranks[9] % combination.dream.combinations, length=1, offset=1)

        for c in combination.generate(5):
            combinations.add(c.rank)

        assert len(combinations) == 15

    def test_combination_copy(self):
        """Test EuroDreamsCombination copy method."""

        combination = EuroDreamsCombination(numbers=[2, 3, 5, 7, 9, 38], dream=[3])

        combination_copy = combination.copy()
        assert isinstance(combination_copy, EuroDreamsCombination)
        assert combination_copy is not combination
        assert combination_copy.numbers == combination.numbers
        assert combination_copy.dream == combination.dream
        assert combination_copy.winning_ranks == combination.winning_ranks
        assert combination_copy.values == combination.values
        assert combination_copy.rank == combination.rank
        assert combination_copy.length == combination.length
        assert combination_copy.count == combination.count
        assert combination_copy.combinations == combination.combinations

        combination_copy = combination.copy(numbers=[1, 2, 3, 4, 5, 6])
        assert isinstance(combination_copy, EuroDreamsCombination)
        assert combination_copy is not combination
        assert combination_copy.numbers == [1, 2, 3, 4, 5, 6]
        assert combination_copy.dream == combination.dream
        assert combination_copy.winning_ranks == combination.winning_ranks
        assert combination_copy.values == [1, 2, 3, 4, 5, 6, 3]
        assert (
            combination_copy.rank
            == get_combination_rank([1, 2, 3, 4, 5, 6], offset=1) * 5 + combination.dream.rank
        )
        assert combination_copy.length == combination.length
        assert combination_copy.count == combination.count
        assert combination_copy.combinations == combination.combinations

        combination_copy = combination.copy(dream=[5])
        assert isinstance(combination_copy, EuroDreamsCombination)
        assert combination_copy is not combination
        assert combination_copy.numbers == combination.numbers
        assert combination_copy.dream == [5]
        assert combination_copy.winning_ranks == combination.winning_ranks
        assert combination_copy.values == combination.numbers.values + [5]
        assert combination_copy.rank == combination.numbers.rank * 5 + get_combination_rank(
            [5], offset=1
        )
        assert combination_copy.length == combination.length
        assert combination_copy.count == combination.count
        assert combination_copy.combinations == combination.combinations

    def test_combination_get_combination(self):
        """Test EuroDreamsCombination get_combination method."""

        combination = EuroDreamsCombination(numbers=[4, 8, 12, 16, 20, 24], dream=[3])

        combination2 = combination.get_combination([2, 3, 4, 5, 6, 7, 1])
        assert isinstance(combination2, EuroDreamsCombination)
        assert combination2.values == [2, 3, 4, 5, 6, 7, 1]
        assert combination2.get_component_values("numbers") == [2, 3, 4, 5, 6, 7]
        assert combination2.get_component_values("dream") == [1]

        new_combination = combination.get_combination([2, 3, 4, 5, 6, 7, 1], dream=[2])
        assert isinstance(new_combination, EuroDreamsCombination)
        assert new_combination.values == [2, 3, 4, 5, 6, 7, 2]
        assert new_combination.get_component_values("numbers") == [2, 3, 4, 5, 6, 7]
        assert new_combination.get_component_values("dream") == [2]

        new_combination = combination.get_combination(dream=[5])
        assert isinstance(new_combination, EuroDreamsCombination)
        assert new_combination.values == [5]
        assert new_combination.get_component_values("dream") == [5]

        new_combination = combination.get_combination(combination2)
        assert isinstance(new_combination, EuroDreamsCombination)
        assert new_combination.values == [2, 3, 4, 5, 6, 7, 1]

        new_combination = combination.get_combination(combination2, dream=[2])
        assert isinstance(new_combination, EuroDreamsCombination)
        assert new_combination.values == [2, 3, 4, 5, 6, 7, 2]

        new_combination = combination.get_combination(numbers=[6, 7, 8, 9, 10, 11])
        assert isinstance(new_combination, EuroDreamsCombination)
        assert new_combination.values == [6, 7, 8, 9, 10, 11]

        new_combination = combination.get_combination(numbers=[6, 7, 8, 9, 10, 15], dream=[4])
        assert isinstance(new_combination, EuroDreamsCombination)
        assert new_combination.values == [6, 7, 8, 9, 10, 15, 4]

        new_combination = new_combination.get_combination(combination.rank)
        assert isinstance(new_combination, EuroDreamsCombination)
        assert new_combination.values == [4, 8, 12, 16, 20, 24, 3]

        with pytest.raises(KeyError):
            _ = combination.get_combination(numbers=[6, 7, 8, 9, 10, 11], extra=[8])

    @pytest.mark.parametrize(
        ("numbers", "dream", "expected", "call_mode"),
        [
            (None, None, None, "none"),
            ([1, 2, 3, 4, 5, 6, 3], None, 1, "values"),
            ([1, 2, 3, 4, 5, 6], [3], 1, "keyword"),
            ([1, 2, 3, 4, 5, 6, 5], None, 2, "values"),
            ([1, 2, 3, 4, 5, 6], [5], 2, "keyword"),
            ([1, 2, 3, 4, 5, 6], None, 2, "numbers"),
            ([1, 2, 3, 4, 5, 7, 3], None, 3, "values"),
            ([1, 2, 3, 4, 5, 7], [3], 3, "keyword"),
            ([1, 2, 3, 4, 5, 7, 5], None, 3, "values"),
            ([1, 2, 3, 4, 5, 7], [5], 3, "keyword"),
            ([1, 2, 3, 4, 5, 7], None, 3, "numbers"),
            ([1, 2, 3, 4, 7, 8, 3], None, 4, "values"),
            ([1, 2, 3, 4, 7, 8], [3], 4, "keyword"),
            ([1, 2, 3, 4, 7, 8, 5], None, 4, "values"),
            ([1, 2, 3, 4, 7, 8], [5], 4, "keyword"),
            ([1, 2, 3, 4, 7, 8], None, 4, "numbers"),
            ([1, 2, 3, 7, 8, 9, 3], None, 5, "values"),
            ([1, 2, 3, 7, 8, 9], [3], 5, "keyword"),
            ([1, 2, 3, 7, 8, 9, 5], None, 5, "values"),
            ([1, 2, 3, 7, 8, 9], [5], 5, "keyword"),
            ([1, 2, 3, 7, 8, 9], None, 5, "numbers"),
            ([1, 2, 7, 8, 9, 10, 3], None, 6, "values"),
            ([1, 2, 7, 8, 9, 10], [3], 6, "keyword"),
            ([1, 2, 7, 8, 9, 10, 5], None, 6, "values"),
            ([1, 2, 7, 8, 9, 10], [5], 6, "keyword"),
            ([1, 2, 7, 8, 9, 10], None, 6, "numbers"),
            ([7, 8, 9, 10, 11, 12, 5], None, None, "values"),
            ([7, 8, 9, 10, 11, 12], [5], None, "keyword"),
        ],
    )
    def test_combination_get_winning_rank(self, numbers, dream, expected, call_mode):
        """Test EuroDreamsCombination winning rank calculation."""

        combination = EuroDreamsCombination([1, 2, 3, 4, 5, 6], [3])

        if call_mode == "none":
            assert combination.get_winning_rank() is None
            return

        if call_mode == "values":
            assert combination.get_winning_rank(numbers) == expected
            return

        if call_mode == "numbers":
            assert combination.get_winning_rank(numbers=numbers) == expected
            return

        assert combination.get_winning_rank(numbers=numbers, dream=dream) == expected

    def test_combination_equality(self):
        """Test EuroDreamsCombination equality comparisons."""

        number_rank = get_combination_rank([1, 2, 3, 4, 5, 6], offset=1)
        dream_rank = get_combination_rank([5], offset=1)

        combination1 = EuroDreamsCombination(numbers=[1, 2, 3, 4, 5, 6], dream=[5])
        combination2 = EuroDreamsCombination(numbers=[6, 5, 4, 3, 2, 1], dream=[5])
        combination3 = EuroDreamsCombination(numbers=[1, 2, 4, 5, 7, 8], dream=[4])

        assert EuroDreamsCombination() == EuroDreamsCombination()
        assert EuroDreamsCombination().equals()

        assert combination1 == combination2
        assert combination1 != combination3

        assert combination1.equals(combination1)
        assert combination1.equals(combination2)
        assert not combination1.equals(combination3)

        assert combination1.equals([1, 2, 3, 4, 5, 6, 5])
        assert combination1.equals(numbers=[1, 2, 3, 4, 5, 6], dream=[5])
        assert not combination1.equals([1, 2, 4, 5, 7, 8, 4])
        assert not combination1.equals(numbers=[1, 2, 4, 5, 7, 8], dream=[4])

        assert combination1.equals(numbers=number_rank, dream=dream_rank)
        assert not combination1.equals(numbers=number_rank + 1, dream=dream_rank)

        assert combination1.equals(number_rank * combination1.dream.combinations + dream_rank)

    def test_combination_includes(self):
        """Test EuroDreamsCombination includes method."""

        combination1 = EuroDreamsCombination(numbers=[1, 2, 3, 4, 5, 6], dream=[5])
        combination2 = EuroDreamsCombination(numbers=[1, 2], dream=[5])
        combination3 = EuroDreamsCombination(numbers=[2, 6], dream=[4])

        assert combination1.includes([])
        assert combination1.includes(dream=[7])
        assert combination1.includes(numbers=[2])
        assert combination1.includes([2, 4])
        assert combination1.includes(numbers=[2, 4], dream=[7])

        assert not combination1.includes(dream=[4])
        assert not combination1.includes(numbers=[2, 7], dream=[5])
        assert not combination1.includes(numbers=[7], dream=[5])
        assert not combination1.includes(numbers=[2, 4], dream=[4])

        assert not combination1.includes([2, 7])
        assert not combination1.includes([7])

        assert combination1.includes(combination2)
        assert not combination1.includes(combination3)

        assert 4 in combination1
        assert 8 not in combination1

        assert [2, 4] in combination1
        assert [2, 7] not in combination1

        assert combination2 in combination1
        assert combination3 not in combination1

    def test_combination_intersects(self):
        """Test EuroDreamsCombination intersects method."""

        combination1 = EuroDreamsCombination(numbers=[1, 2, 3, 4, 5, 6], dream=[5])
        combination2 = EuroDreamsCombination(numbers=[1, 3, 5, 7, 8, 9], dream=[5])
        combination3 = EuroDreamsCombination(numbers=[7, 8, 9, 10, 11, 12], dream=[4])

        assert combination1.intersects([3])
        assert combination1.intersects([3, 4])
        assert combination1.intersects([3, 4, 5])

        assert combination1.intersects(numbers=[3], dream=[5])
        assert combination1.intersects(numbers=[3, 4], dream=[5])
        assert combination1.intersects(numbers=[3, 4, 5], dream=[5])

        assert not combination1.intersects([7, 8, 9])
        assert not combination1.intersects([7, 8])
        assert not combination1.intersects([7])
        assert not combination1.intersects([])

        assert not combination1.intersects([7, 8, 9], dream=[4])
        assert not combination1.intersects([7, 8], dream=[4])
        assert not combination1.intersects([7], dream=[4])
        assert not combination1.intersects(dream=[4])

        assert combination1.intersects(combination2)
        assert not combination1.intersects(combination3)

    def test_combination_intersection(self):
        """Test EuroDreamsCombination intersection method."""

        combination1 = EuroDreamsCombination(numbers=[1, 2, 3, 4, 5, 6], dream=[5])
        combination2 = EuroDreamsCombination(numbers=[1, 3, 5, 7, 8, 9], dream=[5])
        combination3 = EuroDreamsCombination(numbers=[7, 8, 9, 10, 11, 12], dream=[4])

        intersection1 = combination1.intersection([1, 3, 5, 7, 8, 9, 5])
        intersection2 = combination1.intersection(numbers=[1, 3, 5, 7, 8, 9])
        intersection3 = combination1.intersection(numbers=[7, 8, 9, 10, 11, 12], dream=[4])
        intersection4 = combination1.intersection(numbers=[7, 8, 9, 10, 11, 12])

        assert isinstance(intersection1, EuroDreamsCombination)
        assert isinstance(intersection2, EuroDreamsCombination)
        assert isinstance(intersection3, EuroDreamsCombination)
        assert isinstance(intersection4, EuroDreamsCombination)

        assert intersection1.values == [1, 3, 5, 5]
        assert intersection2.values == [1, 3, 5]
        assert not intersection3.values
        assert not intersection4.values

        assert combination1.intersection(combination2).values == [1, 3, 5, 5]
        assert not combination1.intersection(combination3).values

    def test_combination_compares(self):
        """Test EuroDreamsCombination compares method."""

        combination1 = EuroDreamsCombination(numbers=[1, 2, 3, 4, 5, 6], dream=[5])
        combination2 = EuroDreamsCombination(numbers=[1, 3, 5, 7, 8, 9], dream=[5])
        combination3 = EuroDreamsCombination(numbers=[1, 2, 3, 4, 5, 6], dream=[5])

        assert combination1.compares(numbers=[1, 3, 5, 6, 7, 8, 9], dream=[4]) == -1
        assert combination2.compares(numbers=[1, 2, 3, 4, 5, 6], dream=[4]) == 1
        assert combination1.compares(numbers=[1, 2, 3, 4, 5, 6], dream=[5]) == 0

        assert combination1.compares([1, 3, 5, 6, 7, 8, 9]) == -1
        assert combination2.compares([1, 2, 3, 4, 5, 6]) == 1

        assert combination1.compares(combination2) == -1
        assert combination2.compares(combination1) == 1
        assert combination1.compares(combination1) == 0
        assert combination1.compares(combination3) == 0

        assert combination1 < combination2
        assert combination1 <= combination2
        assert combination1 == combination3
        assert combination2 > combination1
        assert combination2 >= combination1

    def test_combination_similarity(self):
        """Test EuroDreamsCombination similarity method."""

        combination1 = EuroDreamsCombination(numbers=[1, 2, 3, 4, 5, 6], dream=[5])
        combination2 = EuroDreamsCombination(numbers=[1, 3, 5, 7, 8, 9], dream=[5])
        combination3 = EuroDreamsCombination(numbers=[7, 8, 9, 10, 11, 12], dream=[4])

        assert EuroDreamsCombination([]).similarity([]) == 1
        assert EuroDreamsCombination([]).similarity(numbers=[1, 2, 3, 4, 5, 6], dream=[5]) == 0

        assert combination1.similarity(numbers=[1, 2, 3, 4, 5, 6], dream=[5]) == 1
        assert combination1.similarity(numbers=[1, 3, 5, 7, 8, 9], dream=[5]) == 4 / 7
        assert combination1.similarity(numbers=[7, 8, 9, 10, 11, 12], dream=[4]) == 0
        assert combination1.similarity(numbers=[1, 3, 5, 7, 8, 9]) == 3 / 7
        assert combination1.similarity(numbers=[7, 8, 9, 10, 11, 12]) == 0

        assert combination1.similarity(combination1) == 1
        assert combination1.similarity(combination2) == 4 / 7
        assert combination1.similarity(combination3) == 0

    def test_combination_iteration(self):
        """Test EuroDreamsCombination iteration."""

        combination = EuroDreamsCombination([5, 3, 1, 4, 6, 2], [3])
        assert list(combination) == [1, 2, 3, 4, 5, 6, 3]

    def test_combination_access(self):
        """Test EuroDreamsCombination item access."""

        combination = EuroDreamsCombination([5, 3, 1, 4, 6, 2], [3])

        assert combination[0] == 1
        assert combination[1] == 2
        assert combination[2] == 3
        assert combination[3] == 4
        assert combination[4] == 5
        assert combination[5] == 6
        assert combination[6] == 3

        with pytest.raises(IndexError):
            _ = combination[7]

    def test_combination_length(self):
        """Test EuroDreamsCombination length method."""

        combination = EuroDreamsCombination([5, 3, 1, 4, 6, 2], [3])
        assert len(combination) == 7
        assert combination.length == 7

    def test_combination_string(self):
        """Test EuroDreamsCombination string representation."""

        combination = EuroDreamsCombination([2, 6, 12, 25, 33, 40], [3])
        assert str(combination) == "numbers: [ 2,  6, 12, 25, 33, 40] dream: [3]"

    def test_combination_repr(self):
        """Test EuroDreamsCombination repr representation."""

        combination = EuroDreamsCombination([5, 3, 1, 4, 6, 2], [3])
        assert repr(combination) == "EuroDreamsCombination(numbers=[1, 2, 3, 4, 5, 6], dream=[3])"

    def test_combination_hash(self):
        """Test EuroDreamsCombination hash method."""

        combination1 = EuroDreamsCombination([1, 2, 3, 4, 5, 6], [1])
        combination2 = EuroDreamsCombination([6, 5, 4, 3, 2, 1], [1])
        combination3 = EuroDreamsCombination([1, 2, 4, 5, 7, 8], [3])

        assert hash(combination1) == hash(combination2)
        assert hash(combination1) != hash(combination3)
        assert hash(combination1) == combination1.rank
