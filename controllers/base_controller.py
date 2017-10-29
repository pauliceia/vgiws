#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create base handlers.
"""


from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    """
        Responsible class to be a base handler for the others classes.
        It extends of the RequestHandler class.
    """

    # Static list to be added the all valid urls to one handler
    urls = []

    def PGSQLConn(self):
        return self.application.PGSQLConn

    def set_default_headers(self):
        # self.set_header('Content-Type', 'application/pdf; charset="utf-8"')
        self.set_header('Content-Type', 'application/json')

    def get_aguments_and_parameters(self, element, param):
        arguments = {k: self.get_argument(k) for k in self.request.arguments}
        arguments["q"] = self.get_q_param_as_dict_from_str(arguments["q"])

        parameters = {
            "element": element.lower(),
            # if there is value, so True, else False
            "create": True if param is not None and param.lower() == "create" else False,
            "history": True if param is not None and param.lower() == "history" else False
        }

        return arguments, parameters

    def get_q_param_as_dict_from_str(self, str_query):

        str_query = str_query.strip()

        # exceptional case: when I want all values
        # if str_query.lower() == "all":
        #     return "all"

        # normal case: I have a query
        prequery = str_query.replace(r"[", "").replace(r"]", "").split(",")

        # with each part of the string, create a dictionary
        query = {}
        for condiction in prequery:
            parts = condiction.split("=")
            query[parts[0]] = parts[1]

        return query
