"""FDJ data providers."""

from __future__ import annotations

import datetime
import logging
import os
import re
from typing import Iterable

import bs4

from ...combinations import CombinationFactory
from ...utils import DrawDays, TimeoutCache, Weekday, fetch_content, get_float, get_int
from ..base_parser import BaseParser
from ..base_provider import BaseProvider
from ..base_resolver import BaseResolver
from ..models import DrawRecord, WinningRank

logger = logging.getLogger(__name__)


class FDJResolver(BaseResolver):
    """Resolver for FDJ EuroMillions archives.

    Environment Variables:
        FDJ_ARCHIVES_PAGE_URL (str): The URL template for the archives page, which must include the
            placeholder '{name}' for the lottery name.
            Defaults to "https://www.fdj.fr/jeux-de-tirage/{name}/historique".

    Args:
        archives_page_url (str): The URL of the archives page. This can be a full URL or a lottery
            name that will be used to construct the URL based on a template.
        cache_timeout (int, optional): Time to live for the cache in seconds.
            Defaults to TimeoutCache.DEFAULT_CACHE_TIMEOUT.

    Examples:
        >>> resolver = FDJResolver("https://www.fdj.fr/...", cache_timeout=600)
        >>> resolver.load()
        {'euromillions_202202': 'https://www.fdj.fr/...', ...}
        >>> resolver = FDJResolver("euromillions-my-million", cache_timeout=600)
        >>> resolver.load()
        {'euromillions_202202': 'https://www.fdj.fr/...', ...}
    """

    ARCHIVES_PAGE_URL = "https://www.fdj.fr/jeux-de-tirage/{name}/historique"

    _archives_page_url: str

    def __init__(
        self,
        archives_page_url: str,
        cache_timeout: int = TimeoutCache.DEFAULT_CACHE_TIMEOUT,
    ) -> None:
        super().__init__(cache_timeout=cache_timeout)
        if not archives_page_url.startswith("http"):
            archives_page_url = FDJResolver.get_archives_page_url(archives_page_url)
        self._archives_page_url = archives_page_url

    def _load_cache(self) -> dict[str, str]:
        logger.info("Fetching list of archives from %s...", self._archives_page_url)
        content = fetch_content(url=self._archives_page_url)
        page = bs4.BeautifulSoup(content, "html.parser")
        return {a["download"]: a["href"] for a in page.select("a[download]")}

    @classmethod
    def get_archives_page_url(cls, name: str) -> str:
        """Get the URL of the archives page for a given lottery name.

        This method constructs the URL of the archives page for a specific lottery based on a
        template URL. The template URL can be defined as the class variable ARCHIVES_PAGE_URL
        or overridden by the environment variable FDJ_ARCHIVES_PAGE_URL. The method ensures that
        the template URL contains the required placeholder for the lottery name and formats the URL
        accordingly.

        Args:
            name (str): The name of the lottery (e.g., "euromillions-my-million", "eurodreams").

        Returns:
            str: The URL of the archives page for the specified lottery.

        Raises:
            ValueError: If the URL template does not contain the required placeholder for the
                lottery name.

        Examples:
            >>> FDJResolver.get_archives_page_url("euromillions-my-million")
            'https://www.fdj.fr/jeux-de-tirage/euromillions-my-million/historique'
            >>> FDJResolver.get_archives_page_url("eurodreams")
            'https://www.fdj.fr/jeux-de-tirage/eurodreams/historique'
        """
        url_template = os.getenv("FDJ_ARCHIVES_PAGE_URL", cls.ARCHIVES_PAGE_URL)
        if "{name}" not in url_template:
            raise ValueError(
                f"Invalid URL template: '{url_template}'. "
                f"It must contain the placeholder '{{name}}'."
            )
        return url_template.format(name=name)


