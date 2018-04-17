from cryptoinvestor.models.account import Account


class User:

    def __init__(self, *, username: str, password: str, account: Account):
        self.username = username
        self.password = password
        self.account = account
