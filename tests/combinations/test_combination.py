"""Unit tests for Combination class."""

import pytest

from pactole.combinations import (
    Combination,
    CombinationInputWithRank,
    get_combination_from_rank,
    get_combination_rank,
)


class TestGetCombinationRank:
    """Test suite for get_combination_rank function."""

    def test_get_combination_rank(self):
        """Test get_combination_rank function."""

        assert get_combination_rank([]) == 0
        assert get_combination_rank([0]) == 0
        assert get_combination_rank([1]) == 1
        assert get_combination_rank([0, 1, 2]) == 0
        assert get_combination_rank([0, 2, 3]) == 2
        assert get_combination_rank([23, 33, 45]) == 14741

    def test_get_combination_rank_with_offset(self):
        """Test get_combination_rank function with offset."""

        assert get_combination_rank([1], offset=1) == 0
        assert get_combination_rank([2], offset=1) == 1
        assert get_combination_rank([1, 2, 3], offset=1) == 0
        assert get_combination_rank([11, 12], offset=1) == 65
        assert get_combination_rank([24, 34, 46], offset=1) == 14741


class TestGetCombinationFromRank:
    """Test suite for get_combination_from_rank function."""

    def test_get_combination_from_rank(self):
        """Test get_combination_from_rank function."""

        assert not get_combination_from_rank(0, 0)
        assert get_combination_from_rank(0, 1) == [0]
        assert get_combination_from_rank(1, 1) == [1]
        assert get_combination_from_rank(65, 2) == [10, 11]
        assert get_combination_from_rank(0, 3) == [0, 1, 2]
        assert get_combination_from_rank(2, 3) == [0, 2, 3]
        assert get_combination_from_rank(14741, 3) == [23, 33, 45]

    def test_get_combination_from_rank_with_offset(self):
        """Test get_combination_from_rank function with offset."""

        assert get_combination_from_rank(0, 1, offset=1) == [1]
        assert get_combination_from_rank(1, 1, offset=1) == [2]
        assert get_combination_from_rank(65, 2, offset=1) == [11, 12]
        assert get_combination_from_rank(0, 3, offset=1) == [1, 2, 3]
        assert get_combination_from_rank(2, 3, offset=1) == [1, 3, 4]
        assert get_combination_from_rank(14741, 3, offset=1) == [24, 34, 46]

    def test_get_combination_from_rank_errors(self):
        """Test get_combination_from_rank function errors."""

        with pytest.raises(ValueError):
            get_combination_from_rank(-1, 3)

        with pytest.raises(ValueError):
            get_combination_from_rank(2, -3)


