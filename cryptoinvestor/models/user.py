from cryptoinvestor.models.account import Account


class User:
    class Error(Exception):
        pass

    def __init__(self, *, username: str, password: str, account: Account):
        self.username = username
        self.password = password
        self.account = account
        self.bought = dict()

    def buy(self, count: float, crypto_name: str) -> float:
        asset = self.account.assets.get(crypto_name)
        if not asset or not asset.is_loaded():
            raise self.Error(f"{crypto_name} is not a valid cryptocurrency or is not loaded")

        if count < 0:
            raise self.Error(f"{count} is not a valid number of units")

        price = asset.rates.get(self.account.local_currency).get('rate')

        if self.account.balance >= (count * price):
            if self.bought.get(crypto_name) is None:
                self.bought[crypto_name] = count
            else:
                self.bought[crypto_name] += count
            self.account.balance -= count * price
            return price * count
        return 0

    def sell(self, count: float, crypto_name: str) -> float:
        asset = self.account.assets.get(crypto_name)
        if not asset or not asset.is_loaded():
            raise self.Error(f"{crypto_name} is not a valid cryptocurrency or is not loaded")

        if count < 0:
            raise self.Error(f"{count} is not a valid number of units")

        price = asset.rates.get(self.account.local_currency).get('rate')

        if not self.bought.get(crypto_name, 0) == 0:
            self.bought[crypto_name] -= count
            self.account.balance += count * price
            return count * price
        return 0

    def balance(self) -> float:
        return self.account.balance
