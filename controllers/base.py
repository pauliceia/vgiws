#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create base handlers.
"""

from json import loads
from abc import ABCMeta
from os import makedirs, remove as remove_file
from os.path import exists
from shutil import rmtree as remove_folder_with_contents
from subprocess import check_call, CalledProcessError
from zipfile import ZipFile

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from psycopg2 import DataError, Error

from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode

from settings.settings import __REDIRECT_URI_GOOGLE__, __REDIRECT_URI_GOOGLE_DEBUG__, \
                                __REDIRECT_URI_FACEBOOK__, __REDIRECT_URI_FACEBOOK_DEBUG__, \
                                __AFTER_LOGIN_REDIRECT_TO__, __AFTER_LOGIN_REDIRECT_TO_DEBUG__
from settings.settings import __TEMP_FOLDER__, __VALIDATE_EMAIL__, __VALIDATE_EMAIL_DEBUG__
from settings.accounts import __TO_MAIL_ADDRESS__, __PASSWORD_MAIL_ADDRESS__, __SMTP_ADDRESS__, __SMTP_PORT__

from modules.common import generate_encoded_jwt_token, get_decoded_jwt_token, exist_shapefile_inside_zip, \
                            get_shapefile_name_inside_zip, catch_generic_exception


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
        # get the database instance
        self.PGSQLConn = self.application.PGSQLConn

        # get the mode of system (debug or not)
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

        # if not user_in_db["features"][0]["properties"]["is_email_valid"]:
        #     raise HTTPError(409, "The email is not validated.")

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
    #     if not self.get_current_user_():
    #         raise HTTPError(404, "Not found any user to logout.")
    #
    #     # if there is a user logged, so remove it from cookie
    #     self.clear_cookie("user")
    #
    #     # self.redirect(self.__AFTER_LOGGED_OUT_REDIRECT_TO__)

    # CURRENT USER

    def get_current_user_(self):
        token = self.request.headers["Authorization"]
        user = get_decoded_jwt_token(token)
        return user

    def get_current_user_id(self):
        try:
            current_user = self.get_current_user_()
            return current_user["properties"]["user_id"]
        except KeyError as error:
            return None
            # raise HTTPError(500, "Problem when get the current user. Please, contact the administrator.")

    def is_current_user_an_administrator(self):
        """
        Verify if the current user is an administrator
        :return: True or False
        """

        current_user = self.get_current_user_()

        return current_user["properties"]["is_the_admin"]

    # MAIL

    def send_notification_to_email(self, to_email_address, subject="", body=""):
        from_mail_address = __TO_MAIL_ADDRESS__

        msg = MIMEMultipart()
        msg['From'] = from_mail_address
        msg['To'] = to_email_address
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = SMTP(__SMTP_ADDRESS__, __SMTP_PORT__)
        server.starttls()
        server.login(from_mail_address, __PASSWORD_MAIL_ADDRESS__)
        server.sendmail(from_mail_address, to_email_address, msg.as_string())
        server.quit()

    def send_validation_email_to(self, to_email_address, user_id):
        if self.DEBUG_MODE:
            url_to_validate_email = __VALIDATE_EMAIL_DEBUG__
        else:
            url_to_validate_email = __VALIDATE_EMAIL__

        email_token = generate_encoded_jwt_token({"user_id": user_id})

        url_to_validate_email += "/" + email_token   # convert bytes to str

        subject = "Email Validation"
        body = """
            Please, not reply this message.

            Please, click on under URL to validate your email:
            {0}
        """.format(url_to_validate_email)
        self.send_notification_to_email(to_email_address, subject=subject, body=body)

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


class BaseHandlerSocialLogin(BaseHandler):

    def social_login(self, user):
        user_json = {
            'type': 'User',
            'properties': {'user_id': -1, 'email': user["email"], 'password': '',
                           'username': user["email"], 'name': user['name'], 'is_email_valid': True,
                           'terms_agreed': True, 'receive_notification_by_email': False}
        }

        encoded_jwt_token = self.login(user_json)

        # self.set_header('Authorization', encoded_jwt_token)
        # put the Token in the URL that redirect
        # URL_TO_REDIRECT = self.__AFTER_LOGIN_REDIRECT_TO__ + "/" + encoded_jwt_token
        # super(BaseHandler, self).redirect(URL_TO_REDIRECT)

        self.write(json_encode({"token": encoded_jwt_token}))


# TEMPLATE METHOD

class BaseHandlerTemplateMethod(BaseHandler, metaclass=ABCMeta):
    ##################################################
    # GET METHOD
    ##################################################

    @catch_generic_exception
    def get_method_api_resource(self, *args):
        arguments = self.get_aguments()

        try:
            result = self._get_resource(*args, **arguments)
        except TypeError as error:
            raise HTTPError(400, str(error))
        except Error as error:
            self.PGSQLConn.rollback()  # do a rollback to comeback in a safe state of DB
            if error.pgcode == "22007":  # 22007 - invalid_datetime_format
                raise HTTPError(400, "Invalid date format. (error: " + str(error) + ")")
            else:
                raise error  # if is other error, so raise it up
        except DataError as error:
            raise HTTPError(500, "Problem when get a resource. Please, contact the administrator. " +
                                 "(error: " + str(error) + " - pgcode " + str(error.pgcode) + " ).")

        # Default: self.set_header('Content-Type', 'application/json')
        self.write(json_encode(result))

    def _get_resource(self, *args, **kwargs):
        raise NotImplementedError

    ##################################################
    # POST METHOD
    ##################################################

    @catch_generic_exception
    def post_method_api_resource(self, *args):
        param = args[0]

        # remove the first argument ('param'), because it is not necessary anymore
        # args = args[1:]  # get the second argument and so on

        if param == "create":
            self.post_method_api_resource_create()
        elif param == "close":
            self.post_method_api_resource_close()
        # elif param == "request":
        #     self._request_resource(*args)
        # elif param == "accept":
        #     self._accept_resource(*args)
        else:
            raise HTTPError(404, "Invalid URL.")

    # create
    def post_method_api_resource_create(self):
        # get the sent JSON, to add in DB
        resource_json = self.get_the_json_validated()
        current_user_id = self.get_current_user_id()
        arguments = self.get_aguments()

        try:
            json_with_id = self._create_resource(resource_json, current_user_id, **arguments)

            # do commit after create a resource
            self.PGSQLConn.commit()
        except KeyError as error:
            raise HTTPError(400, "Some attribute in JSON is missing. Look the documentation! (error: " +
                            str(error) + " is missing)")
        except Error as error:
            self.PGSQLConn.rollback()  # do a rollback to comeback in a safe state of DB
            if error.pgcode == "23505":  # 23505 - unique_violation
                error = str(error).replace("\n", " ").split("DETAIL: ")[1]
                raise HTTPError(400, "Attribute already exists. (error: " + str(error) + ")")
            else:
                raise error  # if is other error, so raise it up
        except DataError as error:
            raise HTTPError(500, "Problem when create a resource. Please, contact the administrator. " +
                            "(error: " + str(error) + " - pgcode " + str(error.pgcode) + " ).")

        self.write(json_encode(json_with_id))

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        raise NotImplementedError

    # close
    def post_method_api_resource_close(self):
        # get the sent JSON, to add in DB
        current_user_id = self.get_current_user_id()
        arguments = self.get_aguments()

        try:
            self._close_resource(current_user_id, **arguments)

            # do commit after create a resource
            self.PGSQLConn.commit()
        except DataError as error:
            raise HTTPError(500, "Problem when close a resource. Please, contact the administrator. " +
                            "(error: " + str(error) + " - pgcode " + str(error.pgcode) + " ).")

    def _close_resource(self, current_user_id, **kwargs):
        raise NotImplementedError

    # request
    # def _request_resource(self, *args, **kwargs):
    #     raise NotImplementedError

    # accept
    # def _accept_resource(self, *args, **kwargs):
    #     raise NotImplementedError

    ##################################################
    # PUT METHOD
    ##################################################

    # update
    @catch_generic_exception
    def put_method_api_resource(self, *args):
        # get the sent JSON, to update in DB
        resource_json = self.get_the_json_validated()
        current_user_id = self.get_current_user_id()
        arguments = self.get_aguments()

        try:
            self._put_resource(resource_json, current_user_id, **arguments)

            # do commit after update a resource
            self.PGSQLConn.commit()
        except KeyError as error:
            raise HTTPError(400, "Some attribute in JSON is missing. Look the documentation! (error: " +
                            str(error) + " is missing)")
        except Error as error:
            self.PGSQLConn.rollback()  # do a rollback to comeback in a safe state of DB
            if error.pgcode == "23505":  # 23505 - unique_violation
                error = str(error).replace("\n", " ").split("DETAIL: ")[1]
                raise HTTPError(400, "Attribute already exists. (error: " + str(error) + ")")
            else:
                raise error  # if is other error, so raise it up
        except DataError as error:
            raise HTTPError(500, "Problem when create a resource. Please, contact the administrator. " +
                            "(error: " + str(error) + " - pgcode " + str(error.pgcode) + " ).")

    def _put_resource(self, resource_json, current_user_id, **kwargs):
        raise NotImplementedError

    ##################################################
    # DELETE METHOD
    ##################################################

    @catch_generic_exception
    def delete_method_api_resource(self, *args):
        current_user_id = self.get_current_user_id()
        arguments = self.get_aguments()

        try:
            self._delete_resource(current_user_id, *args, **arguments)

            # do commit after delete the resource
            self.PGSQLConn.commit()
        except DataError as error:
            raise HTTPError(500, "Problem when delete a resource. Please, contact the administrator. " +
                            "(error: " + str(error) + " - pgcode " + str(error.pgcode) + " ).")

    def _delete_resource(self, current_user_id, *args, **kwargs):
        raise NotImplementedError


# SUBCLASSES

class BaseHandlerUser(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_users(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        result = self.PGSQLConn.create_user(resource_json)

        # if is alright about register a new user, so send to him/her an email
        # self.send_validation_email_to(resource_json["properties"]["email"], result["user_id"])

        return result

    # PUT

    def _put_resource(self, resource_json, current_user_id, **kwargs):
        self.can_current_user_update(current_user_id, resource_json)

        return self.PGSQLConn.update_user(resource_json, current_user_id, **kwargs)

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        self.can_current_user_delete()

        user_id = args[0]

        self.PGSQLConn.delete_user(user_id)

    # VALIDATION

    def can_current_user_update(self, current_user_id, resource_json):
        """
        Verify if a user is himself/herself or an administrator, who are can update another user.
        :return:
        """

        if current_user_id == resource_json["properties"]["user_id"]:
            return

        if self.is_current_user_an_administrator():
            return

        raise HTTPError(403, "Just the own user or an administrator can update a user.")

    def can_current_user_delete(self):
        """
        Verify if a user is administrator to delete another user.
        Just administrators can delete users.
        :return:
        """

        if not self.is_current_user_an_administrator():
            raise HTTPError(403, "Just administrator can delete other user.")


class BaseHandlerCurator(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_curators(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        self.can_current_user_create_update_or_delete_curator()

        return self.PGSQLConn.create_curator(resource_json, current_user_id, **kwargs)

    # PUT

    def _put_resource(self, resource_json, current_user_id, **kwargs):
        self.can_current_user_create_update_or_delete_curator()

        return self.PGSQLConn.update_curator(resource_json, current_user_id, **kwargs)

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        self.can_current_user_create_update_or_delete_curator()

        self.PGSQLConn.delete_curator(**kwargs)

    # VALIDATION

    def can_current_user_create_update_or_delete_curator(self):
        """
        Verify if the current user is an administrator to create, update or delete a curator user
        :return:
        """

        # if currente user is an administrator, so ok ...
        if self.is_current_user_an_administrator():
            return

        # ... else, raise an exception.
        raise HTTPError(403, "The administrator is who can create/update/delete a curator")


class BaseHandlerLayer(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_layers(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        return self.PGSQLConn.create_layer(resource_json, current_user_id, **kwargs)

    # PUT

    def _put_resource(self, *args, **kwargs):
        raise NotImplementedError

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        layer_id = args[0]
        self.can_current_user_delete_a_layer(current_user_id, layer_id)

        self.PGSQLConn.delete_layer(*args)

    # VALIDATION

    def can_current_user_delete_a_layer(self, current_user_id, layer_id):
        """
        Verify if the user has permission of deleting a layer
        :param current_user_id: current user id
        :param layer_id: layer id
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


