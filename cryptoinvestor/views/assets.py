import plotly
import json

from cryptoinvestor.views import BaseView


class AssetsListView(BaseView):
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

        graphs_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

        return {
            'assets': assets,
            'local_currency': self.app.local_currency,
            'graphJSON': graphs_json
        }
