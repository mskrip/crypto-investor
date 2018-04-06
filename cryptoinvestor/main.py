import argparse
import datetime
import flask
import logging
import sys

import dash
import dash_html_components as html


from cryptoinvestor.api.coinapi import Api as CoinApi
from cryptoinvestor.objects import AppBase

logger = logging.getLogger(__name__)

application = flask.Flask(__name__)

app.layout = html.Div([
    html.H1('App')
])


def setup_argparse():
    parser = argparse.ArgumentParser('CryptoInvestor app for investment simulations')

    parser.add_argument(
        '--config', '-c', type=argparse.FileType(),
        help='Path to config file. Template in cryptioinvestor/skel/cryptoinvestor.config.yaml',
        required=True
        )

    return parser


class App(AppBase):
    def __init__(self, file):
        super(App, self).__init__(file)

        self.api = CoinApi(self.config.get('api', {}).get('coinapi'))

        assets = self.api.get()

        if not assets and self.api.error:
            logger.error(self.api.error)

        for asset in assets:
            self.add_asset(asset.id, asset)

        print(self.assets)

        self.api.load(e_rate=self.assets.get('BTC'), base='EUR', time=datetime.datetime.now())

        if self.api.error:
            logger.error(self.api.error)

        print(self.assets.get('BTC').rates)


def main():
    parser = setup_argparse()

    args = parser.parse_args()

    App(file=args.config)

def main(args=None):
    application.run()


if __name__ == '__main__':
    sys.exit(main())
