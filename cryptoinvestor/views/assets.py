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

        graph = [
          {
            'data': [
                {
                    'x': [1, 2, 3],
                    'y': [10, 20, 30],
                    'type': 'scatter'
                },
            ],
            'layout': {
                'title': 'first graph'
            }
          }
        ]

        ids = ['graph-{}'.format(i) for i in range(len(graph))]

        graph_json = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

        return {
            'assets': assets,
            'local_currency': self.app.local_currency,
            'ids': ids,
            'graphJSON': graph_json
        }
