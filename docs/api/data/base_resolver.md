# BaseResolver

[Pactole Index](../README.md#pactole-index) / [Data](./index.md#data) / BaseResolver

> Auto-generated documentation for [data.base_resolver](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_resolver.py) module.

- [BaseResolver](#baseresolver)
  - [BaseResolver](#baseresolver-1)
    - [BaseResolver()._load_cache](#baseresolver()_load_cache)
    - [BaseResolver().cache](#baseresolver()cache)
    - [BaseResolver().load](#baseresolver()load)
    - [BaseResolver().resolve](#baseresolver()resolve)

## BaseResolver

[Show source in base_resolver.py:6](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_resolver.py#L6)

Base class for resolving available archives.

#### Arguments

- `cache_timeout` *float, optional* - Time to live for the cache in seconds.
    Defaults to TimeoutCache.DEFAULT_CACHE_TIMEOUT.

#### Examples

```python
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
```

#### Signature

```python
class BaseResolver:
    def __init__(
        self, cache_timeout: float = TimeoutCache.DEFAULT_CACHE_TIMEOUT
    ) -> None: ...
```

### BaseResolver()._load_cache

[Show source in base_resolver.py:111](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_resolver.py#L111)

Loads the list of available archives from the source.

This method should be implemented by subclasses.

#### Returns

- `dict[str,` *str]* - A dictionary mapping archive filenames to their URLs.

#### Examples

```python
>>> class MyResolver(BaseResolver):
...     def _load_cache(self) -> dict[str, str]:
...         return {"archive.zip": "https://example.com/archive.zip"}
...
>>> resolver = MyResolver(cache_timeout=600)
>>> resolver.load()
{'archive.zip': 'https://example.com/archive.zip'}
```

#### Signature

```python
def _load_cache(self) -> dict[str, str]: ...
```

### BaseResolver().cache

[Show source in base_resolver.py:39](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_resolver.py#L39)

Get the memory cache instance.

#### Returns

- `TimeoutCache` - The memory cache instance.

#### Examples

```python
>>> resolver = BaseResolver(cache_timeout=600)
>>> resolver.cache
<pactole.utils.timeout_cache.TimeoutCache object at 0x...>
>>> resolver.cache.timeout
600
>>> resolver.cache.expired
False
```

#### Signature

```python
@property
def cache(self) -> TimeoutCache: ...
```

### BaseResolver().load

[Show source in base_resolver.py:87](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_resolver.py#L87)

Loads the list of available archives.

#### Arguments

- `force` *bool* - If True, forces reloading the list even if cached.

#### Returns

- `dict[str,` *str]* - A dictionary mapping archive filenames to their URLs.

#### Examples

```python
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
```

#### Signature

```python
def load(self, force: bool = False) -> dict[str, str]: ...
```

### BaseResolver().resolve

[Show source in base_resolver.py:57](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_resolver.py#L57)

Resolve the URL for a given archive name.

#### Arguments

- `name` *str* - The name of the archive to resolve.
- `force` *bool, optional* - If True, forces reloading the cache even if it's still valid.
    Defaults to False.

#### Returns

- `str` - The URL of the resolved archive.

#### Raises

- `ValueError` - If the specified archive name is not found in the available archives.

#### Examples

```python
>>> class MyResolver(BaseResolver):
...     def _load_cache(self) -> dict[str, str]:
...         return {"archive.zip": "https://example.com/archive.zip"}
...
>>> resolver = MyResolver(cache_timeout=600)
>>> resolver.resolve("archive.zip")
'https://example.com/archive.zip'
>>> resolver.resolve("archive.zip", force=True)
'https://example.com/archive.zip'
```

#### Signature

```python
def resolve(self, name: str, force: bool = False) -> str: ...
```