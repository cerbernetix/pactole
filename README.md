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

### EuroMillions combinations

```python
from pactole import EuroMillionsCombination

# Build a known combination
euro_millions = EuroMillionsCombination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])

print(euro_millions.numbers.values)
print(euro_millions.stars.values)
print(euro_millions.rank)

# Generate 3 random combinations
combinations = EuroMillionsCombination().generate(3)
print(combinations)
```

### EuroDreams combinations

```python
from pactole import EuroDreamsCombination

# Build a known combination
euro_dreams = EuroDreamsCombination(numbers=[2, 3, 5, 7, 9, 38], dream=[3])

print(euro_dreams.numbers.values)
print(euro_dreams.dream.values)
print(euro_dreams.rank)

# Generate 3 random combinations
combinations = EuroDreamsCombination().generate(3)
print(combinations)
```

## License

Copyright (c) 2026 Jean-Sébastien CONAN

Distributed under the MIT License.
