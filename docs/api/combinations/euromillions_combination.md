# EuroMillionsCombination

[Pactole Index](../README.md#pactole-index) / [Combinations](./index.md#combinations) / EuroMillionsCombination

> Auto-generated documentation for [combinations.euromillions_combination](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/euromillions_combination.py) module.

- [EuroMillionsCombination](#euromillionscombination)
  - [EuroMillionsCombination](#euromillionscombination-1)

## EuroMillionsCombination

[Show source in euromillions_combination.py:37](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/euromillions_combination.py#L37)

Class representing a EuroMillions combination.

EuroMillions is a lottery game where players choose 5 main numbers from 1 to 50 and
2 star numbers from 1 to 12. The total number of combinations is 2,118,760 for the main numbers
and 66 for the star numbers. In total, there are 139,838,160 possible combinations.

#### Arguments

numbers (CombinationInputOrRank | EuroMillionsCombination | None): The main numbers of the
    combination or its rank. It can also contain the star numbers if `stars` is None.
    Default is None.
stars (CombinationInputOrRank | None): The star numbers of the combination, or its rank.
    If None, the star numbers are taken from `numbers`. Default is None.

#### Examples

```python
>>> euro_comb = EuroMillionsCombination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
>>> euro_comb.numbers
BoundCombination(values=[3, 15, 22, 28, 44], start=1, end=50, count=5, combinations=2118760)
>>> euro_comb.stars
BoundCombination(values=[2, 9], start=1, end=12, count=2, combinations=66)
```

#### Signature

```python
class EuroMillionsCombination(LotteryCombination):
    def __init__(
        self,
        numbers: CombinationInputOrRank | EuroMillionsCombination | None = None,
        stars: CombinationInputOrRank | None = None,
    ) -> None: ...
```