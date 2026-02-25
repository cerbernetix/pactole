"""Unit tests for BaseProvider."""

from __future__ import annotations

import datetime
import json
import os
import zipfile
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
from typing import Any, Generator, cast
from unittest.mock import patch

import pytest

import pactole.data.base_provider as base_provider_module
from pactole.combinations import BoundCombination, LotteryCombination
from pactole.data import BaseParser, BaseProvider, BaseResolver, DrawRecord, WinningRank
from pactole.data.models import Manifest
from pactole.utils import DrawDays, Weekday


class SampleResolver(BaseResolver):
    """Resolver for tests with a fixed archive map."""

    def __init__(self, archives: dict[str, str]) -> None:
        self._archives = archives
        super().__init__(cache_timeout=0.0)

    def _load_cache(self) -> dict[str, str]:
        return self._archives

    def set_archives(self, archives: dict[str, str]) -> None:
        """Update the archives returned by the resolver."""

        self._archives = archives


class SampleParser(BaseParser):
    """Parser for tests that builds draw records from CSV rows."""

    def __call__(self, data: dict) -> DrawRecord:
        draw_date = datetime.date.fromisoformat(data["draw_date"])
        deadline_date = datetime.date.fromisoformat(data["deadline_date"])
        numbers = {"main": [int(data["main_1"]), int(data["main_2"])]}
        winning_ranks = [
            WinningRank(
                rank=1,
                winners=int(data["rank_1_winners"]),
                gain=float(data["rank_1_gain"]),
            )
        ]

        return DrawRecord(
            period=draw_date.strftime("%Y%m"),
            draw_date=draw_date,
            deadline_date=deadline_date,
            combination=LotteryCombination(),
            numbers=numbers,
            winning_ranks=winning_ranks,
        )


def build_combination(
    combination: LotteryCombination | None = None,
    **components: Any,
) -> LotteryCombination:
    """Build a LotteryCombination with predictable bounds for tests."""

    base_components = {}
    if isinstance(combination, LotteryCombination):
        base_components = combination.components

    component_input = components.get("main", base_components.get("main", []))
    rank = None
    values: Any = component_input
    if isinstance(component_input, dict):
        rank = component_input.get("rank")
        values = component_input.get("values")
    elif isinstance(component_input, BoundCombination):
        rank = component_input.rank
        values = component_input.values

    if isinstance(values, int):
        count = 2
        values_input: Any = values
    else:
        values_list = list(values) if values else []
        count = len(values_list) if values_list else 2
        values_input = values_list

    main_component = BoundCombination(
        values=values_input,
        rank=rank,
        start=1,
        end=50,
        count=count,
    )

    return LotteryCombination(
        main=main_component,
        winning_ranks={(2,): 1, (1,): 2},
    )


def build_source_csv(rows: list[dict[str, Any]]) -> str:
    """Build a CSV payload for the source data used in tests."""

    if not rows:
        return ""

    header = list(rows[0].keys())
    lines = [",".join(header)]
    for row in rows:
        lines.append(",".join(str(row[key]) for key in header))
    return "\n".join(lines) + "\n"


def cache_root(cache_name: str) -> Path:
    """Build the root cache path for a test cache name."""

    return base_provider_module.get_cache_path(BaseProvider.CACHE_ROOT_NAME) / cache_name


def manifest_path(cache_name: str) -> Path:
    """Build the manifest path for a test cache name."""

    return cache_root(cache_name) / BaseProvider.MANIFEST_FILE_NAME


def data_path(cache_name: str) -> Path:
    """Build the data path for a test cache name."""

    return cache_root(cache_name) / BaseProvider.DATA_FILE_NAME


def source_path(cache_name: str, name: str) -> Path:
    """Build the source path for a test cache name and archive."""

    return (cache_root(cache_name) / BaseProvider.SOURCE_DIR_NAME / name).with_suffix(".csv")


def archive_path(cache_name: str, name: str) -> Path:
    """Build the archive path for a test cache name and archive."""

    return (cache_root(cache_name) / BaseProvider.ARCHIVE_DIR_NAME / name).with_suffix(".csv")


def read_manifest(cache_name: str) -> Manifest:
    """Read a manifest file from the cache path."""

    path = manifest_path(cache_name)
    return json.loads(path.read_text(encoding="utf-8"))


def set_future_mtime(path: Path) -> None:
    """Set a file mtime far in the future to keep caches fresh."""

    future = datetime.datetime(2100, 1, 1).timestamp()
    os.utime(path, (future, future))


@contextmanager
def freeze_provider_clock(
    *,
    today: datetime.date,
    now: datetime.datetime,
) -> Generator[None, None, None]:
    """Freeze current date/time for BaseProvider refresh-condition tests."""

    class FrozenDate(datetime.date):
        """Frozen date class for deterministic tests."""

        @classmethod
        def today(cls) -> datetime.date:
            return cls(today.year, today.month, today.day)

    class FrozenDateTime(datetime.datetime):
        """Frozen datetime class for deterministic tests."""

        @classmethod
        def now(cls, tz: datetime.tzinfo | None = None) -> datetime.datetime:
            frozen_now = cls(
                now.year,
                now.month,
                now.day,
                now.hour,
                now.minute,
                now.second,
                now.microsecond,
            )
            if tz is not None:
                return frozen_now.replace(tzinfo=tz)
            return frozen_now

    with (
        patch("pactole.utils.days.datetime.date", FrozenDate),
        patch.object(base_provider_module.datetime, "datetime", FrozenDateTime),
    ):
        yield


