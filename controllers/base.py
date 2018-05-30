#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create base handlers.
"""
from json import loads
from abc import abstractmethod, ABCMeta
import jwt
from jwt import DecodeError

from psycopg2 import Error, ProgrammingError
from requests import exceptions

from psycopg2._psycopg import DataError
from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode, json_decode

from modules.user import get_new_user_struct_cookie
from settings.accounts import __GOOGLE_SETTINGS__, __FACEBOOK_SETTINGS__, \
                                __JWT_SECRET__, __JWT_ALGORITHM__
from settings.settings import __REDIRECT_URI_GOOGLE__, __REDIRECT_URI_GOOGLE_DEBUG__, \
                                __REDIRECT_URI_FACEBOOK__, __REDIRECT_URI_FACEBOOK_DEBUG__, \
                                __AFTER_LOGIN_REDIRECT_TO__, __AFTER_LOGIN_REDIRECT_TO_DEBUG__


def catch_generic_exception(method):

    def wrapper(self, *args, **kwargs):

        try:
            # try to execute the method
            return method(self, *args, **kwargs)

        # all methods can raise a psycopg exception, so catch it
        except ProgrammingError as error:
            # print(">>>> ", error)
            self.PGSQLConn.rollback()  # do a rollback to comeback in a safe state of DB
            raise HTTPError(500, "Psycopg2 error (psycopg2.ProgrammingError). Please, contact the administrator. " +
                                 "\nInformation: " + str(error) + "\npgcode: " + str(error.pgcode))

        except Error as error:
            # print(">>>> ", dir(error))
            self.PGSQLConn.rollback()  # do a rollback to comeback in a safe state of DB
            raise HTTPError(500, "Psycopg2 error (psycopg2.Error). Please, contact the administrator. " +
                                 "\n Information: " + str(error) + "\npgcode: " + str(error.pgcode))

    return wrapper


# def auth_non_browser_based(method):
#     """
#     Authentication to non browser based service
#     :param method: the method decorated
#     :return: the method wrapped
#     """
#     def wrapper(self, *args, **kwargs):
#
#         # if user is not logged in, so return a 403 Forbidden
#         if not self.current_user:
#             raise HTTPError(403, "It is necessary a user logged in to access this URL.")
#
#         # if the user is logged in, so execute the method
#         return method(self, *args, **kwargs)
#
#     return wrapper

def auth_non_browser_based(method):
    """
    Authentication to non browser based service
    :param method: the method decorated
    :return: the method wrapped
    """

    def wrapper(self, *args, **kwargs):

        if "Authorization" in self.request.headers:
            try:
                token = self.request.headers["Authorization"]
                self.get_decoded_jwt_token(token)
            except HTTPError as error:
                raise error
            except Exception as error:
                raise HTTPError(500, "Problem when authorize a resource. Please, contact the administrator.")

            return method(self, *args, **kwargs)
        else:
            raise HTTPError(403, "It is necessary an Authorization header valid.")

    return wrapper


def just_run_on_debug_mode(method):
    """
    Just run the method on Debug Mode
    :param method: the method decorated
    :return: the method wrapped
    """
    def wrapper(self, *args, **kwargs):

        # if is not in debug mode, so return a 404 Not Found
        if not self.DEBUG_MODE:
            raise HTTPError(404, "Invalid URL.")

        # if is in debug mode, so execute the method
        return method(self, *args, **kwargs)

    return wrapper


def generate_encoded_jwt_token_by_user(user):
    return jwt.encode(user, __JWT_SECRET__, algorithm=__JWT_ALGORITHM__)


# BASE CLASS

