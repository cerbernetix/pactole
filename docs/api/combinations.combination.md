<!-- markdownlint-disable -->

<a href="../../src/pactole/combinations/combination.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `combinations.combination`
Combination module for handling combinations of values and their lexicographic ranks. 

**Global Variables**
---------------
- **DEFAULT_START**
- **DEFAULT_END**
- **DEFAULT_COUNT**

---

<a href="../../src/pactole/combinations/combination.py#L42"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_combination_rank`

```python
get_combination_rank(combination: 'Iterable[int]', offset: 'int' = 0) → int
```

Get the lexicographic rank of a given combination. 



**Args:**
 
 - <b>`combination`</b> (Iterable[int]):  The combination to get the lexicographic rank for. 
 - <b>`offset`</b> (int, optional):  An offset to apply to each value in the combination. Defaults to 0. 



**Returns:**
 
 - <b>`int`</b>:  The lexicographic rank of the combination. 



**Examples:**
 ``` get_combination_rank([0, 1, 2])```
    0
    >>> get_combination_rank([0, 2, 3])
    2
    >>> get_combination_rank([1, 2, 3], offset=1)
    0



---

<a href="../../src/pactole/combinations/combination.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_combination_from_rank`

```python
get_combination_from_rank(
    rank: 'int',
    length: 'int' = 2,
    offset: 'int' = 0
) → list[int]
```

Get the combination corresponding to a given lexicographic rank. 



**Args:**
 
 - <b>`rank`</b> (int):  The lexicographic rank of the combination. 
 - <b>`length`</b> (int, optional):  The length of the combination. Defaults to 2. 
 - <b>`offset`</b> (int, optional):  An offset to apply to each value in the combination. Defaults to 0. 



**Returns:**
 
 - <b>`list[int]`</b>:  The combination corresponding to the lexicographic rank. 



**Raises:**
 
 - <b>`ValueError`</b>:  If the rank or length is negative. 



**Examples:**
 ``` get_combination_from_rank(0, 3)```
    [0, 1, 2]
    >>> get_combination_from_rank(2, 3)
    [0, 2, 3]
    >>> get_combination_from_rank(0, 3, offset=1)
    [1, 2, 3]



---

<a href="../../src/pactole/combinations/combination.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Combination`
A class representing a combination of values. 



**Args:**
 
 - <b>`values`</b> (CombinationInputValues | CombinationInputWithRank | None, optional):  The values of  the combination. Defaults to None. 
 - <b>`rank`</b> (CombinationRank | None, optional):  The lexicographic rank of the combination.  If not provided, it will be calculated on demand from the values. Defaults to None. 
 - <b>`start`</b> (int, optional):  The starting offset for the combination values.  Defaults to DEFAULT_START. 



**Examples:**
 ``` combination = Combination([12, 3, 42, 6, 22])```
    >>> combination.values
    [3, 6, 12, 22, 42]
    >>> combination.rank
    755560
    >>> combination.length
    5
    >>> combination.start
    1


<a href="../../src/pactole/combinations/combination.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Combination.__init__`

```python
__init__(
    values: 'CombinationInputValues | CombinationInputWithRank | None' = None,
    rank: 'CombinationRank | None' = None,
    start: 'int | None' = None
) → None
```






---

#### <kbd>property</kbd> Combination.rank

Get the lexicographic rank of the combination. 



**Returns:**
 
 - <b>`CombinationRank`</b>:  The lexicographic rank of the combination. 



**Examples:**
 ``` combination = Combination([3, 1, 2])```
    >>> combination.rank
    0


---

#### <kbd>property</kbd> Combination.start

Get the starting offset of the combination. 



**Returns:**
 
 - <b>`int`</b>:  The starting offset of the combination. 



**Examples:**
 ``` combination = Combination([3, 1, 2], start=0)```
    >>> combination.start
    0
    >>> combination = Combination([3, 1, 2])
    >>> combination.start
    1




---

<a href="../../src/pactole/combinations/combination.py#L417"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Combination.compares`

```python
compares(combination: 'CombinationInput') → int
```

Compare the combination with another combination or lexicographic rank. 



**Args:**
 
 - <b>`combination`</b> (CombinationInput):  The combination or lexicographic rank to compare with. 



**Returns:**
 
 - <b>`int`</b>:  -1 if self < combination, 0 if self == combination, 1 if self > combination. 



**Examples:**
 ``` combination1 = Combination([1, 2, 3])```
    >>> combination2 = Combination([1, 2, 4])
    >>> combination1.compares(combination2)

        -1
    >>> combination2.compares(combination1)
    1
    >>> combination1.compares([1, 2, 3])
    0


---

<a href="../../src/pactole/combinations/combination.py#L246"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Combination.copy`

