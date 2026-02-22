"""Unit tests for system utilities."""

from __future__ import annotations

import pytest

from pactole.utils.system import import_namespace


class TestImportNamespace:
    """Tests for import_namespace."""

    def test_import_namespace_loads_resource(self) -> None:
        """Test importing a valid resource returns the class."""

        resource = import_namespace("pactole.data.providers.fdj.FDJResolver")

        assert resource.__name__ == "FDJResolver"
        assert resource.__module__ == "pactole.data.providers.fdj"

    def test_import_namespace_rejects_invalid_format(self) -> None:
        """Test invalid namespace formats raise a ValueError."""

        with pytest.raises(ValueError):
            import_namespace("pactole")

        with pytest.raises(ValueError):
            import_namespace(".")

        with pytest.raises(ValueError):
            import_namespace(123)  # type: ignore[arg-type]

    def test_import_namespace_raises_for_missing_module(self) -> None:
        """Test missing modules raise ImportError."""

        with pytest.raises(ImportError):
            import_namespace("pactole.utils.missing_module.Foo")

    def test_import_namespace_raises_for_missing_resource(self) -> None:
        """Test missing resources raise AttributeError."""

        with pytest.raises(AttributeError, match="Resource 'MissingClass'"):
            import_namespace("pactole.utils.system.MissingClass")
