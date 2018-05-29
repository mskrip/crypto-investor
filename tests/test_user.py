import random
import pytest
import string

from cryptoinvestor.models.account import Account
from cryptoinvestor.models.asset import Asset
from cryptoinvestor.models.user import User

INITIAL_CAPITAL = 10000
BASE_CURRENCY = 'EUR'
RATES = {
    'BTC': {
        'name': 'Bitcoin',
        'rate': 6995.258427052127,
        'timestamp': "2018-05-22T11:06:54.0722052Z",
        'is_crypto': True
    },
    'ETH': {
        'name': 'Etherium',
        'rate': 584.0151880934651,
        'timestamp': "2018-05-22T11:06:53.9940728Z",
        'is_crypto': True
    },
    'LTC': {
        'name': 'Litecoin',
        'rate': 104.41433400354525,
        'timestamp': "2018-04-16T02:28:34.8024930Z",
        'is_crypto': True
        },
    'USD': {
        'name': 'US Dollar',
        'rate': 0.8174678765225807,
        'timestamp': "2018-04-16T02:28:31.4594913Z",
        'is_crypto': False
    },
}


class TestUser:
    def _create_user(self) -> User:
        return User(
            username="Test",
            password="TestPassword1",
            account=Account(self._assets(), balance=INITIAL_CAPITAL)
        )

    def _assets(self) -> {str: Asset}:
        assets = {}

        for key, val in RATES.items():
            asset = Asset(key, val['name'], key, val['is_crypto'])
            asset.set_rate(BASE_CURRENCY, val['rate'], val['timestamp'])
            assets[key] = asset

        return assets

    def _rate_for(self, user: User, currency: str) -> float:
        return user.account.assets.get(currency).rates[BASE_CURRENCY]['rate']

    def test_buy(self):
        user = self._create_user()

        assert user.balance() == INITIAL_CAPITAL

        btc_rate = self._rate_for(user, "BTC")

        t1 = user.buy(1, "BTC")

        assert t1 == btc_rate

        assert user.balance() == INITIAL_CAPITAL - (1 * btc_rate)

        eth_rate = self._rate_for(user, "ETH")

        t2 = user.buy(1, "ETH")

        assert t2 == eth_rate

        t3 = user.buy(10e-4, "ETH")

        assert t3 == pytest.approx(10e-4 * eth_rate)

        assert user.balance() == pytest.approx(INITIAL_CAPITAL - (t1 + t2 + t3))

    def test_buy_nonexistant_currency(self):
        user = self._create_user()

        non_existant_currencies = [''.join(random.choices(
            string.ascii_uppercase, k=random.randint(2, 20)
        )) for _ in range(1000)]

        for c in non_existant_currencies:
            if c not in RATES.keys():
                with pytest.raises(user.Error):
                    user.buy(1, c)

        assert user.balance() == INITIAL_CAPITAL

    def test_buy_too_much(self):
        user = self._create_user()

        with pytest.raises(user.Error):
            user.buy(999, "BTC")

        t1 = user.buy(0.5, "BTC")

        with pytest.raises(user.Error):
            user.buy(999, "BTC")

        assert user.balance() == INITIAL_CAPITAL - t1

    def test_buy_negative(self):
        user = self._create_user()

        with pytest.raises(user.Error):
            user.buy(-1, "BTC")

        assert user.balance() == INITIAL_CAPITAL

        t1 = user.buy(1, "ETH")

        assert user.balance() == pytest.approx(INITIAL_CAPITAL - t1)

        with pytest.raises(user.Error):
            user.buy(-0.0001, "BTC")

        assert user.balance() == pytest.approx(INITIAL_CAPITAL - t1)

        with pytest.raises(user.Error):
            user.buy(-0.0001, "ETH")

        assert user.balance() == pytest.approx(INITIAL_CAPITAL - t1)

    def test_sell_not_owned(self):
        user = self._create_user()

        with pytest.raises(user.Error):
            user.sell(1, "BTC") is None

        assert user.balance() == INITIAL_CAPITAL

    def test_sell_all_owned(self):
        user = self._create_user()

        btc_rate = self._rate_for(user, "BTC")
        eth_rate = self._rate_for(user, "ETH")

        user.buy(1, "BTC")
        user.buy(2, "ETH")

        assert user.sell(0.5, "BTC") == btc_rate * 0.5
        assert user.sell(1.2, "ETH") == eth_rate * 1.2
        assert user.sell(0.8, "ETH") == eth_rate * 0.8
        assert user.sell(0.3, "BTC") == btc_rate * 0.3
        assert user.sell(0.2, "BTC") == btc_rate * 0.2

        assert user.balance() == INITIAL_CAPITAL

    def test_sell_not_enough_owned(self):
        user = self._create_user()

        btc_rate = self._rate_for(user, "BTC")

        user.buy(1, "BTC")

        t1 = user.sell(0.5, "BTC")

        assert t1 == btc_rate * 0.5

        with pytest.raises(user.Error):
            user.sell(0.51, "BTC")

        assert user.balance() == (INITIAL_CAPITAL - t1)

        t2 = user.sell(0.5, "BTC")

        assert t2 == btc_rate * 0.5

        assert user.balance() == INITIAL_CAPITAL

    def test_sell_negative(self):
        user = self._create_user()

        t1 = user.buy(1, "BTC")

        t2 = user.buy(1, "ETH")

        with pytest.raises(user.Error):
            user.sell(-1, "BTC")

        with pytest.raises(user.Error):
            user.sell(-0.1, "BTC")

        with pytest.raises(user.Error):
            user.sell(-2, "ETH")

        with pytest.raises(user.Error):
            user.sell(-0.0001, "ETH")

        assert user.balance() == pytest.approx(INITIAL_CAPITAL - (t1 + t2))

    def test_profit(self):
        user = self._create_user()

        user.buy(1, "BTC")
        user.buy(2, "ETH")

        delta = {
            'BTC': 2.3432,
            'ETH': 14.3432
        }

        self.change_rate(user, delta)

        user.account.assets = self._assets()

        delta = {
            'BTC': -8.34332,
            'ETH': -23.43232
        }

        self.change_rate(user, delta)

    def change_rate(self, user: User, delta: dict):
        for key in delta:
            user.account.assets[
                key
                ].rates[
                    BASE_CURRENCY
                    ]['rate'] = user.account.assets[key].rates[BASE_CURRENCY]['rate'] + delta[key]

        investments = user.get_investments(BASE_CURRENCY)

        for key in delta:
            for investment in investments[key]:
                assert investment['amount'] != 0
                assert investment['profit'] == round(delta[key] * investment['amount'], 2)
