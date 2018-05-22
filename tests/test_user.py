import random
import string

from cryptoinvestor.models.account import Account
from cryptoinvestor.models.asset import Asset
from cryptoinvestor.models.user import User

INITIAL_CAPITAL = 10000
LOADED_CURRENCIES = ['BTC', 'ETH', 'EUR', 'USD', 'LTC']
BASE_CURRENCY = 'EUR'


class TestUser:
    def _create_user(self) -> User:
        return User(
            username="Test",
            password="TestPassword1",
            account=Account(self._assets(), INITIAL_CAPITAL)
        )

    def _assets(self) -> {str: Asset}:
        btc = Asset('BTC', 'Bitcoin', 'BTC', True)
        btc.set_rate(BASE_CURRENCY, 6995.258427052127, "2018-05-22T11:06:54.0722052Z")

        eth = Asset('ETH', 'Etherium', 'ETH', True)
        eth.set_rate(BASE_CURRENCY, 584.0151880934651, "2018-05-22T11:06:53.9940728Z")

        ltc = Asset('LTC', 'Litecoin', 'LTC', True)
        ltc.set_rate(BASE_CURRENCY, 104.41433400354525, "2018-04-16T02:28:34.8024930Z")

        usd = Asset('USD', 'US Dollar', 'USD', False)
        usd.set_rate(BASE_CURRENCY, 0.8174678765225807, "2018-04-16T02:28:31.4594913Z")
        return {
            'BTC': btc,
            'ETH': eth,
            'LTC': ltc,
            'USD': usd
        }

    def test_buy(self):
        user = self._create_user()

        initial_balance = user.account.balance

        assert initial_balance == INITIAL_CAPITAL

        user.buy(1, 100, "BTC")

        assert user.account.balance == INITIAL_CAPITAL - (1 * 100)

    def test_buy_nonexistant_currency(self):
        user = self._create_user()

        non_existant_currencies = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=3)
        )

        try:
            for c in non_existant_currencies:
                if c not in LOADED_CURRENCIES:
                    user.buy(1, 100, c)
        except user.Error:
            pass

        assert user.account.balance == INITIAL_CAPITAL
