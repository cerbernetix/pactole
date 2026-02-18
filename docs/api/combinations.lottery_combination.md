<!-- markdownlint-disable -->

<a href="../../src/pactole/combinations/lottery_combination.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `combinations.lottery_combination`
Module for Lottery combination representation and manipulation. 



---

<a href="../../src/pactole/combinations/lottery_combination.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CombinationFactory`
Protocol for a combination factory. 





---

<a href="../../src/pactole/combinations/lottery_combination.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `LotteryCombination`
Class representing a Lottery combination. 

A Lottery combination is a compound combination that can consist of multiple components (e.g., main numbers, bonus numbers). 



**Args:**
 
 - <b>`combination`</b> (LotteryCombination | None):  The combination to copy from. 
 - <b>`winning_ranks`</b> (CombinationWinningRanks | None):  The winning ranks mapping. If None,  initializes an empty mapping. 
 - <b>`**components (BoundCombination)`</b>:  The components of the combination. 



**Raises:**
 
 - <b>`TypeError`</b>:  If any component is not an instance of BoundCombination. 



**Examples:**
 ``` main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
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


<a href="../../src/pactole/combinations/lottery_combination.py#L80"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.__init__`

```python
__init__(
    combination: 'LotteryCombination | None' = None,
    winning_ranks: 'CombinationWinningRanks | None' = None,
    **components: 'BoundCombination'
) → None
```






---

#### <kbd>property</kbd> LotteryCombination.combinations

Return the total number of possible combinations. 



**Returns:**
 
 - <b>`int`</b>:  The total number of combinations. 



**Examples:**
 ``` main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
    >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
    >>> lottery_comb = LotteryCombination(
    ...     main=main_numbers,
    ...     bonus=bonus_number
    ... )
    >>> lottery_comb.combinations
    21187600


---

#### <kbd>property</kbd> LotteryCombination.components

Get the components of the combination. 



**Returns:**
 
 - <b>`CombinationComponents`</b>:  The components of the combination. 



**Examples:**
 ``` main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
    >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
    >>> lottery_comb = LotteryCombination(
    ...     main=main_numbers,
    ...     bonus=bonus_number
    ... )
    >>> lottery_comb.components
    {'main': BoundCombination(...), 'bonus': BoundCombination(...)}


---

#### <kbd>property</kbd> LotteryCombination.max_winning_rank

Get the maximum winning rank. 



**Returns:**
 
 - <b>`int | None`</b>:  The maximum winning rank, or None if there are no winning ranks. 



**Examples:**
 ``` winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}```
    >>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
    >>> lottery_comb.max_winning_rank
    4
    >>> lottery_comb_empty = LotteryCombination()
    >>> lottery_comb_empty.max_winning_rank
    None


---

#### <kbd>property</kbd> LotteryCombination.min_winning_rank

Get the minimum winning rank. 



**Returns:**
 
 - <b>`int | None`</b>:  The minimum winning rank, or None if there are no winning ranks. 



**Examples:**
 ``` winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}```
    >>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
    >>> lottery_comb.min_winning_rank
    1
    >>> lottery_comb_empty = LotteryCombination()
    >>> lottery_comb_empty.min_winning_rank
    None


---

#### <kbd>property</kbd> LotteryCombination.nb_winning_ranks

Get the number of winning ranks. 



**Returns:**
 
 - <b>`int`</b>:  The number of winning ranks. 



**Examples:**
 ``` winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}```
    >>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
    >>> lottery_comb.nb_winning_ranks
    4


---

#### <kbd>property</kbd> LotteryCombination.winning_ranks

Get the winning ranks mapping. 



**Returns:**
 
 - <b>`CombinationWinningRanks`</b>:  The winning ranks mapping. 



**Examples:**
 ``` winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}```
    >>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
    >>> lottery_comb.winning_ranks
    {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}




---

<a href="../../src/pactole/combinations/lottery_combination.py#L773"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.compares`

```python
compares(
    combination: 'CombinationInput | LotteryCombination | None' = None,
    **components: 'CombinationInputOrRank | LotteryCombination'
) → int
```

Compare the combination with another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInput | LotteryCombination | None):  The other combination to  compare against. 
 - <b>`**components (CombinationInputOrRank | LotteryCombination)`</b>:  The components of the other  combination. 



**Returns:**
 
 - <b>`int`</b>:  -1 if self < combination, 0 if self == combination, 1 if self > combination. 



**Raises:**
 
 - <b>`KeyError`</b>:  If a component name does not exist in the current combination. 



**Examples:**
 ``` main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
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


