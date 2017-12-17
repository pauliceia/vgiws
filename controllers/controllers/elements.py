#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""


from ..base import BaseHandlerElement, auth_non_browser_based


class APIElementNode(BaseHandlerElement):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/node/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/node/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        # param on this case is the id of element
        # self.get_method_api_element("node")
        self.get_method_api_feature("node")

    @auth_non_browser_based
    def put(self, param=None):
        # param on this case is "create" or "update"
        self.put_method_api_element("node", param)

    @auth_non_browser_based
    def delete(self, param=None):
        # param on this case is the id of element
        self.delete_method_api_feature("node", param)


class APIElementWay(BaseHandlerElement):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/way/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/way/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        # param on this case is the id of element
        # self.get_method_api_element("way")
        self.get_method_api_feature("way")

    @auth_non_browser_based
    def put(self, param=None):
        # param on this case is "create" or "update"
        self.put_method_api_element("way", param)

    @auth_non_browser_based
    def delete(self, param=None):
        # param on this case is the id of element
        self.delete_method_api_feature("way", param)


class APIElementArea(BaseHandlerElement):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/area/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/area/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        # param on this case is the id of element
        # self.get_method_api_element("area")
        self.get_method_api_feature("area")

    @auth_non_browser_based
    def put(self, param=None):
        # param on this case is "create" or "update"
        self.put_method_api_element("area", param)

    @auth_non_browser_based
    def delete(self, param=None):
        # param on this case is the id of element
        self.delete_method_api_feature("area", param)


"""
    /api/0.6/[nodes|ways|relations]?#params
OK - Create: PUT /api/0.6/changeset/create
    Read: GET /api/0.6/changeset/#id?include_discussion=true
    Update: PUT /api/0.6/changeset/#id
OK - Close: PUT /api/0.6/changeset/#id/close
    Query: GET /api/0.6/changesets
        user=#uid, open=true, ...
    Add comment: POST /api/0.6/changeset/#id/comment

OK - Read: GET /api/0.6/[node|way|relation]/#id
OK - Create: PUT /api/0.6/[node|way|relation]/create
    Update: PUT /api/0.6/[node|way|relation]/#id
OK - Delete: DELETE /api/0.6/[node|way|relation]/#id
    History: GET /api/0.6/[node|way|relation]/#id/history
        Retrieves all old versions of an element.

base: http://wiki.openstreetmap.org/wiki/API_v0.6
http://wiki.openstreetmap.org/wiki/API_v0.6#Create:_PUT_.2Fapi.2F0.6.2Fchangeset.2Fcreate
http://wiki.openstreetmap.org/wiki/API_v0.6#Create:_PUT_.2Fapi.2F0.6.2F.5Bnode.7Cway.7Crelation.5D.2Fcreate
https://buildinginspector.nypl.org/data

"""