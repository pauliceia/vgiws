#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""

from ..base import auth_non_browser_based  #, BaseHandlerChangeset


# NOTIFICATION

# class APINotification(BaseHandlerNotification):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/notification/?(?P<param>[A-Za-z0-9-]+)?/",
#             r"/api/notification/?(?P<param>[A-Za-z0-9-]+)?"]
#
#     def get(self, param=None):
#         self.get_method_api_feature()
#
#     @auth_non_browser_based
#     def put(self, param=None):
#         self.put_method_api_feature(param)
#
#     @auth_non_browser_based
#     def delete(self, param=None):
#         self.delete_method_api_feature(param)
