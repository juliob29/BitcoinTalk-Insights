"""
Functions to start and configure the Sanic
application. It simply configures the server.
"""
import os

from sanic import Sanic
from sanic_compress import Compress
from sanic_cors import CORS, cross_origin
from skill.api.routes import create_routes


class Server:
    """
    Doris HTTP server representation. This class
    contains logic for managing the configuration
    and deployment of a Sanic server.

    Parameters
    ----------
    debug: bool, default False
        If should start with a debugger.

    cors: bool, default True
        If the application should accept CORS
        requests.

    compress: bool, default True
        If the applications should compress messages
        as Gzip before sending them out.
    """
    def __init__(self, debug=False, cors=True, compress=True):
        self.debug = debug
        self.cors = cors
        self.compress = compress

        self.app = self.create()

    def create(self):
        """
        Method for creating a Sanic server.

        Returns
        -------
        A Sanic application object.
        """
        app = Sanic(__name__)
        
        #
        #  Application configuration. Here we
        #  configure the application to accept
        #  CORS requests, its routes, and
        #  its debug flag.
        #
        if self.cors:
            CORS(app)
        
        if self.compress:
            Compress(app)

        app.config['DEBUG'] = self.debug
        create_routes(app)

        return app

    def run(self, *args, **kwargs): # pragma: no cover
        """
        Method for running a Sanic server.

        Parameters
        ----------
        *args, **kwargs: parameters passed to the Sanic application.
        """
        self.app.run(*args, **kwargs)
