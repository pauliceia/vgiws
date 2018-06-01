#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""

# from ..base import BaseHandlerChangeset
# from modules.common import auth_non_browser_based


# CHANGESET

# class APIChangeset(BaseHandlerChangeset):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/changeset/?(?P<param>[A-Za-z0-9-]+)?/?(?P<param2>[A-Za-z0-9-]+)?"]
#
#     def get(self, param=None, param2=None):
#         self.get_method_api_feature()
#         # self.get_method_api_changeset()
#
#     @auth_non_browser_based
#     def put(self, param=None, param2=None):
#         # self.put_method_api_changeset(param, param2)
#         self.put_method_api_feature(param, param2)
#
#     @auth_non_browser_based
#     def delete(self, param=None, param2=None):
#         # self.delete_method_api_changeset(param)
#         self.delete_method_api_feature(param)
