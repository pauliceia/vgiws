#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""


from ..base import *

from settings import VERSION


class APICapabilities(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/capabilities/", r"/api/capabilities"]

    def get(self):
        capabilities = {
            "version": VERSION,
            "status": {
                "database": self.PGSQLConn.get_connection_status(readable=False)
            }
        }

        # Default: self.set_header('Content-Type', 'application/json')
        self.write(json_encode(capabilities))


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
