#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base64 import b64encode
from copy import deepcopy
from hashlib import sha512
from json import loads, dumps
import requests
from requests import Session
from unittest import TestCase

from .common import by_multi_element_get_url_name, get_url_arguments
from modules.common import generate_encoded_jwt_token


def get_email_and_password_as_string_in_base64(email, password):
    email_and_password = email + ":" + password

    string_in_base64 = (b64encode(email_and_password.encode('utf-8'))).decode('utf-8')

    return string_in_base64


def get_string_in_hash_sha512(string):
    return sha512(string.encode()).hexdigest()


def get_string_in_base64(string):
    return (b64encode(string.encode('utf-8'))).decode('utf-8')


class RequestTester(TestCase):

    def __init__(self, *args, **kwargs):
        # This is necessary to extend from TestCase and override `__init__` method correctly
        TestCase.__init__(self, *args, **kwargs)

        # Create a session, in order to simulate a browser.
        # This is necessary to create cookies on the server
        # self.app = Session()

        self.app = requests

        # Default values. They can be override by the setters methods
        self.__url__ = "http://localhost:8888"
        self.__urn__ = "/api/user"

        self.__urn__login__ = '/api/auth/login/'

        self.__headers__ = {
            'Content-type': 'application/json',
            'Accept': 'application/json; charset=UTF-8'
        }

    ######################################################################
    # GETTERS AND SETTERS
    ######################################################################

    def get_url(self):
        return self.__url__

    def set_url(self, url):
        self.__url__ = url

    def get_urn(self):
        return self.__urn__

    def set_urn(self, urn):
        self.__urn__ = urn

    def get_uri(self):
        return self.__url__ + self.__urn__

    def get_uri_login(self):
        return self.__url__ + self.__urn__login__

    def set_urn_login(self, urn_login):
        self.__urn__login__ = urn_login

    ######################################################################
    # UTILS
    ######################################################################

    def get_headers(self, headers=None):
        # if 'headers' is empty, then add the cached 'self.__headers__'
        if headers is None:
	        headers = self.__headers__
        # else it returns the passed 'headers'
        return headers

    def error_asserts(self, response, status_code, error_message):
        # method to encapsulate the error asserts

        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data, error_message)

    ######################################################################
    # LOGIN
    ######################################################################

    def auth_login(self, email="gabriel@admin.com", password="gabriel", status_code=200, text_message=""):
        # method to sign the user on the app

        password = get_string_in_hash_sha512(password)

        headers = {
            # 'Access-Control-Allow-Origin': '*',
            # 'Content-Type': 'application/json',
            'Authorization': 'Basic ' + get_string_in_base64(email + ":" + password)
        }

        response = self.app.get(self.get_uri_login(), headers=headers)

        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.text, text_message)

        # just save the token if the login was successfull (i.e. status_code == 200)
        if status_code == 200:
            # save the JWT token of the server in Authorization header
            self.__headers__["Authorization"] = response.headers["Authorization"]

            # self.__headers__ = {
            #     'Access-Control-Allow-Origin': '*',
            #     'Content-Type': 'application/json',
            #     'Authorization': 'Basic ' + self.authorization
            # }

    def login_error(self, status_code=500, text_message="", headers=None):
        headers = self.get_headers(headers=headers)

        response = self.app.post(self.get_uri_login(), headers=headers)

        self.error_asserts(response, status_code, text_message)

    def auth_logout(self):
        # remove the JWT Token from the header
        del self.__headers__["Authorization"]

    ######################################################################
    # GET, POST, DELETE METHODS
    ######################################################################

    def get(self, expected={}, status_code=200, text_message="", **params):
        response = self.app.get(self.get_uri(), params=params, headers=self.__headers__)

        self.assertEqual(response.status_code, status_code)

        # if I expect a `text_message` instead of a JSON
        if text_message != "":
            self.assertEqual(response.text, text_message)

        # if the response constains curly brackets, then it is a JSON
        elif "{" in response.text and "}" in response.text:
            self.assertEqual(loads(response.text), expected)

    def post(self, body, status_code=200, text_message=""):
        response = self.app.post(self.get_uri(), data=dumps(body), headers=self.__headers__)

        self.assertEqual(response.status_code, status_code)

        if response.text.isdigit():
            id = int(response.text)

            self.assertGreater(id, 0)

            return id
        else:
            self.assertEqual(response.text, text_message)

    def post_create(self, body, status_code=200, text_message=""):
        response = self.app.post(self.get_uri() + '/create', data=dumps(body), headers=self.__headers__)

        self.assertEqual(response.status_code, status_code)

        if response.text.isdigit():
            id = int(response.text)

            self.assertGreater(id, 0)

            return id
        else:
            self.assertEqual(response.text, text_message)

    def put(self, body, status_code=200, text_message=""):
        response = self.app.put(self.get_uri(), data=dumps(body), headers=self.__headers__)

        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.text, text_message)

    def delete(self, status_code=200, text_message="", **params):
        response = self.app.delete(self.get_uri(), params=params, headers=self.__headers__)

        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.text, text_message)

    ######################################################################
    # GET, POST, DELETE ERROR METHODS
    ######################################################################
    '''
    def get_error(self, query_string="", status_code=500, error_message="", headers=None):
        headers = self.get_headers(headers=headers)

        response = self.app.get(self.get_uri(), query_string=query_string, headers=headers)

        self.error_asserts(response, status_code, error_message)

    def post_error(self, body, status_code=500, error_message="", headers=None):
        headers = self.get_headers(headers=headers)

        response = self.app.post(self.get_uri(), data=dumps(body), headers=headers)

        self.error_asserts(response, status_code, error_message)

    def put_error(self, body, status_code=500, error_message="", headers=None):
        headers = self.get_headers(headers=headers)

        response = self.app.put(self.get_uri(), data=dumps(body), headers=headers)

        self.error_asserts(response, status_code, error_message)

    def delete_error(self, query_string="", status_code=500, error_message="", headers=None):
        headers = self.get_headers(headers=headers)

        response = self.app.delete(self.get_uri(), query_string=query_string, headers=headers)

        self.error_asserts(response, status_code, error_message)
    '''


