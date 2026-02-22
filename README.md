# Pactole

A Python library for managing lottery results.

## Installation

Add `pactole` to your project:

```sh
pip install -U pactole
```

Or with `uv`:

```sh
uv add -U pactole
```

## Documentation

See the complete documentation index: [Documentation](https://cerbernetix.github.io/pactole/).

## Requirements

Requires **`Python 3`** (version `3.10` or newer).

## Usage

```python
import pactole
```

### What you can do with Pactole

With built-in lottery classes (`EuroMillions`, `EuroDreams`), you can:

- Compute last/next draw dates from any date.
- Build validated tickets from numbers or component ranks.
- Generate random ticket batches (`generate`) with optional rank-space partitioning.
- Query and export historical draws (`get_records`, `count`, `dump`).
- Search historical results for a ticket and filter by winning rank (`find_records`).

### EuroMillions: plan, generate, and analyze

```python
from datetime import date

from pactole import EuroMillions

lottery = EuroMillions()
today = date(2026, 2, 19)

# 1) Plan around draw days
print(lottery.draw_days.days)
print(lottery.get_last_draw_date(from_date=today))
print(lottery.get_next_draw_date(from_date=today))

# 2) Build a ticket from user input
ticket = lottery.get_combination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
print(ticket.numbers.values, ticket.stars.values, ticket.rank)

# 3) Generate candidate tickets for the next draw
# partitions spreads picks across slices of the full rank space
suggested = lottery.generate(n=6, partitions=3)
for candidate in suggested:
    print(candidate)

# 4) Inspect history and evaluate your ticket
total_records = lottery.count()
records = list(lottery.get_records())
matches = list(lottery.find_records(ticket))

print(total_records, len(records), len(matches))

# Optional: keep only rank 4 (strict) or better than/equal to rank 4 (non-strict)
exact_rank_4 = list(lottery.find_records(ticket, target_rank=4, strict=True))
at_least_rank_4 = list(lottery.find_records(ticket, target_rank=4, strict=False))
print(len(exact_rank_4), len(at_least_rank_4))
```

### EuroDreams: same workflow, different components

```python
from datetime import date

from pactole import EuroDreams

lottery = EuroDreams()
today = date(2026, 2, 19)

# Draw planning
print(lottery.get_last_draw_date(from_date=today))
print(lottery.get_next_draw_date(from_date=today))

# Ticket creation (numbers + dream)
ticket = lottery.get_combination(numbers=[2, 3, 5, 7, 9, 38], dream=[3])
print(ticket.numbers.values, ticket.dream.values, ticket.rank)

# Ticket suggestions
combinations = lottery.generate(n=3)
print(combinations)

# History lookup for this ticket
records = list(lottery.get_records())
matches = list(lottery.find_records(ticket))
print(len(records), len(matches))
```

### Useful API methods at a glance

- `get_last_draw_date(from_date=...)` / `get_next_draw_date(from_date=...)`: draw-day planning.
- `get_combination(...)`: build a validated game-specific ticket.
- `generate(n=..., partitions=...)`: create random tickets.
- `count()`: total number of cached draw records.
- `get_records(force=False)`: iterate over structured `DrawRecord` objects.
- `dump(force=False)`: export raw dictionary rows (ready for tools like Pandas).
- `find_records(..., target_rank=..., strict=...)`: search matches in history.

See detailed usage guides:

- [Combinations](https://cerbernetix.github.io/pactole/usage/combinations/)
- [Lottery classes](https://cerbernetix.github.io/pactole/usage/lotteries/)

## License

MIT License - See LICENSE file for details.
