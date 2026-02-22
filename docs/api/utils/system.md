# System

[Pactole Index](../README.md#pactole-index) / [Utils](./index.md#utils) / System

> Auto-generated documentation for [utils.system](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/system.py) module.

- [System](#system)
  - [import_namespace](#import_namespace)

## import_namespace

[Show source in system.py:6](https://github.com/cerbernetix/pactole/blob/main/src/pactole/utils/system.py#L6)

Import a resource from a namespace string.

#### Arguments

- `namespace` *str* - The namespace string in the format "module.resource".

#### Returns

- `type` - The imported resource.

#### Raises

- `ValueError` - If the namespace string is not in the correct format.
- `ImportError` - If the module or resource cannot be imported.
- `AttributeError` - If the resource does not exist in the module.

#### Examples

```python
>>> import_namespace("pactole.data.providers.fdj.FDJResolver")
<class 'pactole.data.providers.fdj.FDJResolver'>
```

#### Signature

```python
def import_namespace(namespace: str) -> type: ...
```