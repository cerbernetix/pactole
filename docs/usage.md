[Pactole](../README.md) / [Documentation](./README.md)

# Combinations Usage

Pactole exposes dedicated classes to represent and manipulate lottery combinations:

- `EuroMillionsCombination`
- `EuroDreamsCombination`

## Create combinations

Create combinations from explicit component values.

```python
from pactole import EuroDreamsCombination, EuroMillionsCombination

euromillions = EuroMillionsCombination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
eurodreams = EuroDreamsCombination(numbers=[2, 3, 5, 7, 9, 38], dream=[3])
```

You can also pass a flat sequence. Values are split automatically by component size.

```python
from pactole import EuroDreamsCombination, EuroMillionsCombination

euromillions = EuroMillionsCombination([3, 15, 22, 28, 44, 2, 9])
eurodreams = EuroDreamsCombination([2, 3, 5, 7, 9, 38, 3])
```

Create combinations from lexicographic rank values (per component).

```python
from pactole import EuroDreamsCombination, EuroMillionsCombination

first_euromillions = EuroMillionsCombination(numbers=0, stars=0)
first_eurodreams = EuroDreamsCombination(numbers=0, dream=0)
```

## Read normalized values and metadata

Each combination exposes normalized component values and computed metadata.

```python
from pactole import EuroMillionsCombination

combination = EuroMillionsCombination(numbers=[44, 3, 28, 22, 15], stars=[9, 2])

print(combination.numbers.values)       # [3, 15, 22, 28, 44]
print(combination.stars.values)         # [2, 9]
print(combination.values)               # Combined values from all components
print(combination.rank)                 # Global lexicographic rank
print(combination.combinations)         # Total number of possible combinations
print(combination.min_winning_rank)     # Best rank value
print(combination.max_winning_rank)     # Worst winning rank value
```

## Generate random combinations

Use `generate(n)` to produce combinations with the same game rules.

```python
from pactole import EuroDreamsCombination

template = EuroDreamsCombination()
generated = template.generate(3)

for combination in generated:
    print(combination)
```

## Compare combinations

The classes provide direct comparison and set-like operations.

```python
from pactole import EuroMillionsCombination

reference = EuroMillionsCombination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
candidate = EuroMillionsCombination(numbers=[3, 15, 22, 30, 45], stars=[2, 10])

print(reference.equals(candidate))
print(reference.includes(numbers=[3, 15, 22], stars=[2]))
print(reference.intersects(candidate))
print(reference.intersection(candidate).numbers.values)
```

## Compute winning ranks

Evaluate a played combination against a reference draw combination with `get_winning_rank`.

```python
from pactole import EuroMillionsCombination

draw = EuroMillionsCombination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
ticket = EuroMillionsCombination(numbers=[3, 15, 22, 30, 45], stars=[2, 10])

rank = draw.get_winning_rank(ticket)
print(rank)  # int rank value, or None if not winning
```
