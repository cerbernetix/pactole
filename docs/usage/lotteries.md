[Pactole](../../README.md) / [Documentation](../README.md) / [Usage](./README.md)

# Lottery Classes

Pactole exposes lottery-handling classes in `pactole.lottery`:

- `BaseLottery`: Generic implementation for draw-day handling and combination creation.
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

## Build your own lottery class

Subclass `BaseLottery` to define custom draw days and your own combination class.

```python
from pactole.combinations import EuroMillionsCombination
from pactole.lottery import BaseLottery
from pactole.utils import Weekday


class CustomLottery(BaseLottery):
    def __init__(self) -> None:
        super().__init__(
            draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
            combination_factory=EuroMillionsCombination,
        )
```
