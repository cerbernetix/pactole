"""FDJ data providers."""

from __future__ import annotations

import logging
import os

import bs4

from ...utils import TimeoutCache, fetch_content
from ..base_resolver import BaseResolver

logger = logging.getLogger(__name__)


class FDJResolver(BaseResolver):
    """Resolver for FDJ EuroMillions archives.

    Environment Variables:
        FDJ_ARCHIVES_PAGE_URL (str): The URL template for the archives page, which must include the
            placeholder '{name}' for the lottery name. Defaults to
            "https://www.fdj.fr/jeux-de-tirage/{name}/historique".

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
