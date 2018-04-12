# Configuration documentation for Cryptoinvestor

There are two ways to configure behaviour of application:

 - [Configuration file](#configuration_file)
 - [Environment variables](#environment_variables)

## Configuration file

Templates of config file is in `cryptoinvestor/skel/cryptoinvestor.config.yaml`.
Copy the template somewhere to you local PC and edit the copy.

| Setting        | Description                                            |
| -------------- | ------------------------------------------------------ |
| local_currency | Local currency string. Defaults to `EUR`.              |
| api            | Configuration of various APIs used for data retrieval. |

### Api - CoinApi

| Setting  | Description                                                                  |
| -------- | ---------------------------------------------------------------------------- |
| base_url | Base url of CoinApi REST service. Defaults to `https://rest.coinapi.io/v1/`. |
| api_key  | Api key provided by CoinApi.                                                 |


## Environment variables

- `LOCAL_CURRENCY` - Local currency string. Defaults to `EUR`.
- `COINAPI_KEY` - Api key provided by CoinApi.
