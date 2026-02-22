# BaseProvider

[Pactole Index](../README.md#pactole-index) / [Data](./index.md#data) / BaseProvider

> Auto-generated documentation for [data.base_provider](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py) module.

- [BaseProvider](#baseprovider)
  - [BaseProvider](#baseprovider-1)
    - [BaseProvider()._build_cache](#baseprovider()_build_cache)
    - [BaseProvider()._check_archive_chain](#baseprovider()_check_archive_chain)
    - [BaseProvider()._check_archives](#baseprovider()_check_archives)
    - [BaseProvider()._check_last_archive](#baseprovider()_check_last_archive)
    - [BaseProvider()._get_archive_path](#baseprovider()_get_archive_path)
    - [BaseProvider()._get_source_path](#baseprovider()_get_source_path)
    - [BaseProvider()._load_manifest](#baseprovider()_load_manifest)
    - [BaseProvider()._load_record](#baseprovider()_load_record)
    - [BaseProvider()._load_record_list](#baseprovider()_load_record_list)
    - [BaseProvider()._load_source](#baseprovider()_load_source)
    - [BaseProvider()._need_refresh](#baseprovider()_need_refresh)
    - [BaseProvider()._parse_archive](#baseprovider()_parse_archive)
    - [BaseProvider()._parse_source](#baseprovider()_parse_source)
    - [BaseProvider()._refresh_archive](#baseprovider()_refresh_archive)
    - [BaseProvider()._refresh_if_needed](#baseprovider()_refresh_if_needed)
    - [BaseProvider().combination_factory](#baseprovider()combination_factory)
    - [BaseProvider().draw_day_refresh_time](#baseprovider()draw_day_refresh_time)
    - [BaseProvider().draw_days](#baseprovider()draw_days)
    - [BaseProvider().load](#baseprovider()load)
    - [BaseProvider().load_raw](#baseprovider()load_raw)
    - [BaseProvider().refresh](#baseprovider()refresh)

## BaseProvider

[Show source in base_provider.py:30](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L30)

A base class for data providers.

#### Arguments

- `resolver` *BaseResolver* - An instance of a resolver to fetch archive information.
- `parser` *BaseParser* - An instance of a parser to process the archive content.
draw_days (DrawDays | Iterable[Day | Weekday], optional): An instance of DrawDays or an
    iterable of Day or Weekday representing the draw days of the lottery.
    Defaults to an empty tuple.
draw_day_refresh_time (str | int | datetime.time, optional): The refresh threshold time on
    draw days. It can be provided as a string in "HH:MM" format, an integer representing
    the hour, or a datetime.time object. Defaults to None, which will be interpreted as
    22:00 (10 PM).
combination_factory (CombinationFactory | LotteryCombination | Any): A factory function
    or class to create a combination instance. If None, a default LotteryCombination
    instance will be used. Default is None.
- `cache_name` *str, optional* - The name of the cache. Defaults to "default".
- `refresh_timeout` *int, optional* - The timeout in seconds for refreshing the cache. Defaults
    to 300 seconds (5 minutes).

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser()
...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
...     draw_day_refresh_time="21:30",
...     combination_factory=EuroMillionsCombination,
...     cache_name="euromillions",
...     refresh_timeout=300,
... )
>>> provider.load()
[DrawRecord(
    period='202001',
    draw_date=date(2020, 1, 1),
    deadline_date=date(2020, 1, 15),
    combination=EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9]),
    numbers={'number': [5, 12, 23, 34, 45], 'star': [2, 9]},
    winning_ranks=[WinningRank(rank=1, winners=1, gain=1000000.0), ...]
), ...]
```

#### Signature

```python
class BaseProvider:
    def __init__(
        self,
        resolver: BaseResolver,
        parser: BaseParser,
        draw_days: DrawDays | Iterable[Day | Weekday] = (),
        draw_day_refresh_time: str | int | datetime.time | None = None,
        combination_factory: CombinationFactory | LotteryCombination | Any = None,
        cache_name: str = DEFAULT_CACHE_NAME,
        refresh_timeout: int = DEFAULT_REFRESH_TIMEOUT,
    ) -> None: ...
```

### BaseProvider()._build_cache

[Show source in base_provider.py:416](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L416)

Build the data file from the manifest of archives.

#### Signature

```python
def _build_cache(self, manifest: Manifest) -> None: ...
```

### BaseProvider()._check_archive_chain

[Show source in base_provider.py:376](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L376)

Check the chain of archives to ensure there are no gaps in the data.

#### Signature

```python
def _check_archive_chain(self, manifest: Manifest) -> bool: ...
```

### BaseProvider()._check_archives

[Show source in base_provider.py:356](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L356)

Check the list of archives match the list of archives from the resolver.

#### Signature

```python
def _check_archives(self, manifest: Manifest) -> bool: ...
```

### BaseProvider()._check_last_archive

[Show source in base_provider.py:395](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L395)

Check the last archive to ensure it is up to date with the latest draw date.

#### Signature

```python
def _check_last_archive(self, manifest: Manifest) -> bool: ...
```

### BaseProvider()._get_archive_path

[Show source in base_provider.py:445](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L445)

Get the file path for the archive file of a given archive name.

#### Signature

```python
def _get_archive_path(self, name: str) -> Path: ...
```

### BaseProvider()._get_source_path

[Show source in base_provider.py:441](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L441)

Get the file path for the source file of a given archive name.

#### Signature

```python
def _get_source_path(self, name: str) -> Path: ...
```

### BaseProvider()._load_manifest

[Show source in base_provider.py:330](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L330)

Load the manifest of archives.

#### Signature

```python
def _load_manifest(self, force: bool) -> Manifest: ...
```

### BaseProvider()._load_record

[Show source in base_provider.py:431](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L431)

Load a DrawRecord instance from a dictionary of data.

#### Signature

```python
def _load_record(self, data: dict) -> DrawRecord: ...
```

### BaseProvider()._load_record_list

[Show source in base_provider.py:435](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L435)

Load a list of DrawRecord instances from a list of dictionaries.

#### Signature

```python
def _load_record_list(self, data: list[dict] | None) -> list[DrawRecord]: ...
```

### BaseProvider()._load_source

[Show source in base_provider.py:449](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L449)

Load the archive content from the given URL and store it in the specified path.

#### Signature

```python
def _load_source(self, url: str, path: Path) -> None: ...
```

### BaseProvider()._need_refresh

[Show source in base_provider.py:312](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L312)

Check if the cache needs to be refreshed based on the last draw date.

#### Signature

```python
def _need_refresh(self) -> bool: ...
```

### BaseProvider()._parse_archive

[Show source in base_provider.py:464](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L464)

Parse the archive file and extract relevant information.

#### Signature

```python
def _parse_archive(self, archive: Path) -> ArchiveContentInfo: ...
```

### BaseProvider()._parse_source

[Show source in base_provider.py:460](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L460)

Parse the source file and store the results in the archive path.

#### Signature

```python
def _parse_source(self, source: Path, archive: Path) -> None: ...
```

### BaseProvider()._refresh_archive

[Show source in base_provider.py:337](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L337)

Refresh a specific archive.

#### Signature

```python
def _refresh_archive(self, name: str, url: str, force: bool = False) -> ArchiveInfo: ...
```

### BaseProvider()._refresh_if_needed

[Show source in base_provider.py:307](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L307)

Refresh the provider's cache if necessary.

#### Signature

```python
def _refresh_if_needed(self, force: bool = False) -> None: ...
```

### BaseProvider().combination_factory

[Show source in base_provider.py:167](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L167)

Return the combination factory used by the provider.

#### Returns

- `CombinationFactory` - The combination factory used by the provider.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
...     combination_factory=EuroMillionsCombination,
... )
>>> provider.combination_factory
<class 'pactole.combinations.euro_millions.EuroMillionsCombination'>
>>> provider.combination_factory()
EuroMillionsCombination(numbers=[], stars=[])
```

#### Signature

```python
@property
def combination_factory(self) -> CombinationFactory: ...
```

### BaseProvider().draw_day_refresh_time

[Show source in base_provider.py:149](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L149)

Return the refresh threshold time used on draw days.

#### Returns

- `datetime.time` - The refresh threshold time used on draw days.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_day_refresh_time="21:30",
... )
>>> provider.draw_day_refresh_time
datetime.time(21, 30)
```

#### Signature

```python
@property
def draw_day_refresh_time(self) -> datetime.time: ...
```

### BaseProvider().draw_days

[Show source in base_provider.py:125](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L125)

Return the draw days of the lottery.

#### Returns

- `DrawDays` - The draw days of the lottery.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
... )
>>> provider.draw_days
DrawDays(days=(Weekday.MONDAY, Weekday.THURSDAY))
>>> provider.draw_days.days
(Weekday.MONDAY, Weekday.THURSDAY)
>>> provider.draw_days.get_last_draw_date(date(2024, 6, 5))
datetime.date(2024, 6, 3)
>>> provider.draw_days.get_next_draw_date(date(2024, 6, 5))
datetime.date(2024, 6, 6)
```

#### Signature

```python
@property
def draw_days(self) -> DrawDays: ...
```

### BaseProvider().load

[Show source in base_provider.py:188](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L188)

Get the cached data as a list of DrawRecord instances.

If the cache is missing or outdated, it will be refreshed before returning the data.

#### Arguments

- `force` *bool, optional* - If True, forces a refresh of the cache before getting the data.
    Defaults to False.

#### Returns

- `list[DrawRecord]` - A list of DrawRecord instances representing the cached data.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
...     combination_factory=EuroMillionsCombination,
...     cache_name="euromillions"
... )
>>> provider.load()
[DrawRecord(
    period='202001',
    draw_date=date(2020, 1, 1),
    deadline_date=date(2020, 1, 15),
    combination=EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9]),
    numbers={'number': [5, 12, 23, 34, 45], 'star': [2, 9]},
    winning_ranks=[WinningRank(rank=1, winners=1, gain=1000000.0), ...]
), ...]
```

#### Signature

```python
def load(self, force: bool = False) -> list[DrawRecord]: ...
```

### BaseProvider().load_raw

[Show source in base_provider.py:221](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L221)

Get the cached data as a list of dictionaries.

If the cache is missing or outdated, it will be refreshed before returning the data.

The returned list of dictionaries will have the same structure as the data stored in
the cache file, without being transformed into DrawRecord instances. This can be useful
for debugging or for scenarios where raw data manipulation is required, like exporting
to Pandas DataFrame or performing custom analyses.

#### Arguments

- `force` *bool, optional* - If True, forces a refresh of the cache before getting the data.
    Defaults to False.

#### Returns

- `list[dict]` - A list of dictionaries representing the cached data.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
...     combination_factory=EuroMillionsCombination,
...     cache_name="euromillions"
... )
>>> provider.load_raw()
[
    {
        'period': '202001',
        'draw_date': '2020-01-01',
        'deadline_date': '2020-01-15',
        'numbers_1': '5',
        'numbers_2': '12',
        'numbers_3': '23',
        'numbers_4': '34',
        'numbers_5': '45',
        'stars_1': '2',
        'stars_2': '9',
        ...
    },
    ...
]
```

#### Signature

```python
def load_raw(self, force: bool = False) -> list[dict]: ...
```

### BaseProvider().refresh

[Show source in base_provider.py:267](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_provider.py#L267)

Refresh the provider's cache.

If force is True, it will refresh the cache even if it is still valid. Otherwise, it will
check the manifest of archives and refresh it if necessary.

The data file will be rebuilt if missing or if the manifest was refreshed.

#### Arguments

- `force` *bool, optional* - If True, forces a refresh even if the cache is still valid.
    Defaults to False.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
...     combination_factory=EuroMillionsCombination,
...     cache_name="euromillions"
... )
>>> provider.refresh()
```

#### Signature

```python
def refresh(self, force: bool = False) -> None: ...
```