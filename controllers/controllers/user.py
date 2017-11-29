#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""


from ..base import BaseHandlerUser


# USER

class APIUser(BaseHandlerUser):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/user/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/user/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        self.get_method_api_user()
