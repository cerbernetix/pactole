<!-- markdownlint-disable -->

# API Overview

## Modules

- [`combinations`](./combinations.md#module-combinations): Combinations package.
- [`combinations.combination`](./combinations.combination.md#module-combinationscombination): Combination module for handling combinations of values and their lexicographic ranks.
- [`combinations.eurodreams_combination`](./combinations.eurodreams_combination.md#module-combinationseurodreams_combination): Module for EuroDreams combination representation and manipulation.
- [`combinations.euromillions_combination`](./combinations.euromillions_combination.md#module-combinationseuromillions_combination): Module for EuroMillions combination representation and manipulation.
- [`combinations.lottery_combination`](./combinations.lottery_combination.md#module-combinationslottery_combination): Module for Lottery combination representation and manipulation.
- [`utils`](./utils.md#module-utils): Utilities package.
- [`utils.days`](./utils.days.md#module-utilsdays): Utilities related to days of the week and lottery draw days.

## Classes

- [`combination.BoundCombination`](./combinations.combination.md#class-boundcombination): A class representing a bound combination of values.
- [`combination.Combination`](./combinations.combination.md#class-combination): A class representing a combination of values.
- [`combination.CombinationInputWithRank`](./combinations.combination.md#class-combinationinputwithrank): Type representing a combination input along with its lexicographic rank.
- [`eurodreams_combination.EuroDreamsCombination`](./combinations.eurodreams_combination.md#class-eurodreamscombination): Class representing a EuroDreams combination.
- [`euromillions_combination.EuroMillionsCombination`](./combinations.euromillions_combination.md#class-euromillionscombination): Class representing a EuroMillions combination.
- [`lottery_combination.CombinationFactory`](./combinations.lottery_combination.md#class-combinationfactory): Protocol for a combination factory.
- [`lottery_combination.LotteryCombination`](./combinations.lottery_combination.md#class-lotterycombination): Class representing a Lottery combination.
- [`days.DrawDays`](./utils.days.md#class-drawdays): Utility class to handle lottery draw days.
- [`days.Weekday`](./utils.days.md#class-weekday): Enumeration for the days of the week.

## Functions

- [`combination.get_combination_from_rank`](./combinations.combination.md#function-get_combination_from_rank): Get the combination corresponding to a given lexicographic rank.
- [`combination.get_combination_rank`](./combinations.combination.md#function-get_combination_rank): Get the lexicographic rank of a given combination.


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
