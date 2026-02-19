"""Lottery package."""

__all__ = [
    "BaseLottery",
    "EuroDreams",
    "EuroMillions",
]

from .base_lottery import BaseLottery
from .eurodreams import EuroDreams
from .euromillions import EuroMillions
