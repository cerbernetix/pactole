# Fdj

[Pactole Index](../../README.md#pactole-index) / [Data](../index.md#data) / [Providers](./index.md#providers) / Fdj

> Auto-generated documentation for [data.providers.fdj](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/providers/fdj.py) module.

- [Fdj](#fdj)
  - [FDJParser](#fdjparser)
    - [FDJParser()._format_date](#fdjparser()_format_date)
  - [FDJProvider](#fdjprovider)
  - [FDJResolver](#fdjresolver)
    - [FDJResolver.get_archives_page_url](#fdjresolverget_archives_page_url)

## FDJParser

[Show source in fdj.py:101](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/providers/fdj.py#L101)

Parser for FDJ archives.

#### Arguments

combination_factory (CombinationFactory | None): A factory function or class to create a
    combination instance. If None, a default LotteryCombination instance will be used.
    Default is None.

#### Examples

```python
>>> parser = FDJParser()
>>> data = {
...     "date_de_tirage": "01/02/2022",
...     "date_de_forclusion": "15/02/2022",
...     "nombre_de_gagnant_au_rang1_en_europe": "2",
...     "rapport_du_rang1": "1000000,00",
...     "boule_1": "1",
...     "boule_2": "2",
...     "boule_3": "3",
...     "boule_4": "4",
...     "boule_5": "5",
...     "etoile_1": "1",
...     "etoile_2": "2",
... }
>>> parsed = parser(data)
>>> parsed
{
    "draw_date": "2022-02-01",
    "deadline_date": "2022-02-15",
    "winning_rank_1_winners": 2,
    "winning_rank_1_gain": 1000000.00,
    "number_1": 1,
    "number_2": 2,
    "number_3": 3,
    "number_4": 4,
    "number_5": 5,
    "star_1": 1,
    "star_2": 2,
}
```

#### Signature

```python
class FDJParser(BaseParser): ...
```

### FDJParser()._format_date

[Show source in fdj.py:213](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/providers/fdj.py#L213)

Format a date string into ISO format (YYYY-MM-DD).

The method checks the format of the input date string and converts it to ISO format.
It supports various date formats, including:
- RFC format (YYYY-MM-DD) and RFC-like format (YYYYMMDD)
- French format (DD/MM/YYYY), including cases where the year is presented in 2-digit format,
    (e.g., DD/MM/YY)

#### Signature

```python
def _format_date(self, value: str) -> str: ...
```



## FDJProvider

[Show source in fdj.py:244](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/providers/fdj.py#L244)

Data provider for FDJ archives.

Environment Variables:
    FDJ_ARCHIVES_PAGE_URL (str): The URL template for the archives page, which must include the
        placeholder '{name}' for the lottery name.
        Defaults to "https://www.fdj.fr/jeux-de-tirage/{name}/historique".
    PACTOLE_CACHE_ROOT (str): The root directory for cache files.
        Defaults to "pactole".

#### Arguments

resolver (BaseResolver | str): An instance of BaseResolver or the URL of the archives page.
    If a string is provided, a default FDJResolver will be used with the given URL.
parser (BaseParser | None): An instance of a parser to process the archive content. If None,
    a default FDJParser will be used. Defaults to None.
draw_days (DrawDays | Iterable[Weekday], optional): An instance of DrawDays or an iterable
    of Weekday representing the draw days of the lottery. Defaults to an empty tuple.
draw_day_refresh_time (str | int | datetime.time, optional): Refresh threshold time used on
    draw days. It can be provided as a string in "HH:MM" format, an integer representing
    the hour, or a datetime.time object. Defaults to None, which will be interpreted as
    22:00 (10 PM).
combination_factory (CombinationFactory | None): A factory function or class to create a
    combination instance. If None, a default LotteryCombination instance will be used.
    Default is None.
- `cache_name` *str, optional* - The name of the cache. Defaults to "fdj".

#### Examples

```python
>>> provider = FDJProvider("https://www.fdj.fr/...")
>>> provider.refresh()
```

#### Signature

```python
class FDJProvider(BaseProvider):
    def __init__(
        self,
        resolver: BaseResolver | str,
        parser: BaseParser | None = None,
        draw_days: DrawDays | Iterable[Weekday] = (),
        draw_day_refresh_time: str | int | datetime.time | None = None,
        combination_factory: CombinationFactory | None = None,
        cache_name: str = DEFAULT_CACHE_NAME,
    ) -> None: ...
```



## FDJResolver

[Show source in fdj.py:23](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/providers/fdj.py#L23)

Resolver for FDJ EuroMillions archives.

Environment Variables:
    FDJ_ARCHIVES_PAGE_URL (str): The URL template for the archives page, which must include the
        placeholder '{name}' for the lottery name.
        Defaults to "https://www.fdj.fr/jeux-de-tirage/{name}/historique".

#### Arguments

- `archives_page_url` *str* - The URL of the archives page. This can be a full URL or a lottery
    name that will be used to construct the URL based on a template.
- `cache_timeout` *int, optional* - Time to live for the cache in seconds.
    Defaults to TimeoutCache.DEFAULT_CACHE_TIMEOUT.

#### Examples

```python
>>> resolver = FDJResolver("https://www.fdj.fr/...", cache_timeout=600)
>>> resolver.load()
{'euromillions_202202': 'https://www.fdj.fr/...', ...}
>>> resolver = FDJResolver("euromillions-my-million", cache_timeout=600)
>>> resolver.load()
{'euromillions_202202': 'https://www.fdj.fr/...', ...}
```

#### Signature

```python
class FDJResolver(BaseResolver):
    def __init__(
        self,
        archives_page_url: str,
        cache_timeout: int = TimeoutCache.DEFAULT_CACHE_TIMEOUT,
    ) -> None: ...
```

### FDJResolver.get_archives_page_url

[Show source in fdj.py:66](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/providers/fdj.py#L66)

Get the URL of the archives page for a given lottery name.

This method constructs the URL of the archives page for a specific lottery based on a
template URL. The template URL can be defined as the class variable ARCHIVES_PAGE_URL
or overridden by the environment variable FDJ_ARCHIVES_PAGE_URL. The method ensures that
the template URL contains the required placeholder for the lottery name and formats the URL
accordingly.

#### Arguments

- `name` *str* - The name of the lottery (e.g., "euromillions-my-million", "eurodreams").

#### Returns

- `str` - The URL of the archives page for the specified lottery.

#### Raises

- `ValueError` - If the URL template does not contain the required placeholder for the
    lottery name.

#### Examples

```python
>>> FDJResolver.get_archives_page_url("euromillions-my-million")
'https://www.fdj.fr/jeux-de-tirage/euromillions-my-million/historique'
>>> FDJResolver.get_archives_page_url("eurodreams")
'https://www.fdj.fr/jeux-de-tirage/eurodreams/historique'
```

#### Signature

```python
@classmethod
def get_archives_page_url(cls, name: str) -> str: ...
```