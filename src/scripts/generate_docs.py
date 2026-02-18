"""Generate documentation for the project."""

import shutil
from pathlib import Path

import lazydocs

SOURCE_DIR = "src/pactole"
DOCS_DIR = "docs/api"
TESTS_DIR = "tests"
OVERVIEW_FILE = "README.md"


def cleanup_docs() -> None:
    """Remove existing docs directory."""
    if Path(DOCS_DIR).exists():
        print("Warning: Existing docs directory found.")
        print(f"Info: Removing existing docs directory. {DOCS_DIR}")
        shutil.rmtree(DOCS_DIR)


def generate_docs() -> None:
    """Generate documentation for the project using lazydocs."""
    print(f"Info: Generating documentation from {SOURCE_DIR} to {DOCS_DIR}")
    lazydocs.generate_docs(
        [SOURCE_DIR],
        output_path=DOCS_DIR,
        ignored_modules=[TESTS_DIR],
        overview_file=OVERVIEW_FILE,
    )
    print("Info: Documentation generated successfully.")


def main():
    """Main function to generate documentation."""
    cleanup_docs()
    generate_docs()


if __name__ == "__main__":
    main()
