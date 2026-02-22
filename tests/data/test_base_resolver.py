"""Unit tests for BaseResolver."""

from __future__ import annotations

from typing import Any, Callable, cast

import pytest

from pactole.data import BaseResolver
from pactole.utils import TimeoutCache


class SampleResolver(BaseResolver):
    """Resolver for tests with a configurable loader."""

    def __init__(self, loader: Callable[[], Any], cache_timeout: float = 3600) -> None:
        self._loader = loader
        super().__init__(cache_timeout=cache_timeout)

    def _load_cache(self) -> dict[str, str]:
        return cast(dict[str, str], self._loader())


class TestBaseResolver:
    """Tests for the BaseResolver class."""

    def test_init_sets_cache_timeout(self) -> None:
        """Test the resolver initializes the cache with the timeout."""

        resolver = SampleResolver(lambda: {}, cache_timeout=12.5)

        assert resolver.cache.timeout == 12.5
        assert not resolver.cache.loaded

    def test_cache_property_returns_memory_cache(self) -> None:
        """Test cache property returns the TimeoutCache instance."""

        resolver = SampleResolver(lambda: {})
        cache = resolver.cache

        assert isinstance(cache, TimeoutCache)
        assert cache is resolver.cache

    def test_load_returns_archives(self) -> None:
        """Test load returns the archives dictionary."""

        data = {"archive.zip": "https://local.test/archive.zip"}
        resolver = SampleResolver(lambda: data)

        result = resolver.load()

        assert result == data
        assert resolver.cache.loaded

    def test_load_force_refreshes_cache(self) -> None:
        """Test load with force refreshes the cache."""

        call_count = 0

        def loader() -> dict[str, str]:
            nonlocal call_count
            call_count += 1
            return {"archive.zip": f"https://local.test/{call_count}.zip"}

        resolver = SampleResolver(loader)
        first_result = resolver.load()
        second_result = resolver.load(force=True)

        assert first_result != second_result
        assert call_count == 2

    def test_resolve_returns_url(self) -> None:
        """Test resolve returns the URL for a known archive."""

        resolver = SampleResolver(lambda: {"archive.zip": "https://local.test/archive.zip"})

        result = resolver.resolve("archive.zip")

        assert result == "https://local.test/archive.zip"

    def test_resolve_unknown_archive_raises(self) -> None:
        """Test resolve raises ValueError when archive is missing."""

        resolver = SampleResolver(lambda: {"archive.zip": "https://local.test/archive.zip"})

        with pytest.raises(ValueError, match="Archive 'missing.zip' not found"):
            resolver.resolve("missing.zip")

    def test_resolve_non_dict_raises(self) -> None:
        """Test resolve raises ValueError when archives are not a dictionary."""

        resolver = SampleResolver(lambda: ["archive.zip"])  # type: ignore[list-item]

        with pytest.raises(ValueError, match="Archive 'archive.zip' not found"):
            resolver.resolve("archive.zip")

    def test_load_cache_not_implemented(self) -> None:
        """Test BaseResolver raises NotImplementedError for _load_cache."""

        resolver = BaseResolver()

        with pytest.raises(NotImplementedError):
            resolver.load()
