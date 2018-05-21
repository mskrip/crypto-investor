from cryptoinvestor.models.account import Account
from flask import request


class User:

    def __init__(self, *, username: str, password: str, account: Account):
        self.username = username
        self.password = password
        self.account = account
        self.id = id
        self.rates = {}
        self.coin_status = 10000
        self.bought = dict()

    def buy(self) -> bool:
        count = float(request.args.get('count'))
        price = float(request.args.get('rate'))
        crypto_name = request.args.get('name')

        if self.coin_status >= (count * price):
            if self.bought.get(crypto_name) is None:
                self.bought[crypto_name] = count
            else:
                self.bought[crypto_name] += count
            self.coin_status -= count * price
            print("coins: ",self.coin_status," bought: ",self.bought)
        else:
            print("You have not enough money")
            return False
        return True

    def sell(self) -> bool:
        count = float(request.args.get('count'))
        price = float(request.args.get('rate'))
        crypto_name = request.args.get('name')
        
        if self.bought.get(crypto_name) is None or self.bought[crypto_name] == 0:
            print("You have nothing to sell")
            return False
        else:
            self.bought[crypto_name] -= count
            self.coin_status += count * price
            print("coins: ",self.coin_status," bought: ",self.bought)
        return True
