"""Unit tests for EuroDreams lottery."""

from __future__ import annotations

import os
from typing import Any
from unittest.mock import patch

from pactole.combinations import EuroDreamsCombination
from pactole.lottery import EuroDreams


class TestEuroDreams:
    """Tests for EuroDreams initialization."""

    def test_default_provider_uses_defaults(self) -> None:
        """Build a provider with default environment values."""

        instances: list[Any] = []

        class DummyProvider:
            """Provider stub used for default configuration tests."""

            def __init__(
                self,
                archives_page: str,
                *,
                draw_days: list[str],
                draw_day_refresh_time: str,
                combination_factory: type[EuroDreamsCombination],
                cache_name: str,
            ) -> None:
                self.archives_page = archives_page
                self.draw_days = draw_days
                self.draw_day_refresh_time = draw_day_refresh_time
                self.combination_factory = combination_factory
                self.cache_name = cache_name
                self.load_calls: list[bool] = []
                instances.append(self)

            def load(self, force: bool = False) -> list[Any]:
                """Return empty records while tracking load calls."""
                self.load_calls.append(force)
                return []

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "pactole.lottery.eurodreams.import_namespace",
                return_value=DummyProvider,
            ) as import_mock:
                lottery = EuroDreams()

        import_mock.assert_called_once_with("pactole.data.providers.fdj.FDJProvider")

        assert len(instances) == 1

        provider = instances[0]

        assert provider.archives_page == "eurodreams"
        assert provider.draw_days == ["MONDAY", "THURSDAY"]
        assert provider.draw_day_refresh_time == "22:00"
        assert provider.combination_factory is EuroDreamsCombination
        assert provider.cache_name == "eurodreams"

        list(lottery.get_records(force=True))

        assert provider.load_calls == [True]

    def test_default_provider_uses_env_overrides(self) -> None:
        """Build a provider with environment override values."""

        instances: list[Any] = []

        class DummyProvider:
            """Provider stub used for override configuration tests."""

            def __init__(
                self,
                archives_page: str,
                *,
                draw_days: list[str],
                draw_day_refresh_time: str,
                combination_factory: type[EuroDreamsCombination],
                cache_name: str,
            ) -> None:
                self.archives_page = archives_page
                self.draw_days = draw_days
                self.draw_day_refresh_time = draw_day_refresh_time
                self.combination_factory = combination_factory
                self.cache_name = cache_name
                self.load_calls: list[bool] = []
                instances.append(self)

            def load(self, force: bool = False) -> list[Any]:
                """Return empty records while tracking load calls."""
                self.load_calls.append(force)
                return []

        env = {
            "EURODREAMS_PROVIDER_CLASS": "custom.provider.DummyProvider",
            "EURODREAMS_DRAW_DAYS": "SATURDAY,SUNDAY",
            "EURODREAMS_DRAW_DAY_REFRESH_TIME": "21:15",
            "EURODREAMS_CACHE_NAME": "custom-cache",
            "EURODREAMS_ARCHIVES_PAGE": "custom-page",
        }

        with patch.dict(os.environ, env, clear=True):
            with patch(
                "pactole.lottery.eurodreams.import_namespace",
                return_value=DummyProvider,
            ) as import_mock:
                lottery = EuroDreams()

        import_mock.assert_called_once_with("custom.provider.DummyProvider")

        assert len(instances) == 1

        provider = instances[0]

        assert provider.archives_page == "custom-page"
        assert provider.draw_days == ["SATURDAY", "SUNDAY"]
        assert provider.draw_day_refresh_time == "21:15"
        assert provider.combination_factory is EuroDreamsCombination
        assert provider.cache_name == "custom-cache"

        list(lottery.get_records())

        assert provider.load_calls == [False]

    def test_provider_argument_skips_default_setup(self) -> None:
        """Use the provided provider instance without importing defaults."""

        class ProvidedProvider:
            """Provider stub supplied directly to the lottery."""

            def __init__(self) -> None:
                self.load_calls: list[bool] = []

            def load(self, force: bool = False) -> list[Any]:
                """Return empty records while tracking load calls."""
                self.load_calls.append(force)
                return []

        provider = ProvidedProvider()

        with patch("pactole.lottery.eurodreams.import_namespace") as import_mock:
            lottery = EuroDreams(provider=provider)

        import_mock.assert_not_called()

        list(lottery.get_records(force=True))

        assert provider.load_calls == [True]
