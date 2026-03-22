# LotteryCombination

[Pactole Index](../README.md#pactole-index) / [Combinations](./index.md#combinations) / LotteryCombination

> Auto-generated documentation for [combinations.lottery_combination](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py) module.

- [LotteryCombination](#lotterycombination)
  - [LotteryCombination](#lotterycombination-1)
    - [LotteryCombination()._create_combination](#lotterycombination()_create_combination)
    - [LotteryCombination().combinations](#lotterycombination()combinations)
    - [LotteryCombination().count](#lotterycombination()count)
    - [LotteryCombination.from_csv](#lotterycombinationfrom_csv)
    - [LotteryCombination.from_dict](#lotterycombinationfrom_dict)
    - [LotteryCombination.from_string](#lotterycombinationfrom_string)
    - [LotteryCombination().generate](#lotterycombination()generate)
    - [LotteryCombination().get_combination](#lotterycombination()get_combination)
    - [LotteryCombination.get_combination_factory](#lotterycombinationget_combination_factory)
    - [LotteryCombination().rank](#lotterycombination()rank)

## LotteryCombination

[Show source in lottery_combination.py:25](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L25)

Class representing a Lottery combination.

A Lottery combination is a compound combination that can consist of multiple components
(e.g., main numbers, bonus numbers). Components are built from BoundCombination instances,
which provide capacity and rank information.

#### Arguments

combination (LotteryCombination | None): The combination to copy from.
winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
    initializes an empty mapping.
- `**components` *BoundCombination* - The components of the combination.

#### Raises

- `TypeError` - If any component is not an instance of BoundCombination.

#### Examples

```python
>>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> lottery_comb = LotteryCombination(
...     main=main_numbers,
...     bonus=bonus_number,
...     winning_ranks=winning_ranks
... )
>>> lottery_comb.components
{'main': BoundCombination(...), 'bonus': BoundCombination(...)}
>>> lottery_comb.values
[1, 2, 3, 4, 5, 6]
```

#### Signature

```python
class LotteryCombination(CompoundCombination):
    def __init__(
        self,
        combination: LotteryCombination | None = None,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: BoundCombination
    ) -> None: ...
```

### LotteryCombination()._create_combination

[Show source in lottery_combination.py:274](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L274)

Create a correct class instance from the given components and winning ranks.

#### Signature

```python
def _create_combination(
    self,
    winning_ranks: CombinationWinningRanks | None = None,
    **components: CombinationInputOrRank | LotteryCombination
) -> LotteryCombination: ...
```

### LotteryCombination().combinations

[Show source in lottery_combination.py:117](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L117)

Return the total number of possible combinations.

#### Returns

- `int` - The total number of combinations, or 0 if empty.

#### Examples

```python
>>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb = LotteryCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> lottery_comb.combinations
21187600
```

#### Signature

```python
@property
def combinations(self) -> int: ...
```

### LotteryCombination().count

[Show source in lottery_combination.py:95](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L95)

Return the total capacity (count) of the combination.

Unlike length (which counts actual values), count sums each component's max capacity
(its count attribute), giving the total number of slots available.

#### Returns

- `int` - The total count.

#### Examples

```python
>>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb = LotteryCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> lottery_comb.count
6
```

#### Signature

```python
@cached_property
def count(self) -> int: ...
```

### LotteryCombination.from_csv

[Show source in lottery_combination.py:303](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L303)

Parse a CSV-compatible dictionary into lottery component values.

LotteryCombination cannot build BoundCombination components from CSV data alone,
because bounds and counts are game-specific. This parser therefore returns raw
component values for subclasses or callers that have the required metadata.

#### Arguments

- [Data](../data/index.md#data) *dict* - A CSV-compatible dictionary representation of a LotteryCombination.

#### Returns

- `dict` - Parsed component values keyed by component name.

#### Examples

```python
>>> data = {'numbers_1': 1, 'numbers_2': 2, 'extra_1': 6}
>>> LotteryCombination.from_csv(data)
{'numbers': [1, 2], 'extra': [6]}
```

#### Signature

```python
@classmethod
def from_csv(cls, data: dict) -> dict: ...
```

### LotteryCombination.from_dict

[Show source in lottery_combination.py:324](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L324)

Create a LotteryCombination from a dictionary.

#### Arguments

- [Data](../data/index.md#data) *dict* - A dictionary representation of a LotteryCombination.

#### Returns

- [LotteryCombination](#lotterycombination) - The created LotteryCombination instance.

#### Examples

```python
>>> data = {
...     'components': {
...         'main': {'values': [1, 2, 3, 4, 5], 'start': 1, 'end': 50, 'count': 5},
...         'bonus': {'values': [6], 'start': 1, 'end': 10, 'count': 1}
...     },
...     'winning_ranks': {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
... }
>>> lottery_comb = LotteryCombination.from_dict(data)
>>> lottery_comb.components
{'main': BoundCombination(...), 'bonus': BoundCombination(...)}
>>> lottery_comb.winning_ranks
{(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
```

#### Signature

```python
@classmethod
def from_dict(cls, data: dict) -> LotteryCombination: ...
```

### LotteryCombination.from_string

[Show source in lottery_combination.py:282](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L282)

Parse a string representation into lottery component values.

LotteryCombination cannot build BoundCombination components from string data alone,
because bounds and counts are game-specific. This parser therefore returns raw
component values for subclasses or callers that have the required metadata.

#### Arguments

- [Data](../data/index.md#data) *str* - A string representation of a LotteryCombination.

#### Returns

- `dict` - Parsed component values keyed by component name.

#### Examples

```python
>>> data = 'numbers: [1, 2, 3, 4, 5]  extra: [6, 7, 8]'
>>> LotteryCombination.from_string(data)
{'numbers': [1, 2, 3, 4, 5], 'extra': [6, 7, 8]}
```

#### Signature

```python
@classmethod
def from_string(cls, data: str) -> dict: ...
```

### LotteryCombination().generate

[Show source in lottery_combination.py:174](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L174)

Generate a list of random LotteryCombination instances with similar components.

#### Arguments

- `n` *int* - The number of combinations to generate. Defaults to 1.
- `partitions` *int* - The number of partitions to divide the generation into.
    Defaults to 1.

#### Returns

- `list[LotteryCombination]` - A list of generated LotteryCombination instances.

#### Examples

```python
>>> main_numbers = BoundCombination(start=1, end=50, count=5)
>>> bonus_number = BoundCombination(start=1, end=10, count=1)
>>> lottery_comb = LotteryCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> random_combs = lottery_comb.generate(n=3)
>>> len(random_combs)
3
```

#### Signature

```python
def generate(self, n: int = 1, partitions: int = 1) -> list[LotteryCombination]: ...
```

### LotteryCombination().get_combination

[Show source in lottery_combination.py:201](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L201)

Get a LotteryCombination based on provided components.

Supports integer rank input to decode a rank into component values. For a flat list
of values, each component receives values based on its count (max capacity) rather than
its current length.

#### Arguments

combination (CombinationInput | LotteryCombination | None): The base combination to
    build from. If None, uses the provided components. An integer rank decodes into
    each component's values using the cross-product encoding.
winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
    uses the current instance's winning ranks.
**components (CombinationInputOrRank | LotteryCombination): The components to
    construct the combination.

#### Returns

- [LotteryCombination](#lotterycombination) - The constructed LotteryCombination.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb = LotteryCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> new_comb = lottery_comb.get_combination(main=[1, 2, 3, 6, 7])
>>> new_comb.components
{'main': BoundCombination(...), 'bonus': BoundCombination(...)}
```

#### Signature

```python
def get_combination(
    self,
    combination: CombinationInput | LotteryCombination | None = None,
    winning_ranks: CombinationWinningRanks | None = None,
    **components: CombinationInputOrRank | LotteryCombination
) -> LotteryCombination: ...
```

### LotteryCombination.get_combination_factory

[Show source in lottery_combination.py:138](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L138)

Get the combination factory.

It checks that the provided combination_factory is a callable, and if not, it returns a
default factory from LotteryCombination, which will produce combinations with no
components and no winning ranks.

An instance of a LotteryCombination can be used to produce a factory.

#### Arguments

combination_factory (CombinationFactory | LotteryCombination | Any): A factory
    function or class to create a combination instance. If not callable,
    a default LotteryCombination instance will be used.

#### Returns

- `CombinationFactory` - The combination factory.

#### Examples

```python
>>> factory = LotteryCombination.get_combination_factory(None)
factory(main=[1, 2, 3, 4, 5], bonus=[6])
LotteryCombination()
>>> factory = LotteryCombination.get_combination_factory(LotteryCombination(
...     main=BoundCombination(start=1, end=50, count=5)
... ))
factory(main=[1, 2, 3, 4, 5])
LotteryCombination(main=BoundCombination(...))
```

#### Signature

```python
@staticmethod
def get_combination_factory(
    combination_factory: CombinationFactory | LotteryCombination | Any,
) -> CombinationFactory: ...
```

### LotteryCombination().rank

[Show source in lottery_combination.py:68](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L68)

Get the lexicographic rank of the combination.

The rank is computed as a cross-product encoding of component ranks: each component's
rank is weighted by the product of the total combinations of all subsequent components.

#### Returns

- `CombinationRank` - The lexicographic rank of the combination.

#### Examples

```python
>>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb = LotteryCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> lottery_comb.rank
1234567
```

#### Signature

```python
@cached_property
def rank(self) -> CombinationRank: ...
```