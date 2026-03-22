# EuroDreamsCombination

[Pactole Index](../README.md#pactole-index) / [Combinations](./index.md#combinations) / EuroDreamsCombination

> Auto-generated documentation for [combinations.eurodreams_combination](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/eurodreams_combination.py) module.

- [EuroDreamsCombination](#eurodreamscombination)
  - [EuroDreamsCombination](#eurodreamscombination-1)
    - [EuroDreamsCombination.from_csv](#eurodreamscombinationfrom_csv)
    - [EuroDreamsCombination.from_dict](#eurodreamscombinationfrom_dict)
    - [EuroDreamsCombination.from_string](#eurodreamscombinationfrom_string)
    - [EuroDreamsCombination().to_dict](#eurodreamscombination()to_dict)

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

### EuroDreamsCombination.from_csv

[Show source in eurodreams_combination.py:157](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/eurodreams_combination.py#L157)

Create a EuroDreamsCombination instance from a CSV string representation.

#### Arguments

- [Data](../data/index.md#data) *dict* - A dictionary representation of the combination in the format
    - `{"numbers_1"` - n1, "numbers_2": n2, ..., "dream_1": d1}.

#### Returns

- [EuroDreamsCombination](#eurodreamscombination) - A new EuroDreamsCombination instance created from
    the CSV string data.

#### Examples

```python
>>> data = {
...    'numbers_1': 1,
...    'numbers_2': 2,
...    'numbers_3': 3,
...    'numbers_4': 4,
...    'numbers_5': 5,
...    'dream_1': 6
... }
>>> euro_comb = EuroDreamsCombination.from_csv(data)
>>> euro_comb.numbers.values
[1, 2, 3, 4, 5]
>>> euro_comb.dream.values
[6]
```

#### Signature

```python
@classmethod
def from_csv(cls, data: dict) -> EuroDreamsCombination: ...
```

### EuroDreamsCombination.from_dict

[Show source in eurodreams_combination.py:113](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/eurodreams_combination.py#L113)

Create a EuroDreamsCombination instance from a dictionary.

#### Arguments

- [Data](../data/index.md#data) *dict* - A dictionary containing the combination data.

#### Returns

- [EuroDreamsCombination](#eurodreamscombination) - A new EuroDreamsCombination instance created from
    the dictionary data.

#### Examples

```python
>>> data = {'numbers': [2, 3, 5, 7, 9, 38], 'dream': [3]}
>>> euro_comb = EuroDreamsCombination.from_dict(data)
>>> euro_comb.numbers.values
[2, 3, 5, 7, 9, 38]
>>> euro_comb.dream.values
[3]
```

#### Signature

```python
@classmethod
def from_dict(cls, data: dict) -> EuroDreamsCombination: ...
```

### EuroDreamsCombination.from_string

[Show source in eurodreams_combination.py:134](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/eurodreams_combination.py#L134)

Create a EuroDreamsCombination instance from a string representation.

#### Arguments

- [Data](../data/index.md#data) *str* - A string representation of the combination in the format
    - `"numbers` - [n1, n2, n3, n4, n5, n6]  dream: [d1]".

#### Returns

- [EuroDreamsCombination](#eurodreamscombination) - A new EuroDreamsCombination instance created from
    the string data.

#### Examples

```python
>>> data = "numbers: [2, 3, 5, 7, 9, 38]  dream: [3]"
>>> euro_comb = EuroDreamsCombination.from_string(data)
>>> euro_comb.numbers.values
[2, 3, 5, 7, 9, 38]
>>> euro_comb.dream.values
[3]
```

#### Signature

```python
@classmethod
def from_string(cls, data: str) -> EuroDreamsCombination: ...
```

### EuroDreamsCombination().to_dict

[Show source in eurodreams_combination.py:100](https://github.com/cerbernetix/pactole/blob/main/src/pactole/combinations/eurodreams_combination.py#L100)

Convert the EuroDreamsCombination to a dictionary.

#### Returns

- `dict` - A dictionary representation of the EuroDreamsCombination.

#### Examples

```python
>>> euro_comb = EuroDreamsCombination(numbers=[2, 3, 5, 7, 9, 38], dream=[3])
>>> euro_comb.to_dict()
{'numbers': [2, 3, 5, 7, 9, 38], 'dream': [3]}
```

#### Signature

```python
def to_dict(self) -> dict: ...
```