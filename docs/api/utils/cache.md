# Cache

[Pactole Index](../README.md#pactole-index) / [Utils](./index.md#utils) / Cache

> Auto-generated documentation for [utils.cache](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py) module.

- [Cache](#cache)
  - [CacheLoader](#cacheloader)
    - [CacheLoader().__call__](#cacheloader()__call__)
  - [CacheTransformer](#cachetransformer)
    - [CacheTransformer().__call__](#cachetransformer()__call__)
  - [FileCache](#filecache)
    - [FileCache().date](#filecache()date)
    - [FileCache().exists](#filecache()exists)
    - [FileCache().path](#filecache()path)
    - [FileCache().size](#filecache()size)
    - [FileCache().type](#filecache()type)
  - [MemoryCache](#memorycache)
    - [MemoryCache()._clear](#memorycache()_clear)
    - [MemoryCache()._read](#memorycache()_read)
    - [MemoryCache()._refresh_condition](#memorycache()_refresh_condition)
    - [MemoryCache()._write](#memorycache()_write)
    - [MemoryCache().clear](#memorycache()clear)
    - [MemoryCache().data](#memorycache()data)
    - [MemoryCache().load](#memorycache()load)
    - [MemoryCache().load_raw](#memorycache()load_raw)
    - [MemoryCache().loaded](#memorycache()loaded)
    - [MemoryCache().set](#memorycache()set)
  - [TimeoutCache](#timeoutcache)
    - [TimeoutCache().age](#timeoutcache()age)
    - [TimeoutCache().expired](#timeoutcache()expired)
    - [TimeoutCache().timeout](#timeoutcache()timeout)
    - [TimeoutCache().timeout](#timeoutcache()timeout-1)

## CacheLoader

[Show source in cache.py:13](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L13)

Protocol for cache loader functions.

#### Signature

```python
class CacheLoader(Protocol): ...
```

### CacheLoader().__call__

[Show source in cache.py:16](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L16)

Load data for the cache.

#### Signature

```python
def __call__(self) -> Any: ...
```



## CacheTransformer

[Show source in cache.py:20](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L20)

Protocol for cache transformer functions.

#### Signature

```python
class CacheTransformer(Protocol): ...
```

### CacheTransformer().__call__

[Show source in cache.py:23](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L23)

Transform the cached data.

#### Signature

```python
def __call__(self, data: Any) -> Any: ...
```



## FileCache

[Show source in cache.py:349](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L349)

A cache that stores data in memory, with a loader function to fetch data from files.

#### Arguments

file_path (Path | str): The path to the file to cache.
file_type (FileType | str, optional): The type of the file (e.g., "csv", "json", "txt").
    If not provided, it will be inferred from the file extension. Defaults to None.
transformer (CacheTransformer | None, optional): A callable that transforms the cached data.
    If not provided, it defaults to a function that returns the data unchanged.
    Defaults to None.

#### Examples

```python
>>> cache = FileCache("data.csv")
>>> cache.load()  # Loads data from data.csv
[{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
>>> cache.set([{'name': 'Charlie', 'age': 35}])  # Updates the cache and writes to data.csv
>>> cache.load()  # Loads the updated data from data.csv
[{'name': 'Charlie', 'age': 35}]
```

#### Signature

```python
class FileCache(MemoryCache):
    def __init__(
        self,
        file_path: Path | str,
        file_type: FileType | str | None = None,
        transformer: CacheTransformer | None = None,
    ) -> None: ...
```

#### See also

- [MemoryCache](#memorycache)

### FileCache().date

[Show source in cache.py:430](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L430)

Get the last modification date of the cache file.

#### Returns

- `datetime.datetime` - The last modification date of the cache file.

#### Raises

- `FileNotFoundError` - If the cache file does not exist.

#### Examples

```python
>>> cache = FileCache("data.csv")
>>> cache.date()
datetime.datetime(2024, 6, 1, 12, 0, 0)  # Example modification time
```

#### Signature

```python
def date(self) -> datetime.datetime: ...
```

### FileCache().exists

[Show source in cache.py:417](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L417)

Check if the cache file exists.

#### Returns

- `bool` - True if the cache file exists, False otherwise.

#### Examples

```python
>>> cache = FileCache("data.csv")
>>> cache.exists()
False  # Assuming data.csv does not exist yet
```

#### Signature

```python
def exists(self) -> bool: ...
```

### FileCache().path

[Show source in cache.py:389](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L389)

Get the file path of the cache.

#### Returns

- `Path` - The file path of the cache.

#### Examples

```python
>>> cache = FileCache("data.csv")
>>> cache.path
PosixPath('data.csv')
```

#### Signature

```python
@property
def path(self) -> Path: ...
```

### FileCache().size

[Show source in cache.py:446](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L446)

Get the size of the cache file in bytes.

#### Returns

- `int` - The size of the cache file in bytes.

#### Examples

```python
>>> cache = FileCache("data.csv")
>>> cache.size()
1024  # Example file size in bytes
```

#### Signature

```python
def size(self) -> int: ...
```

### FileCache().type

[Show source in cache.py:403](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L403)

Get the file type of the cache.

#### Returns

- `FileType` - The file type of the cache.

#### Examples

```python
>>> cache = FileCache("data.csv")
>>> cache.type
<FileType.CSV: 'csv'>
```

#### Signature

```python
@property
def type(self) -> FileType: ...
```



## MemoryCache

[Show source in cache.py:27](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L27)

A simple in-memory cache implementation.

#### Arguments

- [Data](../data/index.md#data) *Any, optional* - Initial data to populate the cache.
    Defaults to None.
loader (CacheLoader | None, optional): A callable that loads the data to be cached.
    If not provided, it defaults to a function that returns None. Defaults to None.
transformer (CacheTransformer | None, optional): A callable that transforms the cached data.
    If not provided, it defaults to a function that returns the data unchanged.
    Defaults to None.

#### Examples

```python
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
```

#### Signature

```python
class MemoryCache:
    def __init__(
        self,
        data: Any = None,
        loader: CacheLoader | None = None,
        transformer: CacheTransformer | None = None,
    ) -> None: ...
```

### MemoryCache()._clear

[Show source in cache.py:86](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L86)

Clear the cache. This method should be overridden.

#### Signature

```python
def _clear(self) -> None: ...
```

### MemoryCache()._read

[Show source in cache.py:78](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L78)

Read the data to be cached. This method should be overridden.

#### Signature

```python
def _read(self) -> Any: ...
```

### MemoryCache()._refresh_condition

[Show source in cache.py:74](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L74)

Determine if the cache should be refreshed. This method should be overridden.

#### Signature

```python
def _refresh_condition(self) -> bool: ...
```

### MemoryCache()._write

[Show source in cache.py:82](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L82)

Write the data to the cache. This method should be overridden.

#### Signature

```python
def _write(self, data: Any) -> None: ...
```

### MemoryCache().clear

[Show source in cache.py:192](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L192)

Clear the cache.

#### Examples

```python
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
```

#### Signature

```python
def clear(self) -> None: ...
```

### MemoryCache().data

[Show source in cache.py:90](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L90)

Get the cached data.

#### Returns

- `Any` - The cached data or None if not loaded.

#### Examples

```python
>>> cache = MemoryCache()
>>> cache.data
None
>>> cache.set({"key": "value"})
>>> cache.data
{'key': 'value'}
```

#### Signature

```python
@property
def data(self) -> Any: ...
```

### MemoryCache().load

[Show source in cache.py:150](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L150)

Load the cached data, refreshing it if necessary.

#### Arguments

- `force` *bool, optional* - If True, forces a refresh of the cache even if it is still
    valid. Defaults to False.

#### Returns

- `Any` - The cached data.

#### Examples

```python
>>> class CustomCache(MemoryCache):
...     def _read(self):
...         return {"data": "value"}
...
>>> cache = CustomCache()
>>> cache.load()
{'data': 'value'}
```

#### Signature

```python
def load(self, force: bool = False) -> Any: ...
```

### MemoryCache().load_raw

[Show source in cache.py:175](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L175)

Load the raw data from the loader without applying the transformer.

Note: This method bypasses the cache and always calls the loader directly.

#### Returns

- `Any` - The raw data without transformation.

#### Examples

```python
>>> cache = MemoryCache(loader=lambda: {"data": 2}, transformer=lambda x: x * 3)
>>> cache.load_raw()
{'data': 2}
>>> cache.load()
{'data': 6}
```

#### Signature

```python
def load_raw(self) -> Any: ...
```

### MemoryCache().loaded

[Show source in cache.py:107](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L107)

Check if the cache has been loaded.

#### Returns

- `bool` - True if the cache has been loaded, False otherwise.

#### Examples

```python
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
```

#### Signature

```python
@property
def loaded(self) -> bool: ...
```

### MemoryCache().set

[Show source in cache.py:135](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L135)

Set the cached data manually.

#### Arguments

- [MemoryCache().data](#memorycachedata) *Any* - The data to be cached.

#### Examples

```python
>>> cache = MemoryCache()
>>> cache.set({"data": "new_value"})
>>> cache.data
{'data': 'new_value'}
```

#### Signature

```python
def set(self, data: Any) -> None: ...
```



## TimeoutCache

[Show source in cache.py:211](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L211)

A simple in-memory cache with timeout support.

#### Arguments

- [Data](../data/index.md#data) *Any, optional* - Initial data to populate the cache.
    Defaults to None.
loader (CacheLoader | None, optional): A callable that loads the data to be cached.
    If not provided, it defaults to a function that returns None. Defaults to None.
transformer (CacheTransformer | None, optional): A callable that transforms the cached data.
    If not provided, it defaults to a function that returns the data unchanged.
    Defaults to None.
- `cache_timeout` *float, optional* - The cache timeout in seconds.
    Defaults to 3600 seconds (1 hour).

#### Examples

```python
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
```

#### Signature

```python
class TimeoutCache(MemoryCache):
    def __init__(
        self,
        data: Any = None,
        loader: CacheLoader | None = None,
        transformer: CacheTransformer | None = None,
        cache_timeout: float = DEFAULT_CACHE_TIMEOUT,
    ) -> None: ...
```

#### See also

- [MemoryCache](#memorycache)

### TimeoutCache().age

[Show source in cache.py:306](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L306)

Get the age of the cache in seconds.

#### Returns

- `float` - The age of the cache in seconds.

#### Examples

```python
>>> def loader():
...     return {"data": "value"}
...
>>> cache = TimeoutCache(loader=loader, cache_timeout=10.0)
>>> cache.load()
{'data': 'value'}
>>> age = cache.age
>>> 0 <= age < 0.1
True
```

#### Signature

```python
@property
def age(self) -> float: ...
```

### TimeoutCache().expired

[Show source in cache.py:326](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L326)

Check if the cache has expired.

#### Returns

- `bool` - True if the cache has expired, False otherwise.

#### Examples

```python
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
```

#### Signature

```python
@property
def expired(self) -> bool: ...
```

### TimeoutCache().timeout

[Show source in cache.py:278](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L278)

Get the cache timeout in seconds.

#### Returns

- `float` - The cache timeout in seconds.

#### Examples

```python
>>> def loader():
...     return {"data": "value"}
...
>>> cache = TimeoutCache(loader=loader, cache_timeout=10)
>>> cache.timeout
10.0
```

#### Signature

```python
@property
def timeout(self) -> float: ...
```

### TimeoutCache().timeout

[Show source in cache.py:295](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/cache.py#L295)

Set the cache timeout in seconds.

#### Arguments

- `value` *float* - The new cache timeout in seconds.

#### Signature

```python
@timeout.setter
def timeout(self, value: float) -> None: ...
```