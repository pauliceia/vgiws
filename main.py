#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible file to start the application.
"""

from os.path import join, dirname

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line

from settings import *
from settings.accounts import __COOKIE_SECRET__
from controllers.main import __LIST_BASEHANDLER_SUBCLASSES__
from models import *


# define all arguments to pass in command line
# Define which IP will be used
define("address", default=IP_APP, help="run on the given IP", type=str)
# Define which port will be used
define("port", default=PORT_APP, help="run on the given port", type=int)
# Debug mode will detail the information on console and use the test DB
define("debug", default=DEBUG_MODE, help="run in debug mode", type=bool)
# Define if the layers will be published in geoserver
define("publish_layers_in_geoserver", default=PUBLISH_LAYERS_IN_GEOSERVER, help="publish or not the layers in geoserver", type=bool)
# to see the list of arguments, use:
# $ python main.py --help


class HttpServerApplication(Application):
    """
        Responsible class to set the handlers and settings of the application.
    """

    def __init__(self):
        """
            Responsible method to be the constructor of the class.

            Args:
                Nothing until the moment.

            Returns:
                Nothing until the moment.

            Raises:
                Nothing until the moment.
        """

        # All the classes added in the under list have to extend of the BaseHandler class
        # because it that have the static variable called urls
        handler_classes = [subclass["class_instance"] for subclass in __LIST_BASEHANDLER_SUBCLASSES__]

        # Create a new handler ( (url, class) ) using the URL of the list of urls with its class correspondent
        __handlers__ = []
        for __class__ in handler_classes:
            for __url__ in __class__.urls:
                __handlers__.append(
                    (__url__, __class__)  # add a tuple with the URL and instance of CLASS
                )

        # Add the path "static" as static file
        static_path = join(dirname(__file__), "static")
        __handlers__.append( ( r"/static/(.*)", StaticFileHandler, { "path": static_path } ) )

        # Put here the settings of the application, that can be accessed in the template
        __setting__s = dict(
            # blog_title=TITLE_APP,
            blog_title="",
            template_path=join(dirname(__file__), "templates"),
            # xsrf_cookies=True,
            xsrf_cookies=False,
            # how to generate: https://gist.github.com/didip/823887
            cookie_secret=__COOKIE_SECRET__,
            # login_url="/auth/login/",
            login_url=LOGIN_URL,
            debug=options.debug,
            current_year=CURRENT_YEAR,
            author=AUTHOR,

            # Passed functions to be used in the template
            # process_text=process_text,
        )

        # create a global variable to debug mode
        self.DEBUG_MODE = options.debug

        self.PUBLISH_LAYERS_IN_GEOSERVER = options.publish_layers_in_geoserver

        # create a instance of the databases passing arguments
        self.PGSQLConn = PGSQLConnection.get_instance(self.DEBUG_MODE, self.PUBLISH_LAYERS_IN_GEOSERVER)

        # Pass the handlers and the settings created to the constructor of the super class (father class)
        Application.__init__(self, __handlers__, **__setting__s)


def start_application():
    parse_command_line()
    # http_server = HTTPServer(HttpServerApplication(), max_buffer_size=10485760000)  # 10G
    http_server = HTTPServer(HttpServerApplication())
    http_server.listen(options.port, address=options.address)
    print("\nRunning Tornado on " + URL_APP)
    print("Is debug mode? ", options.debug)
    print("Is publishing the layers in Geoserver? ", options.publish_layers_in_geoserver)
    print("Version of service: ", VERSION, "\n")
    IOLoop.current().start()


def stop_application():
    # Get the instance of the DB connection
    PGSQLConn = PGSQLConnection.get_instance()
    # PGSQLConn.close()

    print("Closing the web service! \n\n")
    IOLoop.instance().stop()


def main():
    """
        Responsible function to execute routines to start the application.

        Args:
            Nothing until the moment.

        Returns:
            Nothing until the moment.

        Raises:
            Nothing until the moment.
    """

    try:
        start_application()
    # CTRL+C on linux / CTRL+BREAK on windows
    except KeyboardInterrupt:
        stop_application()


# If this file is the main application, so will execute the main function
# If the file is run as Python script (main), so execute it
# if the file is called as a module, so doesn't execute it
if __name__ == "__main__":
    main()
