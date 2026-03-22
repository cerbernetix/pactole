# Combination

[Pactole Index](../README.md#pactole-index) / [Combinations](./index.md#combinations) / Combination

> Auto-generated documentation for [combinations.combination](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py) module.

- [Combination](#combination)
  - [BoundCombination](#boundcombination)
    - [BoundCombination().combinations](#boundcombination()combinations)
    - [BoundCombination().copy](#boundcombination()copy)
    - [BoundCombination().count](#boundcombination()count)
    - [BoundCombination().end](#boundcombination()end)
    - [BoundCombination.from_dict](#boundcombinationfrom_dict)
    - [BoundCombination().generate](#boundcombination()generate)
    - [BoundCombination().to_dict](#boundcombination()to_dict)
    - [BoundCombination().to_string](#boundcombination()to_string)
  - [Combination](#combination-1)
    - [Combination().compares](#combination()compares)
    - [Combination().copy](#combination()copy)
    - [Combination().equals](#combination()equals)
    - [Combination.from_csv](#combinationfrom_csv)
    - [Combination.from_dict](#combinationfrom_dict)
    - [Combination.from_json](#combinationfrom_json)
    - [Combination.from_string](#combinationfrom_string)
    - [Combination().get_values](#combination()get_values)
    - [Combination().includes](#combination()includes)
    - [Combination().intersection](#combination()intersection)
    - [Combination().intersects](#combination()intersects)
    - [Combination().length](#combination()length)
    - [Combination().rank](#combination()rank)
    - [Combination().similarity](#combination()similarity)
    - [Combination().start](#combination()start)
    - [Combination().stored_rank](#combination()stored_rank)
    - [Combination().to_csv](#combination()to_csv)
    - [Combination().to_dict](#combination()to_dict)
    - [Combination().to_json](#combination()to_json)
    - [Combination().to_string](#combination()to_string)
    - [Combination().values](#combination()values)
  - [CombinationInputWithRank](#combinationinputwithrank)
  - [generate](#generate)
  - [get_combination_from_rank](#get_combination_from_rank)
  - [get_combination_rank](#get_combination_rank)

## BoundCombination

[Show source in combination.py:748](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L748)

A class representing a bound combination of values.

#### Arguments

values (CombinationInputOrRank | None): The values of the combination.
    If an integer is provided, it is treated as the lexicographic rank of the combination.
rank (CombinationRank | None, optional): The lexicographic rank of the combination.
    If not provided, it will be calculated on demand from the values. Defaults to None.
start (int | None): The start value of the combination range. Defaults to DEFAULT_START.
end (int | None): The end value of the combination range. Defaults to DEFAULT_END.
count (int | None): The count of numbers in the combination. Defaults to DEFAULT_COUNT.
combinations (int | None): The total number of possible combinations. If not provided,
    it is calculated based on the start, end, and count.

#### Examples

```python
>>> bound_comb = BoundCombination(values=10, start=1, end=50, count=5)
>>> bound_comb.values
[2, 3, 4, 5, 7]
>>> bound_comb.end
50
>>> bound_comb.count
5
>>> bound_comb.combinations
2118760
```

#### Signature

```python
class BoundCombination(Combination):
    def __init__(
        self,
        values: CombinationInputOrRank | None = None,
        rank: CombinationRank | None = None,
        start: int | None = None,
        end: int | None = None,
        count: int | None = None,
        combinations: int | None = None,
    ) -> None: ...
```

#### See also

- [Combination](#combination)

### BoundCombination().combinations

[Show source in combination.py:847](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L847)

Return the total number of possible combinations.

#### Returns

- `int` - The total number of combinations.

#### Examples

```python
>>> bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)
>>> bound_comb.combinations
2118760
```

#### Signature

```python
@property
def combinations(self) -> int: ...
```

### BoundCombination().copy

[Show source in combination.py:885](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L885)

Return a copy of the BoundCombination with optional modifications.

#### Arguments

values (CombinationInputOrRank | None): The values of the combination.
    If an integer is provided, it is treated as the lexicographic rank of the
    combination. If None, the current values are used. Defaults to None.
rank (CombinationRank | None, optional): The lexicographic rank of the combination. If
    not provided, it will be calculated on demand from the values. Defaults to None.
start (int | None): The start value of the combination range. If None, the current start
    is used. Defaults to None.
end (int | None): The end value of the combination range. If None, the current end is
    used. Defaults to None.
count (int | None): The count of numbers in the combination. If None, the current count
    is used. Defaults to None.
combinations (int | None): The total number of possible combinations. If None, the
    current combinations are used. Defaults to None.

#### Returns

- [BoundCombination](#boundcombination) - A new BoundCombination instance with the specified modifications.

#### Examples

```python
>>> bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)
>>> new_comb = bound_comb.copy(values=15)
>>> new_comb.values
 [1, 2, 5, 6, 7]
```

#### Signature

```python
def copy(
    self,
    values: CombinationInputOrRank | None = None,
    rank: CombinationRank | None = None,
    start: int | None = None,
    end: int | None = None,
    count: int | None = None,
    combinations: int | None = None,
) -> BoundCombination: ...
```

### BoundCombination().count

[Show source in combination.py:833](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L833)

Return the count of numbers in the combination.

#### Returns

- `int` - The count of numbers.

#### Examples

```python
>>> bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)
>>> bound_comb.count
5
```

#### Signature

```python
@property
def count(self) -> int: ...
```

### BoundCombination().end

[Show source in combination.py:819](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L819)

Return the end value of the combination range.

#### Returns

- `int` - The end value.

#### Examples

```python
>>> bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)
>>> bound_comb.end
50
```

#### Signature

```python
@property
def end(self) -> int: ...
```

### BoundCombination.from_dict

[Show source in combination.py:986](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L986)

Create a BoundCombination instance from a dictionary.

#### Arguments

- [Data](../data/index.md#data) *dict* - A dictionary containing the keys 'values', 'rank', 'start', 'end', 'count',
    and 'combinations'.

#### Returns

- [BoundCombination](#boundcombination) - A new BoundCombination instance created from the dictionary data.

#### Examples

```python
>>> data = {
...     'values': [1, 2, 3],
...     'rank': 0,
...     'start': 1,
...     'end': 50,
...     'count': 5,
...     'combinations': 2118760
... }
>>> bound_comb = BoundCombination.from_dict(data)
>>> bound_comb.values
[1, 2, 3]
>>> bound_comb.rank
0
>>> bound_comb.start
1
>>> bound_comb.end
50
>>> bound_comb.count
5
>>> bound_comb.combinations
2118760
```

#### Signature

```python
@staticmethod
def from_dict(data: dict) -> BoundCombination: ...
```

### BoundCombination().generate

[Show source in combination.py:861](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L861)

Generate a list of random combinations within the bounds.

#### Arguments

- `n` *int* - The number of combinations to generate. Defaults to 1.
- `partitions` *int* - The number of partitions to divide the range into for generation.
    Defaults to 1.

#### Returns

- `list[BoundCombination]` - A list of randomly generated combinations.

#### Examples

```python
>>> bound_comb = BoundCombination(start=1, end=50, count=5)
>>> random_combs = bound_comb.generate()
>>> len(random_combs)
1
>>> random_combs[0].values
[3, 15, 22, 34, 45]
```

#### Signature

```python
def generate(self, n: int = 1, partitions: int = 1) -> list[BoundCombination]: ...
```

### BoundCombination().to_dict

[Show source in combination.py:959](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L959)

Convert the BoundCombination instance to a dictionary.

#### Returns

- `dict` - A dictionary representation of the BoundCombination instance.

#### Examples

```python
>>> bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)
>>> bound_comb.to_dict()
{
    'values': [1, 2, 3],
    'rank': 0,
    'start': 1,
    'end': 50,
    'count': 5,
    'combinations': 2118760
}
```

#### Signature

```python
def to_dict(self) -> dict: ...
```

### BoundCombination().to_string

[Show source in combination.py:946](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L946)

Convert the Combination instance to a string representation.

#### Returns

- `str` - A string representation of the combination values.

#### Examples

```python
>>> combination = Combination([3, 1, 2], rank=123)
>>> combination.to_string()
'values: [1,2,3]  rank: 123'
```

#### Signature

```python
def to_string(self) -> str: ...
```



## Combination

[Show source in combination.py:168](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L168)

A class representing a combination of values.

#### Arguments

values (CombinationInputValues | CombinationInputWithRank | None, optional): The values of
    the combination. Defaults to None.
rank (CombinationRank | None, optional): The lexicographic rank of the combination.
    If not provided, it will be calculated on demand from the values. Defaults to None.
- `start` *int, optional* - The starting offset for the combination values.
    Defaults to DEFAULT_START.

#### Raises

- `ValueError` - If the provided rank is negative or if the values are not valid.

#### Examples

```python
>>> combination = Combination([12, 3, 42, 6, 22])
>>> combination.values
[3, 6, 12, 22, 42]
>>> combination.rank
755560
>>> combination.length
5
>>> combination.start
1
```

#### Signature

```python
class Combination:
    def __init__(
        self,
        values: CombinationInputValues | CombinationInputWithRank | None = None,
        rank: CombinationRank | None = None,
        start: int | None = None,
    ) -> None: ...
```

### Combination().compares

[Show source in combination.py:485](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L485)

Compare the combination with another combination or lexicographic rank.

#### Arguments

- `combination` *CombinationInput* - The combination or lexicographic rank to compare with.

#### Returns

- `int` - -1 if self < combination, 0 if self == combination, 1 if self > combination.

#### Examples

```python
>>> combination1 = Combination([1, 2, 3])
>>> combination2 = Combination([1, 2, 4])
>>> combination1.compares(combination2)
-1
>>> combination2.compares(combination1)
1
>>> combination1.compares([1, 2, 3])
0
```

#### Signature

```python
def compares(self, combination: CombinationInput) -> int: ...
```

#### See also

- [CombinationInput](#combinationinput)

### Combination().copy

[Show source in combination.py:311](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L311)

Return a copy of the Combination with optional modifications.

#### Arguments

values (CombinationInputOrRank | None): The values of the combination.
    If an integer is provided, it is treated as the lexicographic rank of the
    combination. If None, the current values are used. Defaults to None.
rank (CombinationRank | None, optional): The lexicographic rank of the combination.
    If not provided, it will be calculated on demand from the values.
    Defaults to None.
start (int | None): The starting offset for the combination values.
    If None, the current start is used. Defaults to None.

#### Returns

- [Combination](#combination) - A new Combination instance with the specified modifications.

#### Examples

```python
>>> combination = Combination([4, 5, 6], start=1)
>>> new_comb = combination.copy(values=[2, 3, 4])
>>> new_comb.values
[2, 3, 4]
>>> new_comb.start
1
>>> new_comb = combination.copy(start=2)
>>> new_comb.values
[5, 6, 7]
>>> new_comb.start
2
```

#### Signature

```python
def copy(
    self,
    values: CombinationInputOrRank | None = None,
    rank: CombinationRank | None = None,
    start: int | None = None,
) -> Combination: ...
```

### Combination().equals

[Show source in combination.py:370](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L370)

Check if the combination is equal to another combination or lexicographic rank.

#### Arguments

- `combination` *CombinationInput* - The combination or lexicographic rank to compare with.

#### Returns

- `bool` - True if the combinations are equal, False otherwise.

#### Examples

```python
>>> combination1 = Combination([1, 2, 3])
>>> combination2 = Combination([3, 2, 1])
>>> combination1.equals(combination2)
True
>>> combination1.equals([1, 2, 4])
False
>>> rank = get_combination_rank([1, 2, 3], offset=1)
>>> combination1.equals(rank)
True
>>> combination1.equals(rank + 1)
False
```

#### Signature

```python
def equals(self, combination: CombinationInput) -> bool: ...
```

#### See also

- [CombinationInput](#combinationinput)

### Combination.from_csv

[Show source in combination.py:633](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L633)

Create a Combination instance from CSV data.

#### Arguments

- [Data](../data/index.md#data) *CombinationValues* - A list of combination values from CSV.

#### Returns

- [Combination](#combination) - A new Combination instance created from the CSV data.

#### Examples

```python
>>> data = [1, 2, 3]
>>> combination = Combination.from_csv(data)
>>> combination.values
[1, 2, 3]
```

#### Signature

```python
@classmethod
def from_csv(cls, data: CombinationValues) -> Combination: ...
```

#### See also

- [CombinationValues](#combinationvalues)

### Combination.from_dict

[Show source in combination.py:671](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L671)

Create a Combination instance from a dictionary.

#### Arguments

- [Data](../data/index.md#data) *dict* - A dictionary containing the keys 'values', 'rank', and 'start'.

#### Returns

- [Combination](#combination) - A new Combination instance created from the dictionary data.

#### Examples

```python
>>> data = {'values': [1, 2, 3], 'rank': 0, 'start': 0}
>>> combination = Combination.from_dict(data)
>>> combination.values
[1, 2, 3]
>>> combination.rank
0
>>> combination.start
0
```

#### Signature

```python
@staticmethod
def from_dict(data: dict) -> Combination: ...
```

### Combination.from_json

[Show source in combination.py:651](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L651)

Create a Combination instance from JSON data.

#### Arguments

data (CombinationValues | dict): A list of combination values or a dictionary from JSON.

#### Returns

- [Combination](#combination) - A new Combination instance created from the JSON data.

#### Examples

```python
>>> data = [1, 2, 3]
>>> combination = Combination.from_json(data)
>>> combination.values
[1, 2, 3]
```

#### Signature

```python
@classmethod
def from_json(cls, data: CombinationValues | dict) -> Combination: ...
```

### Combination.from_string

[Show source in combination.py:599](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L599)

Create a Combination instance from a string representation.

#### Arguments

- [Data](../data/index.md#data) *str* - A string representation of the combination, expected in the
    - `format` *'values* - [1,2,3]  rank: 123'.

#### Returns

- [Combination](#combination) - A new Combination instance created from the string data.

#### Examples

```python
>>> data = 'values: [1,2,3]  rank: 123'
>>> combination = Combination.from_string(data)
>>> combination.values
[1, 2, 3]
>>> combination.rank
123
```

#### Signature

```python
@classmethod
def from_string(cls, data: str) -> Combination: ...
```

### Combination().get_values

[Show source in combination.py:355](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L355)

Get the values of the combination as a sorted list with an optional new start offset.

#### Arguments

- [Combination().start](#combinationstart) *int, optional* - The new starting offset for the values. Defaults to None.

#### Returns

- [CombinationValues](#combination) - The sorted list of combination values with the new offset.

#### Signature

```python
def get_values(self, start: int | None = None) -> CombinationValues: ...
```

#### See also

- [CombinationValues](#combinationvalues)

### Combination().includes

[Show source in combination.py:403](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L403)

Check if the combination includes another combination.

#### Arguments

combination (CombinationNumber | CombinationInputValues): The combination to check for
    inclusion, or a single number.

#### Returns

- `bool` - True if the combination includes the other combination, False otherwise.

#### Examples

```python
>>> combination1 = Combination([2, 4, 6])
>>> combination2 = Combination([2, 4])
>>> combination1.includes(combination2)
True
>>> combination1.includes([2, 5])
False
```

#### Signature

```python
def includes(self, combination: CombinationNumber | CombinationInputValues) -> bool: ...
```

### Combination().intersection

[Show source in combination.py:458](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L458)

Get the intersection of the combination with another combination.

#### Arguments

combination (CombinationInputValues | Combination): The combination to intersect with.

#### Returns

- [Combination](#combination) - The intersection of the two combinations.

#### Examples

```python
>>> combination1 = Combination([1, 2, 3])
>>> combination2 = Combination([3, 4, 5])
>>> intersection = combination1.intersection(combination2)
>>> intersection.values
[3]
>>> intersection2 = combination1.intersection([4, 5, 6])
>>> intersection2.values
[]
```

#### Signature

```python
def intersection(self, combination: CombinationInputValues) -> Combination: ...
```

#### See also

- [CombinationInputValues](#combinationinputvalues)

### Combination().intersects

[Show source in combination.py:432](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L432)

Check if the combination intersects with another combination.

#### Arguments

combination (CombinationInputValues | Combination): The combination to check for
    intersection.

#### Returns

- `bool` - True if the combination intersects with the other combination, False otherwise.

#### Examples

```python
>>> combination1 = Combination([1, 2, 3])
>>> combination2 = Combination([3, 4, 5])
>>> combination1.intersects(combination2)
True
>>> combination1.intersects([4, 5, 6])
False
```

#### Signature

```python
def intersects(self, combination: CombinationInputValues | Combination) -> bool: ...
```

### Combination().length

[Show source in combination.py:280](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L280)

Get the length of the combination.

#### Returns

- `int` - The length of the combination.

#### Examples

```python
>>> combination = Combination([3, 1, 2])
>>> combination.length
3
```

#### Signature

```python
@cached_property
def length(self) -> int: ...
```

### Combination().rank

[Show source in combination.py:246](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L246)

Get the lexicographic rank of the combination.

#### Returns

- [CombinationRank](#combination) - The lexicographic rank of the combination.

#### Examples

```python
>>> combination = Combination([3, 1, 2])
>>> combination.rank
0
```

#### Signature

```python
@property
def rank(self) -> CombinationRank: ...
```

#### See also

- [CombinationRank](#combinationrank)

### Combination().similarity

[Show source in combination.py:522](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L522)

Calculate the similarity between the combination and another combination.

#### Arguments

- `combination` *CombinationInputValues* - The combination to compare with.

#### Returns

- `float` - The similarity ratio between the two combinations.

#### Examples

```python
>>> combination1 = Combination([1, 2, 3])
>>> combination2 = Combination([2, 3, 4])
>>> combination1.similarity(combination2)
0.6666666666666666
>>> combination1.similarity([4, 5, 6])
0.0
```

#### Signature

```python
def similarity(self, combination: CombinationInputValues) -> float: ...
```

#### See also

- [CombinationInputValues](#combinationinputvalues)

### Combination().start

[Show source in combination.py:294](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L294)

Get the starting offset of the combination.

#### Returns

- `int` - The starting offset of the combination.

#### Examples

```python
>>> combination = Combination([3, 1, 2], start=0)
>>> combination.start
0
>>> combination = Combination([3, 1, 2])
>>> combination.start
1
```

#### Signature

```python
@property
def start(self) -> int: ...
```

### Combination().stored_rank

[Show source in combination.py:262](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L262)

Get the stored lexicographic rank of the combination without calculating it.

#### Returns

CombinationRank | None: The stored lexicographic rank of the combination, or None if
    it has not been calculated yet.

#### Examples

```python
>>> combination = Combination([3, 1, 2])
>>> combination.stored_rank
None
>>> _ = combination.rank  # Calculate the rank
>>> combination.stored_rank
0
```

#### Signature

```python
@property
def stored_rank(self) -> CombinationRank | None: ...
```

### Combination().to_csv

[Show source in combination.py:560](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L560)

Convert the Combination instance to a format suitable for CSV export.

#### Returns

- [CombinationValues](#combination) - A list of combination values suitable for CSV export.

#### Examples

```python
>>> combination = Combination([3, 1, 2])
>>> combination.to_csv()
[1, 2, 3]
```

#### Signature

```python
def to_csv(self) -> CombinationValues: ...
```

#### See also

- [CombinationValues](#combinationvalues)

### Combination().to_dict

[Show source in combination.py:586](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L586)

Convert the Combination instance to a dictionary.

#### Returns

- `dict` - A dictionary representation of the Combination instance.

#### Examples

```python
>>> combination = Combination([3, 1, 2], start=0)
>>> combination.to_dict()
{'values': [1, 2, 3], 'rank': 0, 'start': 0}
```

#### Signature

```python
def to_dict(self) -> dict: ...
```

### Combination().to_json

[Show source in combination.py:573](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L573)

Convert the Combination instance to a JSON-serializable format.

#### Returns

- [CombinationValues](#combination) - A list of combination values suitable for JSON serialization.

#### Examples

```python
>>> combination = Combination([3, 1, 2])
>>> combination.to_json()
[1, 2, 3]
```

#### Signature

```python
def to_json(self) -> CombinationValues: ...
```

#### See also

- [CombinationValues](#combinationvalues)

### Combination().to_string

[Show source in combination.py:547](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L547)

Convert the Combination instance to a string representation.

#### Returns

- `str` - A string representation of the combination values.

#### Examples

```python
>>> combination = Combination([3, 1, 2], rank=123)
>>> combination.to_string()
'values: [1,2,3]  rank: 123'
```

#### Signature

```python
def to_string(self) -> str: ...
```

### Combination().values

[Show source in combination.py:232](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L232)

Get the values of the combination as a sorted list.

#### Returns

- [CombinationValues](#combination) - The sorted list of values in the combination.

#### Examples

```python
>>> combination = Combination([3, 1, 2])
>>> combination.values
[1, 2, 3]
```

#### Signature

```python
@cached_property
def values(self) -> CombinationValues: ...
```

#### See also

- [CombinationValues](#combinationvalues)



## CombinationInputWithRank

[Show source in combination.py:736](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L736)

Type representing a combination input along with its lexicographic rank.

#### Signature

```python
class CombinationInputWithRank(TypedDict): ...
```



## generate

[Show source in combination.py:139](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L139)

Generate a list of random combination ranks within a given range.

#### Arguments

- [Combinations](./index.md#combinations) *int* - The total number of possible combinations.
- `n` *int* - The number of combinations to generate. Defaults to 1.
- `partitions` *int* - The number of partitions to divide the range into for generation.
    Defaults to 1.

#### Yields

- `int` - A randomly generated combination rank.

#### Examples

```python
>>> list(generate(10, n=3))
[2, 5, 7]
>>> list(generate(100, n=5, partitions=2))
[10, 20, 30, 40, 50]
```

#### Signature

```python
def generate(combinations: int, n: int = 1, partitions: int = 1) -> Iterator[int]: ...
```



## get_combination_from_rank

[Show source in combination.py:81](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L81)

Get the combination corresponding to a given lexicographic rank.

Values are returned sorted, and `offset` is added to each value in the resulting combination.

#### Arguments

- `rank` *int* - The lexicographic rank of the combination.
- `length` *int, optional* - The length of the combination. Defaults to 2.
- `offset` *int, optional* - An offset to apply to each value in the combination. Defaults to 0.

#### Returns

- `list[int]` - The combination corresponding to the lexicographic rank.

#### Raises

- `ValueError` - If the rank or length is negative.

#### Examples

```python
>>> get_combination_from_rank(0, 3)
[0, 1, 2]
>>> get_combination_from_rank(2, 3)
[0, 2, 3]
>>> get_combination_from_rank(0, 3, offset=1)
[1, 2, 3]
```

#### Signature

```python
def get_combination_from_rank(
    rank: int, length: int = 2, offset: int = 0
) -> list[int]: ...
```



## get_combination_rank

[Show source in combination.py:48](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L48)

Get the lexicographic rank of a given combination.

Values are sorted before computing rank, and `offset` is subtracted from each value during
ranking.

#### Arguments

- `combination` *Iterable[int]* - The combination to get the lexicographic rank for.
- `offset` *int, optional* - An offset to apply to each value in the combination. Defaults to 0.

#### Returns

- `int` - The lexicographic rank of the combination.

#### Examples

```python
>>> get_combination_rank([0, 1, 2])
0
>>> get_combination_rank([0, 2, 3])
2
>>> get_combination_rank([1, 2, 3], offset=1)
0
```

#### Signature

```python
def get_combination_rank(combination: Iterable[int], offset: int = 0) -> int: ...
```