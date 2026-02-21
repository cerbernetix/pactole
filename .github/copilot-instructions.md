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
- **Imports**: Place all imports at the top of the file, sorted using `ruff` (isort compatible). Avoid adding imports in the middle of code; only use lazy loading (imports within functions) when necessary for business logic (e.g., optional dependencies, circular import resolution).

## Documentation

- Update `README.md` or relevant `docs/` files when adding new features.
- Ensure all public functions and classes have clear docstrings.
- Use Google-style docstrings for all public APIs as per PEP 257.
- When modifying public APIs, update the appropriate docstrings and examples.

## Docstrings (Google style)

- **Classes**: Document the class and all constructor parameters in the **class docstring**. Do not add docstrings to `__init__` or other dunder methods (e.g. `__str__`); they do not appear in code hints, so keep constructor behavior in the class docstring.
- **Public functions and methods**: Use this order: (1) One line summarizing behavior; (2) blank line, then any extraneous detail; (3) **Args** — include type and default for each, e.g. `name (type, optional): Description. Defaults to value.`; (4) **Returns** or **Yields** — include type, e.g. `type: Description.`; (5) **Raises** (if any); (6) **Examples** (7).

## Security

- **Domains**: Use only controlled domains (e.g., `local.test`, `test.local`) in tests and runtime. Avoid using real 3rd-party domains like `example.com` to prevent potential data leakage in tests and runtime. However, using 3rd-party domains in docstrings is acceptable as long as code is not executed.
- **Secrets**: Never hardcode real secrets or keys. Use environment variables or mock values.

## Project Structure

- `src/pactole/`: Main package source code.
- `src/scripts/`: Utility scripts for development and maintenance.
- `docs/`: Documentation.
- `tests/`: Unit tests.
- `pyproject.toml`: Project configuration and dependencies.

## Development Workflow

- Use `uv sync` to install dependencies.
- Use `uv run` to execute scripts and tests, e.g., `uv run pytest` for testing.
- Use `ruff check .` and `ruff format .` to lint and format code.
- When generating code, ensure it is compatible with Python 3.10.
- Prefer using `pathlib` for file system operations.
- Use the standard `logging` module for logging.

## Code Quality Checklist

Before finishing work on generated code:

**For code changes only:**

- **Format and lint check**: Run `uv run ruff check` and `uv run pylint`. Correct any issues using `uv run ruff format`.
- **Test coverage**: Run `uv run pytest --cov` to ensure all code passes tests with complete coverage. Fix any failing tests or missing coverage before completing the task.

**Note**: Code checks (testing, linting, formatting, security checks) are only required when code changes are made. If changes are made only to non-code files (e.g., documentation, markdown files), these checks are not necessary.

## Testing

- Use `pytest` for testing.
- Ensure tests are placed in a `tests/` directory.
- Target complete coverage when writing unit tests, make sure to test all functions and methods; pay also attention to unmet conditions.
- Prefer `unittest.mock.patch` over `monkeypatch` in tests.
- Prefer mocked time (e.g., `time.monotonic` via `unittest.mock.patch`) over `time.sleep()`.
- Only mock external dependencies; use real internal classes and utilities when practical.
- Always run tests after making code or test changes. Default to `pytest` unless tests are known to be long-running.
- If tests cannot be run, explain why and provide the exact command that should be run.
- Run coverage checks before finishing a code task when feasible; otherwise, note that coverage was skipped.
- Always fix failing tests before finishing a code task.
- Intercept logging events using the `caplog` fixture to verify log messages.
- Ensure test messages do not leak into the test runner output (stdout/stderr).
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
