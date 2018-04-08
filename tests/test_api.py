import datetime

from cryptoinvestor.api.coinapi import Api as CoinApi


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

        assert round(btc_to_usd.get('rate'), 2) == self.test_btc_to_usd

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
