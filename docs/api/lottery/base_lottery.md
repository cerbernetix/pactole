# BaseLottery

[Pactole Index](../README.md#pactole-index) / [Lottery](./index.md#lottery) / BaseLottery

> Auto-generated documentation for [lottery.base_lottery](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py) module.

- [BaseLottery](#baselottery)
  - [BaseLottery](#baselottery-1)
    - [BaseLottery()._find_records_by_combination](#baselottery()_find_records_by_combination)
    - [BaseLottery()._find_records_by_winning_rank](#baselottery()_find_records_by_winning_rank)
    - [BaseLottery().combination_factory](#baselottery()combination_factory)
    - [BaseLottery().count](#baselottery()count)
    - [BaseLottery().draw_days](#baselottery()draw_days)
    - [BaseLottery().dump](#baselottery()dump)
    - [BaseLottery().find_records](#baselottery()find_records)
    - [BaseLottery().generate](#baselottery()generate)
    - [BaseLottery().get_combination](#baselottery()get_combination)
    - [BaseLottery().get_last_draw_date](#baselottery()get_last_draw_date)
    - [BaseLottery().get_next_draw_date](#baselottery()get_next_draw_date)
    - [BaseLottery().get_records](#baselottery()get_records)

## BaseLottery

[Show source in base_lottery.py:17](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L17)

A base class for lottery implementations.

#### Arguments

- `provider` *BaseProvider* - The data provider to use for fetching lottery results.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
...     combination_factory=EuroMillionsCombination,
... )
>>> lottery = BaseLottery(provider)
>>> lottery.draw_days
DrawDays(days=[<Weekday.MONDAY: 0>, <Weekday.THURSDAY: 3>])
>>> lottery.combination_factory
<class 'pactole.combinations.EuroMillionsCombination'>
>>> lottery.combination_factory(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
>>> lottery.get_next_draw_date(date(2024, 6, 5))
datetime.date(2024, 6, 6)
>>> combination = EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9])
>>> list(lottery.find_records(combination))
[DrawRecord(
    period='202001',
    draw_date=date(2020, 1, 1),
    deadline_date=date(2020, 1, 15),
    combination=EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9]),
    numbers={'number': [5, 12, 23, 34, 45], 'star': [2, 9]},
     winning_ranks=[WinningRank(rank=1, winners=1, gain=1000000.0), ...]
), ...]
```

#### Signature

```python
class BaseLottery:
    def __init__(self, provider: BaseProvider) -> None: ...
```

### BaseLottery()._find_records_by_combination

[Show source in base_lottery.py:384](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L384)

Find lottery results based on a combination.

#### Signature

```python
def _find_records_by_combination(
    self, combination: LotteryCombination, force: bool = False
) -> Iterator[FoundCombination]: ...
```

### BaseLottery()._find_records_by_winning_rank

[Show source in base_lottery.py:396](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L396)

Find lottery results based on a combination and an optional target rank.

#### Signature

```python
def _find_records_by_winning_rank(
    self,
    combination: LotteryCombination,
    target_rank: CombinationRank,
    strict: bool = False,
    force: bool = False,
) -> Iterator[FoundCombination]: ...
```

### BaseLottery().combination_factory

[Show source in base_lottery.py:76](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L76)

Return the combination factory associated with this lottery.

#### Returns

- `CombinationFactory` - The combination factory associated with this lottery.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
...     combination_factory=EuroMillionsCombination,
... )
>>> lottery = BaseLottery(provider)
>>> lottery.combination_factory
<class 'pactole.combinations.EuroMillionsCombination'>
>>> lottery.combination_factory(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
EuroMillionsCombination(numbers=[1, 2, 3, 4, 5], stars=[1, 2])
```

#### Signature

```python
@property
def combination_factory(self) -> CombinationFactory: ...
```

### BaseLottery().count

[Show source in base_lottery.py:217](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L217)

Return the total number of lottery records available in the cache.

#### Returns

- `int` - The total number of lottery records.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
...     combination_factory=EuroMillionsCombination,
... )
>>> lottery = BaseLottery(provider)
>>> lottery.count()
1234
```

#### Signature

```python
def count(self) -> int: ...
```

### BaseLottery().draw_days

[Show source in base_lottery.py:57](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L57)

Return the DrawDays instance associated with this lottery.

#### Returns

- `DrawDays` - The DrawDays instance associated with this lottery.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
... )
>>> lottery = BaseLottery(provider)
>>> lottery.draw_days
DrawDays(days=[<Weekday.MONDAY: 0>, <Weekday.THURSDAY: 3>])
```

#### Signature

```python
@property
def draw_days(self) -> DrawDays: ...
```

### BaseLottery().dump

[Show source in base_lottery.py:236](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L236)

Dump the cached data as a list of dictionaries.

If the cache is missing or outdated, it will be refreshed before dumping the data.

The returned list of dictionaries will have the same structure as the data stored in
the cache file, without being transformed into DrawRecord instances. This can be useful
for debugging or for scenarios where raw data manipulation is required, like exporting
to Pandas DataFrame or performing custom analyses.

#### Arguments

- `force` *bool, optional* - If True, forces a refresh of the cache before dumping.
    Defaults to False.

#### Returns

- `list[dict]` - A list of dictionaries representing the cached data.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
...     combination_factory=EuroMillionsCombination,
... )
>>> lottery = BaseLottery(provider)
>>> lottery.dump()
[
    {
        'period': '202201',
        'draw_date': '2022-01-15',
        'deadline_date': '2022-02-15',
        'numbers_1': 12,
        'numbers_2': 5,
        'numbers_3': 23,
        'numbers_4': 34,
        'numbers_5': 45,
        'stars_1': 7,
        'stars_2': 9,
        'numbers_rank': 1128527,
        'stars_rank': 34,
        'rank_1_winners': 2,
        'rank_1_gain': 1000000.0,
        'rank_2_winners': 10,
        'rank_2_gain': 50000.0
    },
    ...
]
```

#### Signature

```python
def dump(self, force: bool = False) -> list[dict]: ...
```

### BaseLottery().find_records

[Show source in base_lottery.py:319](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L319)

Find lottery results based on a query.

#### Arguments

combination (CombinationInput | LotteryCombination | None, optional): A combination to
    search for. Defaults to None.
target_rank (CombinationRank | None, optional): If provided, only results with the
    specified winning rank will be returned. Defaults to None.
- `strict` *bool, optional* - If True, the search will be strict, meaning that only
    records that exactly match the provided combination and target rank will be
    returned. If False, the search will be more flexible, allowing for partial matches
    as long as a winning rank is found. Defaults to False.
- `force` *bool, optional* - If True, forces a refresh of the cache before searching for
    results. Defaults to False.
**components (CombinationInputOrRank | LotteryCombination): Additional
    components of the combination to search for, provided as keyword arguments.
    The keys should correspond to the component names defined in the combination
    factory.

#### Returns

- `Iterator[FoundCombination]` - An iterator of FoundCombination instances matching the
    search criteria.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
...     combination_factory=EuroMillionsCombination,
...     cache_name="euromillions",
... )
>>> combination = EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9])
>>> lottery = BaseLottery(provider)
>>> list(lottery.find_records(combination))
[FoundCombination(
    record=DrawRecord(
        period='202001',
        draw_date=date(2020, 1, 1),
        deadline_date=date(2020, 1, 15),
        combination=EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9]),
        numbers={'number': [5, 12, 23, 34, 45], 'star': [2, 9]},
        winning_ranks=[WinningRank(rank=1, winners=1, gain=1000000.0), ...]
    ),
    rank=1
), ...]
```

#### Signature

```python
def find_records(
    self,
    combination: CombinationInput | LotteryCombination | None = None,
    target_rank: CombinationRank | None = None,
    strict: bool = False,
    force: bool = False,
    **components: CombinationInputOrRank | LotteryCombination
) -> Iterator[FoundCombination]: ...
```

### BaseLottery().generate

[Show source in base_lottery.py:168](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L168)

Generate a list of random lottery combinations.

#### Arguments

- `n` *int, optional* - The number of combinations to generate. Defaults to 1.
- `partitions` *int, optional* - The number of partitions to use when generating
    combinations. Defaults to 1.

#### Returns

- `list[LotteryCombination]` - A list of generated lottery combinations.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
...     combination_factory=EuroMillionsCombination,
... )
>>> lottery = BaseLottery(provider)
>>> lottery.generate(n=2)
[EuroMillionsCombination(numbers=[...], stars=[...]),
 EuroMillionsCombination(numbers=[...], stars=[...])]
```

#### Signature

```python
def generate(self, n: int = 1, partitions: int = 1) -> list[LotteryCombination]: ...
```

### BaseLottery().get_combination

[Show source in base_lottery.py:193](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L193)

Create a lottery combination from the provided components.

#### Arguments

- `**components` *CombinationInputOrRank* - The components of the combination, provided as
    keyword arguments. The keys should correspond to the component names defined in the
    combination factory.

#### Returns

- `LotteryCombination` - A lottery combination created from the provided components.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
...     combination_factory=EuroMillionsCombination,
... )
>>> lottery = BaseLottery(provider)
>>> lottery.get_combination(numbers=[5, 12, 23, 34, 45], stars=[2, 9])
EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9])
```

#### Signature

```python
def get_combination(
    self, **components: CombinationInputOrRank
) -> LotteryCombination: ...
```

### BaseLottery().get_last_draw_date

[Show source in base_lottery.py:98](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L98)

Return the date of the last lottery draw.

#### Arguments

from_date (Day | Weekday | None, optional): The starting date.

A timestamp can be provided as an integer or float representing
seconds since the epoch. When a string is provided, it must be in the ISO format
'YYYY-MM-DD'. Finally, a date object can be provided directly.

Defaults to None.

#### Returns

- `date` - The date of the last lottery draw.

#### Raises

- `TypeError` - If the provided date is not a string, timestamp, or date object.
- `ValueError` - If the string is not a valid date in ISO format.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
... )
>>> lottery = BaseLottery(provider)
>>> lottery.get_last_draw_date(date(2024, 6, 5))
datetime.date(2024, 6, 3)
```

#### Signature

```python
def get_last_draw_date(
    self, from_date: Day | Weekday | None = None, closest: bool = True
) -> date: ...
```

### BaseLottery().get_next_draw_date

[Show source in base_lottery.py:133](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L133)

Return the date of the next lottery draw.

#### Arguments

from_date (Day | Weekday | None, optional): The starting date.

A timestamp can be provided as an integer or float representing
seconds since the epoch. When a string is provided, it must be in the ISO format
'YYYY-MM-DD'. Finally, a date object can be provided directly.

Defaults to None.

#### Returns

- `date` - The date of the next lottery draw.

#### Raises

- `TypeError` - If the provided date is not a string, timestamp, or date object.
- `ValueError` - If the string is not a valid date in ISO format.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.MONDAY, Weekday.THURSDAY],
... )
>>> lottery = BaseLottery(provider)
>>> lottery.get_next_draw_date(date(2024, 6, 5))
datetime.date(2024, 6, 6)
```

#### Signature

```python
def get_next_draw_date(
    self, from_date: Day | Weekday | None = None, closest: bool = True
) -> date: ...
```

### BaseLottery().get_records

[Show source in base_lottery.py:286](https://github.com/cerbernetix/pactole/blob/main/src/pactole/lottery/base_lottery.py#L286)

Get the cached data as an iterator of DrawRecord instances.

If the cache is missing or outdated, it will be refreshed before returning the data.

#### Arguments

- `force` *bool, optional* - If True, forces a refresh of the cache before getting the data.
    Defaults to False.

#### Returns

- `Iterator[DrawRecord]` - An iterator of DrawRecord instances representing the cached data.

#### Examples

```python
>>> provider = BaseProvider(
...     resolver=MyResolver(),
...     parser=MyParser(),
...     draw_days=[Weekday.TUESDAY, Weekday.FRIDAY],
...     combination_factory=EuroMillionsCombination,
...     cache_name="euromillions"
... )
>>> lottery = BaseLottery(provider)
>>> list(lottery.get_records())
[DrawRecord(
    period='202001',
    draw_date=date(2020, 1, 1),
    deadline_date=date(2020, 1, 15),
    combination=EuroMillionsCombination(numbers=[5, 12, 23, 34, 45], stars=[2, 9]),
    numbers={'number': [5, 12, 23, 34, 45], 'star': [2, 9]},
    winning_ranks=[WinningRank(rank=1, winners=1, gain=1000000.0), ...]
), ...]
```

#### Signature

```python
def get_records(self, force: bool = False) -> Iterator[DrawRecord]: ...
```