class FDJParser(BaseParser):
    """Parser for FDJ archives.

    Args:
        combination_factory (CombinationFactory | None): A factory function or class to create a
            combination instance. If None, a default LotteryCombination instance will be used.
            Default is None.

    Examples:
        >>> parser = FDJParser()
        >>> data = {
        ...     "date_de_tirage": "01/02/2022",
        ...     "date_de_forclusion": "15/02/2022",
        ...     "nombre_de_gagnant_au_rang1_en_europe": "2",
        ...     "rapport_du_rang1": "1000000,00",
        ...     "boule_1": "1",
        ...     "boule_2": "2",
        ...     "boule_3": "3",
        ...     "boule_4": "4",
        ...     "boule_5": "5",
        ...     "etoile_1": "1",
        ...     "etoile_2": "2",
        ... }
        >>> parsed = parser(data)
        >>> parsed
        {
            "draw_date": "2022-02-01",
            "deadline_date": "2022-02-15",
            "winning_rank_1_winners": 2,
            "winning_rank_1_gain": 1000000.00,
            "number_1": 1,
            "number_2": 2,
            "number_3": 3,
            "number_4": 4,
            "number_5": 5,
            "star_1": 1,
            "star_2": 2,
        }
    """

    SOURCE_DRAW_DATE = "date_de_tirage"
    SOURCE_DEADLINE_DATE = "date_de_forclusion"
    SOURCE_NUMBERS_MAPPING = {
        "boule": "numbers",
        "etoile": "stars",
        "numero_dream": "dream",
    }

    RE_NUMBER = re.compile(r"^(?P<component>\w+)_(?P<index>\d+)$")
    RE_WINNERS = re.compile(r"^nombre_de_gagnant_au_rang(?P<rank>\d+)\w*$")
    RE_GAIN = re.compile(r"^rapport_du_rang(?P<rank>\d+)\w*$")

    def __call__(self, data: dict) -> DrawRecord:
        draw_date = self._format_date(data.get(self.SOURCE_DRAW_DATE, "1970-01-01"))
        deadline_date = self._format_date(data.get(self.SOURCE_DEADLINE_DATE, "1970-01-01"))

        numbers = {}
        winners = {}
        gains = {}

        known = set([self.SOURCE_DRAW_DATE, self.SOURCE_DEADLINE_DATE])
        for key, value in data.items():
            key = str(key)  # Ensure the key is a string for regex matching
            if key in known:
                continue

            if key in self.SOURCE_NUMBERS_MAPPING:
                numbers.setdefault(self.SOURCE_NUMBERS_MAPPING[key], []).append(get_int(value))
                continue

            if match := self.RE_NUMBER.match(key):
                component_name = match.group("component")
                if component_name in self.SOURCE_NUMBERS_MAPPING:
                    component_name = self.SOURCE_NUMBERS_MAPPING[component_name]
                numbers.setdefault(component_name, []).append(get_int(value))
                continue

            if match := self.RE_WINNERS.match(key):
                rank_number = get_int(match.group("rank"))
                if rank_number not in winners:
                    winners[rank_number] = get_int(value)
                continue

            if match := self.RE_GAIN.match(key):
                rank_number = get_int(match.group("rank"))
                if rank_number not in gains:
                    gains[rank_number] = get_float(value)
                continue

        combination = self._combination_factory(**numbers)
        winning_ranks = []

        min_rank = combination.min_winning_rank
        if min_rank is None:
            min_rank = 1
        max_rank = combination.max_winning_rank
        if max_rank is None:
            max_rank = max(winners.keys() | gains.keys() | {0})
        for rank in range(min_rank, max_rank + 1):
            winning_ranks.append(
                WinningRank(rank=rank, winners=winners.get(rank, 0), gain=gains.get(rank, 0.0))
            )

        return DrawRecord(
            period="",
            draw_date=datetime.date.fromisoformat(draw_date),
            deadline_date=datetime.date.fromisoformat(deadline_date),
            combination=combination,
            numbers=numbers,
            winning_ranks=winning_ranks,
        )

    def _format_date(self, value: str) -> str:
        """Format a date string into ISO format (YYYY-MM-DD).

        The method checks the format of the input date string and converts it to ISO format.
        It supports various date formats, including:
        - RFC format (YYYY-MM-DD) and RFC-like format (YYYYMMDD)
        - French format (DD/MM/YYYY), including cases where the year is presented in 2-digit format,
            (e.g., DD/MM/YY)
        """
        if "-" in value:
            # The date is presented in RFC format
            return value

        if "/" in value:
            # The date is presented in French format
            date_parts = value.split("/")
        else:
            # The date is presented in RFC-like format
            date_parts = [
                value[6:8],
                value[4:6],
                value[0:4],
            ]

        # Correct the year when presented in 2-digits format
        if len(date_parts[2]) == 2:
            date_parts[2] = f"20{date_parts[2]}"

        return "-".join(date_parts[::-1])


class FDJProvider(BaseProvider):
    """Data provider for FDJ archives.

    Environment Variables:
        FDJ_ARCHIVES_PAGE_URL (str): The URL template for the archives page, which must include the
            placeholder '{name}' for the lottery name.
            Defaults to "https://www.fdj.fr/jeux-de-tirage/{name}/historique".
        PACTOLE_CACHE_ROOT (str): The root directory for cache files.
            Defaults to "pactole".

    Args:
        resolver (BaseResolver | str): An instance of BaseResolver or the URL of the archives page.
            If a string is provided, a default FDJResolver will be used with the given URL.
        parser (BaseParser | None): An instance of a parser to process the archive content. If None,
            a default FDJParser will be used. Defaults to None.
        draw_days (DrawDays | Iterable[Weekday], optional): An instance of DrawDays or an iterable
            of Weekday representing the draw days of the lottery. Defaults to an empty tuple.
        draw_day_refresh_time (str | int | datetime.time, optional): Refresh threshold time used on
            draw days. It can be provided as a string in "HH:MM" format, an integer representing
            the hour, or a datetime.time object. Defaults to None, which will be interpreted as
            22:00 (10 PM).
        combination_factory (CombinationFactory | None): A factory function or class to create a
            combination instance. If None, a default LotteryCombination instance will be used.
            Default is None.
        cache_name (str, optional): The name of the cache. Defaults to "fdj".

    Examples:
        >>> provider = FDJProvider("https://www.fdj.fr/...")
        >>> provider.refresh()
    """

    DEFAULT_CACHE_NAME = "fdj"

    def __init__(
        self,
        resolver: BaseResolver | str,
        parser: BaseParser | None = None,
        draw_days: DrawDays | Iterable[Weekday] = (),
        draw_day_refresh_time: str | int | datetime.time | None = None,
        combination_factory: CombinationFactory | None = None,
        cache_name: str = DEFAULT_CACHE_NAME,
    ) -> None:
        if isinstance(resolver, str):
            resolver = FDJResolver(resolver)
        if parser is None:
            parser = FDJParser(combination_factory=combination_factory)

        super().__init__(
            resolver,
            parser,
            draw_days=draw_days,
            draw_day_refresh_time=draw_day_refresh_time,
            combination_factory=combination_factory,
            cache_name=cache_name,
        )
