[Pactole](../README.md) / [Documentation](./README.md)

# Pactole Developer Overview

This document provides a comprehensive overview of the Pactole codebase architecture, data flow, and implementation details for developers.

## Project Overview

Pactole is a Python library for managing lottery results, specifically designed to fetch, cache, and query historical draw data for European lotteries. The library currently supports **EuroMillions** and **EuroDreams**, with an extensible architecture that allows adding new lottery types.

### Key Features

- **Data fetching**: Automatically downloads lottery archives from official sources (FDJ - Française des Jeux)
- **Caching**: Stores parsed data locally to avoid redundant downloads
- **Combination management**: Models lottery combinations with rank calculation and validation
- **Draw date computation**: Determines next and previous draw dates based on configured days
- **Search capabilities**: Find past draws matching a specific combination

## Architecture

Pactole follows a layered architecture with clear separation of concerns:

```
┌───────────────────────────────────────────────────┐
│                    User Interface                 │
│                                                   │
│  - EuroMillions, EuroDreams classes (public API)  │
└───────────────────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────┐
│                    Lottery Layer                  │
│                                                   │
│  - BaseLottery, EuroMillions, EuroDreams          │
│  - Manages draw dates, combinations, queries      │
└───────────────────────────────────────────────────┘
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
┌─────────────────────┐            ┌──────────────────┐
│  Combination Layer  │            │     Data Layer   │
│                     │            │                  │
│  - Lottery          │            │  - BaseProvider  │
│    Combination      │            │  - BaseParser    │
│  - EuroMillions     │            │  - BaseResolver  │
│  - EuroDreams       │            │                  │
└─────────────────────┘            └──────────────────┘
                                             │
                            ┌────────────────┴───────────────┐
                            ▼                                ▼
                   ┌──────────────────┐             ┌─────────────────┐
                   │    Utils Layer   │             │   Providers     │
                   │                  │             │                 │
                   │  - DrawDays      │             │  - FDJProvider  │
                   │  - Weekday       │             │                 │
                   │  - FileCache     │             │                 │
                   │  - TimeoutCache  │             │                 │
                   └──────────────────┘             └─────────────────┘
```

## Core Components

### 1. Combination Layer

Handles the mathematical modeling of lottery combinations.

#### Key Classes

**LotteryCombination** (`src/pactole/combinations/lottery_combination.py`)

- Base class representing compound lottery combinations
- Manages multiple components (e.g., main numbers + stars)
- Calculates lexicographic rank for unique combination identification
- Supports winning rank lookups

**BoundCombination** (`src/pactole/combinations/combination.py`)

- Represents a single component with bounded values
- Enforces value ranges (e.g., 1-50 for main numbers)
- Provides validation and uniqueness checks
- Computes number of possible combinations

**EuroMillionsCombination** (`src/pactole/combinations/euromillions_combination.py`)

- Implements 5 main numbers (1-50) + 2 stars (1-12)
- Total combinations: 139,838,160
- Winning ranks based on matching pattern

**EuroDreamsCombination** (`src/pactole/combinations/eurodreams_combination.py`)

- Implements 6 main numbers (1-40) + 1 dream (1-5)
- Total combinations: 19,191,900
- Different winning rank structure

#### Combination Lifecycle

1. **Creation**: Via factory method or direct instantiation
2. **Validation**: Values checked against bounds
3. **Rank calculation**: Unique lexicographic position computed
4. **Winning lookup**: Match pattern → winning rank

### 2. Data Layer

Handles data fetching, parsing, and caching.

#### Key Classes

**BaseProvider** (`src/pactole/data/base_provider.py`)

- Orchestrates data loading from archives
- Manages caching with FileCache and a refresh Timeout
- Converts raw data to DrawRecord objects
- Auto-refreshes cache when new draws expected

**BaseResolver** (`src/pactole/data/base_resolver.py`)

- Resolves archive URLs from source websites
- Maintains cache of available archives
- HTTP requests handled via `fetch_content()` utility

**BaseParser** (`src/pactole/data/base_parser.py`)

- Converts raw archive rows to DrawRecord instances
- Maps source field names to internal representation
- Creates combination instances via factory pattern

