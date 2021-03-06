class Asset:
    class Error(Exception):
        pass

    def __init__(self, id: str, name: str, symbol: str, is_crypto: bool):
        """Asset of some currency with rates

        Arguments:
            id {str} -- Abbreviation or ID of the currency (i.e. USD)
            name {str} -- Full name of the currency (i.e. US Dollar)
            is_crypto {bool} -- If the currency is virtual (cryptocurrency)

        Raises:
            self.Error -- If name is not provided
        """

        if not name:
            raise self.Error('Name not provided')

        self.id = id
        self.name = name
        self.symbol = symbol
        self.is_crypto = is_crypto
        self.rates = {}

    def set_rate(self, base: str, rate: float, time: str):
        """Adds a rate with some base to the currency

        Arguments:
            base {str} -- Base of what other currency is rate calculated against this currency
            rate {float} -- Rate between currencies
            time {str} -- Time at which the currency was loaded in ISO 8601 format
        """

        self.rates[base] = {
            'rate': rate,
            'time': time
        }

    def is_loaded(self) -> bool:
        """Check whether the currency has any loaded rate

        Returns:
            bool -- Asset is loaded
        """

        return len(self.rates) > 0
