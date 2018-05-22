from cryptoinvestor.models.asset import Asset


class Account:

    def __init__(self, assets: {str: Asset}, balance=0):
        self.balance = balance
        self.assets = assets
