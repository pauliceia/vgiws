#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create base handlers.
"""
from json import loads

from psycopg2._psycopg import DataError
from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode, json_decode

from modules.user import get_new_user_struct_cookie


def auth_non_browser_based(method):
    """
    Authentication to non browser based service
    :param method: the method decorated
    :return: the method wrapped
    """
    def wrapper(self, *args, **kwargs):

        # if user is not logged in, so return a 403 Forbidden
        if not self.current_user:
            # raise HTTPError(403)
            self.set_and_send_status(status=403, reason="It needs a user looged to access this URL")
            return

        # if the user is logged in, so execute the method
        return method(self, *args, **kwargs)

    return wrapper


class BaseHandler(RequestHandler):
    """
        Responsible class to be a base handler for the others classes.
        It extends of the RequestHandler class.
    """

    # Static list to be added the all valid urls to one handler
    urls = []

    __AFTER_LOGGED_IN_REDIRECT_TO__ = "/auth/login/success/"
    __AFTER_LOGGED_OUT_REDIRECT_TO__ = "/auth/logout/success/"

    # __init__ for Tornado subclasses
    def initialize(self):
        self.PGSQLConn = self.application.PGSQLConn
        self.DEBUG_MODE = self.application.DEBUG_MODE

    def set_default_headers(self):
        # self.set_header('Content-Type', 'application/json; charset="utf-8"')
        self.set_header('Content-Type', 'application/json')

    def get_the_json_validated(self):
        """
            Responsible method to validate the JSON received in the POST method.

            Args:
                Nothing until the moment.

            Returns:
                The JSON validated.

            Raises:
                - HTTPError (400 - Bad request): if don't receive a JSON.
                - HTTPError (400 - Bad request): if the JSON received is empty or is None.
        """

        # Verify if the type of the content is JSON
        if self.request.headers["Content-Type"].startswith("application/json"):
            # Convert string to unicode in Python 2 or convert bytes to string in Python 3
            # How string in Python 3 is unicode, so independent of version, both are converted in unicode
            foo = self.request.body.decode("utf-8")

            # Transform the string/unicode received to JSON (dictionary in Python)
            search = loads(foo)
        else:
            raise HTTPError(400, "It is not a JSON...")  # 400 - Bad request

        if search == {} or search is None:
            raise HTTPError(400, "The search given is empty...")  # 400 - Bad request

        return search

    ################################################################################
    # LOGIN
    ################################################################################

    def login(self, user, type_login):

        # looking for a user in db, if not exist user, so create a new one
        user_in_db = self.PGSQLConn.get_user_in_db(user["email"])

        if not user_in_db:
            user_in_db = self.PGSQLConn.create_user_in_db(user["email"])

        ############################################################
        # if on debug mode, so print...
        # if self.DEBUG_MODE:
        #     print("Logged in System")
        #     print("user: ", user)
        #     print("user_in_db: ", user_in_db)
        #     print("type_login: ", type_login, "\n")
        ############################################################

        # insert the user in cookie
        self.set_current_user(user=user_in_db, type_login=type_login, new_user=True)

    ################################################################################
    # COOKIES
    ################################################################################

    def set_current_user(self, user={}, type_login="", new_user=True):
        if new_user:
            # if new user, so create a new cookie
            user_cookie = get_new_user_struct_cookie()
        else:
            # if already exist, so get the cookie
            user_cookie = json_decode(self.get_secure_cookie("user"))

        # insert the information
        user_cookie["login"]["user"] = user
        user_cookie["login"]["type_login"] = type_login

        # set the cookie (it needs to be separated)
        # transform dictionary in JSON and add in cookie
        encode = json_encode(user_cookie)
        self.set_secure_cookie("user", encode)

    def get_current_user(self):
        user_cookie = self.get_secure_cookie("user")

        if user_cookie:
            return json_decode(user_cookie)
        else:
            return None

    def get_current_user_id(self):
        user_cookie = self.get_secure_cookie("user")

        if user_cookie:
            user = json_decode(user_cookie)
            return user["login"]["user"]["id"]
        else:
            return None

    ################################################################################
    # URLS
    ################################################################################

    def get_method_api_element(self, element, param):

        arguments, parameters = self.get_aguments_and_parameters(element, param)

        result_list = self.PGSQLConn.get_elements(parameters["element"],
                                                  q=arguments["q"],
                                                  format=arguments["format"])

        # Default: self.set_header('Content-Type', 'application/json')
        self.write(json_encode(result_list))

    def put_method_api_element(self, element, param):

        if param.lower() != "create":
            self.set_and_send_status(status=400, reason="Invalid URL")
            return

        element_json = self.get_the_json_validated()

        if not self.is_element_type_valid(element, element_json):
            self.set_and_send_status(status=400, reason="Invalid element type")
            return

        current_user_id = self.get_current_user_id()

        try:
            json_with_id = self.PGSQLConn.create_element(element, element_json, current_user_id)
        except DataError:
            self.set_and_send_status(status=400, reason="Problem when create a element. " +
                                                        "Please, contact the administrator.")
            return

        # Default: self.set_header('Content-Type', 'application/json')
        self.write(json_encode(json_with_id))

    ################################################################################
    # URLS
    ################################################################################

    # status HTTP

    def set_and_send_status(self, status=404, reason="", extra={}, raise_error=False):

        response_json = {"status": status, "statusText": reason}

        if extra != {}:
            response_json["extra"] = extra

        self.set_status(status, reason=reason)
        self.write(json_encode(response_json))

        if raise_error:
            raise HTTPError(status, reason)

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

        # if key "format" not in arguments, put a default value, the "geojson"
        if "format" not in arguments:
            arguments["format"] = "geojson"

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

    ################################################################################
    # AUXILIAR FUNCTION
    ################################################################################

    def is_element_type_valid(self, element, element_json):
        multi_element = element_json["features"][0]["geometry"]["type"]

        return ((element == "node" and multi_element == "MultiPoint") or
                (element == "way" and multi_element == "MultiLineString") or
                (element == "area" and multi_element == "MultiPolygon"))
