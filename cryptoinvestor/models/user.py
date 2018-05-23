from cryptoinvestor.models.account import Account


class User:
    class Error(Exception):
        pass

    def __init__(self, *, username: str, password: str, account: Account):
        self.username = username
        self.password = password
        self.account = account
        self.bought = dict()

    def buy(self, count: float, a_name: str) -> float:
        asset = self.account.assets.get(a_name)
        if not asset or not asset.is_loaded():
            raise self.Error(f"{a_name} is not a valid cryptocurrency or is not loaded")

        if count < 0:
            raise self.Error(f"{count} is not a valid number of units")

        lc = self.account.local_currency

        price = asset.rates.get(lc).get('rate')

        s = count * price

        if self.balance() < s:
            raise self.Error(
                f"Buying {count} of {a_name} would cost {s} {lc}. You have {self.balance()} {lc}"
            )

        owned = self.bought.get(a_name, 0)

        self.bought[a_name] = owned + count
        self._buy(s)

        return s

    def sell(self, count: float, a_name: str) -> float:
        asset = self.account.assets.get(a_name)
        if not asset or not asset.is_loaded():
            raise self.Error(f"{a_name} is not a valid cryptocurrency or is not loaded")

        if count < 0:
            raise self.Error(f"{count} is not a valid number of units")

        owned = self.bought.get(a_name, 0)

        if owned == 0:
            raise self.Error(f"You own no {a_name}")

        if owned < count:
            raise self.Error(f"You can't sell {count} of {a_name}.You have only {owned}.")

        price = asset.rates.get(self.account.local_currency).get('rate')

        s = count * price

        self.bought[a_name] -= count
        self._sell(s)

        return s

    def _buy(self, sum: float):
        self.account.balance -= sum

    def _sell(self, sum: float):
        self.account.balance += sum

    def balance(self) -> float:
        return self.account.balance
