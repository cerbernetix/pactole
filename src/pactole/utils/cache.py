"""Cache utilities for in-memory caching."""

from __future__ import annotations

from typing import Any, Protocol


class CacheLoader(Protocol):
    """Protocol for cache loader functions."""

    def __call__(self) -> Any:
        """Load data for the cache."""


class CacheTransformer(Protocol):
    """Protocol for cache transformer functions."""

    def __call__(self, data: Any) -> Any:
        """Transform the cached data."""


class MemoryCache:
    """A simple in-memory cache implementation.

    Args:
        data (Any, optional): Initial data to populate the cache.
            Defaults to None.
        loader (CacheLoader | None, optional): A callable that loads the data to be cached.
            If not provided, it defaults to a function that returns None. Defaults to None.
        transformer (CacheTransformer | None, optional): A callable that transforms the cached data.
            If not provided, it defaults to a function that returns the data unchanged.
            Defaults to None.

    Examples:
        >>> class CustomCache(MemoryCache):
        ...     def _read(self):
        ...         return {"data": "value"}
        ...
        >>> cache = CustomCache({"data": "initial"})
        >>> cache.data
        {'data': 'initial'}
        >>> cache.loaded
        True
        >>> cache.load()
        {'data': 'initial'}
        >>> cache.load(force=True)
        {'data': 'value'}
        >>> cache.clear()
        >>> cache.data
        None
    """

    _cache: Any
    _loaded: bool
    _loader: CacheLoader
    _transformer: CacheTransformer

    def __init__(
        self,
        data: Any = None,
        loader: CacheLoader | None = None,
        transformer: CacheTransformer | None = None,
    ) -> None:
        self._cache = data
        self._loader = loader if callable(loader) else (lambda: None)
        self._transformer = transformer if callable(transformer) else (lambda x: x)
        self._loaded = data is not None

    def _refresh_condition(self) -> bool:
        """Determine if the cache should be refreshed. This method should be overridden."""
        return not self._loaded

    def _read(self) -> Any:
        """Read the data to be cached. This method should be overridden."""
        return self._transformer(self._loader())

    def _write(self, data: Any) -> None:
        """Write the data to the cache. This method should be overridden."""
        self._cache = data

    def _clear(self) -> None:
        """Clear the cache. This method should be overridden."""
        self._cache = None

    @property
    def data(self) -> Any:
        """Get the cached data.

        Returns:
            Any: The cached data or None if not loaded.

        Examples:
            >>> cache = MemoryCache()
            >>> cache.data
            None
            >>> cache.set({"key": "value"})
            >>> cache.data
            {'key': 'value'}
        """
        return self._cache

    @property
    def loaded(self) -> bool:
        """Check if the cache has been loaded.

        Returns:
            bool: True if the cache has been loaded, False otherwise.

        Examples:
            >>> class CustomCache(MemoryCache):
            ...     def _read(self):
            ...         return {"data": "value"}
            ...
            >>> cache = CustomCache()
            >>> cache.loaded
            False
            >>> cache.load()
            {'data': 'value'}
            >>> cache.loaded
            True
            >>> cache.clear()
            >>> cache.loaded
            False
            >>> cache.set({"data": "new_value"})
            >>> cache.loaded
            True
        """
        return self._loaded

    def set(self, data: Any) -> None:
        """Set the cached data manually.

        Args:
            data (Any): The data to be cached.

        Examples:
            >>> cache = MemoryCache()
            >>> cache.set({"data": "new_value"})
            >>> cache.data
            {'data': 'new_value'}
        """
        self._write(data)
        self._loaded = True

    def load(self, force: bool = False) -> Any:
        """Load the cached data, refreshing it if necessary.

        Args:
            force (bool, optional): If True, forces a refresh of the cache even if it is still
                valid. Defaults to False.

        Returns:
            Any: The cached data.

        Examples:
            >>> class CustomCache(MemoryCache):
            ...     def _read(self):
            ...         return {"data": "value"}
            ...
            >>> cache = CustomCache()
            >>> cache.load()
            {'data': 'value'}
        """
        if force or self._refresh_condition():
            self._cache = self._read()
            self._loaded = True

        return self._cache

    def load_raw(self) -> Any:
        """Load the raw data from the loader without applying the transformer.

        Note: This method bypasses the cache and always calls the loader directly.

        Returns:
            Any: The raw data without transformation.

        Examples:
            >>> cache = MemoryCache(loader=lambda: {"data": 2}, transformer=lambda x: x * 3)
            >>> cache.load_raw()
            {'data': 2}
            >>> cache.load()
            {'data': 6}
        """
        return self._loader()

    def clear(self) -> None:
        """Clear the cache.

        Examples:
            >>> class CustomCache(MemoryCache):
            ...     def _read(self):
            ...         return {"data": "value"}
            ...
            >>> cache = CustomCache()
            >>> cache.load()
            {'data': 'value'}
            >>> cache.clear()
            >>> cache.data
            None
        """
        self._clear()
        self._loaded = False
