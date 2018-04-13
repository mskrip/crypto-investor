import plotly
import json

from cryptoinvestor.views import BaseView


class AssetsListView(BaseView):
    def get_template_name(self):
        return 'assets/assets.html'

    def get_objects(self):
        assets = []

        for name in self.app.assets:
            asset = self.app.assets.get(name)
            if asset.is_loaded():
                assets.append({
                    'id': name,
                    'name': asset.name,
                    'rate': asset.rates.get(self.app.local_currency, {}).get('rate', 'N/A'),
                })

        graphs = {
            'BTC': {
                'data': [
                    {
                        'x': [1, 2, 3],
                        'y': [10, 20, 30],
                        'type': 'scatter'
                    },
                ],
                'layout': {
                    'title': 'Bitcoint'
                }
            },
            'USD': {
                'data': [
                    {
                        'x': [1, 2, 3],
                        'y': [18, 2, 22],
                        'type': 'scatter'
                    },
                ],
                'layout': {
                    'title': 'US Dollar'
                }
            }
        }

        graphs_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

        return {
            'assets': assets,
            'local_currency': self.app.local_currency,
            'graphJSON': graphs_json
        }
