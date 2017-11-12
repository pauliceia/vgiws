#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create handlers.
"""

from ..base import *

from tornado.escape import json_encode


class APIProject(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    # urls = [r"/api/project/?(?P<param>[A-Za-z0-9-]+)?/",
    #         r"/api/project/?(?P<param>[A-Za-z0-9-]+)?"]

    urls = [r"/api/project/?(?P<method>[A-Za-z0-9-]+)?/?(?P<id_project>[A-Za-z0-9-]+)?"]

    # @auth_non_browser_based
    def get(self, method=None, id_project=None):
        if method == "get":
            result = self.PGSQLConn.get_projects(id_project)

            # if there is no feature
            if result["features"] is None:
                raise HTTPError(404, "There is no feature")

            # Default: self.set_header('Content-Type', 'application/json')
            self.write(json_encode(result))
        else:
            raise HTTPError(404, "Invalid URL")

    @auth_non_browser_based
    def put(self, method=None, id_project=None):
        if method == "create":
            self.put_method_api_project_create()
        elif method == "update":
            self.write(json_encode({"ok", 1}))
        else:
            raise HTTPError(404, "Invalid URL")

    @auth_non_browser_based
    def delete(self, method=None, id_project=None):
        if method == "delete":
            try:
                self.PGSQLConn.delete_project_in_db(id_project)
            except DataError as error:
                # print("Error: ", error)
                raise HTTPError(400, "Invalid parameter")
        else:
            raise HTTPError(404, "Invalid URL")


# class APIProjectDelete(BaseHandler):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/project/delete/(?P<id_project>[^\/]+)/",
#             r"/api/project/delete/(?P<id_project>[^\/]+)"]
#
#     @auth_non_browser_based
#     def delete(self, id_project):
#         try:
#             self.PGSQLConn.delete_project_in_db(id_project)
#         except DataError as error:
#             # print("Error: ", error)
#             raise HTTPError(400, "Invalid parameter")


# CHANGESET

class APIChangesetCreate(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/changeset/create/", r"/api/changeset/create"]

    @auth_non_browser_based
    def put(self):
        # get the JSON sent, to add in DB
        changeset_json = self.get_the_json_validated()

        current_user_id = self.get_current_user_id()

        json_with_id = self.PGSQLConn.create_changeset(changeset_json, current_user_id)

        # Default: self.set_header('Content-Type', 'application/json')
        self.write(json_encode(json_with_id))


class APIChangesetClose(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/changeset/close/(?P<id_changeset>[^\/]+)/",
            r"/api/changeset/close/(?P<id_changeset>[^\/]+)"]

    @auth_non_browser_based
    def put(self, id_changeset):
        # close the changeset of id = id_changeset
        self.PGSQLConn.close_changeset(id_changeset)

        self.set_and_send_status(status=200, reason="Changeset was closed!")


# ELEMENT

class APIElementNode(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/node/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/node/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        self.get_method_api_element("node", param)

    @auth_non_browser_based
    def put(self, param=None):
        self.put_method_api_element("node", param)

    @auth_non_browser_based
    def delete(self, param=None):
        self.delete_method_api_element("node", param)


class APIElementWay(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/way/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/way/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        self.get_method_api_element("way", param)

    @auth_non_browser_based
    def put(self, param=None):
        self.put_method_api_element("way", param)

    @auth_non_browser_based
    def delete(self, param=None):
        self.delete_method_api_element("way", param)


class APIElementArea(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/area/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/area/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        self.get_method_api_element("area", param)

    @auth_non_browser_based
    def put(self, param=None):
        self.put_method_api_element("area", param)

    @auth_non_browser_based
    def delete(self, param=None):
        self.delete_method_api_element("area", param)


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


class HelperExecute(BaseHandler):

    # A list of URLs that can be use for the HTTP methods

    urls = [r"/helper/execute/", r"/helper/execute"]

    @just_run_on_debug_mode
    def get(self):

        query_text = """            
            SELECT json_agg(json_build_object('name', name, 'geom', ST_AsText(geom) , 
                                                'first_year', first_year, 
                                                'last_year', last_year)) AS jsontags 
            FROM tb_street
            WHERE id >= 1 AND id <= 5;
        """

        result_list = self.PGSQLConn.execute(query_text)

        # Default: self.set_header('Content-Type', 'application/json')
        self.write(json_encode(result_list))
