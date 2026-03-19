"""Module for EuroMillions combination representation and manipulation."""

from __future__ import annotations

from .combination import BoundCombination, CombinationInputOrRank, comb
from .lottery_combination import CombinationWinningRanks, LotteryCombination

NUMBER_COUNT = 5
NUMBER_START = 1
NUMBER_END = 50
NUMBER_COMBINATIONS = comb(NUMBER_END - NUMBER_START + 1, NUMBER_COUNT)

STAR_COUNT = 2
STAR_START = 1
STAR_END = 12
STAR_COMBINATIONS = comb(STAR_END - STAR_START + 1, STAR_COUNT)

TOTAL_COMBINATIONS = NUMBER_COMBINATIONS * STAR_COMBINATIONS

WINNING_RANKS = {
    (5, 2): 1,
    (5, 1): 2,
    (5, 0): 3,
    (4, 2): 4,
    (4, 1): 5,
    (3, 2): 6,
    (4, 0): 7,
    (2, 2): 8,
    (3, 1): 9,
    (3, 0): 10,
    (1, 2): 11,
    (2, 1): 12,
    (2, 0): 13,
}


class EuroMillionsCombination(LotteryCombination):
    """Class representing a EuroMillions combination.

    EuroMillions is a lottery game where players choose 5 main numbers from 1 to 50 and
    2 star numbers from 1 to 12. The total number of combinations is 2,118,760 for the main numbers
    and 66 for the star numbers. In total, there are 139,838,160 possible combinations.

    Args:
        numbers (CombinationInputOrRank | EuroMillionsCombination | None): The main numbers of the
            combination or its rank. It can also contain the star numbers if `stars` is None.
            Default is None.
        stars (CombinationInputOrRank | None): The star numbers of the combination, or its rank.
            If None, the star numbers are taken from `numbers`. Default is None.

    Examples:
        >>> euro_comb = EuroMillionsCombination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
        >>> euro_comb.numbers
        BoundCombination(values=[3, 15, 22, 28, 44], start=1, end=50, count=5, combinations=2118760)
        >>> euro_comb.stars
        BoundCombination(values=[2, 9], start=1, end=12, count=2, combinations=66)
    """

    def __init__(
        self,
        numbers: CombinationInputOrRank | EuroMillionsCombination | None = None,
        stars: CombinationInputOrRank | None = None,
    ) -> None:
        if isinstance(numbers, EuroMillionsCombination):
            stars = numbers.stars.copy(values=stars)
            numbers = numbers.numbers
            super().__init__(numbers=numbers, stars=stars, winning_ranks=WINNING_RANKS)
            return

        if stars is None and numbers is not None and not isinstance(numbers, (int, dict)):
            numbers = list(numbers)
            stars = numbers[NUMBER_COUNT : NUMBER_COUNT + STAR_COUNT]
            numbers = numbers[:NUMBER_COUNT]

        super().__init__(
            numbers=BoundCombination(
                values=numbers,
                start=NUMBER_START,
                end=NUMBER_END,
                count=NUMBER_COUNT,
                combinations=NUMBER_COMBINATIONS,
            ),
            stars=BoundCombination(
                values=stars,
                start=STAR_START,
                end=STAR_END,
                count=STAR_COUNT,
                combinations=STAR_COMBINATIONS,
            ),
            winning_ranks=WINNING_RANKS,
        )

    def _create_combination(
        self,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> EuroMillionsCombination:
        return EuroMillionsCombination(**components)

    def __repr__(self) -> str:
        return f"EuroMillionsCombination(numbers={self.numbers.values}, stars={self.stars.values})"

    def to_dict(self) -> dict:
        """Convert the EuroMillionsCombination to a dictionary.

        Returns:
            dict: A dictionary representation of the EuroMillionsCombination.

        Examples:
            >>> euro_comb = EuroMillionsCombination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
            >>> euro_comb.to_dict()
            {'numbers': [3, 15, 22, 28, 44], 'stars': [2, 9]}
        """
        return {name: component.to_json() for name, component in self._components.items()}

    @classmethod
    def from_dict(cls, data: dict) -> EuroMillionsCombination:
        """Create a EuroMillionsCombination instance from a dictionary.

        Args:
            data (dict): A dictionary containing the combination data.

        Returns:
            EuroMillionsCombination: A new EuroMillionsCombination instance created from
                the dictionary data.

        Examples:
            >>> data = {'numbers': [3, 15, 22, 28, 44], 'stars': [2, 9]}
            >>> euro_comb = EuroMillionsCombination.from_dict(data)
            >>> euro_comb.numbers.values
            [3, 15, 22, 28, 44]
            >>> euro_comb.stars.values
            [2, 9]
        """
        return cls(**data)

    @classmethod
    def from_string(cls, data: str) -> EuroMillionsCombination:
        """Create a EuroMillionsCombination instance from a string representation.

        Args:
            data (str): A string representation of the combination, in the format
                "numbers: [n1, n2, n3, n4, n5]  stars: [s1, s2]".

        Returns:
            EuroMillionsCombination: A new EuroMillionsCombination instance created from
                the string data.

        Examples:
            >>> data = "numbers: [3, 15, 22, 28, 44]  stars: [2, 9]"
            >>> euro_comb = EuroMillionsCombination.from_string(data)
            >>> euro_comb.numbers.values
            [3, 15, 22, 28, 44]
            >>> euro_comb.stars.values
            [2, 9]
        """
        components = LotteryCombination.from_string(data)
        return cls(**components)

    @classmethod
    def from_csv(cls, data: dict) -> EuroMillionsCombination:
        """Create a EuroMillionsCombination instance from a CSV string representation.

        Args:
            data (dict): A dictionary representation of the combination, in the format
                {"numbers_1": n1, "numbers_2": n2, ..., "stars_1": s1, "stars_2": s2}.

        Returns:
            EuroMillionsCombination: A new EuroMillionsCombination instance created from
                the CSV string data.

        Examples:
            >>> data = {
            ...    'numbers_1': 3,
            ...    'numbers_2': 15,
            ...    'numbers_3': 22,
            ...    'numbers_4': 28,
            ...    'numbers_5': 44,
            ...    'stars_1': 2,
            ...    'stars_2': 9
            ... }
            >>> euro_comb = EuroMillionsCombination.from_csv(data)
            >>> euro_comb.numbers.values
            [3, 15, 22, 28, 44]
            >>> euro_comb.stars.values
            [2, 9]
        """
        components = LotteryCombination.from_csv(data)
        return cls(**components)
