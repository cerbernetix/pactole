"""Unit tests for BoundCombination class."""

import random
from math import ceil

import pytest

from pactole.combinations import (
    BoundCombination,
    Combination,
    CombinationInputWithRank,
    get_combination_from_rank,
    get_combination_rank,
)


class TestBoundCombination:
    """Tests for the BoundCombination class."""

    def test_combination_empty(self) -> None:
        """Test creating an empty BoundCombination."""

        combination = BoundCombination()
        assert not combination
        assert combination.values == []
        assert combination.rank == 0
        assert combination.length == 0
        assert combination.start == 1
        assert combination.end == 50
        assert combination.count == 5
        assert combination.combinations == 2118760

    def test_combination_from_values(self):
        """Test Combination construction with number inputs."""

        combination = BoundCombination([3, 2, 1], start=1, end=50, count=5, combinations=2118760)
        assert combination == [1, 2, 3]
        assert combination.values == [1, 2, 3]
        assert combination.rank == get_combination_rank([1, 2, 3], offset=1)
        assert combination.length == 3
        assert combination.start == 1
        assert combination.end == 50
        assert combination.count == 5
        assert combination.combinations == 2118760

    def test_combination_from_values_computing_combinations(self):
        """Test Combination construction with number inputs and computing combinations."""

        combination = BoundCombination([1, 2, 3, 4, 5, 6, 7], start=1, end=50, count=5)
        assert combination == [1, 2, 3, 4, 5]
        assert combination.values == [1, 2, 3, 4, 5]
        assert combination.rank == get_combination_rank([1, 2, 3, 4, 5], offset=1)
        assert combination.length == 5
        assert combination.start == 1
        assert combination.end == 50
        assert combination.count == 5
        assert combination.combinations == 2118760

    def test_combination_from_rank(self):
        """Test Combination construction with rank input."""

        rank = 1000
        combination = BoundCombination(rank, start=1, end=50, count=5)
        expected_values = get_combination_from_rank(rank, length=5, offset=1)
        assert combination.values == expected_values
        assert combination.rank == rank
        assert combination.length == 5
        assert combination.start == 1
        assert combination.end == 50
        assert combination.count == 5
        assert combination.combinations == 2118760

    def test_combination_from_rank_without_values(self) -> None:
        """Test Combination construction with rank and empty values."""

        rank = 42
        combination = BoundCombination(values=None, rank=rank, start=1, end=10, count=3)

        expected_values = get_combination_from_rank(rank, length=3, offset=1)

        assert combination.values == expected_values
        assert combination.rank == rank
        assert combination.length == 3
        assert combination.start == 1
        assert combination.end == 10
        assert combination.count == 3
        assert combination.combinations == 120

    def test_combination_from_combination(self):
        """Test Combination construction with another Combination input."""

        original_combination = BoundCombination([10, 20, 30], start=1, end=50, count=5)
        combination = BoundCombination(original_combination, start=1, end=50, count=5)
        assert combination.values == original_combination.values
        assert combination.rank == original_combination.rank
        assert combination.length == original_combination.length
        assert combination.start == 1
        assert combination.end == 50
        assert combination.count == 5
        assert combination.combinations == 2118760

        combination = BoundCombination(original_combination, start=0, end=49)
        assert combination.values == [9, 19, 29]
        assert combination.rank == get_combination_rank([9, 19, 29], offset=0)
        assert combination.length == original_combination.length
        assert combination.start == 0
        assert combination.end == 49
        assert combination.count == 5
        assert combination.combinations == 2118760

        ranked_combination = Combination([1, 2, 3], rank=321, start=1)
        combination = BoundCombination(ranked_combination, start=1, end=10, count=3)

        assert combination.values == [1, 2, 3]
        assert combination.rank == 321
        assert combination.start == 1
        assert combination.end == 10
        assert combination.count == 3

    def test_combination_from_input_with_rank(self):
        """Test Combination construction with a CombinationInputWithRank input."""

        combination = BoundCombination(
            CombinationInputWithRank(values=[4, 5, 6], rank=123), start=1, end=50, count=5
        )
        assert combination.values == [4, 5, 6]
        assert combination.rank == 123
        assert combination.rank != get_combination_rank([4, 5, 6], offset=1)
        assert combination.length == 3
        assert combination.start == 1
        assert combination.end == 50
        assert combination.count == 5

    def test_combination_generate(self):
        """Test the generate method of BoundCombination."""

        combination = BoundCombination(start=1, end=10, count=5)
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
        assert generated1[0].values == get_combination_from_rank(ranks[0], length=5, offset=1)

        generated2 = combination.generate(2)
        for c in generated2:
            combinations.add(c.rank)

        assert len(generated2) == 2
        assert generated2[0].values == get_combination_from_rank(ranks[1], length=5, offset=1)
        assert generated2[1].values == get_combination_from_rank(ranks[2], length=5, offset=1)

        generated3 = combination.generate(3, partitions=3)
        for c in generated3:
            combinations.add(c.rank)

        assert len(generated3) == 3
        assert generated3[0].values == get_combination_from_rank(ranks[3], length=5, offset=1)
        assert generated3[1].values == get_combination_from_rank(ranks[4], length=5, offset=1)
        assert generated3[2].values == get_combination_from_rank(ranks[5], length=5, offset=1)

        generated4 = combination.generate(4, partitions=2)
        for c in generated4:
            combinations.add(c.rank)

        assert len(generated4) == 4
        assert generated4[0].values == get_combination_from_rank(ranks[6], length=5, offset=1)
        assert generated4[1].values == get_combination_from_rank(ranks[7], length=5, offset=1)
        assert generated4[2].values == get_combination_from_rank(ranks[8], length=5, offset=1)
        assert generated4[3].values == get_combination_from_rank(ranks[9], length=5, offset=1)

        for c in combination.generate(5):
            combinations.add(c.rank)

        assert len(combinations) == 15

    def test_combination_copy(self):
        """Test the copy method of BoundCombination."""

        combination = BoundCombination(values=[2, 3, 4, 5, 7], start=1, end=50, count=5)

        new_comb = combination.copy(values=15)
        assert isinstance(new_comb, BoundCombination)
        assert new_comb is not combination
        assert new_comb.values == [1, 2, 5, 6, 7]
        assert new_comb.start == 1
        assert new_comb.end == 50
        assert new_comb.count == 5
        assert new_comb.combinations == 2118760

        new_comb = combination.copy(start=0, end=49)
        assert isinstance(new_comb, BoundCombination)
        assert new_comb is not combination
        assert new_comb.values == [1, 2, 3, 4, 6]
        assert new_comb.start == 0
        assert new_comb.end == 49
        assert new_comb.count == 5
        assert new_comb.combinations == 2118760

        new_comb = combination.copy(count=3)
        assert isinstance(new_comb, BoundCombination)
        assert new_comb is not combination
        assert new_comb.values == [2, 3, 4]
        assert new_comb.start == 1
        assert new_comb.end == 50
        assert new_comb.count == 3
        assert new_comb.combinations == 19600

    def test_combination_get_values(self):
        """Test Combination get_values method."""

        combination = BoundCombination([3, 1, 2], start=1, end=10, count=3)
        assert combination.get_values() == [1, 2, 3]
        assert combination.get_values(start=0) == [0, 1, 2]
        assert combination.get_values(start=1) == [1, 2, 3]
        assert combination.get_values(start=2) == [2, 3, 4]

    def test_combination_equality(self):
        """Test Combination equality comparisons."""

        combination1 = BoundCombination([1, 2, 3], start=1, end=10, count=3)
        combination2 = BoundCombination([3, 2, 1], start=1, end=10, count=3)
        combination3 = BoundCombination([1, 2, 4], start=1, end=10, count=3)
        combination4 = BoundCombination([1, 2, 3], start=0, end=9, count=3)
        rank = get_combination_rank([1, 2, 3], offset=1)

        assert combination1 == [1, 2, 3]
        assert combination2 == [1, 2, 3]
        assert combination3 == [1, 2, 4]
        assert combination4 == [1, 2, 3]
        assert combination1 != [1, 2, 4]

        assert combination1 == combination2
        assert combination1 != combination3
        assert combination1 != combination4

        assert combination1.equals(combination1)
        assert combination1.equals(combination2)
        assert not combination1.equals(combination3)
        assert not combination1.equals(combination4)

        assert combination1.equals([1, 2, 3])
        assert combination2.equals([1, 2, 3])
        assert combination3.equals([1, 2, 4])
        assert combination4.equals([1, 2, 3])
        assert not combination1.equals([1, 2, 4])

        assert combination1.equals(rank)
        assert not combination1.equals(rank + 1)

        assert not combination1.equals([])
        assert not combination1.equals(None)

    def test_combination_includes(self):
        """Test Combination includes method."""

        combination1 = BoundCombination([2, 4, 6], start=1, end=10, count=3)
        combination2 = BoundCombination([2, 4], start=1, end=10, count=3)
        combination3 = BoundCombination([2, 5], start=1, end=10, count=3)
        combination4 = BoundCombination([2, 4], start=0, end=9, count=2)
        combination5 = BoundCombination([1, 3], start=0, end=9, count=2)
        combination6 = BoundCombination([1, 3])

        assert combination1.includes([])
        assert combination1.includes([2])
        assert combination1.includes([2, 4])
        assert combination1.includes(4)
        assert not combination1.includes([2, 5])
        assert not combination1.includes([5])
        assert not combination1.includes(5)

        assert combination1.includes(combination2)
        assert not combination1.includes(combination3)
        assert not combination1.includes(combination4)
        assert combination1.includes(combination5)
        assert not combination1.includes(combination6)

        assert combination1.includes(None)
        assert combination1.includes([])

        assert 4 in combination1
        assert 5 not in combination1

        assert [2, 4] in combination1
        assert [2, 5] not in combination1

        assert combination2 in combination1
        assert combination3 not in combination1
        assert combination4 not in combination1
        assert combination5 in combination1
        assert combination6 not in combination1

    def test_combination_intersects(self):
        """Test Combination intersects method."""

        combination1 = BoundCombination([1, 2, 3], start=1, end=10, count=3)
        combination2 = BoundCombination([3, 4, 5], start=1, end=10, count=3)
        combination3 = BoundCombination([4, 5, 6], start=1, end=10, count=3)
        combination4 = BoundCombination([0, 1, 2], start=0, end=9, count=3)

        assert combination1.intersects([3])
        assert combination1.intersects([3, 4])
        assert combination1.intersects([3, 4, 5])
        assert not combination1.intersects([4, 5, 6])
        assert not combination1.intersects([4, 5])
        assert not combination1.intersects([4])
        assert not combination1.intersects([])
        assert not combination1.intersects(None)

        assert combination1.intersects(combination2)
        assert not combination1.intersects(combination3)
        assert combination1.intersects(combination4)

    def test_combination_intersection(self):
        """Test Combination intersection method."""

        combination1 = BoundCombination([1, 2, 3], start=1, end=10, count=3)
        combination2 = BoundCombination([3, 4, 5], start=1, end=10, count=3)
        combination3 = BoundCombination([4, 5, 6], start=1, end=10, count=3)
        combination4 = BoundCombination([0, 1, 2], start=0, end=9, count=3)

        intersection1 = combination1.intersection([3, 4, 5])
        intersection2 = combination1.intersection([4, 5, 6])
        intersection3 = combination1.intersection([])
        intersection4 = combination1.intersection(None)

        assert isinstance(intersection1, Combination)
        assert isinstance(intersection2, Combination)
        assert isinstance(intersection3, Combination)
        assert isinstance(intersection4, Combination)

        assert intersection1.values == [3]
        assert not intersection2.values
        assert not intersection3.values
        assert not intersection4.values

        intersection1 = combination1.intersection(combination2)
        intersection2 = combination1.intersection(combination3)
        intersection3 = combination1.intersection(combination4)

        assert isinstance(intersection1, Combination)
        assert isinstance(intersection2, Combination)
        assert isinstance(intersection3, Combination)

        assert intersection1.values == [3]
        assert not intersection2.values
        assert intersection3.values == [1, 2, 3]

    def test_combination_compares(self):
        """Test Combination compares method."""

        combination1 = BoundCombination([1, 2, 3], start=1, end=10, count=3)
        combination2 = BoundCombination([1, 2, 4], start=1, end=10, count=3)
        combination3 = BoundCombination([0, 1, 2], start=0, end=9, count=3)
        rank1 = get_combination_rank([1, 2, 3], offset=1)
        rank2 = get_combination_rank([1, 2, 4], offset=1)

        assert combination1.compares(None) == -1
        assert combination1.compares([]) == -1
        assert combination1.compares([1, 2, 4]) == -1
        assert combination2.compares([1, 2, 3]) == 1
        assert combination1.compares([1, 2, 3]) == 0

        assert combination1.compares(combination2) == -1
        assert combination2.compares(combination1) == 1
        assert combination1.compares(combination1) == 0
        assert combination1.compares(combination3) == 0

        assert combination1.compares(rank2) == -1
        assert combination2.compares(rank1) == 1
        assert combination1.compares(rank1) == 0

        assert combination1 < combination2
        assert combination1 <= combination2
        assert combination1 == combination3
        assert combination2 > combination1
        assert combination2 >= combination1

        assert combination1 < rank2
        assert combination1 <= rank2
        assert combination1 == rank1
        assert combination2 > rank1
        assert combination2 >= rank1

    def test_combination_similarity(self):
        """Test Combination similarity method."""

        combination1 = BoundCombination([1, 2, 3], start=1, end=10, count=3)
        combination2 = BoundCombination([2, 3, 4], start=1, end=10, count=3)
        combination3 = BoundCombination([4, 5, 6], start=1, end=10, count=3)
        combination4 = BoundCombination([0, 1, 2], start=0, end=9, count=3)

        assert BoundCombination(None, start=1, end=10, count=3).similarity(None) == 1
        assert BoundCombination([], start=1, end=10, count=3).similarity([]) == 1
        assert BoundCombination([], start=1, end=10, count=3).similarity([1, 2, 3]) == 0
        assert BoundCombination(None, start=1, end=10, count=3).similarity([1, 2, 3]) == 0

        assert combination1.similarity([1, 2, 3]) == 1
        assert combination1.similarity([2, 3, 4]) == 2 / 3
        assert combination1.similarity([4, 5, 6]) == 0
        assert combination1.similarity([]) == 0
        assert combination1.similarity(None) == 0

        assert combination1.similarity(combination1) == 1
        assert combination1.similarity(combination2) == 2 / 3
        assert combination1.similarity(combination3) == 0
        assert combination1.similarity(combination4) == 1

    def test_combination_iteration(self):
        """Test Combination iteration."""

        combination = BoundCombination([3, 1, 2], start=1, end=10, count=3)
        assert list(combination) == [1, 2, 3]

    def test_combination_access(self):
        """Test Combination item access."""

        combination = BoundCombination([3, 1, 2], start=1, end=10, count=3)

        assert combination[0] == 1
        assert combination[1] == 2
        assert combination[2] == 3

        with pytest.raises(IndexError):
            _ = combination[3]

    def test_combination_length(self):
        """Test Combination length method."""

        combination = BoundCombination([1, 2, 3, 4, 5], start=1, end=10, count=5)
        assert len(combination) == 5
        assert combination.length == 5

    def test_combination_string(self):
        """Test Combination string representation."""

        combination = BoundCombination([3, 1, 2], start=1, end=9, count=3)
        assert str(combination) == "[1, 2, 3]"

        combination = BoundCombination([3, 6, 12, 33, 42], start=1, end=50, count=5)
        assert str(combination) == "[ 3,  6, 12, 33, 42]"

        combination = BoundCombination([3, 6, 12], start=1, end=50, count=5)
        assert str(combination) == "[         3,  6, 12]"

    def test_combination_repr(self):
        """Test Combination repr representation."""

        combination = BoundCombination([3, 1, 2], start=1, end=10, count=3)
        assert repr(combination) == (
            "BoundCombination(values=[1, 2, 3], rank=None, "
            "start=1, end=10, count=3, combinations=120)"
        )

        combination = BoundCombination([3, 1, 2], rank=123, start=1, end=10, count=3)
        assert repr(combination) == (
            "BoundCombination(values=[1, 2, 3], rank=123, "
            "start=1, end=10, count=3, combinations=120)"
        )

    def test_combination_hash(self):
        """Test Combination hash method."""

        combination1 = BoundCombination([1, 2, 3], start=1, end=10, count=3)
        combination2 = Combination([3, 2, 1], start=1)
        combination3 = BoundCombination([1, 2, 4], start=1, end=10, count=3)

        assert hash(combination1) == hash(combination2)
        assert hash(combination1) != hash(combination3)
        assert hash(combination1) == combination1.rank
