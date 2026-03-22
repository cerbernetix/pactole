# Models

[Pactole Index](../README.md#pactole-index) / [Data](./index.md#data) / Models

> Auto-generated documentation for [data.models](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py) module.

- [Models](#models)
  - [ArchiveContentInfo](#archivecontentinfo)
  - [ArchiveInfo](#archiveinfo)
  - [DrawRecord](#drawrecord)
    - [DrawRecord.from_csv](#drawrecordfrom_csv)
    - [DrawRecord.from_dict](#drawrecordfrom_dict)
    - [DrawRecord.from_json](#drawrecordfrom_json)
    - [DrawRecord().to_csv](#drawrecord()to_csv)
    - [DrawRecord().to_dict](#drawrecord()to_dict)
    - [DrawRecord().to_json](#drawrecord()to_json)
  - [FoundCombination](#foundcombination)
    - [FoundCombination.from_csv](#foundcombinationfrom_csv)
    - [FoundCombination.from_dict](#foundcombinationfrom_dict)
    - [FoundCombination.from_json](#foundcombinationfrom_json)
    - [FoundCombination().to_csv](#foundcombination()to_csv)
    - [FoundCombination().to_dict](#foundcombination()to_dict)
    - [FoundCombination().to_json](#foundcombination()to_json)
  - [WinningRank](#winningrank)

## ArchiveContentInfo

[Show source in models.py:25](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L25)

A dictionary containing information about the content of an archive.

#### Signature

```python
class ArchiveContentInfo(TypedDict): ...
```



## ArchiveInfo

[Show source in models.py:34](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L34)

A dictionary containing information about an archive.

#### Signature

```python
class ArchiveInfo(ArchiveContentInfo): ...
```

#### See also

- [ArchiveContentInfo](#archivecontentinfo)



## DrawRecord

[Show source in models.py:59](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L59)

A class representing a record of a lottery draw.

#### Signature

```python
class DrawRecord: ...
```

### DrawRecord.from_csv

[Show source in models.py:206](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L206)

Create a DrawRecord instance from a CSV dictionary.

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
>>> record = DrawRecord.from_csv(data)
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
def from_csv(
    data: dict, combination_factory: CombinationFactory | None = None
) -> DrawRecord: ...
```

### DrawRecord.from_dict

[Show source in models.py:354](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L354)

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
...     "combination": {'main': [12, 5, 23], 'bonus': [7]},
...     "numbers": [12, 5, 23, 7],
...     "winning_ranks": [
...         {'rank': 1, 'winners': 2, 'gain': 1000000.0},
...         {'rank': 2, 'winners': 10, 'gain': 50000.0}
...     ]
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

### DrawRecord.from_json

[Show source in models.py:311](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L311)

Create a DrawRecord instance from a JSON dictionary.

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
...     "combination": {'main': [12, 5, 23], 'bonus': [7]},
...     "numbers": [12, 5, 23, 7],
...     "winning_ranks": [
...         {'rank': 1, 'winners': 2, 'gain': 1000000.0},
...         {'rank': 2, 'winners': 10, 'gain': 50000.0}
...     ]
... }
>>> record = DrawRecord.from_json(data)
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
@classmethod
def from_json(
    cls, data: dict, combination_factory: CombinationFactory | None = None
) -> DrawRecord: ...
```

### DrawRecord().to_csv

[Show source in models.py:80](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L80)

Convert the DrawRecord instance to a dictionary suitable for CSV export.

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
>>> record.to_csv()
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
def to_csv(self) -> dict: ...
```

### DrawRecord().to_dict

[Show source in models.py:165](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L165)

Convert the DrawRecord instance to a dictionary.

#### Returns

- `dict` - A dictionary representation of the DrawRecord instance.

#### Examples

```python
>>> record = DrawRecord(
...     period="202201",
...     draw_date=datetime.date(2022, 1, 15),
...     deadline_date=datetime.date(2022, 2, 15),
...     combination=LotteryCombination(components={'main': ..., 'bonus': ...}),
...     numbers={'main': [12, 5, 23], 'bonus': [7]},
...     winning_ranks=[
...         WinningRank(rank=1, winners=2, gain=1000000.0),
...         WinningRank(rank=2, winners=10, gain=50000.0)
...     ]
... )
>>> record.to_dict()
{'period': '202201',
 'draw_date': '2022-01-15',
 'deadline_date': '2022-02-15',
 'combination': {'main': [12, 5, 23], 'bonus': [7]},
 'numbers': [12, 5, 23, 7],
 'winning_ranks': [
     {'rank': 1, 'winners': 2, 'gain': 1000000.0},
     {'rank': 2, 'winners': 10, 'gain': 50000.0}
 ]}
```

#### Signature

```python
def to_dict(self) -> dict: ...
```

### DrawRecord().to_json

[Show source in models.py:134](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L134)

Convert the DrawRecord instance to a JSON-serializable dictionary.

#### Returns

- `dict` - A JSON-serializable dictionary representation of the DrawRecord instance.

#### Examples

```python
>>> record = DrawRecord(
...     period="202201",
...     draw_date=datetime.date(2022, 1, 15),
...     deadline_date=datetime.date(2022, 2, 15),
...     combination=LotteryCombination(components={'main': ..., 'bonus': ...}),
...     numbers={'main': [12, 5, 23], 'bonus': [7]},
...     winning_ranks=[
...         WinningRank(rank=1, winners=2, gain=1000000.0),
...         WinningRank(rank=2, winners=10, gain=50000.0)
...     ]
... )
>>> record.to_json()
{'period': '202201',
 'draw_date': '2022-01-15',
 'deadline_date': '2022-02-15',
 'combination': {'main': [12, 5, 23], 'bonus': [7]},
 'numbers': [12, 5, 23, 7],
 'winning_ranks': [
     {'rank': 1, 'winners': 2, 'gain': 1000000.0},
     {'rank': 2, 'winners': 10, 'gain': 50000.0}
 ]}
```

#### Signature

```python
def to_json(self) -> dict: ...
```



## FoundCombination

[Show source in models.py:429](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L429)

A class representing a found combination in a lottery search.

#### Signature

```python
class FoundCombination: ...
```

### FoundCombination.from_csv

[Show source in models.py:514](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L514)

Create a FoundCombination instance from a CSV dictionary.

#### Arguments

- [Data](./index.md#data) *dict* - A dictionary containing the found combination data.
combination_factory (CombinationFactory | None): A factory function or class to create a
    combination instance. If None, a default LotteryCombination instance will be used.
    Default is None.

#### Returns

- [FoundCombination](#foundcombination) - An instance of FoundCombination created from the input dictionary.

#### Examples

```python
>>> data = {
...     'period': '202201',
...     'draw_date': '2022-01-15',
...     'deadline_date': '2022-02-15',
...     'main_1': 12,
...     'main_2': 5,
...     'main_3': 23,
...     'bonus_1': 7,
...     'main_rank': 1,
...     'bonus_rank': 2,
...     'combination_rank': 1,
...     'rank_1_winners': 2,
...     'rank_1_gain': 1000000.0,
...     'rank_2_winners': 10,
...     'rank_2_gain': 50000.0,
...     'rank': 1,
...     'match': 'main: [5, 12, 23]  bonus: [7]'
... }
>>> found = FoundCombination.from_csv(data)
>>> print(found)
FoundCombination(
    record=DrawRecord(...),
    rank=CombinationRank(...),
    match=CompoundCombination(...)
)
```

#### Signature

```python
@staticmethod
def from_csv(
    data: dict, combination_factory: CombinationFactory | None = None
) -> FoundCombination: ...
```

### FoundCombination.from_dict

[Show source in models.py:598](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L598)

Create a FoundCombination instance from a dictionary.

#### Arguments

- [Data](./index.md#data) *dict* - A dictionary containing the found combination data.
combination_factory (CombinationFactory | None): A factory function or class to create a
    combination instance. If None, a default LotteryCombination instance will be used.
    Default is None.

#### Returns

- [FoundCombination](#foundcombination) - An instance of FoundCombination created from the input dictionary.

#### Examples

```python
>>> data = {
...     'record': {...},
...     'rank': ...,
...     'match': {...},
... }
>>> found = FoundCombination.from_dict(data)
>>> print(found)
FoundCombination(
    record=DrawRecord(...),
    rank=CombinationRank(...),
    match=CompoundCombination(...)
)
```

#### Signature

```python
@staticmethod
def from_dict(
    data: dict, combination_factory: CombinationFactory | None = None
) -> FoundCombination: ...
```

### FoundCombination.from_json

[Show source in models.py:567](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L567)

Create a FoundCombination instance from a JSON dictionary.

#### Arguments

- [Data](./index.md#data) *dict* - A dictionary containing the found combination data.
combination_factory (CombinationFactory | None): A factory function or class to create a
    combination instance. If None, a default LotteryCombination instance will be used.
    Default is None.

#### Returns

- [FoundCombination](#foundcombination) - An instance of FoundCombination created from the input dictionary.

#### Examples

```python
>>> data = {
...     'record': {...},
...     'rank': ...,
...     'match': {...},
... }
>>> found = FoundCombination.from_json(data)
>>> print(found)
FoundCombination(
    record=DrawRecord(...),
    rank=CombinationRank(...),
    match=CompoundCombination(...)
)
```

#### Signature

```python
@classmethod
def from_json(
    cls, data: dict, combination_factory: CombinationFactory | None = None
) -> FoundCombination: ...
```

### FoundCombination().to_csv

[Show source in models.py:441](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L441)

Convert the FoundCombination instance to a dictionary suitable for CSV export.

#### Returns

- `dict` - A dictionary representation of the FoundCombination instance.

#### Examples

```python
>>> found = FoundCombination(
...     record=DrawRecord(...),
...     rank=CombinationRank(...),
...     match=CompoundCombination(...)
... )
>>> found.to_csv()
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
 'rank_2_gain': 50000.0,
 'rank': 1,
 'match':'main: [5, 12, 23]  bonus: [7]'}
```

#### Signature

```python
def to_csv(self) -> dict: ...
```

### FoundCombination().to_dict

[Show source in models.py:493](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L493)

Convert the FoundCombination instance to a dictionary.

#### Returns

- `dict` - A dictionary representation of the FoundCombination instance.

#### Examples

```python
>>> found = FoundCombination(
...     record=DrawRecord(...),
...     rank=CombinationRank(...),
...     match=CompoundCombination(...)
... )
>>> found.to_dict()
{'record': {...}, 'rank': ..., 'match': {...}}
```

#### Signature

```python
def to_dict(self) -> dict: ...
```

### FoundCombination().to_json

[Show source in models.py:476](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L476)

Convert the FoundCombination instance to a JSON-serializable dictionary.

#### Returns

- `dict` - A JSON-serializable dictionary representation of the FoundCombination instance.

#### Examples

```python
>>> found = FoundCombination(
...     record=DrawRecord(...),
...     rank=CombinationRank(...)
...     match=CompoundCombination(...)
... )
>>> found.to_json()
{'record': {...}, 'rank': ..., 'match': {...}}
```

#### Signature

```python
def to_json(self) -> dict: ...
```



## WinningRank

[Show source in models.py:45](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/models.py#L45)

A class representing a winning rank in a lottery draw.

#### Signature

```python
class WinningRank: ...
```