import random
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

        btc_rate = user.account.assets.get('BTC').rates[BASE_CURRENCY]['rate']

        t1 = user.buy(1, "BTC")

        assert t1 == btc_rate

        assert user.balance() == INITIAL_CAPITAL - (1 * btc_rate)

        eth_rate = user.account.assets.get('ETH').rates[BASE_CURRENCY]['rate']

        t2 = user.buy(1, "ETH")

        assert t2 == eth_rate

        t3 = user.buy(10e-4, "ETH")

        assert round(t3, 6) == round((10e-4 * eth_rate), 6)

        assert round(user.balance(), 6) == round(INITIAL_CAPITAL - (t1 + t2 + t3), 6)

    def test_buy_nonexistant_currency(self):
        user = self._create_user()

        non_existant_currencies = [''.join(random.choices(
            string.ascii_uppercase, k=random.randint(2, 20)
        )) for _ in range(1000)]

        try:
            for c in non_existant_currencies:
                if c not in RATES.keys():
                    assert user.buy(1, c) == 0
        except user.Error:
            pass

        assert user.balance() == INITIAL_CAPITAL

    def test_buy_negative(self):
        user = self._create_user()

        try:
            assert user.buy(-1, "BTC") == 0
        except user.Error:
            pass

        assert user.balance() == INITIAL_CAPITAL

        t1 = user.buy(1, "ETH")

        assert round(user.balance(), 6) == round(INITIAL_CAPITAL - t1, 6)

        try:
            assert user.buy(-0.0001, "BTC") == 0
        except user.Error:
            pass

        assert round(user.balance(), 6) == round(INITIAL_CAPITAL - t1, 6)

        try:
            assert user.buy(-0.0001, "ETH") == 0
        except user.Error:
            pass

        assert round(user.balance(), 6) == round(INITIAL_CAPITAL - t1, 6)
