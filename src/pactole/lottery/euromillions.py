"""EuroMillions lottery module."""

from ..combinations import EuroMillionsCombination
from ..utils import Weekday
from .base_lottery import BaseLottery


class EuroMillions(BaseLottery):
    """Class representing the EuroMillions lottery.

    EuroMillions is a lottery game where players choose 5 main numbers from 1 to 50 and
    2 star numbers from 1 to 12. The total number of combinations is 2,118,760 for the main numbers
    and 66 for the star numbers. In total, there are 139,838,160 possible combinations.

    Draws take place every Tuesday and Friday.

    Examples:
        >>> lottery = EuroMillions()
        >>> lottery.draw_days
        DrawDays(days=[<Weekday.TUESDAY: 1>, <Weekday.FRIDAY: 4>])
        >>> lottery.combination_factory
        <class 'pactole.combinations.EuroMillionsCombination'>
        >>> lottery.combination_factory(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
        EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
    """

    def __init__(self) -> None:
        super().__init__(
            draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
            combination_factory=EuroMillionsCombination,
        )
