"""Make the app."""
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import logging
from tornado.log import enable_pretty_logging

enable_pretty_logging()
# logging.basicConfig(filename='/var/www/youtube-taut/youtube-taut-server.log', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
# settings = {'debug': True, 'auth': True}
settings = {'debug': True}

connections = []

# def send_pluck(the_pluck):
#     """Propagate youtube events across handlers."""
#     global payload
#     payload = the_pluck
#     global flag
#     flag = True


class BaseHandler(tornado.web.RequestHandler):
    """Make the app."""

    def set_default_headers(self):
        """Make the app."""
        print("setting headers, does this happen often")
        logging.debug("setting headers, we need this for CORS (and CORBS!)")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        """Receive POST youtube event info from Chrome ext."""
        payload = json.loads(self.request.body)
        for i in payload:
            ss = ": ".join([str(i), str(payload[i])])
            print(ss)
            logging.debug(ss)
            print(payload[i])
            logging.debug(payload[i])
        self.write('cool youtube action buddy')
        [client.write_message(ss) for client in self.connections]

    def get(self):
        """Make the app."""
        self.write("My dude, you're not supposed to do GETs on this server")

    def options(self):
        """Make the app."""
        # no body
        self.set_status(204)
        self.finish()


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    """Websocket handler to talk to all clients."""

    # connections = set()

    def open(self):
        """Open websocket."""
        logging.debug("socket OPEN - adding to connections")
        print("ppp socket OPEN - adding to connections")
        self.connections.append(self)

    def on_message(self, message):
        """Send a message."""
        logging.debug("socket on_message, content: ")
        print("ppp socket on_message, content: ")
        logging.debug(message)
        print(message)
        [client.write_message("+".join(message)) for client in self.connections]

    def on_pluck(self, message):
        """Send a youtube-statechange message."""
        logging.debug("socket on_pluck, content: ")
        print("ppp socket on_pluck, content: ")
        logging.debug(message)
        print(message)
        [client.write_message("-".join(message)) for client in self.connections]

    def on_close(self):
        """Close websocket."""
        logging.debug("socket CLOSE")
        print("ppp socket CLOSE")
        self.connections.remove(self)


def send_message_to_all(self, message):
    """Make the app."""
    [con.write_message('Hi! Sent to ALL') for con in self.connections]


def make_app():
    """Make the app."""
    return tornado.web.Application([
        (r"/taut", BaseHandler),
        (r"/websocket", SimpleWebSocket),
        (r"/", tornado.web.StaticFileHandler, {'path': 'tester.html'}),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': '/var/www/youtube-taut/server/static'})
    ], **settings)


if __name__ == "__main__":
    """Make the app."""
    app = make_app()
    logging.debug("listening now")
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
