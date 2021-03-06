import datetime
import os
import logging

from urllib.parse import urljoin

from cryptoinvestor.api import ApiBase
from cryptoinvestor.models.asset import Asset

logger = logging.getLogger(__name__)


class Api(ApiBase):
    def __init__(self, config: dict):
        super(Api, self).__init__(config)

        if config is None:
            config = {}

        self.base = config.get('base_url', 'https://rest.coinapi.io/v1/')

        if not config.get('api_key'):
            config['api_key'] = os.environ.get('COINAPI_KEY')

        if not config.get('api_key'):
            raise self.Error(
                'Please provide CoinApi access key in env variable \'COINAPI_KEY\''
            )

        self.sess.headers.update({
            'X-CoinAPI-Key': config.get('api_key')
        })

    def connect(self) -> bool:
        url = urljoin(self.base, 'exchanges')

        r = self.sess.get(url)

        if not r.ok:
            self.error = f'Error while connecting to {url}'
            return False

        self.error = ''
        return True

    def get(self) -> [Asset]:
        url = urljoin(self.base, 'assets')

        r = self.sess.get(url)

        if not r.ok:
            self.error = f'Error while connecting to {url}'
            return []

        data = r.json()

        assets = []

        for asset in data:
            assets.append(Asset(
                id=asset.get('asset_id'), name=asset.get('name'),
                symbol=asset.get('asset_id'),
                is_crypto=asset.get('type_is_crypto')
            ))

        self.error = ''

        return assets

    def load(self, *, asset: Asset, base: str, time: datetime.datetime) -> Asset:
        payload = {
            'time':  time.strftime('%Y%m%dT%H%M%S')
        }

        url = urljoin(self.base, f'exchangerate/{asset.id}/{base}')

        r = self.sess.get(url, params=payload)

        if not r.ok:
            self.error = f'Error loading data from {url} request: {r.content}'
            return None

        data = r.json()

        if not data:
            self.error = f'No data loaded from {url}'
        else:
            self.error = ''

        asset.set_rate(data.get('asset_id_quote'), data.get('rate'), data.get('time'))

        return asset

    def update(self, assets: {str: Asset}) -> {str: Asset}:
        updated = {}

        now = datetime.datetime.utcnow()

        for asset in assets.values():
            is_new = False
            if asset.is_loaded():
                new_asset = Asset(asset.id, asset.name, asset.symbol, asset.is_crypto)
                for base in asset.rates.keys():
                    self.load(asset=new_asset, base=base, time=now)

                    if asset.rates[base]['time'] < new_asset.rates[base]['time']:
                        is_new = True

                if is_new:
                    updated[asset.symbol] = new_asset

        return updated