class UtilTester:

    def __init__(self, ut_self):
        # create a session, simulating a browser. It is necessary to create cookies on server
        self.session = Session()
        # headers
        # self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        self.headers = {'Content-type': 'application/json', 'Accept': 'application/json; charset=UTF-8'}
        # unittest self
        self.ut_self = ut_self

        self.URL = "http://localhost:8888"

    ##################################################
    # LOGIN
    ##################################################

    # login and logout

    def prepare_header(self, email, password):
        password = get_string_in_hash_sha512(password)

        email_and_password_in_base64 = get_email_and_password_as_string_in_base64(email, password)

        headers = deepcopy(self.headers)

        headers["Authorization"] = "Basic " + email_and_password_in_base64

        return headers

    def auth_login(self, email, password):
        headers = self.prepare_header(email, password)

        response = self.session.get(self.URL + '/api/auth/login/', headers=headers)

        # Save the JWT token of the server in Authorization header
        self.headers["Authorization"] = response.headers["Authorization"]

        self.ut_self.assertEqual(response.status_code, 200)

    def auth_login_non_existing_user(self):
        # create an `Authorization` header to a non-existing user
        self.headers["Authorization"] = generate_encoded_jwt_token({
            'type': 'User',
            'properties': {'name': 'Non-existing user', 'email': 'no_user@admin.com', 'picture': '', 'user_id': 543, 'username': 'no_user', 'social_id': '', 'created_at': '2017-06-09 00:00:00', 'login_date': '2017-06-09T00:00:00', 'is_the_admin': False, 'terms_agreed': False, 'is_email_valid': True, 'social_account': '', 'receive_notification_by_email': True}
        })

    # auth_login error

    def auth_login_409_conflict(self, email, password):
        headers = self.prepare_header(email, password)

        response = self.session.get(self.URL + '/api/auth/login/', headers=headers)

        self.ut_self.assertEqual(response.status_code, 409)

    ##################################################
    # CHANGE PASSWORD
    ##################################################

    def api_change_password(self, resource_json):
        # encrypt the passwords
        resource_json["properties"]["current_password"] = get_string_in_hash_sha512(resource_json["properties"]["current_password"])
        resource_json["properties"]["new_password"] = get_string_in_hash_sha512(resource_json["properties"]["new_password"])

        response = self.session.post(self.URL + '/api/auth/change_password/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_change_password_error_400_bad_request(self, resource_json):
        response = self.session.post(self.URL + '/api/auth/change_password/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_change_password_error_401_unauthorized(self, resource_json):
        response = self.session.post(self.URL + '/api/auth/change_password/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_change_password_error_409_conflict(self, resource_json):
        # encrypt the passwords
        resource_json["properties"]["current_password"] = get_string_in_hash_sha512(resource_json["properties"]["current_password"])
        resource_json["properties"]["new_password"] = get_string_in_hash_sha512(resource_json["properties"]["new_password"])

        response = self.session.post(self.URL + '/api/auth/change_password/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 409)

    # def auth_login_fake(self):
    #     response = self.session.get(self.URL + '/api/auth/login/fake/')
    #
    #     # Save the JWT token of the server in Authorization header
    #     self.headers["Authorization"] = response.headers["Authorization"]
    #
    #     self.ut_self.assertEqual(response.status_code, 200)

    def auth_logout(self):
        # response = self.session.get(self.URL + '/auth/logout')
        #
        # self.ut_self.assertEqual(response.status_code, 200)

        # remove the JWT Token of the Authorization
        del self.headers["Authorization"]

    # logout error

    def auth_logout_404_not_found(self):
        response = self.session.get(self.URL + '/auth/logout')

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # USER
    ##################################################

    def api_user(self, expected=None, expected_at_least=None, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/user/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        if expected is not None:
            self.ut_self.assertEqual(expected, resulted)

        elif expected_at_least is not None:
            self.compare_expected_at_least_with_resulted(expected_at_least, resulted)

        return resulted

    def api_user_create(self, feature_json):
        # create a copy to send to server (with the password encrypted)
        feature_json_copy = deepcopy(feature_json)

        # cryptography the password before to send
        feature_json_copy["properties"]["password"] = get_string_in_hash_sha512(feature_json_copy["properties"]["password"])

        response = self.session.post(self.URL + '/api/user/create/',
                                     data=dumps(feature_json_copy), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("user_id", resulted)
        self.ut_self.assertNotEqual(resulted["user_id"], -1)

        # put the id received in the original JSON
        feature_json["properties"]["user_id"] = resulted["user_id"]

        return feature_json

    def api_user_update(self, resource_json):
        response = self.session.put(self.URL + '/api/user/',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_user_delete(self, feature_id):
        response = self.session.delete(self.URL + '/api/user/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # user errors - get

    def api_user_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/user/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    # user errors - create

    def api_user_error_create_400_bad_request(self, feature_json):
        # create a copy to send to server (with the password encrypted)
        feature_json_copy = deepcopy(feature_json)

        # cryptography the password before to send
        feature_json_copy["properties"]["password"] = get_string_in_hash_sha512(feature_json_copy["properties"]["password"])

        response = self.session.post(self.URL + '/api/user/create/',
                                    data=dumps(feature_json_copy), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    # user errors - update

    def api_user_update_error_400_bad_request(self, resource_json):
        response = self.session.put(self.URL + '/api/user',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_user_update_error_401_unauthorized(self, resource_json):
        response = self.session.put(self.URL + '/api/user',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_user_update_error_403_forbidden(self, resource_json):
        response = self.session.put(self.URL + '/api/user',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_user_update_error_404_not_found(self, resource_json):
        response = self.session.put(self.URL + '/api/user',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    # user errors - delete

    def api_user_delete_error_400_bad_request(self, feature_id):
        response = self.session.delete(self.URL + '/api/user/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_user_delete_error_401_unauthorized(self, feature_id):
        response = self.session.delete(self.URL + '/api/user/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_user_delete_error_403_forbidden(self, feature_id):
        response = self.session.delete(self.URL + '/api/user/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_user_delete_error_404_not_found(self, feature_id):
        response = self.session.delete(self.URL + '/api/user/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # VALIDATE EMAIL
    ##################################################

    def api_validate_email(self, token):
        response = self.session.get(self.URL + '/api/validate_email/{0}'.format(token))

        self.ut_self.assertEqual(response.status_code, 200)

    def api_validate_email_400_bad_request(self, token):
        response = self.session.get(self.URL + '/api/validate_email/{0}'.format(token))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_validate_email_404_not_found(self, token):
        response = self.session.get(self.URL + '/api/validate_email/{0}'.format(token))

        self.ut_self.assertEqual(response.status_code, 404)

    def api_is_email_valid(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/is_email_valid/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

    ##################################################
    # CURATOR
    ##################################################

    def api_curator(self, expected=None, expected_at_least=None, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/curator/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        if expected is not None:
            self.ut_self.assertEqual(expected, resulted)

        elif expected_at_least is not None:
            self.compare_expected_at_least_with_resulted(expected_at_least, resulted)

    def api_curator_create(self, resource_json, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/curator/create/{0}'.format(arguments),
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_curator_update(self, resource_json):
        response = self.session.put(self.URL + '/api/curator/',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_curator_delete(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/curator/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # curator errors - get

    def api_curator_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/curator/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    # curator errors - create

    def api_curator_create_error_400_bad_request(self, feature_json):
        response = self.session.post(self.URL + '/api/curator/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_curator_create_error_401_unauthorized(self, feature_json):
        response = self.session.post(self.URL + '/api/curator/create/',
                                     data=dumps(feature_json))

        self.ut_self.assertEqual(response.status_code, 401)

    def api_curator_create_error_403_forbidden(self, feature_json):
        response = self.session.post(self.URL + '/api/curator/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    # curator errors - update

    def api_curator_update_error_400_bad_request(self, resource_json):
        response = self.session.put(self.URL + '/api/curator',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_curator_update_error_401_unauthorized(self, feature_json):
        response = self.session.put(self.URL + '/api/curator',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_curator_update_error_403_forbidden(self, feature_json):
        response = self.session.put(self.URL + '/api/curator',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_curator_update_error_404_not_found(self, feature_json):
        response = self.session.put(self.URL + '/api/curator',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    # curator errors - delete

    def api_curator_delete_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/curator/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_curator_delete_error_401_unauthorized(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/curator/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_curator_delete_error_403_forbidden(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/curator/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_curator_delete_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/curator/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # LAYER
    ##################################################

    def api_layer(self, expected=None, expected_at_least=None, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/layer/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        if expected is not None:
            self.ut_self.assertEqual(expected, resulted)

        elif expected_at_least is not None:
            self.compare_expected_at_least_with_resulted(expected_at_least, resulted)

    def api_layer_create(self, feature_json, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/layer/create/{0}'.format(arguments),
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("layer_id", resulted)
        self.ut_self.assertNotEqual(resulted["layer_id"], -1)

        # put the id received in the original JSON
        feature_json["properties"]["layer_id"] = resulted["layer_id"]

        return feature_json

    def api_layer_update(self, resource_json):
        response = self.session.put(self.URL + '/api/layer/',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_layer_delete(self, feature_id):
        response = self.session.delete(self.URL + '/api/layer/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # layer errors - get

    def api_layer_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/layer/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    # layer errors - create

    def api_layer_create_error_400_bad_request(self, resource_json):
        response = self.session.post(self.URL + '/api/layer/create/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_layer_create_error_404_not_found(self, resource_json):
        response = self.session.post(self.URL + '/api/layer/create/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    def api_layer_create_error_401_unauthorized(self, feature_json):
        response = self.session.post(self.URL + '/api/layer/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_layer_create_error_409_conflict(self, resource_json):
        response = self.session.post(self.URL + '/api/layer/create/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 409)

    # layer errors - update

    def api_layer_update_error_400_bad_request(self, resource_json):
        response = self.session.put(self.URL + '/api/layer',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_layer_update_error_401_unauthorized(self, resource_json):
        response = self.session.put(self.URL + '/api/layer',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_layer_update_error_403_forbidden(self, resource_json):
        response = self.session.put(self.URL + '/api/layer',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_layer_update_error_404_not_found(self, resource_json):
        response = self.session.put(self.URL + '/api/layer',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    def api_layer_update_error_409_conflict(self, resource_json):
        response = self.session.put(self.URL + '/api/layer',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 409)

    # layer errors - delete

    def api_layer_delete_error_400_bad_request(self, feature_id):
        response = self.session.delete(self.URL + '/api/layer/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_layer_delete_error_401_unauthorized(self, feature_id):
        response = self.session.delete(self.URL + '/api/layer/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_layer_delete_error_403_forbidden(self, feature_id):
        response = self.session.delete(self.URL + '/api/layer/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_layer_delete_error_404_not_found(self, feature_id):
        response = self.session.delete(self.URL + '/api/layer/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # TIME COLUMNS
    ##################################################

    def api_temporal_columns(self, expected, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/temporal_columns/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

    def api_temporal_columns_create(self, resource_json, **arguments):
        response = self.session.post(self.URL + '/api/temporal_columns/create/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_temporal_columns_update(self, resource_json):
        response = self.session.put(self.URL + '/api/temporal_columns/',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # def api_temporal_columns_delete(self, **arguments):
    #     arguments = get_url_arguments(**arguments)
    #
    #     response = self.session.delete(self.URL + '/api/temporal_columns/{0}'.format(arguments),
    #                                    headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 200)

    # temporal_columns errors - get

    def api_temporal_columns_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/temporal_columns/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    # temporal_columns errors - create

    def api_temporal_columns_create_error_400_bad_request(self, feature_json):
        response = self.session.post(self.URL + '/api/temporal_columns/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_temporal_columns_create_error_401_unauthorized(self, feature_json):
        response = self.session.post(self.URL + '/api/temporal_columns/create/',
                                     data=dumps(feature_json))

        self.ut_self.assertEqual(response.status_code, 401)

    def api_temporal_columns_create_error_403_forbidden(self, feature_json):
        response = self.session.post(self.URL + '/api/temporal_columns/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_temporal_columns_create_error_404_not_found(self, feature_json):
        response = self.session.post(self.URL + '/api/temporal_columns/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    def api_temporal_columns_create_error_409_conflict(self, feature_json):
        response = self.session.post(self.URL + '/api/temporal_columns/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 409)

    # temporal_columns errors - update

    def api_temporal_columns_update_error_400_bad_request(self, resource_json):
        response = self.session.put(self.URL + '/api/temporal_columns',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_temporal_columns_update_error_401_unauthorized(self, feature_json):
        response = self.session.put(self.URL + '/api/temporal_columns',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_temporal_columns_update_error_403_forbidden(self, feature_json):
        response = self.session.put(self.URL + '/api/temporal_columns',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_temporal_columns_update_error_404_not_found(self, feature_json):
        response = self.session.put(self.URL + '/api/temporal_columns',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    # temporal_columns errors - delete

    # def api_curator_delete_error_400_bad_request(self, **arguments):
    #     arguments = get_url_arguments(**arguments)
    #
    #     response = self.session.delete(self.URL + '/api/curator/{0}'.format(arguments),
    #                                    headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 400)
    #
    # def api_curator_delete_error_401_unauthorized(self, **arguments):
    #     arguments = get_url_arguments(**arguments)
    #
    #     response = self.session.delete(self.URL + '/api/curator/{0}'.format(arguments),
    #                                    headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 401)
    #
    # def api_curator_delete_error_403_forbidden(self, **arguments):
    #     arguments = get_url_arguments(**arguments)
    #
    #     response = self.session.delete(self.URL + '/api/curator/{0}'.format(arguments),
    #                                    headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 403)
    #
    # def api_curator_delete_error_404_not_found(self, **arguments):
    #     arguments = get_url_arguments(**arguments)
    #
    #     response = self.session.delete(self.URL + '/api/curator/{0}'.format(arguments),
    #                                    headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # FEATURE TABLE
    ##################################################

    def api_feature_table(self, expected, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/feature_table/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

    def api_feature_table_create(self, resource_json):
        response = self.session.post(self.URL + '/api/feature_table/create/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_feature_table_update(self, resource_json):
        response = self.session.put(self.URL + '/api/feature_table/',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # def api_feature_table_delete(self, **arguments):
    #     arguments = get_url_arguments(**arguments)
    #
    #     response = self.session.delete(self.URL + '/api/feature_table/{0}'.format(arguments),
    #                                    headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 200)

    # feature_table errors - get

    def api_feature_table_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/feature_table/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    # feature_table errors - create

    def api_feature_table_create_error_400_bad_request(self, feature_json):
        response = self.session.post(self.URL + '/api/feature_table/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_feature_table_create_error_401_unauthorized(self, feature_json):
        response = self.session.post(self.URL + '/api/feature_table/create/',
                                     data=dumps(feature_json))

        self.ut_self.assertEqual(response.status_code, 401)

    def api_feature_table_create_error_403_forbidden(self, feature_json):
        response = self.session.post(self.URL + '/api/feature_table/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_feature_table_create_error_404_not_found(self, feature_json):
        response = self.session.post(self.URL + '/api/feature_table/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    def api_feature_table_create_error_409_conflict(self, feature_json):
        response = self.session.post(self.URL + '/api/feature_table/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 409)

    # feature_table errors - update

    def api_feature_table_update_error_400_bad_request(self, resource_json):
        response = self.session.put(self.URL + '/api/feature_table',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_feature_table_update_error_401_unauthorized(self, feature_json):
        response = self.session.put(self.URL + '/api/feature_table',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_feature_table_update_error_403_forbidden(self, feature_json):
        response = self.session.put(self.URL + '/api/feature_table',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    ##################################################
    # FEATURE TABLE COLUMNS
    ##################################################

    def api_feature_table_column_create(self, resource_json):
        response = self.session.post(self.URL + '/api/feature_table_column/create',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_feature_table_column_delete(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/feature_table_column/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # feature_table errors - create

    def api_feature_table_column_create_error_400_bad_request(self, feature_json):
        response = self.session.post(self.URL + '/api/feature_table_column/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_feature_table_column_create_error_401_unauthorized(self, feature_json):
        response = self.session.post(self.URL + '/api/feature_table_column/create/',
                                     data=dumps(feature_json))

        self.ut_self.assertEqual(response.status_code, 401)

    def api_feature_table_column_create_error_403_forbidden(self, feature_json):
        response = self.session.post(self.URL + '/api/feature_table_column/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_feature_table_column_create_error_404_not_found(self, feature_json):
        response = self.session.post(self.URL + '/api/feature_table_column/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    # feature_table_column errors - delete

    def api_feature_table_column_delete_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/feature_table_column/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_feature_table_column_delete_error_401_unauthorized(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/feature_table_column/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_feature_table_column_delete_error_403_forbidden(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/feature_table_column/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_feature_table_column_delete_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/feature_table_column/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # USER LAYER
    ##################################################

    def api_user_layer(self, expected, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/user_layer/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

    def api_user_layer_create(self, feature_json, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/user_layer/create/{0}'.format(arguments),
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        # resulted = loads(response.text)  # convert string to dict/JSON

    def api_user_layer_update(self, resource_json):
        response = self.session.put(self.URL + '/api/user_layer/',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_user_layer_delete(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/user_layer/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # user layer errors - get

    def api_user_layer_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/user_layer/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    # user layer errors - create

    def api_user_layer_create_error_400_bad_request(self, feature_json):
        response = self.session.post(self.URL + '/api/user_layer/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_user_layer_create_error_401_unauthorized(self, feature_json):
        response = self.session.post(self.URL + '/api/user_layer/create/',
                                    data=dumps(feature_json))

        self.ut_self.assertEqual(response.status_code, 401)

    def api_user_layer_create_error_403_forbidden(self, feature_json):
        response = self.session.post(self.URL + '/api/user_layer/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    # user_layer errors - update

    # def api_user_layer_update_error_400_bad_request(self, resource_json):
    #     response = self.session.put(self.URL + '/api/user_layer',
    #                                 data=dumps(resource_json), headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 400)
    #
    # def api_user_layer_update_error_401_unauthorized(self, feature_json):
    #     response = self.session.put(self.URL + '/api/user_layer',
    #                                 data=dumps(feature_json), headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 401)

    # user layer errors - delete

    def api_user_layer_delete_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/user_layer/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_user_layer_delete_error_401_unauthorized(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/user_layer/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_user_layer_delete_error_403_forbidden(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/user_layer/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_user_layer_delete_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/user_layer/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # REFERENCE
    ##################################################

    def api_reference(self, expected=None, expected_at_least=None, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/reference/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        if expected is not None:
            self.ut_self.assertEqual(expected, resulted)

        elif expected_at_least is not None:
            self.compare_expected_at_least_with_resulted(expected_at_least, resulted)

    def api_reference_create(self, resource_json, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/reference/create/{0}'.format(arguments),
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("reference_id", resulted)
        self.ut_self.assertNotEqual(resulted["reference_id"], -1)

        # put the id received in the original JSON
        resource_json["properties"]["reference_id"] = resulted["reference_id"]

        return resource_json

    def api_reference_update(self, resource_json):
        response = self.session.put(self.URL + '/api/reference/',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_reference_delete(self, feature_id):
        response = self.session.delete(self.URL + '/api/reference/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # reference errors - get

    def api_reference_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/reference/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    # reference errors - create

    def api_reference_create_error_400_bad_request(self, resource_json):
        response = self.session.post(self.URL + '/api/reference/create/',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_reference_create_error_401_unauthorized(self, feature_json):
        response = self.session.post(self.URL + '/api/reference/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    # reference errors - update

    def api_reference_update_error_400_bad_request(self, resource_json):
        response = self.session.put(self.URL + '/api/reference',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_reference_update_error_401_unauthorized(self, resource_json):
        response = self.session.put(self.URL + '/api/reference',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_reference_update_error_403_forbidden(self, resource_json):
        response = self.session.put(self.URL + '/api/reference',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_reference_update_error_404_not_found(self, resource_json):
        response = self.session.put(self.URL + '/api/reference',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    # reference errors - delete

    def api_reference_delete_error_400_bad_request(self, feature_id):
        response = self.session.delete(self.URL + '/api/reference/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_reference_delete_error_401_unauthorized(self, feature_id):
        response = self.session.delete(self.URL + '/api/reference/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_reference_delete_error_403_forbidden(self, feature_id):
        response = self.session.delete(self.URL + '/api/reference/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_reference_delete_error_404_not_found(self, feature_id):
        response = self.session.delete(self.URL + '/api/reference/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # KEYWORD
    ##################################################

    def api_keyword(self, expected=None, expected_at_least=None, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/keyword/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        if expected is not None:
            self.ut_self.assertEqual(expected, resulted)

        elif expected_at_least is not None:
            self.compare_expected_at_least_with_resulted(expected_at_least, resulted)

    def api_keyword_create(self, resource_json, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/keyword/create/{0}'.format(arguments),
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("keyword_id", resulted)
        self.ut_self.assertNotEqual(resulted["keyword_id"], -1)

        # put the id received in the original JSON
        resource_json["properties"]["keyword_id"] = resulted["keyword_id"]

        return resource_json

    def api_keyword_update(self, resource_json):
        response = self.session.put(self.URL + '/api/keyword/',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_keyword_delete(self, feature_id):
        response = self.session.delete(self.URL + '/api/keyword/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # keyword errors - get

    def api_keyword_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/keyword/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    # keyword errors - create

    def api_keyword_create_error_400_bad_request(self, resource_json):
        response = self.session.post(self.URL + '/api/keyword/create/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_keyword_create_error_401_unauthorized(self, feature_json):
        response = self.session.post(self.URL + '/api/keyword/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    # keyword errors - update

    def api_keyword_update_error_400_bad_request(self, resource_json):
        response = self.session.put(self.URL + '/api/keyword',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_keyword_update_error_401_unauthorized(self, feature_json):
        response = self.session.put(self.URL + '/api/keyword',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_keyword_update_error_403_forbidden(self, feature_json):
        response = self.session.put(self.URL + '/api/keyword',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_keyword_update_error_404_not_found(self, feature_json):
        response = self.session.put(self.URL + '/api/keyword',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    # keyword errors - delete

    def api_keyword_delete_error_400_bad_request(self, feature_id):
        response = self.session.delete(self.URL + '/api/keyword/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_keyword_delete_error_401_unauthorized(self, feature_id):
        response = self.session.delete(self.URL + '/api/keyword/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_keyword_delete_error_403_forbidden(self, feature_id):
        response = self.session.delete(self.URL + '/api/keyword/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_keyword_delete_error_404_not_found(self, feature_id):
        response = self.session.delete(self.URL + '/api/keyword/{0}'.format(feature_id),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # CHANGESET
    ##################################################

    def api_changeset(self, expected, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/changeset/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

        # if expected_at_least is not None:
        #     """
        #     Test Case: Changesets can not be removed, because of this, the result of the returned
        #     changesets may be larger than expected (because there are other tests that create
        #     changesets). Because of this I pass a subset of minimum changesets that have to exist.
        #     """
        #
        #     """ Explanation: Generator creating booleans by looping through list
        #         'expected_at_least["features"]', checking if that item is in list 'resulted["features"]'.
        #         all() returns True if every item is truthy, else False.
        #         https://stackoverflow.com/questions/16579085/python-verifying-if-one-list-is-a-subset-of-the-other
        #     """
        #     __set__ = resulted["features"]  # set returned
        #     __subset__ = expected_at_least["features"]  # subset expected
        #
        #     # check if the elements of a subset is in a set, if OK, return True, else False
        #     resulted_bool = all(element in __set__ for element in __subset__)
        #
        #     self.ut_self.assertTrue(resulted_bool)

    def api_changeset_create(self, resource_json):
        # do a GET call, sending a changeset to add in DB
        response = self.session.post(self.URL + '/api/changeset/create',
                                     data=dumps(resource_json), headers=self.headers)

        id = int(response.text)

        self.ut_self.assertEqual(response.status_code, 200)
        self.ut_self.assertGreater(id, 0)

        return id

    def api_changeset_close(self, resource_json):
        response = self.session.post(self.URL + '/api/changeset/close',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_changeset_delete(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/changeset/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # changeset errors - get

    def api_changeset_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/changeset/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    # changeset errors - create

    def api_changeset_create_error_400_bad_request(self, feature_json):
        response = self.session.post(self.URL + '/api/changeset/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_changeset_create_error_401_unauthorized(self, feature_json):
        response = self.session.post(self.URL + '/api/changeset/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    # changeset errors - close

    def api_changeset_close_error_400_bad_request(self, resource_json):
        response = self.session.post(self.URL + '/api/changeset/close',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_changeset_close_error_401_unauthorized(self, resource_json):
        response = self.session.post(self.URL + '/api/changeset/close',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_changeset_close_error_404_not_found(self, resource_json):
        response = self.session.post(self.URL + '/api/changeset/close',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    def api_changeset_close_error_409_conflict(self, resource_json):
        response = self.session.post(self.URL + '/api/changeset/close',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 409)

    # changeset errors - delete

    def api_changeset_delete_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/changeset/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_changeset_delete_error_401_unauthorized(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/changeset/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_changeset_delete_error_403_forbidden(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/changeset/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_changeset_delete_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/changeset/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # NOTIFICATION
    ##################################################

    def api_notification(self, expected=None, expected_at_least=None, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/notification/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        if expected is not None:
            self.ut_self.assertEqual(expected, resulted)

        elif expected_at_least is not None:
            self.compare_expected_at_least_with_resulted(expected_at_least, resulted)

    def api_notification_create(self, resource_json):
        response = self.session.post(self.URL + '/api/notification/create',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("notification_id", resulted)
        self.ut_self.assertNotEqual(resulted["notification_id"], -1)

        # put the id received in the original JSON
        resource_json["properties"]["notification_id"] = resulted["notification_id"]

        return resource_json

    def api_notification_update(self, resource_json):
        response = self.session.put(self.URL + '/api/notification/',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_notification_delete(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/notification/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # notification errors - get

    def api_notification_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/notification/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    # notification errors - create

    def api_notification_create_error_400_bad_request(self, resource_json):
        response = self.session.post(self.URL + '/api/notification/create',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_notification_create_error_401_unauthorized(self, feature_json):
        response = self.session.post(self.URL + '/api/notification/create',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    # notification errors - update

    def api_notification_update_error_400_bad_request(self, resource_json):
        response = self.session.put(self.URL + '/api/notification',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_notification_update_error_401_unauthorized(self, feature_json):
        response = self.session.put(self.URL + '/api/notification',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_notification_update_error_403_forbidden(self, feature_json):
        response = self.session.put(self.URL + '/api/notification',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_notification_update_error_404_not_found(self, feature_json):
        response = self.session.put(self.URL + '/api/notification',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    # notification errors - delete

    def api_notification_delete_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/notification/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_notification_delete_error_401_unauthorized(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/notification/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_notification_delete_error_403_forbidden(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/notification/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_notification_delete_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/notification/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # NOTIFICATION RELATED TO USER
    ##################################################

    def api_notification_related_to_user(self, expected=None, expected_at_least=None, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/notification_related_to_user/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        if expected is not None:
            self.ut_self.assertEqual(expected, resulted)

        elif expected_at_least is not None:
            self.compare_expected_at_least_with_resulted(expected_at_least, resulted)

    # notification errors - get

    def api_notification_related_to_user_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/notification_related_to_user/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_notification_related_to_user_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/notification_related_to_user/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # FEATURE
    ##################################################

    def api_feature(self, expected=None, expected_at_least=None, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/feature/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        if expected is not None:
            self.ut_self.assertEqual(expected, resulted)

        elif expected_at_least is not None:
            self.compare_expected_at_least_with_resulted(expected_at_least, resulted)

    def api_feature_create(self, resource_json, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/feature/create/{0}'.format(arguments),
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON
        resource_json["properties"]["id"] = resulted["id"]

        return resource_json

    def api_feature_update(self, resource_json):
        response = self.session.put(self.URL + '/api/feature/',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_feature_delete(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/feature/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # feature errors - get

    def api_feature_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/feature/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_feature_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/feature/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # feature errors - create

    def api_feature_create_error_400_bad_request(self, resource_json):
        response = self.session.post(self.URL + '/api/feature/create/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_feature_create_error_401_unauthorized(self, feature_json):
        response = self.session.post(self.URL + '/api/feature/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_feature_create_error_403_forbidden(self, resource_json):
        response = self.session.post(self.URL + '/api/feature/create/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_feature_create_error_404_not_found(self, resource_json, string_to_compare_error=None):
        response = self.session.post(self.URL + '/api/feature/create/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

        # check if the error message is the correct
        if string_to_compare_error is not None:
            self.ut_self.assertIn(string_to_compare_error.lower(), response.text.lower())

    def api_feature_create_error_409_conflict(self, resource_json):
        response = self.session.post(self.URL + '/api/feature/create/',
                                     data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 409)

    # feature errors - update

    def api_feature_update_error_400_bad_request(self, resource_json, string_to_compare_error=None):
        response = self.session.put(self.URL + '/api/feature',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

        # check if the error message is the correct
        if string_to_compare_error is not None:
            self.ut_self.assertIn(string_to_compare_error.lower(), response.text.lower())

    def api_feature_update_error_401_unauthorized(self, resource_json):
        response = self.session.put(self.URL + '/api/feature',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_feature_update_error_403_forbidden(self, resource_json, string_to_compare_error=None):
        response = self.session.put(self.URL + '/api/feature',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

        # check if the error message is the correct
        if string_to_compare_error is not None:
            self.ut_self.assertIn(string_to_compare_error.lower(), response.text.lower())

    def api_feature_update_error_404_not_found(self, resource_json, string_to_compare_error=None):
        response = self.session.put(self.URL + '/api/feature',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

        # check if the error message is the correct
        if string_to_compare_error is not None:
            self.ut_self.assertIn(string_to_compare_error.lower(), response.text.lower())

    def api_feature_update_error_409_conflict(self, resource_json, string_to_compare_error=None):
        response = self.session.put(self.URL + '/api/feature',
                                    data=dumps(resource_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 409)

        # check if the error message is the correct
        if string_to_compare_error is not None:
            self.ut_self.assertIn(string_to_compare_error.lower(), response.text.lower())

    # feature errors - delete

    def api_feature_delete_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/feature/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_feature_delete_error_401_unauthorized(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/feature/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_feature_delete_error_403_forbidden(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/feature/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_feature_delete_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/feature/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    def api_feature_delete_error_409_conflict(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/feature/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 409)

    ##################################################
    # LAYER FOLLOWER
    ##################################################

    def api_layer_follower(self, expected=None, expected_at_least=None, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/layer_follower/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        if expected is not None:
            self.ut_self.assertEqual(expected, resulted)

        elif expected_at_least is not None:
            self.compare_expected_at_least_with_resulted(expected_at_least, resulted)

    def api_layer_follower_create(self, feature_json, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/layer_follower/create/{0}'.format(arguments),
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # def api_layer_follower_update(self, resource_json):
    #     response = self.session.put(self.URL + '/api/layer_follower/',
    #                                 data=dumps(resource_json), headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 200)

    def api_layer_follower_delete(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/layer_follower/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # layer_follower errors - get

    def api_layer_follower_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/layer_follower/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    # user layer errors - create

    def api_layer_follower_create_error_400_bad_request(self, feature_json):
        response = self.session.post(self.URL + '/api/layer_follower/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_layer_follower_create_error_401_unauthorized(self, feature_json):
        response = self.session.post(self.URL + '/api/layer_follower/create/',
                                     data=dumps(feature_json))

        self.ut_self.assertEqual(response.status_code, 401)

    def api_layer_follower_create_error_403_forbidden(self, feature_json):
        response = self.session.post(self.URL + '/api/layer_follower/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_layer_follower_create_error_409_conflict(self, feature_json):
        response = self.session.post(self.URL + '/api/layer_follower/create/',
                                     data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 409)

    # layer_follower errors - update

    # def api_layer_follower_update_error_400_bad_request(self, resource_json):
    #     response = self.session.put(self.URL + '/api/layer_follower',
    #                                 data=dumps(resource_json), headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 400)
    #
    # def api_layer_follower_update_error_401_unauthorized(self, feature_json):
    #     response = self.session.put(self.URL + '/api/layer_follower',
    #                                 data=dumps(feature_json), headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 401)

    # layer_follower errors - delete

    def api_layer_follower_delete_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/layer_follower/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_layer_follower_delete_error_401_unauthorized(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/layer_follower/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_layer_follower_delete_error_403_forbidden(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/layer_follower/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_layer_follower_delete_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/layer_follower/{0}'.format(arguments),
                                       headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # IMPORT
    ##################################################

    def api_import_shp_create(self, binary_file, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/import/shp/{0}'.format(arguments),
                                     data=binary_file, headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    # import errors - create

    def api_import_shp_create_error_400_bad_request(self, binary_file, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/import/shp/{0}'.format(arguments),
                                     data=binary_file, headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_import_shp_create_error_401_unauthorized(self, binary_file, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/import/shp/{0}'.format(arguments),
                                     data=binary_file, headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    def api_import_shp_create_error_403_forbidden(self, binary_file, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/import/shp/{0}'.format(arguments),
                                     data=binary_file, headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_import_shp_create_error_404_not_found(self, binary_file, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/import/shp/{0}'.format(arguments),
                                     data=binary_file, headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 404)

    def api_import_shp_create_error_409_conflict(self, binary_file, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/import/shp/{0}'.format(arguments),
                                     data=binary_file, headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 409)

    def api_import_shp_create_error_500_internal_server_error(self, binary_file, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/import/shp/{0}'.format(arguments),
                                     data=binary_file, headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 500)

    ##################################################
    # MASK
    ##################################################

    def api_mask(self, expected, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/mask/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

    # mask errors - get

    def api_mask_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/mask/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_mask_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/mask/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    ##################################################
    # CONVERT GEOJSON TO SHAPEFILE
    ##################################################

    def api_post_convert_geojson_to_shapefile(self, binary_file, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/convert_geojson_to_shapefile/{0}'.format(arguments),
                                     data=binary_file, headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        # (source: https://stackoverflow.com/questions/17011357/what-is-the-difference-between-content-and-text)
        # binary_zip_file = response.text  # r.text is the content of the response in unicode
        binary_zip_file = response.content  # r.content is the content of the response in bytes.

        return binary_zip_file

    def api_post_convert_geojson_to_shapefile_400_bad_request(self, binary_file, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/convert_geojson_to_shapefile/{0}'.format(arguments),
                                     data=binary_file, headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_post_convert_geojson_to_shapefile_500_internal_server_error(self, binary_file, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.post(self.URL + '/api/convert_geojson_to_shapefile/{0}'.format(arguments),
                                     data=binary_file, headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 500)

    # FEATURE TABLE

    # ELEMENT

    # def api_element(self, element, element_expected, **arguments):
    #     # get the arguments of the URL
    #     arguments = get_url_arguments(**arguments)
    #
    #     # do a GET call with default format (GeoJSON)
    #     response = self.session.get(self.URL + '/api/{0}/{1}'.format(element, arguments))
    #
    #     self.ut_self.assertEqual(response.status_code, 200)
    #
    #     resulted = loads(response.text)  # convert string to dict/JSON
    #
    #     self.ut_self.assertEqual(element_expected, resulted)
    #
    # def api_element_create(self, element_json):
    #     multi_element = element_json["features"][0]["geometry"]["type"]
    #     element = by_multi_element_get_url_name(multi_element)
    #
    #     # do a post call, sending a node to add in DB
    #     response = self.session.post(self.URL + '/api/{0}/create/'.format(element),
    #                                 data=dumps(element_json), headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 200)
    #
    #     list_of_id_of_features_created = loads(response.text)  # convert string to dict/JSON
    #
    #     # add the id of the feature for each feature created
    #     for feature, id_feature in zip(element_json["features"], list_of_id_of_features_created):
    #         feature["properties"]["id"] = id_feature
    #
    #     return element_json
    #
    # def api_element_delete(self, element_json):
    #     multi_element = element_json["features"][0]["geometry"]["type"]
    #
    #     element = by_multi_element_get_url_name(multi_element)
    #     element_id = element_json["features"][0]["properties"]["id"]  # get the id of element
    #
    #     response = self.session.delete(self.URL + '/api/{0}/{1}'.format(element, element_id))
    #
    #     self.ut_self.assertEqual(response.status_code, 200)
    #
    # # elements - check
    #
    # def check_if_element_was_add_in_db(self, element_json_expected):
    #     element_id = element_json_expected["features"][0]["properties"]["id"]  # get the id of element
    #
    #     multi_element = element_json_expected["features"][0]["geometry"]["type"]
    #
    #     element = by_multi_element_get_url_name(multi_element)
    #
    #     self.api_element(element, element_json_expected, element_id=element_id)
    #
    # def check_if_element_was_not_add_in_db(self, element_json_expected):
    #     element_id = element_json_expected["features"][0]["properties"]["id"]  # get the id of element
    #
    #     multi_element = element_json_expected["features"][0]["geometry"]["type"]
    #     element = by_multi_element_get_url_name(multi_element)
    #
    #     # get the arguments of the URL
    #     arguments = get_url_arguments(element_id=element_id)
    #
    #     # do a GET call with default format (GeoJSON)
    #     response = self.session.get(self.URL + '/api/{0}/{1}'.format(element, arguments))
    #
    #     self.ut_self.assertEqual(response.status_code, 404)
    #
    # # element errors - get
    #
    # def api_element_error_400_bad_request(self, element, element_id):
    #     arguments = get_url_arguments(element_id=element_id)
    #
    #     response = self.session.get(self.URL + '/api/{0}/{1}'.format(element, arguments))
    #
    #     self.ut_self.assertEqual(response.status_code, 400)
    #
    # def api_element_error_404_not_found(self, element, element_id):
    #     arguments = get_url_arguments(element_id=element_id)
    #
    #     response = self.session.get(self.URL + '/api/{0}/{1}'.format(element, arguments))
    #
    #     self.ut_self.assertEqual(response.status_code, 404)
    #
    # # element errors - create
    #
    # def api_element_create_error_403_forbidden(self, element_json):
    #     multi_element = element_json["features"][0]["geometry"]["type"]
    #     element = by_multi_element_get_url_name(multi_element)
    #
    #     # do a post call, sending a node to add in DB
    #     response = self.session.post(self.URL + '/api/{0}/create/'.format(element),
    #                                 data=dumps(element_json), headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 403)
    #
    # def api_element_create_error_409_conflict(self, element_json):
    #     multi_element = element_json["features"][0]["geometry"]["type"]
    #     element = by_multi_element_get_url_name(multi_element)
    #
    #     # do a post call, sending a node to add in DB
    #     response = self.session.post(self.URL + '/api/{0}/create/'.format(element),
    #                                 data=dumps(element_json), headers=self.headers)
    #
    #     self.ut_self.assertEqual(response.status_code, 409)
    #
    # # element errors - delete
    #
    # def api_element_delete_error_400_bad_request(self, element, element_id):
    #     response = self.session.delete(self.URL + '/api/{0}/{1}'.format(element, element_id))
    #
    #     self.ut_self.assertEqual(response.status_code, 400)
    #
    # def api_element_delete_error_403_forbidden(self, element, element_id):
    #     response = self.session.delete(self.URL + '/api/{0}/{1}'.format(element, element_id))
    #
    #     self.ut_self.assertEqual(response.status_code, 403)
    #
    # def api_element_delete_error_404_not_found(self,  element, element_id):
    #     response = self.session.delete(self.URL + '/api/{0}/{1}'.format(element, element_id))
    #
    #     self.ut_self.assertEqual(response.status_code, 404)
    #
    # # THEME TREE
    #
    # def api_theme_tree(self, expected):
    #     response = self.session.get(self.URL + '/api/theme_tree')
    #
    #     self.ut_self.assertEqual(response.status_code, 200)
    #
    #     resulted = loads(response.text)  # convert string to dict/JSON
    #
    #     self.ut_self.assertEqual(expected, resulted)

    # OTHERS

    def api_capabilities(self, expected):
        response = self.session.get(self.URL + '/api/capabilities/')

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(resulted, expected)

    # user_by_token

    def api_user_by_token(self, expected_at_least):
        response = self.session.get(self.URL + '/api/user_by_token', headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        # comparing the items in an isolated way

        # iterate in expected_at_least dict, because it contains the AT LEAST
        # that has to exist in result.
        # with these way, do not compare the "id" and "created_at" attributes, because
        # these attributes are created in a dynamic way
        for key in expected_at_least["properties"]:
            self.ut_self.assertEqual(resulted["properties"][key], expected_at_least["properties"][key])
        self.ut_self.assertEqual(resulted["type"], expected_at_least["type"])

    def function_api_user_by_token(self):
        response = self.session.get(self.URL + '/api/user_by_token', headers=self.headers)

        if response.status_code == 200:
            return loads(response.text)  # convert string to dict/JSON and return
        else:
            raise Exception("VGIMWS API status error: " + str(response.status_code))

    # user_by_token - errors

    def api_user_by_token_400_bad_request(self, invalid_authorization):
        headers = deepcopy(self.headers)
        headers["Authorization"] = invalid_authorization

        response = self.session.get(self.URL + '/api/user_by_token', headers=headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_user_by_token_401_unauthorized(self):
        response = self.session.get(self.URL + '/api/user_by_token', headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 401)

    ##################################################
    # METHODS
    ##################################################

    def compare_expected_at_least_with_resulted(self, expected_at_least, resulted):
        for feature_at_least, feature_resulted in zip(expected_at_least["features"], resulted["features"]):
            for key in feature_at_least["properties"]:
                self.ut_self.assertEqual(feature_resulted["properties"][key], feature_at_least["properties"][key])
            self.ut_self.assertEqual(resulted["type"], expected_at_least["type"])

    def get_session_user(self):
        response = self.session.get(self.URL + '/api/session/user')

        resulted = loads(response.text)  # convert string to dict/JSON

        return resulted

    def code_windows_to_ubuntu(self, resulted):
        """
        Remove the \r of a string created in Windows. Ubuntu doesn't have \r in its string.
        :param resulted: the returned JSON of the server.
        :return: the formatted JSON.
        """

        for resource in resulted['features']:
            # Remove the \r for the bibtex of a Layer
            if resource['type'] == 'Layer':
                if resource['properties']['reference'] is not None:
                    for reference in resource['properties']['reference']:
                        reference['bibtex'] = reference['bibtex'].replace("\r", "")

        return resulted
