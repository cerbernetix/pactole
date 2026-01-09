[Pactole](../README.md) / [Documentation](./README.md)

# Installation

Pactole is a Python library for managing lottery results.

### Requirements

The library is written in **`Python 3`** and requires version `3.10`.

The dependencies are managed by [`uv`](https://docs.astral.sh/uv/).

### Installation

The package needs to be installed from the source code.

```sh
uv add -U git+ssh://git@github.com/cerbernetix/pactole.git
```

Similar command, with `pip`:

```sh
pip install -U git+ssh://git@github.com/cerbernetix/pactole.git
```

### Install for development

Clone the repository:

```sh
git clone git@github.com:cerbernetix/pactole.git
cd pactole
uv sync
```

The development stack is installed with the dependencies, by default. This includes all necessary tools. However, one of them needs special attention as it needs to be specifically loaded: `pre-commit`.

```sh
uv run pre-commit install
```

#### Dependencies

Pactole relies on several dependencies, which need to be installed in a [virtual environment](./tools/venv.md).

Dependencies are managed through `uv`. This is a drop-in replacement for `pip`. Both managers are supported.

#### UV

`uv` is an extremely fast Python package and project manager, written in Rust. This is the recommended tool for managing this project.

If not already done, please install `uv`. Installation instructions can be found [here](https://docs.astral.sh/uv/getting-started/installation/).

> **Note**: [Short instructions are also available in this repo.](./tools/uv.md)

Then, create the virtual env and install the dependencies:

```sh
cd pactole
uv sync
```

**Note:** This will install all dependencies, including the development stack. When only the runtime is needed, it is recommended to exclude the `dev` group, using the `--no-dev` option.

```
uv sync --no-dev
```

#### PIP

Still want to use `pip`?

```sh
cd pactole
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Note**: The library needs Python version `3.10`. When creating the environment, make sure to use the right version of Python.

---

Copyright (c) 2026 Jean-Sébastien CONAN

Distributed under the MIT License.
