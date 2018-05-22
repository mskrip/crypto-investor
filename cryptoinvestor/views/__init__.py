from flask import redirect, url_for
from flask.views import View
from flask.templating import render_template


class BaseView(View):
    class Error(Exception):
        pass

    app = None

    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        context = self.get_objects()

        rd = context.get('redirect')

        if rd:
            path = self.app.cache.get(rd, {}).get('view', '/')
            return redirect(url_for(path, redirected=rd))

        return self.render_template(context)
