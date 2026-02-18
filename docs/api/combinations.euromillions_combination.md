<!-- markdownlint-disable -->

<a href="../../src/pactole/combinations/euromillions_combination.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `combinations.euromillions_combination`
Module for EuroMillions combination representation and manipulation. 

**Global Variables**
---------------
- **NUMBER_COUNT**
- **NUMBER_START**
- **NUMBER_END**
- **NUMBER_COMBINATIONS**
- **STAR_COUNT**
- **STAR_START**
- **STAR_END**
- **STAR_COMBINATIONS**
- **TOTAL_COMBINATIONS**
- **WINNING_RANKS**


---

<a href="../../src/pactole/combinations/euromillions_combination.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EuroMillionsCombination`
Class representing a EuroMillions combination. 

EuroMillions is a lottery game where players choose 5 main numbers from 1 to 50 and 2 star numbers from 1 to 12. The total number of combinations is 2,118,760 for the main numbers and 66 for the star numbers. In total, there are 139,838,160 possible combinations. 



**Args:**
 
 - <b>`numbers`</b> (CombinationInputOrRank | EuroMillionsCombination | None):  The main numbers of the  combination or its rank. It can also contain the star numbers if `stars` is None.  Default is None. 
 - <b>`stars`</b> (CombinationInputOrRank | None):  The star numbers of the combination, or its rank.  If None, the star numbers are taken from `numbers`. Default is None. 



**Examples:**
 ``` euro_comb = EuroMillionsCombination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])```
    >>> euro_comb.numbers
    BoundCombination(values=[3, 15, 22, 28, 44], start=1, end=50, count=5, combinations=2118760)
    >>> euro_comb.stars
    BoundCombination(values=[2, 9], start=1, end=12, count=2, combinations=66)


<a href="../../src/pactole/combinations/euromillions_combination.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `EuroMillionsCombination.__init__`

```python
__init__(
    numbers: 'CombinationInputOrRank | EuroMillionsCombination | None' = None,
    stars: 'CombinationInputOrRank | None' = None
) → None
```






---

#### <kbd>property</kbd> EuroMillionsCombination.combinations

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

#### <kbd>property</kbd> EuroMillionsCombination.components

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

#### <kbd>property</kbd> EuroMillionsCombination.max_winning_rank

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

#### <kbd>property</kbd> EuroMillionsCombination.min_winning_rank

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

#### <kbd>property</kbd> EuroMillionsCombination.nb_winning_ranks

Get the number of winning ranks. 



**Returns:**
 
 - <b>`int`</b>:  The number of winning ranks. 



**Examples:**
 ``` winning_ranks = {(5, 1): 1, (5, 0): 2, (4, 1): 3, (4, 0): 4}```
    >>> lottery_comb = LotteryCombination(winning_ranks=winning_ranks)
    >>> lottery_comb.nb_winning_ranks
    4


---

#### <kbd>property</kbd> EuroMillionsCombination.winning_ranks

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