class TestCombination:
    """Test suite for Combination class."""

    def test_combination_empty(self):
        """Test empty Combination."""

        combination = Combination()
        assert not combination
        assert combination.values == []
        assert combination.rank == 0
        assert combination.length == 0
        assert combination.start == 1

    def test_combination_from_values_default_start(self):
        """Test Combination construction with number inputs and default start."""

        combination = Combination([3, 2, 1])
        assert combination == [1, 2, 3]
        assert combination.values == [1, 2, 3]
        assert combination.rank == get_combination_rank([1, 2, 3], offset=1)
        assert combination.length == 3
        assert combination.start == 1

    def test_combination_from_values_specified_start(self):
        """Test Combination construction with number inputs and specified start."""

        combination = Combination([3, 2, 1], start=0)
        assert combination == [1, 2, 3]
        assert combination.values == [1, 2, 3]
        assert combination.rank == get_combination_rank([1, 2, 3], offset=0)
        assert combination.length == 3
        assert combination.start == 0

    def test_combination_from_combination_default_start(self):
        """Test Combination construction with Combination input and default start."""

        original = Combination([4, 5, 6])
        combination = Combination(original)
        assert combination.values == original.values
        assert combination.rank == original.rank
        assert combination.length == original.length
        assert combination.start == original.start

        combination = Combination(original, start=1)
        assert combination.values == original.values
        assert combination.rank == original.rank
        assert combination.length == original.length
        assert combination.start == original.start

    def test_combination_from_combination_specified_start(self):
        """Test Combination construction with Combination input and specified start."""

        original = Combination([4, 5, 6], start=0)
        combination = Combination(original)
        assert combination.values == original.values
        assert combination.rank == original.rank
        assert combination.length == original.length
        assert combination.start == original.start

    def test_combination_from_combination_different_start(self):
        """Test Combination construction with Combination input and different start."""

        original = Combination([4, 5, 6], start=1)
        combination = Combination(original, start=2)
        assert combination.values == [5, 6, 7]
        assert combination.rank == get_combination_rank([5, 6, 7], offset=2)
        assert combination.length == original.length
        assert combination.start == 2

    def test_combination_from_values_and_specified_rank(self):
        """Test Combination construction with number input and specified rank."""

        combination = Combination([4, 5, 6], rank=123)
        assert combination.values == [4, 5, 6]
        assert combination.rank == 123
        assert combination.rank != get_combination_rank([4, 5, 6], offset=1)
        assert combination.length == combination.length
        assert combination.start == 1

    def test_combination_from_input_with_rank(self):
        """Test Combination construction with CombinationInputWithRank."""

        combination = Combination(CombinationInputWithRank(values=[4, 5, 6], rank=123))
        assert combination.values == [4, 5, 6]
        assert combination.rank == 123
        assert combination.rank != get_combination_rank([4, 5, 6], offset=1)
        assert combination.length == 3
        assert combination.start == 1

    def test_combination_copy(self):
        """Test Combination copy method."""

        combination = Combination([3, 5, 7], start=1)

        new_comb = combination.copy()
        assert isinstance(new_comb, Combination)
        assert new_comb is not combination
        assert new_comb.values == [3, 5, 7]
        assert new_comb.start == 1
        assert new_comb.length == 3
        assert new_comb.rank == get_combination_rank([3, 5, 7], offset=1)

        new_comb = combination.copy(start=0)
        assert isinstance(new_comb, Combination)
        assert new_comb is not combination
        assert new_comb.values == [2, 4, 6]
        assert new_comb.start == 0
        assert new_comb.length == 3
        assert new_comb.rank == get_combination_rank([2, 4, 6], offset=0)

        new_comb = combination.copy(values=[8, 10, 12])

        assert isinstance(new_comb, Combination)
        assert new_comb is not combination
        assert new_comb.values == [8, 10, 12]
        assert new_comb.start == 1
        assert new_comb.length == 3
        assert new_comb.rank == get_combination_rank([8, 10, 12], offset=1)

        combination = Combination([2, 4, 6], rank=123, start=1)

        new_comb = combination.copy()

        assert new_comb.values == [2, 4, 6]
        assert new_comb.start == 1
        assert new_comb.rank == 123

    def test_combination_get_values(self):
        """Test Combination get_values method."""

        combination = Combination([3, 1, 2])
        assert combination.get_values() == [1, 2, 3]
        assert combination.get_values(start=0) == [0, 1, 2]
        assert combination.get_values(start=1) == [1, 2, 3]
        assert combination.get_values(start=2) == [2, 3, 4]

    def test_combination_equality(self):
        """Test Combination equality comparisons."""

        combination1 = Combination([1, 2, 3])
        combination2 = Combination([3, 2, 1])
        combination3 = Combination([1, 2, 4])
        combination4 = Combination([1, 2, 3], start=0)
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

        combination1 = Combination([2, 4, 6])
        combination2 = Combination([2, 4])
        combination3 = Combination([2, 5])
        combination4 = Combination([2, 4], start=0)
        combination5 = Combination([1, 3], start=0)
        combination6 = Combination([1, 3])

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

        combination1 = Combination([1, 2, 3])
        combination2 = Combination([3, 4, 5])
        combination3 = Combination([4, 5, 6])
        combination4 = Combination([0, 1, 2], start=0)

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

        combination1 = Combination([1, 2, 3])
        combination2 = Combination([3, 4, 5])
        combination3 = Combination([4, 5, 6])
        combination4 = Combination([0, 1, 2], start=0)

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

        combination1 = Combination([1, 2, 3])
        combination2 = Combination([1, 2, 4])
        combination3 = Combination([0, 1, 2], start=0)
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

        combination1 = Combination([1, 2, 3])
        combination2 = Combination([2, 3, 4])
        combination3 = Combination([4, 5, 6])
        combination4 = Combination([0, 1, 2], start=0)

        assert Combination(None).similarity(None) == 1
        assert Combination([]).similarity([]) == 1
        assert Combination([]).similarity([1, 2, 3]) == 0
        assert Combination(None).similarity([1, 2, 3]) == 0

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

        combination = Combination([3, 1, 2])
        assert list(combination) == [1, 2, 3]

    def test_combination_access(self):
        """Test Combination item access."""

        combination = Combination([3, 1, 2])

        assert combination[0] == 1
        assert combination[1] == 2
        assert combination[2] == 3

        with pytest.raises(IndexError):
            _ = combination[3]

    def test_combination_length(self):
        """Test Combination length method."""

        combination = Combination([1, 2, 3, 4, 5])
        assert len(combination) == 5
        assert combination.length == 5

    def test_combination_string(self):
        """Test Combination string representation."""

        combination = Combination([3, 1, 2])
        assert str(combination) == "[1, 2, 3]"

    def test_combination_repr(self):
        """Test Combination repr representation."""

        combination = Combination([3, 1, 2], start=0)
        assert repr(combination) == "Combination(values=[1, 2, 3], rank=None, start=0)"

        combination = Combination([3, 1, 2], rank=123, start=0)
        assert repr(combination) == "Combination(values=[1, 2, 3], rank=123, start=0)"

    def test_combination_hash(self):
        """Test Combination hash method."""

        combination1 = Combination([1, 2, 3])
        combination2 = Combination([3, 2, 1])
        combination3 = Combination([1, 2, 4])

        assert hash(combination1) == hash(combination2)
        assert hash(combination1) != hash(combination3)
        assert hash(combination1) == combination1.rank
