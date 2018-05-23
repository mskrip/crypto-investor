import plotly
import json

from cryptoinvestor.views import BaseView
from flask import request

SUCCESS_MSG = "You have successfuly {} {} {} for total of {} {}"


class AssetsListView(BaseView):
    methods = ['GET']

    def get_template_name(self):
        return 'assets/assets.html'

    def get_objects(self):
        assets = []
        toasts = []

        context = {}
        rd_key = request.args.get('redirected')
        if rd_key:
            messages = self.app.cache.get(int(rd_key), {}).get('messages', [])
            toasts += messages

        data = self.app.load()

        graphs = {}

        base = self.app.local_currency

        for name in self.app.assets:
            if name == base:
                continue

            asset = self.app.assets.get(name)
            if asset.is_loaded():
                assets.append({
                    'id': name,
                    'name': asset.name,
                    'rate': asset.rates.get(base, []).get('rate', 'N/A'),
                })

            graphs[name] = {
                'data': [
                    {
                        'x': [rate['time'] for rate in data.get(name, {}).get(base, [])],
                        'y': [rate['rate'] for rate in data.get(name, {}).get(base, [])],
                        'type': 'scatter'
                    },
                ],
                'layout': {
                    'title': asset.name
                }
            }

        if not rd_key:
            for asset in assets:
                id_ = asset.get('id', 'N/A')
                current_rate = asset.get('rate', 0.00)
                try:
                    previous_rate = data.get(id_, {}).get(base, [])[-2].get('rate', 0.00)
                    value = round((current_rate - previous_rate), 4)
                except IndexError:
                    value = 0

                toasts.append(self._crypto_toast(id_, value))

        graphs_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

        context.update({
            'assets': assets,
            'local_currency': self.app.local_currency,
            'graphJSON': graphs_json,
            'toasts': toasts
        })

        return context

    def _crypto_toast(self, id_='N/A', value=0.00):
        if value > 0:
            message = f"From last time {id_} went up by {value}!"
            color = 'green'
        elif value < 0:
            message = f"From last time {id_} went down by {value}!"
            color = 'red'
        else:
            message = f"From last time value of {id_} did not change!"
            color = 'blue'

        return self.toast(message, color)


class BuyView(BaseView):
    def get_objects(self):
        count = float(request.args.get('count', 0))
        crypto_id = request.args.get('id', '')

        msgs = []
        try:
            total = self.app.user.buy(count, crypto_id)
            msgs = [
                self.toast(SUCCESS_MSG.format(
                    'bough', count, crypto_id, total, self.app.local_currency
                ), 'green'),
            ]
        except self.app.user.Error as e:
            msgs = [self.toast(e, 'red')]

        return {'redirect': self._prepare_redirect(msgs)}


class SellView(BaseView):
    def get_objects(self):
        count = float(request.args.get('count', 0))
        crypto_id = request.args.get('id', '')

        try:
            total = self.app.user.sell(count, crypto_id)
            msgs = [
                self.toast(SUCCESS_MSG.format(
                    'sold', count, crypto_id, total, self.app.local_currency
                ), 'green')
            ]
        except self.app.user.Error as e:
            msgs = [self.toast(e, 'red')]

        return {'redirect': self._prepare_redirect(msgs)}
