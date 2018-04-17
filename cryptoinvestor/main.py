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

logger = logging.getLogger(__name__)

application = flask.Flask(__name__)

setup_urls(application)

DEFAULT_DUMP_PATH = '/srv/cryptoinvestor/data.dump.json'

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
        self.user = {'name': 'tester'}  # TODO: instance of user object
        self.config = {}

        if config_file:
            self.config = yaml.load(config_file)

        self.api = CoinApi(self.config.get('api', {}).get('coinapi'))

        self.local_currency = self.config.get('local_currency', '').upper()
        if not self.local_currency:
            self.local_currency = os.environ.get('LOCAL_CURRENCY')

        if not self.local_currency:
            logger.warn(
                'Local currency not found. Defaulting to EUR. If you want to change that use env '
                'variable \'LOCAL_CURRENCY\''
            )
            self.local_currency = 'EUR'

        self.run()

    def add_asset(self, name: str, asset: Asset):
        """Adds new asset to app instance

        Arguments:
            name {str} -- [description]
            asset {Asset} -- [description]
        """
        self.assets[name] = asset

    def run(self):
        now = datetime.datetime.utcnow()
        # Just example code, this will change
        # assets = self.api.get()

        # if not assets and self.api.error:
        #     logger.error(self.api.error)

        # for asset in assets:
        #     self.add_asset(asset.id, asset)

        # self.api.load(
        #     asset=self.assets.get('BTC'), base=self.local_currency, time=now
        # )
        # self.api.load(
        #     asset=self.assets.get('USD'), base=self.local_currency, time=now
        # )

        btc = Asset('BTC', 'Bitcoin', True)

        btc.set_rate('EUR', 1000, now)
        self.add_asset(btc.id, btc)

        usd = Asset('USD', 'US Dollar', False)
        usd.set_rate('EUR', 0.86, now)
        self.add_asset(usd.id, usd)

        if self.api.error:
            logger.error(self.api.error)

        print(self.assets.get('BTC').rates)

    def update_assets(self):
        updated = self.api.update(self.assets)
        self.assets.update(updated)


def main(args=None):
    views.BaseView.app = App(config_file=args.config)
    application.run()


if __name__ == '__main__':
    parser = setup_argparse()
    args = parser.parse_args()

    sys.exit(main(args))
