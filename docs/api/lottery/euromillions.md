# EuroMillions

[Pactole Index](../README.md#pactole-index) / [Lottery](./index.md#lottery) / EuroMillions

> Auto-generated documentation for [lottery.euromillions](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/euromillions.py) module.

- [EuroMillions](#euromillions)
  - [EuroMillions](#euromillions-1)

## EuroMillions

[Show source in euromillions.py:11](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/euromillions.py#L11)

Class representing the EuroMillions lottery.

EuroMillions is a lottery game where players choose 5 main numbers from 1 to 50 and
2 star numbers from 1 to 12. The total number of combinations is 2,118,760 for the main numbers
and 66 for the star numbers. In total, there are 139,838,160 possible combinations.

Draws take place every Tuesday and Friday.

Environment Variables:
    EUROMILLIONS_PROVIDER_CLASS (str): The fully qualified class name of the provider to use.
        Defaults to "pactole.data.providers.fdj.FDJProvider".
    EUROMILLIONS_DRAW_DAYS (str): Comma-separated list of draw days.
        Defaults to "TUESDAY,FRIDAY".
    EUROMILLIONS_DRAW_DAY_REFRESH_TIME (str): Refresh threshold time in "HH:MM" format.
        Defaults to "22:00".
    EUROMILLIONS_CACHE_NAME (str): The name of the cache to use.
        Defaults to "euromillions".
    EUROMILLIONS_ARCHIVES_PAGE (str): The name of the archives page to use.
        Defaults to "euromillions-my-million".

#### Arguments

- `provider` *BaseProvider, optional* - The data provider to use. If None, a default provider
    will be created using environment variables or defaults. Defaults to None.

#### Raises

- `ValueError` - If the provider class is not in the correct format.
- `ImportError` - If the provider cannot be imported.
- `AttributeError` - If the provider does not exist in the module.

#### Examples

```python
>>> lottery = EuroMillions()
>>> lottery.load()
[DrawRecord(
    period="202311",
    draw_date=datetime.date(2024, 1, 1),
    combination=EuroMillionsCombination(numbers=[1, 2, 3, 4, 5],
    winning_ranks={(5, 0): 1}))]
```

#### Signature

```python
class EuroMillions(BaseLottery):
    def __init__(self, provider: BaseProvider | None = None) -> None: ...
```