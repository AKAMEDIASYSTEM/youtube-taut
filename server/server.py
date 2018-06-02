"""Make the app."""
import tornado.ioloop
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """Make the app."""

    def set_default_headers(self):
        """Make the app."""
        print "setting headers!!!"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        """Make the app."""
        self.write('some post')

    def get(self):
        """Make the app."""
        self.write('some get')

    def options(self):
        """Make the app."""
        # no body
        self.set_status(204)
        self.finish()


class MainHandler(tornado.web.RequestHandler):
    """Make the app."""

    def get(self):
        """Make the app."""
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        # self.set_header('Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')
        self.write("Hello, world")


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
