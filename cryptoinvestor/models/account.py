from cryptoinvestor.models.asset import Asset


class Account:

    def __init__(self, assets: {str: Asset}, local_currency='EUR', balance=0):
        self.local_currency = local_currency
        self.balance = balance
        self.assets = assets
        self.investments = dict()

    def buy(self, sum: float):
        self.balance -= sum

    def sell(self, sum: float):
        self.balance += sum
