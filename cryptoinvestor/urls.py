import flask

from cryptoinvestor.views import assets, index, investments


def setup_urls(application: flask.Flask):
    application.add_url_rule('/', view_func=index.IndexView.as_view('index'))
    application.add_url_rule('/assets', view_func=assets.AssetsListView.as_view('assets_listview'))
    application.add_url_rule('/sell', view_func=assets.SellView.as_view('sell_view'))
    application.add_url_rule('/buy', view_func=assets.BuyView.as_view('buy_view'))
    application.add_url_rule(
        '/investments', view_func=investments.InvestmentsListView.as_view('investments_listview')
    )
