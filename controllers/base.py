#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create base handlers.
"""

from json import loads
from abc import ABCMeta
from os import makedirs
from os.path import exists
from subprocess import check_call, CalledProcessError
from zipfile import ZipFile

from psycopg2._psycopg import DataError

from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode

from settings.settings import __REDIRECT_URI_GOOGLE__, __REDIRECT_URI_GOOGLE_DEBUG__, \
                                __REDIRECT_URI_FACEBOOK__, __REDIRECT_URI_FACEBOOK_DEBUG__, \
                                __AFTER_LOGIN_REDIRECT_TO__, __AFTER_LOGIN_REDIRECT_TO_DEBUG__

from settings.settings import __TEMP_FOLDER__

from modules.common import generate_encoded_jwt_token, get_decoded_jwt_token, exist_shapefile_inside_zip, \
                            catch_generic_exception, auth_non_browser_based, just_run_on_debug_mode


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

    # HEADERS

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
    @catch_generic_exception
    def auth_login(self, email, password):
        user_in_db = self.PGSQLConn.get_users(email=email, password=password)

        encoded_jwt_token = generate_encoded_jwt_token(user_in_db["features"][0])

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

        encoded_jwt_token = generate_encoded_jwt_token(user_in_db["features"][0])

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

    # CURRENT USER

    def get_current_user(self):
        token = self.request.headers["Authorization"]
        user = get_decoded_jwt_token(token)
        return user

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

    # def is_element_type_valid(self, element, element_json):
    #     multi_element = element_json["features"][0]["geometry"]["type"]
    #
    #     return ((element == "point" and multi_element == "MultiPoint") or
    #             (element == "line" and multi_element == "MultiLineString") or
    #             (element == "polygon" and multi_element == "MultiPolygon"))

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
            result = self._get_feature(*args, **arguments)
        except TypeError as error:
            raise HTTPError(400, str(error))
        except DataError as error:
            raise HTTPError(500, "Problem when get a resource. Please, contact the administrator. " +
                                 "(error: " + str(error) + ").")

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
            raise HTTPError(500, "Problem when create a resource. Please, contact the administrator. " +
                            "(error: " + str(error) + ").")

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
            raise HTTPError(500, "Problem when update a feature. Please, contact the administrator. " +
                            "(error: " + str(error) + ").")

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
            self._delete_feature(current_user_id, *args, **arguments)

            # do commit after delete the feature
            self.PGSQLConn.commit()
        except DataError as error:
            raise HTTPError(500, "Problem when delete a resource. Please, contact the administrator. " +
                            "(error: " + str(error) + ").")

    def _delete_feature(self, current_user_id, *args, **kwargs):
        raise NotImplementedError


# SUBCLASSES

class BaseHandlerUser(BaseHandlerTemplateMethod):

    # GET

    def _get_feature(self, *args, **kwargs):
        return self.PGSQLConn.get_users(**kwargs)

    # PUT

    def _create_feature(self, feature_json, current_user_id, **kwargs):
        return self.PGSQLConn.create_user(feature_json)

    def _update_feature(self, *args, **kwargs):
        raise NotImplementedError

    # DELETE

    def _delete_feature(self, current_user_id, *args, **kwargs):
        self.is_current_user_an_administrator()

        user_id = args[0]

        self.PGSQLConn.delete_user(user_id)

    # VALIDATION

    def is_current_user_an_administrator(self):
        """
        Verify if a user is administrator to delete a user.
        Just administrators can delete users.
        :return:
        """

        current_user = self.get_current_user()

        is_the_admin = current_user["properties"]["is_the_admin"]

        if not is_the_admin:
            raise HTTPError(403, "Just administrator can delete other user.")


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

    def _delete_feature(self, current_user_id, *args, **kwargs):
        layer_id = args[0]
        self.can_current_user_delete_a_layer(current_user_id, layer_id)

        self.PGSQLConn.delete_layer_in_db(*args)

    # VALIDATION

    def can_current_user_delete_a_layer(self, current_user_id, layer_id):
        """
        Verify if the user has permission of deleting a layer
        :param resource_id: layer id
        :return:
        """

        layers = self.PGSQLConn.get_user_layers(layer_id=layer_id)

        for layer in layers["features"]:
            if layer["properties"]['is_the_creator'] and \
                    layer["properties"]['user_id'] == current_user_id:
                # if the current_user_id is the creator of the layer, so ok...
                return

        # ... else, raise an exception.
        raise HTTPError(403, "The creator of the layer is the unique who can delete the layer.")


class BaseHandlerUserLayer(BaseHandlerTemplateMethod):

    # GET

    def _get_feature(self, *args, **kwargs):
        return self.PGSQLConn.get_user_layers(**kwargs)

    # PUT

    def _create_feature(self, feature_json, current_user_id, **kwargs):
        if "layer_id" not in feature_json["properties"]:
            raise HTTPError(400, "Some attribute in JSON is missing. Look the documentation! (Hint: layer_id)")

        self.can_current_user_add_user_in_layer(current_user_id, feature_json["properties"]["layer_id"])

        return self.PGSQLConn.create_user_layer(feature_json, **kwargs)

    def _update_feature(self, *args, **kwargs):
        raise NotImplementedError

    # DELETE

    def _delete_feature(self, current_user_id, *args, **kwargs):
        self.can_current_user_delete_user_in_layer(current_user_id, kwargs["layer_id"])

        self.PGSQLConn.delete_user_layer(**kwargs)

    # VALIDATION

    def can_current_user_add_user_in_layer(self, current_user_id, layer_id):
        """
        Verify if the user has permission of adding a user in a layer
        :param layer_id: layer id
        :param current_user_id: current_user_id
        :return:
        """

        layers = self.PGSQLConn.get_user_layers(layer_id=str(layer_id))

        for layer in layers["features"]:
            if layer["properties"]['is_the_creator'] and \
                    layer["properties"]['user_id'] == current_user_id:
                # if the current_user_id is the creator of the layer, so ok...
                return

        # ... else, raise an exception.
        raise HTTPError(403, "The creator of the layer is the unique who can add user in layer.")

    def can_current_user_delete_user_in_layer(self, current_user_id, layer_id):
        """
        Verify if the user has permission of deleting a user from a layer
        :param layer_id: layer id
        :return:
        """

        resources = self.PGSQLConn.get_user_layers(layer_id=layer_id)

        for resource in resources["features"]:
            if resource["properties"]['is_the_creator'] and \
                    resource["properties"]['user_id'] == current_user_id:
                # if the current_user_id is the creator of the layer, so ok...
                return

        # ... else, raise an exception.
        raise HTTPError(403, "The creator of the layer is the unique who can delete a user from a layer.")


class BaseHandlerReference(BaseHandlerTemplateMethod):

    # GET

    def _get_feature(self, *args, **kwargs):
        return self.PGSQLConn.get_references(**kwargs)

    # PUT

    def _create_feature(self, feature_json, current_user_id, **kwargs):
        return self.PGSQLConn.create_reference(feature_json, current_user_id, **kwargs)

    def _update_feature(self, *args, **kwargs):
        raise NotImplementedError

    # DELETE

    def _delete_feature(self, current_user_id, *args, **kwargs):
        # layer_id = args[0]
        # self.can_current_user_delete_a_layer(current_user_id, layer_id)

        self.PGSQLConn.delete_reference_in_db(*args)

    # VALIDATION

    # def can_current_user_delete_a_layer(self, current_user_id, layer_id):
    #     """
    #     Verify if the user has permission of deleting a layer
    #     :param resource_id: layer id
    #     :return:
    #     """
    #
    #     layers = self.PGSQLConn.get_user_layers(layer_id=layer_id)
    #
    #     for layer in layers["features"]:
    #         if layer["properties"]['is_the_creator'] and \
    #                 layer["properties"]['user_id'] == current_user_id:
    #             # if the current_user_id is the creator of the layer, so ok...
    #             return
    #
    #     # ... else, raise an exception.
    #     raise HTTPError(403, "The creator of the layer is the unique who can delete the layer.")

