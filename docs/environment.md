[Documentation](./README.md)

# Environment Variables

Pactole can be configured with environment variables to override built-in defaults for providers
and lotteries. These settings are read when creating a lottery instance without explicitly
providing a provider.

## Global provider cache

Base provider cache root configuration used by `pactole.data.base_provider.BaseProvider`.

| Name                 | Default value | Description                                                                                 |
| -------------------- | ------------- | ------------------------------------------------------------------------------------------- |
| `PACTOLE_CACHE_ROOT` | `pactole`     | Root cache directory name used by providers when `cache_root_name` is not provided in code. |

Notes:

- `cache_root_name` constructor parameter takes precedence over `PACTOLE_CACHE_ROOT`.
- If neither `cache_root_name` nor `PACTOLE_CACHE_ROOT` is provided, the default is `pactole`.

## EuroMillions

EuroMillions lottery configuration used when instantiating `pactole.lottery.euromillions.EuroMillions`.

| Name                                 | Default value                            | Description                                |
| ------------------------------------ | ---------------------------------------- | ------------------------------------------ |
| `EUROMILLIONS_PROVIDER_CLASS`        | `pactole.data.providers.fdj.FDJProvider` | Fully qualified provider class.            |
| `EUROMILLIONS_DRAW_DAYS`             | `TUESDAY,FRIDAY`                         | Comma-separated draw days.                 |
| `EUROMILLIONS_DRAW_DAY_REFRESH_TIME` | `22:00`                                  | Refresh threshold time in `HH:MM`.         |
| `EUROMILLIONS_CACHE_NAME`            | `euromillions`                           | Cache name used for stored data.           |
| `EUROMILLIONS_ARCHIVES_PAGE`         | `euromillions-my-million`                | Archives page name passed to the provider. |

## EuroDreams

EuroDreams lottery configuration used when instantiating `pactole.lottery.eurodreams.EuroDreams`.

| Name                               | Default value                            | Description                                |
| ---------------------------------- | ---------------------------------------- | ------------------------------------------ |
| `EURODREAMS_PROVIDER_CLASS`        | `pactole.data.providers.fdj.FDJProvider` | Fully qualified provider class.            |
| `EURODREAMS_DRAW_DAYS`             | `MONDAY,THURSDAY`                        | Comma-separated draw days.                 |
| `EURODREAMS_DRAW_DAY_REFRESH_TIME` | `22:00`                                  | Refresh threshold time in `HH:MM`.         |
| `EURODREAMS_CACHE_NAME`            | `eurodreams`                             | Cache name used for stored data.           |
| `EURODREAMS_ARCHIVES_PAGE`         | `eurodreams`                             | Archives page name passed to the provider. |

## FDJProvider

FDJ provider configuration used by `pactole.data.providers.fdj.FDJProvider` and `pactole.data.providers.fdj.FDJResolver`.

| Name                    | Default value                                         | Description                                                               |
| ----------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------- |
| `FDJ_ARCHIVES_PAGE_URL` | `https://www.fdj.fr/jeux-de-tirage/{name}/historique` | Template URL for the archives page, with a required `{name}` placeholder. |
