#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create base handlers.
"""

from os import listdir, makedirs, remove as remove_file
from os.path import exists, isdir, isfile, getsize as get_file_size, join, sep as os_separator

from abc import ABCMeta
from copy import deepcopy
from difflib import SequenceMatcher
from geopandas import read_file as gp_read_file
from json import loads
import logging
from requests import get as requests_get
from shutil import rmtree as remove_folder_with_contents
from subprocess import check_call, CalledProcessError
from shutil import make_archive
from threading import Thread
from time import sleep
from unidecode import unidecode
from traceback import format_exception
from zipfile import ZipFile, BadZipFile

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

from psycopg2 import ProgrammingError, DataError, Error, InternalError
# from psycopg2._psycopg import DataError

from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode

from settings.settings import __REDIRECT_URI_GOOGLE__, __REDIRECT_URI_GOOGLE_DEBUG__, \
                                __REDIRECT_URI_FACEBOOK__, __REDIRECT_URI_FACEBOOK_DEBUG__, \
                                __AFTER_LOGIN_REDIRECT_TO__, __AFTER_LOGIN_REDIRECT_TO_DEBUG__
from settings.settings import __TEMP_FOLDER__, __VALIDATE_EMAIL__, __VALIDATE_EMAIL_DEBUG__, \
                                __TIME_TO_WAIT_AFTER_SENDING_AN_EMAIL_IN_SECONDS__
from settings.accounts import __TO_MAIL_ADDRESS__, __PASSWORD_MAIL_ADDRESS__, __SMTP_ADDRESS__, __SMTP_PORT__, \
                                __EMAIL_SIGNATURE__

from modules.common import generate_encoded_jwt_token, get_decoded_jwt_token, get_shapefile_file_name_inside_folder, \
                            catch_generic_exception, is_there_shapefile_files_inside_folder, remove_special_chars_from_string, \
                            rename_files_names_inside_folder, move_files_from_src_to_dist, does_the_string_have_special_chars


def send_email(to_email_address, subject="", body=""):

    def __thread_send_email__(__to_email_address__, __subject__, __body__):
        __from_mail_address__ = __TO_MAIL_ADDRESS__

        msg = MIMEMultipart()
        msg['From'] = __from_mail_address__
        msg['To'] = __to_email_address__
        msg['Subject'] = __subject__

        msg.attach(MIMEText(__body__, 'plain'))

        server = SMTP(__SMTP_ADDRESS__, __SMTP_PORT__)
        server.starttls()
        server.login(__from_mail_address__, __PASSWORD_MAIL_ADDRESS__)
        server.sendmail(__from_mail_address__, __to_email_address__, msg.as_string())
        server.quit()

        # print("\n\n -----> Sent email to: " + __to_email_address__ + "\n\n")

    thread = Thread(target=__thread_send_email__, args=(to_email_address, subject, body,))
    thread.start()

    # wait X second(s) after sending an e-mail in order to avoid blocking the SMTP server
    sleep(__TIME_TO_WAIT_AFTER_SENDING_AN_EMAIL_IN_SECONDS__)


def remove_special_chars_from_gdf_columns(gdf):
    new_column_names = {}

    # get the Shapefile file columns
    columns = gdf.columns.values.tolist()

    for old_column in columns:
        column = remove_special_chars_from_string(old_column)

        # save the new column name in a dict to rename inside the gdf afterwards
        new_column_names[old_column] = column

    # rename the columns names in place
    gdf.rename(columns=new_column_names, inplace=True)

    return gdf


def remove_invalid_columns_from_gdf_columns(gdf):
    # get the Shapefile file columns
    columns = gdf.columns.values.tolist()

    # If the Shapefile file has private column names, than remove them
    if "version" in columns:
        del gdf['version']

    if "changeset_" in columns:
        del gdf['changeset_']

    return gdf


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

    ##################################################
    # OVERRIDED METHODS
    ##################################################

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages.

        ``write_error`` may call `write`, `render`, `set_header`, etc
        to produce output as usual.

        If this error was caused by an uncaught exception (including
        HTTPError), an ``exc_info`` triple will be available as
        ``kwargs["exc_info"]``.  Note that this exception may not be
        the "current" exception for purposes of methods like
        ``sys.exc_info()`` or ``traceback.format_exc``.
        """

        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header("Content-Type", "text/plain")

            if len(kwargs["exc_info"]) >= 2:
                http_error = kwargs["exc_info"][1]

                track_message = ''.join(format_exception(*kwargs["exc_info"]))
                # error_message = format_exception(*kwargs["exc_info"])[-1]

                # the track message just will be logged then a 50X error occurs
                if status_code >= 500:
                    logging.error(track_message)

                self.write(http_error.log_message)
                self.finish()
            else:
                # original behavior
                for line in format_exception(*kwargs["exc_info"]):
                    self.write(line)
                self.finish()

        else:
            self.finish(
                "<html><title>%(code)d: %(message)s</title>"
                "<body>%(code)d: %(message)s</body></html>"
                % {"code": status_code, "message": self._reason}
            )

    ##################################################
    # HEADERS
    ##################################################

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

        # Check if the type of the content is JSON
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

    ##################################################
    # LOGIN
    ##################################################

    @catch_generic_exception
    def auth_login(self, email, password):
        user_in_db = self.PGSQLConn.get_users(email=email, password=password)

        if not user_in_db["features"]:  # if the list is empty
            raise HTTPError(404, "Not found any user.")

        if not user_in_db["features"][0]["properties"]["is_email_valid"]:
            raise HTTPError(409, "The email has not been validated.")

        encoded_jwt_token = generate_encoded_jwt_token(user_in_db["features"][0])

        return encoded_jwt_token

    @catch_generic_exception
    def change_password(self, email, current_password, new_password):
        # try to login with the email and password, it doesn't raise an exception, so it is OK
        try:
            self.auth_login(email, current_password)
        except HTTPError as error:
            if error.status_code == 404:
                raise HTTPError(409, "Current password is invalid.")

        # try to update the user's password by id
        current_user_id = self.get_current_user_id()
        self.PGSQLConn.update_user_password(current_user_id, new_password)

    @catch_generic_exception
    def login(self, user_json, verified_social_login_email=False):
        # looking for a user in db, if not exist user, so create a new one
        user_in_db = self.PGSQLConn.get_users(email=user_json["properties"]["email"])

        if not user_in_db["features"]:  # if the list is empty
            # ... because I expected a 404 to create a new user
            id_in_json = self.PGSQLConn.create_user(user_json, verified_social_login_email=verified_social_login_email)
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

    ##################################################
    # CURRENT USER
    ##################################################

    def get_current_user_(self):
        token = self.request.headers["Authorization"]
        user = get_decoded_jwt_token(token)
        return user

    def get_current_user_id(self):
        try:
            current_user = self.get_current_user_()
            return current_user["properties"]["user_id"]
        except KeyError:
            return None
            # raise HTTPError(500, "Problem when get the current user. Please, contact the administrator.")

    def is_current_user_an_administrator(self):
        """
        Check if the current user is an administrator
        :return: True or False
        """

        current_user = self.get_current_user_()

        return current_user["properties"]["is_the_admin"]

    ##################################################
    # MAIL
    ##################################################

    def send_validation_email_to(self, to_email_address, user_id):
        if self.DEBUG_MODE:
            url_to_validate_email = __VALIDATE_EMAIL_DEBUG__
        else:
            url_to_validate_email = __VALIDATE_EMAIL__

        email_token = generate_encoded_jwt_token({"user_id": user_id})

        url_to_validate_email += "/" + email_token   # convert bytes to str

        subject = "Email Validation - Not reply"
        body = """
Hello,

Please, not reply this message.

Please, click on under URL to validate your email:
{0}

{1}
        """.format(url_to_validate_email, __EMAIL_SIGNATURE__)

        send_email(to_email_address, subject=subject, body=body)

    def get_users_to_send_email(self, resource_json):
        users = {"features": []}

        # (1) general notification, everybody receives a notification by email
        if resource_json["properties"]["layer_id"] is None and resource_json["properties"]["keyword_id"] is None \
                and resource_json["properties"]["notification_id_parent"] is None:
            users = self.PGSQLConn.get_users()

        # (2) notification by layer
        elif resource_json["properties"]["layer_id"] is not None:
            # (2.1) everybody who is collaborator of the layer, will receive a not. by email

            # get all the collaborators of the layer
            # users_layer = self.PGSQLConn.get_user_layers(layer_id=resource_json["properties"]["layer_id"])
            #
            # # get the user information of the collaborators
            # for user_layer in users_layer["features"]:
            #     user = self.PGSQLConn.get_users(user_id=user_layer["properties"]["user_id"])["features"][0]
            #     users["features"].append(user)

            # (2.1) everybody who follows the layer, will receive a notification by email

            users_follow_layer = self.PGSQLConn.get_layer_follower(layer_id=resource_json["properties"]["layer_id"])

            # get the user information of the collaborators
            for user_follow_layer in users_follow_layer["features"]:
                user = self.PGSQLConn.get_users(user_id=user_follow_layer["properties"]["user_id"])["features"][0]
                users["features"].append(user)

        # TODO: (3) notification by keyword: everybody who follows the keyword, will receive a notification by email
        # elif resource_json["properties"]["keyword_id"] is not None:
        #     pass

        return users

    def send_email_to_selected_users(self, users_to_send_email, current_user_id, resource_json):
        user_that_is_sending_email = self.PGSQLConn.get_users(user_id=current_user_id)["features"][0]

        subject = "Notification - Not reply"
        body = """
Hello,

Please, not reply this message.

{0} has sent a new notification:

"{1}"

Enter on the Pauliceia platform to visualize or reply this notification.

{2}
        """.format(user_that_is_sending_email["properties"]["name"],
                   resource_json["properties"]["description"],
                   __EMAIL_SIGNATURE__)

        for user in users_to_send_email["features"]:
            if user["properties"]["receive_notification_by_email"] and user["properties"]["is_email_valid"]:
                send_email(user["properties"]["email"], subject=subject, body=body)

    def send_notification_by_email(self, resource_json, current_user_id):
        try:
            users_to_send_email = self.get_users_to_send_email(resource_json)
        except HTTPError as error:
            # if not found users, send to 0 users the notifications
            if error.status_code == 404:
                users_to_send_email = {"features": []}
            else:
                raise error

        self.send_email_to_selected_users(users_to_send_email, current_user_id, resource_json)

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

    def social_login(self, user, social_account):
        # print("\nuser: ", user, "\n")
        # for key in user:
        #     print(key, ": ", user[key])

        if isinstance(user["picture"], str):  # google photo
            picture = user["picture"]
        elif isinstance(user["picture"], dict):  # facebook photo
            # picture = user["picture"]["data"]["url"]  # this image is 50x50
            picture = "https://graph.facebook.com/{0}/picture?type=large&height=500".format(user['id'])
        else:
            picture = ''

        user_json = {
            'type': 'User',
            'properties': {'user_id': -1, 'email': user["email"], 'password': '', 'username': user["email"],
                           'name': user['name'], 'terms_agreed': True, 'receive_notification_by_email': False,
                           'picture': picture, 'social_id': user['id'], 'social_account': social_account}
        }

        if "verified_email" not in user:  # login with facebook doesn't have "verified_email", but google has, so put it
            user["verified_email"] = True

        encoded_jwt_token = self.login(user_json, verified_social_login_email=user["verified_email"])

        #self.write(json_encode({"token": encoded_jwt_token}))
        URL_TO_REDIRECT = self.__AFTER_LOGIN_REDIRECT_TO__ + "/" + encoded_jwt_token
        super(BaseHandler, self).redirect(URL_TO_REDIRECT)


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
        except KeyError as error:
            raise HTTPError(400, "Some attribute is missing. Look the documentation! (error: " +
                            str(error) + " is missing)")
        except TypeError as error:
            # example: - 400 (Bad Request): get_keywords() got an unexpected keyword argument 'parent_id'
            raise HTTPError(400, "TypeError: " + str(error))
        except Error as error:
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
        except KeyError as error:
            raise HTTPError(400, "Some attribute in the JSON is missing. Look at the documentation! (error: " +
                            str(error) + " is missing)")
        except TypeError as error:
            # example: - 400 (Bad Request): create_keywords() got an unexpected keyword argument 'parent_id'
            raise HTTPError(400, "TypeError: " + str(error))
        except ProgrammingError as error:
            if error.pgcode == "42703":  # 42703 - undefined_column
                raise HTTPError(400, "One specified attribute is invalid. (error: " + str(error) + ")")
            else:
                raise error  # if is other error, so raise it up
        except Error as error:
            if error.pgcode == "23505":  # 23505 - unique_violation
                error = str(error).replace("\n", " ").split("DETAIL: ")[1]
                raise HTTPError(400, "Attribute already exists. (error: " + str(error) + ")")
            elif error.pgcode == "22023":  # 22023 - invalid_parameter_value
                raise HTTPError(400, "One specified attribute is invalid. (error: " + str(error) + ")")
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
        resource_json = self.get_the_json_validated()
        current_user_id = self.get_current_user_id()

        try:
            self._close_resource(resource_json, current_user_id)
        except DataError as error:
            raise HTTPError(500, "Problem when close a resource. Please, contact the administrator. " +
                            "(error: " + str(error) + " - pgcode " + str(error.pgcode) + " ).")

    def _close_resource(self, resource_json, current_user_id):
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
        except KeyError as error:
            raise HTTPError(400, "Some attribute in the JSON is missing. Look at the documentation! (error: " +
                            str(error) + " is missing)")
        except TypeError as error:
            # example: - 400 (Bad Request): update_keywords() got an unexpected keyword argument 'parent_id'
            raise HTTPError(400, "TypeError: " + str(error))
        except Error as error:
            if error.pgcode == "23505":  # 23505 - unique_violation
                error = str(error).replace("\n", " ").split("DETAIL: ")[1]
                raise HTTPError(400, "Attribute already exists. (error: " + str(error) + ")")
            elif error.pgcode == "22023":  # 22023 - invalid_parameter_value
                raise HTTPError(400, "One specified attribute is invalid. (error: " + str(error) + ")")
            else:
                raise error  # if is other error, so raise it up
        except DataError as error:
            raise HTTPError(500, "Problem when update a resource. Please, contact the administrator. " +
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
        except TypeError as error:
            # example: - 400 (Bad Request): delete_keywords() got an unexpected keyword argument 'parent_id'
            raise HTTPError(400, "TypeError: " + str(error))
        except ProgrammingError as error:
            if error.pgcode == "42703":  # 42703 - undefined_column
                error = str(error).replace("\n", " ")
                raise HTTPError(404, "Not found the specified column. (error: " + str(error) + ")")
            else:
                raise error  # if is other error, so raise it up
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

        # TODO: temporarily all users will be registered with is_email_valid=True.
        #       after it returns to normal, undo the changes
        # if a new user is registered, then send him an email
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
        Check if a user is himself/herself or an administrator, who are can update another user.
        :return:
        """

        if current_user_id == resource_json["properties"]["user_id"]:
            return

        if self.is_current_user_an_administrator():
            return

        raise HTTPError(403, "Just the own user or an administrator can update a user.")

    def can_current_user_delete(self):
        """
        Check if a user is administrator to delete another user.
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
        Check if the current user is an administrator to create, update or delete a curator user
        :return:
        """

        # if current user is an administrator, so ok ...
        if self.is_current_user_an_administrator():
            return

        # ... else, raise an exception.
        raise HTTPError(403, "The administrator is who can create/update/delete a curator")


class LayerValidator(BaseHandler):

    def check_if_f_table_name_starts_with_number_or_it_has_special_chars(self, f_table_name):
        if does_the_string_have_special_chars(f_table_name):
            raise HTTPError(400, "f_table_name can not have special characters. (f_table_name: `" + f_table_name + "`)")

        if f_table_name[0].isdigit():
            raise HTTPError(400, "f_table_name can not start with number. (f_table_name: " + f_table_name + ")")

    def check_if_f_table_name_is_a_reserved_word(self, f_table_name):
        if f_table_name.lower() in self.PGSQLConn.get_reserved_words_of_postgresql():
            raise HTTPError(409, "Conflict of f_table_name. The table name is a reserved word. Please, rename it."
                            + "(table: " + f_table_name + ")")

    def check_if_f_table_name_already_exist_in_db(self, f_table_name):
        if f_table_name in self.PGSQLConn.get_table_names_that_already_exist_in_db():
            raise HTTPError(409, "Conflict of f_table_name. The table name already exist. Please, rename it. "
                            + "(table: " + f_table_name + ")")

    def check_f_table_name_length(self, f_table_name):
        if len(f_table_name) < 5:
            raise HTTPError(400, "The minimum length for the f_table_name attribute is 5 characters.")

        if len(f_table_name) > 63:
            raise HTTPError(400, "The maximum length for the f_table_name attribute is 63 characters.")

    def validate_f_table_name_attribute(self, f_table_name):
        self.check_if_f_table_name_starts_with_number_or_it_has_special_chars(f_table_name)
        self.check_if_f_table_name_is_a_reserved_word(f_table_name)
        self.check_if_f_table_name_already_exist_in_db(f_table_name)
        self.check_f_table_name_length(f_table_name)

    def check_if_layer_has_max_5_keywords(self, resource_json):
        amount_of_keywords = len(resource_json["properties"]["keyword"])

        if amount_of_keywords > 5:
            raise HTTPError(409, "The maximum of keywords allowed to a layer are 5.")


class BaseHandlerLayer(BaseHandlerTemplateMethod, LayerValidator):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_layers(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        f_table_name = resource_json["properties"]["f_table_name"]

        self.validate_f_table_name_attribute(f_table_name)

        self.check_if_layer_has_max_5_keywords(resource_json)

        return self.PGSQLConn.create_layer(resource_json, current_user_id, **kwargs)

    # PUT

    def _put_resource(self, resource_json, current_user_id, **kwargs):
        self.check_if_layer_has_max_5_keywords(resource_json)

        self.can_current_user_update(current_user_id, resource_json["properties"]["layer_id"])

        return self.PGSQLConn.update_layer(resource_json, current_user_id)

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        layer_id = args[0]
        self.can_current_user_delete(current_user_id, layer_id)

        self.PGSQLConn.delete_layer(*args)

    # VALIDATION

    def can_current_user_update(self, current_user_id, layer_id):
        """
        Check if the user has permission to update a layer
        :param current_user_id: current user id
        :param layer_id: layer id
        :return:
        """

        # if the `current_user_id` belongs to the admin user, then ok...
        if self.is_current_user_an_administrator():
            return

        layers = self.PGSQLConn.get_layers(layer_id=layer_id)

        if not layers["features"]:  # if list is empty:
            raise HTTPError(404, "Not found the layer {0}.".format(layer_id))

        user_layers = self.PGSQLConn.get_user_layers(layer_id=layer_id)

        for user_layer in user_layers["features"]:
            if user_layer["properties"]['user_id'] == current_user_id:
                # if the `current_user_id` belongs to the layer creator or collaborator user, then ok...
                return

        # ... else, raise an exception.
        raise HTTPError(403, "The layer owner or collaborator user, or administrator one are who can update a layer.")

    def can_current_user_delete(self, current_user_id, layer_id):
        """
        Check if the user has permission to delete a layer
        :param current_user_id: current user id
        :param layer_id: layer id
        :return:
        """

        # if the `current_user_id` belongs to the admin user, then ok...
        if self.is_current_user_an_administrator():
            return

        layers = self.PGSQLConn.get_layers(layer_id=layer_id)

        if not layers["features"]:  # if list is empty:
            raise HTTPError(404, "Not found the layer {0}.".format(layer_id))

        user_layers = self.PGSQLConn.get_user_layers(layer_id=layer_id)

        for user_layer in user_layers["features"]:
            if user_layer["properties"]['is_the_creator'] and user_layer["properties"]['user_id'] == current_user_id:
                # if the `current_user_id` belongs to the layer creator user, then ok...
                return

        # ... else, raise an exception.
        raise HTTPError(403, "The layer owner or administrator user are who can delete a layer.")


class FeatureTableValidator(BaseHandler):

    def can_current_user_update(self, current_user_id, f_table_name):
        layers = self.PGSQLConn.get_layers(f_table_name=f_table_name)

        if not layers["features"]:  # if list is empty
            raise HTTPError(404, "Not found any layer with the passed f_table_name. " +
                            "You need to create a layer with the f_table_name before of using this function.")

        layer_id = layers["features"][0]["properties"]["layer_id"]

        layer = self.PGSQLConn.get_user_layers(layer_id=str(layer_id))

        for feature in layer["features"]:
            if feature["properties"]['user_id'] == current_user_id:
                # if the current user is the creator user or a collaborator one, then ok...
                return

        # if current user is an administrator one, then ok ...
        if self.is_current_user_an_administrator():
            return

        # ... else, raise an exception.
        raise HTTPError(403, "The layer owner or collaborator user, or administrator one are who can update this resource.")

    def can_current_user_create_or_delete(self, current_user_id, f_table_name):
        layers = self.PGSQLConn.get_layers(f_table_name=f_table_name)

        if not layers["features"]:  # if list is empty
            raise HTTPError(404, "Not found any layer with the passed f_table_name. " +
                            "You need to create a layer with the f_table_name before using this function.")

        layer_id = layers["features"][0]["properties"]["layer_id"]

        layer = self.PGSQLConn.get_user_layers(layer_id=str(layer_id))

        for feature in layer["features"]:
            if feature["properties"]['is_the_creator'] and feature["properties"]['user_id'] == current_user_id:
                # if the current_user_id is the creator of this layer, then ok...
                return

        # if `current_user_id` is an administrator user, then ok ...
        if self.is_current_user_an_administrator():
            return

        # ... else, raise an exception.
        raise HTTPError(403, "The layer owner or administrator user are who can create or delete this resource.")


class BaseHandlerFeatureTable(BaseHandlerTemplateMethod, FeatureTableValidator, LayerValidator):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_feature_table(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        f_table_name = resource_json["f_table_name"]

        self.check_if_f_table_name_starts_with_number_or_it_has_special_chars(f_table_name)
        self.check_if_f_table_name_is_a_reserved_word(f_table_name)

        self.check_if_fields_of_f_table_are_invalids(resource_json)

        self.can_current_user_create_or_delete(current_user_id, f_table_name)

        return self.PGSQLConn.create_feature_table(resource_json, current_user_id, **kwargs)

    # PUT

    # BaseHandlerFeatureTableColumn class below is the `PUT` method for this class

    # DELETE

    # A feature table is deleted automatically when its layer is deleted

    # VALIDATION

    # The validator methods of this class are inherited by its super classes

    def check_if_fields_of_f_table_are_invalids(self, resource_json):
        list_invalid_words = ["id", "geom", "version", "changeset_id"]
        list_db_reserved_words = self.PGSQLConn.get_reserved_words_of_postgresql()

        # union both lists with invalid words
        list_reserved_words = list_invalid_words + list_db_reserved_words

        for field in resource_json["properties"]:
            if does_the_string_have_special_chars(field):
                raise HTTPError(400, "There is a field with have special characters. " +
                                     "Please, rename it. (field: " + str(field) + ")")

            if field[0].isdigit():
                raise HTTPError(400, "There is a field that starts with number. " +
                                "Please, rename it. (field: " + str(field) + ")")

            if " " in field:
                raise HTTPError(400, "There is a field with white spaces. " +
                                "Please, rename it. (field: " + str(field) + ")")

            # version is a reserved word that is allowed
            f = str(field).lower()
            if f in list_reserved_words:
                raise HTTPError(400, "There is a field that is a reserved word. " +
                                "Please, rename it. (field: " + str(field) + ")")


class BaseHandlerFeatureTableColumn(BaseHandlerTemplateMethod, FeatureTableValidator):
    '''This class is the `PUT` method for the BaseHandlerFeatureTable class.
    A feature table is updated when a column is added or deleted by this class.'''

    # GET

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        self.can_current_user_update(current_user_id, resource_json["f_table_name"])

        return self.PGSQLConn.create_feature_table_column(resource_json)

    # PUT

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        self.can_current_user_update(current_user_id, kwargs["f_table_name"])

        self.PGSQLConn.delete_feature_table_column(**kwargs)

    # VALIDATION

    # The validator methods of this class are inherited by its super class


class BaseHandlerTemporalColumns(BaseHandlerTemplateMethod, FeatureTableValidator, LayerValidator):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_temporal_columns(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        f_table_name = resource_json["properties"]["f_table_name"]

        self.check_if_f_table_name_starts_with_number_or_it_has_special_chars(f_table_name)
        self.check_if_f_table_name_is_a_reserved_word(f_table_name)

        self.can_current_user_create_or_delete(current_user_id, f_table_name)

        return self.PGSQLConn.create_temporal_columns(resource_json, current_user_id, **kwargs)

    # PUT

    def _put_resource(self, resource_json, current_user_id, **kwargs):
        self.can_current_user_update(current_user_id, resource_json["properties"]["f_table_name"])

        return self.PGSQLConn.update_temporal_columns(resource_json, current_user_id, **kwargs)

    # DELETE

    # A temporal columns table is deleted automatically when its layer is deleted

    # VALIDATION

    # The validator methods of this class are inherited by its super classes


class BaseHandlerUserLayer(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_user_layers(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        self.can_current_user_add_user_in_layer(current_user_id, resource_json["properties"]["layer_id"])

        # the layer's creator is just who was added by create_layer function, the others are not
        resource_json["properties"]["is_the_creator"] = False

        return self.PGSQLConn.create_user_layer(resource_json, current_user_id)

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
        Check if the user has permission of adding a user in a layer
        :param current_user_id: current user id
        :param layer_id: layer id
        :return:
        """

        # if the current user is admin, so ok...
        if self.is_current_user_an_administrator():
            return

        user_layers = self.PGSQLConn.get_user_layers(layer_id=str(layer_id))

        for user_layer in user_layers["features"]:
            if user_layer["properties"]['is_the_creator'] and user_layer["properties"]['user_id'] == current_user_id:
                # if the current_user_id is the creator of the layer, so ok...
                return

        # ... else, raise an exception.
        raise HTTPError(403, "The creator of the layer is the unique who can add user in layer.")

    def can_current_user_delete_user_in_layer(self, current_user_id, layer_id):
        """
        Check if the user has permission of deleting a user from a layer
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
        self.can_current_user_update_or_delete(current_user_id, resource_json["properties"]["reference_id"])

        return self.PGSQLConn.update_reference(resource_json, current_user_id, **kwargs)

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        reference_id = args[0]
        self.can_current_user_update_or_delete(current_user_id, reference_id)

        try:
            self.PGSQLConn.delete_layer_reference(reference_id=reference_id)
        except HTTPError:
            # `delete_layer_reference` method has raised an HTTPError exception,
            # because this reference id does not belong to an existing layer yet.
            # Hence, the statement above is ignored.
            pass

        self.PGSQLConn.delete_reference(resource_id=reference_id)

    # VALIDATION

    def can_current_user_update_or_delete(self, current_user_id, reference_id):
        """
        Check if the user has permission of deleting a reference
        :param current_user_id: current user id
        :param reference_id: reference id
        :return:
        """

        # if the current user is admin, so ok...
        if self.is_current_user_an_administrator():
            return

        references = self.PGSQLConn.get_references(reference_id=reference_id)

        if not references["features"]:  # if the list is empty
            raise HTTPError(404, "Not found the reference {0}.".format(reference_id))

        # if the current_user_id is the creator of the reference, then ok...
        if references["features"][0]["properties"]['user_id_creator'] == current_user_id:
            return

        try:
            # get the layer id of the layer that has the reference id
            layer_reference = self.PGSQLConn.get_layer_reference(reference_id=str(reference_id))
            layer_id = layer_reference["features"][0]["properties"]['layer_id']

            layer = self.PGSQLConn.get_user_layers(layer_id=str(layer_id))

            for feature in layer["features"]:
                if feature["properties"]['user_id'] == current_user_id:
                    # if the current user is the creator user or a collaborator one, then ok...
                    return
        except HTTPError:
            # `get_layer_reference` method has raised an HTTPError exception,
            # because this reference id does not belong to an existing layer yet.
            # Hence, the statements above are ignored.
            pass

        # ... else, raise an exception.
        raise HTTPError(403, "The layer owner or collaborator user, or administrator one are who can update or delete a reference.")


class BaseHandlerKeyword(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_keywords(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        return self.PGSQLConn.create_keyword(resource_json, current_user_id, **kwargs)

    # PUT

    def _put_resource(self, resource_json, current_user_id, **kwargs):
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
        Check if the user has permission of deleting a keyword
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
        changeset = self.PGSQLConn.create_changeset(resource_json, current_user_id)
        return changeset['changeset_id']

    def _close_resource(self, resource_json, current_user_id):
        self.PGSQLConn.close_changeset(resource_json, current_user_id)

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
        Check if the user has permission of deleting a resource
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
        resource_json_copy = deepcopy(resource_json)

        result = self.PGSQLConn.create_notification(resource_json, current_user_id, **kwargs)

        # self.send_notification_by_email(resource_json_copy, current_user_id)

        return result

    # PUT

    def _put_resource(self, resource_json, current_user_id, **kwargs):
        self.can_current_user_update_or_delete_notification(current_user_id, resource_json["properties"]["notification_id"])

        return self.PGSQLConn.update_notification(resource_json, current_user_id, **kwargs)

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        self.can_current_user_update_or_delete_notification(current_user_id, **kwargs)

        self.PGSQLConn.delete_notification(**kwargs)

    # VALIDATION

    def can_current_user_update_or_delete_notification(self, current_user_id, notification_id):
        """
        Check if the current user can update or delete a notification
        :return:
        """

        # if current user is an administrator, so ok ...
        if self.is_current_user_an_administrator():
            return

        notification = self.PGSQLConn.get_notification(notification_id=notification_id)

        # if the current_user_id is the creator of the notification, so ok...
        if notification["features"][0]["properties"]['user_id_creator'] == current_user_id:
            return

        # ... else, raise an exception.
        raise HTTPError(403, "The owner of notification or administrator are who can update/delete a notification.")


class BaseHandlerNotificationRelatedToUser(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_notification_related_to_user(kwargs["user_id"])

    # POST

    # def _create_resource(self, resource_json, current_user_id, **kwargs):
    #     resource_json_copy = deepcopy(resource_json)
    #
    #     result = self.PGSQLConn.create_notification(resource_json, current_user_id, **kwargs)
    #
    #     self.send_notification_by_email(resource_json_copy, current_user_id)
    #
    #     return result
    #
    # # PUT
    #
    # def _put_resource(self, resource_json, current_user_id, **kwargs):
    #     self.can_current_user_update_or_delete_notification(current_user_id, resource_json["properties"]["notification_id"])
    #
    #     return self.PGSQLConn.update_notification(resource_json, current_user_id, **kwargs)
    #
    # # DELETE
    #
    # def _delete_resource(self, current_user_id, *args, **kwargs):
    #     self.can_current_user_update_or_delete_notification(current_user_id, **kwargs)
    #
    #     self.PGSQLConn.delete_notification(**kwargs)
    #
    # # VALIDATION
    #
    # def can_current_user_update_or_delete_notification(self, current_user_id, notification_id):
    #     """
    #     Check if the current user can update or delete a notification
    #     :return:
    #     """
    #
    #     # if current user is an administrator, so ok ...
    #     if self.is_current_user_an_administrator():
    #         return
    #
    #     notification = self.PGSQLConn.get_notification(notification_id=notification_id)
    #
    #     # if the current_user_id is the creator of the notification, so ok...
    #     if notification["features"][0]["properties"]['user_id_creator'] == current_user_id:
    #         return
    #
    #     # ... else, raise an exception.
    #     raise HTTPError(403, "The owner of notification or administrator are who can update/delete a notification.")


class BaseHandlerMask(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_mask(**kwargs)

    # POST

    # def _create_resource(self, resource_json, current_user_id, **kwargs):
    #     return self.PGSQLConn.create_reference(resource_json, current_user_id, **kwargs)

    # PUT

    # def _put_resource(self, resource_json, current_user_id, **kwargs):
    #     if "reference_id" not in resource_json["properties"]:
    #         raise HTTPError(400, "Some attribute in the JSON is missing. Look at the documentation! (Hint: reference_id)")
    #
    #     reference_id = resource_json["properties"]["reference_id"]
    #     self.can_current_user_update_or_delete(current_user_id, reference_id)
    #
    #     return self.PGSQLConn.update_reference(resource_json, current_user_id, **kwargs)

    # DELETE

    # def _delete_resource(self, current_user_id, *args, **kwargs):
    #     reference_id = args[0]
    #     self.can_current_user_update_or_delete(current_user_id, reference_id)
    #
    #     self.PGSQLConn.delete_reference(*args)

    # VALIDATION


class BaseHandlerFeature(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        f_table_name = kwargs["f_table_name"]
        del kwargs["f_table_name"]  # remove the f_table_name from dict

        return self.PGSQLConn.get_feature(f_table_name, **kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        self.can_user_uses_the_changeset(current_user_id, resource_json["properties"]["changeset_id"])
        self.can_current_user_manage(current_user_id, resource_json["f_table_name"])

        return self.PGSQLConn.create_feature(resource_json, current_user_id)

    # PUT

    def _put_resource(self, resource_json, current_user_id, **kwargs):
        self.can_user_uses_the_changeset(current_user_id, resource_json["properties"]["changeset_id"])
        self.can_current_user_manage(current_user_id, resource_json["f_table_name"])

        return self.PGSQLConn.update_feature(resource_json, current_user_id)

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        self.can_user_uses_the_changeset(current_user_id, kwargs["changeset_id"])
        self.can_current_user_manage(current_user_id, kwargs["f_table_name"])

        self.PGSQLConn.delete_feature(kwargs["f_table_name"], kwargs["feature_id"], kwargs["changeset_id"], current_user_id)

    # VALIDATION

    def can_user_uses_the_changeset(self, current_user_id, changeset_id):
        changeset = self.PGSQLConn.get_changesets(changeset_id)

        if not changeset["features"]:  # if the list is empty
            raise HTTPError(404, "Not found the changeset `{0}`.".format(changeset_id))

        changeset = changeset["features"][0]["properties"]

        if changeset["user_id_creator"] != current_user_id:
            raise HTTPError(403, "The changeset_id {0} was not created by current user.".format(changeset_id))

        closed_at = changeset["closed_at"]
        if closed_at is not None:
            raise HTTPError(409, "The changeset_id {0} was already closed at {1}.".format(changeset_id, str(closed_at)))

    def can_current_user_manage(self, current_user_id, f_table_name):
        # if current user is an administrator one, then ok...
        if self.is_current_user_an_administrator():
            return

        layers = self.PGSQLConn.get_layers(f_table_name=f_table_name)

        if not layers["features"]:  # if list is empty
            raise HTTPError(404, "Not found layer " + f_table_name +
                            ". You need to create a layer with the f_table_name before of using this function.")

        layer_id = layers["features"][0]["properties"]["layer_id"]

        layers = self.PGSQLConn.get_user_layers(layer_id=str(layer_id))

        for layer in layers["features"]:
            if layer["properties"]['user_id'] == current_user_id:
                # if the current user is a collaborator one of this layer, then ok...
                return

        # ... else, raise an exception.
        raise HTTPError(403, "Just the collaborator of the layer or administrator can manage a resource.")


class BaseHandlerLayerFollower(BaseHandlerTemplateMethod):

    # GET

    def _get_resource(self, *args, **kwargs):
        return self.PGSQLConn.get_layer_follower(**kwargs)

    # POST

    def _create_resource(self, resource_json, current_user_id, **kwargs):
        layer_id = resource_json["properties"]["layer_id"]
        self.can_current_user_create(current_user_id, layer_id)
        return self.PGSQLConn.create_layer_follower(resource_json, current_user_id, **kwargs)

    # PUT

    # def _put_resource(self, resource_json, current_user_id, **kwargs):
    #     self.can_current_user_update_or_delete(current_user_id, resource_json["properties"]["reference_id"])
    #
    #     return self.PGSQLConn.update_reference(resource_json, current_user_id, **kwargs)

    # DELETE

    def _delete_resource(self, current_user_id, *args, **kwargs):
        self.PGSQLConn.delete_layer_follower(kwargs["layer_id"], kwargs["user_id"])

    # VALIDATION

    def can_current_user_create(self, current_user_id, layer_id):
        # layers = {"features": []}
        layer_followers = {"features": []}

        # try:
        #     layers = self.PGSQLConn.get_user_layers(user_id=str(current_user_id), layer_id=str(layer_id))
        # except HTTPError as error:
        #     # if the error is different of 404, raise an exception..., because I expect a 404
        #     # (when a user is not a collaborator of a layer he can follow the layer)
        #     if error.status_code != 404:
        #         raise error
        #
        # # if it was returned a list with users, raise an exception
        # if layers["features"]:
        #     raise HTTPError(409, "The user can't follow a layer, because he/she is a collaborator or owner of it.")

        try:
            layer_followers = self.PGSQLConn.get_layer_follower(user_id=str(current_user_id), layer_id=str(layer_id))
        except HTTPError as error:
            # if the error is different of 404, raise an exception..., because I expect a 404
            # (when a user is not a collaborator of a layer he can follow the layer)
            if error.status_code != 404:
                raise error

        # if it was returned a list with users, raise an exception
        if layer_followers["features"]:
            raise HTTPError(409, "The user can't follow a layer, because he/she already follow it.")


# IMPORT

class BaseHandlerImportShapeFile(BaseHandlerTemplateMethod, FeatureTableValidator, LayerValidator):

    PATH_ZIP_FILE = ''
    PATH_EXTRACTED_ZIP_FILE = ''

    # VALIDATION

    # The validator methods of this class are inherited by its super classes

    # POST - IMPORT

    def remove_temporary_file_and_folder(self):
        # remove the temporary file and folder of the shapefile
        remove_file(self.PATH_ZIP_FILE)
        remove_folder_with_contents(self.PATH_EXTRACTED_ZIP_FILE)

    def do_validation(self, arguments, binary_file):
        if ("f_table_name" not in arguments) or ("file_name" not in arguments) or ("changeset_id" not in arguments):
            raise HTTPError(400, "`f_table_name`, `file_name` and `changeset_id` are required parameters in request.")

        f_table_name = arguments["f_table_name"]

        self.check_if_f_table_name_starts_with_number_or_it_has_special_chars(f_table_name)
        self.check_if_f_table_name_is_a_reserved_word(f_table_name)

        if binary_file == b'':
            raise HTTPError(400, "A binary zip file is required in the body of the request.")

        # if do not exist the temp folder, create it
        if not exists(__TEMP_FOLDER__):
            makedirs(__TEMP_FOLDER__)

        # the file needs to be in a zip file
        if not arguments["file_name"].endswith(".zip"):
            raise HTTPError(400, "Invalid file name: " + str(arguments["file_name"]) + ". It is necessary to be a zip.")

    def save_binary_file_in_folder(self, binary_file):
        """
        :param binary_file: a binary file
        :return:
        """
        # save the zip file with the Shapefile files inside the temporary folder
        output_file = open(self.PATH_ZIP_FILE, 'wb')  # wb - write binary
        output_file.write(binary_file)
        output_file.close()

    def extract_zip_in_folder(self):
        try:
            with ZipFile(self.PATH_ZIP_FILE, "r") as zip_reference:
                # extract the zip in a folder
                zip_reference.extractall(self.PATH_EXTRACTED_ZIP_FILE)

                # check if there are the shapefile files inside the folder where the zip was extracted,
                # if ok, then it returns a 200 status code, else it returns a 404 status code and an error message
                status, message = is_there_shapefile_files_inside_folder(self.PATH_EXTRACTED_ZIP_FILE)

                # if there is not shapefile files inside the folder for the first time,
                # then I try to check if there is the files inside `myshapes` folder
                if status != 200:
                    path_myshapes = join(self.PATH_EXTRACTED_ZIP_FILE, 'myshapes')

                    # check if there is `myshapes` folder inside the root folder
                    if isdir(path_myshapes):
                        # if there is `myshapes` folder, then I move all files inside it to the previous folder
                        move_files_from_src_to_dist(path_myshapes, self.PATH_EXTRACTED_ZIP_FILE)

                # check again if the shapefile files are inside the correct folder
                # if they are not, in other words, `status != 200`, then raise an exception
                status, message = is_there_shapefile_files_inside_folder(self.PATH_EXTRACTED_ZIP_FILE)

                # if there is not shapefile files inside the folder, then remove the files and raise an exception
                if status != 200:
                    self.remove_temporary_file_and_folder()
                    raise HTTPError(status, message)

        except BadZipFile as error:
            raise HTTPError(409, "File is not a zip file. (" + str(error) + ")")

    def check_if_the_shapefile_files_are_empty(self):
        # get only the files inside the directory
        files = [f for f in listdir(self.PATH_EXTRACTED_ZIP_FILE) if isfile(join(self.PATH_EXTRACTED_ZIP_FILE, f))]

        for file in files:
            if 'prj' in file:
                file_path = join(self.PATH_EXTRACTED_ZIP_FILE, file)

                if get_file_size(file_path) <= 0:
                    self.remove_temporary_file_and_folder()
                    raise HTTPError(400, '.prj file is empty!')

                break

    def import_shp_file_into_postgis(self, f_table_name, shapefile_path, EPSG):
        # Splitting `shapefile_path` in order to extract the `directory` and `file_name`
        splitted = shapefile_path.split(os_separator)

        directory = os_separator.join(splitted[:-1])  # get the first element until the last one and join them, in other words, the directory
        file_name = splitted[-1]  # get the last element, in other words, the file name

        __DB_CONNECTION__ = self.PGSQLConn.get_db_connection()

        postgresql_connection = '"host=' + __DB_CONNECTION__["HOSTNAME"] + ' port=' + str(__DB_CONNECTION__["PORT"]) + \
                                ' dbname=' + __DB_CONNECTION__["DATABASE"] + \
                                ' user=' + __DB_CONNECTION__["USERNAME"] + ' password=' + __DB_CONNECTION__["PASSWORD"] + '"'
        try:
            # FEATURE TABLE
            command_to_import_shp_into_postgis = 'ogr2ogr -append -f "PostgreSQL" PG:' + postgresql_connection + ' ' + \
                                                 file_name + ' -nln ' + f_table_name + ' -a_srs EPSG:' + str(EPSG) + \
                                                 ' -skipfailures -lco FID=id -lco GEOMETRY_NAME=geom -nlt PROMOTE_TO_MULTI'

            # command_to_import_shp_into_postgis = 'PGCLIENTENCODING=LATIN1 ogr2ogr -append -f "PostgreSQL" PG:' + postgresql_connection + ' ' + \
            #                                      file_name + ' -nln ' + f_table_name + ' -skipfailures -lco FID=id -lco GEOMETRY_NAME=geom -nlt PROMOTE_TO_MULTI'

            # print("command_to_import_shp_into_postgis: ", command_to_import_shp_into_postgis)

            # call a process to execute the command to import the SHP into the PostGIS
            check_call(command_to_import_shp_into_postgis, cwd=directory, shell=True)

        except CalledProcessError as error:
            raise HTTPError(500, "Problem when importing the Shapefile file. OGR was not able to import it. \n" + str(error))

        # self.check_if_there_is_some_invalid_attribute_in_feature_table(f_table_name)

    def check_if_the_gdf_is_inside_the_default_city(self, gdf, EPSG):
        # get the Shapefile file bounding box
        bbox = gdf.total_bounds.tolist()

        try:
            is_shapefile_intersects_default_city = self.PGSQLConn.bounding_box_of_shapefile_intersects_with_bounding_box_of_default_city(bbox, EPSG)
        except InternalError as error:
            raise HTTPError(500, "Some geometries of the Shapefile are with problem. Please, check them and try to " + \
                                 "import again later. \nError: " + str(error))

        if not is_shapefile_intersects_default_city:
            raise HTTPError(409, "Shapefile is not inside the default city of the project.")

    def import_shp(self):
        try:
            # get the arguments of the request
            arguments = self.get_aguments()

            # get the binary file in body of the request
            binary_file = self.request.body

            # validate the arguments and binary_file
            self.do_validation(arguments, binary_file)

            f_table_name = arguments["f_table_name"]

            # check if the user has permission to import the shapefile (same permissions than the feature table)
            self.can_current_user_create_or_delete(self.get_current_user_id(), f_table_name)

            # absolute path where I'm going to save my zip file (e.g. /tmp/vgiws/points.zip)
            self.PATH_ZIP_FILE = join(__TEMP_FOLDER__, arguments["file_name"])

            self.save_binary_file_in_folder(binary_file)

            # remove the extension of the file name (e.g. points)
            FILE_NAME_WITHOUT_EXTENSION = arguments["file_name"].replace(".zip", "")

            # absolute path where I'm going to extract the zip file (e.g. /tmp/vgiws/points)
            self.PATH_EXTRACTED_ZIP_FILE = join(__TEMP_FOLDER__, FILE_NAME_WITHOUT_EXTENSION)

            # extract the zip in a folder
            self.extract_zip_in_folder()

            self.check_if_the_shapefile_files_are_empty()

            # rename the files names inside the folder where the zip was extracted, in order to fix them
            rename_files_names_inside_folder(self.PATH_EXTRACTED_ZIP_FILE)

            # get the shapefile file_name (e.g. points.shp) and the full path (e.g. tmp/vgiws/points.shp)
            SHP_FILE_NAME, SHAPEFILE_PATH = get_shapefile_file_name_inside_folder(self.PATH_EXTRACTED_ZIP_FILE)

            try:
                # gdf - read the Shapefile file as a GeoDataFrame
                gdf = gp_read_file(SHAPEFILE_PATH)

                gdf = remove_special_chars_from_gdf_columns(gdf)
                gdf = remove_invalid_columns_from_gdf_columns(gdf)

                gdf.to_file(SHAPEFILE_PATH)  # save the editions

                EPSG = gdf.crs.to_epsg()

                # if EPSG is None, then I raise an exception
                if EPSG is None:
                    raise HTTPError(400, "Invalid .prj file. The EPSG could not be found from the .prj file.")

                # check if shapefile is inside default city
                self.check_if_the_gdf_is_inside_the_default_city(gdf, EPSG)

            except ValueError as error:
                raise HTTPError(500, "Problem when importing the Shapefile file. Fiona was not able to read it. \n" + \
                                "One reason can be that the Shapefile file has an empty column name, then name it inside the `.dbf` file. \n" +
                                "Hint: " + str(error))

            self.import_shp_file_into_postgis(f_table_name, SHAPEFILE_PATH, EPSG)

            VERSION_TABLE_NAME = "version_{}".format(f_table_name)

            self.PGSQLConn.create_new_table_with_the_schema_of_old_table(VERSION_TABLE_NAME, f_table_name)

            # arranging the feature table
            self.PGSQLConn.add_version_column_in_table(f_table_name)
            self.PGSQLConn.add_changeset_id_column_in_table(f_table_name)
            self.PGSQLConn.update_feature_table_setting_in_all_records_a_changeset_id(f_table_name, arguments["changeset_id"])
            self.PGSQLConn.update_feature_table_setting_in_all_records_a_version(f_table_name, 1)

            # arranging the version feature table
            self.PGSQLConn.add_version_column_in_table(VERSION_TABLE_NAME)
            self.PGSQLConn.add_changeset_id_column_in_table(VERSION_TABLE_NAME)

            # publish the feature table/layer in geoserver
            self.PGSQLConn.publish_feature_table_in_geoserver(f_table_name, EPSG)
            # self.PGSQLConn.publish_feature_table_in_geoserver("version_" + f_table_name)

            self.remove_temporary_file_and_folder()
        except ProgrammingError as error:
            raise HTTPError(500, "Problem when to import the Shapefile: " + str(error))


# CONVERT

class BaseHandlerConvertGeoJSONToShapefile(BaseHandler):

    __TEMP_FOLDER_TO_CONVERT__ = join(__TEMP_FOLDER__, "geojson_to_shapefile/")

    def do_validation(self, arguments, binary_file):
        if "file_name" not in arguments:
            raise HTTPError(400, "It is necessary to pass the file_name in the request.")

        if "/" in arguments["file_name"] or "\\" in arguments["file_name"]:
            raise HTTPError(400, "It is an invalid file name. (file_name: " + arguments["file_name"] + ")")

        if binary_file == b'' or binary_file == "":
            raise HTTPError(400, "It is necessary to pass one binary file in the body of the request.")

        # if do not exist the temp folders, create them
        if not exists(__TEMP_FOLDER__):
            makedirs(__TEMP_FOLDER__)

        if not exists(self.__TEMP_FOLDER_TO_CONVERT__):
            makedirs(self.__TEMP_FOLDER_TO_CONVERT__)

        # the file needs to be in a zip file
        if not arguments["file_name"].endswith(".geojson"):
            raise HTTPError(400, "Invalid file name: " + str(arguments["file_name"]) + ". It is necessary to be a GeoJSON.")

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

    def convert_geojson_to_shapefile_with_ogr2ogr(self, geojson_name, folder_to_create_shapefile):

        shapefile_name = geojson_name.replace("geojson", "shp")

        try:
            command_to_import_shp_into_postgis = 'ogr2ogr -f "ESRI Shapefile" ' + shapefile_name + ' "' + geojson_name + '"'

            # call a process to execute the command to import the SHP into the PostGIS
            check_call(command_to_import_shp_into_postgis, cwd=folder_to_create_shapefile, shell=True)

        except CalledProcessError as error:
            raise HTTPError(500, "Problem when to convert the GeoJSON to Shapefile. OGR was not able to convert.")

    def create_zip_with_shapefile(self, zip_file_name, folder_to_zip):
        make_archive(zip_file_name, 'zip', folder_to_zip)

    def convert_geojson_to_shapefile(self):
        # get the arguments of the request
        arguments = self.get_aguments()
        # get the binary file in body of the request
        binary_file = self.request.body

        # validate the arguments and binary_file
        self.do_validation(arguments, binary_file)

        # file name of the zip (e.g. /tmp/vgiws/geojson_to_shapefile/geojson_01.geojson)
        FILE_NAME_WITH_FOLDER = self.__TEMP_FOLDER_TO_CONVERT__ + arguments["file_name"]

        self.save_binary_file_in_folder(binary_file, FILE_NAME_WITH_FOLDER)

        self.convert_geojson_to_shapefile_with_ogr2ogr(arguments["file_name"], self.__TEMP_FOLDER_TO_CONVERT__)

        # delete the file (it is not needed anymore and because it doesn't have to appear inside the zip)
        remove_file(FILE_NAME_WITH_FOLDER)

        ZIP_FILE_NAME_WITH_FOLDER = join(__TEMP_FOLDER__, arguments["file_name"].replace(".geojson", ""))

        self.create_zip_with_shapefile(ZIP_FILE_NAME_WITH_FOLDER, self.__TEMP_FOLDER_TO_CONVERT__)

        # remove the temp folder
        remove_folder_with_contents(self.__TEMP_FOLDER_TO_CONVERT__)

        ZIP_FILE_NAME_WITH_FOLDER = ZIP_FILE_NAME_WITH_FOLDER + ".zip"

        # read the zip in binary to send to front
        with open(ZIP_FILE_NAME_WITH_FOLDER, mode='rb') as file:  # r = read binary
            binary_file_content = file.read()
            self.write(binary_file_content)  # send the zip to the front

        # delete the zip after using it
        remove_file(ZIP_FILE_NAME_WITH_FOLDER)

