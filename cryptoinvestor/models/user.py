from cryptoinvestor.models.account import Account


class User:
    class Error(Exception):
        pass

    def __init__(self, *, username: str, password: str, account: Account):
        self.username = username
        self.password = password
        self.account = account

    def buy(self, amount: float, a_name: str) -> float:
        asset = self.account.assets.get(a_name)
        if not asset or not asset.is_loaded():
            raise self.Error(f"{a_name} is not a valid cryptocurrency or is not loaded")

        if amount < 0:
            raise self.Error(f"{amount} is not a valid number of units")

        lc = self.account.local_currency

        price = asset.rates.get(lc).get('rate')

        s = amount * price

        if self.balance() < s:
            raise self.Error(
                f"Buying {amount} of {a_name} would cost {s} {lc}."
                f"You have {self.balance()} {lc}"
            )

        if a_name not in self.account.investments:
            self.account.investments[a_name] = []
        self.account.investments[a_name].append({'amount': amount, 'price': price})

        self.account.buy(s)

        return s

    def sell(self, amount: float, a_name: str) -> float:
        asset = self.account.assets.get(a_name)
        if not asset or not asset.is_loaded():
            raise self.Error(f"{a_name} is not a valid cryptocurrency or is not loaded")

        if amount < 0:
            raise self.Error(f"{amount} is not a valid number of units")

        owned = 0
        for investment in self.account.investments.get(a_name, []):
            owned += investment['amount']

        if owned == 0:
            raise self.Error(f"You own no {a_name}")

        if owned < amount:
            raise self.Error(f"You can't sell {amount} of {a_name}.You have only {owned}.")

        price = asset.rates.get(self.account.local_currency).get('rate')

        s = amount * price

        self.account.investments[a_name].append({'amount': -amount, 'price': price})
        self.account.sell(s)

        return s

    def get_investments(self, base: str) -> dict:
        investments = self.account.investments
        for key in investments:
            asset = self.account.assets.get(key)
            rate = asset.rates.get(base, []).get('rate', 'N/A')

            for investment in investments[key]:
                investment['profit'] = self.get_profit(investment, rate)

        return investments

    def get_profit(self, investment: dict, rate: float) -> float:
        return round(
                    (rate * investment['amount']) - (investment['price'] * investment['amount']), 2)

    def balance(self) -> float:
        return self.account.balance
