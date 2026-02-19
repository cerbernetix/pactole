"""A library for managing lottery results."""

__all__ = [
    "EuroDreams",
    "EuroDreamsCombination",
    "EuroMillions",
    "EuroMillionsCombination",
]

from .combinations import EuroDreamsCombination, EuroMillionsCombination
from .lottery import EuroDreams, EuroMillions
