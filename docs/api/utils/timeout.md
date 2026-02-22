# Timeout

[Pactole Index](../README.md#pactole-index) / [Utils](./index.md#utils) / Timeout

> Auto-generated documentation for [utils.timeout](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/timeout.py) module.

- [Timeout](#timeout)
  - [Timeout](#timeout-1)
    - [Timeout().elapsed](#timeout()elapsed)
    - [Timeout().expired](#timeout()expired)
    - [Timeout().remaining](#timeout()remaining)
    - [Timeout().reset](#timeout()reset)
    - [Timeout().seconds](#timeout()seconds)
    - [Timeout().seconds](#timeout()seconds-1)
    - [Timeout().start](#timeout()start)
    - [Timeout().started](#timeout()started)
    - [Timeout().stop](#timeout()stop)

## Timeout

[Show source in timeout.py:6](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/timeout.py#L6)

A class to represent a timeout duration.

#### Arguments

- `seconds` *float* - The duration of the timeout in seconds.
- `start` *bool, optional* - Whether to start the timeout immediately. Defaults to True.

#### Examples

```python
>>> timeout = Timeout(5)
>>> timeout.seconds
5
>>> timeout.elapsed
0.0
>>> timeout.remaining
5.0
>>> timeout.expired
False
>>> time.sleep(6)
>>> timeout.elapsed
6.0
>>> timeout.remaining
0.0
>>> timeout.expired
True
>>> timeout.reset()
>>> timeout.elapsed
0.0
>>> timeout.remaining
5.0
>>> timeout.expired
False
```

#### Signature

```python
class Timeout:
    def __init__(self, seconds: float, start: bool = True) -> None: ...
```

### Timeout().elapsed

[Show source in timeout.py:94](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/timeout.py#L94)

Return the elapsed time since the timeout was started.

#### Returns

- `float` - The elapsed time in seconds.

#### Examples

```python
>>> timeout = Timeout(5)
>>> timeout.elapsed
0.0
>>> time.sleep(2)
>>> timeout.elapsed
2.0
```

#### Signature

```python
@property
def elapsed(self) -> float: ...
```

### Timeout().expired

[Show source in timeout.py:132](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/timeout.py#L132)

Return True if the timeout has expired, False otherwise.

#### Returns

- `bool` - True if the timeout has expired, False otherwise.

#### Examples

```python
>>> timeout = Timeout(5)
>>> timeout.expired
False
>>> time.sleep(6)
>>> timeout.expired
True
```

#### Signature

```python
@property
def expired(self) -> bool: ...
```

### Timeout().remaining

[Show source in timeout.py:113](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/timeout.py#L113)

Return the remaining time before the timeout expires.

#### Returns

- `float` - The remaining time in seconds.

#### Examples

```python
>>> timeout = Timeout(5)
>>> timeout.remaining
5.0
>>> time.sleep(2)
>>> timeout.remaining
3.0
```

#### Signature

```python
@property
def remaining(self) -> float: ...
```

### Timeout().reset

[Show source in timeout.py:166](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/timeout.py#L166)

Reset the timeout to start counting from now.

#### Examples

```python
>>> timeout = Timeout(5)
>>> time.sleep(3)
>>> timeout.elapsed
3.0
>>> timeout.reset()
>>> timeout.elapsed
0.0
```

#### Signature

```python
def reset(self) -> None: ...
```

### Timeout().seconds

[Show source in timeout.py:48](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/timeout.py#L48)

Return the timeout duration in seconds.

#### Returns

- `float` - The timeout duration in seconds.

#### Examples

```python
>>> timeout = Timeout(5)
>>> timeout.seconds
5
```

#### Signature

```python
@property
def seconds(self) -> float: ...
```

### Timeout().seconds

[Show source in timeout.py:62](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/timeout.py#L62)

Set the timeout duration in seconds.

#### Arguments

- `value` *float* - The new timeout duration in seconds.

#### Examples

```python
>>> timeout = Timeout(5)
>>> timeout.seconds = 10
>>> timeout.seconds
10
```

#### Signature

```python
@seconds.setter
def seconds(self, value: float) -> None: ...
```

### Timeout().start

[Show source in timeout.py:149](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/timeout.py#L149)

Start the timeout.

#### Examples

```python
>>> timeout = Timeout(5, start=False)
>>> timeout.expired
False
>>> timeout.start()
>>> timeout.expired
False
>>> time.sleep(6)
>>> timeout.expired
True
```

#### Signature

```python
def start(self) -> None: ...
```

### Timeout().started

[Show source in timeout.py:77](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/timeout.py#L77)

Return whether the timeout has been started.

#### Returns

- `bool` - True if the timeout has been started, False otherwise.

#### Examples

```python
>>> timeout = Timeout(5, start=False)
>>> timeout.started
False
>>> timeout.start()
>>> timeout.started
True
```

#### Signature

```python
@property
def started(self) -> bool: ...
```

### Timeout().stop

[Show source in timeout.py:180](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/timeout.py#L180)

Stop the timeout.

#### Examples

```python
>>> timeout = Timeout(5)
>>> time.sleep(2)
>>> timeout.stop()
>>> timeout.elapsed
2.0
>>> timeout.remaining
3.0
>>> timeout.expired
False
```

#### Signature

```python
def stop(self) -> None: ...
```