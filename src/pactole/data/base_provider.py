"""Base classes for data providers."""

import datetime
import logging
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Any, Iterable

from ..combinations import CombinationFactory, LotteryCombination
from ..utils import (
    Day,
    DrawDays,
    File,
    FileCache,
    Timeout,
    Weekday,
    ensure_directory,
    fetch_content,
    get_cache_path,
    read_zip_file,
)
from .base_parser import BaseParser
from .base_resolver import BaseResolver
from .models import ArchiveContentInfo, ArchiveInfo, DrawRecord, Manifest

logger = logging.getLogger(__name__)


class BaseProvider:
    """A base class for data providers.

    Args:
        resolver (BaseResolver): An instance of a resolver to fetch archive information.
        parser (BaseParser): An instance of a parser to process the archive content.
        draw_days (DrawDays | Iterable[Day | Weekday], optional): An instance of DrawDays or an
            iterable of Day or Weekday representing the draw days of the lottery.
            Defaults to an empty tuple.
        draw_day_refresh_time (str | int | datetime.time, optional): The refresh threshold time on
            draw days. It can be provided as a string in "HH:MM" format, an integer representing
            the hour, or a datetime.time object. Defaults to None, which will be interpreted as
            22:00 (10 PM).
        combination_factory (CombinationFactory | LotteryCombination | Any): A factory function
            or class to create a combination instance. If None, a default LotteryCombination
            instance will be used. Default is None.
        cache_name (str, optional): The name of the cache. Defaults to "default".
        refresh_timeout (int, optional): The timeout in seconds for refreshing the cache. Defaults
            to 300 seconds (5 minutes).

    Examples:
        >>> provider = BaseProvider(
        ...     resolver=MyResolver(),
        ...     parser=MyParser()
        ...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
        ...     draw_day_refresh_time="21:30",
        ...     combination_factory=EuroMillionsCombination,
        ...     cache_name="euromillions",
        ...     refresh_timeout=300,
        ... )
        >>> provider.load()
        [DrawRecord(
            period='202001',
            draw_date=date(2020, 1, 1),
            deadline_date=date(2020, 1, 15),
            combination=EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9]),
            numbers={'number': [5, 12, 23, 34, 45], 'star': [2, 9]},
            winning_ranks=[WinningRank(rank=1, winners=1, gain=1000000.0), ...]
        ), ...]
    """

    CACHE_ROOT_NAME = "pactole"
    SOURCE_DIR_NAME = "sources"
    ARCHIVE_DIR_NAME = "archives"
    MANIFEST_FILE_NAME = "manifest.json"
    DATA_FILE_NAME = "data.csv"
    DEFAULT_CACHE_NAME = "default"
    DEFAULT_DRAW_DAY_REFRESH_TIME = datetime.time(hour=22)
    DEFAULT_REFRESH_TIMEOUT = 300

    _resolver: BaseResolver
    _parser: BaseParser
    _manifest: FileCache
    _cache: FileCache
    _cache_name: str
    _cache_path: Path
    _draw_days: DrawDays
    _draw_day_refresh_time: datetime.time
    _refresh_timeout: Timeout
    _combination_factory: CombinationFactory

    def __init__(
        self,
        resolver: BaseResolver,
        parser: BaseParser,
        draw_days: DrawDays | Iterable[Day | Weekday] = (),
        draw_day_refresh_time: str | int | datetime.time | None = None,
        combination_factory: CombinationFactory | LotteryCombination | Any = None,
        cache_name: str = DEFAULT_CACHE_NAME,
        refresh_timeout: int = DEFAULT_REFRESH_TIMEOUT,
    ) -> None:
        if isinstance(draw_day_refresh_time, int):
            draw_day_refresh_time = datetime.time(hour=draw_day_refresh_time)
        elif isinstance(draw_day_refresh_time, str):
            draw_day_refresh_time = datetime.datetime.strptime(
                draw_day_refresh_time,
                "%H:%M",
            ).time()
        elif not isinstance(draw_day_refresh_time, datetime.time):
            draw_day_refresh_time = self.DEFAULT_DRAW_DAY_REFRESH_TIME

        self._resolver = resolver
        self._parser = parser
        self._cache_name = cache_name
        self._cache_path = get_cache_path(self.CACHE_ROOT_NAME) / cache_name
        self._manifest = FileCache(self._cache_path / self.MANIFEST_FILE_NAME)
        self._cache = FileCache(
            self._cache_path / self.DATA_FILE_NAME,
            transformer=self._load_record_list,
        )
        self._draw_days = draw_days if isinstance(draw_days, DrawDays) else DrawDays(draw_days)
        self._draw_day_refresh_time = draw_day_refresh_time
        self._refresh_timeout = Timeout(refresh_timeout, start=False)
        self._combination_factory = LotteryCombination.get_combination_factory(combination_factory)

    @property
    def draw_days(self) -> DrawDays:
        """Return the draw days of the lottery.

        Returns:
            DrawDays: The draw days of the lottery.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
            ... )
            >>> provider.draw_days
            DrawDays(days=(Weekday.MONDAY, Weekday.THURSDAY))
            >>> provider.draw_days.days
            (Weekday.MONDAY, Weekday.THURSDAY)
            >>> provider.draw_days.get_last_draw_date(date(2024, 6, 5))
            datetime.date(2024, 6, 3)
            >>> provider.draw_days.get_next_draw_date(date(2024, 6, 5))
            datetime.date(2024, 6, 6)
        """
        return self._draw_days

    @property
    def draw_day_refresh_time(self) -> datetime.time:
        """Return the refresh threshold time used on draw days.

        Returns:
            datetime.time: The refresh threshold time used on draw days.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_day_refresh_time="21:30",
            ... )
            >>> provider.draw_day_refresh_time
            datetime.time(21, 30)
        """
        return self._draw_day_refresh_time

    @property
    def combination_factory(self) -> CombinationFactory:
        """Return the combination factory used by the provider.

        Returns:
            CombinationFactory: The combination factory used by the provider.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
            ...     combination_factory=EuroMillionsCombination,
            ... )
            >>> provider.combination_factory
            <class 'pactole.combinations.euro_millions.EuroMillionsCombination'>
            >>> provider.combination_factory()
            EuroMillionsCombination(numbers=[], stars=[])
        """
        return self._combination_factory

    def load(self, force: bool = False) -> list[DrawRecord]:
        """Get the cached data as a list of DrawRecord instances.

        If the cache is missing or outdated, it will be refreshed before returning the data.

        Args:
            force (bool, optional): If True, forces a refresh of the cache before getting the data.
                Defaults to False.

        Returns:
            list[DrawRecord]: A list of DrawRecord instances representing the cached data.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
            ...     combination_factory=EuroMillionsCombination,
            ...     cache_name="euromillions"
            ... )
            >>> provider.load()
            [DrawRecord(
                period='202001',
                draw_date=date(2020, 1, 1),
                deadline_date=date(2020, 1, 15),
                combination=EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9]),
                numbers={'number': [5, 12, 23, 34, 45], 'star': [2, 9]},
                winning_ranks=[WinningRank(rank=1, winners=1, gain=1000000.0), ...]
            ), ...]
        """
        self._refresh_if_needed(force=force)
        return self._cache.load()

    def load_raw(self, force: bool = False) -> list[dict]:
        """Get the cached data as a list of dictionaries.

        If the cache is missing or outdated, it will be refreshed before returning the data.

        The returned list of dictionaries will have the same structure as the data stored in
        the cache file, without being transformed into DrawRecord instances. This can be useful
        for debugging or for scenarios where raw data manipulation is required, like exporting
        to Pandas DataFrame or performing custom analyses.

        Args:
            force (bool, optional): If True, forces a refresh of the cache before getting the data.
                Defaults to False.

        Returns:
            list[dict]: A list of dictionaries representing the cached data.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
            ...     combination_factory=EuroMillionsCombination,
            ...     cache_name="euromillions"
            ... )
            >>> provider.load_raw()
            [
                {
                    'period': '202001',
                    'draw_date': '2020-01-01',
                    'deadline_date': '2020-01-15',
                    'numbers_1': '5',
                    'numbers_2': '12',
                    'numbers_3': '23',
                    'numbers_4': '34',
                    'numbers_5': '45',
                    'stars_1': '2',
                    'stars_2': '9',
                    ...
                },
                ...
            ]
        """
        self._refresh_if_needed(force=force)
        return self._cache.load_raw()

    def refresh(self, force: bool = False) -> None:
        """Refresh the provider's cache.

        If force is True, it will refresh the cache even if it is still valid. Otherwise, it will
        check the manifest of archives and refresh it if necessary.

        The data file will be rebuilt if missing or if the manifest was refreshed.

        Args:
            force (bool, optional): If True, forces a refresh even if the cache is still valid.
                Defaults to False.

        Examples:
            >>> provider = BaseProvider(
            ...     resolver=MyResolver(),
            ...     parser=MyParser(),
            ...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
            ...     combination_factory=EuroMillionsCombination,
            ...     cache_name="euromillions"
            ... )
            >>> provider.refresh()
        """
        manifest = self._manifest.load()
        if force or not manifest:
            manifest = self._load_manifest(force=force)
            refreshed = True

        else:
            refreshed = any(
                (
                    self._check_archives(manifest),
                    self._check_archive_chain(manifest),
                    self._check_last_archive(manifest),
                )
            )

        if refreshed or not self._cache.exists():
            self._build_cache(manifest)
        self._refresh_timeout.start()

    def _refresh_if_needed(self, force: bool = False) -> None:
        """Refresh the provider's cache if necessary."""
        if force or self._need_refresh():
            self.refresh(force=force)

    def _need_refresh(self) -> bool:
        """Check if the cache needs to be refreshed based on the last draw date."""
        if not self._cache.exists():
            return True

        if self._refresh_timeout.started and not self._refresh_timeout.expired:
            return False

        last_draw_date = self._draw_days.get_last_draw_date(closest=False)
        last_draw_datetime = datetime.datetime.combine(last_draw_date, self._draw_day_refresh_time)
        if self._cache.date() < last_draw_datetime:
            return True

        records = self._cache.load()
        if not records:
            return True
        return records[-1].draw_date < last_draw_date

    def _load_manifest(self, force: bool) -> Manifest:
        """Load the manifest of archives."""
        archives = self._resolver.load(force=force)
        manifest = [self._refresh_archive(name, url, force=force) for name, url in archives.items()]
        self._manifest.set(manifest)
        return manifest

    def _refresh_archive(self, name: str, url: str, force: bool = False) -> ArchiveInfo:
        """Refresh a specific archive."""
        source_path = self._get_source_path(name)
        if force or not source_path.exists():
            ensure_directory(source_path)
            self._load_source(url, source_path)
            force = True  # Force parsing if the source was reloaded

        archive_path = self._get_archive_path(name)
        if force or not archive_path.exists():
            ensure_directory(archive_path)
            self._parse_source(source_path, archive_path)

        return ArchiveInfo(
            name=name,
            url=url,
            **self._parse_archive(archive_path),
        )

    def _check_archives(self, manifest: Manifest) -> bool:
        """Check the list of archives match the list of archives from the resolver."""
        archives = self._resolver.load()
        if not archives:
            return False

        manifest_names = {archive["name"] for archive in manifest}
        resolver_names = set(archives.keys())
        updated = False
        for name in resolver_names.difference(manifest_names):
            if name not in archives:
                continue
            url = archives[name]
            manifest.append(self._refresh_archive(name, url, force=True))
            updated = True

        if updated:
            self._manifest.set(manifest)
        return updated

    def _check_archive_chain(self, manifest: Manifest) -> bool:
        """Check the chain of archives to ensure there are no gaps in the data."""
        if not manifest or len(manifest) == 1:
            return False

        manifest.sort(key=lambda x: x["last_date"] or "")
        last_date = Weekday.get_date(manifest[-2]["last_date"])
        next_date = Weekday.get_date(manifest[-1]["first_date"])

        if self._draw_days.get_next_draw_date(last_date, closest=False) != next_date:
            manifest[-2] = self._refresh_archive(
                manifest[-2]["name"],
                manifest[-2]["url"],
                force=True,
            )
            self._manifest.set(manifest)
            return True
        return False

    def _check_last_archive(self, manifest: Manifest) -> bool:
        """Check the last archive to ensure it is up to date with the latest draw date."""
        if not manifest:
            return False

        manifest.sort(key=lambda x: x["last_date"] or "")
        last_date = Weekday.get_date(manifest[-1]["last_date"])
        last_draw_date = self._draw_days.get_last_draw_date(
            closest=datetime.datetime.now().time() >= self._draw_day_refresh_time
        )

        if last_date != last_draw_date:
            manifest[-1] = self._refresh_archive(
                manifest[-1]["name"],
                manifest[-1]["url"],
                force=True,
            )
            self._manifest.set(manifest)
            return True
        return False

    def _build_cache(self, manifest: Manifest) -> None:
        """Build the data file from the manifest of archives."""
        data = []
        for archive in manifest:
            period = archive["period"] or "unknown"
            archive_path = self._get_archive_path(archive["name"])
            if not archive_path.exists():
                continue
            for line in File(archive_path).readlines():
                record = self._load_record({**line, "period": period})
                data.append(record)

        data.sort(key=lambda x: x.draw_date)
        self._cache.set(data)

    def _load_record(self, data: dict) -> DrawRecord:
        """Load a DrawRecord instance from a dictionary of data."""
        return DrawRecord.from_dict(data, combination_factory=self._combination_factory)

    def _load_record_list(self, data: list[dict] | None) -> list[DrawRecord]:
        """Load a list of DrawRecord instances from a list of dictionaries."""
        if not data:
            return []
        return [self._load_record(record) for record in data]

    def _get_source_path(self, name: str) -> Path:
        """Get the file path for the source file of a given archive name."""
        return (self._cache_path / self.SOURCE_DIR_NAME / name).with_suffix(".csv")

    def _get_archive_path(self, name: str) -> Path:
        """Get the file path for the archive file of a given archive name."""
        return (self._cache_path / self.ARCHIVE_DIR_NAME / name).with_suffix(".csv")

    def _load_source(self, url: str, path: Path) -> None:
        """Load the archive content from the given URL and store it in the specified path."""
        logger.info("Fetching archive from %s...", url)
        content = fetch_content(url=url, binary=True)
        io_content = BytesIO(content)
        if zipfile.is_zipfile(io_content):
            content = read_zip_file(file=io_content, encoding="utf-8")
            path.write_text(content, encoding="utf-8")
        else:
            path.write_bytes(content)

    def _parse_source(self, source: Path, archive: Path) -> None:
        """Parse the source file and store the results in the archive path."""
        File(archive).write(self._parser(line).to_dict() for line in File(source).readlines())

    def _parse_archive(self, archive: Path) -> ArchiveContentInfo:
        """Parse the archive file and extract relevant information."""
        first_date = None
        last_date = None
        period = None
        count = 0

        for line in File(archive).readlines():
            count += 1

            draw_date = line.get("draw_date")
            if draw_date:
                if not first_date or draw_date < first_date:
                    first_date = draw_date
                if not last_date or draw_date > last_date:
                    last_date = draw_date

        if first_date:
            period = first_date[:4] + first_date[5:7]

        return ArchiveContentInfo(
            count=count,
            period=period,
            first_date=first_date,
            last_date=last_date,
        )
