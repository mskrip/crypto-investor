import datetime
import requests

from cryptoinvestor.objects import Asset


class ApiBase:
    class Error(Exception):
        pass

    def __init__(self, config: dict):
        self.sess = requests.Session()
        self.error = ''

    def connect(self) -> bool:
        raise NotImplementedError()

    def get(self) -> [Asset]:
        raise NotImplementedError()

    def load(self, *, asset: Asset, base: str, time: datetime.datetime) -> Asset:
        raise NotImplementedError()

    def update(self) -> list:
        raise NotImplementedError()

    def clear(self, *, asset: Asset):
        raise NotImplementedError()

    def dump(self):
        raise NotImplementedError()
