# Configuration documentation for Cryptoinvestor

There are two ways to configure behaviour of application:

- [Configuration file](#configuration_file)
- [Environment variables](#environment_variables)

## Configuration file

Templates of config file is in `cryptoinvestor/skel/cryptoinvestor.config.yaml`.
Copy the template somewhere to you local PC and edit the copy.

| Setting        | Description                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------------- |
| dump_path      | Path to a dump file where all the currency rate history is saved. Defaults to `/srv/cryptoinvestor/data.dump.json`. |
| local_currency | Local currency string. Defaults to `EUR`.                                                                           |
| api            | Configuration of various APIs used for data retrieval.                                                              |

### Api - CoinApi

| Setting  | Description                                                                  |
| -------- | ---------------------------------------------------------------------------- |
| base_url | Base url of CoinApi REST service. Defaults to `https://rest.coinapi.io/v1/`. |
| api_key  | Api key provided by CoinApi.                                                 |

### Api - CoinMarketCap

| Setting  | Description                                                                           |
| -------- | ------------------------------------------------------------------------------------- |
| base_url | Base url of CoinMarketCap REST service. Defaults to `https://api.coinmarketcap.com/`. |

### Api - Firebase

| Setting      | Description                  |
| ------------ | ---------------------------- |
| api_key      | API key to Firebase project. |
| database_url | URL of Firebase database.    |
| project_id   |          |

## Environment variables

- `DUMP_PATH` - Path to a dump file where all the currency rate history is saved. Defaults to `/srv/cryptoinvestor/data.dump.json`.
- `LOCAL_CURRENCY` - Local currency string. Defaults to `EUR`.
- `COINAPI_KEY` - Api key provided by CoinApi.
- `FIREBASE_API_KEY` - API key to Firebase project.
- `FIREBASE_PROJECT_ID` - Firebase project ID.
- `FIREBASE_DATABASE_URL` - URL of Firebase database.
