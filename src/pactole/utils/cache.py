"""Cache utilities for in-memory and file-based caching with optional timeout support."""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any, Protocol

from .file import File, FileType
from .timeout import Timeout


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


class TimeoutCache(MemoryCache):
    """A simple in-memory cache with timeout support.

    Args:
        data (Any, optional): Initial data to populate the cache.
            Defaults to None.
        loader (CacheLoader | None, optional): A callable that loads the data to be cached.
            If not provided, it defaults to a function that returns None. Defaults to None.
        transformer (CacheTransformer | None, optional): A callable that transforms the cached data.
            If not provided, it defaults to a function that returns the data unchanged.
            Defaults to None.
        cache_timeout (float, optional): The cache timeout in seconds.
            Defaults to 3600 seconds (1 hour).

    Examples:
        >>> def loader():
        ...     return {"data": "value"}
        ...
        >>> cache = TimeoutCache(loader=loader, cache_timeout=1)
        >>> cache.data
        None
        >>> cache.load()
        {'data': 'value'}
        >>> cache.data
        {'data': 'value'}
        >>> cache.expired
        False
        >>> time.sleep(1.1)
        >>> cache.expired
        True
        >>> cache.load()  # This will reload the cache
        {'data': 'value'}
        >>> cache.clear()
        >>> cache.data
        None
    """

    DEFAULT_CACHE_TIMEOUT = 3600.0

    _timeout: Timeout

    def __init__(
        self,
        data: Any = None,
        loader: CacheLoader | None = None,
        transformer: CacheTransformer | None = None,
        cache_timeout: float = DEFAULT_CACHE_TIMEOUT,
    ) -> None:
        super().__init__(data=data, loader=loader, transformer=transformer)
        self._timeout = Timeout(cache_timeout, start=data is not None)

    def _refresh_condition(self) -> bool:
        return super()._refresh_condition() or self._timeout.expired

    def _read(self) -> Any:
        data = super()._read()
        self._timeout.start()
        return data

    def _write(self, data: Any) -> None:
        super()._write(data)
        self._timeout.start()

    def _clear(self) -> None:
        self._cache = None
        self._timeout.stop()

    @property
    def timeout(self) -> float:
        """Get the cache timeout in seconds.

        Returns:
            float: The cache timeout in seconds.

        Examples:
            >>> def loader():
            ...     return {"data": "value"}
            ...
            >>> cache = TimeoutCache(loader=loader, cache_timeout=10)
            >>> cache.timeout
            10.0
        """
        return self._timeout.seconds

    @timeout.setter
    def timeout(self, value: float) -> None:
        """Set the cache timeout in seconds.

        Args:
            value (float): The new cache timeout in seconds.

        Examples:
        """
        self._timeout.seconds = value

    @property
    def age(self) -> float:
        """Get the age of the cache in seconds.

        Returns:
            float: The age of the cache in seconds.

        Examples:
            >>> def loader():
            ...     return {"data": "value"}
            ...
            >>> cache = TimeoutCache(loader=loader, cache_timeout=10.0)
            >>> cache.load()
            {'data': 'value'}
            >>> age = cache.age
            >>> 0 <= age < 0.1
            True
        """
        return self._timeout.elapsed

    @property
    def expired(self) -> bool:
        """Check if the cache has expired.

        Returns:
            bool: True if the cache has expired, False otherwise.

        Examples:
            >>> def loader():
            ...     return {"data": "value"}
            ...
            >>> cache = TimeoutCache(loader=loader, cache_timeout=1)
            >>> cache.load()
            {'data': 'value'}
            >>> cache.expired
            False
            >>> time.sleep(1.1)
            >>> cache.expired
            True
        """
        return self._timeout.expired


class FileCache(MemoryCache):
    """A cache that stores data in memory, with a loader function to fetch data from files.

    Args:
        file_path (Path | str): The path to the file to cache.
        file_type (FileType | str, optional): The type of the file (e.g., "csv", "json", "txt").
            If not provided, it will be inferred from the file extension. Defaults to None.
        transformer (CacheTransformer | None, optional): A callable that transforms the cached data.
            If not provided, it defaults to a function that returns the data unchanged.
            Defaults to None.

    Examples:
        >>> cache = FileCache("data.csv")
        >>> cache.load()  # Loads data from data.csv
        [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        >>> cache.set([{'name': 'Charlie', 'age': 35}])  # Updates the cache and writes to data.csv
        >>> cache.load()  # Loads the updated data from data.csv
        [{'name': 'Charlie', 'age': 35}]
    """

    _transformer: CacheTransformer
    _file: File

    def __init__(
        self,
        file_path: Path | str,
        file_type: FileType | str | None = None,
        transformer: CacheTransformer | None = None,
    ) -> None:
        super().__init__(loader=lambda: self._file.read(throw=False), transformer=transformer)
        self._file = File(file_path, file_type=file_type)

    def _write(self, data: Any) -> None:
        self._file.write(data, throw=False)
        super()._write(data)

    def _clear(self) -> None:
        self._file.delete(throw=False)
        super()._clear()

    @property
    def path(self) -> Path:
        """Get the file path of the cache.

        Returns:
            Path: The file path of the cache.

        Examples:
            >>> cache = FileCache("data.csv")
            >>> cache.path
            PosixPath('data.csv')
        """
        return self._file.path

    @property
    def type(self) -> FileType:
        """Get the file type of the cache.

        Returns:
            FileType: The file type of the cache.

        Examples:
            >>> cache = FileCache("data.csv")
            >>> cache.type
            <FileType.CSV: 'csv'>
        """
        return self._file.type

    def exists(self) -> bool:
        """Check if the cache file exists.

        Returns:
            bool: True if the cache file exists, False otherwise.

        Examples:
            >>> cache = FileCache("data.csv")
            >>> cache.exists()
            False  # Assuming data.csv does not exist yet
        """
        return self._file.exists()

    def date(self) -> datetime.datetime:
        """Get the last modification date of the cache file.

        Returns:
            datetime.datetime: The last modification date of the cache file.

        Raises:
            FileNotFoundError: If the cache file does not exist.

        Examples:
            >>> cache = FileCache("data.csv")
            >>> cache.date()
            datetime.datetime(2024, 6, 1, 12, 0, 0)  # Example modification time
        """
        return self._file.date()

    def size(self) -> int:
        """Get the size of the cache file in bytes.

        Returns:
            int: The size of the cache file in bytes.

        Examples:
            >>> cache = FileCache("data.csv")
            >>> cache.size()
            1024  # Example file size in bytes
        """
        return self._file.size()
