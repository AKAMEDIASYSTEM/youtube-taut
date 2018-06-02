"""Make the app."""
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    """Make the app."""

    def get(self):
        """Make the app."""
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write("Hello, world")


def make_app():
    """Make the app."""
    return tornado.web.Application([
        (r"/taut", MainHandler),
    ])


if __name__ == "__main__":
    """Make the app."""
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
