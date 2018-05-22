from cryptoinvestor.models.asset import Asset


class Account:

    def __init__(self, assets: {str: Asset}, local_currency='EUR', balance=0):
        self.local_currency = local_currency
        self.balance = balance
        self.assets = assets
