import argparse
import datetime
import flask
import logging
import sys
import yaml


from cryptoinvestor.api.coinapi import Api as CoinApi
from cryptoinvestor.objects import Asset, Singleton

logger = logging.getLogger(__name__)

application = flask.Flask(__name__)


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
        self.user = None
        self.config = {}

        if config_file:
            self.config = yaml.load(config_file)

        self.api = CoinApi(self.config.get('api', {}).get('coinapi'))

        self.run()

    def add_asset(self, name: str, asset: Asset):
        """Adds new asset to app instance

        Arguments:
            name {str} -- [description]
            asset {Asset} -- [description]
        """
        self.assets[name] = asset

    def run(self):
        # Just example code, this will change
        assets = self.api.get()

        if not assets and self.api.error:
            logger.error(self.api.error)

        for asset in assets:
            self.add_asset(asset.id, asset)

        self.api.load(asset=self.assets.get('BTC'), base='EUR', time=datetime.datetime.utcnow())

        if self.api.error:
            logger.error(self.api.error)

        print(self.assets.get('BTC').rates)

    def update_assets(self):
        updated = self.api.update(self.assets)
        self.assets.update(updated)


parser = setup_argparse()
args = parser.parse_args()
app = None


@application.route('/')
def index():
    global app

    if app is None:
        app = App(config_file=args.config)

    app.update_assets()

    return str(app.assets.get('BTC').rates)


def main(args=None):
    application.run()


if __name__ == '__main__':
    sys.exit(main(args))
