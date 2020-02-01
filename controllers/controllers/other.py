#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""

from tornado.escape import json_encode

from ..base import BaseHandler, BaseHandlerMask, BaseHandlerConvertGeoJSONToShapefile
from modules.common import auth_non_browser_based, just_run_on_debug_mode, get_decoded_jwt_token

# from settings import VERSION


class APIUserByToken(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/user_by_token/", r"/api/user_by_token"]

    @auth_non_browser_based
    def get(self):
        current_user = self.get_current_user_()

        self.write(json_encode(current_user))


class APIValidateEmailToken(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/validate_email/([^/]+)"]

    def get(self, email_token):
        decoded_token = get_decoded_jwt_token(email_token)

        # change the status of is_email_valid of the user for TRUE
        self.PGSQLConn.update_user_email_is_valid(decoded_token["user_id"])


class APIUpdateUserIsEmailValid(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/is_email_valid", r"/api/is_email_valid/"]

    @just_run_on_debug_mode
    def get(self):
        arguments = self.get_aguments()

        # change the status of is_email_valid of the user for FALSE
        self.PGSQLConn.update_user_email_is_valid(arguments["user_id"], arguments["is_email_valid"])


# MASK

class APIMask(BaseHandlerMask):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/mask", r"/api/mask/"]

    def get(self, param=None):
        self.get_method_api_resource()

    # @auth_non_browser_based
    # def post(self, param=None):
    #     self.post_method_api_resource(param)
    #
    # @auth_non_browser_based
    # def put(self, param=None):
    #     self.put_method_api_resource(param)
    #
    # @auth_non_browser_based
    # def delete(self, param=None):
    #     self.delete_method_api_resource(param)


# CONVERT GEOJSON TO SHAPEFILE

class APIConvertGeoJSONToShapefile(BaseHandlerConvertGeoJSONToShapefile):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/convert_geojson_to_shapefile/", r"/api/convert_geojson_to_shapefile"]

    # def get(self):
    #     self.convert_geojson_to_shapefile()

    def post(self):
        self.convert_geojson_to_shapefile()

    # @auth_non_browser_based
    # def put(self, param=None):
    #     self.put_method_api_resource(param)

    # @auth_non_browser_based
    # def delete(self, param=None):
    #     self.delete_method_api_feature(param)

    # def options(self, param=None):
    #     super().options()


# class APICapabilities(BaseHandler):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/capabilities/", r"/api/capabilities"]
#
#     def get(self):
#         pgsql_status = self.PGSQLConn.get_connection_status(readable=True)
#         # neo4j_status = self.Neo4JConn.get_connection_status(readable=True)
#
#         capabilities = {
#             "version": VERSION,
#             "status": {
#                 "postgresql": pgsql_status
#             }
#         }
#
#         # Default: self.set_header('Content-Type', 'application/json')
#         self.write(json_encode(capabilities))


# class HelperExecute(BaseHandler):
#
#     # A list of URLs that can be use for the HTTP methods
#
#     urls = [r"/helper/execute/", r"/helper/execute"]
#
#     @just_run_on_debug_mode
#     def get(self):
#
#         query_text = """
#             SELECT json_agg(json_build_object('name', name, 'geom', ST_AsText(geom) ,
#                                                 'first_year', first_year,
#                                                 'last_year', last_year)) AS jsontags
#             FROM tb_street
#             WHERE id >= 1 AND id <= 5;
#         """
#
#         result_list = self.PGSQLConn.execute(query_text)
#
#         # Default: self.set_header('Content-Type', 'application/json')
#         self.write(json_encode(result_list))
