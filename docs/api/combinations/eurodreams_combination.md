# EuroDreamsCombination

[Pactole Index](../README.md#pactole-index) / [Combinations](./index.md#combinations) / EuroDreamsCombination

> Auto-generated documentation for [combinations.eurodreams_combination](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/eurodreams_combination.py) module.

- [EuroDreamsCombination](#eurodreamscombination)
  - [EuroDreamsCombination](#eurodreamscombination-1)

## EuroDreamsCombination

[Show source in eurodreams_combination.py:34](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/eurodreams_combination.py#L34)

Class representing a EuroDreams combination.

EuroDreams is a lottery game where players choose 6 main numbers from 1 to 40 and
1 dream number from 1 to 5. The total number of combinations is 3,838,380 for the main numbers
and 5 for the dream numbers. In total, there are 19,191,900 possible combinations.

#### Arguments

numbers (CombinationInputOrRank | EuroDreamsCombination | None): The main numbers of the
    combination or its rank. It can also contain the dream numbers if `dream` is None.
    Default is None.
dream (CombinationInputOrRank | None): The dream number of the combination.
    If None, the dream number is taken from `numbers`. Default is None.

#### Examples

```python
>>> euro_comb = EuroDreamsCombination(numbers=[2, 3, 5, 7, 9, 38], dream=[3])
>>> euro_comb.numbers
BoundCombination(values=[2, 3, 5, 7, 9, 38], start=1, end=40, count=6, combinations=3838380)
>>> euro_comb.dream
BoundCombination(values=[3], start=1, end=5, count=1, combinations=5)
```

#### Signature

```python
class EuroDreamsCombination(LotteryCombination):
    def __init__(
        self,
        numbers: CombinationInputOrRank | EuroDreamsCombination | None = None,
        dream: CombinationInputOrRank | None = None,
    ) -> None: ...
```