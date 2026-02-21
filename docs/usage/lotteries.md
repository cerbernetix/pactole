[Pactole](../../README.md) / [Documentation](../README.md) / [Usage](./README.md)

# Lottery Classes

Pactole exposes lottery-handling classes in `pactole.lottery`:

- `BaseLottery`: Generic implementation for draw-day handling, combination creation, and history search.
- `EuroMillions`: Preconfigured lottery (`Tuesday`, `Friday`) using `EuroMillionsCombination`.
- `EuroDreams`: Preconfigured lottery (`Monday`, `Thursday`) using `EuroDreamsCombination`.

## Create a lottery instance

Use built-in classes when your game rules match EuroMillions or EuroDreams.

```python
from pactole import EuroDreams, EuroMillions

euromillions = EuroMillions()
eurodreams = EuroDreams()

print(euromillions.draw_days.days)
print(eurodreams.draw_days.days)
```

## Get last and next draw dates

Lottery instances delegate date computations to configured draw days.

```python
from datetime import date

from pactole import EuroMillions

lottery = EuroMillions()

print(lottery.get_last_draw_date(from_date=date(2026, 2, 19), closest=True))
print(lottery.get_next_draw_date(from_date=date(2026, 2, 19), closest=True))
```

## Create and generate combinations from a lottery

Use the same API through the lottery class instead of calling combination classes directly.

```python
from pactole import EuroMillions

lottery = EuroMillions()

played = lottery.get_combination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
random_tickets = lottery.generate(n=3)

print(played)
print(random_tickets)
```

## Work with historical draw records

Lottery classes expose helper methods backed by their configured provider.

```python
from pactole import EuroMillions

lottery = EuroMillions()
ticket = lottery.get_combination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])

print(lottery.count())
print(lottery.dump(force=False)[:1])

records = list(lottery.get_records())
matches = list(lottery.find_records(ticket, strict=False))

print(len(records))
print(matches[:3])
```

## Build your own lottery class

Subclass `BaseLottery` by passing a configured provider to `super().__init__`.

```python
from pactole.combinations import EuroMillionsCombination
from pactole.data.providers import FDJProvider
from pactole.lottery import BaseLottery


class CustomLottery(BaseLottery):
    def __init__(self) -> None:
        super().__init__(
            provider=FDJProvider(
                "euromillions-my-million",
                draw_days=["MONDAY", "THURSDAY"],
                combination_factory=EuroMillionsCombination,
                cache_name="custom_lottery",
            )
        )
```

## Configure built-in lotteries with environment variables

`EuroMillions` and `EuroDreams` can be customized without subclassing.

- `EUROMILLIONS_PROVIDER_CLASS`, `EURODREAMS_PROVIDER_CLASS`
- `EUROMILLIONS_DRAW_DAYS`, `EURODREAMS_DRAW_DAYS`
- `EUROMILLIONS_DRAW_DAY_REFRESH_TIME`, `EURODREAMS_DRAW_DAY_REFRESH_TIME`
- `EUROMILLIONS_CACHE_NAME`, `EURODREAMS_CACHE_NAME`
- `EUROMILLIONS_ARCHIVES_PAGE`, `EURODREAMS_ARCHIVES_PAGE`
