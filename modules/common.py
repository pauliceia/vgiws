#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from base64 import b64encode
from jwt import encode as jwt_encode, decode as jwt_decode, DecodeError, InvalidAlgorithmError
from string import ascii_uppercase, digits
from random import choice

from psycopg2 import Error, ProgrammingError
from tornado.web import HTTPError

from settings.accounts import __JWT_SECRET__, __JWT_ALGORITHM__


# DECORATORS

def catch_generic_exception(method):

    def wrapper(self, *args, **kwargs):

        try:
            # try to execute the method
            return method(self, *args, **kwargs)

        # all methods can raise a psycopg exception, so catch it
        except ProgrammingError as error:
            self.PGSQLConn.rollback()  # do a rollback to comeback in a safe state of DB
            raise HTTPError(500, "Psycopg2 error (psycopg2.ProgrammingError). Please, contact the administrator. " +
                                 "\nInformation: " + str(error) + "\npgcode: " + str(error.pgcode))

        except Error as error:
            self.PGSQLConn.rollback()  # do a rollback to comeback in a safe state of DB
            raise HTTPError(500, "Psycopg2 error (psycopg2.Error). Please, contact the administrator. " +
                                 "\n Information: " + str(error) + "\npgcode: " + str(error.pgcode))

    return wrapper


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
                get_decoded_jwt_token(token)
            except HTTPError as error:
                raise error
            except Exception as error:
                raise HTTPError(500, "Problem when authorize a resource. Please, contact the administrator. " +
                                     "(" + str(error) + ")")

            return method(self, *args, **kwargs)
        else:
            raise HTTPError(401, "It is necessary an Authorization header valid.")

    return wrapper


def auth_just_admin_can_use(method):
    """
    Authentication to non browser based service
    :param method: the method decorated
    :return: the method wrapped
    """

    def wrapper(self, *args, **kwargs):

        if not self.is_current_user_an_administrator():
            raise HTTPError(403, "The administrator is who can use this resource.")

        return method(self, *args, **kwargs)

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


# JWT

def generate_encoded_jwt_token(json_dict):
    return jwt_encode(json_dict, __JWT_SECRET__, algorithm=__JWT_ALGORITHM__)


def get_decoded_jwt_token(token):
    try:
        return jwt_decode(token, __JWT_SECRET__, algorithms=[__JWT_ALGORITHM__])
    except DecodeError as error:
        raise HTTPError(400, "Invalid Token. (error: " + str(error) + ")")  # 400 - Bad request
    except InvalidAlgorithmError as error:
        raise HTTPError(400, "Invalid Token. (error: " + str(error) + ")")  # 400 - Bad request


# SHAPEFILE

def exist_shapefile_inside_zip(zip_reference):
    list_file_names_of_zip = zip_reference.namelist()

    for file_name_in_zip in list_file_names_of_zip:
        # if exist a SHP file inside the zip, return true
        if file_name_in_zip.endswith(".shp"):
            return True

    return False


# OTHERS

def get_current_datetime(formatted=True):
    now = datetime.now()

    if formatted:
        now = now.strftime("%Y-%m-%d %H:%M")

    return now


def get_username_and_password_as_string_in_base64(username, password):
    username_and_password = username + ":" + password

    string_in_base64 = (b64encode(username_and_password.encode('utf-8'))).decode('utf-8')

    return string_in_base64


def generate_random_string(size=6, chars=ascii_uppercase + digits):
    """
    #Source: https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    """
    return ''.join(choice(chars) for _ in range(size))

