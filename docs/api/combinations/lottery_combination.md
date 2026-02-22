# LotteryCombination

[Pactole Index](../README.md#pactole-index) / [Combinations](./index.md#combinations) / LotteryCombination

> Auto-generated documentation for [combinations.lottery_combination](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py) module.

- [LotteryCombination](#lotterycombination)
  - [CombinationFactory](#combinationfactory)
    - [CombinationFactory().__call__](#combinationfactory()__call__)
  - [LotteryCombination](#lotterycombination-1)
    - [LotteryCombination()._create_combination](#lotterycombination()_create_combination)
    - [LotteryCombination().combinations](#lotterycombination()combinations)
    - [LotteryCombination().compares](#lotterycombination()compares)
    - [LotteryCombination().components](#lotterycombination()components)
    - [LotteryCombination().copy](#lotterycombination()copy)
    - [LotteryCombination().count](#lotterycombination()count)
    - [LotteryCombination().equals](#lotterycombination()equals)
    - [LotteryCombination().generate](#lotterycombination()generate)
    - [LotteryCombination().get_combination](#lotterycombination()get_combination)
    - [LotteryCombination.get_combination_factory](#lotterycombinationget_combination_factory)
    - [LotteryCombination().get_component](#lotterycombination()get_component)
    - [LotteryCombination().get_component_values](#lotterycombination()get_component_values)
    - [LotteryCombination().get_components](#lotterycombination()get_components)
    - [LotteryCombination().get_winning_rank](#lotterycombination()get_winning_rank)
    - [LotteryCombination().includes](#lotterycombination()includes)
    - [LotteryCombination().intersection](#lotterycombination()intersection)
    - [LotteryCombination().intersects](#lotterycombination()intersects)
    - [LotteryCombination().length](#lotterycombination()length)
    - [LotteryCombination().max_winning_rank](#lotterycombination()max_winning_rank)
    - [LotteryCombination().min_winning_rank](#lotterycombination()min_winning_rank)
    - [LotteryCombination().nb_winning_ranks](#lotterycombination()nb_winning_ranks)
    - [LotteryCombination().rank](#lotterycombination()rank)
    - [LotteryCombination().similarity](#lotterycombination()similarity)
    - [LotteryCombination().values](#lotterycombination()values)
    - [LotteryCombination().winning_ranks](#lotterycombination()winning_ranks)

## CombinationFactory

[Show source in lottery_combination.py:25](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L25)

Protocol for a combination factory.

#### Signature

```python
class CombinationFactory(Protocol): ...
```

### CombinationFactory().__call__

[Show source in lottery_combination.py:28](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L28)

Create a combination from the provided components.

#### Arguments

combination (CombinationInput | LotteryCombination | None): The base combination to
    build from. If None, uses the provided components.
**components (CombinationInputOrRank | LotteryCombination): The components to construct
    the combination.

#### Returns

- [LotteryCombination](#lotterycombination) - An instance of LotteryCombination created from the provided
    components.

#### Signature

```python
def __call__(
    self,
    combination: CombinationInput | LotteryCombination | None = None,
    **components: CombinationInputOrRank | LotteryCombination
) -> LotteryCombination: ...
```

#### See also

- [LotteryCombination](#lotterycombination)



## LotteryCombination

[Show source in lottery_combination.py:47](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L47)

Class representing a Lottery combination.

A Lottery combination is a compound combination that can consist of multiple components
(e.g., main numbers, bonus numbers).

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
class LotteryCombination:
    def __init__(
        self,
        combination: LotteryCombination | None = None,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: BoundCombination
    ) -> None: ...
```

### LotteryCombination()._create_combination

[Show source in lottery_combination.py:467](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L467)

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

[Show source in lottery_combination.py:202](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L202)

Return the total number of possible combinations.

#### Returns

- `int` - The total number of combinations.

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

### LotteryCombination().compares

[Show source in lottery_combination.py:817](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L817)

Compare the combination with another combination.

#### Arguments

combination (CombinationInput | LotteryCombination | None): The other combination to
    compare against.
**components (CombinationInputOrRank | LotteryCombination): The components of the other
    combination.

#### Returns

- `int` - -1 if self < combination, 0 if self == combination, 1 if self > combination.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number1 = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb1 = LotteryCombination(
...     main=main_numbers1,
...     bonus=bonus_number1
... )
>>> main_numbers2 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number2 = BoundCombination(values=[7], start=1, end=10, count=1)
>>> lottery_comb2 = LotteryCombination(
...     main=main_numbers2,
...     bonus=bonus_number2
... )
>>> lottery_comb1.compares(lottery_comb2)
-1
```

#### Signature

```python
def compares(
    self,
    combination: CombinationInput | LotteryCombination | None = None,
    **components: CombinationInputOrRank | LotteryCombination
) -> int: ...
```

### LotteryCombination().components

[Show source in lottery_combination.py:102](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L102)

Get the components of the combination.

#### Returns

- [CombinationComponents](#lotterycombination) - The components of the combination.

#### Examples

```python
>>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb = LotteryCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> lottery_comb.components
{'main': BoundCombination(...), 'bonus': BoundCombination(...)}
```

#### Signature

```python
@property
def components(self) -> CombinationComponents: ...
```

#### See also

- [CombinationComponents](#combinationcomponents)

### LotteryCombination().copy

[Show source in lottery_combination.py:379](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L379)

Create a copy of the LotteryCombination with optional modifications.

#### Arguments

winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
    uses the current instance's winning ranks.
**components (CombinationInputOrRank | LotteryCombination): The components to modify in
    the copy. If not provided, the original component is used.

#### Returns

- [LotteryCombination](#lotterycombination) - A new LotteryCombination instance with the specified modifications.

#### Signature

```python
def copy(
    self,
    winning_ranks: CombinationWinningRanks | None = None,
    **components: CombinationInputOrRank | LotteryCombination
) -> LotteryCombination: ...
```

### LotteryCombination().count

[Show source in lottery_combination.py:183](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L183)

Return the count of numbers in the combination.

#### Returns

- `int` - The count of numbers.

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

### LotteryCombination().equals

[Show source in lottery_combination.py:615](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L615)

Check if the combination is equal to another combination.

#### Arguments

combination (CombinationInput | LotteryCombination | None): The other combination to
    compare against.
**components (CombinationInputOrRank | LotteryCombination): The components of the other
    combination.

#### Returns

- `bool` - True if equal, False otherwise.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number1 = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb1 = LotteryCombination(
...     main=main_numbers1,
...     bonus=bonus_number1
... )
>>> main_numbers2 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number2 = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb2 = LotteryCombination(
...     main=main_numbers2,
...     bonus=bonus_number2
... )
>>> lottery_comb1.equals(lottery_comb2)
True
```

#### Signature

```python
def equals(
    self,
    combination: CombinationInput | LotteryCombination | None = None,
    **components: CombinationInputOrRank | LotteryCombination
) -> bool: ...
```

### LotteryCombination().generate

[Show source in lottery_combination.py:341](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L341)

Generate a list of random LotteryCombination with similar components.

#### Arguments

- `n` *int* - The number of combinations to generate. Defaults to 1.
- `partitions` *int* - The number of partitions to divide the generation into. Defaults to 1.

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
>>> random_combs[0].values
[3, 15, 22, 34, 45, 7]
```

#### Signature

```python
def generate(self, n: int = 1, partitions: int = 1) -> list[LotteryCombination]: ...
```

### LotteryCombination().get_combination

[Show source in lottery_combination.py:405](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L405)

Get a LotteryCombination based on provided components.

#### Arguments

combination (CombinationInput | LotteryCombination | None): The base combination to
    build from. If None, uses the provided components.
winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
    uses the current instance's winning ranks.
**components (CombinationInputOrRank | LotteryCombination): The components to construct
    the combination.

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

[Show source in lottery_combination.py:297](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L297)

Get the combination factory.

It check that the provided combination_factory is a callable, and if not, it returns a
default factory from LotteryCombination, which is in this case will produce combinations
with no components and no winning ranks.

An instance of a LotteryCombination can be used to produce a factory.

#### Arguments

combination_factory (CombinationFactory | LotteryCombination | Any): A factory function
    or class to create a combination instance. If None, a default LotteryCombination
    instance will be used. Default is None.

#### Returns

- [CombinationFactory](#combinationfactory) - The combination factory.

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
>>> factory = LotteryCombination.get_combination_factory(lambda **components:
...     LotteryCombination(**{
...         k: BoundCombination(start=min(v), end=max(v), count=len(v))
...         for k, v in components.items()
...     })
... )
factory(main=[1, 2, 3, 4, 5], bonus=[6])
LotteryCombination(main=BoundCombination(...), bonus=BoundCombination(...))
```

#### Signature

```python
@staticmethod
def get_combination_factory(
    combination_factory: CombinationFactory | LotteryCombination | Any,
) -> CombinationFactory: ...
```

#### See also

- [CombinationFactory](#combinationfactory)

### LotteryCombination().get_component

[Show source in lottery_combination.py:511](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L511)

Get the parameters for a specific component of the combination.

#### Arguments

- `name` *str* - The name of the component.

#### Returns

BoundCombination | None: The parameters for the specified component,
    or None if not found.

#### Examples

```python
>>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb = LotteryCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> lottery_comb.get_component('main')
BoundCombination(...)
>>> lottery_comb.get_component('bonus')
BoundCombination(...)
>>> lottery_comb.get_component('extra')
None
```

#### Signature

```python
def get_component(self, name: str) -> BoundCombination | None: ...
```

### LotteryCombination().get_component_values

[Show source in lottery_combination.py:537](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L537)

Get the values for a specific component of the combination.

#### Arguments

- `name` *str* - The name of the component.

#### Returns

- `CombinationValues` - The values for the specified component.

#### Examples

```python
>>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb = LotteryCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> lottery_comb.get_component_values('main')
[1, 2, 3, 4, 5]
>>> lottery_comb.get_component_values('bonus')
[6]
>>> lottery_comb.get_component_values('extra')
[]
```

#### Signature

```python
def get_component_values(self, name: str) -> CombinationValues: ...
```

### LotteryCombination().get_components

[Show source in lottery_combination.py:475](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L475)

Get the parameters for multiple components of the combination.

#### Arguments

**components (CombinationInputOrRank | LotteryCombination): The names and values of the
    components.

#### Returns

- [CombinationComponents](#lotterycombination) - The parameters for the specified components.

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
>>> lottery_comb.get_components(main=[1, 2, 3, 4, 5], bonus=[6])
{'main': BoundCombination(...), 'bonus': BoundCombination(...)}
>>> lottery_comb.get_components(main=[1, 2, 3])
{'main': BoundCombination(...)}
>>> lottery_comb.get_components(bonus=[7])
{'bonus': BoundCombination(...)}
>>> lottery_comb.get_components(extra=[8])
KeyError: 'Component "extra" does not exist in the combination.'
```

#### Signature

```python
def get_components(
    self, **components: CombinationInputOrRank | LotteryCombination
) -> CombinationComponents: ...
```

#### See also

- [CombinationComponents](#combinationcomponents)

### LotteryCombination().get_winning_rank

[Show source in lottery_combination.py:566](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L566)

Get the winning rank of the combination against a winning combination.

#### Arguments

combination (CombinationInput | LotteryCombination | None): The winning combination to
    compare against.
**components (CombinationInputOrRank | LotteryCombination): The components of the
    winning combination.

#### Returns

int | None: The winning rank, or None if not a winning combination.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

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
>>> winning_comb = lottery_comb.get_combination(main=[1, 2, 3, 4, 5], bonus=[6])
>>> lottery_comb.get_winning_rank(winning_comb)
1
>>> winning_comb = lottery_comb.get_combination(main=[1, 2, 3, 4, 5], bonus=[7])
>>> lottery_comb.get_winning_rank(winning_comb)
2
>>> winning_comb = lottery_comb.get_combination(main=[1, 2, 3, 4, 6], bonus=[6])
>>> lottery_comb.get_winning_rank(winning_comb)
3
>>> winning_comb = lottery_comb.get_combination(main=[1, 2, 3, 4, 6], bonus=[7])
>>> lottery_comb.get_winning_rank(winning_comb)
4
>>> winning_comb = lottery_comb.get_combination(main=[10, 11, 12, 13, 14], bonus=[15])
>>> lottery_comb.get_winning_rank(winning_comb)
None
```

#### Signature

```python
def get_winning_rank(
    self,
    combination: CombinationInput | LotteryCombination | None = None,
    **components: CombinationInputOrRank | LotteryCombination
) -> int | None: ...
```

### LotteryCombination().includes

[Show source in lottery_combination.py:665](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L665)

Check if the combination includes another combination.

#### Arguments

combination (CombinationInput | LotteryCombination | None): The other combination to
    compare against.
**components (CombinationInputOrRank | LotteryCombination): The components of the other
    combination.

#### Returns

- `bool` - True if includes, False otherwise.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number1 = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb1 = LotteryCombination(
...     main=main_numbers1,
...     bonus=bonus_number1
... )
>>> main_numbers2 = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)
>>> bonus_number2 = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb2 = LotteryCombination(
...     main=main_numbers2,
...     bonus=bonus_number2
... )
>>> lottery_comb1.includes(lottery_comb2)
True
>>> main_numbers3 = BoundCombination(values=[1, 2, 6], start=1, end=50, count=5)
>>> lottery_comb3 = LotteryCombination(
...     main=main_numbers3,
...     bonus=bonus_number2
... )
>>> lottery_comb1.includes(lottery_comb3)
False
```

#### Signature

```python
def includes(
    self,
    combination: CombinationInput | LotteryCombination | None = None,
    **components: CombinationInputOrRank | LotteryCombination
) -> bool: ...
```

### LotteryCombination().intersection

[Show source in lottery_combination.py:770](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L770)

Get the intersection with another combination.

#### Arguments

combination (CombinationInput | LotteryCombination | None): The other combination to
    compare against.
**components (CombinationInputOrRank | LotteryCombination): The components of the other
    combination.

#### Returns

- [LotteryCombination](#lotterycombination) - The intersection combination.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number1 = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb1 = LotteryCombination(
...     main=main_numbers1,
...     bonus=bonus_number1
... )
>>> main_numbers2 = BoundCombination(values=[4, 5, 6], start=1, end=50, count=5)
>>> bonus_number2 = BoundCombination(values=[7], start=1, end=10, count=1)
>>> lottery_comb2 = LotteryCombination(
...     main=main_numbers2,
...     bonus=bonus_number2
... )
>>> intersection_comb = lottery_comb1.intersection(lottery_comb2)
>>> intersection_comb.components
{'main': BoundCombination(...), 'bonus': BoundCombination(...)}
>>> intersection_comb.values
[4, 5]
```

#### Signature

```python
def intersection(
    self,
    combination: CombinationInput | LotteryCombination | None = None,
    **components: CombinationInputOrRank | LotteryCombination
) -> LotteryCombination: ...
```

### LotteryCombination().intersects

[Show source in lottery_combination.py:717](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L717)

Check if the combination intersects with another combination.

#### Arguments

combination (CombinationInput | LotteryCombination | None): The other combination to
    compare against.
**components (CombinationInputOrRank | LotteryCombination): The components of the other
    combination.

#### Returns

- `bool` - True if intersects, False otherwise.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number1 = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb1 = LotteryCombination(
...     main=main_numbers1,
...     bonus=bonus_number1
... )
>>> main_numbers2 = BoundCombination(values=[4, 5, 6], start=1, end=50, count=5)
>>> bonus_number2 = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb2 = LotteryCombination(
...     main=main_numbers2,
...     bonus=bonus_number2
... )
>>> lottery_comb1.intersects(lottery_comb2)
True
>>> main_numbers3 = BoundCombination(values=[7, 8, 9], start=1, end=50, count=5)
>>> lottery_comb3 = LotteryCombination(
...     main=main_numbers3,
...     bonus=bonus_number2
... )
>>> lottery_comb1.intersects(lottery_comb3)
False
```

#### Signature

```python
def intersects(
    self,
    combination: CombinationInput | LotteryCombination | None = None,
    **components: CombinationInputOrRank | LotteryCombination
) -> bool: ...
```

### LotteryCombination().length

[Show source in lottery_combination.py:164](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L164)

Get the total length of the combination.

#### Returns

- `int` - The total length of the combination.

#### Examples

```python
>>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb = LotteryCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> lottery_comb.length
6
```

#### Signature

```python
@cached_property
def length(self) -> int: ...
```

### LotteryCombination().max_winning_rank

[Show source in lottery_combination.py:277](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L277)

Get the maximum winning rank.

#### Returns

int | None: The maximum winning rank, or None if there are no winning ranks.

#### Examples

```python
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
>>> lottery_comb.max_winning_rank
4
>>> lottery_comb_empty = LotteryCombination()
>>> lottery_comb_empty.max_winning_rank
None
```

#### Signature

```python
@property
def max_winning_rank(self) -> int | None: ...
```

### LotteryCombination().min_winning_rank

[Show source in lottery_combination.py:257](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L257)

Get the minimum winning rank.

#### Returns

int | None: The minimum winning rank, or None if there are no winning ranks.

#### Examples

```python
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
>>> lottery_comb.min_winning_rank
1
>>> lottery_comb_empty = LotteryCombination()
>>> lottery_comb_empty.min_winning_rank
None
```

#### Signature

```python
@property
def min_winning_rank(self) -> int | None: ...
```

### LotteryCombination().nb_winning_ranks

[Show source in lottery_combination.py:238](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L238)

Get the number of winning ranks.

#### Returns

- `int` - The number of winning ranks.

#### Examples

```python
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
>>> lottery_comb.nb_winning_ranks
4
```

#### Signature

```python
@property
def nb_winning_ranks(self) -> int: ...
```

### LotteryCombination().rank

[Show source in lottery_combination.py:140](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L140)

Get the lexicographic rank of the combination.

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

### LotteryCombination().similarity

[Show source in lottery_combination.py:868](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L868)

Calculate the similarity with another combination.

#### Arguments

combination (CombinationInput | LotteryCombination | None): The other combination to
    compare against.
**components (CombinationInputOrRank | LotteryCombination): The components of the other
    combination.

#### Returns

- `float` - Similarity ratio between 0 and 1.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number1 = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb1 = LotteryCombination(
...     main=main_numbers1,
...     bonus=bonus_number1
... )
>>> main_numbers2 = BoundCombination(values=[1, 2, 3, 6, 7], start=1, end=50, count=5)
>>> bonus_number2 = BoundCombination(values=[8], start=1, end=10, count=1)
>>> lottery_comb2 = LotteryCombination(
...     main=main_numbers2,
...     bonus=bonus_number2
... )
>>> lottery_comb1.similarity(lottery_comb2)
0.375
```

#### Signature

```python
def similarity(
    self,
    combination: CombinationInput | LotteryCombination | None = None,
    **components: CombinationInputOrRank | LotteryCombination
) -> float: ...
```

### LotteryCombination().values

[Show source in lottery_combination.py:121](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L121)

Get all numbers in the combination.

#### Returns

- `CombinationValues` - The list of all numbers in the combination.

#### Examples

```python
>>> main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)
>>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
>>> lottery_comb = LotteryCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> lottery_comb.values
[1, 2, 3, 4, 5, 6]
```

#### Signature

```python
@cached_property
def values(self) -> CombinationValues: ...
```

### LotteryCombination().winning_ranks

[Show source in lottery_combination.py:223](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/lottery_combination.py#L223)

Get the winning ranks mapping.

#### Returns

- [CombinationWinningRanks](#lotterycombination) - The winning ranks mapping.

#### Examples

```python
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
>>> lottery_comb.winning_ranks
{(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
```

#### Signature

```python
@property
def winning_ranks(self) -> CombinationWinningRanks: ...
```

#### See also

- [CombinationWinningRanks](#combinationwinningranks)