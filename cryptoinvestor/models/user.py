from cryptoinvestor.models.account import Account


class User:

    def __init__(self, *, username: str, password: str, account: Account):
        self.username = username
        self.password = password
        self.account = account
        self.id = id
        self.rates = {}
        self.coin_status = 10000
        self.bought = dict()

    def buy(self, crypto_name, count, price) -> bool:
        print("ide buy "+crypto_name)
        if self.coin_status >= (count * price):
            if self.bought.get(crypto_name) is None:
                self.bought[crypto_name] = count
            else:
                self.bought[crypto_name] += count
            self.coin_status -= count * price
            print("coins: ",self.coin_status," bought: ",self.bought)
        else:
            return False

        return True

    def sell(self, crypto_name, count, price) -> bool:
        print("ide sell "+crypto_name)
        
        if self.bought.get(crypto_name) is None or self.bought[crypto_name] == 0:
            print("You have nothing to sell")
            return False
        else:
            self.bought[crypto_name] -= count
            self.coin_status += count * price
            print("coins: ",self.coin_status," bought: ",self.bought)
        return True
