from cryptoinvestor.views import BaseView


class InvestmentsListView(BaseView):
    def get_template_name(self):
        return 'investments/investments.html'

    def get_objects(self):

        context = {}

        base = self.app.local_currency
        investments = self.app.user.get_investments(base)

        context.update({
            'investments': investments,
            'currency': base
        })

        return context