**FDJProvider** (`src/pactole/data/providers/fdj.py`)

- Concrete provider for FDJ archives
- Uses Beautiful Soup for HTML parsing
- Implements FDJ-specific field mappings

#### Data Flow

```
1. Request draw records → BaseProvider.load()
2. Check cache → FileCache
3. If cache missing/expired:
    a. BaseResolver.load() → Get archive list
    b. fetch_content() → Download archive (ZIP/CSV)
    c. BaseParser.__call__() → Parse raw data
    d. FileCache.write() → Save CSV
4. FileCache.load() → Return parsed records
```

### 3. Utility Layer

Provides foundational functionality.

#### Key Classes

**DrawDays** (`src/pactole/utils/days.py`)

- Manages lottery draw days (e.g., Tuesday/Friday)
- Calculates next/previous draw dates
- Handles weekday arithmetic

**Weekday** (`src/pactole/utils/days.py`)

- Enum wrapper for days of week
- Date arithmetic (next, previous, until)
- Flexible input parsing (string, date, integer)

**FileCache** (`src/pactole/utils/cache.py`)

- Extends MemoryCache with file persistence
- Auto-saves to CSV/JSON files
- Modification time tracking

**TimeoutCache** (`src/pactole/utils/cache.py`)

- Time-based cache with TTL
- Lazy loading with custom loader function
- Thread-safe cache invalidation

**Timeout** (`src/pactole/utils/timeout.py`)

- Tracks refresh windows used by providers

### 4. Lottery Layer

High-level API for specific lotteries.

#### Key Classes

**BaseLottery** (`src/pactole/lottery/base_lottery.py`)

- Base class for all lottery implementations
- Provides common operations:
    - `get_last_draw_date()`: Find most recent draw
    - `get_next_draw_date()`: Find next scheduled draw
    - `find_records()`: Search for matching combinations
    - `generate()`: Create random valid combinations
    - `get_records()`: Load all historical draws

**EuroMillions** (`src/pactole/lottery/euromillions.py`)

- EuroMillions-specific implementation
- Environment variable configuration:
    - `EUROMILLIONS_PROVIDER_CLASS`
    - `EUROMILLIONS_DRAW_DAYS`
    - `EUROMILLIONS_DRAW_DAY_REFRESH_TIME`
    - `EUROMILLIONS_CACHE_NAME`
    - `EUROMILLIONS_ARCHIVES_PAGE`

**EuroDreams** (`src/pactole/lottery/eurodreams.py`)

- EuroDreams-specific implementation
- Environment variable configuration:
    - `EURODREAMS_PROVIDER_CLASS`
    - `EURODREAMS_DRAW_DAYS`
    - `EURODREAMS_DRAW_DAY_REFRESH_TIME`
    - `EURODREAMS_CACHE_NAME`
    - `EURODREAMS_ARCHIVES_PAGE`

## Data Models

### DrawRecord

Represents a single lottery draw with all relevant information.

```python
@dataclass
class DrawRecord:
    period: str              # Period identifier (e.g., "202311")
    draw_date: date          # Date of the draw
    deadline_date: date      # Deadline for claims
    combination: LotteryCombination  # Winning numbers
    numbers: dict[str, list[int]]    # Component breakdown
    winning_ranks: list[WinningRank] # Prize information
```

### WinningRank

```python
@dataclass
class WinningRank:
    rank: int    # Rank (1 = jackpot)
    winners: int # Number of winners
    gain: float  # Prize amount per winner
```

### FoundCombination

Result of searching for combinations in draw records.

```python
class FoundCombination:
    record: DrawRecord
    rank: int
```

## Usage Examples

### Basic Usage

```python
from pactole import EuroMillions
from datetime import date

lottery = EuroMillions()

# Get history
records = list(lottery.get_records())

# Check if a combination won
ticket = lottery.get_combination(numbers=[3, 15, 22, 28, 44], stars=[2, 9])
matches = list(lottery.find_records(ticket))

# Next draw date
next_draw = lottery.get_next_draw_date(from_date=date(2026, 2, 19))

# Generate random tickets
random_tickets = lottery.generate(n=3)
```

### Custom Provider

