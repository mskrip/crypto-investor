import datetime
from urllib.parse import urljoin

from cryptoinvestor.api import ApiBase
from cryptoinvestor.models.asset import Asset


class Api(ApiBase):
    def __init__(self, config: dict):
        super(Api, self).__init__(config)

        if config is None:
            config = {}

        self.base = config.get('base_url', 'https://api.coinmarketcap.com/v1/')

    def connect(self) -> bool:
        url = urljoin(self.base, 'ticker')

        r = self.sess.get(url)

        if not r.ok:
            self.error = f"Error connecting to {url}. {r.reason}:{r.status_code}"
            return False

        self.error = ""

        return True

    def get(self) -> [Asset]:
        url = urljoin(self.base, 'ticker/')

        params = {
            'limit': 0
        }

        r = self.sess.get(url, params=params)

        if not r.ok:
            self.error = f"Error connecting to {url}. {r.reason}:{r.status_code}"
            return []

        self.error = ""

        data = r.json()

        assets = []

        for entry in data:
            assets.append(
                Asset(id=entry['id'], name=entry['name'], symbol=entry['symbol'], is_crypto=True)
            )

        return assets

    def load(self, *, asset: Asset, base: str, time: datetime.datetime) -> Asset:
        url = urljoin(self.base, 'ticker/')
        url = urljoin(url, asset.id)

        params = {
            'convert': base
        }

        r = self.sess.get(url, params=params)

        if not r.ok:
            error_msg = r.json()
            self.error = f"Error connecting to {url}. {r.reason}:{r.status_code} -> {error_msg}"
            return None

        data = r.json()[0]

        asset.set_rate(
            base,
            data[f'price_{base.lower()}'],
            datetime.datetime.fromtimestamp(int(data['last_updated']))
        )

        return asset

    def update(self, assets: {str: Asset}) -> {str: Asset}:
        url = urljoin(self.base, 'ticker/')

        bases = set()
        for asset in assets.values():
            if asset.is_loaded():
                for base in asset.rates.keys():
                    bases.add(base)

        params = {
            'limit': 0
        }

        full_data = {}

        for base in bases:
            params.update({
                'convert': base
            })

            r = self.sess.get(url, params=params)

            if not r.ok:
                self.error = f"Error connecting to {url}. {r.reason}:{r.status_code}"
                return {}

            data = r.json()
            full_data[base] = data

        self.error = ""

        updated = {}

        for base in bases:
            data = full_data[base]
            for entry in data:
                asset = assets.get(entry['symbol'])
                if asset and asset.is_loaded():
                    new_time = datetime.datetime.fromtimestamp(int(entry['last_updated']))

                    old_rate = asset.rates.get(base)

                    if old_rate and old_rate.get('time') < new_time:
                        updated[asset.symbol] = asset
                        updated[asset.symbol].set_rate(
                            base,
                            data[f'price_{base.lower()}'],
                            datetime.datetime.fromtimestamp(int(data['last_updated']))
                        )

        return updated