class BaseHandler(RequestHandler):
    """
        Responsible class to be a base handler for the others classes.
        It extends of the RequestHandler class.
    """

    # Static list to be added the all valid urls to one handler
    urls = []

    # __init__ for Tornado subclasses
    def initialize(self):
        # get the database instances
        self.PGSQLConn = self.application.PGSQLConn
        # self.Neo4JConn = self.application.Neo4JConn

        self.DEBUG_MODE = self.application.DEBUG_MODE

        if self.DEBUG_MODE:
            self.__REDIRECT_URI_GOOGLE__ = __REDIRECT_URI_GOOGLE_DEBUG__
            self.__REDIRECT_URI_FACEBOOK__ = __REDIRECT_URI_FACEBOOK_DEBUG__
            self.__AFTER_LOGIN_REDIRECT_TO__ = __AFTER_LOGIN_REDIRECT_TO_DEBUG__
        else:
            self.__REDIRECT_URI_GOOGLE__ = __REDIRECT_URI_GOOGLE__
            self.__REDIRECT_URI_FACEBOOK__ = __REDIRECT_URI_FACEBOOK__
            self.__AFTER_LOGIN_REDIRECT_TO__ = __AFTER_LOGIN_REDIRECT_TO__

    # headers

    def set_default_headers(self):
        # self.set_header('Content-Type', 'application/json; charset="utf-8"')
        self.set_header('Content-Type', 'application/json')

        # how solve the CORS problem: https://stackoverflow.com/questions/32500073/request-header-field-access-control-allow-headers-is-not-allowed-by-itself-in-pr
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization")
        self.set_header('Access-Control-Allow-Methods', ' POST, GET, PUT, DELETE, OPTIONS')
        self.set_header('Access-Control-Expose-Headers', 'Authorization')
        self.set_header("Access-Control-Allow-Credentials", "true")

    def options(self, *args, **kwargs):
        """
        This method is necessary to do the CORS works.
        """
        # no body
        self.set_status(204)
        self.finish()

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

    # LOGIN AND LOGOUT

    def get_decoded_jwt_token(self, token):
        try:
            decoded_jwt_token = jwt.decode(token, __JWT_SECRET__, algorithms=[__JWT_ALGORITHM__])
            return decoded_jwt_token
        except DecodeError as error:
            raise HTTPError(400, "Invalid Token.")  # 400 - Bad request

    @catch_generic_exception
    def auth_login(self, email, password):
        user_in_db = self.PGSQLConn.get_users(email=email, password=password)

        encoded_jwt_token = generate_encoded_jwt_token_by_user(user_in_db["features"][0])

        return encoded_jwt_token

    @catch_generic_exception
    def login(self, user_json):
        # looking for a user in db, if not exist user, so create a new one
        try:
            user_in_db = self.PGSQLConn.get_users(email=user_json["properties"]["email"])
        except HTTPError as error:
            # if the error is different of 404, raise a exception...
            if error.status_code != 404:
                raise HTTPError(500, str(error))
            # ... because I expected a 404 to create a new user
            id_in_json = self.PGSQLConn.create_user(user_json)
            user_in_db = self.PGSQLConn.get_users(user_id=str(id_in_json["user_id"]))

        encoded_jwt_token = generate_encoded_jwt_token_by_user(user_in_db["features"][0])

        return encoded_jwt_token

    # def logout(self):
    #     # if there is no user logged, so raise a exception
    #     if not self.get_current_user():
    #         raise HTTPError(404, "Not found any user to logout.")
    #
    #     # if there is a user logged, so remove it from cookie
    #     self.clear_cookie("user")
    #
    #     # self.redirect(self.__AFTER_LOGGED_OUT_REDIRECT_TO__)

    # COOKIES

    def set_current_user(self, user={}, new_user=True):
        if new_user:
            # if new user, so create a new cookie
            user_cookie = get_new_user_struct_cookie()
        else:
            # if already exist, so get the cookie
            user_cookie = json_decode(self.get_secure_cookie("user"))

        # insert the information
        user_cookie["user"] = user

        # set the cookie (it needs to be separated)
        # transform dictionary in JSON and add in cookie
        encode = json_encode(user_cookie)
        self.set_secure_cookie("user", encode)

    # def get_current_user(self):
    #     user_cookie = self.get_secure_cookie("user")
    #
    #     if user_cookie:
    #         return json_decode(user_cookie)
    #     else:
    #         return None

    def get_current_user(self):
        token = self.request.headers["Authorization"]
        decoded_jwt_token = self.get_decoded_jwt_token(token)
        return decoded_jwt_token

    def get_current_user_id(self):
        try:
            current_user = self.get_current_user()
            return current_user["properties"]["user_id"]
        except KeyError as error:
            return None
            # raise HTTPError(500, "Problem when get the current user. Please, contact the administrator.")

    # URLS

    def get_aguments(self):
        """
        Create the 'arguments' dictionary.
        :return: the 'arguments' dictionary contained the arguments and parameters of URL,
                in a easier way to work with them.
        """
        arguments = {k: self.get_argument(k) for k in self.request.arguments}

        for key in arguments:
            argument = arguments[key].lower()

            # transform in boolean the string received
            if argument == 'true':
                arguments[key] = True
            if argument == 'false':
                arguments[key] = False

        # "q" is the query argument, that have the fields of query
        # if "q" in arguments:
        #     arguments["q"] = self.get_q_param_as_dict_from_str(arguments["q"])
        # else:
        #     # if "q" is not in arguments, so put None value
        #     arguments["q"] = None

        # if key "format" not in arguments, put a default value, the "geojson"
        # if "format" not in arguments:
        #     arguments["format"] = "geojson"

        return arguments

    # AUXILIAR FUNCTION

    def is_element_type_valid(self, element, element_json):
        multi_element = element_json["features"][0]["geometry"]["type"]

        return ((element == "point" and multi_element == "MultiPoint") or
                (element == "line" and multi_element == "MultiLineString") or
                (element == "polygon" and multi_element == "MultiPolygon"))

    def get_q_param_as_dict_from_str(self, str_query):
        str_query = str_query.strip()

        # normal case: I have a query
        prequery = str_query.replace(r"[", "").replace(r"]", "").split(",")

        # with each part of the string, create a dictionary
        query = {}
        for condiction in prequery:
            parts = condiction.split("=")
            query[parts[0]] = parts[1]

        return query