```python
from pactole.data import BaseProvider, BaseParser, BaseResolver, DrawRecord
from pactole.combinations import EuroMillionsCombination
from pactole.lottery import BaseLottery
from pactole.utils import DrawDays, Weekday

class MyResolver(BaseResolver):
    def _load_cache(self) -> dict[str, str]:
        return {"archive.csv": "https://local.test/archives/evm.csv"}

class MyParser(BaseParser):
    def __call__(self, data: dict) -> DrawRecord:
        # Parse your data source
        return DrawRecord(...)

provider = BaseProvider(
    resolver=MyResolver(),
    parser=MyParser(),
    draw_days=DrawDays([Weekday.MONDAY, Weekday.WEDNESDAY]),
    combination_factory=EuroMillionsCombination,
    cache_name="my-lottery",
)

lottery = BaseLottery(provider)
```

## Caching System

### File Cache Structure

```
{cache_dir}/
├── pactole/
│   ├── {cache_name}/
│   │   ├── manifest.json      # Archive metadata
│   │   ├── data.csv           # Parsed draw records
│   │   └── sources/           # Original archives
│   │       └── {archive_name}.zip
```

### Cache Invalidation

Cache refreshes automatically when:

1. New draws are expected based on draw days
2. `force=True` is passed to `load()` or `find_records()`
3. Provider refresh timeout elapses (default: 300 seconds)

Resolver archive listings use an in-memory `TimeoutCache` (default: 3600 seconds).

### Memory Cache

- TTL-based expiration
- Automatic reload on access
- Used for resolver archive lists

## Testing

Test coverage includes:

- **Combinations**: BoundCombination, LotteryCombination, EuroMillions, EuroDreams
- **Data**: Providers, Parsers, Resolvers, Models
- **Lottery**: BaseLottery, EuroMillions, EuroDreams
- **Utils**: DrawDays, Weekday, Caching

Run tests with:

```bash
uv run pytest tests/
uv run pytest --cov=src/pactole
```

## Configuration

### Environment Variables

**EuroMillions:**

- `EUROMILLIONS_PROVIDER_CLASS`: Fully qualified class name
- `EUROMILLIONS_DRAW_DAYS`: Comma-separated days (e.g., "TUESDAY,FRIDAY")
- `EUROMILLIONS_DRAW_DAY_REFRESH_TIME`: Refresh threshold in "HH:MM" format
- `EUROMILLIONS_CACHE_NAME`: Cache directory name
- `EUROMILLIONS_ARCHIVES_PAGE`: Archive page name

**EuroDreams:**

- `EURODREAMS_PROVIDER_CLASS`
- `EURODREAMS_DRAW_DAYS`
- `EURODREAMS_DRAW_DAY_REFRESH_TIME`
- `EURODREAMS_CACHE_NAME`
- `EURODREAMS_ARCHIVES_PAGE`

**FDJ Provider:**

- `FDJ_ARCHIVES_PAGE_URL`: URL template with `{name}` placeholder

## Extension Points

### Adding a New Lottery

1. Create combination class (extends LotteryCombination)
2. Implement winning rank mapping
3. Implement provider/parser for data source
4. Implement lottery class (extends BaseLottery)
5. Wire up environment variables

### Adding a New Data Source

1. Implement BaseResolver (fetch archive URLs)
2. Implement BaseParser (parse archive content)
3. Create provider instance with resolver/parser

### Modifying Winning Ranks

Update the `WINNING_RANKS` dictionary in your combination class:

```python
WINNING_RANKS = {
    (5, 2): 1,  # 5 main + 2 stars = Rank 1
    (5, 1): 2,  # 5 main + 1 star = Rank 2
    ...
}
```

## Performance Considerations

1. **Caching**: Minimizes redundant HTTP requests
2. **Lazy loading**: Archives parsed only when needed
3. **Memory cache**: Fast access to archive lists
4. **File cache**: Persistent CSV storage

## Dependencies

**Production:**

- beautifulsoup4>=4.14.3
- requests>=2.32.5

**Development:**

- pytest>=8.4.2
- pytest-cov>=7.0.0
- pre-commit>=4.3.0
- pylint>=3.3.9
- ruff>=0.14.11

## License

MIT License - See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Run linting and formatting
5. Submit a pull request
