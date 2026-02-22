[Documentation](../README.md) / [Usage](./README.md)

# Combinations

Pactole exposes dedicated classes to represent and manipulate lottery combinations:

- `EuroMillionsCombination`
- `EuroDreamsCombination`

Use them when you want to:

- Create a played ticket from user input.
- Normalize and validate values before storage.
- Compare multiple tickets.
- Evaluate a played ticket against a draw result.

## Create combinations from player input

Create combinations from explicit components when your UI already separates fields.

```python
from pactole import EuroDreamsCombination, EuroMillionsCombination

euromillions = EuroMillionsCombination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
eurodreams = EuroDreamsCombination(numbers=[2, 3, 5, 7, 9, 38], dream=[3])

print(euromillions)
print(eurodreams)
```

If your source is a flat list (CSV row, form payload, pasted string), pass a single
sequence. Pactole automatically splits values by component size.

```python
from pactole import EuroDreamsCombination, EuroMillionsCombination

euromillions = EuroMillionsCombination([3, 15, 22, 28, 44, 2, 9])
eurodreams = EuroDreamsCombination([2, 3, 5, 7, 9, 38, 3])

print(euromillions.numbers.values, euromillions.stars.values)
print(eurodreams.numbers.values, eurodreams.dream.values)
```

You can also rebuild combinations from per-component lexicographic ranks.
This is useful for reproducible indexing, partitioning, or deterministic test fixtures.

```python
from pactole import EuroDreamsCombination, EuroMillionsCombination

first_euromillions = EuroMillionsCombination(numbers=1352788, stars=43)
first_eurodreams = EuroDreamsCombination(numbers=1765425, dream=3)

print(first_euromillions)
print(first_eurodreams)
```

## Read normalized values and metadata

Each combination exposes normalized values and metadata you can persist or display.

```python
from pactole import EuroMillionsCombination

ticket = EuroMillionsCombination(numbers=[44, 3, 28, 22, 15], stars=[9, 2])

print(ticket.numbers.values)        # [3, 15, 22, 28, 44]
print(ticket.stars.values)          # [2, 9]
print(ticket.values)                # [3, 15, 22, 28, 44, 2, 9]
print(ticket.rank)                  # Global rank across all components
print(ticket.combinations)          # 139_838_160 for EuroMillions
print(ticket.min_winning_rank)      # 1
print(ticket.max_winning_rank)      # 13
```

## Generate random combinations

Use a template combination to generate random tickets that follow game rules.

```python
from pactole import EuroDreamsCombination

generator = EuroDreamsCombination()
tickets = generator.generate(n=3)

for index, ticket in enumerate(tickets, start=1):
    print(f"Ticket #{index}: {ticket}")
```

### Use partitioning to spread generation across the rank space

`generate(n, partitions)` does more than repeated random picks:

- The global rank space is split into `partitions` contiguous slices.
- Ticket `i` is sampled from slice `i % partitions`.
- This gives broader coverage than sampling all tickets from one undivided range.

Practical effects:

- Better spread in large batches (less clustering in one area of rank space).
- Deterministic slice selection order (round-robin by partition index).
- Randomness is still used inside each selected slice.

```python
from pactole import EuroMillionsCombination

generator = EuroMillionsCombination()

# 12 tickets sampled across 4 slices of the full rank space.
tickets = generator.generate(n=12, partitions=4)

for ticket in tickets:
    print(ticket.rank, ticket)
```

### Typical partitioning patterns

Use partitioning according to your generation strategy.

```python
from pactole import EuroMillionsCombination

generator = EuroMillionsCombination()

# 1) Quick balanced batch for one user session.
balanced_batch = generator.generate(n=8, partitions=4)

# 2) Parallel job pattern: one partition per worker group.
worker_batch = generator.generate(n=40, partitions=8)

# 3) Keep default behavior for small needs.
simple_batch = generator.generate(n=3)
```

Notes:

- `n` and `partitions` are clamped to at least `1`.
- Partitioning does not guarantee uniqueness; duplicates can still occur.
- If `partitions` is very large compared to `n`, many slices are never sampled.

## Compare tickets in a realistic workflow

Use comparison helpers to evaluate a candidate ticket against a reference ticket.

```python
from pactole import EuroMillionsCombination

reference = EuroMillionsCombination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
candidate = EuroMillionsCombination(numbers=[3, 15, 22, 30, 45], stars=[2, 10])

print(reference.equals(candidate))                    # Exact same ticket?
print(reference.includes(numbers=[3, 15, 22]))        # Candidate subset check
print(reference.intersects(candidate))                # Any overlap per component?

common = reference.intersection(candidate)
print(common.numbers.values)                           # [3, 15, 22]
print(common.stars.values)                             # [2]
```

## Compute winning ranks

A common use case is scoring a played ticket against an official draw.

`get_winning_rank` returns:

- an integer rank if the ticket is winning,
- `None` if it is not in any winning pattern.

```python
from pactole import EuroMillionsCombination

draw = EuroMillionsCombination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
ticket = EuroMillionsCombination(numbers=[3, 15, 22, 30, 45], stars=[2, 10])

rank = draw.get_winning_rank(ticket)

if rank is None:
    print("No winning rank")
else:
    print(f"Winning rank: {rank}")
```