class DummyCombination:
    """Combination stub with a predictable generate method for tests."""

    def generate(self, n: int = 1, partitions: int = 1) -> list[str]:
        """Generate a predictable combination string for tests."""
        return [f"generated:{n}:{partitions}"]


class PublicProvider(BaseProvider):
    """Expose limited hooks for BaseProvider tests."""

    def check_last_archive(self, manifest: Manifest) -> bool:
        """Expose the last-archive check for tests."""

        return self._check_last_archive(manifest)

    def build_cache(self, manifest: Manifest) -> None:
        """Expose cache building for tests."""

        self._build_cache(manifest)

    def need_refresh(self) -> bool:
        """Expose refresh check for tests."""

        return self._need_refresh()

    def set_refresh_timeout(self, seconds: float) -> None:
        """Update refresh timeout duration for tests."""

        self._refresh_timeout.seconds = seconds


class TestBaseProvider:
    """Tests for the BaseProvider class."""

    def test_init_coerces_draw_days_to_draw_days(self) -> None:
        """Test draw_days iterables are wrapped in DrawDays."""

        resolver = SampleResolver({})
        parser = SampleParser()

        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
        )

        result = provider.draw_days.get_last_draw_date(datetime.date(2024, 6, 5))

        assert result == datetime.date(2024, 6, 3)
        assert provider.draw_days.days == (Weekday.MONDAY, Weekday.THURSDAY)

    def test_init_accepts_draw_days_instance(self) -> None:
        """Test draw_days accepts a DrawDays instance directly."""

        resolver = SampleResolver({})
        parser = SampleParser()
        draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])

        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
        )

        result = provider.draw_days.get_next_draw_date(datetime.date(2024, 6, 5))

        assert result == datetime.date(2024, 6, 6)
        assert provider.draw_days is draw_days

    def test_init_accepts_draw_day_refresh_time_as_time(self) -> None:
        """Test draw_day_refresh_time accepts a datetime.time instance directly."""

        resolver = SampleResolver({})
        parser = SampleParser()
        refresh_time = datetime.time(22, 30)

        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_day_refresh_time=refresh_time,
        )

        assert provider.draw_day_refresh_time is refresh_time

    def test_init_uses_cache_root_name_parameter(self, tmp_path: Path) -> None:
        """Test cache root name from parameter takes precedence over environment variable."""

        resolver = SampleResolver({})
        parser = SampleParser()
        captured_root_names: list[str] = []

        def fake_get_cache_path(root_name: str) -> Path:
            captured_root_names.append(root_name)
            return tmp_path

        with patch.dict(os.environ, {"PACTOLE_CACHE_ROOT": "env-root"}):
            with patch.object(base_provider_module, "get_cache_path", fake_get_cache_path):
                BaseProvider(
                    resolver=resolver,
                    parser=parser,
                    cache_root_name="param-root",
                )

        assert captured_root_names == ["param-root"]

    def test_init_uses_cache_root_name_from_environment(self, tmp_path: Path) -> None:
        """Test cache root name is read from environment when parameter is not provided."""

        resolver = SampleResolver({})
        parser = SampleParser()
        captured_root_names: list[str] = []

        def fake_get_cache_path(root_name: str) -> Path:
            captured_root_names.append(root_name)
            return tmp_path

        with patch.dict(os.environ, {"PACTOLE_CACHE_ROOT": "env-root"}, clear=False):
            with patch.object(base_provider_module, "get_cache_path", fake_get_cache_path):
                BaseProvider(
                    resolver=resolver,
                    parser=parser,
                )

        assert captured_root_names == ["env-root"]

    def test_init_uses_default_cache_root_name_when_not_provided(self, tmp_path: Path) -> None:
        """Test cache root name defaults to 'pactole' when unset in parameter and environment."""

        resolver = SampleResolver({})
        parser = SampleParser()
        captured_root_names: list[str] = []

        def fake_get_cache_path(root_name: str) -> Path:
            captured_root_names.append(root_name)
            return tmp_path

        with patch.dict(os.environ, {}, clear=True):
            with patch.object(base_provider_module, "get_cache_path", fake_get_cache_path):
                BaseProvider(
                    resolver=resolver,
                    parser=parser,
                )

        assert captured_root_names == [BaseProvider.CACHE_ROOT_NAME]

    def test_generate_uses_combination_factory(self) -> None:
        """Test combination_factory returns the provided factory."""

        resolver = SampleResolver({})
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            combination_factory=DummyCombination,
        )

        result = provider.combination_factory().generate(n=2, partitions=3)

        assert result == ["generated:2:3"]
        assert provider.combination_factory is DummyCombination

    def test_load_uses_cache_when_fresh(self) -> None:
        """Test load returns cached data when up to date."""

        cache_name = "records-fresh"
        draw_days = DrawDays([Weekday.TUESDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        csv_content = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: csv_content.encode("utf-8"),
        ):
            provider.refresh(force=True)
        resolver.set_archives({})
        set_future_mtime(data_path(cache_name))
        fresh_provider = BaseProvider(
            resolver=SampleResolver({}),
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: (_ for _ in ()).throw(AssertionError("refresh not expected")),
        ):
            records = fresh_provider.load()

        assert len(records) == 1
        assert isinstance(records[0], DrawRecord)
        assert records[0].numbers == {"main": [5, 12]}

    def test_load_raw_returns_cached_raw_data(self) -> None:
        """Test load_raw returns untransformed cached records."""

        cache_name = "records-raw-force"
        draw_days = DrawDays([Weekday.TUESDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        provider = BaseProvider(
            resolver=resolver,
            parser=SampleParser(),
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        csv_content = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )

        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: csv_content.encode("utf-8"),
        ):
            raw_records = cast(list[dict[str, Any]], provider.load_raw(force=True))

        assert isinstance(raw_records, list)
        assert len(raw_records) == 1
        first_record = next(iter(raw_records), None)
        assert first_record is not None
        assert isinstance(first_record, dict)
        assert first_record["draw_date"] == last_draw_date.isoformat()
        assert str(first_record["main_1"]) == "5"

    def test_load_raw_uses_cache_when_fresh(self) -> None:
        """Test load_raw uses cache without refreshing when data is fresh."""

        cache_name = "records-raw-fresh"
        draw_days = DrawDays([Weekday.TUESDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        provider = BaseProvider(
            resolver=resolver,
            parser=SampleParser(),
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        csv_content = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: csv_content.encode("utf-8"),
        ):
            provider.refresh(force=True)

        set_future_mtime(data_path(cache_name))
        fresh_provider = BaseProvider(
            resolver=SampleResolver({}),
            parser=SampleParser(),
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: (_ for _ in ()).throw(AssertionError("refresh not expected")),
        ):
            raw_records = cast(list[dict[str, Any]], fresh_provider.load_raw())

        assert isinstance(raw_records, list)
        assert len(raw_records) == 1
        first_record = next(iter(raw_records), None)
        assert first_record is not None
        assert isinstance(first_record, dict)
        assert first_record["draw_date"] == last_draw_date.isoformat()

    def test_need_refresh_returns_true_when_cache_outdated(self) -> None:
        """Test outdated cache data triggers refresh."""

        cache_name = "refresh-outdated-cache"
        draw_days = DrawDays([Weekday.MONDAY])
        provider = PublicProvider(
            resolver=SampleResolver({}),
            parser=SampleParser(),
            draw_days=draw_days,
            cache_name=cache_name,
        )
        path = data_path(cache_name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
        old_timestamp = datetime.datetime(2000, 1, 1).timestamp()
        os.utime(path, (old_timestamp, old_timestamp))

        result = provider.need_refresh()

        assert result is True

    def test_need_refresh_returns_true_when_cache_missing(self) -> None:
        """Test missing cache file triggers refresh."""

        cache_name = "refresh-missing-cache-file"
        provider = PublicProvider(
            resolver=SampleResolver({}),
            parser=SampleParser(),
            draw_days=DrawDays([Weekday.MONDAY]),
            cache_name=cache_name,
        )
        path = data_path(cache_name)
        if path.exists():
            path.unlink()

        result = provider.need_refresh()

        assert result is True

    def test_need_refresh_returns_true_when_cache_empty(self) -> None:
        """Test empty cache data triggers refresh."""

        cache_name = "refresh-empty-cache"
        provider = PublicProvider(
            resolver=SampleResolver({}),
            parser=SampleParser(),
            draw_days=DrawDays([Weekday.MONDAY]),
            cache_name=cache_name,
        )
        path = data_path(cache_name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
        set_future_mtime(path)

        result = provider.need_refresh()

        assert result is True

    def test_need_refresh_returns_true_when_last_record_is_outdated(self) -> None:
        """Test refresh is triggered when the latest draw record is missing after draw day."""

        cache_name = "refresh-stale-record"
        draw_days = DrawDays([Weekday.MONDAY])
        frozen_today = datetime.date(2024, 6, 11)
        frozen_now = datetime.datetime(2024, 6, 11, 9, 0)
        previous_draw_date = datetime.date(2024, 6, 3)
        provider = PublicProvider(
            resolver=SampleResolver({"archive-1": "https://local.test/archive-1.csv"}),
            parser=SampleParser(),
            draw_days=draw_days,
            combination_factory=build_combination,
            draw_day_refresh_time=0,
            cache_name=cache_name,
            refresh_timeout=0,
        )
        payload = build_source_csv(
            [
                {
                    "draw_date": previous_draw_date.isoformat(),
                    "deadline_date": (previous_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: payload.encode("utf-8"),
        ):
            provider.refresh(force=True)
        set_future_mtime(data_path(cache_name))

        with freeze_provider_clock(today=frozen_today, now=frozen_now):
            result = provider.need_refresh()

        assert result is True

    def test_need_refresh_returns_false_when_cache_and_records_are_current(self) -> None:
        """Test fresh cache with up-to-date records does not trigger refresh."""

        cache_name = "refresh-current-cache"
        draw_days = DrawDays([Weekday.MONDAY])
        frozen_today = datetime.date(2024, 6, 11)
        frozen_now = datetime.datetime(2024, 6, 11, 9, 0)
        last_draw_date = datetime.date(2024, 6, 10)
        provider = PublicProvider(
            resolver=SampleResolver({"archive-1": "https://local.test/archive-1.csv"}),
            parser=SampleParser(),
            draw_days=draw_days,
            combination_factory=build_combination,
            draw_day_refresh_time=0,
            cache_name=cache_name,
            refresh_timeout=0,
        )
        payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: payload.encode("utf-8"),
        ):
            provider.refresh(force=True)
        set_future_mtime(data_path(cache_name))

        with freeze_provider_clock(today=frozen_today, now=frozen_now):
            result = provider.need_refresh()

        assert result is False

    def test_need_refresh_returns_false_before_draw_refresh_time_when_timeout_active(self) -> None:
        """Test refresh stays disabled while timeout is active, including on draw day."""

        cache_name = "refresh-before-draw-time-margin"
        draw_days = DrawDays([Weekday.MONDAY])
        frozen_today = datetime.date(2024, 6, 10)
        frozen_now = datetime.datetime(2024, 6, 10, 19, 50)
        last_draw_date = datetime.date(2024, 6, 3)
        provider = PublicProvider(
            resolver=SampleResolver({"archive-1": "https://local.test/archive-1.csv"}),
            parser=SampleParser(),
            draw_days=draw_days,
            combination_factory=build_combination,
            draw_day_refresh_time="20:00",
            cache_name=cache_name,
            refresh_timeout=300,
        )
        payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: payload.encode("utf-8"),
        ):
            provider.refresh(force=True)
        before_refresh_time = datetime.datetime.combine(
            frozen_today,
            datetime.time(19, 50),
        ).timestamp()
        path = data_path(cache_name)
        os.utime(path, (before_refresh_time, before_refresh_time))

        with freeze_provider_clock(today=frozen_today, now=frozen_now):
            result = provider.need_refresh()

        assert result is False

    def test_need_refresh_returns_true_after_draw_refresh_time_on_draw_day(self) -> None:
        """Test draw-day refresh happens after the configured refresh threshold."""

        cache_name = "refresh-after-draw-threshold"
        draw_days = DrawDays([Weekday.MONDAY])
        frozen_today = datetime.date(2024, 6, 10)
        frozen_now = datetime.datetime(2024, 6, 10, 20, 10)
        last_draw_date = datetime.date(2024, 6, 3)
        provider = PublicProvider(
            resolver=SampleResolver({"archive-1": "https://local.test/archive-1.csv"}),
            parser=SampleParser(),
            draw_days=draw_days,
            combination_factory=build_combination,
            draw_day_refresh_time="20:00",
            cache_name=cache_name,
            refresh_timeout=0,
        )
        payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: payload.encode("utf-8"),
        ):
            provider.refresh(force=True)
        before_refresh_time = datetime.datetime.combine(
            frozen_today,
            datetime.time(19, 50),
        ).timestamp()
        path = data_path(cache_name)
        os.utime(path, (before_refresh_time, before_refresh_time))

        with freeze_provider_clock(today=frozen_today, now=frozen_now):
            result = provider.need_refresh()

        assert result is True

    def test_load_skips_refresh_until_timeout_expires(self) -> None:
        """Test load skips refresh checks while timeout has not expired."""

        cache_name = "refresh-timeout-active"
        draw_days = DrawDays([Weekday.MONDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        provider = BaseProvider(
            resolver=resolver,
            parser=SampleParser(),
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
            refresh_timeout=300,
        )
        payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: payload.encode("utf-8"),
        ):
            provider.refresh(force=True)

        resolver.set_archives(
            {
                "archive-1": "https://local.test/archive-1.csv",
                "archive-2": "https://local.test/archive-2.csv",
            }
        )

        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: (_ for _ in ()).throw(AssertionError("refresh not expected")),
        ):
            records = provider.load()

        assert len(records) == 1

    def test_load_refreshes_when_timeout_expires(self) -> None:
        """Test load refreshes data when timeout has expired."""

        cache_name = "refresh-timeout-expired"
        draw_days = DrawDays([Weekday.MONDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        previous_draw_date = last_draw_date - datetime.timedelta(days=7)
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        provider = PublicProvider(
            resolver=resolver,
            parser=SampleParser(),
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
            refresh_timeout=300,
        )
        payload_1 = build_source_csv(
            [
                {
                    "draw_date": previous_draw_date.isoformat(),
                    "deadline_date": (previous_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        payload_2 = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "7",
                    "main_2": "14",
                    "rank_1_winners": "2",
                    "rank_1_gain": "200.0",
                }
            ]
        )

        def fake_fetch_content(url: str, **_kwargs: Any) -> bytes:
            return {
                "https://local.test/archive-1.csv": payload_1.encode("utf-8"),
                "https://local.test/archive-2.csv": payload_2.encode("utf-8"),
            }[url]

        with patch.object(base_provider_module, "fetch_content", fake_fetch_content):
            provider.refresh(force=True)

        resolver.set_archives(
            {
                "archive-1": "https://local.test/archive-1.csv",
                "archive-2": "https://local.test/archive-2.csv",
            }
        )
        provider.set_refresh_timeout(0)

        with patch.object(base_provider_module, "fetch_content", fake_fetch_content):
            records = provider.load()

        assert len(records) == 2

    def test_need_refresh_returns_false_when_cache_is_after_refresh_time(self) -> None:
        """Test refresh is skipped after the configured refresh time."""

        cache_name = "refresh-after-draw-time-margin"
        draw_days = DrawDays([Weekday.MONDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        provider = PublicProvider(
            resolver=SampleResolver({"archive-1": "https://local.test/archive-1.csv"}),
            parser=SampleParser(),
            draw_days=draw_days,
            combination_factory=build_combination,
            draw_day_refresh_time="20:00",
            cache_name=cache_name,
        )
        payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: payload.encode("utf-8"),
        ):
            provider.refresh(force=True)
        after_refresh_time = datetime.datetime.combine(
            last_draw_date,
            datetime.time(20, 10),
        ).timestamp()
        path = data_path(cache_name)
        os.utime(path, (after_refresh_time, after_refresh_time))

        result = provider.need_refresh()

        assert result is False

    def test_refresh_builds_cache_from_manifest(self) -> None:
        """Test refresh builds the cache from resolver archives."""

        csv_content = (
            "draw_date,deadline_date,main_1,main_2,rank_1_winners,rank_1_gain\n"
            "2024-01-02,2024-01-15,5,12,1,100.0\n"
            "2024-01-09,2024-01-20,3,7,0,0.0\n"
        )
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            combination_factory=build_combination,
            draw_days=[Weekday.TUESDAY],
            cache_name="tests",
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: csv_content.encode("utf-8"),
        ):
            records = provider.load(force=True)

        assert len(records) == 2
        assert records[0].numbers == {"main": [5, 12]}
        assert records[0].combination.components["main"].values == [5, 12]

    def test_refresh_skips_rebuild_when_manifest_current(self) -> None:
        """Test refresh avoids rebuild when manifest is current."""

        cache_name = "refresh-current"
        draw_days = DrawDays([Weekday.MONDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        csv_content = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: csv_content.encode("utf-8"),
        ):
            provider.refresh(force=True)
            mtime_before = data_path(cache_name).stat().st_mtime

            provider.refresh()

            mtime_after = data_path(cache_name).stat().st_mtime

        assert mtime_before == mtime_after

    def test_refresh_builds_cache_when_cache_missing(self) -> None:
        """Test refresh rebuilds cache when manifest exists but cache is missing."""

        cache_name = "refresh-missing-cache"
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        draw_days = DrawDays([Weekday.TUESDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        csv_content = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: csv_content.encode("utf-8"),
        ):
            provider.refresh(force=True)
            data_path(cache_name).unlink()

            provider.refresh()

        assert data_path(cache_name).exists()
        records = provider.load()

        assert len(records) == 1

    def test_refresh_skips_source_reload_when_files_exist(self) -> None:
        """Test refresh reuses existing files when present."""

        cache_name = "refresh-skip-load"
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        draw_days = DrawDays([Weekday.TUESDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        source = source_path(cache_name, "archive-1")
        archive = archive_path(cache_name, "archive-1")
        source.parent.mkdir(parents=True, exist_ok=True)
        archive.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(payload, encoding="utf-8")
        archive.write_text(payload, encoding="utf-8")
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: (_ for _ in ()).throw(AssertionError("reload not expected")),
        ):
            provider.refresh()

        records = provider.load()

        assert len(records) == 1

    def test_refresh_parses_source_when_archive_missing(self) -> None:
        """Test refresh parses source when archive is missing."""

        cache_name = "refresh-parse-source"
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        draw_days = DrawDays([Weekday.TUESDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        source = source_path(cache_name, "archive-1")
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(payload, encoding="utf-8")
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: (_ for _ in ()).throw(AssertionError("load not expected")),
        ):
            provider.refresh()

        records = provider.load()

        assert len(records) == 1

    def test_refresh_loads_zip_and_plain_sources(self) -> None:
        """Test refresh writes zip and plain sources correctly."""

        cache_name = "refresh-zip"
        resolver = SampleResolver(
            {
                "archive-zip": "https://local.test/archive.zip",
                "archive-plain": "https://local.test/archive.csv",
            }
        )
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=[Weekday.TUESDAY],
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        zip_buffer = BytesIO()
        zip_payload = build_source_csv(
            [
                {
                    "draw_date": "2024-01-02",
                    "deadline_date": "2024-01-15",
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with zipfile.ZipFile(zip_buffer, "w") as archive:
            archive.writestr("data.csv", zip_payload)
        zip_content = zip_buffer.getvalue()
        plain_content = build_source_csv(
            [
                {
                    "draw_date": "2024-01-09",
                    "deadline_date": "2024-01-20",
                    "main_1": "3",
                    "main_2": "7",
                    "rank_1_winners": "0",
                    "rank_1_gain": "0.0",
                }
            ]
        ).encode("utf-8")

        def fake_fetch_content(url: str, **_kwargs: Any) -> bytes:
            return {
                "https://local.test/archive.zip": zip_content,
                "https://local.test/archive.csv": plain_content,
            }[url]

        with patch.object(base_provider_module, "fetch_content", fake_fetch_content):
            provider.refresh(force=True)

        zip_source = source_path(cache_name, "archive-zip")
        plain_source = source_path(cache_name, "archive-plain")

        assert zip_source.read_text(encoding="utf-8") == zip_payload
        assert plain_source.read_bytes() == plain_content

    def test_refresh_no_archives_leaves_manifest_unchanged(self) -> None:
        """Test refresh keeps the manifest intact when the resolver has no archives."""

        cache_name = "refresh-no-archives"
        draw_days = DrawDays([Weekday.MONDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: payload.encode("utf-8"),
        ):
            provider.refresh(force=True)
        resolver.set_archives({})
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: (_ for _ in ()).throw(AssertionError("refresh not expected")),
        ):
            provider.refresh()

        assert len(read_manifest(cache_name)) == 1
        assert len(provider.load()) == 1

    def test_build_cache_skips_missing_archive_file(self) -> None:
        """Test cache build skips archives that are missing on disk."""

        cache_name = "build-cache-missing-archive"
        provider = PublicProvider(
            resolver=SampleResolver({}),
            parser=SampleParser(),
            draw_days=[Weekday.TUESDAY],
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        manifest: Manifest = [
            {
                "name": "missing-archive",
                "url": "https://local.test/missing.csv",
                "period": "202401",
                "first_date": "2024-01-02",
                "last_date": "2024-01-02",
                "count": 1,
            }
        ]

        provider.build_cache(manifest)

        assert data_path(cache_name).exists()
        assert data_path(cache_name).stat().st_size == 0

    def test_check_last_archive_returns_false_for_empty_manifest(self) -> None:
        """Test last archive check returns False when the manifest is empty."""

        provider = PublicProvider(
            resolver=SampleResolver({}),
            parser=SampleParser(),
            draw_days=[Weekday.TUESDAY],
        )

        result = provider.check_last_archive([])

        assert result is False

    def test_check_last_archive_refreshes_after_draw_time_on_draw_day(self) -> None:
        """Test last archive refreshes on draw day once refresh time has passed."""

        provider = PublicProvider(
            resolver=SampleResolver({}),
            parser=SampleParser(),
            draw_days=[Weekday.MONDAY],
            draw_day_refresh_time="21:00",
        )
        manifest: Manifest = [
            {
                "name": "archive-1",
                "url": "https://local.test/archive-1.csv",
                "period": "202406",
                "first_date": "2024-06-03",
                "last_date": "2024-06-03",
                "count": 1,
            }
        ]
        payload = build_source_csv(
            [
                {
                    "draw_date": "2024-06-10",
                    "deadline_date": "2024-06-17",
                    "main_1": "3",
                    "main_2": "7",
                    "rank_1_winners": "0",
                    "rank_1_gain": "0.0",
                }
            ]
        )

        class FrozenDateTime(datetime.datetime):
            """Frozen datetime for deterministic tests."""

            @classmethod
            def now(cls, tz=None) -> datetime.datetime:  # noqa: ANN001
                return cls(2024, 6, 10, 21, 30, tzinfo=tz)

        with (
            patch.object(base_provider_module.datetime, "datetime", FrozenDateTime),
            patch.object(
                DrawDays,
                "get_last_draw_date",
                return_value=datetime.date(2024, 6, 10),
            ) as draw_date_mock,
            patch.object(
                base_provider_module,
                "fetch_content",
                lambda **_kwargs: payload.encode("utf-8"),
            ),
        ):
            result = provider.check_last_archive(manifest)

        assert result is True
        draw_date_mock.assert_called_once()
        assert draw_date_mock.call_args.kwargs == {"closest": True}
        assert manifest[0]["last_date"] == "2024-06-10"

    def test_check_last_archive_skips_refresh_before_draw_time_on_draw_day(self) -> None:
        """Test last archive refresh is deferred before refresh time on draw day."""

        provider = PublicProvider(
            resolver=SampleResolver({}),
            parser=SampleParser(),
            draw_days=[Weekday.MONDAY],
            draw_day_refresh_time="21:00",
        )
        manifest: Manifest = [
            {
                "name": "archive-1",
                "url": "https://local.test/archive-1.csv",
                "period": "202406",
                "first_date": "2024-06-03",
                "last_date": "2024-06-03",
                "count": 1,
            }
        ]

        class FrozenDateTime(datetime.datetime):
            """Frozen datetime for deterministic tests."""

            @classmethod
            def now(cls, tz=None) -> datetime.datetime:  # noqa: ANN001
                return cls(2024, 6, 10, 20, 30, tzinfo=tz)

        with (
            patch.object(base_provider_module.datetime, "datetime", FrozenDateTime),
            patch.object(
                DrawDays,
                "get_last_draw_date",
                return_value=datetime.date(2024, 6, 3),
            ) as draw_date_mock,
            patch.object(
                base_provider_module,
                "fetch_content",
                lambda **_kwargs: (_ for _ in ()).throw(AssertionError("refresh not expected")),
            ),
        ):
            result = provider.check_last_archive(manifest)

        assert result is False
        draw_date_mock.assert_called_once()
        assert draw_date_mock.call_args.kwargs == {"closest": False}
        assert manifest[0]["last_date"] == "2024-06-03"

    def test_refresh_adds_new_archive_when_manifest_exists(self) -> None:
        """Test refresh adds new archives discovered by the resolver."""

        cache_name = "refresh-new-archive"
        draw_days = DrawDays([Weekday.TUESDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        previous_draw_date = last_draw_date - datetime.timedelta(days=7)
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        first_payload = build_source_csv(
            [
                {
                    "draw_date": previous_draw_date.isoformat(),
                    "deadline_date": (previous_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        second_payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "3",
                    "main_2": "7",
                    "rank_1_winners": "0",
                    "rank_1_gain": "0.0",
                }
            ]
        )
        contents = {
            "https://local.test/archive-1.csv": first_payload.encode("utf-8"),
            "https://local.test/archive-2.csv": second_payload.encode("utf-8"),
        }
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda url, **_kwargs: contents[url],
        ):
            provider.refresh(force=True)
            resolver.set_archives(
                {
                    "archive-1": "https://local.test/archive-1.csv",
                    "archive-2": "https://local.test/archive-2.csv",
                }
            )

            provider.refresh()

        records = provider.load()
        manifest = read_manifest(cache_name)

        assert len(records) == 2
        assert len(manifest) == 2

    def test_refresh_skips_missing_names_in_archives(self) -> None:
        """Test refresh skips archives that fail membership checks."""

        class FakeArchives(dict):
            """Fake archives that fail membership checks."""

            def __contains__(self, key: object) -> bool:
                return False

        cache_name = "refresh-missing-name"
        draw_days = DrawDays([Weekday.MONDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: payload.encode("utf-8"),
        ):
            provider.refresh(force=True)

        provider = BaseProvider(
            resolver=SampleResolver(FakeArchives({"archive-2": "https://local.test/2.csv"})),
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: (_ for _ in ()).throw(AssertionError("refresh not expected")),
        ):
            provider.refresh()

        manifest = read_manifest(cache_name)
        records = provider.load()

        assert len(manifest) == 1
        assert len(records) == 1

    def test_refresh_repairs_archive_chain_gap(self) -> None:
        """Test refresh repairs archive chains with missing draw dates."""

        cache_name = "refresh-gap"
        draw_days = DrawDays([Weekday.MONDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        previous_draw_date = last_draw_date - datetime.timedelta(days=7)
        older_draw_date = last_draw_date - datetime.timedelta(days=14)
        resolver = SampleResolver(
            {
                "archive-1": "https://local.test/archive-1.csv",
                "archive-2": "https://local.test/archive-2.csv",
            }
        )
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        first_payload = build_source_csv(
            [
                {
                    "draw_date": older_draw_date.isoformat(),
                    "deadline_date": (older_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        second_payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "3",
                    "main_2": "7",
                    "rank_1_winners": "0",
                    "rank_1_gain": "0.0",
                }
            ]
        )
        updated_payload = build_source_csv(
            [
                {
                    "draw_date": older_draw_date.isoformat(),
                    "deadline_date": (older_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                },
                {
                    "draw_date": previous_draw_date.isoformat(),
                    "deadline_date": (previous_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "9",
                    "main_2": "10",
                    "rank_1_winners": "1",
                    "rank_1_gain": "50.0",
                },
            ]
        )
        contents = {
            "https://local.test/archive-1.csv": [
                first_payload.encode("utf-8"),
                updated_payload.encode("utf-8"),
            ],
            "https://local.test/archive-2.csv": [second_payload.encode("utf-8")],
        }

        def fake_fetch_content(url: str, **_kwargs: Any) -> bytes:
            return contents[url].pop(0)

        with patch.object(base_provider_module, "fetch_content", fake_fetch_content):
            provider.refresh(force=True)
            provider.refresh()

        records = provider.load()

        assert any(record.draw_date == previous_draw_date for record in records)

    def test_refresh_keeps_contiguous_archive_chain(self) -> None:
        """Test refresh leaves contiguous archive chains unchanged."""

        cache_name = "refresh-contiguous"
        draw_days = DrawDays([Weekday.MONDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        previous_draw_date = last_draw_date - datetime.timedelta(days=7)
        resolver = SampleResolver(
            {
                "archive-1": "https://local.test/archive-1.csv",
                "archive-2": "https://local.test/archive-2.csv",
            }
        )
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        first_payload = build_source_csv(
            [
                {
                    "draw_date": previous_draw_date.isoformat(),
                    "deadline_date": (previous_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        second_payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "3",
                    "main_2": "7",
                    "rank_1_winners": "0",
                    "rank_1_gain": "0.0",
                }
            ]
        )
        contents = {
            "https://local.test/archive-1.csv": first_payload.encode("utf-8"),
            "https://local.test/archive-2.csv": second_payload.encode("utf-8"),
        }
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda url, **_kwargs: contents[url],
        ):
            provider.refresh(force=True)
            mtime_before = data_path(cache_name).stat().st_mtime
            provider.refresh()

            mtime_after = data_path(cache_name).stat().st_mtime

        assert mtime_before == mtime_after

    def test_refresh_updates_last_archive_when_outdated(self) -> None:
        """Test refresh updates the last archive when outdated."""

        cache_name = "refresh-outdated"
        draw_days = DrawDays([Weekday.MONDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        previous_draw_date = last_draw_date - datetime.timedelta(days=7)
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        first_payload = build_source_csv(
            [
                {
                    "draw_date": previous_draw_date.isoformat(),
                    "deadline_date": (previous_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        updated_payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "3",
                    "main_2": "7",
                    "rank_1_winners": "0",
                    "rank_1_gain": "0.0",
                }
            ]
        )
        contents = [first_payload.encode("utf-8"), updated_payload.encode("utf-8")]
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: contents.pop(0),
        ):
            provider.refresh(force=True)
            provider.refresh()

        records = provider.load()

        assert any(record.draw_date == last_draw_date for record in records)

    def test_refresh_leaves_last_archive_current(self) -> None:
        """Test refresh leaves last archive intact when current."""

        cache_name = "refresh-current-last"
        draw_days = DrawDays([Weekday.MONDAY])
        last_draw_date = draw_days.get_last_draw_date(closest=False)
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=draw_days,
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        payload = build_source_csv(
            [
                {
                    "draw_date": last_draw_date.isoformat(),
                    "deadline_date": (last_draw_date + datetime.timedelta(days=7)).isoformat(),
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                }
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: payload.encode("utf-8"),
        ):
            provider.refresh(force=True)
            mtime_before = data_path(cache_name).stat().st_mtime

            provider.refresh()

            mtime_after = data_path(cache_name).stat().st_mtime

        assert mtime_before == mtime_after

    def test_refresh_parses_archive_without_dates(self) -> None:
        """Test refresh handles archives without draw dates."""

        cache_name = "refresh-no-dates"
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=[Weekday.TUESDAY],
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        source = source_path(cache_name, "archive-1")
        archive = archive_path(cache_name, "archive-1")
        source.parent.mkdir(parents=True, exist_ok=True)
        archive.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("other\nvalue\n", encoding="utf-8")
        archive.write_text("other\nvalue\n", encoding="utf-8")
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: (_ for _ in ()).throw(AssertionError("load not expected")),
        ):
            provider.refresh()

        manifest = read_manifest(cache_name)

        assert manifest[0]["first_date"] is None
        assert manifest[0]["last_date"] is None

    def test_refresh_parses_archive_out_of_order_dates(self) -> None:
        """Test refresh extracts the correct date range from archives."""

        cache_name = "refresh-parse-range"
        resolver = SampleResolver({"archive-1": "https://local.test/archive-1.csv"})
        parser = SampleParser()
        provider = BaseProvider(
            resolver=resolver,
            parser=parser,
            draw_days=[Weekday.TUESDAY],
            combination_factory=build_combination,
            cache_name=cache_name,
        )
        payload = build_source_csv(
            [
                {
                    "draw_date": "2024-01-20",
                    "deadline_date": "2024-01-25",
                    "main_1": "5",
                    "main_2": "12",
                    "rank_1_winners": "1",
                    "rank_1_gain": "100.0",
                },
                {
                    "draw_date": "2024-01-02",
                    "deadline_date": "2024-01-10",
                    "main_1": "3",
                    "main_2": "7",
                    "rank_1_winners": "0",
                    "rank_1_gain": "0.0",
                },
            ]
        )
        with patch.object(
            base_provider_module,
            "fetch_content",
            lambda **_kwargs: payload.encode("utf-8"),
        ):
            provider.refresh(force=True)

        manifest = read_manifest(cache_name)

        assert manifest[0]["first_date"] == "2024-01-02"
        assert manifest[0]["last_date"] == "2024-01-20"


@pytest.fixture(autouse=True)
def _force_temp_cache_root(tmp_path) -> Generator[None, None, None]:
    """Force cache writes to a temporary directory for tests."""

    with patch.object(
        base_provider_module,
        "get_cache_path",
        lambda *_args, **_kwargs: tmp_path,
    ):
        yield
