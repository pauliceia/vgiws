#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""


from ..base import BaseHandlerProject, BaseHandlerLayer, \
                    BaseHandlerChangeset, auth_non_browser_based


# GROUP

# class APIGroup(BaseHandlerGroup):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/group/?(?P<param>[A-Za-z0-9-]+)?/",
#             r"/api/group/?(?P<param>[A-Za-z0-9-]+)?"]
#
#     def get(self, param=None):
#         self.get_method_api_feature()

    # @auth_non_browser_based
    # def put(self, param=None):
    #     self.put_method_api_feature(param)
    #
    # @auth_non_browser_based
    # def delete(self, param=None):
    #     self.delete_method_api_feature(param)


# PROJECT

class APIProject(BaseHandlerProject):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/project/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/project/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        self.get_method_api_feature()

    @auth_non_browser_based
    def put(self, param=None):
        self.put_method_api_feature(param)

    @auth_non_browser_based
    def delete(self, param=None):
        self.delete_method_api_feature(param)


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


# CHANGESET

class APIChangeset(BaseHandlerChangeset):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/changeset/?(?P<param>[A-Za-z0-9-]+)?/?(?P<param2>[A-Za-z0-9-]+)?"]

    def get(self, param=None, param2=None):
        self.get_method_api_feature()
        # self.get_method_api_changeset()

    @auth_non_browser_based
    def put(self, param=None, param2=None):
        # self.put_method_api_changeset(param, param2)
        self.put_method_api_feature(param, param2)

    @auth_non_browser_based
    def delete(self, param=None, param2=None):
        # self.delete_method_api_changeset(param)
        self.delete_method_api_feature(param)


# class APIChangesetCreate(BaseHandler):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/changeset/create/", r"/api/changeset/create"]
#
#     @auth_non_browser_based
#     def put(self):
#         # get the JSON sent, to add in DB
#         changeset_json = self.get_the_json_validated()
#
#         current_user_id = self.get_current_user_id()
#
#         json_with_id = self.PGSQLConn.create_changeset(changeset_json, current_user_id)
#
#         # Default: self.set_header('Content-Type', 'application/json')
#         self.write(json_encode(json_with_id))
#
#
# class APIChangesetClose(BaseHandler):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/changeset/close/(?P<id_changeset>[^\/]+)/",
#             r"/api/changeset/close/(?P<id_changeset>[^\/]+)"]
#
#     @auth_non_browser_based
#     def put(self, id_changeset):
#         # close the changeset of id = id_changeset
#         self.PGSQLConn.close_changeset(id_changeset)
#
#         self.set_and_send_status(status=200, reason="Changeset was closed!")