---

<a href="../../src/pactole/combinations/lottery_combination.py#L335"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.copy`

```python
copy(
    winning_ranks: 'CombinationWinningRanks | None' = None,
    **components: 'CombinationInputOrRank | LotteryCombination'
) → LotteryCombination
```

Create a copy of the LotteryCombination with optional modifications. 



**Args:**
 
 - <b>`winning_ranks`</b> (CombinationWinningRanks | None):  The winning ranks mapping. If None,  uses the current instance's winning ranks. 
 - <b>`**components (CombinationInputOrRank | LotteryCombination)`</b>:  The components to modify in  the copy. If not provided, the original component is used. 



**Returns:**
 
 - <b>`LotteryCombination`</b>:  A new LotteryCombination instance with the specified modifications. 

---

<a href="../../src/pactole/combinations/lottery_combination.py#L571"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.equals`

```python
equals(
    combination: 'CombinationInput | LotteryCombination | None' = None,
    **components: 'CombinationInputOrRank | LotteryCombination'
) → bool
```

Check if the combination is equal to another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInput | LotteryCombination | None):  The other combination to  compare against. 
 - <b>`**components (CombinationInputOrRank | LotteryCombination)`</b>:  The components of the other  combination. 



**Returns:**
 
 - <b>`bool`</b>:  True if equal, False otherwise. 



**Raises:**
 
 - <b>`KeyError`</b>:  If a component name does not exist in the current combination. 



**Examples:**
 ``` main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
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


---

<a href="../../src/pactole/combinations/lottery_combination.py#L297"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.generate`

```python
generate(n: 'int' = 1, partitions: 'int' = 1) → list[LotteryCombination]
```

Generate a list of random LotteryCombination with similar components. 



**Args:**
 
 - <b>`n`</b> (int):  The number of combinations to generate. Defaults to 1. 
 - <b>`partitions`</b> (int):  The number of partitions to divide the generation into. Defaults to 1. 



**Returns:**
 
 - <b>`list[LotteryCombination]`</b>:  A list of generated LotteryCombination instances. 



**Examples:**
 ``` main_numbers = BoundCombination(start=1, end=50, count=5)```
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


---

<a href="../../src/pactole/combinations/lottery_combination.py#L361"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.get_combination`

```python
get_combination(
    combination: 'CombinationInput | LotteryCombination | None' = None,
    winning_ranks: 'CombinationWinningRanks | None' = None,
    **components: 'CombinationInputOrRank | LotteryCombination'
) → LotteryCombination
```

Get a LotteryCombination based on provided components. 



**Args:**
 
 - <b>`combination`</b> (CombinationInput | LotteryCombination | None):  The base combination to  build from. If None, uses the provided components. 
 - <b>`winning_ranks`</b> (CombinationWinningRanks | None):  The winning ranks mapping. If None,  uses the current instance's winning ranks. 
 - <b>`**components (CombinationInputOrRank | LotteryCombination)`</b>:  The components to construct  the combination. 



**Returns:**
 
 - <b>`LotteryCombination`</b>:  The constructed LotteryCombination. 



**Raises:**
 
 - <b>`KeyError`</b>:  If a component name does not exist in the current combination. 



**Examples:**
 ``` main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
    >>> bonus_number = BoundCombination(values=[6], start=1, end=10, count=1)
    >>> lottery_comb = LotteryCombination(
    ...     main=main_numbers,
    ...     bonus=bonus_number
    ... )
    >>> new_comb = lottery_comb.get_combination(main=[1, 2, 3, 6, 7])
    >>> new_comb.components
    {'main': BoundCombination(...), 'bonus': BoundCombination(...)}


---

<a href="../../src/pactole/combinations/lottery_combination.py#L467"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.get_component`

```python
get_component(name: 'str') → BoundCombination | None
```

Get the parameters for a specific component of the combination. 



**Args:**
 
 - <b>`name`</b> (str):  The name of the component. 



**Returns:**
 
 - <b>`BoundCombination | None`</b>:  The parameters for the specified component,  or None if not found. 



**Examples:**
 ``` main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
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


---

<a href="../../src/pactole/combinations/lottery_combination.py#L493"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.get_component_values`

```python
get_component_values(name: 'str') → CombinationValues
```

Get the values for a specific component of the combination. 



**Args:**
 
 - <b>`name`</b> (str):  The name of the component. 



**Returns:**
 
 - <b>`CombinationValues`</b>:  The values for the specified component. 



**Examples:**
 ``` main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
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


