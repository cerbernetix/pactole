[Pactole](../../README.md) / [Documentation](../README.md) / [Usage](./README.md)

# Lottery Classes

Pactole exposes lottery-handling classes in `pactole.lottery`:

- `BaseLottery`: Generic implementation for draw-day handling, combination creation, and history search.
- `EuroMillions`: Preconfigured lottery (`Tuesday`, `Friday`) using `EuroMillionsCombination`.
- `EuroDreams`: Preconfigured lottery (`Monday`, `Thursday`) using `EuroDreamsCombination`.

In day-to-day usage, a lottery object is the main entry point to:

- Plan plays around next draw dates.
- Build valid game-specific combinations.
- Inspect cached historical draws.
- Search past results for winning ranks.

## Create lottery instances

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

This is typically used to decide if a ticket should be registered for the current draw
or for the next one.

```python
from datetime import date

from pactole import EuroMillions

lottery = EuroMillions()
today = date(2026, 2, 19)

print(lottery.get_last_draw_date(from_date=today, closest=True))
print(lottery.get_next_draw_date(from_date=today, closest=True))
```

## Create and generate tickets from a lottery

Use the lottery API to keep code generic, even if you later swap provider or game type.

```python
from pactole import EuroMillions

lottery = EuroMillions()

played = lottery.get_combination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
suggested = lottery.generate(n=3)
spread_suggested = lottery.generate(n=12, partitions=4)

print(played)
for ticket in suggested:
    print(ticket)

print(len(spread_suggested))
```

`partitions` lets you spread generated tickets across slices of the full combination
rank space. This is useful when generating larger batches.

## Work with historical draw records

Lottery classes expose helper methods backed by their configured provider.

`force=True` refreshes source data before reading.

```python
from pactole import EuroMillions

lottery = EuroMillions()
ticket = lottery.get_combination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])

print(lottery.count())

raw_rows = lottery.dump(force=False)
print(raw_rows[:1])

records = list(lottery.get_records())
matches = list(lottery.find_records(ticket, strict=False))

print(len(records))
for found in matches[:3]:
    print(found.record.draw_date, found.rank)
```

### Build a Pandas DataFrame from raw export

Use `dump()` when you want tabular analysis (filtering, grouping, charts, exports).

```python
import pandas as pd

from pactole import EuroMillions

lottery = EuroMillions()
raw_rows = lottery.dump(force=False)

df = pd.DataFrame(raw_rows)
df["draw_date"] = pd.to_datetime(df["draw_date"])

print(df.shape)
print(df[["draw_date", "numbers_1", "numbers_2", "stars_1", "stars_2"]].head())

# Example: average rank-1 gain by year
df["year"] = df["draw_date"].dt.year
avg_rank1_gain = df.groupby("year", as_index=False)["rank_1_gain"].mean()
print(avg_rank1_gain.tail())
```

## Search with rank constraints

Use `target_rank` to filter matches by prize category and `strict` to control matching behavior.

- `strict=False`: return matches whose rank is equal to or better than `target_rank`.
- `strict=True`: return matches with exactly `target_rank`.

```python
from pactole import EuroMillions

lottery = EuroMillions()
ticket = lottery.get_combination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])

at_least_rank_4 = list(lottery.find_records(ticket, target_rank=4, strict=False))
exactly_rank_4 = list(lottery.find_records(ticket, target_rank=4, strict=True))

print(len(at_least_rank_4), len(exactly_rank_4))
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

### Create a specific provider class first

For reusable setups, create a provider class dedicated to one source/game configuration,
then inject it into your lottery class.

```python
from pactole.combinations import EuroMillionsCombination
from pactole.data.providers import FDJProvider
from pactole.lottery import BaseLottery


class EuroMillionsFDJProvider(FDJProvider):
    def __init__(self) -> None:
        super().__init__(
            resolver="euromillions-my-million",
            draw_days=["TUESDAY", "FRIDAY"],
            draw_day_refresh_time="22:00",
            combination_factory=EuroMillionsCombination,
            cache_name="euromillions_fdj_custom",
        )


class EuroMillionsCustomLottery(BaseLottery):
    def __init__(self) -> None:
        super().__init__(provider=EuroMillionsFDJProvider())
```

### Create a fully custom provider from resolver + parser

If your archive source is not FDJ, create a provider by composing your own resolver and parser.

```python
from pactole.combinations import EuroMillionsCombination
from pactole.data import BaseParser, BaseProvider, BaseResolver, DrawRecord


class CustomResolver(BaseResolver):
    def _load_cache(self) -> dict[str, str]:
        return {
            "draws_2026.zip": "https://local.test/lottery/draws_2026.zip",
        }


class CustomParser(BaseParser):
    def __call__(self, data: dict) -> DrawRecord:
        # Parse one source row into a DrawRecord.
        # Implement mapping according to your data schema.
        ...


class CustomProvider(BaseProvider):
    def __init__(self) -> None:
        super().__init__(
            resolver=CustomResolver(),
            parser=CustomParser(combination_factory=EuroMillionsCombination),
            draw_days=["TUESDAY", "FRIDAY"],
            combination_factory=EuroMillionsCombination,
            cache_name="custom_provider",
        )
```

## Configure built-in lotteries with environment variables

`EuroMillions` and `EuroDreams` can be customized without subclassing.

- `EUROMILLIONS_PROVIDER_CLASS`, `EURODREAMS_PROVIDER_CLASS`
- `EUROMILLIONS_DRAW_DAYS`, `EURODREAMS_DRAW_DAYS`
- `EUROMILLIONS_DRAW_DAY_REFRESH_TIME`, `EURODREAMS_DRAW_DAY_REFRESH_TIME`
- `EUROMILLIONS_CACHE_NAME`, `EURODREAMS_CACHE_NAME`
- `EUROMILLIONS_ARCHIVES_PAGE`, `EURODREAMS_ARCHIVES_PAGE`

Example:

```bash
export EUROMILLIONS_DRAW_DAYS="MONDAY,THURSDAY"
export EUROMILLIONS_CACHE_NAME="euromillions_local"
```
