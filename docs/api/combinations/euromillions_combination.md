# EuroMillionsCombination

[Pactole Index](../README.md#pactole-index) / [Combinations](./index.md#combinations) / EuroMillionsCombination

> Auto-generated documentation for [combinations.euromillions_combination](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/euromillions_combination.py) module.

- [EuroMillionsCombination](#euromillionscombination)
  - [EuroMillionsCombination](#euromillionscombination-1)
    - [EuroMillionsCombination.from_csv](#euromillionscombinationfrom_csv)
    - [EuroMillionsCombination.from_dict](#euromillionscombinationfrom_dict)
    - [EuroMillionsCombination.from_string](#euromillionscombinationfrom_string)
    - [EuroMillionsCombination().to_dict](#euromillionscombination()to_dict)

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

### EuroMillionsCombination.from_csv

[Show source in euromillions_combination.py:160](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/euromillions_combination.py#L160)

Create a EuroMillionsCombination instance from a CSV string representation.

#### Arguments

- [Data](../data/index.md#data) *dict* - A dictionary representation of the combination, in the format
    - `{"numbers_1"` - n1, "numbers_2": n2, ..., "stars_1": s1, "stars_2": s2}.

#### Returns

- [EuroMillionsCombination](#euromillionscombination) - A new EuroMillionsCombination instance created from
    the CSV string data.

#### Examples

```python
>>> data = {
...    'numbers_1': 3,
...    'numbers_2': 15,
...    'numbers_3': 22,
...    'numbers_4': 28,
...    'numbers_5': 44,
...    'stars_1': 2,
...    'stars_2': 9
... }
>>> euro_comb = EuroMillionsCombination.from_csv(data)
>>> euro_comb.numbers.values
[3, 15, 22, 28, 44]
>>> euro_comb.stars.values
[2, 9]
```

#### Signature

```python
@classmethod
def from_csv(cls, data: dict) -> EuroMillionsCombination: ...
```

### EuroMillionsCombination.from_dict

[Show source in euromillions_combination.py:116](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/euromillions_combination.py#L116)

Create a EuroMillionsCombination instance from a dictionary.

#### Arguments

- [Data](../data/index.md#data) *dict* - A dictionary containing the combination data.

#### Returns

- [EuroMillionsCombination](#euromillionscombination) - A new EuroMillionsCombination instance created from
    the dictionary data.

#### Examples

```python
>>> data = {'numbers': [3, 15, 22, 28, 44], 'stars': [2, 9]}
>>> euro_comb = EuroMillionsCombination.from_dict(data)
>>> euro_comb.numbers.values
[3, 15, 22, 28, 44]
>>> euro_comb.stars.values
[2, 9]
```

#### Signature

```python
@classmethod
def from_dict(cls, data: dict) -> EuroMillionsCombination: ...
```

### EuroMillionsCombination.from_string

[Show source in euromillions_combination.py:137](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/euromillions_combination.py#L137)

Create a EuroMillionsCombination instance from a string representation.

#### Arguments

- [Data](../data/index.md#data) *str* - A string representation of the combination, in the format
    - `"numbers` - [n1, n2, n3, n4, n5]  stars: [s1, s2]".

#### Returns

- [EuroMillionsCombination](#euromillionscombination) - A new EuroMillionsCombination instance created from
    the string data.

#### Examples

```python
>>> data = "numbers: [3, 15, 22, 28, 44]  stars: [2, 9]"
>>> euro_comb = EuroMillionsCombination.from_string(data)
>>> euro_comb.numbers.values
[3, 15, 22, 28, 44]
>>> euro_comb.stars.values
[2, 9]
```

#### Signature

```python
@classmethod
def from_string(cls, data: str) -> EuroMillionsCombination: ...
```

### EuroMillionsCombination().to_dict

[Show source in euromillions_combination.py:103](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/euromillions_combination.py#L103)

Convert the EuroMillionsCombination to a dictionary.

#### Returns

- `dict` - A dictionary representation of the EuroMillionsCombination.

#### Examples

```python
>>> euro_comb = EuroMillionsCombination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
>>> euro_comb.to_dict()
{'numbers': [3, 15, 22, 28, 44], 'stars': [2, 9]}
```

#### Signature

```python
def to_dict(self) -> dict: ...
```