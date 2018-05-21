import plotly
import json

from cryptoinvestor.views import BaseView
from flask import Flask, request

class AssetsListView(BaseView):
    methods = ['GET']
    
    def get_template_name(self):
        return 'assets/assets.html'

    def get_objects(self):
        assets = []

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
                    'rate': asset.rates.get(base, {}).get('rate', 'N/A'),
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

        toasts = []
        for asset in assets:
            id_ = asset.get('id', 'N/A')
            current_rate = asset.get('rate', 0.00)
            try:
                previous_rate = data.get(id_, {}).get(base, [])[-2].get('rate', 0.00)
                value = round((current_rate - previous_rate), 4)
            except IndexError:
                value = 0

            toasts.append(self.add_toast(id_, value))

        graphs_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

        return {
            'assets': assets,
            'local_currency': self.app.local_currency,
            'graphJSON': graphs_json,
            'toasts': toasts
        }

    def add_toast(self, id_='N/A', value=0.00):
        if value > 0:
            message = f"From last time {id_} went up by {value}!"
            color = 'green'
        elif value < 0:
            message = f"From last time {id_} went down by {value}!"
            color = 'red'
        else:
            message = f"From last time value of {id_} did not change!"
            color = 'blue'

        return {
            'message': message,
            'color': color
        }


class Sell(BaseView):
    methods = ['GET', 'POST']
    #def dispatch_request(self):
     #   if request.method == 'POST':
      #      print("test")
       # pass

    def get_template_name(self):
        return 'assets/assets.html'

    def get_objects(self):
        assets = []

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
                    'rate': asset.rates.get(base, {}).get('rate', 'N/A'),
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
        self.app.user.sell()

        graphs_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
        action = request.path
        if(action != "/assets"):
            count = float(request.args.get('count'))
            price = float(request.args.get('rate'))
            crypto_name = request.args.get('name')
        if(action == "/sell"):
            self.app.user.sell(count, price, crypto_name)
        elif(action == "/buy"):
            self.app.user.buy(count, price, crypto_name)

        return {
            'assets': assets,
            'local_currency': self.app.local_currency,
            'graphJSON': graphs_json
        }
