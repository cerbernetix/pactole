"""Unit tests for TimeoutCache class."""

# pylint: disable=unused-argument,redefined-outer-name

from pactole.utils import TimeoutCache


class TestMemoryCache:
    """Tests for TimeoutCache class."""

    def test_init_default_timeout(self, fake_time):
        """Test TimeoutCache initialization with default timeout."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(loader=loader)

        assert cache.data is None
        assert cache.timeout == TimeoutCache.DEFAULT_CACHE_TIMEOUT
        assert not cache.expired
        assert not cache.loaded

    def test_init_custom_timeout(self, fake_time):
        """Test TimeoutCache initialization with custom timeout."""

        def loader():
            return {"data": "value"}

        cache_timeout = 10.0
        cache = TimeoutCache(loader=loader, cache_timeout=cache_timeout)

        assert cache.timeout == cache_timeout
        assert cache.data is None
        assert not cache.loaded

    def test_data_property_before_load(self, fake_time):
        """Test data property returns None before loading."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(loader=loader)

        assert cache.data is None
        assert not cache.loaded

    def test_data_property_after_load(self, fake_time):
        """Test data property returns loaded data after loading."""

        test_data = {"data": "value"}

        def loader():
            return test_data

        cache = TimeoutCache(loader=loader)
        result = cache.load()

        assert result == test_data
        assert cache.data == test_data
        assert cache.loaded

    def test_load_returns_loaded_data(self, fake_time):
        """Test load method returns the loaded data."""

        test_data = {"key": "value"}

        def loader():
            return test_data

        cache = TimeoutCache(loader=loader)

        result = cache.load()

        assert result == test_data
        assert cache.loaded

    def test_load_caches_data(self, fake_time):
        """Test load method caches the data."""

        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"value": call_count}

        cache = TimeoutCache(loader=loader)
        first_result = cache.load()
        second_result = cache.load()

        assert first_result == {"value": 1}
        assert second_result == {"value": 1}
        assert call_count == 1
        assert cache.loaded

    def test_load_with_force_refreshes_cache(self, fake_time):
        """Test load with force=True refreshes the cache."""

        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"value": call_count}

        cache = TimeoutCache(loader=loader)
        first_result = cache.load()
        second_result = cache.load(force=True)

        assert first_result == {"value": 1}
        assert second_result == {"value": 2}
        assert call_count == 2
        assert cache.loaded

    def test_cache_expired_before_timeout(self, fake_time):
        """Test cache expired is False before timeout."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(loader=loader, cache_timeout=10.0)
        cache.load()

        assert not cache.expired
        assert cache.loaded

    def test_cache_expired_after_timeout(self, fake_time):
        """Test cache expired is True after timeout."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(loader=loader, cache_timeout=0.1)
        cache.load()
        fake_time.advance(0.15)

        assert cache.expired
        assert cache.loaded

    def test_load_refreshes_after_expiration(self, fake_time):
        """Test load refreshes cache after expiration."""

        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"value": call_count}

        cache = TimeoutCache(loader=loader, cache_timeout=0.1)
        first_result = cache.load()
        fake_time.advance(0.15)
        second_result = cache.load()

        assert first_result == {"value": 1}
        assert second_result == {"value": 2}
        assert call_count == 2
        assert cache.loaded

    def test_cache_age(self, fake_time):
        """Test cache age returns reasonable value."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(loader=loader, cache_timeout=10.0)
        cache.load()
        age = cache.age

        assert age == 0.0
        assert cache.loaded

    def test_cache_age_increases_over_time(self, fake_time):
        """Test cache age increases over time."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(loader=loader, cache_timeout=10.0)
        cache.load()
        age1 = cache.age
        fake_time.advance(0.1)
        age2 = cache.age

        assert age2 > age1
        assert cache.loaded

    def test_clear_removes_cache(self, fake_time):
        """Test clear method removes cached data."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(loader=loader)
        cache.load()

        assert cache.data is not None
        assert cache.loaded

        cache.clear()

        assert cache.data is None
        assert not cache.loaded

    def test_clear_resets_timeout(self, fake_time):
        """Test clear method resets the timeout."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(loader=loader, cache_timeout=10.0)
        cache.load()

        assert not cache.expired
        assert cache.loaded

        cache.clear()
        fake_time.advance(0.1)

        assert not cache.expired
        assert not cache.loaded

    def test_cache_timeout_setter(self, fake_time):
        """Test cache timeout setter changes timeout."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(loader=loader, cache_timeout=10.0)

        cache.timeout = 20.0

        assert cache.timeout == 20.0
        assert not cache.loaded

    def test_cache_with_none_data(self, fake_time):
        """Test cache can store None as data."""

        def loader():
            return None

        cache = TimeoutCache(loader=loader)
        result = cache.load()

        assert result is None
        assert cache.data is None
        assert cache.loaded

    def test_cache_with_complex_data(self, fake_time):
        """Test cache can store complex data structures."""

        complex_data = {
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
            "tuple": (1, 2, 3),
        }

        def loader():
            return complex_data

        cache = TimeoutCache(loader=loader)
        result = cache.load()

        assert result == complex_data
        assert cache.data == complex_data
        assert cache.loaded

    def test_multiple_loads_return_same_object(self, fake_time):
        """Test multiple loads return the same cached object."""

        test_data = {"data": "value"}

        def loader():
            return test_data

        cache = TimeoutCache(loader=loader)
        result1 = cache.load()
        result2 = cache.load()

        assert result1 is result2
        assert cache.loaded

    def test_loader_called_once_per_cache_cycle(self, fake_time):
        """Test loader is called once per cache cycle."""

        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"value": call_count}

        cache = TimeoutCache(loader=loader, cache_timeout=0.1)
        cache.load()
        cache.load()
        cache.load()

        assert call_count == 1
        assert cache.loaded

        fake_time.advance(0.15)
        cache.load()

        assert call_count == 2

    def test_force_refresh_before_expiration(self, fake_time):
        """Test force refresh works before natural expiration."""

        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"value": call_count}

        cache = TimeoutCache(loader=loader, cache_timeout=10.0)
        cache.load()
        assert not cache.expired
        cache.load(force=True)

        assert call_count == 2
        assert cache.loaded

    def test_set_stores_data(self, fake_time):
        """Test set method stores data and resets timeout."""

        def loader():
            return {"data": "from_loader"}

        cache = TimeoutCache(loader=loader, cache_timeout=10.0)
        new_data = {"data": "from_set"}

        cache.set(new_data)

        assert cache.data == new_data
        assert not cache.expired
        assert cache.loaded

    def test_set_resets_timeout(self, fake_time):
        """Test set method resets the timeout."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(loader=loader, cache_timeout=0.1)
        cache.load()
        fake_time.advance(0.15)

        assert cache.expired

        cache.set({"new": "data"})

        assert not cache.expired
        assert cache.loaded

    def test_set_replaces_cached_data(self, fake_time):
        """Test set method replaces previously cached data."""

        def loader():
            return {"data": "from_loader"}

        cache = TimeoutCache(loader=loader)
        cache.load()

        assert cache.data == {"data": "from_loader"}
        assert cache.loaded

        cache.set({"data": "from_set"})

        assert cache.data == {"data": "from_set"}
        assert cache.loaded

    def test_set_with_none_value(self, fake_time):
        """Test set method can store None value."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(loader=loader)
        cache.set(None)

        assert cache.data is None
        assert cache.loaded

    def test_set_does_not_call_loader(self, fake_time):
        """Test set method does not call the loader function."""

        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"value": call_count}

        cache = TimeoutCache(loader=loader)
        cache.set({"data": "manual"})

        assert cache.data == {"data": "manual"}
        assert call_count == 0
        assert cache.loaded

    def test_init_with_initial_data(self, fake_time):
        """Test TimeoutCache initialization with initial data."""

        def loader():
            return {"data": "from_loader"}

        initial_data = {"data": "initial"}
        cache = TimeoutCache(data=initial_data, loader=loader, cache_timeout=10.0)

        assert cache.data == initial_data
        assert cache.loaded

    def test_init_with_initial_data_starts_timeout(self, fake_time):
        """Test that providing initial data starts the timeout."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(data={"initial": "data"}, loader=loader, cache_timeout=0.1)
        fake_time.advance(0.15)

        assert cache.expired
        assert cache.loaded

    def test_init_without_data_does_not_start_timeout(self, fake_time):
        """Test that without initial data, timeout is not started."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(loader=loader, cache_timeout=0.1)
        fake_time.advance(0.15)

        assert not cache.expired

    def test_init_with_none_data_does_not_start_timeout(self, fake_time):
        """Test that providing None as initial data does not start timeout."""

        def loader():
            return {"data": "value"}

        cache = TimeoutCache(data=None, loader=loader, cache_timeout=0.1)
        fake_time.advance(0.15)

        assert not cache.expired
        assert not cache.loaded

    def test_load_with_initial_data_does_not_call_loader(self, fake_time):
        """Test that load with initial data does not call loader immediately."""

        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"data": "from_loader"}

        cache = TimeoutCache(data={"initial": "data"}, loader=loader)

        assert cache.data == {"initial": "data"}
        assert call_count == 0
        assert cache.loaded

    def test_initial_data_can_be_refreshed(self, fake_time):
        """Test that initial data can be refreshed with load."""

        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"value": call_count}

        cache = TimeoutCache(data={"initial": "data"}, loader=loader, cache_timeout=0.1)

        assert cache.data == {"initial": "data"}
        assert cache.loaded

        fake_time.advance(0.15)
        result = cache.load()

        assert result == {"value": 1}
        assert call_count == 1
        assert cache.loaded

    def test_initial_data_with_force_refresh(self, fake_time):
        """Test force refresh works with initial data."""

        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"value": call_count}

        cache = TimeoutCache(data={"initial": "data"}, loader=loader)

        assert cache.data == {"initial": "data"}
        assert cache.loaded

        result = cache.load(force=True)

        assert result == {"value": 1}
        assert call_count == 1
        assert cache.loaded

    def test_transformer_applied_to_loaded_data(self, fake_time):
        """Test transformer is applied to data returned by loader."""

        cache = TimeoutCache(
            loader=lambda: {"value": 3},
            transformer=lambda data: {"value": data["value"] * 2},
            cache_timeout=10.0,
        )

        result = cache.load()

        assert result == {"value": 6}
        assert cache.data == {"value": 6}
        assert cache.loaded

    def test_non_callable_transformer_fallback_to_identity(self, fake_time):
        """Test non-callable transformer falls back to identity transformer."""

        source = {"value": 7}
        cache = TimeoutCache(
            loader=lambda: source,
            transformer="not callable",
            cache_timeout=10.0,
        )

        result = cache.load()

        assert result == source
        assert result is source

    def test_transformer_called_once_per_cache_cycle(self, fake_time):
        """Test transformer runs once until refresh, then runs again."""

        transform_calls = 0

        def transformer(data):
            nonlocal transform_calls
            transform_calls += 1
            return {"value": data["value"] + 1}

        cache = TimeoutCache(
            loader=lambda: {"value": 1},
            transformer=transformer,
            cache_timeout=0.1,
        )

        first = cache.load()
        second = cache.load()

        assert first == {"value": 2}
        assert second == {"value": 2}
        assert transform_calls == 1

        fake_time.advance(0.15)
        refreshed = cache.load()

        assert refreshed == {"value": 2}
        assert transform_calls == 2

    def test_load_raw_returns_loader_data_without_transformer(self, fake_time):
        """Test load_raw bypasses transformer and returns raw loader result."""

        source = {"value": 3}
        transformer_calls = 0

        def transformer(data):
            nonlocal transformer_calls
            transformer_calls += 1
            return {"value": data["value"] * 2}

        cache = TimeoutCache(loader=lambda: source, transformer=transformer, cache_timeout=10.0)

        raw = cache.load_raw()

        assert raw == source
        assert raw is source
        assert transformer_calls == 0

    def test_load_raw_does_not_update_cache_or_timeout(self, fake_time):
        """Test load_raw keeps cache unloaded and timeout inactive."""

        cache = TimeoutCache(loader=lambda: {"value": 1}, cache_timeout=0.1)

        raw = cache.load_raw()
        fake_time.advance(0.15)

        assert raw == {"value": 1}
        assert cache.data is None
        assert not cache.loaded
        assert not cache.expired
