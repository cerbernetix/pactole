# GitHub Copilot Instructions

You are an expert AI programming assistant working on the `pactole` project.
This project is a Python library for managing lottery results.

## Project Overview

- **Language**: Python 3.10+
- **Dependency Manager**: `uv`
- **Linter/Formatter**: `ruff`
- **Documentation**: Markdown files in `docs/`

## Coding Standards

- **Style**: Follow PEP 8.
- **Docstrings**: Follow PEP 257 using **Google style**.
- **Line Length**: Maximum 100 characters.
- **Type Hints**: Use type annotations for all function arguments and return values.
- **Imports**: Sort imports using `ruff` (isort compatible).

## Security

- **Domains**: Use only controlled domains (e.g., `local.test`, `test.local`) in tests and examples. Avoid using real 3rd-party domains like `example.com` to prevent potential data leakage.
- **Secrets**: Never hardcode real secrets or keys. Use environment variables or mock values.

## Project Structure

- `src/pactole/`: Main package source code.
- `docs/`: Documentation.
- `tests/`: Unit tests.
- `pyproject.toml`: Project configuration and dependencies.

## Development Workflow

- Use `uv sync` to install dependencies.
- Use `ruff check .` and `ruff format .` to lint and format code.
- When generating code, ensure it is compatible with Python 3.10.
- Prefer using `pathlib` for file system operations.
- Use the standard `logging` module for logging.

## Testing

- Use `pytest` for testing.
- Ensure tests are placed in a `tests/` directory.
- Target complete coverage when writing unit tests, make sure to test all functions and methods; pay also attention to unmet conditions.
- Prefer `unittest.mock.patch` over `monkeypatch` in tests.
- Prefer mocked time (e.g., `time.monotonic` via `unittest.mock.patch`) over `time.sleep()`.
- Only mock external dependencies; use real internal classes and utilities when practical.
- Always run tests after making code or test changes. Default to `pytest` unless tests are known to be long-running.
- If tests are long-running, require external services, or could modify system state, ask for confirmation before running.
- If tests cannot be run, explain why and provide the exact command that should be run.
- Run coverage checks before finishing a code task when feasible; otherwise, note that coverage was skipped.
- Always fix failing tests before finishing a code task.
- **Structure**:
    - Global functions: Single unit test functions are acceptable.
    - Classes: Use a single unit test class per module (e.g., `class TestClassName:`).
    - Avoid accessing private members (those starting with `_`) in tests; use public APIs instead.
    - If private access is unavoidable, prefer a test-only subclass that exposes the needed behavior.
    - When adding public methods in test-only subclasses, include docstrings for those methods.
    - Add one blank line between a test function docstring and its first statement.
    - Add one blank line between preparation steps and the first assertion in tests.
    - Keep unit tests ordered to match the order of the source code under test.
    - Do not add dummy comments in unit tests unless intent needs to be explained.

## Documentation

- Update `README.md` or relevant `docs/` files when adding new features.
- Ensure all public functions and classes have clear docstrings.
