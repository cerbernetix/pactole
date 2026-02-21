"""Unit tests for MemoryCache class."""

from pactole.utils import MemoryCache


class _TestableCache(MemoryCache):
    """Concrete test cache used to validate MemoryCache hooks."""

    def __init__(self, data=None, refresh=True, read_value=None):
        super().__init__(data=data)
        self._refresh = refresh
        self._read_value = read_value
        self.read_calls = 0
        self.write_calls = []
        self.clear_calls = 0

    def _refresh_condition(self):
        return self._refresh

    def _read(self):
        self.read_calls += 1
        return self._read_value

    def _write(self, data):
        self.write_calls.append(data)
        super()._write(data)

    def _clear(self):
        self.clear_calls += 1
        super()._clear()


class TestBaseCache:
    """Tests for MemoryCache class."""

    def test_init_with_defaults_sets_empty_unloaded_cache(self):
        """Test default initialization state."""

        cache = MemoryCache()

        assert cache.data is None
        assert not cache.loaded

    def test_init_with_data_marks_cache_as_loaded(self):
        """Test initialization with initial data."""

        initial_data = {"value": 1}
        cache = MemoryCache(data=initial_data)

        assert cache.data == initial_data
        assert cache.loaded

    def test_set_updates_cache_and_calls_write_hook(self):
        """Test set stores data and invokes _write hook."""

        payload = {"key": "value"}
        cache = _TestableCache()

        cache.set(payload)

        assert cache.write_calls == [payload]
        assert cache.data == payload
        assert cache.loaded

    def test_load_uses_read_when_refresh_condition_is_true(self):
        """Test load refreshes cache using _read when refresh is needed."""

        cache = _TestableCache(refresh=True, read_value={"value": 1})

        result = cache.load()

        assert cache.read_calls == 1
        assert result == {"value": 1}
        assert cache.data == {"value": 1}
        assert cache.loaded

    def test_load_keeps_existing_data_when_refresh_condition_is_false(self):
        """Test load keeps current data and skips _read when refresh is not needed."""

        cache = _TestableCache(
            data={"value": "existing"}, refresh=False, read_value={"value": "new"}
        )

        result = cache.load()

        assert cache.read_calls == 0
        assert result == {"value": "existing"}
        assert cache.loaded

    def test_load_force_true_bypasses_refresh_condition(self):
        """Test force=True triggers a refresh regardless of refresh condition."""

        cache = _TestableCache(data={"value": 1}, refresh=False, read_value={"value": 2})

        result = cache.load(force=True)

        assert cache.read_calls == 1
        assert result == {"value": 2}
        assert cache.data == {"value": 2}
        assert cache.loaded

    def test_clear_resets_cache_and_loaded_flag(self):
        """Test clear removes cached data and marks cache as unloaded."""

        cache = _TestableCache(data={"value": 1})

        cache.clear()

        assert cache.clear_calls == 1
        assert cache.data is None
        assert not cache.loaded

    def test_default_refresh_condition_loads_once_when_unloaded(self):
        """Test MemoryCache default refresh logic loads only while unloaded."""

        cache = MemoryCache()

        first = cache.load()
        second = cache.load()

        assert first is None
        assert second is None
        assert cache.data is None
        assert cache.loaded

    def test_init_with_loader_uses_loader_in_read(self):
        """Test MemoryCache accepts loader parameter and uses it in default _read."""

        def loader():
            return {"value": "loaded"}

        cache = MemoryCache(loader=loader)
        result = cache.load()

        assert result == {"value": "loaded"}
        assert cache.data == {"value": "loaded"}
        assert cache.loaded

    def test_loader_called_only_on_refresh(self):
        """Test loader is called only when refresh condition is true."""

        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"call": call_count}

        cache = MemoryCache(loader=loader)

        first = cache.load()
        second = cache.load()

        assert first == {"call": 1}
        assert second == {"call": 1}
        assert call_count == 1
        assert cache.loaded

    def test_force_load_calls_loader_again(self):
        """Test force=True on load triggers loader call again."""

        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"call": call_count}

        cache = MemoryCache(loader=loader)

        first = cache.load()
        forced = cache.load(force=True)

        assert first == {"call": 1}
        assert forced == {"call": 2}
        assert call_count == 2

    def test_non_callable_loader_fallback_to_default(self):
        """Test non-callable loader falls back to default no-op loader."""

        cache = MemoryCache(loader="not callable")

        result = cache.load()

        assert result is None
        assert cache.data is None
        assert cache.loaded

    def test_transformer_applied_to_loader_result(self):
        """Test transformer is applied to the value returned by loader."""

        def loader():
            return {"value": 2}

        cache = MemoryCache(loader=loader, transformer=lambda data: {"value": data["value"] * 3})

        result = cache.load()

        assert result == {"value": 6}
        assert cache.data == {"value": 6}
        assert cache.loaded

    def test_non_callable_transformer_fallback_to_identity(self):
        """Test non-callable transformer falls back to identity transformer."""

        source = {"value": 5}
        cache = MemoryCache(loader=lambda: source, transformer="not callable")

        result = cache.load()

        assert result == source
        assert result is source

    def test_loader_and_transformer_called_on_refresh_only(self):
        """Test loader and transformer are called only when a refresh occurs."""

        load_calls = 0
        transform_calls = 0

        def loader():
            nonlocal load_calls
            load_calls += 1
            return {"value": load_calls}

        def transformer(data):
            nonlocal transform_calls
            transform_calls += 1
            return {"value": data["value"] + 10}

        cache = MemoryCache(loader=loader, transformer=transformer)

        first = cache.load()
        second = cache.load()
        forced = cache.load(force=True)

        assert first == {"value": 11}
        assert second == {"value": 11}
        assert forced == {"value": 12}
        assert load_calls == 2
        assert transform_calls == 2

    def test_load_raw_returns_loader_data_without_transformer(self):
        """Test load_raw bypasses transformer and returns raw loader result."""

        source = {"value": 2}
        transformer_calls = 0

        def transformer(data):
            nonlocal transformer_calls
            transformer_calls += 1
            return {"value": data["value"] * 10}

        cache = MemoryCache(loader=lambda: source, transformer=transformer)

        raw = cache.load_raw()

        assert raw == source
        assert raw is source
        assert transformer_calls == 0

    def test_load_raw_does_not_mark_cache_as_loaded(self):
        """Test load_raw does not update cache state or loaded flag."""

        cache = MemoryCache(loader=lambda: {"value": 1})

        result = cache.load_raw()

        assert result == {"value": 1}
        assert cache.data is None
        assert not cache.loaded

    def test_load_raw_calls_loader_each_time(self):
        """Test load_raw invokes loader for each call."""

        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"value": call_count}

        cache = MemoryCache(loader=loader)

        first = cache.load_raw()
        second = cache.load_raw()

        assert first == {"value": 1}
        assert second == {"value": 2}
        assert call_count == 2
