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

        return {'assets': assets, 'local_currency': self.app.local_currency}
