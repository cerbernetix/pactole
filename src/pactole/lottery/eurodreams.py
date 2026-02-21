"""EuroDreams lottery module."""

import os

from ..combinations import EuroDreamsCombination
from ..data import BaseProvider
from ..utils import import_namespace
from .base_lottery import BaseLottery


class EuroDreams(BaseLottery):
    """Class representing the EuroDreams lottery.

    EuroDreams is a lottery game where players choose 6 main numbers from 1 to 40 and
    1 dream number from 1 to 5. The total number of combinations is 3,838,380 for the main numbers
    and 5 for the dream numbers. In total, there are 19,191,900 possible combinations.

    Draws take place every Monday and Thursday.

    Environment Variables:
        EURODREAMS_PROVIDER_CLASS (str): The fully qualified class name of the provider to use.
            Defaults to "pactole.data.providers.fdj.FDJProvider".
        EURODREAMS_DRAW_DAYS (str): Comma-separated list of draw days.
            Defaults to "MONDAY,THURSDAY".
        EURODREAMS_DRAW_DAY_REFRESH_TIME (str): Refresh threshold time in "HH:MM" format.
            Defaults to "22:00".
        EURODREAMS_CACHE_NAME (str): The name of the cache to use.
            Defaults to "eurodreams".
        EURODREAMS_ARCHIVES_PAGE (str): The name of the archives page to use.
            Defaults to "eurodreams".

    Args:
        provider (BaseProvider, optional): The data provider to use. If None, a default provider
            will be created using environment variables or defaults. Defaults to None.

    Raises:
        ValueError: If the provider class is not in the correct format.
        ImportError: If the provider cannot be imported.
        AttributeError: If the provider does not exist in the module.

    Examples:
        >>> lottery = EuroDreams()
        >>> lottery.load()
        [DrawRecord(
            period="202002",
            draw_date=datetime.date(2024, 1, 1),
            combination=EuroDreamsCombination(numbers=[1, 2, 3, 4, 5],
            winning_ranks={(5, 0): 1}))]
    """

    DEFAULT_PROVIDER = "pactole.data.providers.fdj.FDJProvider"
    DEFAULT_ARCHIVES_PAGE = "eurodreams"
    DEFAULT_DRAW_DAYS = "MONDAY,THURSDAY"
    DEFAULT_DRAW_DAY_REFRESH_TIME = "22:00"
    DEFAULT_CACHE_NAME = "eurodreams"

    def __init__(self, provider: BaseProvider | None = None) -> None:
        if provider is None:
            provider_class = os.getenv("EURODREAMS_PROVIDER_CLASS", self.DEFAULT_PROVIDER)
            draw_days = os.getenv("EURODREAMS_DRAW_DAYS", self.DEFAULT_DRAW_DAYS).split(",")
            draw_day_refresh_time = os.getenv(
                "EURODREAMS_DRAW_DAY_REFRESH_TIME",
                self.DEFAULT_DRAW_DAY_REFRESH_TIME,
            )
            cache_name = os.getenv("EURODREAMS_CACHE_NAME", self.DEFAULT_CACHE_NAME)
            archives_page = os.getenv("EURODREAMS_ARCHIVES_PAGE", self.DEFAULT_ARCHIVES_PAGE)

            provider_class = import_namespace(provider_class)

            provider = provider_class(
                archives_page,
                draw_days=draw_days,
                draw_day_refresh_time=draw_day_refresh_time,
                combination_factory=EuroDreamsCombination,
                cache_name=cache_name,
            )
        super().__init__(provider)