```python
copy(
    values: 'CombinationInputOrRank | None' = None,
    rank: 'CombinationRank | None' = None,
    start: 'int | None' = None
) → Combination
```

Return a copy of the Combination with optional modifications. 



**Args:**
 
 - <b>`values`</b> (CombinationInputOrRank | None):  The values of the combination.  If an integer is provided, it is treated as the lexicographic rank of the  combination. If None, the current values are used. Defaults to None. 
 - <b>`rank`</b> (CombinationRank | None, optional):  The lexicographic rank of the combination.  If not provided, it will be calculated on demand from the values.  Defaults to None. 
 - <b>`start`</b> (int | None):  The starting offset for the combination values.  If None, the current start is used. Defaults to None. 



**Returns:**
 
 - <b>`Combination`</b>:  A new Combination instance with the specified modifications. 



**Examples:**
 ``` combination = Combination([4, 5, 6], start=1)```
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


---

<a href="../../src/pactole/combinations/combination.py#L302"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Combination.equals`

```python
equals(combination: 'CombinationInput') → bool
```

Check if the combination is equal to another combination or lexicographic rank. 



**Args:**
 
 - <b>`combination`</b> (CombinationInput):  The combination or lexicographic rank to compare with. 



**Returns:**
 
 - <b>`bool`</b>:  True if the combinations are equal, False otherwise. 



**Examples:**
 ``` combination1 = Combination([1, 2, 3])```
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


---

<a href="../../src/pactole/combinations/combination.py#L287"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Combination.get_values`

```python
get_values(start: 'int | None' = None) → CombinationValues
```

Get the values of the combination as a sorted list with an optional new start offset. 



**Args:**
 
 - <b>`start`</b> (int, optional):  The new starting offset for the values. Defaults to None. 



**Returns:**
 
 - <b>`CombinationValues`</b>:  The sorted list of combination values with the new offset. 

---

<a href="../../src/pactole/combinations/combination.py#L335"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Combination.includes`

```python
includes(combination: 'CombinationNumber | CombinationInputValues') → bool
```

Check if the combination includes another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationNumber | CombinationInputValues):  The combination to check for  inclusion, or a single number. 



**Returns:**
 
 - <b>`bool`</b>:  True if the combination includes the other combination, False otherwise. 



**Examples:**
 ``` combination1 = Combination([2, 4, 6])```
    >>> combination2 = Combination([2, 4])
    >>> combination1.includes(combination2)
    True
    >>> combination1.includes([2, 5])
    False


---

<a href="../../src/pactole/combinations/combination.py#L390"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Combination.intersection`

```python
intersection(combination: 'CombinationInputValues') → Combination
```

Get the intersection of the combination with another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInputValues | Combination):  The combination to intersect with. 



**Returns:**
 
 - <b>`Combination`</b>:  The intersection of the two combinations. 



**Examples:**
 ``` combination1 = Combination([1, 2, 3])```
    >>> combination2 = Combination([3, 4, 5])
    >>> intersection = combination1.intersection(combination2)
    >>> intersection.values
    [3]
    >>> intersection2 = combination1.intersection([4, 5, 6])
    >>> intersection2.values
    []


---

<a href="../../src/pactole/combinations/combination.py#L364"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Combination.intersects`

```python
intersects(combination: 'CombinationInputValues | Combination') → bool
```

Check if the combination intersects with another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInputValues | Combination):  The combination to check for  intersection. 



**Returns:**
 
 - <b>`bool`</b>:  True if the combination intersects with the other combination, False otherwise. 



**Examples:**
 ``` combination1 = Combination([1, 2, 3])```
    >>> combination2 = Combination([3, 4, 5])
    >>> combination1.intersects(combination2)
    True
    >>> combination1.intersects([4, 5, 6])
    False


---

<a href="../../src/pactole/combinations/combination.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Combination.similarity`

```python
similarity(combination: 'CombinationInputValues') → float
```

Calculate the similarity between the combination and another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInputValues):  The combination to compare with. 



**Returns:**
 
 - <b>`float`</b>:  The similarity ratio between the two combinations. 



**Examples:**
 ``` combination1 = Combination([1, 2, 3])```
    >>> combination2 = Combination([2, 3, 4])
    >>> combination1.similarity(combination2)
    0.6666666666666666
    >>> combination1.similarity([4, 5, 6])
    0.0



---

<a href="../../src/pactole/combinations/combination.py#L519"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CombinationInputWithRank`
Type representing a combination input along with its lexicographic rank. 





---

<a href="../../src/pactole/combinations/combination.py#L531"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BoundCombination`
A class representing a bound combination of values. 



