import datetime

from cryptoinvestor.api.coinapi import Api as CoinApi
from cryptoinvestor.api.coinmarketcap import Api as CoinMarketCapApi


TEST_COINAPI_KEY = '61A647BB-A3D1-4A9C-A736-5FD660914697'


class TestCoinApi:
    test_date = datetime.datetime(2015, 12, 5, 20, 30)
    test_btc_to_usd = 387.62

    def test_init_f(self):
        try:
            CoinApi({'api_key': ''})
        except CoinApi.Error:
            assert True
            return

        assert False

    def test_init(self):
        api = CoinApi({'api_key': TEST_COINAPI_KEY})
        assert api.connect()

    def test_get(self):
        api = CoinApi({'api_key': TEST_COINAPI_KEY})
        assets = api.get()

        assert assets

    def test_load(self):
        api = CoinApi({'api_key': TEST_COINAPI_KEY})
        all_assets = api.get()

        assets = {}
        for asset in all_assets:
            assets[asset.id] = asset

        btc = assets.get('BTC')
        assert not btc.is_loaded()

        btc = api.load(asset=btc, base='USD', time=self.test_date)

        assert btc.is_loaded()

        btc_to_usd = btc.rates.get('USD')
        assert btc_to_usd

    def test_update(self):
        api = CoinApi({'api_key': TEST_COINAPI_KEY})
        all_assets = api.get()

        assets = {}
        for asset in all_assets:
            assets[asset.id] = asset

        btc = assets.get('BTC')
        assert not btc.is_loaded()

        btc = api.load(asset=btc, base='USD', time=self.test_date)

        assert btc.is_loaded()

        btc_to_usd_then = btc.rates.get('USD')
        assert btc_to_usd_then

        updated = api.update(assets)
        btc_now = updated.get('BTC')
        assert btc_now

        btc_to_usd_now = btc_now.rates.get('USD')
        assert btc_to_usd_now

        assert btc_to_usd_now.get('rate') != btc_to_usd_then.get('rate')
        assert btc_to_usd_now.get('time') > btc_to_usd_then.get('time')


class TestCoinMarketCap:
    def test_init(self):
        api = CoinMarketCapApi({})

        assert api
        assert api.base

    def test_connect(self):
        api = CoinMarketCapApi({})

        assert api.connect()
        assert not api.error

    def test_get(self):
        api = CoinMarketCapApi({})

        assets = api.get()

        assert assets
        assert not api.error

    def _test_load_btc_and_eth(self):
        api = CoinMarketCapApi({})

        data = api.get()
        assets = {}

        for asset in data:
            assets[asset.symbol] = asset

        btc = assets.get('BTC')

        assert not btc.is_loaded()

        api.load(asset=btc, base='EUR', time=None)

        assert btc.is_loaded()

        eth = assets.get('ETH')

        assert not eth.is_loaded()

        api.load(asset=eth, base='EUR', time=None)

        assert eth.is_loaded()

        return api, assets

    def test_load(self):
        self._test_load_btc_and_eth()

    def test_update(self):
        api, assets = self._test_load_btc_and_eth()

        updated = api.update(assets)

        old_btc = assets.get('BTC')
        new_btc = updated.get('BTC')

        old_eth = assets.get('ETH')
        new_eth = updated.get('ETH')

        assert new_btc is None or old_btc.time < new_btc.time
        assert new_eth is None or old_eth.time < new_eth.time
