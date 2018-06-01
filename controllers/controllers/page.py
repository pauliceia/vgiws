#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""

from ..base import BaseHandler


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


# class APIDocPage(BaseHandler):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/doc", r"/api/doc/"]
#
#     def get(self):
#         # Some fictional context
#         # context = {"text": "API DOC"}
#
#         context = {
#             "text": "...",
#             "api_urls": [
#                 {"method": "GET", "url": "/api/",
#                  "description": "", "example_geojson": ""},
#             ]
#         }
#
#         # to render HTML
#         self.set_header('Content-Type', 'text/html')
#
#         # The ** before the context do that dictionary is "break" in the positions of the render method
#         # The under line is like this: self.render("index.html", text = "Welcome")
#         self.render("api/doc/index.html", **context)
