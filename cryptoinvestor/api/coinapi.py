import datetime
import os
import logging

from urllib.parse import urljoin

from cryptoinvestor.api import ApiBase
from cryptoinvestor.objects import Asset

logger = logging.getLogger(__name__)


class Api(ApiBase):
    def __init__(self, config: dict):
        super(Api, self).__init__(config)
        self.base = config.get('base_url', 'https://rest.coinapi.io/v1/')

        self.sess.headers.update({
            'X-CoinAPI-Key': config.get('api_key')
        })

        if not config.get('api_key'):
            config['api_key'] = os.environ.get('COINAPI_KEY')

        if not config.get('api_key'):
            raise self.Error(
                'Please provide CoinApi access key in env variable \'COINAPI_KEY\''
            )

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
                is_crypto=asset.get('type_is_crypto')
            ))

        self.error = ''

        return assets

    def load(self, *, e_rate: Asset, base: str, time: datetime.datetime) -> Asset:
        url = urljoin(self.base, f'exchangerate/{e_rate.id}/{base}')

        payload = {
            'time': time.isoformat()
        }

        r = self.sess.get(url, data=payload)

        if not r.ok:
            self.error = f'Error loading data from {url}'
            return None

        data = r.json()

        if not data:
            self.error = f'No data loaded from {url}'
        else:
            self.error = ''

        e_rate.set_rate(data.get('asset_id_quote'), data.get('rate'), data.get('time'))

        return e_rate
