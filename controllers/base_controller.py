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

    # __init__ for Tornado subclasses
    def initialize(self):
        self.PGSQLConn = self.application.PGSQLConn

    def set_default_headers(self):
        # self.set_header('Content-Type', 'application/pdf; charset="utf-8"')
        self.set_header('Content-Type', 'application/json')

    def get_aguments_and_parameters(self, element, param):
        """
        Given the 'element' and 'param' passed in URL, create the 'arguments' and 'parameters' dictionaries.
        :param element: is the main parameter of URL, describing the element, i.e. node, way or area.
        :param param: others parameters of URL, like 'create' or 'history'.
        :return: 'arguments' and 'parameters' dictionaries contained the arguments and parameters of URL,
                in a easier way to work with them.
        """
        arguments = {k: self.get_argument(k) for k in self.request.arguments}

        # "q" is the query argument, that have the fields of query
        if "q" in arguments:
            arguments["q"] = self.get_q_param_as_dict_from_str(arguments["q"])
        else:
            # if "q" is not in arguments, so put None value
            arguments["q"] = None

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