# TEMPLATE METHOD

class BaseHandlerTemplateMethod(BaseHandler, metaclass=ABCMeta):
    ##################################################
    # GET METHOD
    ##################################################

    @catch_generic_exception
    def get_method_api_feature(self, *args):
        arguments = self.get_aguments()

        try:
            # break the arguments dict in each parameter of method
            result = self._get_feature(*args, **arguments)
        except DataError as error:
            # print("Error: ", error)
            raise HTTPError(500, "Problem when get a resource. Please, contact the administrator.")

        # Default: self.set_header('Content-Type', 'application/json')
        self.write(json_encode(result))

    def _get_feature(self, *args, **kwargs):
        raise NotImplementedError

    ##################################################
    # PUT METHOD
    ##################################################

    @catch_generic_exception
    def put_method_api_feature(self, *args):
        param = args[0]

        # remove the first argument ('param'), because it is not necessary anymore
        args = args[1:]  # get the second argument and so on

        if param == "create":
            # self._create_feature(*args)
            self.put_method_api_feature_create(*args)
        # elif param == "update":
        #     # self._update_feature(*args)
        #     self.put_method_api_feature_update(*args)
        elif param == "close":
            self._close_feature(*args)
        elif param == "request":
            self._request_feature(*args)
        elif param == "accept":
            self._accept_feature(*args)
        else:
            raise HTTPError(404, "Invalid URL.")

    # create

    def put_method_api_feature_create(self, *args):
        # get the JSON sent, to add in DB
        feature_json = self.get_the_json_validated()
        current_user_id = self.get_current_user_id()
        arguments = self.get_aguments()

        try:
            json_with_id = self._create_feature(feature_json, current_user_id, **arguments)

            # do commit after create a feature
            self.PGSQLConn.commit()
        except DataError as error:
            # print("Error: ", error)
            raise HTTPError(500, "Problem when create a resource. Please, contact the administrator.")

        # Default: self.set_header('Content-Type', 'application/json')
        self.write(json_encode(json_with_id))

    def _create_feature(self, feature_json, current_user_id, **kwargs):
        raise NotImplementedError

    # update

    def put_method_api_feature_update(self, *args):
        # get the JSON sent, to add in DB
        feature_json = self.get_the_json_validated()
        # current_user_id = self.get_current_user_id()

        try:
            # json_with_id = self._create_feature(feature_json, current_user_id)
            self._update_feature(feature_json)

            # do commit after create a feature
            self.PGSQLConn.commit()
        except DataError as error:
            # print("Error: ", error)
            raise HTTPError(500, "Problem when update a feature. Please, contact the administrator.")

    def _update_feature(self, *args, **kwargs):
        raise NotImplementedError

    # close

    def _close_feature(self, *args, **kwargs):
        raise NotImplementedError

    # request

    def _request_feature(self, *args, **kwargs):
        raise NotImplementedError

    # accept

    def _accept_feature(self, *args, **kwargs):
        raise NotImplementedError

    ##################################################
    # DELETE METHOD
    ##################################################

    @catch_generic_exception
    def delete_method_api_feature(self, *args):
        current_user_id = self.get_current_user_id()
        arguments = self.get_aguments()

        try:
            self._delete_feature(*args, **arguments)

            # do commit after delete the feature
            self.PGSQLConn.commit()
        except DataError as error:
            # print("Error: ", error)
            raise HTTPError(500, "Problem when delete a resource. Please, contact the administrator.")

    def _delete_feature(self, *args, **kwargs):
        raise NotImplementedError


