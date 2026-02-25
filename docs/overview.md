[Documentation](./README.md)

# Pactole Library Overview

Pactole is a Python library that fetches, caches, and queries lottery draw results. It models
lottery combinations, draws, and winning ranks, and provides helpers to search historical
records by combination or by winning rank.

## Core concepts

- Lottery classes: `EuroMillions` and `EuroDreams` provide a ready-to-use interface.
- Providers: `BaseProvider` orchestrates fetching archives, parsing them, and caching results.
- Parsers and resolvers: `BaseParser` converts raw archive rows into `DrawRecord` instances;
  `BaseResolver` discovers archive URLs.
- Combinations: `LotteryCombination` and its subclasses model draw numbers and ranks.

## Quick start

```python
from pactole import EuroMillions

lottery = EuroMillions()

# Build a combination using the lottery factory.
played = lottery.get_combination(numbers=[5, 12, 23, 34, 45], stars=[2, 9])

# Get cached records (auto-refreshes if needed).
records = list(lottery.get_records())

# Find a specific combination in past draws.
matches = list(lottery.find_records(played))

# Inspect cache-backed history helpers.
total_draws = lottery.count()
sample = lottery.dump()[:1]

# Compute draw dates
last_draw = lottery.get_last_draw_date()
next_draw = lottery.get_next_draw_date()

# Generate random combinations with the same game rules.
random_tickets = lottery.generate(n=3)
```

See detailed usage guides:

- [Combinations](./usage/combinations.md)
- [Lottery classes](./usage/lotteries.md)

## Provider customization

If you want to pull data from a different source, implement a resolver and parser:

```python
from pactole.data import BaseParser, BaseProvider, BaseResolver, DrawRecord
from pactole.combinations import EuroMillionsCombination
from pactole.lottery import BaseLottery
from pactole.utils import Weekday

class MyResolver(BaseResolver):
    def _load_cache(self) -> dict[str, str]:
        return {"archive.csv": "https://local.test/archives/evm.csv"}

class MyParser(BaseParser):
    def __call__(self, data: dict) -> DrawRecord:
        # Convert raw fields to a DrawRecord
        raise NotImplementedError

provider = BaseProvider(
    resolver=MyResolver(),
    parser=MyParser(),
    draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
    combination_factory=EuroMillionsCombination,
    cache_name="euromillions-custom",
)

lottery = BaseLottery(provider)
records = list(lottery.get_records())
```

## Caching behavior

- Archives are downloaded and parsed into cached CSV files under the OS cache directory.
- The cache is refreshed when a new draw is expected or when `force=True` is used.

## Environment variables

Defaults can be overridden for built-in lotteries:

- `PACTOLE_CACHE_ROOT`
- `EUROMILLIONS_PROVIDER_CLASS`
- `EUROMILLIONS_DRAW_DAYS`
- `EUROMILLIONS_DRAW_DAY_REFRESH_TIME`
- `EUROMILLIONS_CACHE_NAME`
- `EUROMILLIONS_ARCHIVES_PAGE`
- `EURODREAMS_PROVIDER_CLASS`
- `EURODREAMS_DRAW_DAYS`
- `EURODREAMS_DRAW_DAY_REFRESH_TIME`
- `EURODREAMS_CACHE_NAME`
- `EURODREAMS_ARCHIVES_PAGE`

## Notes

- This library focuses on draw history management and combination-based queries.
- For custom lotteries, plug in your own resolver/parser pair and combination class.
