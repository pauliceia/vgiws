#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""


from ..base import BaseHandlerLayer, auth_non_browser_based  #, BaseHandlerChangeset


# USER IN GROUP

# class APIUserGroup(BaseHandlerUserGroup):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/user_group/?(?P<param>[A-Za-z0-9-]+)?/",
#             r"/api/user_group/?(?P<param>[A-Za-z0-9-]+)?"]
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


# GROUP

# class APIGroup(BaseHandlerGroup):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/group/?(?P<param>[A-Za-z0-9-]+)?/",
#             r"/api/group/?(?P<param>[A-Za-z0-9-]+)?"]
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


# PROJECT

# class APIProject(BaseHandlerProject):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/project/?(?P<param>[A-Za-z0-9-]+)?/",
#             r"/api/project/?(?P<param>[A-Za-z0-9-]+)?"]
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



# LAYER


class APILayer(BaseHandlerLayer):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/layer/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/layer/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        # self.get_method_api_layer()
        self.get_method_api_feature()

    @auth_non_browser_based
    def put(self, param=None):
        # self.put_method_api_layer(param)
        self.put_method_api_feature(param)

    @auth_non_browser_based
    def delete(self, param=None):
        self.delete_method_api_feature(param)

    # def options(self, param=None):
    #     super().options()


# FEATURE TABLE


# class APIFeatureTable(BaseHandlerFeatureTable):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/feature_table/?(?P<param>[A-Za-z0-9-]+)?/",
#             r"/api/feature_table/?(?P<param>[A-Za-z0-9-]+)?"]
#
#     # def get(self, param=None):
#     #     # self.get_method_api_layer()
#     #     self.get_method_api_feature()
#
#     @auth_non_browser_based
#     def put(self, param=None):
#         # self.put_method_api_layer(param)
#         self._create_feature()
#
#     # @auth_non_browser_based
#     # def delete(self, param=None):
#     #     self.delete_method_api_feature(param)
#
#     # def options(self, param=None):
#     #     super().options()



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
