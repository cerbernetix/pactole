# EuroDreams

[Pactole Index](../README.md#pactole-index) / [Lottery](./index.md#lottery) / EuroDreams

> Auto-generated documentation for [lottery.eurodreams](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/eurodreams.py) module.

- [EuroDreams](#eurodreams)
  - [EuroDreams](#eurodreams-1)

## EuroDreams

[Show source in eurodreams.py:11](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/eurodreams.py#L11)

Class representing the EuroDreams lottery.

EuroDreams is a lottery game where players choose 6 main numbers from 1 to 40 and
1 dream number from 1 to 5. The total number of combinations is 3,838,380 for the main numbers
and 5 for the dream numbers. In total, there are 19,191,900 possible combinations.

Draws take place every Monday and Thursday.

Environment Variables:
    EURODREAMS_PROVIDER_CLASS (str): The fully qualified class name of the provider to use.
        Defaults to "pactole.data.providers.fdj.FDJProvider".
    EURODREAMS_DRAW_DAYS (str): Comma-separated list of draw days.
        Defaults to "MONDAY,THURSDAY".
    EURODREAMS_DRAW_DAY_REFRESH_TIME (str): Refresh threshold time in "HH:MM" format.
        Defaults to "22:00".
    EURODREAMS_CACHE_NAME (str): The name of the cache to use.
        Defaults to "eurodreams".
    EURODREAMS_ARCHIVES_PAGE (str): The name of the archives page to use.
        Defaults to "eurodreams".
    FDJ_ARCHIVES_PAGE_URL (str): The URL template for the archives page, which must include the
        placeholder '{name}' for the lottery name.
        Defaults to "https://www.fdj.fr/jeux-de-tirage/{name}/historique".
    PACTOLE_CACHE_ROOT (str): The root directory for cache files.
        Defaults to "pactole".

#### Arguments

- `provider` *BaseProvider, optional* - The data provider to use. If None, a default provider
    will be created using environment variables or defaults. Defaults to None.

#### Raises

- `ValueError` - If the provider class is not in the correct format.
- `ImportError` - If the provider cannot be imported.
- `AttributeError` - If the provider does not exist in the module.

#### Examples

```python
>>> lottery = EuroDreams()
>>> lottery.load()
[DrawRecord(
    period="202002",
    draw_date=datetime.date(2024, 1, 1),
    combination=EuroDreamsCombination(numbers=[1, 2, 3, 4, 5],
    winning_ranks={(5, 0): 1}))]
```

#### Signature

```python
class EuroDreams(BaseLottery):
    def __init__(self, provider: BaseProvider | None = None) -> None: ...
```