---

<a href="../../src/pactole/combinations/lottery_combination.py#L431"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.get_components`

```python
get_components(
    **components: 'CombinationInputOrRank | LotteryCombination'
) → CombinationComponents
```

Get the parameters for multiple components of the combination. 



**Args:**
 
 - <b>`**components (CombinationInputOrRank | LotteryCombination)`</b>:  The names and values of the  components. 



**Returns:**
 
 - <b>`CombinationComponents`</b>:  The parameters for the specified components. 



**Raises:**
 
 - <b>`KeyError`</b>:  If a component name does not exist in the current combination. 



**Examples:**
 ``` main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
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


---

<a href="../../src/pactole/combinations/lottery_combination.py#L522"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.get_winning_rank`

```python
get_winning_rank(
    combination: 'CombinationInput | LotteryCombination | None' = None,
    **components: 'CombinationInputOrRank | LotteryCombination'
) → int | None
```

Get the winning rank of the combination against a winning combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInput | LotteryCombination | None):  The winning combination to  compare against. 
 - <b>`**components (CombinationInputOrRank | LotteryCombination)`</b>:  The components of the  winning combination. 



**Returns:**
 
 - <b>`int | None`</b>:  The winning rank, or None if not a winning combination. 



**Raises:**
 
 - <b>`KeyError`</b>:  If a component name does not exist in the current combination. 



**Examples:**
 ``` main_numbers = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
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


---

<a href="../../src/pactole/combinations/lottery_combination.py#L621"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.includes`

```python
includes(
    combination: 'CombinationInput | LotteryCombination | None' = None,
    **components: 'CombinationInputOrRank | LotteryCombination'
) → bool
```

Check if the combination includes another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInput | LotteryCombination | None):  The other combination to  compare against. 
 - <b>`**components (CombinationInputOrRank | LotteryCombination)`</b>:  The components of the other  combination. 



**Returns:**
 
 - <b>`bool`</b>:  True if includes, False otherwise. 



**Raises:**
 
 - <b>`KeyError`</b>:  If a component name does not exist in the current combination. 



**Examples:**
 ``` main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
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


---

<a href="../../src/pactole/combinations/lottery_combination.py#L726"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.intersection`

```python
intersection(
    combination: 'CombinationInput | LotteryCombination | None' = None,
    **components: 'CombinationInputOrRank | LotteryCombination'
) → LotteryCombination
```

Get the intersection with another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInput | LotteryCombination | None):  The other combination to  compare against. 
 - <b>`**components (CombinationInputOrRank | LotteryCombination)`</b>:  The components of the other  combination. 



**Returns:**
 
 - <b>`LotteryCombination`</b>:  The intersection combination. 



**Raises:**
 
 - <b>`KeyError`</b>:  If a component name does not exist in the current combination. 



**Examples:**
 ``` main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
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


---

<a href="../../src/pactole/combinations/lottery_combination.py#L673"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.intersects`

```python
intersects(
    combination: 'CombinationInput | LotteryCombination | None' = None,
    **components: 'CombinationInputOrRank | LotteryCombination'
) → bool
```

Check if the combination intersects with another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInput | LotteryCombination | None):  The other combination to  compare against. 
 - <b>`**components (CombinationInputOrRank | LotteryCombination)`</b>:  The components of the other  combination. 



**Returns:**
 
 - <b>`bool`</b>:  True if intersects, False otherwise. 



**Raises:**
 
 - <b>`KeyError`</b>:  If a component name does not exist in the current combination. 



**Examples:**
 ``` main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
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


---

<a href="../../src/pactole/combinations/lottery_combination.py#L824"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LotteryCombination.similarity`

```python
similarity(
    combination: 'CombinationInput | LotteryCombination | None' = None,
    **components: 'CombinationInputOrRank | LotteryCombination'
) → float
```

Calculate the similarity with another combination. 



**Args:**
 
 - <b>`combination`</b> (CombinationInput | LotteryCombination | None):  The other combination to  compare against. 
 - <b>`**components (CombinationInputOrRank | LotteryCombination)`</b>:  The components of the other  combination. 



**Returns:**
 
 - <b>`float`</b>:  Similarity ratio between 0 and 1. 



**Raises:**
 
 - <b>`KeyError`</b>:  If a component name does not exist in the current combination. 



**Examples:**
 ``` main_numbers1 = BoundCombination(values=[1, 2, 3, 4, 5], start=1, end=50, count=5)```
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





---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
