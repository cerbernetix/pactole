# CompoundCombination

[Pactole Index](../README.md#pactole-index) / [Combinations](./index.md#combinations) / CompoundCombination

> Auto-generated documentation for [combinations.compound_combination](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py) module.

- [CompoundCombination](#compoundcombination)
  - [CombinationFactory](#combinationfactory)
    - [CombinationFactory().__call__](#combinationfactory()__call__)
  - [CompoundCombination](#compoundcombination-1)
    - [CompoundCombination()._create_combination](#compoundcombination()_create_combination)
    - [CompoundCombination().compares](#compoundcombination()compares)
    - [CompoundCombination().components](#compoundcombination()components)
    - [CompoundCombination().copy](#compoundcombination()copy)
    - [CompoundCombination().dump](#compoundcombination()dump)
    - [CompoundCombination().equals](#compoundcombination()equals)
    - [CompoundCombination.from_csv](#compoundcombinationfrom_csv)
    - [CompoundCombination.from_dict](#compoundcombinationfrom_dict)
    - [CompoundCombination.from_json](#compoundcombinationfrom_json)
    - [CompoundCombination.from_string](#compoundcombinationfrom_string)
    - [CompoundCombination().get](#compoundcombination()get)
    - [CompoundCombination().get_combination](#compoundcombination()get_combination)
    - [CompoundCombination.get_combination_factory](#compoundcombinationget_combination_factory)
    - [CompoundCombination().get_components](#compoundcombination()get_components)
    - [CompoundCombination.get_components_from_csv](#compoundcombinationget_components_from_csv)
    - [CompoundCombination.get_components_from_string](#compoundcombinationget_components_from_string)
    - [CompoundCombination().get_values](#compoundcombination()get_values)
    - [CompoundCombination().get_winning_rank](#compoundcombination()get_winning_rank)
    - [CompoundCombination().includes](#compoundcombination()includes)
    - [CompoundCombination().intersection](#compoundcombination()intersection)
    - [CompoundCombination().intersects](#compoundcombination()intersects)
    - [CompoundCombination().length](#compoundcombination()length)
    - [CompoundCombination().max_winning_rank](#compoundcombination()max_winning_rank)
    - [CompoundCombination().min_winning_rank](#compoundcombination()min_winning_rank)
    - [CompoundCombination().nb_winning_ranks](#compoundcombination()nb_winning_ranks)
    - [CompoundCombination().similarity](#compoundcombination()similarity)
    - [CompoundCombination().to_csv](#compoundcombination()to_csv)
    - [CompoundCombination().to_dict](#compoundcombination()to_dict)
    - [CompoundCombination().to_json](#compoundcombination()to_json)
    - [CompoundCombination().to_string](#compoundcombination()to_string)
    - [CompoundCombination().values](#compoundcombination()values)
    - [CompoundCombination().winning_ranks](#compoundcombination()winning_ranks)

## CombinationFactory

[Show source in compound_combination.py:27](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L27)

Protocol for a combination factory.

#### Signature

```python
class CombinationFactory(Protocol): ...
```

### CombinationFactory().__call__

[Show source in compound_combination.py:30](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L30)

Create a combination from the provided components.

#### Arguments

combination (CombinationInput | CompoundCombination | None): The base combination to
    build from. If None, uses the provided components.
**components (Combination | CombinationInput | CompoundCombination): The components to
    construct the combination. Can be Combination instances, values to convert to
    Combination, or CompoundCombination instances.

#### Returns

- [CompoundCombination](#compoundcombination) - An instance of CompoundCombination created from the provided
    components.

#### Signature

```python
def __call__(
    self,
    combination: CombinationInput | CompoundCombination | None = None,
    **components: Combination | CombinationInput | CompoundCombination
) -> CompoundCombination: ...
```

#### See also

- [CompoundCombination](#compoundcombination)



## CompoundCombination

[Show source in compound_combination.py:50](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L50)

Class representing a compound combination.

A compound combination can consist of multiple components (e.g., main numbers, bonus numbers).
Components are built from Combination instances.

#### Arguments

combination (CompoundCombination | None): The combination to copy from.
winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
    initializes an empty mapping.
**components (Combination | CombinationInput): The components of the combination. Each
    can be either a Combination instance or a value/list that will be converted to a
    Combination.

#### Raises

- `ValueError` - If a component cannot be converted to a Combination instance.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> compound_comb.components
{'main': Combination([1, 2, 3, 4, 5]), 'bonus': Combination([6])}
```

You can also use lists directly:

```python
>>> compound_comb = CompoundCombination(
...     main=[1, 2, 3, 4, 5],
...     bonus=[6]
... )
>>> compound_comb.values
[1, 2, 3, 4, 5, 6]
```

#### Signature

```python
class CompoundCombination:
    def __init__(
        self,
        combination: CompoundCombination | None = None,
        winning_ranks: CombinationWinningRanks | None = None,
        **components: Combination | CombinationInput
    ) -> None: ...
```

### CompoundCombination()._create_combination

[Show source in compound_combination.py:376](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L376)

Create a correct class instance from the given components and winning ranks.

#### Signature

```python
def _create_combination(
    self,
    winning_ranks: CombinationWinningRanks | None = None,
    **components: Combination | CombinationInput
) -> CompoundCombination: ...
```

### CompoundCombination().compares

[Show source in compound_combination.py:701](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L701)

Compare the combination with another combination.

#### Arguments

combination (CombinationInput | CompoundCombination | None): The other combination to
    compare against.
**components (CombinationInputOrRank | CompoundCombination): The components of the
    other combination.

#### Returns

- `int` - -1 if self < combination, 0 if self == combination, 1 if self > combination.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers1 = Combination([1, 2, 3, 4, 5])
>>> bonus_number1 = Combination([6])
>>> compound_comb1 = CompoundCombination(
...     main=main_numbers1,
...     bonus=bonus_number1
... )
>>> main_numbers2 = Combination([1, 2, 3, 4, 5])
>>> bonus_number2 = Combination([7])
>>> compound_comb2 = CompoundCombination(
...     main=main_numbers2,
...     bonus=bonus_number2
... )
>>> compound_comb1.compares(compound_comb2)
-1
```

#### Signature

```python
def compares(
    self,
    combination: CombinationInput | CompoundCombination | None = None,
    **components: CombinationInputOrRank | CompoundCombination
) -> int: ...
```

### CompoundCombination().components

[Show source in compound_combination.py:108](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L108)

Get the components of the combination.

#### Returns

- [CombinationComponents](#compoundcombination) - The components of the combination.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> compound_comb.components
{'main': Combination([1, 2, 3, 4, 5]), 'bonus': Combination([6])}
```

#### Signature

```python
@property
def components(self) -> CombinationComponents: ...
```

#### See also

- [CombinationComponents](#combinationcomponents)

### CompoundCombination().copy

[Show source in compound_combination.py:273](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L273)

Create a copy of the CompoundCombination with optional modifications.

#### Arguments

winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
    uses the current instance's winning ranks.
**components (Combination | CombinationInput): The components to modify in the copy.
    Can be Combination instances or values that will be converted to Combination.
    If not provided, the original component is used.

#### Returns

- [CompoundCombination](#compoundcombination) - A new CompoundCombination instance with the specified
    modifications.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number,
...     winning_ranks=winning_ranks
... )
>>> new_comb = compound_comb.copy(main=[1, 2, 3, 6, 7])
>>> new_comb.components
{'main': Combination([1, 2, 3, 6, 7]), 'bonus': Combination([6])}
```

#### Signature

```python
def copy(
    self,
    winning_ranks: CombinationWinningRanks | None = None,
    **components: Combination | CombinationInput
) -> CompoundCombination: ...
```

### CompoundCombination().dump

[Show source in compound_combination.py:813](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L813)

Dump the CompoundCombination to a dictionary.

#### Returns

- `dict` - A dictionary representation of the CompoundCombination.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number,
...     winning_ranks=winning_ranks
... )
>>> compound_comb.dump()
{
    'main': [1, 2, 3, 4, 5],
    'bonus': [6],
}
```

#### Signature

```python
def dump(self) -> dict: ...
```

### CompoundCombination().equals

[Show source in compound_combination.py:515](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L515)

Check if the combination is equal to another combination.

#### Arguments

combination (CombinationInput | CompoundCombination | None): The other combination to
    compare against.
**components (CombinationInputOrRank | CompoundCombination): The components of the
    other combination.

#### Returns

- `bool` - True if equal, False otherwise.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers1 = Combination([1, 2, 3, 4, 5])
>>> bonus_number1 = Combination([6])
>>> compound_comb1 = CompoundCombination(
...     main=main_numbers1,
...     bonus=bonus_number1
... )
>>> main_numbers2 = Combination([1, 2, 3, 4, 5])
>>> bonus_number2 = Combination([6])
>>> compound_comb2 = CompoundCombination(
...     main=main_numbers2,
...     bonus=bonus_number2
... )
>>> compound_comb1.equals(compound_comb2)
True
```

#### Signature

```python
def equals(
    self,
    combination: CombinationInput | CompoundCombination | None = None,
    **components: CombinationInputOrRank | CompoundCombination
) -> bool: ...
```

### CompoundCombination.from_csv

[Show source in compound_combination.py:1002](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L1002)

Create a CompoundCombination from a CSV-serializable dictionary.

#### Arguments

- [Data](../data/index.md#data) *dict* - A CSV-serializable dictionary representation of a CompoundCombination.

#### Returns

- [CompoundCombination](#compoundcombination) - The created CompoundCombination instance.

#### Examples

```python
>>> data = {'main_1': 1, 'main_2': 2, 'main_3': 3, 'main_4': 4, 'main_5': 5,
...         'bonus_1': 6}
>>> combination = CompoundCombination.from_csv(data)
>>> combination.components['main'].values
[1, 2, 3, 4, 5]
>>> combination.components['bonus'].values
[6]
```

#### Signature

```python
@classmethod
def from_csv(cls, data: dict) -> CompoundCombination: ...
```

### CompoundCombination.from_dict

[Show source in compound_combination.py:1047](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L1047)

Create a CompoundCombination from a dictionary.

#### Arguments

- [Data](../data/index.md#data) *dict* - A dictionary representation of a CompoundCombination.

#### Returns

- [CompoundCombination](#compoundcombination) - The created CompoundCombination instance.

#### Examples

```python
>>> data = {
...     'components': {
...         'main': {'values': [1, 2, 3, 4, 5], 'rank': None, 'start': 1},
...         'bonus': {'values': [6], 'rank': None, 'start': 1}
...     },
...     'winning_ranks': {(5, 1): 1}
... }
>>> compound_comb = CompoundCombination.from_dict(data)
>>> compound_comb.components
{'main': Combination([1, 2, 3, 4, 5]), 'bonus': Combination([6])}
>>> compound_comb.winning_ranks
{(5, 1): 1}
```

#### Signature

```python
@classmethod
def from_dict(cls, data: dict) -> CompoundCombination: ...
```

### CompoundCombination.from_json

[Show source in compound_combination.py:1023](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L1023)

Create a CompoundCombination from a JSON-serializable dictionary.

#### Arguments

- [Data](../data/index.md#data) *dict* - A JSON-serializable dictionary representation of a CompoundCombination.

#### Returns

- [CompoundCombination](#compoundcombination) - The created CompoundCombination instance.

#### Examples

```python
>>> data = {
...     'components': {
...         'main': {'values': [1, 2, 3, 4, 5], 'rank': None, 'start': 1},
...         'bonus': {'values': [6], 'rank': None, 'start': 1}
...     },
...     'winning_ranks': {(5, 1): 1}
... }
>>> compound_comb = CompoundCombination.from_json(data)
>>> compound_comb.components
{'main': Combination([1, 2, 3, 4, 5]), 'bonus': Combination([6])}
```

#### Signature

```python
@classmethod
def from_json(cls, data: dict) -> CompoundCombination: ...
```

### CompoundCombination.from_string

[Show source in compound_combination.py:982](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L982)

Create a CompoundCombination from a string representation.

#### Arguments

- [Data](../data/index.md#data) *str* - A string representation of a CompoundCombination.

#### Returns

- [CompoundCombination](#compoundcombination) - The created CompoundCombination instance.

#### Examples

```python
>>> data = 'main: [1, 2, 3, 4, 5]  bonus: [6]'
>>> combination = CompoundCombination.from_string(data)
>>> combination.components['main'].values
[1, 2, 3, 4, 5]
>>> combination.components['bonus'].values
[6]
```

#### Signature

```python
@classmethod
def from_string(cls, data: str) -> CompoundCombination: ...
```

### CompoundCombination().get

[Show source in compound_combination.py:421](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L421)

Get the parameters for a specific component of the combination.

#### Arguments

- `name` *str* - The name of the component.

#### Returns

Combination | None: The parameters for the specified component, or None if not found.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> compound_comb.get('main')
Combination([1, 2, 3, 4, 5])
>>> compound_comb.get('bonus')
Combination([6])
>>> compound_comb.get('extra')
None
```

#### Signature

```python
def get(self, name: str) -> Combination | None: ...
```

### CompoundCombination().get_combination

[Show source in compound_combination.py:314](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L314)

Get a CompoundCombination based on provided components.

When a flat list of values is provided, it is split among the components in order by the
current length of each component. This means the flat-list input works correctly only when
all components have at least one value.

#### Arguments

combination (CombinationInput | CompoundCombination | None): The base combination to
    build from. If None, uses the provided components. Integer rank input is not
    supported; use a subclass that provides rank-based retrieval.
winning_ranks (CombinationWinningRanks | None): The winning ranks mapping. If None,
    uses the current instance's winning ranks.
**components (Combination | CombinationInput | CompoundCombination): The components to
    construct the combination. Can be Combination instances, values to convert to
    Combination, or CompoundCombination instances.

#### Returns

- [CompoundCombination](#compoundcombination) - The constructed CompoundCombination.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> new_comb = compound_comb.get_combination(main=[1, 2, 3, 6, 7])
>>> new_comb.components
{'main': Combination([1, 2, 3, 6, 7]), 'bonus': Combination([6])}
```

#### Signature

```python
def get_combination(
    self,
    combination: CombinationInput | CompoundCombination | None = None,
    winning_ranks: CombinationWinningRanks | None = None,
    **components: Combination | CombinationInput | CompoundCombination
) -> CompoundCombination: ...
```

### CompoundCombination.get_combination_factory

[Show source in compound_combination.py:237](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L237)

Get the combination factory.

It checks that the provided combination_factory is a callable, and if not, it returns a
default factory from CompoundCombination, which in this case will produce combinations
with no winning ranks since the default CompoundCombination has no winning ranks.

An instance of a CompoundCombination can be used to produce a factory.

#### Arguments

combination_factory (CombinationFactory | CompoundCombination | Any): A factory
    function or class to create a combination instance. If not callable,
    a default CompoundCombination instance will be used.

#### Returns

- [CombinationFactory](#combinationfactory) - The combination factory.

#### Examples

```python
>>> factory = CompoundCombination.get_combination_factory(None)
>>> factory(main=[1, 2, 3, 4, 5], bonus=[6])
CompoundCombination(main=Combination([1, 2, 3, 4, 5]), bonus=Combination([6]))
>>> factory = CompoundCombination.get_combination_factory(CompoundCombination(
...     main=Combination([1, 2, 3, 4, 5])
... ))
>>> factory(main=[3, 4, 5, 6, 7])
CompoundCombination(main=Combination([3, 4, 5, 6, 7]), bonus=Combination([]))
```

#### Signature

```python
@staticmethod
def get_combination_factory(
    combination_factory: CombinationFactory | CompoundCombination | Any,
) -> CombinationFactory: ...
```

#### See also

- [CombinationFactory](#combinationfactory)

### CompoundCombination().get_components

[Show source in compound_combination.py:384](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L384)

Get the parameters for multiple components of the combination.

#### Arguments

**components (Combination | CombinationInput | CompoundCombination): The names and
    values of the components. Can be Combination instances, values to convert to
    Combination, or CompoundCombination instances.

#### Returns

- [CombinationComponents](#compoundcombination) - The parameters for the specified components.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> compound_comb.get_components(main=[1, 2, 3, 4, 5], bonus=[6])
{'main': Combination([1, 2, 3, 4, 5]), 'bonus': Combination([6])}
>>> compound_comb.get_components(main=[1, 2, 3])
{'main': Combination([1, 2, 3])}
>>> compound_comb.get_components(bonus=[7])
{'bonus': Combination([7])}
>>> compound_comb.get_components(extra=[8])
KeyError: 'extra'
```

#### Signature

```python
def get_components(
    self, **components: Combination | CombinationInput | CompoundCombination
) -> CombinationComponents: ...
```

#### See also

- [CombinationComponents](#combinationcomponents)

### CompoundCombination.get_components_from_csv

[Show source in compound_combination.py:955](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L955)

Parse a CSV-compatible dictionary into compound component values.

#### Arguments

- [Data](../data/index.md#data) *dict* - A CSV-compatible dictionary representation of a CompoundCombination.

#### Returns

- `dict` - Parsed component values keyed by component name.

#### Examples

```python
>>> data = {'numbers_1': 1, 'numbers_2': 2, 'extra_1': 6}
>>> CompoundCombination.get_components_from_csv(data)
{'numbers': [1, 2], 'extra': [6]}
```

#### Signature

```python
@staticmethod
def get_components_from_csv(data: dict) -> dict: ...
```

### CompoundCombination.get_components_from_string

[Show source in compound_combination.py:935](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L935)

Parse a string representation into compound component values.

#### Arguments

- [Data](../data/index.md#data) *str* - A string representation of a CompoundCombination.

#### Returns

- `dict` - Parsed component values keyed by component name.

#### Examples

```python
>>> data = 'numbers: [1, 2, 3, 4, 5]  extra: [6, 7, 8]'
>>> CompoundCombination.get_components_from_string(data)
{'numbers': [1, 2, 3, 4, 5], 'extra': [6, 7, 8]}
```

#### Signature

```python
@staticmethod
def get_components_from_string(data: str) -> dict: ...
```

### CompoundCombination().get_values

[Show source in compound_combination.py:446](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L446)

Get the values for a specific component of the combination.

#### Arguments

- `name` *str* - The name of the component.

#### Returns

- `CombinationValues` - The values for the specified component.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> compound_comb.get_values('main')
[1, 2, 3, 4, 5]
>>> compound_comb.get_values('bonus')
[6]
>>> compound_comb.get_values('extra')
[]
```

#### Signature

```python
def get_values(self, name: str) -> CombinationValues: ...
```

### CompoundCombination().get_winning_rank

[Show source in compound_combination.py:475](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L475)

Get the winning rank of the combination against a winning combination.

#### Arguments

combination (CombinationInput | CompoundCombination | None): The winning combination
    to compare against.
**components (CombinationInputOrRank | CompoundCombination): The components of the
    winning combination.

#### Returns

int | None: The winning rank, or None if not a winning combination.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number,
...     winning_ranks=winning_ranks
... )
>>> winning_comb = compound_comb.get_combination(main=[1, 2, 3, 4, 5], bonus=[6])
>>> compound_comb.get_winning_rank(winning_comb)
1
>>> winning_comb = compound_comb.get_combination(main=[1, 2, 3, 4, 5], bonus=[7])
>>> compound_comb.get_winning_rank(winning_comb)
2
```

#### Signature

```python
def get_winning_rank(
    self,
    combination: CombinationInput | CompoundCombination | None = None,
    **components: CombinationInputOrRank | CompoundCombination
) -> int | None: ...
```

### CompoundCombination().includes

[Show source in compound_combination.py:565](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L565)

Check if the combination includes another combination.

#### Arguments

combination (CombinationInput | CompoundCombination | None): The other combination to
    compare against.
**components (CombinationInputOrRank | CompoundCombination): The components of the
    other combination.

#### Returns

- `bool` - True if includes, False otherwise.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers1 = Combination([1, 2, 3, 4, 5])
>>> bonus_number1 = Combination([6])
>>> compound_comb1 = CompoundCombination(
...     main=main_numbers1,
...     bonus=bonus_number1
... )
>>> main_numbers2 = Combination([1, 2, 3])
>>> bonus_number2 = Combination([6])
>>> compound_comb2 = CompoundCombination(
...     main=main_numbers2,
...     bonus=bonus_number2
... )
>>> compound_comb1.includes(compound_comb2)
True
```

#### Signature

```python
def includes(
    self,
    combination: CombinationInput | CompoundCombination | None = None,
    **components: CombinationInputOrRank | CompoundCombination
) -> bool: ...
```

### CompoundCombination().intersection

[Show source in compound_combination.py:656](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L656)

Get the intersection with another combination.

#### Arguments

combination (CombinationInput | CompoundCombination | None): The other combination to
    compare against.
**components (CombinationInputOrRank | CompoundCombination): The components of the
    other combination.

#### Returns

- [CompoundCombination](#compoundcombination) - The intersection combination.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers1 = Combination([1, 2, 3, 4, 5])
>>> bonus_number1 = Combination([6])
>>> compound_comb1 = CompoundCombination(
...     main=main_numbers1,
...     bonus=bonus_number1
... )
>>> main_numbers2 = Combination([4, 5, 6])
>>> bonus_number2 = Combination([7])
>>> compound_comb2 = CompoundCombination(
...     main=main_numbers2,
...     bonus=bonus_number2
... )
>>> intersection_comb = compound_comb1.intersection(compound_comb2)
>>> intersection_comb.values
[4, 5]
```

#### Signature

```python
def intersection(
    self,
    combination: CombinationInput | CompoundCombination | None = None,
    **components: CombinationInputOrRank | CompoundCombination
) -> CompoundCombination: ...
```

### CompoundCombination().intersects

[Show source in compound_combination.py:610](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L610)

Check if the combination intersects with another combination.

#### Arguments

combination (CombinationInput | CompoundCombination | None): The other combination to
    compare against.
**components (CombinationInputOrRank | CompoundCombination): The components of the
    other combination.

#### Returns

- `bool` - True if intersects, False otherwise.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers1 = Combination([1, 2, 3, 4, 5])
>>> bonus_number1 = Combination([6])
>>> compound_comb1 = CompoundCombination(
...     main=main_numbers1,
...     bonus=bonus_number1
... )
>>> main_numbers2 = Combination([4, 5, 6])
>>> bonus_number2 = Combination([6])
>>> compound_comb2 = CompoundCombination(
...     main=main_numbers2,
...     bonus=bonus_number2
... )
>>> compound_comb1.intersects(compound_comb2)
True
```

#### Signature

```python
def intersects(
    self,
    combination: CombinationInput | CompoundCombination | None = None,
    **components: CombinationInputOrRank | CompoundCombination
) -> bool: ...
```

### CompoundCombination().length

[Show source in compound_combination.py:146](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L146)

Get the total length of the combination.

#### Returns

- `int` - The total length of the combination.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> compound_comb.length
6
```

#### Signature

```python
@cached_property
def length(self) -> int: ...
```

### CompoundCombination().max_winning_rank

[Show source in compound_combination.py:218](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L218)

Get the maximum winning rank.

#### Returns

int | None: The maximum winning rank, or None if there are no winning ranks.

#### Examples

```python
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> compound_comb = CompoundCombination(winning_ranks=winning_ranks)
>>> compound_comb.max_winning_rank
4
>>> CompoundCombination().max_winning_rank
None
```

#### Signature

```python
@property
def max_winning_rank(self) -> int | None: ...
```

### CompoundCombination().min_winning_rank

[Show source in compound_combination.py:199](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L199)

Get the minimum winning rank.

#### Returns

int | None: The minimum winning rank, or None if there are no winning ranks.

#### Examples

```python
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> compound_comb = CompoundCombination(winning_ranks=winning_ranks)
>>> compound_comb.min_winning_rank
1
>>> CompoundCombination().min_winning_rank
None
```

#### Signature

```python
@property
def min_winning_rank(self) -> int | None: ...
```

### CompoundCombination().nb_winning_ranks

[Show source in compound_combination.py:180](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L180)

Get the number of winning ranks.

#### Returns

- `int` - The number of winning ranks.

#### Examples

```python
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> compound_comb = CompoundCombination(winning_ranks=winning_ranks)
>>> compound_comb.nb_winning_ranks
4
```

#### Signature

```python
@property
def nb_winning_ranks(self) -> int: ...
```

### CompoundCombination().similarity

[Show source in compound_combination.py:752](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L752)

Calculate the similarity with another combination.

#### Arguments

combination (CombinationInput | CompoundCombination | None): The other combination to
    compare against.
**components (CombinationInputOrRank | CompoundCombination): The components of the
    other combination.

#### Returns

- `float` - Similarity ratio between 0 and 1.

#### Raises

- `KeyError` - If a component name does not exist in the current combination.

#### Examples

```python
>>> main_numbers1 = Combination([1, 2, 3, 4, 5])
>>> bonus_number1 = Combination([6])
>>> compound_comb1 = CompoundCombination(
...     main=main_numbers1,
...     bonus=bonus_number1
... )
>>> main_numbers2 = Combination([1, 2, 3, 6, 7])
>>> bonus_number2 = Combination([8])
>>> compound_comb2 = CompoundCombination(
...     main=main_numbers2,
...     bonus=bonus_number2
... )
>>> compound_comb1.similarity(compound_comb2)
0.5
```

#### Signature

```python
def similarity(
    self,
    combination: CombinationInput | CompoundCombination | None = None,
    **components: CombinationInputOrRank | CompoundCombination
) -> float: ...
```

### CompoundCombination().to_csv

[Show source in compound_combination.py:854](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L854)

Convert the CompoundCombination to a CSV-serializable dictionary.

#### Returns

- `dict` - A CSV-serializable dictionary representation of the CompoundCombination.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> compound_comb.to_csv()
{'main_1': 1, 'main_2': 2, 'main_3': 3, 'main_4': 4, 'main_5': 5, 'bonus_1': 6}
```

#### Signature

```python
def to_csv(self) -> dict: ...
```

### CompoundCombination().to_dict

[Show source in compound_combination.py:904](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L904)

Convert the CompoundCombination to a dictionary.

#### Returns

- `dict` - A dictionary representation of the CompoundCombination.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number,
...     winning_ranks=winning_ranks
... )
>>> compound_comb.to_dict()
{
    'components': {
        'main': {'values': [1, 2, 3, 4, 5], 'rank': None, 'start': 1},
        'bonus': {'values': [6], 'rank': None, 'start': 1}
    },
    'winning_ranks': {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
}
```

#### Signature

```python
def to_dict(self) -> dict: ...
```

### CompoundCombination().to_json

[Show source in compound_combination.py:878](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L878)

Convert the CompoundCombination to a JSON-serializable dictionary.

#### Returns

- `dict` - A JSON-serializable dictionary representation of the CompoundCombination.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number,
...     winning_ranks=winning_ranks
... )
>>> compound_comb.to_json()
{
    'components': {
        'main': {'values': [1, 2, 3, 4, 5], 'rank': None, 'start': 1},
        'bonus': {'values': [6], 'rank': None, 'start': 1}
    },
    'winning_ranks': {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
}
```

#### Signature

```python
def to_json(self) -> dict: ...
```

### CompoundCombination().to_string

[Show source in compound_combination.py:836](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L836)

Convert the CompoundCombination to a string representation.

#### Returns

- `str` - A string representation of the CompoundCombination.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> compound_comb.to_string()
'main: [1, 2, 3, 4, 5]  bonus: [6]'
```

#### Signature

```python
def to_string(self) -> str: ...
```

### CompoundCombination().values

[Show source in compound_combination.py:127](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L127)

Get all numbers in the combination.

#### Returns

- `CombinationValues` - The list of all numbers in the combination.

#### Examples

```python
>>> main_numbers = Combination([1, 2, 3, 4, 5])
>>> bonus_number = Combination([6])
>>> compound_comb = CompoundCombination(
...     main=main_numbers,
...     bonus=bonus_number
... )
>>> compound_comb.values
[1, 2, 3, 4, 5, 6]
```

#### Signature

```python
@cached_property
def values(self) -> CombinationValues: ...
```

### CompoundCombination().winning_ranks

[Show source in compound_combination.py:165](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/compound_combination.py#L165)

Get the winning ranks mapping.

#### Returns

- [CombinationWinningRanks](#compoundcombination) - The winning ranks mapping.

#### Examples

```python
>>> winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
>>> compound_comb = CompoundCombination(winning_ranks=winning_ranks)
>>> compound_comb.winning_ranks
{(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}
```

#### Signature

```python
@property
def winning_ranks(self) -> CombinationWinningRanks: ...
```

#### See also

- [CombinationWinningRanks](#combinationwinningranks)