**Args:**
 
 - <b>`values`</b> (CombinationInputOrRank | None):  The values of the combination.  If an integer is provided, it is treated as the lexicographic rank of the combination. 
 - <b>`rank`</b> (CombinationRank | None, optional):  The lexicographic rank of the combination.  If not provided, it will be calculated on demand from the values. Defaults to None. 
 - <b>`start`</b> (int | None):  The start value of the combination range. Defaults to DEFAULT_START. 
 - <b>`end`</b> (int | None):  The end value of the combination range. Defaults to DEFAULT_END. 
 - <b>`count`</b> (int | None):  The count of numbers in the combination. Defaults to DEFAULT_COUNT. 
 - <b>`combinations`</b> (int | None):  The total number of possible combinations. If not provided,  it is calculated based on the start, end, and count. 



**Examples:**
 ``` bound_comb = BoundCombination(values=10, start=1, end=50, count=5)```
    >>> bound_comb.values
    [2, 3, 4, 5, 7]
    >>> bound_comb.end
    50
    >>> bound_comb.count
    5
    >>> bound_comb.combinations
    2118760


<a href="../../src/pactole/combinations/combination.py#L561"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `BoundCombination.__init__`

```python
__init__(
    values: 'CombinationInputOrRank | None' = None,
    rank: 'CombinationRank | None' = None,
    start: 'int | None' = None,
    end: 'int | None' = None,
    count: 'int | None' = None,
    combinations: 'int | None' = None
) → None
```






---

#### <kbd>property</kbd> BoundCombination.combinations

Return the total number of possible combinations. 



**Returns:**
 
 - <b>`int`</b>:  The total number of combinations. 



**Examples:**
 ``` bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)```
    >>> bound_comb.combinations
    2118760


---

#### <kbd>property</kbd> BoundCombination.count

Return the count of numbers in the combination. 



**Returns:**
 
 - <b>`int`</b>:  The count of numbers. 



**Examples:**
 ``` bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)```
    >>> bound_comb.count
    5


---

#### <kbd>property</kbd> BoundCombination.end

Return the end value of the combination range. 



**Returns:**
 
 - <b>`int`</b>:  The end value. 



**Examples:**
 ``` bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)```
    >>> bound_comb.end
    50


---

#### <kbd>property</kbd> BoundCombination.rank

Get the lexicographic rank of the combination. 



**Returns:**
 
 - <b>`CombinationRank`</b>:  The lexicographic rank of the combination. 



**Examples:**
 ``` combination = Combination([3, 1, 2])```
    >>> combination.rank
    0


---

#### <kbd>property</kbd> BoundCombination.start

Get the starting offset of the combination. 



**Returns:**
 
 - <b>`int`</b>:  The starting offset of the combination. 



**Examples:**
 ``` combination = Combination([3, 1, 2], start=0)```
    >>> combination.start
    0
    >>> combination = Combination([3, 1, 2])
    >>> combination.start
    1




---

<a href="../../src/pactole/combinations/combination.py#L417"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `BoundCombination.compares`

```python
compares(combination: 'CombinationInput') → int
```

Compare the combination with another combination or lexicographic rank. 



**Args:**
 
 - <b>`combination`</b> (CombinationInput):  The combination or lexicographic rank to compare with. 



**Returns:**
 
 - <b>`int`</b>:  -1 if self < combination, 0 if self == combination, 1 if self > combination. 



**Examples:**
 ``` combination1 = Combination([1, 2, 3])```
    >>> combination2 = Combination([1, 2, 4])
    >>> combination1.compares(combination2)

        -1
    >>> combination2.compares(combination1)
    1
    >>> combination1.compares([1, 2, 3])
    0


---

<a href="../../src/pactole/combinations/combination.py#L678"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `BoundCombination.copy`

```python
copy(
    values: 'CombinationInputOrRank | None' = None,
    rank: 'CombinationRank | None' = None,
    start: 'int | None' = None,
    end: 'int | None' = None,
    count: 'int | None' = None,
    combinations: 'int | None' = None
) → BoundCombination
```

Return a copy of the BoundCombination with optional modifications. 



**Args:**
 
 - <b>`values`</b> (CombinationInputOrRank | None):  The values of the combination.  If an integer is provided, it is treated as the lexicographic rank of the  combination. If None, the current values are used. Defaults to None. 
 - <b>`rank`</b> (CombinationRank | None, optional):  The lexicographic rank of the combination. If  not provided, it will be calculated on demand from the values. Defaults to None. 
 - <b>`start`</b> (int | None):  The start value of the combination range. If None, the current start  is used. Defaults to None. 
 - <b>`end`</b> (int | None):  The end value of the combination range. If None, the current end is  used. Defaults to None. 
 - <b>`count`</b> (int | None):  The count of numbers in the combination. If None, the current count  is used. Defaults to None. 
 - <b>`combinations`</b> (int | None):  The total number of possible combinations. If None, the  current combinations are used. Defaults to None. 



