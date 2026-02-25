# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added configurable provider cache root support via `PACTOLE_CACHE_ROOT` and
  `cache_root_name` handling in provider-related classes.

### Changed

- Updated documentation for environment-variable based configuration of providers and cache.

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
