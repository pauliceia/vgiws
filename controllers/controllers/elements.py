#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create handlers.
"""
import functools

from ..base import *

from tornado.web import authenticated
from tornado.escape import json_encode


def auth_non_browser_based(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):

        print(">>> self.current_user: ", self.current_user)
        print(">>> self.get_current_user(): ", self.get_current_user())

        # if user is not logged in, so return a 403 Forbidden
        if not self.current_user:
            # raise HTTPError(403)
            self.set_and_send_status(status=403, reason="It needs a user looged to access this URL")
            return

        return method(self, *args, **kwargs)

    return wrapper


# def auth_non_browser_based(method):
#     """
#     Authentication to non browser based service
#     :param method:
#     :return:
#     """
#
#     def wrapper(self, *args, **kwargs):
#         print(">>> self.current_user: ", self.current_user)
#         print(">>> self.get_current_user(): ", self.get_current_user())
#
#         # if user is not logged in, so return a 403 Forbidden
#         if not self.current_user:
#             # raise HTTPError(403)
#             self.set_and_send_status(status=403, reason="It needs a user looged to access this URL")
#             return
#
#         return method(self, *args, **kwargs)
#
#     return wrapper


class APIChangeset(BaseHandler):

    # A list of URLs that can be use for the HTTP methods

    urls = [r"/api/changeset/create", r"/api/changeset/create/"]

    # @auth_non_browser_based
    def get(self):

        self.set_secure_cookie("a_cookie", "a_value")
        a_cookie = self.get_secure_cookie("a_cookie")

        print(">>> a_cookie ", a_cookie)

        self.set_cookie("a_cookie", "a_value")
        a_cookie = self.get_cookie("a_cookie")

        print(">>> a_cookie ", a_cookie)




        print(">>> self.current_user: ", self.current_user)
        print(">>> self.get_current_user(): ", self.get_current_user())

        # if user is not logged in, so return a 403 Forbidden
        if not self.current_user:
            # raise HTTPError(403)
            self.set_and_send_status(status=403, reason="It needs a user looged to access this URL")
            return


        print("self.current_user: ", self.current_user)

        self.set_and_send_status(status=200, reason="...")



        # current_user = self.get_current_user()
        #
        # # if there is a logged user, can create a changeset
        # if current_user:
        #
        #     id_changeset = self.PGSQLConn.create_changeset()
        #
        #     # Default: self.set_header('Content-Type', 'application/json')
        #     self.write(json_encode({"id_changeset": id_changeset}))
        #
        # else:
        #     self.set_and_send_status(status=400, reason="There is no user logged")



class APIElementNode(BaseHandler):

    # A list of URLs that can be use for the HTTP methods

    urls = [r"/api/node/?(?P<param>[A-Za-z0-9-]+)?",
            r"/api/node/?(?P<param>[A-Za-z0-9-]+)?/"]

    def get(self, param=None):

        self.GET_api_element("node", param)


class APIElementWay(BaseHandler):
    # A list of URLs that can be use for the HTTP methods

    urls = [r"/api/way/?(?P<param>[A-Za-z0-9-]+)?",
            r"/api/way/?(?P<param>[A-Za-z0-9-]+)?/"]

    def get(self, param=None):
        self.GET_api_element("way", param)


class APIElementArea(BaseHandler):
    # A list of URLs that can be use for the HTTP methods

    urls = [r"/api/area/?(?P<param>[A-Za-z0-9-]+)?",
            r"/api/area/?(?P<param>[A-Za-z0-9-]+)?/"]

    def get(self, param=None):
        self.GET_api_element("area", param)


# class APIElement(BaseHandler):
#     # A list of URLs that can be use for the HTTP methods
#
#     # urls = [r"/api/(?P<element>[^\/]+)/?(?P<param>[A-Za-z0-9-]+)?",
#     #         r"/api/(?P<element>[^\/]+)/?(?P<param>[A-Za-z0-9-]+)?/"]
#
#     urls = [r"/api/(?P<element>[(node|way|area)]+)/?(?P<param>[A-Za-z0-9-]+)?",
#             r"/api/(?P<element>[(node|way|area)]+)/?(?P<param>[A-Za-z0-9-]+)?/"]
#
#     def get(self, element, param=None):
#         arguments, parameters = self.get_aguments_and_parameters(element, param)
#
#         # print("self.request.arguments: ", self.request.arguments)
#         # print("arguments", arguments)
#         # print("arguments['q']: ", arguments["q"])
#         # print("parameters: ", parameters)
#         # print("element: ", parameters["element"])
#         # print("self.PGSQLConn: ", self.PGSQLConn)
#
#         result_list = self.PGSQLConn.get_elements(parameters["element"],
#                                                   q=arguments["q"],
#                                                   format=arguments["format"])
#
#         # Default: self.set_header('Content-Type', 'application/json')
#         self.write(json_encode(result_list))




# class APIElement(BaseHandler):
#
#     # A list of URLs that can be use for the HTTP methods
#
#     urls = [r"/api/(?P<element>[^\/]+)/?(?P<param>[A-Za-z0-9-]+)?",
#             r"/api/(?P<element>[^\/]+)/?(?P<param>[A-Za-z0-9-]+)?/"]
#
#     def get(self, element, param=None):
#
#         arguments, parameters = self.get_aguments_and_parameters(element, param)
#
#         # print("self.request.arguments: ", self.request.arguments)
#         print("arguments", arguments)
#         # print("arguments['q']: ", arguments["q"])
#         print("parameters: ", parameters)
#         # print("element: ", parameters["element"])
#         # print("self.PGSQLConn: ", self.PGSQLConn)
#
#         # if the URL is something about changeset
#         if parameters["element"] == "changeset":
#             self.GET_api_changeset(arguments, parameters)
#
#         # if the URL is something about the elements
#         elif parameters["element"] == "node" or parameters["element"] == "way" \
#                 or parameters["element"] == "area":
#             self.GET_api_element(arguments, parameters)
#
#         else:
#             self.set_and_send_status(status=400, reason=("Bad element: {0}".format(parameters["element"])))
#
#
#
#
#         # result_list = self.PGSQLConn.get_elements(parameters["element"],
#         #                                           q=arguments["q"],
#         #                                           format=arguments["format"])
#         #
#         # # Default: self.set_header('Content-Type', 'application/json')
#         # self.write(json_encode(result_list))




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
