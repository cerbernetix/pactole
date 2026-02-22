[Documentation](./README.md)

# Installation

Pactole is a Python library for managing lottery results.

## Requirements

Pactole requires Python 3.10 or newer.

The dependencies are managed by [`uv`](https://docs.astral.sh/uv/).

## Install the package

Install the published package with `uv`:

```sh
uv add -U pactole
```

Or with `pip`:

```sh
pip install -U pactole
```

## Install from source

To install the latest source version directly from GitHub:

```sh
uv add -U git+https://github.com/cerbernetix/pactole.git
```

Or:

```sh
pip install -U git+https://github.com/cerbernetix/pactole.git
```

## Development setup

Clone the repository:

```sh
git clone git@github.com:cerbernetix/pactole.git
cd pactole
uv sync
```

`uv sync` installs runtime and development dependencies by default.

Install Git hooks with `pre-commit`:

```sh
uv run pre-commit install
```

## Optional: runtime-only environment

If you only need runtime dependencies, exclude the development group:

```sh
uv sync --no-dev
```

## Optional: pip-based development setup

Still want to use `pip`?

```sh
cd pactole
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

When creating the environment, make sure Python 3.10+ is used.
