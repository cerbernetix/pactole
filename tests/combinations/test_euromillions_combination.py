"""Unit tests for EuroMillionsCombination class."""

import random
from math import ceil

import pytest

from pactole.combinations import (
    CombinationInputWithRank,
    EuroMillionsCombination,
    get_combination_from_rank,
    get_combination_rank,
)


class TestEuroMillionsCombination:
    """Test suite for EuroMillionsCombination class."""

    def test_combination_empty(self):
        """Test empty EuroMillionsCombination."""

        combination = EuroMillionsCombination()
        assert combination.numbers == []
        assert combination.stars == []
        assert combination.nb_winning_ranks == 13
        assert combination.min_winning_rank == 1
        assert combination.max_winning_rank == 13
        assert combination.values == []
        assert combination.rank == 0
        assert combination.length == 0

    def test_combination_from_values(self):
        """Test EuroMillionsCombination construction with number inputs."""

        combination = EuroMillionsCombination(numbers=[3, 2, 1])
        assert combination.numbers == [1, 2, 3]
        assert combination.stars == []
        assert combination.values == [1, 2, 3]
        assert combination.rank == get_combination_rank([1, 2, 3], offset=1)
        assert combination.length == 3

        combination = EuroMillionsCombination(numbers=[3, 2, 1], stars=[3])
        assert combination.numbers == [1, 2, 3]
        assert combination.stars == [3]
        assert combination.values == [1, 2, 3, 3]
        assert combination.rank == get_combination_rank(
            [1, 2, 3], offset=1
        ) * 66 + get_combination_rank([3], offset=1)
        assert combination.length == 4

        combination = EuroMillionsCombination(stars=[3])
        assert combination.numbers == []
        assert combination.stars == [3]
        assert combination.values == [3]
        assert combination.rank == get_combination_rank([3], offset=1)
        assert combination.length == 1

        combination = EuroMillionsCombination([3, 5, 2, 4, 1, 6, 7, 8])
        assert combination.numbers == [1, 2, 3, 4, 5]
        assert combination.stars == [6, 7]
        assert combination.values == [1, 2, 3, 4, 5, 6, 7]
        assert combination.rank == get_combination_rank(
            [1, 2, 3, 4, 5], offset=1
        ) * 66 + get_combination_rank([6, 7], offset=1)
        assert combination.length == 7

    def test_combination_from_combination(self):
        """Test EuroMillionsCombination construction with EuroMillionsCombination input."""

        original = EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[6, 7])
        combination = EuroMillionsCombination(original)
        assert combination.numbers == original.numbers
        assert combination.stars == original.stars
        assert combination.values == original.values
        assert combination.rank == original.rank
        assert combination.length == original.length

        combination = EuroMillionsCombination(original, stars=[8, 9])
        assert combination.numbers == original.numbers
        assert combination.stars == [8, 9]
        assert combination.values == original.numbers.values + [8, 9]
        assert combination.rank == original.numbers.rank * 66 + get_combination_rank(
            [8, 9], offset=1
        )
        assert combination.length == original.length

    def test_combination_from_ranks(self):
        """Test EuroMillionsCombination construction with rank inputs."""

        number_rank = get_combination_rank([1, 2, 3, 4, 5], offset=1)
        star_rank = get_combination_rank([6, 7], offset=1)
        total_rank = number_rank * 66 + star_rank

        combination = EuroMillionsCombination(numbers=number_rank, stars=star_rank)
        assert combination.numbers == [1, 2, 3, 4, 5]
        assert combination.stars == [6, 7]
        assert combination.values == [1, 2, 3, 4, 5, 6, 7]
        assert combination.rank == total_rank
        assert combination.length == 7

    def test_combination_from_component_ranks(self):
        """Test EuroMillionsCombination construction with component rank dictionaries."""

        numbers_rank = get_combination_rank([1, 2, 3, 4, 5], offset=1)
        stars_rank = get_combination_rank([2, 9], offset=1)

        combination = EuroMillionsCombination(
            numbers=CombinationInputWithRank(values=[5, 1, 4, 2, 3], rank=numbers_rank),
            stars=CombinationInputWithRank(values=[9, 2], rank=stars_rank),
        )

        assert combination.numbers == [1, 2, 3, 4, 5]
        assert combination.stars == [2, 9]
        assert combination.values == [1, 2, 3, 4, 5, 2, 9]
        assert combination.numbers.rank == numbers_rank
        assert combination.stars.rank == stars_rank
        assert combination.rank == numbers_rank * 66 + stars_rank
        assert combination.length == 7

    def test_combination_generate(self):
        """Test the generate method of EuroMillionsCombination."""

        combination = EuroMillionsCombination()

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
            ranks[0] // 66, length=5, offset=1
        ) + get_combination_from_rank(ranks[0] % 66, length=2, offset=1)

        generated2 = combination.generate(2)
        for c in generated2:
            combinations.add(c.rank)

        assert len(generated2) == 2
        assert generated2[0].values == get_combination_from_rank(
            ranks[1] // 66, length=5, offset=1
        ) + get_combination_from_rank(ranks[1] % 66, length=2, offset=1)
        assert generated2[1].values == get_combination_from_rank(
            ranks[2] // 66, length=5, offset=1
        ) + get_combination_from_rank(ranks[2] % 66, length=2, offset=1)

        generated3 = combination.generate(3, partitions=3)
        for c in generated3:
            combinations.add(c.rank)

        assert len(generated3) == 3
        assert generated3[0].values == get_combination_from_rank(
            ranks[3] // 66, length=5, offset=1
        ) + get_combination_from_rank(ranks[3] % 66, length=2, offset=1)
        assert generated3[1].values == get_combination_from_rank(
            ranks[4] // 66, length=5, offset=1
        ) + get_combination_from_rank(ranks[4] % 66, length=2, offset=1)
        assert generated3[2].values == get_combination_from_rank(
            ranks[5] // 66, length=5, offset=1
        ) + get_combination_from_rank(ranks[5] % 66, length=2, offset=1)

        generated4 = combination.generate(4, partitions=2)
        for c in generated4:
            combinations.add(c.rank)

        assert len(generated4) == 4
        assert generated4[0].values == get_combination_from_rank(
            ranks[6] // 66, length=5, offset=1
        ) + get_combination_from_rank(ranks[6] % 66, length=2, offset=1)
        assert generated4[1].values == get_combination_from_rank(
            ranks[7] // 66, length=5, offset=1
        ) + get_combination_from_rank(ranks[7] % 66, length=2, offset=1)
        assert generated4[2].values == get_combination_from_rank(
            ranks[8] // 66, length=5, offset=1
        ) + get_combination_from_rank(ranks[8] % 66, length=2, offset=1)
        assert generated4[3].values == get_combination_from_rank(
            ranks[9] // 66, length=5, offset=1
        ) + get_combination_from_rank(ranks[9] % 66, length=2, offset=1)

        for c in combination.generate(5):
            combinations.add(c.rank)

        assert len(combinations) == 15

    def test_combination_copy(self):
        """Test EuroMillionsCombination copy method."""

        combination = EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[6, 7])

        combination_copy = combination.copy()
        assert isinstance(combination_copy, EuroMillionsCombination)
        assert combination_copy is not combination
        assert combination_copy.numbers == combination.numbers
        assert combination_copy.stars == combination.stars
        assert combination_copy.winning_ranks == combination.winning_ranks
        assert combination_copy.values == combination.values
        assert combination_copy.rank == combination.rank
        assert combination_copy.length == combination.length
        assert combination_copy.count == combination.count
        assert combination_copy.combinations == combination.combinations

        combination_copy = combination.copy(numbers=[4, 8, 15, 16, 23])
        assert isinstance(combination_copy, EuroMillionsCombination)
        assert combination_copy is not combination
        assert combination_copy.numbers == [4, 8, 15, 16, 23]
        assert combination_copy.stars == combination.stars
        assert combination_copy.winning_ranks == combination.winning_ranks
        assert combination_copy.values == [4, 8, 15, 16, 23, 6, 7]
        assert (
            combination_copy.rank
            == get_combination_rank([4, 8, 15, 16, 23], offset=1) * combination.stars.combinations
            + combination.stars.rank
        )
        assert combination_copy.length == combination.length
        assert combination_copy.count == combination.count
        assert combination_copy.combinations == combination.combinations

        combination_copy = combination.copy(stars=[5, 8])
        assert isinstance(combination_copy, EuroMillionsCombination)
        assert combination_copy is not combination
        assert combination_copy.numbers == combination.numbers
        assert combination_copy.stars == [5, 8]
        assert combination_copy.winning_ranks == combination.winning_ranks
        assert combination_copy.values == combination.numbers.values + [5, 8]
        assert (
            combination_copy.rank
            == combination.numbers.rank * combination.stars.combinations
            + get_combination_rank([5, 8], offset=1)
        )
        assert combination_copy.length == combination.length
        assert combination_copy.count == combination.count
        assert combination_copy.combinations == combination.combinations

    def test_combination_get_combination(self):
        """Test EuroMillionsCombination get_combination method."""

        combination = EuroMillionsCombination(numbers=[4, 8, 12, 16, 20], stars=[3, 8])

        combination2 = combination.get_combination([2, 3, 4, 5, 6, 7, 8])
        assert isinstance(combination2, EuroMillionsCombination)
        assert combination2.values == [2, 3, 4, 5, 6, 7, 8]
        assert combination2.get_component_values("numbers") == [2, 3, 4, 5, 6]
        assert combination2.get_component_values("stars") == [7, 8]

        new_combination = combination.get_combination([2, 3, 4, 5, 6, 7, 8], stars=[2, 3])
        assert isinstance(new_combination, EuroMillionsCombination)
        assert new_combination.values == [2, 3, 4, 5, 6, 2, 3]
        assert new_combination.get_component_values("numbers") == [2, 3, 4, 5, 6]
        assert new_combination.get_component_values("stars") == [2, 3]

        new_combination = combination.get_combination(stars=[5, 9])
        assert isinstance(new_combination, EuroMillionsCombination)
        assert new_combination.values == [5, 9]
        assert new_combination.get_component_values("stars") == [5, 9]

        new_combination = combination.get_combination(combination2)
        assert isinstance(new_combination, EuroMillionsCombination)
        assert new_combination.values == [2, 3, 4, 5, 6, 7, 8]

        new_combination = combination.get_combination(combination2, stars=[2, 4])
        assert isinstance(new_combination, EuroMillionsCombination)
        assert new_combination.values == [2, 3, 4, 5, 6, 2, 4]

        new_combination = combination.get_combination(numbers=[6, 7, 8, 9, 10, 11])
        assert isinstance(new_combination, EuroMillionsCombination)
        assert new_combination.values == [6, 7, 8, 9, 10]

        new_combination = combination.get_combination(numbers=[6, 7, 8, 9, 10], stars=[4, 12])
        assert isinstance(new_combination, EuroMillionsCombination)
        assert new_combination.values == [6, 7, 8, 9, 10, 4, 12]

        new_combination = new_combination.get_combination(combination.rank)
        assert isinstance(new_combination, EuroMillionsCombination)
        assert new_combination.values == [4, 8, 12, 16, 20, 3, 8]

        with pytest.raises(KeyError):
            _ = combination.get_combination(numbers=[6, 7, 8, 9, 10, 11], extra=[8])

    @pytest.mark.parametrize(
        ("numbers", "stars", "expected", "call_mode"),
        [
            (None, None, None, "none"),
            ([1, 2, 3, 4, 5, 6, 7], None, 1, "values"),
            ([1, 2, 3, 4, 5], [6, 7], 1, "positional"),
            ([1, 2, 3, 4, 5], [6, 7], 1, "keyword"),
            ([1, 2, 3, 4, 5, 7, 8], None, 2, "values"),
            ([1, 2, 3, 4, 5], [7, 8], 2, "positional"),
            ([1, 2, 3, 4, 5], [7, 8], 2, "keyword"),
            ([1, 2, 3, 4, 5], [7], 2, "keyword"),
            ([1, 2, 3, 4, 5, 8, 9], None, 3, "values"),
            ([1, 2, 3, 4, 5], [8, 9], 3, "positional"),
            ([1, 2, 3, 4, 5], [8, 9], 3, "keyword"),
            ([1, 2, 3, 4, 5], [8], 3, "keyword"),
            ([1, 2, 3, 4, 5], [], 3, "keyword"),
            ([1, 2, 3, 4, 6, 6, 7], None, 4, "values"),
            ([1, 2, 3, 4, 6], [6, 7], 4, "positional"),
            ([1, 2, 3, 4, 6], [6, 7], 4, "keyword"),
            ([1, 2, 3, 4], [6, 7], 4, "keyword"),
            ([1, 2, 3, 4, 6, 6, 8], None, 5, "values"),
            ([1, 2, 3, 4, 6], [6, 8], 5, "positional"),
            ([1, 2, 3, 4, 6], [6, 8], 5, "keyword"),
            ([1, 2, 3, 4], [6], 5, "keyword"),
            ([1, 2, 3, 6, 7, 6, 7], None, 6, "values"),
            ([1, 2, 3, 6, 7], [6, 7], 6, "positional"),
            ([1, 2, 3, 6, 7], [6, 7], 6, "keyword"),
            ([1, 2, 3], [6, 7], 6, "keyword"),
            ([1, 2, 3, 4, 6, 8, 9], None, 7, "values"),
            ([1, 2, 3, 4, 6], [8, 9], 7, "keyword"),
            ([1, 2, 3, 4, 6], [8], 7, "keyword"),
            ([1, 2, 3, 4, 6], [], 7, "keyword"),
            ([1, 2, 3, 4], [8, 9], 7, "keyword"),
            ([1, 2, 3, 4], [8], 7, "keyword"),
            ([1, 2, 3, 4], [], 7, "keyword"),
            ([1, 2, 7, 8, 9, 6, 7], None, 8, "values"),
            ([1, 2, 7, 8, 9], [6, 7], 8, "keyword"),
            ([1, 2], [6, 7], 8, "keyword"),
            ([1, 2, 3, 8, 9, 6, 8], None, 9, "values"),
            ([1, 2, 3, 8, 9], [6, 8], 9, "keyword"),
            ([1, 2, 3, 8, 9], [6], 9, "keyword"),
            ([1, 2, 3], [6, 8], 9, "keyword"),
            ([1, 2, 3], [6], 9, "keyword"),
            ([1, 2, 3, 8, 9, 8, 9], None, 10, "values"),
            ([1, 2, 3, 8, 9], [8, 9], 10, "keyword"),
            ([1, 2, 3, 8, 9], [], 10, "keyword"),
            ([1, 2, 3], [8, 9], 10, "keyword"),
            ([1, 2, 3], [], 10, "keyword"),
            ([1, 6, 7, 8, 9, 6, 7], None, 11, "values"),
            ([1, 6, 7, 8, 9], [6, 7], 11, "keyword"),
            ([1], [6, 7], 11, "keyword"),
            ([1, 2, 7, 8, 9], [6, 8], 12, "keyword"),
            ([1, 2, 7, 8, 9], [6], 12, "keyword"),
            ([1, 2], [6, 8], 12, "keyword"),
            ([1, 2], [6], 12, "keyword"),
            ([1, 2, 7, 8, 9], [8, 9], 13, "keyword"),
            ([1, 2, 7, 8, 9], [], 13, "keyword"),
            ([1, 2], [8, 9], 13, "keyword"),
            ([1, 2], [], 13, "keyword"),
            ([6, 7, 8, 9, 10, 8, 9], None, None, "values"),
            ([6, 7, 8, 9, 10], [8, 9], None, "keyword"),
        ],
    )
    def test_combination_get_winning_rank(self, numbers, stars, expected, call_mode):
        """Test EuroMillionsCombination winning rank calculation."""

        combination = EuroMillionsCombination([1, 2, 3, 4, 5], [6, 7])

        if call_mode == "none":
            assert combination.get_winning_rank() is None
            return

        if call_mode == "values":
            assert combination.get_winning_rank(numbers) == expected
            return

        if call_mode == "positional":
            assert combination.get_winning_rank(numbers, stars=stars) == expected
            return

        assert combination.get_winning_rank(numbers=numbers, stars=stars) == expected

    def test_combination_equality(self):
        """Test EuroMillionsCombination equality comparisons."""

        number_rank = get_combination_rank([1, 2, 3, 4, 5], offset=1)
        star_rank = get_combination_rank([1, 2], offset=1)

        combination1 = EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        combination2 = EuroMillionsCombination(numbers=[5, 4, 3, 2, 1], stars=[2, 1])
        combination3 = EuroMillionsCombination(numbers=[1, 2, 4, 5, 7], stars=[3, 4])

        assert EuroMillionsCombination() == EuroMillionsCombination()
        assert EuroMillionsCombination().equals()

        assert combination1 == combination2
        assert combination1 != combination3

        assert combination1.equals(combination1)
        assert combination1.equals(combination2)
        assert not combination1.equals(combination3)

        assert combination1.equals([1, 2, 3, 4, 5, 1, 2])
        assert combination1.equals(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        assert not combination1.equals([1, 2, 4, 5, 7, 3, 4])
        assert not combination1.equals(numbers=[1, 2, 4, 5, 7], stars=[3, 4])

        assert combination1.equals(numbers=number_rank, stars=star_rank)
        assert not combination1.equals(numbers=number_rank + 1, stars=star_rank)

        assert combination1.equals(number_rank * combination1.stars.combinations + star_rank)

    def test_combination_includes(self):
        """Test EuroMillionsCombination includes method."""

        combination1 = EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        combination2 = EuroMillionsCombination(numbers=[1, 2], stars=[1])
        combination3 = EuroMillionsCombination(numbers=[2, 6], stars=[1])

        assert combination1.includes([])
        assert combination1.includes(stars=[1])
        assert combination1.includes(numbers=[2])
        assert combination1.includes([2, 4])
        assert combination1.includes(numbers=[2, 4], stars=[1])

        assert not combination1.includes([], stars=[3])
        assert not combination1.includes([2, 6], stars=[1])
        assert not combination1.includes([6], stars=[1])
        assert not combination1.includes([2, 4], stars=[3])

        assert not combination1.includes([2, 7])
        assert not combination1.includes([7])

        assert combination1.includes(combination2)
        assert not combination1.includes(combination3)

        assert 4 in combination1
        assert 6 not in combination1

        assert [2, 4] in combination1
        assert [2, 6] not in combination1

        assert combination2 in combination1
        assert combination3 not in combination1

    def test_combination_intersects(self):
        """Test EuroMillionsCombination intersects method."""

        combination1 = EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        combination2 = EuroMillionsCombination(numbers=[1, 3, 5, 6, 7], stars=[1, 3])
        combination3 = EuroMillionsCombination(numbers=[6, 7, 8, 9, 10], stars=[3, 4])

        assert combination1.intersects([3])
        assert combination1.intersects([3, 4])
        assert combination1.intersects([3, 4, 5])

        assert combination1.intersects(numbers=[3], stars=[1])
        assert combination1.intersects(numbers=[3, 4], stars=[2])
        assert combination1.intersects(numbers=[3, 4, 5], stars=[1, 2])

        assert not combination1.intersects([6, 7, 8])
        assert not combination1.intersects([6, 7])
        assert not combination1.intersects([6])
        assert not combination1.intersects([])

        assert not combination1.intersects(numbers=[6, 7, 8], stars=[3])
        assert not combination1.intersects(numbers=[6, 7], stars=[3])
        assert not combination1.intersects(numbers=[6], stars=[3])
        assert not combination1.intersects(stars=[3])

        assert combination1.intersects(combination2)
        assert not combination1.intersects(combination3)

    def test_combination_intersection(self):
        """Test EuroMillionsCombination intersection method."""

        combination1 = EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        combination2 = EuroMillionsCombination(numbers=[1, 3, 5, 6, 7], stars=[1, 3])
        combination3 = EuroMillionsCombination(numbers=[6, 7, 8, 9, 10], stars=[3, 4])

        intersection1 = combination1.intersection(numbers=[1, 3, 5, 6, 7], stars=[1, 3])
        intersection2 = combination1.intersection(numbers=[1, 3, 5, 6, 7])
        intersection3 = combination1.intersection(numbers=[6, 7, 8, 9, 10], stars=[3, 4])
        intersection4 = combination1.intersection(numbers=[6, 7, 8, 9, 10])

        assert isinstance(intersection1, EuroMillionsCombination)
        assert isinstance(intersection2, EuroMillionsCombination)
        assert isinstance(intersection3, EuroMillionsCombination)
        assert isinstance(intersection4, EuroMillionsCombination)

        assert intersection1.values == [1, 3, 5, 1]
        assert intersection2.values == [1, 3, 5]
        assert not intersection3.values
        assert not intersection4.values

        assert combination1.intersection(combination2).values == [1, 3, 5, 1]
        assert not combination1.intersection(combination3).values

    def test_combination_compares(self):
        """Test EuroMillionsCombination compares method."""

        combination1 = EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        combination2 = EuroMillionsCombination(numbers=[1, 3, 5, 6, 7], stars=[1, 3])
        combination3 = EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])

        assert combination1.compares(numbers=[1, 3, 5, 6, 7], stars=[1, 3]) == -1
        assert combination2.compares(numbers=[1, 2, 3, 4, 5], stars=[1, 2]) == 1
        assert combination1.compares(numbers=[1, 2, 3, 4, 5], stars=[1, 2]) == 0

        assert combination1.compares([1, 3, 5, 6, 7]) == -1
        assert combination2.compares([1, 2, 3, 4, 5]) == 1

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
        """Test EuroMillionsCombination similarity method."""

        combination1 = EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        combination2 = EuroMillionsCombination(numbers=[1, 3, 5, 6, 7], stars=[1, 3])
        combination3 = EuroMillionsCombination(numbers=[6, 7, 8, 9, 10], stars=[3, 4])

        assert EuroMillionsCombination([]).similarity([]) == 1
        assert EuroMillionsCombination([]).similarity(numbers=[1, 2, 3, 4, 5], stars=[1, 2]) == 0

        assert combination1.similarity(numbers=[1, 2, 3, 4, 5], stars=[1, 2]) == 1
        assert combination1.similarity(numbers=[1, 3, 5, 6, 7], stars=[1, 3]) == 4 / 7
        assert combination1.similarity(numbers=[6, 7, 8, 9, 10], stars=[3, 4]) == 0
        assert combination1.similarity(numbers=[1, 3, 5, 6, 7]) == 3 / 7
        assert combination1.similarity([6, 7, 8, 9, 10]) == 0

        assert combination1.similarity(combination1) == 1
        assert combination1.similarity(combination2) == 4 / 7
        assert combination1.similarity(combination3) == 0

    def test_combination_iteration(self):
        """Test EuroMillionsCombination iteration."""

        combination = EuroMillionsCombination([5, 3, 1, 4, 2], [4, 2])
        assert list(combination) == [1, 2, 3, 4, 5, 2, 4]

    def test_combination_access(self):
        """Test EuroMillionsCombination item access."""

        combination = EuroMillionsCombination([5, 3, 1, 4, 2], [4, 2])

        assert combination[0] == 1
        assert combination[1] == 2
        assert combination[2] == 3
        assert combination[3] == 4
        assert combination[4] == 5
        assert combination[5] == 2
        assert combination[6] == 4

        with pytest.raises(IndexError):
            _ = combination[7]

    def test_combination_length(self):
        """Test EuroMillionsCombination length method."""

        combination = EuroMillionsCombination([5, 3, 1, 4, 2], [4, 2])
        assert len(combination) == 7
        assert combination.length == 7

    def test_combination_string(self):
        """Test EuroMillionsCombination string representation."""

        combination = EuroMillionsCombination([3, 6, 12, 33, 42], [4, 12])
        assert str(combination) == "numbers: [ 3,  6, 12, 33, 42] stars: [ 4, 12]"

    def test_combination_repr(self):
        """Test EuroMillionsCombination repr representation."""

        combination = EuroMillionsCombination([5, 3, 1, 4, 2], [4, 2])
        assert repr(combination) == "EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[2, 4])"

    def test_combination_hash(self):
        """Test EuroMillionsCombination hash method."""

        combination1 = EuroMillionsCombination([1, 2, 3, 4, 5], [1, 2])
        combination2 = EuroMillionsCombination([5, 4, 3, 2, 1], [2, 1])
        combination3 = EuroMillionsCombination([1, 2, 4, 5, 7], [3, 4])

        assert hash(combination1) == hash(combination2)
        assert hash(combination1) != hash(combination3)
        assert hash(combination1) == combination1.rank
