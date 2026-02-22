# Models

[Pactole Index](../README.md#pactole-index) / [Data](./index.md#data) / Models

> Auto-generated documentation for [data.models](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py) module.

- [Models](#models)
  - [ArchiveContentInfo](#archivecontentinfo)
  - [ArchiveInfo](#archiveinfo)
  - [DrawRecord](#drawrecord)
    - [DrawRecord.from_dict](#drawrecordfrom_dict)
    - [DrawRecord().to_dict](#drawrecord()to_dict)
  - [FoundCombination](#foundcombination)
  - [WinningRank](#winningrank)

## ArchiveContentInfo

[Show source in models.py:24](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L24)

A dictionary containing information about the content of an archive.

#### Signature

```python
class ArchiveContentInfo(TypedDict): ...
```



## ArchiveInfo

[Show source in models.py:33](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L33)

A dictionary containing information about an archive.

#### Signature

```python
class ArchiveInfo(ArchiveContentInfo): ...
```

#### See also

- [ArchiveContentInfo](#archivecontentinfo)



## DrawRecord

[Show source in models.py:58](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L58)

A class representing a record of a lottery draw.

#### Signature

```python
class DrawRecord: ...
```

### DrawRecord.from_dict

[Show source in models.py:133](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L133)

Create a DrawRecord instance from a dictionary.

#### Arguments

- [Data](./index.md#data) *dict* - A dictionary containing the draw record data.
combination_factory (CombinationFactory | None): A factory function or class to create a
    combination instance. If None, a default LotteryCombination instance will be used.
    Default is None.

#### Returns

- [DrawRecord](#drawrecord) - An instance of DrawRecord created from the input dictionary.

#### Examples

```python
>>> data = {
...     "period": "202201",
...     "draw_date": "2022-01-15",
...     "deadline_date": "2022-02-15",
...     "main_1": 12,
...     "main_2": 5,
...     "main_3": 23,
...     "bonus_1": 7,
...     "main_rank": 1,
...     "bonus_rank": 2,
...     "combination_rank": 1,
...     "rank_1_winners": 2,
...     "rank_1_gain": 1000000.0,
...     "rank_2_winners": 10,
...     "rank_2_gain": 50000.0,
... }
>>> record = DrawRecord.from_dict(data)
>>> print(record)
DrawRecord(
    period='202201',
    draw_date=datetime.date(2022, 1, 15),
    deadline_date=datetime.date(2022, 2, 15),
    combination=LotteryCombination(components={'main': ..., 'bonus': ...}),
    numbers={'main': [12, 5, 23], 'bonus': [7]},
    winning_ranks=[
        WinningRank(rank=1, winners=2, gain=1000000.0),
        WinningRank(rank=2, winners=10, gain=50000.0)
    ]
)
```

#### Signature

```python
@staticmethod
def from_dict(
    data: dict, combination_factory: CombinationFactory | None = None
) -> DrawRecord: ...
```

### DrawRecord().to_dict

[Show source in models.py:79](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L79)

Convert the DrawRecord instance to a dictionary.

#### Returns

- `dict` - A dictionary representation of the DrawRecord instance.

#### Examples

```python
>>> record = DrawRecord(
...     period="202201",
...     draw_date=datetime.date(2022, 1, 15),
...     deadline_date=datetime.date(2022, 2, 15),
...     combination=LotteryCombination(components={"main": ..., "bonus": ...}),
...     numbers={"main": [12, 5, 23], "bonus": [7]},
...     winning_ranks=[
...         WinningRank(rank=1, winners=2, gain=1000000.0),
...         WinningRank(rank=2, winners=10, gain=50000.0)],
...     ]
... )
>>> record.to_dict()
{'period': '202201',
 'draw_date': '2022-01-15',
 'deadline_date': '2022-02-15',
 'main_1': 12,
 'main_2': 5,
 'main_3': 23,
 'bonus_1': 7,
 'main_rank': 1,
 'bonus_rank': 2,
 'combination_rank': 1,
 'rank_1_winners': 2,
 'rank_1_gain': 1000000.0,
 'rank_2_winners': 10,
 'rank_2_gain': 50000.0}
```

#### Signature

```python
def to_dict(self) -> dict: ...
```



## FoundCombination

[Show source in models.py:240](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L240)

A class representing a found combination in a lottery search.

#### Signature

```python
class FoundCombination: ...
```



## WinningRank

[Show source in models.py:44](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L44)

A class representing a winning rank in a lottery draw.

#### Signature

```python
class WinningRank: ...
```