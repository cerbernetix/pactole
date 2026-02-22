# Combination

[Pactole Index](../README.md#pactole-index) / [Combinations](./index.md#combinations) / Combination

> Auto-generated documentation for [combinations.combination](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py) module.

- [Combination](#combination)
  - [BoundCombination](#boundcombination)
    - [BoundCombination().combinations](#boundcombination()combinations)
    - [BoundCombination().copy](#boundcombination()copy)
    - [BoundCombination().count](#boundcombination()count)
    - [BoundCombination().end](#boundcombination()end)
    - [BoundCombination().generate](#boundcombination()generate)
  - [Combination](#combination-1)
    - [Combination().compares](#combination()compares)
    - [Combination().copy](#combination()copy)
    - [Combination().equals](#combination()equals)
    - [Combination().get_values](#combination()get_values)
    - [Combination().includes](#combination()includes)
    - [Combination().intersection](#combination()intersection)
    - [Combination().intersects](#combination()intersects)
    - [Combination().length](#combination()length)
    - [Combination().rank](#combination()rank)
    - [Combination().similarity](#combination()similarity)
    - [Combination().start](#combination()start)
    - [Combination().values](#combination()values)
  - [CombinationInputWithRank](#combinationinputwithrank)
  - [get_combination_from_rank](#get_combination_from_rank)
  - [get_combination_rank](#get_combination_rank)

## BoundCombination

[Show source in combination.py:531](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L531)

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

[Show source in combination.py:630](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L630)

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

[Show source in combination.py:678](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L678)

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

[Show source in combination.py:616](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L616)

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

[Show source in combination.py:602](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L602)

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

### BoundCombination().generate

[Show source in combination.py:644](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L644)

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



## Combination

[Show source in combination.py:131](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L131)

A class representing a combination of values.

#### Arguments

values (CombinationInputValues | CombinationInputWithRank | None, optional): The values of
    the combination. Defaults to None.
rank (CombinationRank | None, optional): The lexicographic rank of the combination.
    If not provided, it will be calculated on demand from the values. Defaults to None.
- `start` *int, optional* - The starting offset for the combination values.
    Defaults to DEFAULT_START.

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

[Show source in combination.py:417](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L417)

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

[Show source in combination.py:246](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L246)

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

[Show source in combination.py:302](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L302)

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

### Combination().get_values

[Show source in combination.py:287](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L287)

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

[Show source in combination.py:335](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L335)

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

[Show source in combination.py:390](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L390)

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

[Show source in combination.py:364](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L364)

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

[Show source in combination.py:215](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L215)

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

[Show source in combination.py:199](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L199)

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

[Show source in combination.py:454](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L454)

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

[Show source in combination.py:229](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L229)

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

### Combination().values

[Show source in combination.py:185](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L185)

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

[Show source in combination.py:519](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L519)

Type representing a combination input along with its lexicographic rank.

#### Signature

```python
class CombinationInputWithRank(TypedDict): ...
```



## get_combination_from_rank

[Show source in combination.py:72](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L72)

Get the combination corresponding to a given lexicographic rank.

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

[Show source in combination.py:42](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/combination.py#L42)

Get the lexicographic rank of a given combination.

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