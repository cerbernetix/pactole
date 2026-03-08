# Types

[Pactole Index](../README.md#pactole-index) / [Utils](./index.md#utils) / Types

> Auto-generated documentation for [utils.types](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/types.py) module.

- [Types](#types)
  - [assert_non_negative_integer](#assert_non_negative_integer)
  - [get_float](#get_float)
  - [get_int](#get_int)

## assert_non_negative_integer

[Show source in types.py:54](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/types.py#L54)

Assert that a value is a non-negative integer.

#### Arguments

- `value` - The value to check.
- `name` - The name of the value for error messages. Defaults to "value".

#### Raises

- `ValueError` - If the value is not a non-negative integer.

#### Examples

```python
>>> assert_non_negative_integer(5)
>>> assert_non_negative_integer(-1)
Traceback (most recent call last):
    ...
ValueError: value must be a non-negative integer, got -1
```

#### Signature

```python
def assert_non_negative_integer(value: int, name: str = "value") -> None: ...
```



## get_float

[Show source in types.py:28](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/types.py#L28)

Convert a value to a float, if possible.

#### Arguments

- `value` - The value to convert.
- `default` - The default value to return if conversion fails. Defaults to 0.0.

#### Returns

- `float` - The converted float value, or the default if conversion fails.

#### Examples

```python
>>> get_float("3.14")
3.14
>>> get_float("abc", default=1.0)
1.0
>>> get_float(None, default=2.5)
2.5
```

#### Signature

```python
def get_float(value, default: float = 0.0) -> float: ...
```



## get_int

[Show source in types.py:4](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/types.py#L4)

Convert a value to an integer, if possible.

#### Arguments

- `value` - The value to convert.
- `default` - The default value to return if conversion fails. Defaults to 0.

#### Returns

- `int` - The converted integer value, or the default if conversion fails.

#### Examples

```python
>>> get_int("42")
42
>>> get_int("abc", default=10)
10
>>> get_int(None, default=5)
5
```

#### Signature

```python
def get_int(value, default: int = 0) -> int: ...
```