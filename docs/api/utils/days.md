# Days

[Pactole Index](../README.md#pactole-index) / [Utils](./index.md#utils) / Days

> Auto-generated documentation for [utils.days](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py) module.

- [Days](#days)
  - [DrawDays](#drawdays)
    - [DrawDays().days](#drawdays()days)
    - [DrawDays().get_last_draw_date](#drawdays()get_last_draw_date)
    - [DrawDays().get_next_draw_date](#drawdays()get_next_draw_date)
  - [Weekday](#weekday)
    - [Weekday._missing_](#weekday_missing_)
    - [Weekday().closest](#weekday()closest)
    - [Weekday().closest_date](#weekday()closest_date)
    - [Weekday().furthest](#weekday()furthest)
    - [Weekday().furthest_date](#weekday()furthest_date)
    - [Weekday.get_date](#weekdayget_date)
    - [Weekday.get_day](#weekdayget_day)
    - [Weekday().next](#weekday()next)
    - [Weekday().next_date](#weekday()next_date)
    - [Weekday().previous](#weekday()previous)
    - [Weekday().previous_date](#weekday()previous_date)
    - [Weekday().since](#weekday()since)

## DrawDays

[Show source in days.py:622](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L622)

Utility class to handle lottery draw days.

#### Arguments

days (Iterable[Day | Weekday]): An iterable of Day or Weekday representing draw days.

#### Examples

```python
>>> draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])
>>> draw_days.get_last_draw_date(date(2024, 6, 5))
datetime.date(2024, 6, 3)
>>> draw_days.get_next_draw_date(date(2024, 6, 5))
datetime.date(2024, 6, 6)
```

#### Signature

```python
class DrawDays:
    def __init__(self, days: Iterable[Day | Weekday]) -> None: ...
```

### DrawDays().days

[Show source in days.py:641](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L641)

Return the draw days.

#### Returns

- `tuple[Weekday,` *...]* - The draw days.

#### Examples

```python
>>> draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])
>>> draw_days.days
(Weekday.MONDAY, Weekday.THURSDAY)
```

#### Signature

```python
@property
def days(self) -> tuple[Weekday, ...]: ...
```

#### See also

- [Weekday](#weekday)

### DrawDays().get_last_draw_date

[Show source in days.py:655](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L655)

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
>>> draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])
>>> draw_days.get_last_draw_date(date(2024, 6, 5))
datetime.date(2024, 6, 3)
```

#### Signature

```python
def get_last_draw_date(
    self, from_date: Day | Weekday | None = None, closest: bool = True
) -> date: ...
```

### DrawDays().get_next_draw_date

[Show source in days.py:688](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L688)

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
>>> draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])
>>> draw_days.get_next_draw_date(date(2024, 6, 5))
datetime.date(2024, 6, 6)
```

#### Signature

```python
def get_next_draw_date(
    self, from_date: Day | Weekday | None = None, closest: bool = True
) -> date: ...
```



## Weekday

[Show source in days.py:18](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L18)

Enumeration for the days of the week.

It provides utility methods to navigate and calculate differences between weekdays.

#### Arguments

value (Day | Weekday | None): The day as an integer (0=Monday, 6=Sunday), a Weekday,
    a timestamp, or a date. If the day is None, the day of the current date is used.

Integers are converted to Weekday. A Weekday enumeration can also be provided directly.
A timestamp can be provided as a float representing seconds since the epoch.
When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
Both timestamp and string inputs are converted to date objects.
Date objects will be converted to the corresponding weekday.

Defaults to None.

#### Raises

- `TypeError` - If the provided day is not an integer, Weekday, or date.

#### Examples

```python
>>> Weekday(0)
Weekday.MONDAY
>>> Weekday("2023-03-15")
Weekday.WEDNESDAY
>>> Weekday(datetime.date(2023, 3, 15))
Weekday.WEDNESDAY
>>> Weekday.today()
Weekday.<CURRENT_DAY>
>>> Weekday(None)
Weekday.<CURRENT_DAY>
>>> Weekday.WEDNESDAY.next()
Weekday.THURSDAY
>>> Weekday.WEDNESDAY.until(Weekday.FRIDAY)
2
>>> Weekday.FRIDAY.next_date("2023-03-15")
datetime.date(2023, 3, 17)
```

#### Signature

```python
class Weekday(Enum): ...
```

### Weekday._missing_

[Show source in days.py:65](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L65)

Create Weekday from various input types.

#### Signature

```python
@classmethod
def _missing_(cls, value: Day | Weekday | None = None) -> None: ...
```

### Weekday().closest

[Show source in days.py:252](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L252)

Get the number of days to the closest occurrence of a given weekday.

If no target day is provided, the day of the current date is used.

#### Arguments

day (Day | Weekday | None, optional): The target day as an integer (0=Monday, 6=Sunday),
    a Weekday, a timestamp, or a date.

Integers are converted to Weekday. A Weekday enumeration can also be provided.
A timestamp can be provided as a float representing seconds since the epoch.
When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
Both timestamp and string inputs are converted to date objects.
Date objects will be converted to the corresponding weekday.

Defaults to None.

#### Returns

- `int` - The number of days to the closest occurrence of the target weekday.

#### Raises

- `TypeError` - If the provided day is not an integer, Weekday, or date.

#### Examples

```python
>>> today = Weekday.WEDNESDAY
>>> today.closest(Weekday.FRIDAY)
2
>>> today.closest(Weekday.MONDAY)
-2
>>> today.closest(Weekday.WEDNESDAY)
0
```

#### Signature

```python
def closest(self, day: Day | Weekday | None = None) -> int: ...
```

### Weekday().closest_date

[Show source in days.py:420](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L420)

Get the closest date for this weekday from a given date.

If no date is provided, the current date is used.

#### Arguments

from_date (Day | None, optional): The starting date.

A timestamp can be provided as an integer or float representing
seconds since the epoch. When a string is provided, it must be in the ISO format
'YYYY-MM-DD'. Finally, a date object can be provided directly.

Defaults to None.

#### Returns

- `date` - The closest date for this weekday.

#### Raises

- `TypeError` - If the provided date is not a string, timestamp, or date object.
- `ValueError` - If the string is not a valid date in ISO format.

#### Examples

```python
>>> today = datetime.date(2023, 3, 15)
>>> Weekday.FRIDAY.closest_date(today)
datetime.date(2023, 3, 17)
>>> Weekday.MONDAY.closest_date(today)
datetime.date(2023, 3, 13)
>>> Weekday.WEDNESDAY.closest_date(today)
datetime.date(2023, 3, 15)
```

#### Signature

```python
def closest_date(self, from_date: Day | None = None) -> date: ...
```

### Weekday().furthest

[Show source in days.py:294](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L294)

Get the number of days to the furthest occurrence of a given weekday from this day.

If no target day is provided, the day of the current date is used.

#### Arguments

day (Day | Weekday | None, optional): The target day as an integer (0=Monday, 6=Sunday),
    a Weekday, a timestamp, or a date.

Integers are converted to Weekday. A Weekday enumeration can also be provided.
A timestamp can be provided as a float representing seconds since the epoch.
When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
Both timestamp and string inputs are converted to date objects.
Date objects will be converted to the corresponding weekday.

Defaults to None.

#### Returns

- `int` - The number of days to the furthest occurrence of the target weekday.

#### Raises

- `TypeError` - If the provided day is not an integer, Weekday, or date.

#### Examples

```python
>>> today = Weekday.WEDNESDAY
>>> today.furthest(Weekday.FRIDAY)
-5
>>> today.furthest(Weekday.MONDAY)
5
>>> today.furthest(Weekday.WEDNESDAY)
7
```

#### Signature

```python
def furthest(self, day: Day | Weekday | None = None) -> int: ...
```

### Weekday().furthest_date

[Show source in days.py:459](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L459)

Get the furthest date for this weekday from a given date.

If no date is provided, the current date is used.

#### Arguments

from_date (Day | None, optional): The starting date.

A timestamp can be provided as an integer or float representing
seconds since the epoch. When a string is provided, it must be in the ISO format
'YYYY-MM-DD'. Finally, a date object can be provided directly.

Defaults to None.

#### Returns

- `date` - The furthest date for this weekday.

#### Raises

- `TypeError` - If the provided date is not a string, timestamp, or date object.
- `ValueError` - If the string is not a valid date in ISO format.

#### Examples

```python
>>> today = datetime.date(2023, 3, 15)
>>> Weekday.FRIDAY.furthest_date(today)
datetime.date(2023, 3, 10)
>>> Weekday.MONDAY.furthest_date(today)
datetime.date(2023, 3, 20)
>>> Weekday.WEDNESDAY.furthest_date(today)
datetime.date(2023, 3, 22)
```

#### Signature

```python
def furthest_date(self, from_date: Day | None = None) -> date: ...
```

### Weekday.get_date

[Show source in days.py:567](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L567)

Get the date from a string, timestamp, or a date object.

If the date is None, the current date is returned.

#### Arguments

from_date (Day | None, optional): The date as a string in ISO format, a timestamp,
    or a date object.

A timestamp can be provided as an integer or float representing
seconds since the epoch.

When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.

Finally, a date object can be provided directly, in which case it is returned as is.

Defaults to None.

#### Returns

- `date` - The corresponding date object.

#### Raises

- `TypeError` - If the provided date is not a string, timestamp, or date object.
- `ValueError` - If the string is not a valid date in ISO format.

#### Examples

```python
>>> Weekday.get_date()
datetime.date(<CURRENT_YEAR>, <CURRENT_MONTH>, <CURRENT_DAY>)
>>> Weekday.get_date("2023-03-15")
datetime.date(2023, 3, 15)
>>> Weekday.get_date(datetime.date(2023, 3, 15))
datetime.date(2023, 3, 15)
>>> Weekday.get_date(1678838400)
datetime.date(2023, 3, 15)
>>> Weekday.get_date("15-03-2023")
Raises ValueError
```

#### Signature

```python
@staticmethod
def get_date(from_date: Day | None = None) -> date: ...
```

### Weekday.get_day

[Show source in days.py:511](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L511)

Get the Weekday enumeration from an integer.

If the day is None, the day of the current date is returned.

#### Arguments

day (Day | Weekday | None): The day as an integer (0=Monday, 6=Sunday), a Weekday,
    a timestamp, or a date.

A Weekday enumeration can be provided directly, in which case it is
returned as is. Integers are converted to Weekday.

A timestamp can be provided as a float representing seconds since the epoch.
When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
Both timestamp and string inputs are converted to date objects.
Date objects will be converted to the corresponding weekday.

Defaults to None.

#### Returns

- [Weekday](#weekday) - The corresponding Weekday enumeration.

#### Raises

- `TypeError` - If the provided day is not an integer, Weekday, or date.

#### Examples

```python
>>> Weekday.get_day()
Weekday.<CURRENT_DAY>
>>> Weekday.get_day(2)
Weekday.WEDNESDAY
>>> Weekday.get_day(Weekday.FRIDAY)
Weekday.FRIDAY
>>> Weekday.get_day("2023-03-15")
Weekday.WEDNESDAY
>>> Weekday.get_day("Tuesday")
Weekday.TUESDAY
>>> Weekday.get_day("April")
Raises TypeError
```

#### Signature

```python
@classmethod
def get_day(cls, day: Day | Weekday | None = None) -> Weekday: ...
```

### Weekday().next

[Show source in days.py:87](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L87)

Get a Weekday representing the next day of the week.

#### Arguments

days (Day | Weekday | Iterable[Day | Weekday] | None, optional): The target day(s) as
    an integer (0=Monday, 6=Sunday), a Weekday, a timestamp, or a date. Accepts multiple
    days as an iterable.

When None is provided, simply returns the next day of the week. Otherwise, finds the
next occurrence among the provided days.

Integers are converted to Weekday. A Weekday enumeration can also be provided.
A timestamp can be provided as a float representing seconds since the epoch.
When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
Both timestamp and string inputs are converted to date objects.
Date objects will be converted to the corresponding weekday.

Defaults to None.

#### Returns

- [Weekday](#weekday) - A Weekday enumeration representing the next day of the week.

#### Raises

- `TypeError` - If the provided day is not an integer, Weekday, or date.

#### Examples

```python
>>> today = Weekday.WEDNESDAY
>>> today.next()
Weekday.THURSDAY
>>> today.next(Weekday.MONDAY)
Weekday.MONDAY
>>> today.next([Weekday.FRIDAY, Weekday.SUNDAY])
Weekday.FRIDAY
```

#### Signature

```python
def next(
    self, days: Day | Weekday | Iterable[Day | Weekday] | None = None
) -> Weekday: ...
```

### Weekday().next_date

[Show source in days.py:336](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L336)

Get the next date for this weekday from a given date.

If no date is provided, the current date is used.

#### Arguments

from_date (Day | None, optional): The starting date.

A timestamp can be provided as an integer or float representing
seconds since the epoch. When a string is provided, it must be in the ISO format
'YYYY-MM-DD'. Finally, a date object can be provided directly.

    Defaults to None.
- [Weekday().closest](#weekdayclosest) *bool* - If True, get the closest date (past or future). Defaults to False.

#### Returns

- `date` - The next date for this weekday.

#### Raises

- `TypeError` - If the provided date is not a string, timestamp, or date object.
- `ValueError` - If the string is not a valid date in ISO format.

#### Examples

```python
>>> today = datetime.date(2023, 3, 15)
>>> Weekday.FRIDAY.next_date(today)
datetime.date(2023, 3, 17)
>>> Weekday.MONDAY.next_date(today)
datetime.date(2023, 3, 20)
>>> Weekday.WEDNESDAY.next_date(today)
datetime.date(2023, 3, 22)
>>> Weekday.WEDNESDAY.next_date(today, closest=True)
datetime.date(2023, 3, 15)
```

#### Signature

```python
def next_date(self, from_date: Day | None = None, closest: bool = False) -> date: ...
```

### Weekday().previous

[Show source in days.py:134](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L134)

Get a Weekday representing the previous day of the week.

#### Arguments

days (Day | Weekday | Iterable[Day | Weekday] | None, optional): The target day(s) as
    an integer (0=Monday, 6=Sunday), a Weekday, a timestamp, or a date. Accepts multiple
    days as an iterable.

When None is provided, simply returns the previous day of the week. Otherwise, finds
the previous occurrence among the provided days.

Integers are converted to Weekday. A Weekday enumeration can also be provided.
A timestamp can be provided as a float representing seconds since the epoch.
When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
Both timestamp and string inputs are converted to date objects.
Date objects will be converted to the corresponding weekday.

Defaults to None.

#### Returns

- [Weekday](#weekday) - A Weekday enumeration representing the previous day of the week.

#### Raises

- `TypeError` - If the provided day is not an integer, Weekday, or date.

#### Examples

```python
>>> today = Weekday.WEDNESDAY
>>> today.previous()
Weekday.TUESDAY
>>> today.previous(Weekday.MONDAY)
Weekday.MONDAY
>>> today.previous([Weekday.FRIDAY, Weekday.SUNDAY])
Weekday.SUNDAY
```

#### Signature

```python
def previous(
    self, days: Day | Weekday | Iterable[Day | Weekday] | None = None
) -> Weekday: ...
```

### Weekday().previous_date

[Show source in days.py:378](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L378)

Get the previous date for this weekday from a given date.

If no date is provided, the current date is used.

#### Arguments

from_date (Day | None, optional): The starting date.

A timestamp can be provided as an integer or float representing
seconds since the epoch. When a string is provided, it must be in the ISO format
'YYYY-MM-DD'. Finally, a date object can be provided directly.

    Defaults to None.
- [Weekday().closest](#weekdayclosest) *bool* - If True, get the closest date (past or future). Defaults to False.

#### Returns

- `date` - The previous date for this weekday.

#### Raises

- `TypeError` - If the provided date is not a string, timestamp, or date object.
- `ValueError` - If the string is not a valid date in ISO format.

#### Examples

```python
>>> today = datetime.date(2023, 3, 15)
>>> Weekday.MONDAY.previous_date(today)
datetime.date(2023, 3, 13)
>>> Weekday.FRIDAY.previous_date(today)
datetime.date(2023, 3, 10)
>>> Weekday.WEDNESDAY.previous_date(today)
datetime.date(2023, 3, 8)
>>> Weekday.WEDNESDAY.previous_date(today, closest=True)
datetime.date(2023, 3, 15)
```

#### Signature

```python
def previous_date(self, from_date: Day | None = None, closest: bool = False) -> date: ...
```

### Weekday().since

[Show source in days.py:216](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L216)

Get the number of days since the previous occurrence of a given weekday.

If no target day is provided, the day of the current date is used.

#### Arguments

day (Day | Weekday | None, optional): The target day as an integer (0=Monday, 6=Sunday),
    a Weekday, a timestamp, or a date.

Integers are converted to Weekday. A Weekday enumeration can also be provided.
A timestamp can be provided as a float representing seconds since the epoch.
When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
Both timestamp and string inputs are converted to date objects.
Date objects will be converted to the corresponding weekday.

Defaults to None.

#### Returns

- `int` - The number of days since the previous occurrence of the target weekday.

#### Raises

- `TypeError` - If the provided day is not an integer, Weekday, or date.

#### Examples

```python
>>> today = Weekday.WEDNESDAY
>>> today.since(Weekday.MONDAY)
2
>>> today.since(Weekday.FRIDAY)
5
>>> today.since(Weekday.WEDNESDAY)
7
```

```

#### Signature

```python
def since(self, day: Day | Weekday | None = None) -> int: ...
```

### Weekday.today

[Show source in days.py:498](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L498)

Get the current day of the week, as a Weekday enumeration.

#### Returns

- [Weekday](#weekday) - A Weekday enumeration representing the current day of the week.

#### Examples

```python
>>> Weekday.today()
Weekday.<CURRENT_DAY>
```

#### Signature

```python
@classmethod
def today(cls) -> Weekday: ...
```

### Weekday().until

[Show source in days.py:181](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/days.py#L181)

Get the number of days until the next occurrence of a given weekday.

If no target day is provided, the day of the current date is used.

#### Arguments

day (Day | Weekday | None, optional): The target day as an integer (0=Monday, 6=Sunday),
    a Weekday, a timestamp, or a date.

Integers are converted to Weekday. A Weekday enumeration can also be provided.
A timestamp can be provided as a float representing seconds since the epoch.
When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.
Both timestamp and string inputs are converted to date objects.
Date objects will be converted to the corresponding weekday.

Defaults to None.

#### Returns

- `int` - The number of days until the next occurrence of the target weekday.

#### Raises

- `TypeError` - If the provided day is not an integer, Weekday, or date.

#### Examples

```python
>>> today = Weekday.WEDNESDAY
>>> today.until(Weekday.FRIDAY)
2
>>> today.until(Weekday.MONDAY)
5
>>> today.until(Weekday.WEDNESDAY)
7
```

#### Signature

```python
def until(self, day: Day | Weekday | None = None) -> int: ...
```