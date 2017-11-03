#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create handlers.
"""

from ..base import *

from tornado.escape import json_encode


class APIElement(BaseHandler):

    # A list of URLs that can be use for the HTTP methods

    urls = [r"/api/(?P<element>[^\/]+)/?(?P<param>[A-Za-z0-9-]+)?",
            r"/api/(?P<element>[^\/]+)/?(?P<param>[A-Za-z0-9-]+)?/"]

    def get(self, element, param=None):

        arguments, parameters = self.get_aguments_and_parameters(element, param)

        # print("self.request.arguments: ", self.request.arguments)
        # print("arguments", arguments)
        # print("arguments['q']: ", arguments["q"])
        # print("parameters: ", parameters)
        # print("element: ", parameters["element"])
        # print("self.PGSQLConn: ", self.PGSQLConn)

        result_list = self.PGSQLConn.get_elements(parameters["element"],
                                                  q=arguments["q"],
                                                  format=arguments["format"])

        # Default: self.set_header('Content-Type', 'application/json')
        self.write(json_encode(result_list))


class APIChangeset(BaseHandler):

    # A list of URLs that can be use for the HTTP methods

    urls = [r"/api/changeset/create", r"/api/changeset/create/"]

    def get(self):

        id_changeset = self.PGSQLConn.create_changeset()

        # Default: self.set_header('Content-Type', 'application/json')
        self.write(json_encode({"id_changeset": id_changeset}))


"""
/api/0.6/[nodes|ways|relations]?#params
Create: PUT /api/0.6/changeset/create
Read: GET /api/0.6/changeset/#id?include_discussion=true
Update: PUT /api/0.6/changeset/#id
Close: PUT /api/0.6/changeset/#id/close
Query: GET /api/0.6/changesets
    user=#uid, open=true, ...
Add comment: POST /api/0.6/changeset/#id/comment

OK Read: GET /api/0.6/[node|way|relation]/#id
Create: PUT /api/0.6/[node|way|relation]/create
Update: PUT /api/0.6/[node|way|relation]/#id
Delete: DELETE /api/0.6/[node|way|relation]/#id
History: GET /api/0.6/[node|way|relation]/#id/history
    Retrieves all old versions of an element.


"""


class HelperExecute(BaseHandler):

    # A list of URLs that can be use for the HTTP methods

    urls = [r"/helper/execute/", r"/helper/execute"]

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
