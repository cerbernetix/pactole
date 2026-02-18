<!-- markdownlint-disable -->

<a href="../../src/pactole/combinations/eurodreams_combination.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `combinations.eurodreams_combination`
Module for EuroDreams combination representation and manipulation. 

**Global Variables**
---------------
- **NUMBER_COUNT**
- **NUMBER_START**
- **NUMBER_END**
- **NUMBER_COMBINATIONS**
- **DREAM_COUNT**
- **DREAM_START**
- **DREAM_END**
- **DREAM_COMBINATIONS**
- **TOTAL_COMBINATIONS**
- **WINNING_RANKS**


---

<a href="../../src/pactole/combinations/eurodreams_combination.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EuroDreamsCombination`
Class representing a EuroDreams combination. 

EuroDreams is a lottery game where players choose 6 main numbers from 1 to 40 and 1 dream number from 1 to 5. The total number of combinations is 3,838,380 for the main numbers and 5 for the dream numbers. In total, there are 19,191,900 possible combinations. 



**Args:**
 
 - <b>`numbers`</b> (CombinationInputOrRank | EuroDreamsCombination | None):  The main numbers of the  combination or its rank. It can also contain the dream numbers if `dream` is None.  Default is None. 
 - <b>`dream`</b> (CombinationInputOrRank | None):  The dream number of the combination.  If None, the dream number is taken from `numbers`. Default is None. 



**Examples:**
 ``` euro_comb = EuroDreamsCombination(numbers=[2, 3, 5, 7, 9, 38], dream=[3])```
    >>> euro_comb.numbers
    BoundCombination(values=[2, 3, 5, 7, 9, 38], start=1, end=40, count=6, combinations=3838380)
    >>> euro_comb.dream
    BoundCombination(values=[3], start=1, end=5, count=1, combinations=5)


<a href="../../src/pactole/combinations/eurodreams_combination.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `EuroDreamsCombination.__init__`

```python
__init__(
    numbers: 'CombinationInputOrRank | EuroDreamsCombination | None' = None,
    dream: 'CombinationInputOrRank | None' = None
) → None
```






---

#### <kbd>property</kbd> EuroDreamsCombination.combinations

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

#### <kbd>property</kbd> EuroDreamsCombination.components

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

#### <kbd>property</kbd> EuroDreamsCombination.max_winning_rank

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

#### <kbd>property</kbd> EuroDreamsCombination.min_winning_rank

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

#### <kbd>property</kbd> EuroDreamsCombination.nb_winning_ranks

Get the number of winning ranks. 



**Returns:**
 
 - <b>`int`</b>:  The number of winning ranks. 



**Examples:**
 ``` winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}```
    >>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
    >>> lottery_comb.nb_winning_ranks
    4


---

#### <kbd>property</kbd> EuroDreamsCombination.winning_ranks

Get the winning ranks mapping. 



**Returns:**
 
 - <b>`CombinationWinningRanks`</b>:  The winning ranks mapping. 



**Examples:**
 ``` winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}```
    >>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
    >>> lottery_comb.winning_ranks
    {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
