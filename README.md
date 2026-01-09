# Pactole

A Python library for managing lottery results.

## Installation

To add `pactole` to your project:

```sh
pip install -U pactole
```

or better, with `uv`:

```sh
uv add -U pactole
```

## Usage

```python
import pactole
```

## Requirements

The application is written in **`Python 3`** and requires version `3.10`.

In source code, dependencies are managed by [`uv`](https://docs.astral.sh/uv/).

## Installation from sources

For getting the last unstable version, the package needs to be installed from the source code. The following command will grab the last develop version:

- HTTP
    ```sh
    pip install --upgrade git+https://github.com/cerbernetix/pactole.git@develop
    ```
- SSH
    ```sh
    pip install --upgrade git+ssh://git@github.com/cerbernetix/pactole.git@develop
    ```

or better, with `uv`:

- HTTP:
    ```sh
    uv add -U git+https://github.com/cerbernetix/pactole.git@develop
    ```
- SSH
    ```sh
    uv add -U git+ssh://git@github.com/cerbernetix/pactole.git@develop
    ```

## Development

Check out the repository:

```sh
git clone git@github.com:cerbernetix/pactole.git
```

Then, create the virtual env and install the dependencies:

```sh
cd pactole
uv sync
```

## License

Copyright (c) 2026 Jean-Sébastien CONAN

Distributed under the MIT License.
