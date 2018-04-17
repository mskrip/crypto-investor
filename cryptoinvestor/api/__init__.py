import datetime
import requests

from cryptoinvestor.models.asset import Asset


class ApiBase:
    class Error(Exception):
        pass

    def __init__(self, config: dict):
        """Instance of this class represent APIs used by cryptoinvestor mainly for retrieving
           currency data from various places.

        Raises:
            self.Error -- If required configuration is not provided.

        Arguments:
            config {dict} -- Configuration dictionary containing all the necessary info for API
                             to be set up (i.e. api tokens, base url)
        """

        self.sess = requests.Session()
        self.error = ''

    def connect(self) -> bool:
        """Checks whether app can successfuly connect to the API.

        Returns:
            bool -- True if connection was successful else False and sets self.error as error
                    message
        """

        raise NotImplementedError()

    def get(self) -> [Asset]:
        """Loads all assets provided by the API. Not necessarily all the data (like rates)
           just names and some other basic data.

        Returns:
            [Asset] -- List of all loaded assets. If empty self.error may be set to approppriate
                       error message
        """

        raise NotImplementedError()

    def load(self, *, asset: Asset, base: str, time: datetime.datetime) -> Asset:
        """Loads rates for requested asset with a set base. (i.e. asset of BTC and base of USD)

        Arguments:
            asset {Asset} -- Which asset should be loaded.
            base {str} -- Which currency should the rate be loaded agains
            time {datetime.datetime} -- At which time the rate should be calculated (Availability
                                        of this will differ between various APIs). Should be UTC
                                        time

        Returns:
            Asset -- Asset with loaded rate or None if error occured (error message saved in
                     self.error)
        """

        raise NotImplementedError()

    def update(self, assets: {str: Asset}) -> {str: Asset}:
        """Updates all already loaded rates to current timestamp

        Arguments:
            assets {{str: Asset}} -- All assets inside app. Key is abbreviation of asset (i.e. BTC)

        Returns:
            {str: Asset} -- Dictionary of all updated assets
        """

        raise NotImplementedError()
