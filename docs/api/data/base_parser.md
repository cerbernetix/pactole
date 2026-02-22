# BaseParser

[Pactole Index](../README.md#pactole-index) / [Data](./index.md#data) / BaseParser

> Auto-generated documentation for [data.base_parser](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_parser.py) module.

- [BaseParser](#baseparser)
  - [BaseParser](#baseparser-1)
    - [BaseParser().__call__](#baseparser()__call__)
    - [BaseParser().combination_factory](#baseparser()combination_factory)

## BaseParser

[Show source in base_parser.py:9](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_parser.py#L9)

A base class for data parsers.

#### Arguments

combination_factory (CombinationFactory | LotteryCombination | Any): A factory function
    or class to create a combination instance. If None, a default LotteryCombination
    instance will be used. Default is None.

#### Examples

```python
>>> class MyParser(BaseParser):
...     def __call__(self, data: dict) -> DrawRecord:
...         # Implement parsing logic here
...         return DrawRecord(...)
>>> parser = MyParser()
>>> record = parser({
...     "date": "2022-01-15",
...     "deadline": "2022-02-15",
...     "main_1": 12,
...     "main_2": 5,
...     "main_3": 23,
...     "bonus_1": 7,
... })
>>> print(record)
DrawRecord(
    period='202201',
    draw_date=datetime.date(2022, 1, 15),
    deadline_date=datetime.date(2022, 2, 15),
    combination=...,
    numbers=...,
    winning_ranks=...)
```

#### Signature

```python
class BaseParser:
    def __init__(
        self, combination_factory: CombinationFactory | LotteryCombination | Any = None
    ) -> None: ...
```

### BaseParser().__call__

[Show source in base_parser.py:49](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_parser.py#L49)

Parse a line of data and return a DrawRecord.

#### Arguments

- [Data](./index.md#data) *dict* - A dictionary representing a line of data.

#### Returns

- `DrawRecord` - The record parsed from the line of data.

#### Examples

```python
>>> class SimpleParser(BaseParser):
...     def __call__(self, data: dict) -> DrawRecord:
...         return DrawRecord(
...             period=data["date"][:7].replace("-", ""),
...             draw_date=datetime.date.fromisoformat(data["date"]),
...             deadline_date=datetime.date.fromisoformat(data["deadline"]),
...             combination=None,
...             numbers={},
...             winning_ranks=[],
...         )
>>> parser = SimpleParser()
>>> record = parser({"date": "2022-01-15", "deadline": "2022-02-15", ... }, factory)
>>> print(record)
DrawRecord(
    period='202201',
    draw_date=datetime.date(2022, 1, 15),
    deadline_date=datetime.date(2022, 2, 15),
    combination=None,
    numbers={},
    winning_ranks=[])
```

#### Signature

```python
def __call__(self, data: dict) -> DrawRecord: ...
```

### BaseParser().combination_factory

[Show source in base_parser.py:82](https://github.com/cerbernetix/pactole/blob/main/src/pactole/data/base_parser.py#L82)

Get the combination factory.

#### Returns

- `CombinationFactory` - The combination factory used by this parser.

#### Examples

```python
>>> parser = BaseParser()
>>> factory = parser.combination_factory
>>> print(factory)
<function LotteryCombination.get_combination at 0x...>
```

#### Signature

```python
@property
def combination_factory(self) -> CombinationFactory: ...
```