#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create handlers.
"""

from .base_controller import *

from tornado.escape import json_encode


# pages
class IndexHandler(BaseHandler):
    """
        Responsible class to render the Home Page (Index).
    """

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/", r"/index", r"/index/"]

    def get(self):
        """
            Responsible method to be the GET method for the URLs listed in the attribute called urls.

            Args:
                Nothing until the moment.

            Returns:
                Just render the index page with some context given.

            Raises:
                Nothing until the moment.
        """

        # Some fictional context
        context = {"text": "Welcome"}

        # to render HTML
        self.set_header('Content-Type', 'text/html')

        # The ** before the context do that dictionary is "break" in the positions of the render method
        # The under line is like this: self.render("index.html", text = "Welcome")
        self.render("index.html", **context)


# API Handlers

class APIDocPage(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/doc", r"/api/doc/"]

    def get(self):
        # Some fictional context
        # context = {"text": "API DOC"}

        context = {
            "text": "...",
            "api_urls": [
                {"method": "GET", "url": "/api/",
                 "description": "", "example_geojson": ""},
            ]
        }

        # to render HTML
        self.set_header('Content-Type', 'text/html')

        # The ** before the context do that dictionary is "break" in the positions of the render method
        # The under line is like this: self.render("index.html", text = "Welcome")
        self.render("api/doc/index.html", **context)


class APIElement(BaseHandler):

    # A list of URLs that can be use for the HTTP methods

    urls = [r"/api/(?P<element>[^\/]+)/?(?P<param>[A-Za-z0-9-]+)?",
            r"/api/(?P<element>[^\/]+)/?(?P<param>[A-Za-z0-9-]+)?/"]

    def get(self, element, param=None):

        arguments, parameters = self.get_aguments_and_parameters(element, param)

        # print("self.request.arguments: ", self.request.arguments)
        # print("arguments", arguments)
        # print("arguments['q']: ", arguments["q"])
        # print("parameters: ", parameters)
        # print("element: ", parameters["element"])
        # print("self.PGSQLConn: ", self.PGSQLConn)

        result_list = self.PGSQLConn.get_elements(parameters["element"],
                                                  q=arguments["q"],
                                                  format=arguments["format"])

        # Default: self.set_header('Content-Type', 'application/json')
        self.write(json_encode(result_list))


"""
/api/0.6/[nodes|ways|relations]?#params
Create: PUT /api/0.6/changeset/create
Read: GET /api/0.6/changeset/#id?include_discussion=true
Update: PUT /api/0.6/changeset/#id
Close: PUT /api/0.6/changeset/#id/close
Query: GET /api/0.6/changesets
user=#uid, open=true, ...
Add comment: POST /api/0.6/changeset/#id/comment

Create: PUT /api/0.6/[node|way|relation]/create
Read: GET /api/0.6/[node|way|relation]/#id
Update: PUT /api/0.6/[node|way|relation]/#id
Delete: DELETE /api/0.6/[node|way|relation]/#id
History: GET /api/0.6/[node|way|relation]/#id/history
Retrieves all old versions of an element.


"""



# CONSTANTS

def get_subclasses_from_class(vars_class):
    """
        Use: get_subclasses_from_class(vars()['NAME_CLASS'])
        :param vars_class: vars()['NAME_CLASS']
        :return: list with subclasses in a dict form: {"class_name": "class_name", "class_instance": instance}
    """

    return [{"class_name": cls.__name__, "class_instance": cls} for cls in vars_class.__subclasses__()]

__LIST_BASEHANDLER_SUBCLASSES__ = get_subclasses_from_class(vars()['BaseHandler'])