# IMPORT

class BaseHandlerImportShapeFile(BaseHandlerTemplateMethod):

    # GET

    def _get_feature(self, *args, **kwargs):
        raise NotImplementedError

    # PUT

    def _create_feature(self, feature_json, current_user_id, **kwargs):
        raise NotImplementedError

    def _update_feature(self, *args, **kwargs):
        raise NotImplementedError

    # DELETE

    def _delete_feature(self, current_user_id, *args, **kwargs):
        raise NotImplementedError

    # IMPORT

    def save_binary_file_in_folder(self, binary_file, folder_with_file_name):
        """
        :param binary_file: a file in binary
        :param folder_with_file_name: file name of the zip with the path (e.g. /tmp/vgiws/points.zip)
        :return:
        """
        # save the zip with the shp inside the temp folder
        output_file = open(folder_with_file_name, 'wb')  # wb - write binary
        output_file.write(binary_file)
        output_file.close()

    def extract_zip_in_folder(self, folder_with_file_name, folder_to_extract_zip):
        """
        :param folder_with_file_name: file name of the zip with the path (e.g. /tmp/vgiws/points.zip)
        :param folder_to_extract_zip: folder where will extract the zip (e.g. /tmp/vgiws/points)
        :return:
        """
        # extract the zip in a folder
        with ZipFile(folder_with_file_name, "r") as zip_reference:

            # if exist one shapefile inside the zip, so extract the zip, else raise an exception
            if exist_shapefile_inside_zip(zip_reference):
                zip_reference.extractall(folder_to_extract_zip)
            else:
                raise HTTPError(400, "Invalid ZIP! It is necessary to exist a ShapeFile (.shp) inside de ZIP.")

    def import_shp_file_into_postgis(self, f_table_name, shape_file_name, folder_to_extract_zip):
        """
        :param f_table_name: name of the feature table that will be created
        :param folder_to_extract_zip: folder where will extract the zip (e.g. /tmp/vgiws/points)
        :return:
        """

        __DB_CONNECTION__ = self.PGSQLConn.get_db_connection()

        postgresql_connection = '"host=' + __DB_CONNECTION__["HOSTNAME"] + ' dbname=' + __DB_CONNECTION__["DATABASE"] + \
                                ' user=' + __DB_CONNECTION__["USERNAME"] + ' password=' + __DB_CONNECTION__[
                                    "PASSWORD"] + '"'
        try:
            command_to_import_shp_into_postgis = 'ogr2ogr -append -f "PostgreSQL" PG:' + postgresql_connection + ' ' + shape_file_name + \
                                                 ' -nln ' + f_table_name + ' -skipfailures'

            # call a process to execute the command to import the SHP into the PostGIS
            check_call(command_to_import_shp_into_postgis, cwd=folder_to_extract_zip, shell=True)

        except CalledProcessError as error:
            raise HTTPError(500, "Problem when import a resource. Please, contact the administrator.")

    def import_shp(self):
        arguments = self.get_aguments()

        # remove the extension of the file name (e.g. points)
        FILE_NAME_WITHOUT_EXTENSION = arguments["file_name"].replace(".zip", "")

        # if do not exist the temp folder, create it
        if not exists(__TEMP_FOLDER__):
            makedirs(__TEMP_FOLDER__)

        # the file needs to be in a zip file
        if not arguments["file_name"].endswith(".zip"):
            raise HTTPError(400, "Invalid file name: " + str(arguments["file_name"]))

        # file name of the zip (e.g. /tmp/vgiws/points.zip)
        ZIP_FILE_NAME = __TEMP_FOLDER__ + arguments["file_name"]
        # folder where will extract the zip (e.g. /tmp/vgiws/points)
        EXTRACTED_ZIP_FOLDER_NAME = __TEMP_FOLDER__ + FILE_NAME_WITHOUT_EXTENSION
        # name of the SHP file in folder (e.g. /tmp/vgiws/points/points.shp)
        SHP_FILE_NAME = FILE_NAME_WITHOUT_EXTENSION + ".shp"

        # get the binary file in body of the request
        binary_file = self.request.body
        self.save_binary_file_in_folder(binary_file, ZIP_FILE_NAME)

        self.extract_zip_in_folder(ZIP_FILE_NAME, EXTRACTED_ZIP_FOLDER_NAME)

        self.import_shp_file_into_postgis(arguments["f_table_name"], SHP_FILE_NAME, EXTRACTED_ZIP_FOLDER_NAME)


# class BaseFeatureTable(BaseHandlerTemplateMethod):
#
#     def _get_feature(self, *args, **kwargs):
#         # print("\n\n*args: ", args)
#         # print("**kwargs: ", kwargs, "\n\n")
#         return self.PGSQLConn.get_feature_table(**kwargs)
#
#     def _create_feature(self, feature_json, current_user_id, **kwargs):
#         raise NotImplementedError
#
#     def _update_feature(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _delete_feature(self, *args, **kwargs):
#         raise NotImplementedError


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

