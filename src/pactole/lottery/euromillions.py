"""EuroMillions lottery module."""

import os

from ..combinations import EuroMillionsCombination
from ..data import BaseProvider
from ..utils import import_namespace
from .base_lottery import BaseLottery


class EuroMillions(BaseLottery):
    """Class representing the EuroMillions lottery.

    EuroMillions is a lottery game where players choose 5 main numbers from 1 to 50 and
    2 star numbers from 1 to 12. The total number of combinations is 2,118,760 for the main numbers
    and 66 for the star numbers. In total, there are 139,838,160 possible combinations.

    Draws take place every Tuesday and Friday.

    Environment Variables:
        EUROMILLIONS_PROVIDER_CLASS (str): The fully qualified class name of the provider to use.
            Defaults to "pactole.data.providers.fdj.FDJProvider".
        EUROMILLIONS_DRAW_DAYS (str): Comma-separated list of draw days.
            Defaults to "TUESDAY,FRIDAY".
        EUROMILLIONS_DRAW_DAY_REFRESH_TIME (str): Refresh threshold time in "HH:MM" format.
            Defaults to "22:00".
        EUROMILLIONS_CACHE_NAME (str): The name of the cache to use.
            Defaults to "euromillions".
        EUROMILLIONS_ARCHIVES_PAGE (str): The name of the archives page to use.
            Defaults to "euromillions-my-million".

    Args:
        provider (BaseProvider, optional): The data provider to use. If None, a default provider
            will be created using environment variables or defaults. Defaults to None.

    Raises:
        ValueError: If the provider class is not in the correct format.
        ImportError: If the provider cannot be imported.
        AttributeError: If the provider does not exist in the module.

    Examples:
        >>> lottery = EuroMillions()
        >>> lottery.load()
        [DrawRecord(
            period="202311",
            draw_date=datetime.date(2024, 1, 1),
            combination=EuroMillionsCombination(numbers=[1, 2, 3, 4, 5],
            winning_ranks={(5, 0): 1}))]
    """

    DEFAULT_PROVIDER = "pactole.data.providers.fdj.FDJProvider"
    DEFAULT_ARCHIVES_PAGE = "euromillions-my-million"
    DEFAULT_DRAW_DAYS = "TUESDAY,FRIDAY"
    DEFAULT_DRAW_DAY_REFRESH_TIME = "22:00"
    DEFAULT_CACHE_NAME = "euromillions"

    def __init__(self, provider: BaseProvider | None = None) -> None:
        if provider is None:
            provider_class = os.getenv("EUROMILLIONS_PROVIDER_CLASS", self.DEFAULT_PROVIDER)
            draw_days = os.getenv("EUROMILLIONS_DRAW_DAYS", self.DEFAULT_DRAW_DAYS).split(",")
            draw_day_refresh_time = os.getenv(
                "EUROMILLIONS_DRAW_DAY_REFRESH_TIME",
                self.DEFAULT_DRAW_DAY_REFRESH_TIME,
            )
            cache_name = os.getenv("EUROMILLIONS_CACHE_NAME", self.DEFAULT_CACHE_NAME)
            archives_page = os.getenv("EUROMILLIONS_ARCHIVES_PAGE", self.DEFAULT_ARCHIVES_PAGE)

            provider_class = import_namespace(provider_class)

            provider = provider_class(
                archives_page,
                draw_days=draw_days,
                draw_day_refresh_time=draw_day_refresh_time,
                combination_factory=EuroMillionsCombination,
                cache_name=cache_name,
            )

        super().__init__(provider)
