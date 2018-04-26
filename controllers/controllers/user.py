#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""


from ..base import BaseHandlerUser, auth_non_browser_based


# USER

class APIUser(BaseHandlerUser):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/user/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/user/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        # self.get_method_api_user()
        self.get_method_api_feature()

    def put(self, param=None):
        self.put_method_api_feature(param)

    # @auth_non_browser_based
    # def delete(self, param=None):
    #     self.delete_method_api_feature(param)