# SUBCLASSES


class BaseHandlerUser(BaseHandlerTemplateMethod):

    def _get_feature(self, *args, **kwargs):
        return self.PGSQLConn.get_users(**kwargs)

    def _create_feature(self, feature_json, current_user_id, **kwargs):
        return self.PGSQLConn.create_user(feature_json)

    def _update_feature(self, *args, **kwargs):
        raise NotImplementedError

    def _delete_feature(self, *args, **kwargs):
        self.delete_validation()

        user_id = args[0]

        self.PGSQLConn.delete_user(user_id)

    def delete_validation(self):
        """
        Verify if a user is administrator to delete a user.
        Just administrators can delete users.
        :return:
        """

        current_user = self.get_current_user()

        is_the_admin = current_user["properties"]["is_the_admin"]

        if not is_the_admin:
            raise HTTPError(403, "Just administrator can delete other user.")


# class BaseHandlerUserGroup(BaseHandlerTemplateMethod):
#
#     def _get_feature(self, *args, **kwargs):
#         return self.PGSQLConn.get_user_group(**kwargs)
#
#     def _create_feature(self, feature_json, current_user_id):
#         return self.PGSQLConn.create_user_group(feature_json, current_user_id)
#
#     def _update_feature(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _request_feature(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _accept_feature(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _delete_feature(self, *args, **kwargs):
#         # receive user_id and group_id as argument
#         arguments = self.get_aguments()
#
#         self.PGSQLConn.delete_user_group(**arguments)


# class BaseHandlerGroup(BaseHandlerTemplateMethod):
#
#     def _get_feature(self, *args, **kwargs):
#         return self.PGSQLConn.get_group(**kwargs)
#
#     def _create_feature(self, feature_json, current_user_id):
#         return self.PGSQLConn.create_group(feature_json, current_user_id)
#
#     def _update_feature(self, feature_json):
#         return self.PGSQLConn.update_group(feature_json)
#
#     def _delete_feature(self, *args, **kwargs):
#         self.PGSQLConn.delete_group_in_db(*args)


# class BaseHandlerProject(BaseHandlerTemplateMethod):
#
#     def _get_feature(self, *args, **kwargs):
#         return self.PGSQLConn.get_projects(**kwargs)
#
#     def _create_feature(self, feature_json, current_user_id):
#         return self.PGSQLConn.create_project(feature_json, current_user_id)
#
#     def _update_feature(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _delete_feature(self, *args, **kwargs):
#         self.PGSQLConn.delete_project_in_db(*args)


class BaseHandlerLayer(BaseHandlerTemplateMethod):

    # GET

    def _get_feature(self, *args, **kwargs):
        return self.PGSQLConn.get_layers(**kwargs)

    # PUT

    def _create_feature(self, feature_json, current_user_id, **kwargs):
        return self.PGSQLConn.create_layer(feature_json, current_user_id, **kwargs)

    def _update_feature(self, *args, **kwargs):
        raise NotImplementedError

    # DELETE

    def _delete_feature(self, *args, **kwargs):
        self.delete_validation(*args)

        self.PGSQLConn.delete_layer_in_db(*args)

    def delete_validation(self, resource_id):
        """
        Verify if the user has permition to delete a layer
        :param resource_id: layer id
        :return:
        """
        current_user_id = self.get_current_user_id()

        resources = self.PGSQLConn.get_user_layers(layer_id=resource_id)

        for resource in resources["features"]:
            if resource["properties"]['is_the_creator'] and \
                    resource["properties"]['user_id'] == current_user_id:
                # if the current_user_id is the creator of the layer, so ok...
                return

        # ... else, raise an exception.
        raise HTTPError(403, "The owner of the layer is the unique who can delete the layer.")


