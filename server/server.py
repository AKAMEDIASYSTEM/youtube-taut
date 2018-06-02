"""Make the app."""
import tornado.ioloop
import tornado.web
import json


class BaseHandler(tornado.web.RequestHandler):
    """Make the app."""

    def set_default_headers(self):
        """Make the app."""
        print("setting headers, does this happen often")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        """Make the app."""
        payload = json.loads(self.request.body)
        for i in payload:
            print(" : ".join([str(i), payload[i]]))
            # print(payload[i])
        self.write('cool youtube action buddy')

    def get(self):
        """Make the app."""
        self.write('some get')

    def options(self):
        """Make the app."""
        # no body
        self.set_status(204)
        self.finish()


def make_app():
    """Make the app."""
    return tornado.web.Application([
        (r"/taut", BaseHandler),
    ])


if __name__ == "__main__":
    """Make the app."""
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
