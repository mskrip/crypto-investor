from cryptoinvestor.views import BaseView


class IndexView(BaseView):
    def get_template_name(self):
        return 'index/index.html'

    def get_objects(self):
        return {
            'user': self.app.user,
            'appname': 'Cryptoinvestor'
        }