class BaseHandlerUserLayer(BaseHandlerTemplateMethod):

    # GET

    def _get_feature(self, *args, **kwargs):
        return self.PGSQLConn.get_user_layers(**kwargs)

    # PUT

    def _create_feature(self, feature_json, current_user_id, **kwargs):
        return self.PGSQLConn.create_user_layer(feature_json, **kwargs)

    def _update_feature(self, *args, **kwargs):
        raise NotImplementedError

    # DELETE

    def _delete_feature(self, *args, **kwargs):
        # self.delete_validation(*args)

        self.PGSQLConn.delete_user_layer(**kwargs)

    # def delete_validation(self, resource_id):
    #     """
    #     Verify if the user has permition to delete a layer
    #     :param resource_id: layer id
    #     :return:
    #     """
    #     current_user_id = self.get_current_user_id()
    #
    #     resources = self.PGSQLConn.get_user_layers(layer_id=resource_id)
    #
    #     for resource in resources["features"]:
    #         if resource["properties"]['is_the_creator'] and \
    #                 resource["properties"]['user_id'] == current_user_id:
    #             # if the current_user_id is the creator of the layer, so ok...
    #             return
    #
    #     # ... else, raise an exception.
    #     raise HTTPError(403, "The owner of the layer is the unique who can delete the layer.")



class BaseFeatureTable(BaseHandlerTemplateMethod):

    def _get_feature(self, *args, **kwargs):
        # print("\n\n*args: ", args)
        # print("**kwargs: ", kwargs, "\n\n")
        return self.PGSQLConn.get_feature_table(**kwargs)

    def _create_feature(self, feature_json, current_user_id, **kwargs):
        raise NotImplementedError

    def _update_feature(self, *args, **kwargs):
        raise NotImplementedError

    def _delete_feature(self, *args, **kwargs):
        raise NotImplementedError







# class BaseHandlerFeatureTable(BaseHandlerTemplateMethod):
#
#     def _get_feature(self, *args, **kwargs):
#         raise NotImplementedError
#
#     @catch_generic_exception
#     def _create_feature(self):
#         # get the JSON sent, to add in DB
#         feature_json = self.get_the_json_validated()
#         current_user_id = self.get_current_user_id()
#
#         try:
#             self.PGSQLConn.create_feature_table(feature_json, current_user_id)
#
#             # do commit after create a feature
#             self.PGSQLConn.commit()
#         except DataError as error:
#             # print("Error: ", error)
#             raise HTTPError(500, "Problem when create a resource. Please, contact the administrator.")
#         except ProgrammingError as error:
#             if error.pgcode == "42P07":
#                 self.PGSQLConn.rollback()  # do a rollback to comeback in a safe state of DB
#                 raise HTTPError(400, "Feature table already exist.")
#             else:
#                 raise error
#
#     def _update_feature(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _delete_feature(self, *args, **kwargs):
#         raise NotImplementedError


# class BaseHandlerChangeset(BaseHandlerTemplateMethod):
#
#     def _get_feature(self, *args, **kwargs):
#         return self.PGSQLConn.get_changesets(**kwargs)
#
#     def _create_feature(self, feature_json, current_user_id):
#         return self.PGSQLConn.create_changeset(feature_json, current_user_id)
#
#     def _update_feature(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _close_feature(self, *args, **kwargs):
#         try:
#             self.PGSQLConn.close_changeset(args[0])
#         except DataError as error:
#             # print("Error: ", error)
#             raise HTTPError(500, "Problem when close a feature. Please, contact the administrator.")
#
#     def _delete_feature(self, *args, **kwargs):
#         self.PGSQLConn.delete_changeset_in_db(*args)


# class BaseHandlerNotification(BaseHandlerTemplateMethod):
#
#     def _get_feature(self, *args, **kwargs):
#         return self.PGSQLConn.get_notification(**kwargs)
#
#     def _create_feature(self, feature_json, current_user_id):
#         return self.PGSQLConn.create_notification(feature_json, current_user_id)
#
#     def _update_feature(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _delete_feature(self, *args, **kwargs):
#         self.PGSQLConn.delete_notification_in_db(*args)


