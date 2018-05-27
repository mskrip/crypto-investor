from cryptoinvestor.views import BaseView


class InvestmentsListView(BaseView):
    def get_template_name(self):
        return 'investments/investments.html'

    def get_objects(self):

        context = {}
        investments = self.app.user.account.investments

        base = self.app.local_currency

        for key in investments:
            asset = self.app.assets.get(key)
            rate = asset.rates.get(base, []).get('rate', 'N/A')

            for investment in investments[key]:
                investment['profit'] = round(
                    (rate * investment['amount']) - (investment['price'] * investment['amount']), 2)

        context.update({
            'investments': investments,
            'currency': base
        })

        return context
