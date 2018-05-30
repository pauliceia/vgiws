#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""

from ..base import auth_non_browser_based #, BaseHandlerThemeTree


# THEME

# class APITheme(BaseHandlerThemeTree):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/theme_tree/?(?P<param>[A-Za-z0-9-]+)?/",
#             r"/api/theme_tree/?(?P<param>[A-Za-z0-9-]+)?"]
#
#     def get(self, param=None):
#         # self.get_method_api_theme(param)
#         self.get_method_api_feature()
#
#     # @auth_non_browser_based
#     # def put(self, param=None):
#     #     print("adding...")
#     #     # self.put_method_api_project(param)
#     #
#     # @auth_non_browser_based
#     # def delete(self, param=None):
#     #     print("deleting...")
#     #     # self.delete_method_api_project(param)
