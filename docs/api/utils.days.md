<!-- markdownlint-disable -->

<a href="../../src/pactole/utils/days.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.days`
Utilities related to days of the week and lottery draw days. 

**Global Variables**
---------------
- **WEEK**
- **MONDAY**
- **TUESDAY**
- **WEDNESDAY**
- **THURSDAY**
- **FRIDAY**
- **SATURDAY**
- **SUNDAY**
- **DAY_NAMES**
- **NAMES_TO_WEEKDAY**


---

<a href="../../src/pactole/utils/days.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Weekday`
Enumeration for the days of the week. 

It provides utility methods to navigate and calculate differences between weekdays. 



**Args:**
 
 - <b>`value`</b> (Day | Weekday | None):  The day as an integer (0=Monday, 6=Sunday), a Weekday,  a timestamp, or a date. If the day is None, the day of the current date is used. 

 Integers are converted to Weekday. A Weekday enumeration can also be provided directly.  A timestamp can be provided as a float representing seconds since the epoch.  When a string is provided, it must be in the ISO format 'YYYY-MM-DD'.  Both timestamp and string inputs are converted to date objects.  Date objects will be converted to the corresponding weekday. 

 Defaults to None. 



**Raises:**
 
 - <b>`TypeError`</b>:  If the provided day is not an integer, Weekday, or date. 



**Examples:**
 ``` Weekday(0)```
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






---

<a href="../../src/pactole/utils/days.py#L622"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DrawDays`
Utility class to handle lottery draw days. 



**Args:**
 
 - <b>`days`</b> (Iterable[Day | Weekday]):  An iterable of Day or Weekday representing draw days. 



**Examples:**
 ``` draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])```
    >>> draw_days.get_last_draw_date(date(2024, 6, 5))
    datetime.date(2024, 6, 3)
    >>> draw_days.get_next_draw_date(date(2024, 6, 5))
    datetime.date(2024, 6, 6)


<a href="../../src/pactole/utils/days.py#L638"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `DrawDays.__init__`

```python
__init__(days: 'Iterable[Day | Weekday]') → None
```






---

#### <kbd>property</kbd> DrawDays.days

Return the draw days. 



**Returns:**
 
 - <b>`tuple[Weekday, ...]`</b>:  The draw days. 



**Examples:**
 ``` draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])```
    >>> draw_days.days
    (Weekday.MONDAY, Weekday.THURSDAY)




---

<a href="../../src/pactole/utils/days.py#L655"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `DrawDays.get_last_draw_date`

```python
get_last_draw_date(
    from_date: 'Day | Weekday | None' = None,
    closest: 'bool' = True
) → date
```

Return the date of the last lottery draw. 



**Args:**
 
 - <b>`from_date`</b> (Day | Weekday | None, optional):  The starting date. 

 A timestamp can be provided as an integer or float representing  seconds since the epoch. When a string is provided, it must be in the ISO format  'YYYY-MM-DD'. Finally, a date object can be provided directly. 

 Defaults to None. 



**Returns:**
 
 - <b>`date`</b>:  The date of the last lottery draw. 



**Raises:**
 
 - <b>`TypeError`</b>:  If the provided date is not a string, timestamp, or date object. 
 - <b>`ValueError`</b>:  If the string is not a valid date in ISO format. 



**Examples:**
 ``` draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])```
    >>> draw_days.get_last_draw_date(date(2024, 6, 5))
    datetime.date(2024, 6, 3)


---

<a href="../../src/pactole/utils/days.py#L688"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `DrawDays.get_next_draw_date`

```python
get_next_draw_date(
    from_date: 'Day | Weekday | None' = None,
    closest: 'bool' = True
) → date
```

Return the date of the next lottery draw. 



**Args:**
 
 - <b>`from_date`</b> (Day | Weekday | None, optional):  The starting date. 

 A timestamp can be provided as an integer or float representing  seconds since the epoch. When a string is provided, it must be in the ISO format  'YYYY-MM-DD'. Finally, a date object can be provided directly. 

 Defaults to None. 



**Returns:**
 
 - <b>`date`</b>:  The date of the next lottery draw. 



**Raises:**
 
 - <b>`TypeError`</b>:  If the provided date is not a string, timestamp, or date object. 
 - <b>`ValueError`</b>:  If the string is not a valid date in ISO format. 



**Examples:**
 ``` draw_days = DrawDays([Weekday.MONDAY, Weekday.THURSDAY])```
    >>> draw_days.get_next_draw_date(date(2024, 6, 5))
    datetime.date(2024, 6, 6)





---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