# class BaseHandlerElement(BaseHandlerTemplateMethod):
#
#     def _get_feature(self, *args, **kwargs):
#         return self.PGSQLConn.get_elements(args[0], **kwargs)
#
#     def _create_feature(self, feature_json, current_user_id):
#         raise NotImplementedError
#
#     @catch_generic_exception
#     def put_method_api_feature_create(self, *args):
#         element = args[0]
#         feature_json = self.get_the_json_validated()
#
#         if not self.is_element_type_valid(element, feature_json):
#             raise HTTPError(404, "Invalid URL.")
#
#         # current_user_id = self.get_current_user_id()
#
#         list_of_id_of_features_created = []
#
#         try:
#             for feature in feature_json["features"]:
#                 # the CRS is necessary inside the geometry, because the DB needs to know the EPSG
#                 feature["geometry"]["crs"] = feature_json["crs"]
#
#                 list_of_id_of_features_created.append(
#                     # create_element returns the id of the element created
#                     self.PGSQLConn.create_element(element, feature)
#                 )
#
#             # send the elements created to DB
#             self.PGSQLConn.commit()
#
#         except psycopg2.Error as error:
#             # print(">>>> ", error)
#             self.PGSQLConn.rollback()  # do a rollback to comeback in a safe state of DB
#
#             if error.pgcode == "VW001":
#                 # VW001 - The changeset with id=#ID was closed at #CLOSED_AT, so it is not possible to use it
#                 raise HTTPError(409, str(error))
#
#             # if the db error is undefined so raise it again...
#             raise error
#             # raise HTTPError(500, "Psycopg2 error. Please, contact the administrator.")
#             # raise HTTPError(500, "Psycopg2 error. Please, contact the administrator. Information: " + str(error))
#
#         except DataError as error:
#             # print("Error: ", error)
#             raise HTTPError(500, "Problem when create a feature. Please, contact the administrator.")
#
#         # Default: self.set_header('Content-Type', 'application/json')
#         self.write(json_encode(list_of_id_of_features_created))
#
#     def _update_feature(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _delete_feature(self, *args, **kwargs):
#         self.PGSQLConn.delete_element_in_db(*args)


# class BaseHandlerThemeTree(BaseHandlerTemplateMethod):
#
#     def _get_feature(self, *args, **kwargs):
#         return self.Neo4JConn.get_theme_tree()
#
#     def _create_feature(self, feature_json, current_user_id):
#         raise NotImplementedError
#
#     def _update_feature(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _delete_feature(self, *args, **kwargs):
#         raise NotImplementedError
#
#     # def get_method_api_theme(self, param):
#     #     if param == "tree":
#     #         self.get_method_api_theme_tree()
#     #     # else:
#     #     #     self.get_method_api_theme_other()
#
#     # def get_method_api_theme_tree(self):
#     #     try:
#     #         result = self.Neo4JConn.get_theme_tree()
#     #     except DataError as error:
#     #         # print("Error: ", error)
#     #         raise HTTPError(500, "Problem when get the theme tree. Please, contact the administrator.")
#     #     except exceptions.ConnectionError as error:
#     #         # print("Error: ", error)
#     #         raise HTTPError(503, "Connection refused. Please, contact the administrator.")
#     #
#     #     # Default: self.set_header('Content-Type', 'application/json')
#     #     self.write(json_encode(result))
#
#     # def put_method_api_layer_create(self):
#     #     # get the JSON sent, to add in DB
#     #     layer_json = self.get_the_json_validated()
#     #
#     #     current_user_id = self.get_current_user_id()
#     #
#     #     try:
#     #         json_with_id = self.PGSQLConn.create_layer(layer_json, current_user_id)
#     #     except DataError as error:
#     #         # print("Error: ", error)
#     #         raise HTTPError(500, "Problem when create a layer. Please, contact the administrator.")
#     #
#     #     # Default: self.set_header('Content-Type', 'application/json')
#     #     self.write(json_encode(json_with_id))
#     #
#     # def put_method_api_layer(self, param):
#     #     # param on this case is "create" or "update"
#     #     if param == "create":
#     #         self.put_method_api_layer_create()
#     #     elif param == "update":
#     #         self.write(json_encode({"ok", 1}))
#     #     else:
#     #         raise HTTPError(404, "Invalid URL")
#     #
#     # def delete_method_api_layer(self, param):
#     #     # param on this case is the id of element
#     #     try:
#     #         self.PGSQLConn.delete_layer_in_db(param)
#     #     except DataError as error:
#     #         # print("Error: ", error)
#     #         raise HTTPError(500, "Problem when delete a layer. Please, contact the administrator.")

