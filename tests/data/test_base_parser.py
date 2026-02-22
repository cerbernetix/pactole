"""Unit tests for BaseParser."""

from __future__ import annotations

import pytest

from pactole.combinations import LotteryCombination
from pactole.data import BaseParser


class TestBaseParser:
    """Tests for the BaseParser class."""

    def test_init_defaults_to_lottery_combination_factory(self) -> None:
        """Test the default factory creates LotteryCombination instances."""

        parser = BaseParser()

        combination = parser.combination_factory()

        assert isinstance(combination, LotteryCombination)

    def test_init_uses_custom_factory(self) -> None:
        """Test custom factories are stored and returned by the property."""

        def build_combination() -> LotteryCombination:
            return LotteryCombination()

        parser = BaseParser(combination_factory=build_combination)

        assert parser.combination_factory is build_combination

    def test_call_raises_not_implemented(self) -> None:
        """Test the base parser raises when __call__ is not implemented."""

        parser = BaseParser()

        with pytest.raises(NotImplementedError, match="Subclasses must implement method __call__"):
            parser({"date": "2024-01-01"})
