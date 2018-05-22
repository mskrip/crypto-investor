from cryptoinvestor.models.account import Account


class User:

    def __init__(self, *, username: str, password: str, account: Account):
        self.username = username
        self.password = password
        self.account = account
        self.bought = dict()

    def buy(self, count, price, crypto_name) -> bool:
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
