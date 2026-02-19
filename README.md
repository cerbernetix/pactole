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

See the complete documentation index: [Documentation](./docs/README.md).

## Requirements

Requires **`Python 3`** (version `3.10` or newer).

## Usage

```python
import pactole
```

### EuroMillions lottery

```python
from datetime import date

from pactole import EuroMillions

lottery = EuroMillions()

# Build a known ticket
ticket = lottery.get_combination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])

print(lottery.draw_days.days)
print(lottery.get_last_draw_date(from_date=date(2026, 2, 19)))
print(lottery.get_next_draw_date(from_date=date(2026, 2, 19)))
print(lottery.get_next_draw_date())  # From today
print(ticket.numbers.values)
print(ticket.stars.values)
print(ticket.rank)

# Generate 3 random combinations
combinations = lottery.generate(3)
print(combinations)
```

### EuroDreams lottery

```python
from datetime import date

from pactole import EuroDreams

lottery = EuroDreams()

# Build a known ticket
ticket = lottery.get_combination(numbers=[2, 3, 5, 7, 9, 38], dream=[3])

print(lottery.draw_days.days)
print(lottery.get_last_draw_date(from_date=date(2026, 2, 19)))
print(lottery.get_next_draw_date(from_date=date(2026, 2, 19)))
print(lottery.get_next_draw_date())  # From today
print(ticket.numbers.values)
print(ticket.dream.values)
print(ticket.rank)

# Generate 3 random combinations
combinations = lottery.generate(3)
print(combinations)
```

## License

Copyright (c) 2026 Jean-Sébastien CONAN

Distributed under the MIT License.
