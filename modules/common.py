#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir, rename
from os.path import isfile, join
from datetime import datetime
from base64 import b64encode
from jwt import encode as jwt_encode, decode as jwt_decode, DecodeError, InvalidAlgorithmError
from string import ascii_uppercase, digits
from random import choice
from re import compile as re_compile, sub as re_sub
from unidecode import unidecode

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
            raise HTTPError(500, "Psycopg2 error (psycopg2.ProgrammingError). Please, contact the administrator. " +
                                 "\nError: " + str(error) + "\npgcode: " + str(error.pgcode))

        except Error as error:
            raise HTTPError(500, "Psycopg2 error (psycopg2.Error). Please, contact the administrator. " +
                                 "\nError: " + str(error) + "\npgcode: " + str(error.pgcode))

    return wrapper


def auth_non_browser_based(method):
    """
    Authentication to non browser based service
    :param method: the decorated method
    :return: the wrapped method
    """

    def wrapper(self, *args, **kwargs):

        if "Authorization" in self.request.headers:
            try:
                token = self.request.headers["Authorization"]
                decoded_token = get_decoded_jwt_token(token)

                # try to search by the logged user in order to check if he exists
                users = self.PGSQLConn.get_users(
                    user_id=decoded_token['properties']['user_id'],
                    username=decoded_token['properties']['username'],
                    name=decoded_token['properties']['name'],
                    email=decoded_token['properties']['email']
                )

                if not users["features"]:  # if list is empty:
                    raise HTTPError(404, "Not found the user `{0}`.".format(decoded_token['properties']['user_id']))
            except HTTPError as error:
                raise error
            except Exception as error:
                raise HTTPError(500, "Problem when authorize a resource. Please, contact the administrator. " +
                                     "(" + str(error) + ")")

            return method(self, *args, **kwargs)
        else:
            raise HTTPError(401, "A valid `Authorization` header is necessary!")

    return wrapper


def auth_just_admin_can_use(method):
    """
    Authentication to non browser based service
    :param method: the decorated method
    :return: the wrapped method
    """

    def wrapper(self, *args, **kwargs):

        if not self.is_current_user_an_administrator():
            raise HTTPError(403, "The administrator is who can use this resource.")

        return method(self, *args, **kwargs)

    return wrapper


def just_run_on_debug_mode(method):
    """
    Just run the method on Debug Mode
    :param method: the decorated method
    :return: the wrapped method
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
    return jwt_encode(json_dict, __JWT_SECRET__, algorithm=__JWT_ALGORITHM__).decode("utf-8")


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


def get_shapefile_file_name_inside_folder(directory):
    files = get_just_files_inside_directory(directory)

    for file_name in files:
        if file_name.endswith(".shp"):
            # return the file_name (e.g. points.shp) and the full path (e.g. tmp/vgiws/points.shp)
            return file_name, join(directory, file_name)

    raise HTTPError(404, "3) Invalid zip file! Not found a ShapeFile file (i.e. .shp) inside the zip file.")  # 400 - Bad request


def rename_file_name(file_name):
    # PS: `unidecode` removes the accent from letters
    return unidecode(file_name.replace(' ', '_').lower())


def rename_files_names_inside_folder(directory):
    files = get_just_files_inside_directory(directory)

    for old_file_name in files:
        new_file_name = rename_file_name(old_file_name)

        # get the full path to one file name (e.g. /tmp/vgiws/point/point.shx)
        full_path_for_old_file_name = join(directory, old_file_name)
        full_path_for_new_file_name = join(directory, new_file_name)

        # rename the old file name to the new file name
        rename(full_path_for_old_file_name, full_path_for_new_file_name)


def move_files_from_src_to_dist(src, dist):
    files = get_just_files_inside_directory(src)

    for _file in files:
        # where the file is in this moment (e.g. /tmp/vgiws/point/myshapes/point.shx)
        _from = join(src, _file)
        # where I would like the file goes (e.g. /tmp/vgiws/point/point.shx)
        _to = join(dist, _file)

        # move ("rename") the file from `_from` to `_to`
        rename(_from, _to)


def is_there_shapefile_files_inside_folder(path_to_extract_zip_file):
    status = 200  # it is expected that it will work OK
    file_extension = ""

    files_and_folders = listdir(path_to_extract_zip_file)

    if not any("shp" in file_or_folder for file_or_folder in files_and_folders):
        status = 404
        file_extension = ".shp"

    if not any("prj" in file_or_folder for file_or_folder in files_and_folders):
        status = 404
        file_extension = ".prj"

    if not any("dbf" in file_or_folder for file_or_folder in files_and_folders):
        status = 404
        file_extension = ".dbf"

    if not any("shx" in file_or_folder for file_or_folder in files_and_folders):
        status = 404
        file_extension = ".shx"

    if status == 200:
        return status, ""

    return status, "Invalid zip file! Not found a ShapeFile file (i.e. {0}) inside the zip file.".format(file_extension)


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


def get_just_files_inside_directory(directory):
    # this method just returns the files inside the directory and not the folders, if there is any
    return [f for f in listdir(directory) if isfile(join(directory, f))]


def remove_special_chars_from_string(string):
    # replace accent letter to ascii representation
    string = unidecode(string.strip().replace(' ', '_').lower())

    # remove special chars from string, minus the underscore
    return re_sub('[^A-Za-z0-9_]+', '', string)


def does_the_string_have_special_chars(string):
    """
    To be a valid string, it must:
    - start with a character without number (i.e. '^[a-zA-Z_]')
    - end with a character that can have numbers (i.e. '[a-zA-Z0-9_]+$')
    - have one or more occurrences of that letter (i.e. '+')
    - not have special characters (i.e. '^[a-zA-Z_]+[a-zA-Z0-9_]+$')

    Return: `True` if the string has some special character, else it returns `False`
    """

    # create an english checker
    # this checker returns True if the string does NOT have a special character,
    # because of that, I return a `not bool(...)`, because I want it returns
    # `True` if the string has a special character
    english_checker = re_compile(r'^[a-zA-Z_]+[a-zA-Z0-9_]+$')

    return not bool(english_checker.match(string))
