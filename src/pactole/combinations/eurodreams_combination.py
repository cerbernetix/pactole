"""Module for EuroDreams combination representation and manipulation."""

from __future__ import annotations

from .combination import BoundCombination, CombinationInputOrRank, comb
from .lottery_combination import CombinationWinningRanks, LotteryCombination

NUMBER_COUNT = 6
NUMBER_START = 1
NUMBER_END = 40
NUMBER_COMBINATIONS = comb(NUMBER_END - NUMBER_START + 1, NUMBER_COUNT)

DREAM_COUNT = 1
DREAM_START = 1
DREAM_END = 5
DREAM_COMBINATIONS = comb(DREAM_END - DREAM_START + 1, DREAM_COUNT)

TOTAL_COMBINATIONS = NUMBER_COMBINATIONS * DREAM_COMBINATIONS

WINNING_RANKS = {
    (6, 1): 1,
    (6, 0): 2,
    (5, 1): 3,
    (5, 0): 3,
    (4, 1): 4,
    (4, 0): 4,
    (3, 1): 5,
    (3, 0): 5,
    (2, 1): 6,
    (2, 0): 6,
}


class EuroDreamsCombination(LotteryCombination):
    """Class representing a EuroDreams combination.

    EuroDreams is a lottery game where players choose 6 main numbers from 1 to 40 and
    1 dream number from 1 to 5. The total number of combinations is 3,838,380 for the main numbers
    and 5 for the dream numbers. In total, there are 19,191,900 possible combinations.

    Args:
        numbers (CombinationInputOrRank | EuroDreamsCombination | None): The main numbers of the
            combination or its rank. It can also contain the dream numbers if `dream` is None.
            Default is None.
        dream (CombinationInputOrRank | None): The dream number of the combination.
            If None, the dream number is taken from `numbers`. Default is None.

    Examples:
        >>> euro_comb = EuroDreamsCombination(numbers=[2, 3, 5, 7, 9, 38], dream=[3])
        >>> euro_comb.numbers
        BoundCombination(values=[2, 3, 5, 7, 9, 38], start=1, end=40, count=6, combinations=3838380)
        >>> euro_comb.dream
        BoundCombination(values=[3], start=1, end=5, count=1, combinations=5)
    """

    def __init__(
        self,
        numbers: CombinationInputOrRank | EuroDreamsCombination | None = None,
        dream: CombinationInputOrRank | None = None,
    ) -> None:
        if isinstance(numbers, EuroDreamsCombination):
            dream = numbers.dream.copy(values=dream)
            numbers = numbers.numbers
            super().__init__(numbers=numbers, dream=dream, winning_ranks=WINNING_RANKS)
            return

        if dream is None and numbers is not None and not isinstance(numbers, (int, dict)):
            numbers = list(numbers)
            dream = numbers[NUMBER_COUNT : NUMBER_COUNT + DREAM_COUNT]
            numbers = numbers[:NUMBER_COUNT]

        super().__init__(
            numbers=BoundCombination(
                values=numbers,
                start=NUMBER_START,
                end=NUMBER_END,
                count=NUMBER_COUNT,
                combinations=NUMBER_COMBINATIONS,
            ),
            dream=BoundCombination(
                values=dream,
                start=DREAM_START,
                end=DREAM_END,
                count=DREAM_COUNT,
                combinations=DREAM_COMBINATIONS,
            ),
            winning_ranks=WINNING_RANKS,
        )

    def _create_combination(
        self,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: CombinationInputOrRank | LotteryCombination,
    ) -> EuroDreamsCombination:
        return EuroDreamsCombination(**components)

    def __repr__(self) -> str:
        return f"EuroDreamsCombination(numbers={self.numbers.values}, dream={self.dream.values})"

    def to_dict(self) -> dict:
        """Convert the EuroDreamsCombination to a dictionary.

        Returns:
            dict: A dictionary representation of the EuroDreamsCombination.

        Examples:
            >>> euro_comb = EuroDreamsCombination(numbers=[2, 3, 5, 7, 9, 38], dream=[3])
            >>> euro_comb.to_dict()
            {'numbers': [2, 3, 5, 7, 9, 38], 'dream': [3]}
        """
        return self.dump()

    @classmethod
    def from_dict(cls, data: dict) -> EuroDreamsCombination:
        """Create a EuroDreamsCombination instance from a dictionary.

        Args:
            data (dict): A dictionary containing the combination data.

        Returns:
            EuroDreamsCombination: A new EuroDreamsCombination instance created from
                the dictionary data.

        Examples:
            >>> data = {'numbers': [2, 3, 5, 7, 9, 38], 'dream': [3]}
            >>> euro_comb = EuroDreamsCombination.from_dict(data)
            >>> euro_comb.numbers.values
            [2, 3, 5, 7, 9, 38]
            >>> euro_comb.dream.values
            [3]
        """
        return cls(**data)

    @classmethod
    def from_string(cls, data: str) -> EuroDreamsCombination:
        """Create a EuroDreamsCombination instance from a string representation.

        Args:
            data (str): A string representation of the combination in the format
                "numbers: [n1, n2, n3, n4, n5, n6]  dream: [d1]".

        Returns:
            EuroDreamsCombination: A new EuroDreamsCombination instance created from
                the string data.

        Examples:
            >>> data = "numbers: [2, 3, 5, 7, 9, 38]  dream: [3]"
            >>> euro_comb = EuroDreamsCombination.from_string(data)
            >>> euro_comb.numbers.values
            [2, 3, 5, 7, 9, 38]
            >>> euro_comb.dream.values
            [3]
        """
        components = LotteryCombination.from_string(data)
        return cls(**components)

    @classmethod
    def from_csv(cls, data: dict) -> EuroDreamsCombination:
        """Create a EuroDreamsCombination instance from a CSV string representation.

        Args:
            data (dict): A dictionary representation of the combination in the format
                {"numbers_1": n1, "numbers_2": n2, ..., "dream_1": d1}.

        Returns:
            EuroDreamsCombination: A new EuroDreamsCombination instance created from
                the CSV string data.

        Examples:
            >>> data = {
            ...    'numbers_1': 1,
            ...    'numbers_2': 2,
            ...    'numbers_3': 3,
            ...    'numbers_4': 4,
            ...    'numbers_5': 5,
            ...    'dream_1': 6
            ... }
            >>> euro_comb = EuroDreamsCombination.from_csv(data)
            >>> euro_comb.numbers.values
            [1, 2, 3, 4, 5]
            >>> euro_comb.dream.values
            [6]
        """
        components = LotteryCombination.from_csv(data)
        return cls(**components)