class BaseHandlerTimeColumns(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_time_columns(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        f_table_name = resource_json["properties"]["f_table_name"]
        self.can_current_user_create_update_or_delete_time_columns(current_user_id, f_table_name)

        return self.PGSQLConn.create_time_columns(resource_json, current_user_id, **kwargs)

    # PUT

    def _put_resource(self, resource_json, current_user_id, **kwargs):
        f_table_name = resource_json["properties"]["f_table_name"]
        self.can_current_user_create_update_or_delete_time_columns(current_user_id, f_table_name)

        return self.PGSQLConn.update_time_columns(resource_json, current_user_id, **kwargs)

    # DELETE

    # def _delete_resource(self, current_user_id, *args, **kwargs):
    #     self.can_current_user_create_update_or_delete_time_columns(current_user_id, kwargs["f_table_name"])
    #
    #     self.PGSQLConn.delete_time_columns(**kwargs)

    # VALIDATION

    def can_current_user_create_update_or_delete_time_columns(self, current_user_id, f_table_name):
        """
        Verify if the current user is an administrator to create, update or delete a curator user
        :return:
        """

        # if currente user is an administrator, so ok ...
        if self.is_current_user_an_administrator():
            return

        # search layers by feature table name and use the layer_id to search the creator of the layer
        layers = self.PGSQLConn.get_layers(f_table_name=f_table_name)
        layer_id = layers["features"][0]["properties"]["layer_id"]

        layers = self.PGSQLConn.get_user_layers(layer_id=str(layer_id))

        for layer in layers["features"]:
            if layer["properties"]['is_the_creator'] and \
                    layer["properties"]['user_id'] == current_user_id:
                # if the current_user_id is the creator of the layer, so ok...
                return

        # ... else, raise an exception.
        raise HTTPError(403, "Just the owner of the layer or administrator can create/update a time_columns")


class BaseHandlerUserLayer(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_user_layers(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        if "layer_id" not in resource_json["properties"]:
            raise HTTPError(400, "Some attribute in JSON is missing. Look the documentation! (Hint: layer_id)")

        self.can_current_user_add_user_in_layer(current_user_id, resource_json["properties"]["layer_id"])

        return self.PGSQLConn.create_user_layer(resource_json, **kwargs)

    # PUT

    def _put_resource(self, *args, **kwargs):
        raise NotImplementedError

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        self.can_current_user_delete_user_in_layer(current_user_id, kwargs["layer_id"])

        self.PGSQLConn.delete_user_layer(**kwargs)

    # VALIDATION

    def can_current_user_add_user_in_layer(self, current_user_id, layer_id):
        """
        Verify if the user has permission of adding a user in a layer
        :param current_user_id: current user id
        :param layer_id: layer id
        :return:
        """

        # if the current user is admin, so ok...
        if self.is_current_user_an_administrator():
            return

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
        :param current_user_id: current user id
        :param layer_id: layer id
        :return:
        """

        # if the current user is admin, so ok...
        if self.is_current_user_an_administrator():
            return

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

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_references(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        return self.PGSQLConn.create_reference(resource_json, current_user_id, **kwargs)

    # PUT

    def _put_resource(self, resource_json, current_user_id, **kwargs):
        if "reference_id" not in resource_json["properties"]:
            raise HTTPError(400, "Some attribute in JSON is missing. Look the documentation! (Hint: reference_id)")

        reference_id = resource_json["properties"]["reference_id"]
        self.can_current_user_update_or_delete(current_user_id, reference_id)

        return self.PGSQLConn.update_reference(resource_json, current_user_id, **kwargs)

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        reference_id = args[0]
        self.can_current_user_update_or_delete(current_user_id, reference_id)

        self.PGSQLConn.delete_reference(*args)

    # VALIDATION

    def can_current_user_update_or_delete(self, current_user_id, reference_id):
        """
        Verify if the user has permission of deleting a reference
        :param current_user_id: current user id
        :param reference_id: reference id
        :return:
        """

        # if the current user is admin, so ok...
        if self.is_current_user_an_administrator():
            return

        references = self.PGSQLConn.get_references(reference_id=reference_id)

        # if the current_user_id is the creator of the reference, so ok...
        if references["features"][0]["properties"]['user_id_creator'] == current_user_id:
            return

        # ... else, raise an exception.
        raise HTTPError(403, "The creator of the reference and the administrator are who can update/delete the reference.")


class BaseHandlerKeyword(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_keywords(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        return self.PGSQLConn.create_keyword(resource_json, current_user_id, **kwargs)

    # PUT

    def _put_resource(self, resource_json, current_user_id, **kwargs):
        if "keyword_id" not in resource_json["properties"]:
            raise HTTPError(400, "Some attribute in JSON is missing. Look the documentation! (Hint: keyword_id)")

        keyword_id = resource_json["properties"]["keyword_id"]
        self.can_current_user_update_or_delete(current_user_id, keyword_id)

        return self.PGSQLConn.update_keyword(resource_json, current_user_id, **kwargs)

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        keyword_id = args[0]
        self.can_current_user_update_or_delete(current_user_id, keyword_id)

        self.PGSQLConn.delete_keyword(*args)

    # VALIDATION

    def can_current_user_update_or_delete(self, current_user_id, keyword_id):
        """
        Verify if the user has permission of deleting a keyword
        :param current_user_id: current user id
        :param keyword_id: keyword id
        :return:
        """

        # if the current user is admin, so ok...
        if self.is_current_user_an_administrator():
            return

        # keywords = self.PGSQLConn.get_keywords(keyword_id=keyword_id)
        #
        # # if the current user is the creator of the reference, so ok...
        # if keywords["features"][0]["properties"]['user_id_creator'] == current_user_id:
        #     return

        # ... else, raise an exception.
        raise HTTPError(403, "The administrator is who can update/delete the keyword.")


class BaseHandlerChangeset(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_changesets(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        return self.PGSQLConn.create_changeset(resource_json, current_user_id)

    def _close_resource(self, current_user_id, **kwargs):
        self.PGSQLConn.close_changeset(current_user_id, **kwargs)

    # PUT

    def _put_resource(self, resource_json, current_user_id, **kwargs):
        raise NotImplementedError

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        self.can_current_user_delete()
        self.PGSQLConn.delete_changeset(**kwargs)

    # VALIDATION

    def can_current_user_delete(self):
        """
        Verify if the user has permission of deleting a resource
        :return:
        """

        # if the current user is admin, so ok...
        if self.is_current_user_an_administrator():
            return

        # ... else, raise an exception.
        raise HTTPError(403, "The administrator is who can delete the changeset.")


class BaseHandlerNotification(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_notification(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        return self.PGSQLConn.create_notification(resource_json, current_user_id, **kwargs)

    # PUT

    def _put_resource(self, resource_json, current_user_id, **kwargs):
        notification_id = resource_json["properties"]["notification_id"]
        self.can_current_user_update_or_delete_notification(current_user_id, notification_id)

        return self.PGSQLConn.update_notification(resource_json, current_user_id, **kwargs)

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        self.can_current_user_update_or_delete_notification(current_user_id, **kwargs)

        self.PGSQLConn.delete_notification(**kwargs)

    # VALIDATION

    def can_current_user_update_or_delete_notification(self, current_user_id, notification_id):
        """
        Verify if the current user can update or delete a notification
        :return:
        """

        # if currente user is an administrator, so ok ...
        if self.is_current_user_an_administrator():
            return

        notification = self.PGSQLConn.get_notification(notification_id=notification_id)

        # if the current_user_id is the creator of the notification, so ok...
        if notification["features"][0]["properties"]['user_id_creator'] == current_user_id:
            return

        # ... else, raise an exception.
        raise HTTPError(403, "The owner of notification or administrator are who can update/delete a notification.")

# class BaseHandlerChangeset(BaseHandlerTemplateMethod):
#
#     def _get_resource(self, *args, **kwargs):
#         return self.PGSQLConn.get_changesets(**kwargs)
#
#     def _create_resource(self, resource_json, current_user_id):
#         return self.PGSQLConn.create_changeset(resource_json, current_user_id)
#
#     def _update_resource(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _close_resource(self, *args, **kwargs):
#         try:
#             self.PGSQLConn.close_changeset(args[0])
#         except DataError as error:
#             # print("Error: ", error)
#             raise HTTPError(500, "Problem when close a resource. Please, contact the administrator.")
#
#     def _delete_resource(self, *args, **kwargs):
#         self.PGSQLConn.delete_changeset_in_db(*args)

# IMPORT

class BaseHandlerImportShapeFile(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        raise NotImplementedError

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        raise NotImplementedError

    # PUT

    def _update_resource(self, *args, **kwargs):
        raise NotImplementedError

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        raise NotImplementedError

    # POST - IMPORT

    def do_validation(self, arguments, binary_file):
        if ("f_table_name" not in arguments) or ("file_name" not in arguments) or ("changeset_id" not in arguments) or\
                ("epsg" not in arguments):
            raise HTTPError(400, "It is necessary to pass the f_table_name, file_name, changeset_id and the epsg in request.")

        if binary_file == b'':
            raise HTTPError(400, "It is necessary to pass one binary zip file in the body of the request.")

        # if do not exist the temp folder, create it
        if not exists(__TEMP_FOLDER__):
            makedirs(__TEMP_FOLDER__)

        # the file needs to be in a zip file
        if not arguments["file_name"].endswith(".zip"):
            raise HTTPError(400, "Invalid file name: " + str(arguments["file_name"]) + ". It is necessary to be a zip.")

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
        remove_and_raise_exception = False

        # extract the zip in a folder
        with ZipFile(folder_with_file_name, "r") as zip_reference:

            # if exist one shapefile inside the zip, so extract the zip, else raise an exception
            if exist_shapefile_inside_zip(zip_reference):
                zip_reference.extractall(folder_to_extract_zip)
            else:
                remove_and_raise_exception = True

        if remove_and_raise_exception:
            # remove the created file after close the file (out of with ZipFile)
            remove_file(folder_with_file_name)
            raise HTTPError(400, "Invalid ZIP! It is necessary to exist a ShapeFile (.shp) inside de ZIP.")

    def import_shp_file_into_postgis(self, f_table_name, shapefile_name, folder_to_extract_zip, epsg):
        """
        :param f_table_name: name of the feature table that will be created
        :param folder_to_extract_zip: folder where will extract the zip (e.g. /tmp/vgiws/points)
        :return:
        """

        __DB_CONNECTION__ = self.PGSQLConn.get_db_connection()

        postgresql_connection = '"host=' + __DB_CONNECTION__["HOSTNAME"] + ' dbname=' + __DB_CONNECTION__["DATABASE"] + \
                                ' user=' + __DB_CONNECTION__["USERNAME"] + ' password=' + __DB_CONNECTION__["PASSWORD"] + '"'
        try:
            # FEATURE TABLE
            # command_to_import_shp_into_postgis = 'ogr2ogr -append -f "PostgreSQL" PG:' + postgresql_connection + ' ' + shapefile_name + \
            #                                      ' -nln ' + f_table_name + ' -skipfailures -lco FID=id -lco GEOMETRY_NAME=geom -a_srs EPSG:' + str(epsg)

            command_to_import_shp_into_postgis = 'ogr2ogr -append -f "PostgreSQL" PG:' + postgresql_connection + ' ' + \
                                                 shapefile_name + ' -nln ' + f_table_name + ' -a_srs EPSG:' + str(epsg) + \
                                                 ' -skipfailures -lco FID=id -lco GEOMETRY_NAME=geom -nlt PROMOTE_TO_MULTI'

            # call a process to execute the command to import the SHP into the PostGIS
            check_call(command_to_import_shp_into_postgis, cwd=folder_to_extract_zip, shell=True)

        except CalledProcessError as error:
            raise HTTPError(500, "Problem when import a resource. Please, contact the administrator.")

    def get_shapefile_name(self, folder_with_file_name):
        """
        :param folder_with_file_name: file name of the zip with the path (e.g. /tmp/vgiws/points.zip)
        :return:
        """
        # open the zip
        with ZipFile(folder_with_file_name, "r") as zip_reference:
            # if exist one shapefile inside the zip, so return the shapefile name, else raise an exception
            return get_shapefile_name_inside_zip(zip_reference)

    def import_shp(self):
        # get the arguments of the request
        arguments = self.get_aguments()
        # get the binary file in body of the request
        binary_file = self.request.body

        self.do_validation(arguments, binary_file)

        # arrange the f_table_name: remove the lateral spaces and change the internal spaces by _
        arguments["f_table_name"] = arguments["f_table_name"].strip().replace(" ", "_")

        # remove the extension of the file name (e.g. points)
        FILE_NAME_WITHOUT_EXTENSION = arguments["file_name"].replace(".zip", "")

        # file name of the zip (e.g. /tmp/vgiws/points.zip)
        ZIP_FILE_NAME = __TEMP_FOLDER__ + arguments["file_name"]
        # folder where will extract the zip (e.g. /tmp/vgiws/points)
        EXTRACTED_ZIP_FOLDER_NAME = __TEMP_FOLDER__ + FILE_NAME_WITHOUT_EXTENSION

        self.save_binary_file_in_folder(binary_file, ZIP_FILE_NAME)

        # name of the SHP file (e.g. points.shp)
        SHP_FILE_NAME = self.get_shapefile_name(ZIP_FILE_NAME)

        self.extract_zip_in_folder(ZIP_FILE_NAME, EXTRACTED_ZIP_FOLDER_NAME)

        self.import_shp_file_into_postgis(arguments["f_table_name"], SHP_FILE_NAME, EXTRACTED_ZIP_FOLDER_NAME, arguments["epsg"])

        VERSION_TABLE_NAME = "version_" + arguments["f_table_name"]

        self.PGSQLConn.create_new_table_with_the_schema_of_old_table(VERSION_TABLE_NAME, arguments["f_table_name"])

        # arranging the feature table
        self.PGSQLConn.add_version_column_in_table(arguments["f_table_name"])
        self.PGSQLConn.add_changeset_id_column_in_table(arguments["f_table_name"])
        self.PGSQLConn.update_feature_table_setting_in_all_records_a_changeset_id(arguments["f_table_name"], arguments["changeset_id"])
        self.PGSQLConn.update_feature_table_setting_in_all_records_a_version(arguments["f_table_name"], 1)

        # arranging the version feature table
        self.PGSQLConn.add_version_column_in_table(VERSION_TABLE_NAME)
        self.PGSQLConn.add_changeset_id_column_in_table(VERSION_TABLE_NAME)

        # commit the feature table
        self.PGSQLConn.commit()
        # publish the feature table/layer in geoserver
        self.PGSQLConn.publish_feature_table_in_geoserver(arguments["f_table_name"])
        # self.PGSQLConn.publish_feature_table_in_geoserver("version_" + arguments["f_table_name"])

        # remove the temporary file and folder of the shapefile
        remove_file(ZIP_FILE_NAME)
        remove_folder_with_contents(EXTRACTED_ZIP_FOLDER_NAME)


# class BaseFeatureTable(BaseHandlerTemplateMethod):
#
#     def _get_resource(self, *args, **kwargs):
#         # print("\n\n*args: ", args)
#         # print("**kwargs: ", kwargs, "\n\n")
#         return self.PGSQLConn.get_resource_table(**kwargs)
#
#     def _create_resource(self, resource_json, current_user_id, **kwargs):
#         raise NotImplementedError
#
#     def _update_resource(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _delete_resource(self, *args, **kwargs):
#         raise NotImplementedError


# class BaseHandlerFeatureTable(BaseHandlerTemplateMethod):
#
#     def _get_resource(self, *args, **kwargs):
#         raise NotImplementedError
#
#     @catch_generic_exception
#     def _create_resource(self):
#         # get the JSON sent, to add in DB
#         resource_json = self.get_the_json_validated()
#         current_user_id = self.get_current_user_id()
#
#         try:
#             self.PGSQLConn.create_resource_table(resource_json, current_user_id)
#
#             # do commit after create a resource
#             self.PGSQLConn.commit()
#         except DataError as error:
#             # print("Error: ", error)
#             raise HTTPError(500, "Problem when create a resource. Please, contact the administrator.")
#         except ProgrammingError as error:
#             if error.pgcode == "42P07":
#                 self.PGSQLConn.rollback()  # do a rollback to comeback in a safe state of DB
#                 raise HTTPError(400, "resource table already exist.")
#             else:
#                 raise error
#
#     def _update_resource(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _delete_resource(self, *args, **kwargs):
#         raise NotImplementedError

# class BaseHandlerElement(BaseHandlerTemplateMethod):
#
#     def _get_resource(self, *args, **kwargs):
#         return self.PGSQLConn.get_elements(args[0], **kwargs)
#
#     def _create_resource(self, resource_json, current_user_id):
#         raise NotImplementedError
#
#     @catch_generic_exception
#     def put_method_api_resource_create(self, *args):
#         element = args[0]
#         resource_json = self.get_the_json_validated()
#
#         if not self.is_element_type_valid(element, resource_json):
#             raise HTTPError(404, "Invalid URL.")
#
#         # current_user_id = self.get_current_user_id()
#
#         list_of_id_of_resources_created = []
#
#         try:
#             for resource in resource_json["features"]:
#                 # the CRS is necessary inside the geometry, because the DB needs to know the EPSG
#                 resource["geometry"]["crs"] = resource_json["crs"]
#
#                 list_of_id_of_resources_created.append(
#                     # create_element returns the id of the element created
#                     self.PGSQLConn.create_element(element, resource)
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
#             raise HTTPError(500, "Problem when create a resource. Please, contact the administrator.")
#
#         # Default: self.set_header('Content-Type', 'application/json')
#         self.write(json_encode(list_of_id_of_resources_created))
#
#     def _update_resource(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def _delete_resource(self, *args, **kwargs):
#         self.PGSQLConn.delete_element_in_db(*args)
