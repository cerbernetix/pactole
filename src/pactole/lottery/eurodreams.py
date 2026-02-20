"""EuroDreams lottery module."""

from ..combinations import EuroDreamsCombination
from ..utils import Weekday
from .base_lottery import BaseLottery


class EuroDreams(BaseLottery):
    """Class representing the EuroDreams lottery.

    EuroDreams is a lottery game where players choose 6 main numbers from 1 to 40 and
    1 dream number from 1 to 5. The total number of combinations is 3,838,380 for the main numbers
    and 5 for the dream numbers. In total, there are 19,191,900 possible combinations.

    Draws take place every Monday and Thursday.

    Examples:
        >>> lottery = EuroDreams()
        >>> lottery.draw_days
        DrawDays(days=[<Weekday.MONDAY: 0>, <Weekday.THURSDAY: 3>])
        >>> lottery.combination_factory
        <class 'pactole.combinations.EuroDreamsCombination'>
        >>> lottery.combination_factory(numbers=[1, 2, 3, 4, 5, 6], dream=[1])
        EuroDreamsCombination(numbers=[1, 2, 3, 4, 5, 6], dream=[1])
    """

    def __init__(self) -> None:
        super().__init__(
            draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
            combination_factory=EuroDreamsCombination,
        )
