import datetime

from cryptoinvestor.api import ApiBase
from cryptoinvestor.objects import Asset


class TestApiBase:
    def test_init(self):
        assert ApiBase({})

    def test_connect(self):
        try:
            api = ApiBase({})
            api.connect()
        except NotImplementedError:
            assert True
            return
        assert True is False

    def test_get(self):
        try:
            api = ApiBase({})
            api.get()
        except NotImplementedError:
            assert True
            return
        assert True is False

    def test_load(self):
        try:
            now = datetime.datetime.now()
            api = ApiBase({})
            acc = Asset('ACC', 'Awesome crypto currency', True)
            api.load(asset=acc, base='USD', time=now)
        except NotImplementedError:
            assert True
            return
        assert True is False

    def test_update(self):
        try:
            api = ApiBase({})
            api.update()
        except NotImplementedError:
            assert True
            return
        assert True is False

    def test_clear(self):
        try:
            api = ApiBase({})
            acc = Asset('ACC', 'Awesome crypto currency', True)
            api.clear(asset=acc)
        except NotImplementedError:
            assert True
            return
        assert True is False

    def test_dump(self):
        try:
            api = ApiBase({})
            api.dump()
        except NotImplementedError:
            assert True
            return
        assert True is False
