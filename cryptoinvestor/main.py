import argparse
import datetime
import flask
import json
import logging
import os
import sys
import yaml


from cryptoinvestor.api.coinapi import Api as CoinApi
# from cryptoinvestor.api.coinmarketcap import Api as CoinMarketCapApi
from cryptoinvestor.api.firebase import Api as FirebaseApi
from cryptoinvestor.models.asset import Asset
from cryptoinvestor import views, Singleton
from cryptoinvestor.urls import setup_urls
from cryptoinvestor.models.user import User
from cryptoinvestor.models.account import Account

logger = logging.getLogger(__name__)

logging.basicConfig(
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)

application = flask.Flask(__name__)

setup_urls(application)

DEFAULT_DUMP_PATH = '/srv/cryptoinvestor'


def setup_argparse():
    parser = argparse.ArgumentParser('CryptoInvestor app for investment simulations')

    parser.add_argument(
        '--config', '-c', type=argparse.FileType(),
        help='Path to config file. Template in cryptioinvestor/skel/cryptoinvestor.config.yaml'
    )

    return parser


class App(metaclass=Singleton):
    def __init__(self, config_file=None):
        """Base of the whole application. All the necessary data are saved in this instance

        Arguments:
            config_file {stream} -- Configuration file
        """

        self.assets = {}
        self.config = {}
        self.cache = {}
        self.firebase = None
        self.user = User(
            username="user", password="123", account=Account(self.assets, balance=10000)
        )
        try:
            if config_file:
                self.config = yaml.load(config_file)

            self.api = CoinApi(self.config.get('api', {}).get('coinapi'))
            # self.api = CoinMarketCapApi(self.config.get('api', {}).get('coinmarketcap'))
        except Exception as error:
            logger.error(error)
            exit()

        self.local_currency = self.config.get('local_currency', '').upper()
        if not self.local_currency:
            self.local_currency = os.environ.get('LOCAL_CURRENCY')

        if not self.local_currency:
            logger.warn(
                'Local currency not found. Defaulting to EUR. If you want to change that use'
                'env variable \'LOCAL_CURRENCY\''
            )
            self.local_currency = 'EUR'

        self._setup_dump_file(self.config.get('dump_path'))

        try:
            self.firebase = FirebaseApi(self.config.get('api', {}).get('firebase'))
        except FirebaseApi.Error as error:
            logger.warn('Firebase was not set up and is not being used. %s', error)

        self.run()

    def _setup_dump_file(self, path):
        if path is None:
            path = os.environ.get('DUMP_PATH')

        if path is None:
            logger.info(
                'Dump path not found, defaulting to  `%s`. If you want to change that use env'
                'variable \'DUMP_PATH\'', DEFAULT_DUMP_PATH
            )
            path = DEFAULT_DUMP_PATH

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        self.dump_file = os.path.join(path, 'data.cryptoinvestor.dump.json')

    def add_asset(self, name: str, asset: Asset):
        """Adds new asset to app instance

        Arguments:
            name {str} -- [description]
            asset {Asset} -- [description]
        """
        self.assets[name] = asset

    def load(self) -> {str: Asset}:
        load = {}

        if self.firebase:
            load.update(self.firebase.load())

        if os.path.exists(self.dump_file):
            with open(self.dump_file, 'r') as fd:
                try:
                    load.update(json.load(fd))
                except json.decoder.JSONDecodeError:
                    pass

        return load

    def dump(self, asset: Asset):
        load = self.load()

        dump_asset = load.get(asset.symbol, {})

        for base in asset.rates.keys():
            rate = dump_asset.get(base, [])
            rate.append(asset.rates.get(base))

            dump_asset[base] = rate

        load[asset.symbol] = dump_asset

        with open(self.dump_file, 'w') as fd:
            json.dump(load, fd)

        if self.firebase:
            self.firebase.save(load)

    def run(self):
        now = datetime.datetime.utcnow()
        # Just example code, this will change
        assets = self.api.get()

        if not assets and self.api.error:
            logger.error(self.api.error)

        for asset in assets:
            self.add_asset(asset.symbol, asset)

        base = self.local_currency

        btc = self.assets.get('BTC')
        eth = self.assets.get('ETH')

        self.api.load(asset=btc, base=base, time=now)
        self.dump(btc)

        self.api.load(asset=eth, base=base, time=now)
        self.dump(eth)

    def update_assets(self):
        updated = self.api.update(self.assets)

        for key in updated.keys():
            self.dump(self.assets.get(key))

        self.assets.update(updated)

    def add_toast(self, message='No content', color='black'):
        return {
            'message': message,
            'color': color
        }


def main(args=None):
    views.BaseView.app = App(config_file=args.config)
    application.run()


if __name__ == '__main__':
    parser = setup_argparse()
    args = parser.parse_args()

    sys.exit(main(args))
