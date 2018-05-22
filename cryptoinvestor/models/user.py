from cryptoinvestor.models.account import Account


class User:
    class Error(Exception):
        pass

    def __init__(self, *, username: str, password: str, account: Account):
        self.username = username
        self.password = password
        self.account = account
        self.bought = dict()

    def buy(self, count: float, price: float, crypto_name: str) -> bool:
        asset = self.account.assets.get(crypto_name)
        if not asset or not asset.is_loaded():
            raise self.Error(f"{crypto_name} is not a valid cryptocurrency or is not loaded")

        if self.account.balance >= (count * price):
            if self.bought.get(crypto_name) is None:
                self.bought[crypto_name] = count
            else:
                self.bought[crypto_name] += count
            self.account.balance -= count * price
            return True
        return False

    def sell(self, count, price, crypto_name) -> bool:
        if not self.bought.get(crypto_name, 0) == 0:
            self.bought[crypto_name] -= count
            self.account.balance += count * price
            return True
        return False

    def balance(self) -> float:
        return self.account.balance
