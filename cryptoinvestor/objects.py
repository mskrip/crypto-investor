import yaml


class Asset:
    class Error(Exception):
        pass

    def __init__(self, id: str, name: str, is_crypto: bool):
        if not name:
            raise self.Error('Name not provided')

        self.id = id
        self.name = name
        self.is_crypto = is_crypto
        self.rates = {}

    def set_rate(self, base: str, rate: float, time: str):
        self.rates[base] = {
            'rate': rate,
            'time': time
        }

    def is_loaded(self) -> bool:
        return len(self.rates) > 0


class AppBase:
    def __init__(self, file):
        self.assets = {}
        self.user = None
        self.config = yaml.load(file)

        self.api = None

    def add_asset(self, name: str, asset: Asset):
        self.assets[name] = asset
