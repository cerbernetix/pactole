# Types

[Pactole Index](../README.md#pactole-index) / [Utils](./index.md#utils) / Types

> Auto-generated documentation for [utils.types](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/types.py) module.

- [Types](#types)
  - [get_float](#get_float)
  - [get_int](#get_int)

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