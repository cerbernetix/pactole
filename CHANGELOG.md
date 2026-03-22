# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added string conversion of Weekday instances
- Added serialization methods to Combination classes and data models (to/from_string/csv/json/dict)
- Added support for custom serialization to CSV and JSON (date, dataclasses, serialization helpers)
- Added `CompoundCombination` superclass to `LotteryCombination`
- Added error handling for invalid values and negative rank in Combination class
- Added dictionary-like access to combination components in `CompoundCombination` and derived classes
- Added `dump` method to combinations for dict representation
- Added `match` attribute to `FoundCombination` for storing matching combinations
- Added static methods to parse components from string and CSV representations in `CompoundCombination`

### Changed

- CSV writer now uses to_csv for serializing objects
- JSON writer now uses to_json for serializing objects
- DrawRecord now has custom methods for CSV and JSON import/export instead of generic to/from_dict
- Renamed `CompoundCombination.get_component` to `CompoundCombination.get`
- Renamed `CompoundCombination.get_component_values` to `CompoundCombination.get_values`

### Fixed

- Ensure values are converted to int in `Combination` and `BoundCombination`
- Return `CompoundCombination` constructor as factory instead of `get_combination` from an empty instance

## v0.3.3 [2026-03-11]

### Fixed

- Add a regex filter in `FDJParser` to ignore unrelated CSV keys when matching winner columns
- Detect empty source or archive files during refresh and force the cache to refresh to avoid stale data
- Invalidate the manifest if a refresh run finds missing or zero-count entries
- Return an empty iterable from `read_csv_file` when the file contains no data

## v0.3.2 [2026-03-08]

### Changed

- Added `generate` function for random combination ranks
- Enhanced `Combination.copy` method to handle rank as input
- Added `assert_non_negative_integer` utility and update related functions

## v0.3.1 [2026-02-25]

### Added

- Added configurable provider cache root support via `PACTOLE_CACHE_ROOT` and
  `cache_root_name` handling in provider-related classes.

### Changed

- Updated documentation for environment-variable based configuration of providers and cache.

### Fixed

- Fixed refresh condition logic in `BaseProvider` so cache refresh checks draw days correctly.

## v0.3.0 [2026-02-22]

### Added

- Introduced the data layer with `BaseProvider`, `BaseResolver`, `BaseParser`, and FDJ-specific
  implementations for fetching and parsing archives.
- Added data models for draw history (`DrawRecord`, `WinningRank`, `FoundCombination`).
- Added cache utilities including file-backed caching and timeout-aware in-memory caching.
- Added history helpers to lotteries: `get_records()`, `find_records()`, `count()`, and `dump()`.
- Added developer and environment documentation pages plus expanded usage examples.
- Added MkDocs project configuration and API documentation generation tooling with `handsdown`.
- Added CI workflows for documentation publication and release requirements alignment.

### Changed

- Refactored lottery classes to use providers as the source of draw data.
- Extended utilities for file handling, system helpers, and typed conversions.
- Updated usage documentation with clearer real-world examples and provider customization guidance.
- Enhanced README examples for `EuroMillions` and `EuroDreams`.
- Updated documentation links to the hosted site and simplified documentation navigation.

### Dependencies

- Added `requests` and `beautifulsoup4` for archive fetching and HTML parsing.

### Breaking Changes

- `BaseLottery` now requires a provider instance; custom lotteries must pass
  `provider=BaseProvider(...)` to `super().__init__`.

## v0.2.0 [2026-02-20]

### Added

- Implemented lottery classes: `BaseLottery`, `EuroMillions`, and `EuroDreams`.
- Implemented utility classes for handling draw days: `Weekday` and `DrawDays`.

## v0.1.0 [2026-02-18]

### Added

- Initial project structure.
- Implemented combination classes: `Combination`, `BoundCombination`, `LotteryCombination`,
  `EuroMillionsCombination`, and `EuroDreamsCombination`.
