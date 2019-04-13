"""Make the app."""
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import logging
from tornado.log import enable_pretty_logging

# enable_pretty_logging()
logging.basicConfig(filename='/var/www/youtube-taut/youtube-taut-server.log', level=logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)
settings = {'debug': True}


class LastState(object):
    """store the latest state globally for new visitors."""

    def __init__(self):
        """Initialize with nothing."""
        self.ls = {}

    def set(self, ns):
        """Set the var."""
        self.ls = ns

    def get(self):
        """Get the var."""
        return self.ls


class BaseHandler(tornado.web.RequestHandler):
    """Make the app."""

    def initialize(self, last_state):
        """Needed to have player state persist across all clients i think."""
        self.last_state = last_state
        print('self.last_state now is:')
        print(self.last_state.get())

    def set_default_headers(self):
        """Make the app."""
        # logging.debug("setting headers, we need this for CORS (and CORBS!)")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        """Receive POST youtube event info from Chrome ext."""
        self.last_state.set(json.loads(self.request.body))
        print('showing last_state next line:')
        print(self.last_state.get())
        logging.debug(self.last_state.get())
        self.write('thanks for the tip-off buddy')
        # next line is what actually forms the taut line; nice lil python list comp
        ls = self.last_state.get()
        [client.write_message(json.dumps(ls)) for client in connections]

    def get(self):
        """Make the app."""
        self.write("My buddy, you're not supposed to do GETs on this server")

    def options(self):
        """Make the app."""
        # no body
        self.set_status(204)
        self.finish()


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    """Websocket handler to talk to all clients."""

    def initialize(self, last_state):
        """Needed to have player state persist across all clients i think."""
        self.last_state = last_state

    def open(self):
        """Open websocket and tell client what we are watching."""
        logging.debug("socket OPEN - adding to connections")
        print("ppp socket OPEN - adding to connections")
        connections.append(self)
        self.write_message(json.dumps(self.last_state.get()))
        logging.debug('sent last_state to new socket client')
        logging.debug(self.last_state.get())
        print(self.last_state.get())

    def on_message(self, message):
        """Send a message to all clients currently connected."""
        logging.debug("socket on_message, content: ")
        print("ppp socket on_message, content: ")
        logging.debug(message)
        print(message)
        [client.write_message("+".join(message)) for client in connections]

    def on_close(self):
        """Close websocket."""
        logging.debug("socket CLOSE")
        print("ppp socket CLOSE")
        connections.remove(self)


def send_message_to_all(self, message):
    """Make the app."""
    [con.write_message('Hi! Sent to ALL') for con in connections]


def make_app():
    """Make the app."""
    last_state = LastState()
    return tornado.web.Application([
        (r"/taut", BaseHandler, dict(last_state=last_state)),
        (r"/websocket", SimpleWebSocket, dict(last_state=last_state)),
        # (r"/(.*)", tornado.web.StaticFileHandler, {'path': '/var/www/youtube-taut/server/static/full.html'}),
        (r"/(.*)", tornado.web.StaticFileHandler, {'path': '/var/www/youtube-taut/server/static/tester2.html'}),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': '/var/www/youtube-taut/server/static'})
    ], **settings)


if __name__ == "__main__":
    """Make the app."""
    connections = []
    # cur_payload = {}
    app = make_app()
    logging.debug("listening now")
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
