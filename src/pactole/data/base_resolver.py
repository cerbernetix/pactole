"""Base class for resolving available archives."""

from ..utils import TimeoutCache


class BaseResolver:
    """Base class for resolving available archives.

    Args:
        cache_timeout (float, optional): Time to live for the cache in seconds.
            Defaults to TimeoutCache.DEFAULT_CACHE_TIMEOUT.

    Examples:
        >>> class MyResolver(BaseResolver):
        ...     def _load_cache(self) -> dict[str, str]:
        ...         return {"archive.zip": "https://example.com/archive.zip"}
        ...
        >>> resolver = MyResolver(cache_timeout=600)
        >>> resolver.load()
        {'archive.zip': 'https://example.com/archive.zip'}
        >>> resolver.cache.expired
        False
        >>> resolver.load()  # This will return cached result
        {'archive.zip': 'https://example.com/archive.zip'}
        >>> resolver.load(force=True)  # This will reload the cache
        {'archive.zip': 'https://example.com/archive.zip'}
        >>> sleep(601)  # Wait for cache to expire
        >>> resolver.cache.expired
        True
        >>> resolver.load()  # This will reload the cache
        {'archive.zip': 'https://example.com/archive.zip'}
    """

    _cache: TimeoutCache

    def __init__(self, cache_timeout: float = TimeoutCache.DEFAULT_CACHE_TIMEOUT) -> None:
        self._cache = TimeoutCache(loader=self._load_cache, cache_timeout=cache_timeout)

    @property
    def cache(self) -> TimeoutCache:
        """Get the memory cache instance.

        Returns:
            TimeoutCache: The memory cache instance.

        Examples:
            >>> resolver = BaseResolver(cache_timeout=600)
            >>> resolver.cache
            <pactole.utils.timeout_cache.TimeoutCache object at 0x...>
            >>> resolver.cache.timeout
            600
            >>> resolver.cache.expired
            False
        """
        return self._cache

    def resolve(self, name: str, force: bool = False) -> str:
        """Resolve the URL for a given archive name.

        Args:
            name (str): The name of the archive to resolve.
            force (bool, optional): If True, forces reloading the cache even if it's still valid.
                Defaults to False.

        Returns:
            str: The URL of the resolved archive.

        Raises:
            ValueError: If the specified archive name is not found in the available archives.

        Examples:
            >>> class MyResolver(BaseResolver):
            ...     def _load_cache(self) -> dict[str, str]:
            ...         return {"archive.zip": "https://example.com/archive.zip"}
            ...
            >>> resolver = MyResolver(cache_timeout=600)
            >>> resolver.resolve("archive.zip")
            'https://example.com/archive.zip'
            >>> resolver.resolve("archive.zip", force=True)
            'https://example.com/archive.zip'
        """
        archives = self.load(force=force)
        if not isinstance(archives, dict) or name not in archives:
            raise ValueError(f"Archive '{name}' not found in available archives.")
        return archives[name]

    def load(self, force: bool = False) -> dict[str, str]:
        """Loads the list of available archives.

        Args:
            force (bool): If True, forces reloading the list even if cached.

        Returns:
            dict[str, str]: A dictionary mapping archive filenames to their URLs.

        Examples:
            >>> class MyResolver(BaseResolver):
            ...     def _load_cache(self) -> dict[str, str]:
            ...         return {"archive.zip": "https://example.com/archive.zip"}
            ...
            >>> resolver = MyResolver(cache_timeout=600)
            >>> resolver.load()
            {'archive.zip': 'https://example.com/archive.zip'}
            >>> resolver.load()  # This will return cached result
            {'archive.zip': 'https://example.com/archive.zip'}
            >>> resolver.load(force=True)  # This will reload the cache
            {'archive.zip': 'https://example.com/archive.zip'}
        """
        return self._cache.load(force=force)

    def _load_cache(self) -> dict[str, str]:
        """Loads the list of available archives from the source.

        This method should be implemented by subclasses.

        Returns:
            dict[str, str]: A dictionary mapping archive filenames to their URLs.

        Examples:
            >>> class MyResolver(BaseResolver):
            ...     def _load_cache(self) -> dict[str, str]:
            ...         return {"archive.zip": "https://example.com/archive.zip"}
            ...
            >>> resolver = MyResolver(cache_timeout=600)
            >>> resolver.load()
            {'archive.zip': 'https://example.com/archive.zip'}
        """
        raise NotImplementedError("Subclasses must implement method _load_cache.")