**Returns:**
 
 - <b>`BoundCombination`</b>:  A new BoundCombination instance with the specified modifications. 



**Examples:**
 ``` bound_comb = BoundCombination(values=[1, 2, 3], start=1, end=50, count=5)```
    >>> new_comb = bound_comb.copy(values=15)
    >>> new_comb.values
      [1, 2, 5, 6, 7]


---

<a href="../../src/pactole/combinations/combination.py#L302"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `BoundCombination.equals`

```python
equals(combination: 'CombinationInput') → bool
```

Check if the combination is equal to another combination or lexicographic rank. 



**Args:**
 
 - <b>`combination`</b> (CombinationInput):  The combination or lexicographic rank to compare with. 



**Returns:**
 
 - <b>`bool`</b>:  True if the combinations are equal, False otherwise. 



**Examples:**
 ``` combination1 = Combination([1, 2, 3])```
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


---

<a href="../../src/pactole/combinations/combination.py#L644"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `BoundCombination.generate`

```python
generate(n: 'int' = 1, partitions: 'int' = 1) → list[BoundCombination]
```

Generate a list of random combinations within the bounds. 



**Args:**
 
 - <b>`n`</b> (int):  The number of combinations to generate. Defaults to 1. 
 - <b>`partitions`</b> (int):  The number of partitions to divide the range into for generation.  Defaults to 1. 



**Returns:**
 
 - <b>`list[BoundCombination]`</b>:  A list of randomly generated combinations. 



**Examples:**
 ``` bound_comb = BoundCombination(start=1, end=50, count=5)```
    >>> random_combs = bound_comb.generate()
    >>> len(random_combs)
    1
    >>> random_combs[0].values
    [3, 15, 22, 34, 45]


---

<a href="../../src/pactole/combinations/combination.py#L287"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `BoundCombination.get_values`

```python
get_values(start: 'int | None' = None) → CombinationValues
```

Get the values of the combination as a sorted list with an optional new start offset. 



**Args:**
 
 - <b>`start`</b> (int, optional):  The new starting offset for the values. Defaults to None. 



**Returns:**
 
 - <b>`CombinationValues`</b>:  The sorted list of combination values with the new offset. 

---

<a href="../../src/pactole/combinations/combination.py#L335"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `BoundCombination.includes`

```python
includes(combination: 'CombinationNumber | CombinationInputValues') → bool
```

Check if the combination includes another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationNumber | CombinationInputValues):  The combination to check for  inclusion, or a single number. 



**Returns:**
 
 - <b>`bool`</b>:  True if the combination includes the other combination, False otherwise. 



**Examples:**
 ``` combination1 = Combination([2, 4, 6])```
    >>> combination2 = Combination([2, 4])
    >>> combination1.includes(combination2)
    True
    >>> combination1.includes([2, 5])
    False


---

<a href="../../src/pactole/combinations/combination.py#L390"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `BoundCombination.intersection`

```python
intersection(combination: 'CombinationInputValues') → Combination
```

Get the intersection of the combination with another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInputValues | Combination):  The combination to intersect with. 



**Returns:**
 
 - <b>`Combination`</b>:  The intersection of the two combinations. 



**Examples:**
 ``` combination1 = Combination([1, 2, 3])```
    >>> combination2 = Combination([3, 4, 5])
    >>> intersection = combination1.intersection(combination2)
    >>> intersection.values
    [3]
    >>> intersection2 = combination1.intersection([4, 5, 6])
    >>> intersection2.values
    []


---

<a href="../../src/pactole/combinations/combination.py#L364"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `BoundCombination.intersects`

```python
intersects(combination: 'CombinationInputValues | Combination') → bool
```

Check if the combination intersects with another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInputValues | Combination):  The combination to check for  intersection. 



**Returns:**
 
 - <b>`bool`</b>:  True if the combination intersects with the other combination, False otherwise. 



**Examples:**
 ``` combination1 = Combination([1, 2, 3])```
    >>> combination2 = Combination([3, 4, 5])
    >>> combination1.intersects(combination2)
    True
    >>> combination1.intersects([4, 5, 6])
    False


---

<a href="../../src/pactole/combinations/combination.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `BoundCombination.similarity`

```python
similarity(combination: 'CombinationInputValues') → float
```

Calculate the similarity between the combination and another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInputValues):  The combination to compare with. 



**Returns:**
 
 - <b>`float`</b>:  The similarity ratio between the two combinations. 



**Examples:**
 ``` combination1 = Combination([1, 2, 3])```
    >>> combination2 = Combination([2, 3, 4])
    >>> combination1.similarity(combination2)
    0.6666666666666666
    >>> combination1.similarity([4, 5, 6])
    0.0





---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
