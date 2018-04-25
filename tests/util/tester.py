#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import loads, dumps
from requests import Session

from .common import *

from copy import deepcopy


# from modules.common import get_username_and_password_as_string_in_base64

from base64 import b64encode
from hashlib import sha512


def get_username_and_password_as_string_in_base64(username, password):
    username_and_password = username + ":" + password

    string_in_base64 = (b64encode(username_and_password.encode('utf-8'))).decode('utf-8')

    return string_in_base64


def get_string_in_hash_sha512(string):
    return sha512(string.encode()).hexdigest()


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

    # login and logout

    def auth_login(self, email, password):

        password = get_string_in_hash_sha512(password)

        email_and_password_in_base64 = get_username_and_password_as_string_in_base64(email, password)

        # self.headers = {'Content-type': 'application/json',
        #                 'Accept': 'application/json; charset=UTF-8',
        #                 'Authorization': 'Basic ' + username_and_password_in_base64}

        headers = deepcopy(self.headers)

        headers["Authorization"] = "Basic " + email_and_password_in_base64

        response = self.session.get(self.URL + '/auth/login/', headers=headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def auth_login_fake(self):
        response = self.session.get(self.URL + '/auth/login/fake/')

        self.ut_self.assertEqual(response.status_code, 200)

    def auth_logout(self):
        response = self.session.get(self.URL + '/auth/logout')

        self.ut_self.assertEqual(response.status_code, 200)

    # logout error

    def auth_logout_404_not_found(self):
        response = self.session.get(self.URL + '/auth/logout')

        self.ut_self.assertEqual(response.status_code, 404)

    # USER

    def api_user(self, expected=None, expected_at_least=None, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/user/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        if expected is not None:
            self.ut_self.assertEqual(expected, resulted)

        elif expected_at_least is not None:
            self.compare_sets(expected_at_least, resulted)

    def api_user_create(self, feature_json):
        # create a copy to send to server (with the password encrypted)
        feature_json_copy = deepcopy(feature_json)

        # cryptography the password before to send
        feature_json_copy["properties"]["password"] = get_string_in_hash_sha512(feature_json_copy["properties"]["password"])

        response = self.session.put(self.URL + '/api/user/create/',
                                    data=dumps(feature_json_copy), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of changeset
        feature_json["properties"]["id"] = resulted["id"]

        return feature_json

    def api_user_delete(self, feature_id):
        response = self.session.delete(self.URL + '/api/user/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 200)

    # user errors - get

    def api_user_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/user/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_user_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/user/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # user errors - delete

    def api_user_delete_error_400_bad_request(self, feature_id):
        response = self.session.delete(self.URL + '/api/user/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_user_delete_error_403_forbidden(self, feature_id):
        response = self.session.delete(self.URL + '/api/user/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_user_delete_error_404_not_found(self, feature_id):
        response = self.session.delete(self.URL + '/api/user/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 404)

    # GROUP

    # get

    def api_group_select(self, **arguments):
        """
        Do a SELECT in DB looking for groups
        :param arguments: a dictionary with arguments to search
        :return: groups found
        """
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/group/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        return resulted

    def api_group(self, expected, **arguments):
        """
        DO a COMPARISON between the group(s) expected and the group(s) found by search
        :param expected: a dictionary expected
        :param arguments: a dictionary with arguments to search
        :return:
        """

        resulted = self.api_group_select(**arguments)

        self.ut_self.assertEqual(expected, resulted)

    def api_group_create(self, feature_json):
        response = self.session.put(self.URL + '/api/group/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of changeset
        feature_json["properties"]["id"] = resulted["id"]

        return feature_json

    def api_group_update(self, feature_json):
        response = self.session.put(self.URL + '/api/group/update/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

    def api_group_delete(self, feature_id):
        response = self.session.delete(self.URL + '/api/group/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 200)

    # group - verify

    def verify_if_one_group_exist_in_db(self, feature_expected):

        feature_id = feature_expected["properties"]["id"]
        feature_tags = feature_expected["tags"]
        feature_type = feature_expected["type"]

        # do a GET in db to obtain the newest version
        feature_resulted = self.api_group_select(group_id=feature_id)
        feature_resulted = feature_resulted["features"][0]

        feature_resulted_id = feature_resulted["properties"]["id"]
        feature_resulted_tags = feature_resulted["tags"]
        feature_resulted_type = feature_resulted["type"]

        # compare parts of the features, because there are some attributes that just the server works
        # with, for example: visible or created_at, so don't compare them
        self.ut_self.assertEqual(feature_id, feature_resulted_id)
        self.ut_self.assertEqual(feature_tags, feature_resulted_tags)
        self.ut_self.assertEqual(feature_type, feature_resulted_type)

    # group errors - get

    def api_group_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/group/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_group_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/group/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # group errors - create

    def api_group_create_error_403_forbidden(self, feature_json):
        response = self.session.put(self.URL + '/api/group/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    # group errors - delete

    def api_group_delete_error_400_bad_request(self, feature_id):
        response = self.session.delete(self.URL + '/api/group/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_group_delete_error_403_forbidden(self, feature_id):
        response = self.session.delete(self.URL + '/api/group/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_group_delete_error_404_not_found(self, feature_id):
        response = self.session.delete(self.URL + '/api/group/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 404)

    # USER_GROUP

    def api_user_group(self, expected, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/user_group/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

    def api_user_group_create(self, feature_json):
        response = self.session.put(self.URL + '/api/user_group/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        # return nothing, because of that, there is no json to compare

        # resulted = loads(response.text)  # convert string to dict/JSON
        #
        # self.ut_self.assertIn("id", resulted)
        # self.ut_self.assertNotEqual(resulted["id"], -1)
        #
        # # put the id received in the original JSON of changeset
        # feature_json["properties"]["id"] = resulted["id"]
        #
        # return feature_json

    def api_user_group_delete(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/user_group/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

    # user_group errors - get

    def api_user_group_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/user_group/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_user_group_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/user_group/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # user_group errors - create

    def api_user_group_create_error_400_bad_request(self, feature_json):
        response = self.session.put(self.URL + '/api/user_group/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_user_group_create_error_403_forbidden(self, feature_json):
        response = self.session.put(self.URL + '/api/user_group/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    # user_group errors - delete

    def api_user_group_delete_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/user_group/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_user_group_delete_error_403_forbidden(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/user_group/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_user_group_delete_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.delete(self.URL + '/api/user_group/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # PROJECT

    def api_project(self, expected, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/project/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

    def api_project_create(self, feature_json):
        response = self.session.put(self.URL + '/api/project/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of changeset
        feature_json["properties"]["id"] = resulted["id"]

        return feature_json

    def api_project_delete(self, feature_id):
        response = self.session.delete(self.URL + '/api/project/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 200)

    # project errors - get

    def api_project_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/project/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_project_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/project/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # project errors - create

    def api_project_create_error_403_forbidden(self, feature_json):
        response = self.session.put(self.URL + '/api/project/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    # project errors - delete

    def api_project_delete_error_400_bad_request(self, feature_id):
        response = self.session.delete(self.URL + '/api/project/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_project_delete_error_403_forbidden(self, feature_id):
        response = self.session.delete(self.URL + '/api/project/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_project_delete_error_404_not_found(self, feature_id):
        response = self.session.delete(self.URL + '/api/project/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 404)

    # LAYER

    def api_layer(self, expected, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/layer/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

    def api_layer_create(self, feature_json):
        response = self.session.put(self.URL + '/api/layer/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of changeset
        feature_json["properties"]["id"] = resulted["id"]

        return feature_json

    def api_layer_delete(self, feature_id):
        response = self.session.delete(self.URL + '/api/layer/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 200)

    # layer errors - get

    def api_layer_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/layer/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_layer_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/layer/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # layer errors - create

    def api_layer_create_error_400_bad_request(self, feature_json):
        response = self.session.put(self.URL + '/api/layer/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_layer_create_error_403_forbidden(self, feature_json):
        response = self.session.put(self.URL + '/api/layer/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    # layer errors - delete

    def api_layer_delete_error_400_bad_request(self, feature_id):
        response = self.session.delete(self.URL + '/api/layer/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_layer_delete_error_403_forbidden(self, feature_id):
        response = self.session.delete(self.URL + '/api/layer/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_layer_delete_error_404_not_found(self, feature_id):
        response = self.session.delete(self.URL + '/api/layer/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 404)

    # FEATURE TABLE

    # def api_layer(self, expected, **arguments):
    #     arguments = get_url_arguments(**arguments)
    #
    #     response = self.session.get(self.URL + '/api/layer/{0}'.format(arguments))
    #
    #     self.ut_self.assertEqual(response.status_code, 200)
    #
    #     resulted = loads(response.text)  # convert string to dict/JSON
    #
    #     self.ut_self.assertEqual(expected, resulted)

    def api_feature_table_create(self, feature_json):
        response = self.session.put(self.URL + '/api/feature_table/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        # resulted = loads(response.text)  # convert string to dict/JSON
        #
        # self.ut_self.assertIn("id", resulted)
        # self.ut_self.assertNotEqual(resulted["id"], -1)
        #
        # # put the id received in the original JSON of changeset
        # feature_json["properties"]["id"] = resulted["id"]
        #
        # return feature_json

    # def api_feature_table_delete(self, feature_id):
    #     response = self.session.delete(self.URL + '/api/layer/{0}'.format(feature_id))
    #
    #     self.ut_self.assertEqual(response.status_code, 200)

    # CHANGESET

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
        #     # verify if the elements of a subset is in a set, if OK, return True, else False
        #     resulted_bool = all(element in __set__ for element in __subset__)
        #
        #     self.ut_self.assertTrue(resulted_bool)

    def api_changeset_create(self, feature_json):
        # do a GET call, sending a changeset to add in DB
        response = self.session.put(self.URL + '/api/changeset/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of changeset
        feature_json["properties"]["id"] = resulted["id"]

        return feature_json

    def api_changeset_close(self, feature_id):
        response = self.session.put(self.URL + '/api/changeset/close/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 200)

    def api_changeset_delete(self, feature_id):
        response = self.session.delete(self.URL + '/api/changeset/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 200)

    # changeset errors - get

    def api_changeset_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/changeset/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_changeset_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/changeset/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # changeset errors - create

    def api_changeset_create_error_403_forbidden(self, feature_json):
        # do a GET call, sending a changeset to add in DB
        response = self.session.put(self.URL + '/api/changeset/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    # changeset errors - close

    def api_changeset_close_error_400_bad_request(self, feature_id):
        response = self.session.put(self.URL + '/api/changeset/close/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_changeset_close_error_403_forbidden(self, feature_id):
        response = self.session.put(self.URL + '/api/changeset/close/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_changeset_close_error_404_not_found(self, feature_id):
        response = self.session.put(self.URL + '/api/changeset/close/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 404)

    # changeset errors - delete

    def api_changeset_delete_error_400_bad_request(self, feature_id):
        response = self.session.delete(self.URL + '/api/changeset/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_changeset_delete_error_403_forbidden(self, feature_id):
        response = self.session.delete(self.URL + '/api/changeset/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_changeset_delete_error_404_not_found(self, feature_id):
        response = self.session.delete(self.URL + '/api/changeset/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 404)

    # NOTIFICATION

    def api_notification(self, expected, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/notification/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

    def api_notification_create(self, feature_json):
        response = self.session.put(self.URL + '/api/notification/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of changeset
        feature_json["properties"]["id"] = resulted["id"]

        return feature_json

    def api_notification_delete(self, feature_id):
        response = self.session.delete(self.URL + '/api/notification/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 200)

    # notification errors - get

    def api_notification_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/notification/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_notification_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get(self.URL + '/api/notification/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # notification errors - create

    def api_notification_create_error_403_forbidden(self, feature_json):
        response = self.session.put(self.URL + '/api/notification/create/',
                                    data=dumps(feature_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    # notification errors - delete

    def api_notification_delete_error_400_bad_request(self, feature_id):
        response = self.session.delete(self.URL + '/api/notification/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_notification_delete_error_403_forbidden(self, feature_id):
        response = self.session.delete(self.URL + '/api/notification/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_notification_delete_error_404_not_found(self, feature_id):
        response = self.session.delete(self.URL + '/api/notification/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 404)

    # ELEMENT

    def api_element(self, element, element_expected, **arguments):
        # get the arguments of the URL
        arguments = get_url_arguments(**arguments)

        # do a GET call with default format (GeoJSON)
        response = self.session.get(self.URL + '/api/{0}/{1}'.format(element, arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(element_expected, resulted)

    def api_element_create(self, element_json):
        multi_element = element_json["features"][0]["geometry"]["type"]
        element = by_multi_element_get_url_name(multi_element)

        # do a PUT call, sending a node to add in DB
        response = self.session.put(self.URL + '/api/{0}/create/'.format(element),
                                    data=dumps(element_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        list_of_id_of_features_created = loads(response.text)  # convert string to dict/JSON

        # add the id of the feature for each feature created
        for feature, id_feature in zip(element_json["features"], list_of_id_of_features_created):
            feature["properties"]["id"] = id_feature

        return element_json

    def api_element_delete(self, element_json):
        multi_element = element_json["features"][0]["geometry"]["type"]

        element = by_multi_element_get_url_name(multi_element)
        element_id = element_json["features"][0]["properties"]["id"]  # get the id of element

        response = self.session.delete(self.URL + '/api/{0}/{1}'.format(element, element_id))

        self.ut_self.assertEqual(response.status_code, 200)

    # elements - verify

    def verify_if_element_was_add_in_db(self, element_json_expected):
        element_id = element_json_expected["features"][0]["properties"]["id"]  # get the id of element

        multi_element = element_json_expected["features"][0]["geometry"]["type"]

        element = by_multi_element_get_url_name(multi_element)

        self.api_element(element, element_json_expected, element_id=element_id)

    def verify_if_element_was_not_add_in_db(self, element_json_expected):
        element_id = element_json_expected["features"][0]["properties"]["id"]  # get the id of element

        multi_element = element_json_expected["features"][0]["geometry"]["type"]
        element = by_multi_element_get_url_name(multi_element)

        # get the arguments of the URL
        arguments = get_url_arguments(element_id=element_id)

        # do a GET call with default format (GeoJSON)
        response = self.session.get(self.URL + '/api/{0}/{1}'.format(element, arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # element errors - get

    def api_element_error_400_bad_request(self, element, element_id):
        arguments = get_url_arguments(element_id=element_id)

        response = self.session.get(self.URL + '/api/{0}/{1}'.format(element, arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_element_error_404_not_found(self, element, element_id):
        arguments = get_url_arguments(element_id=element_id)

        response = self.session.get(self.URL + '/api/{0}/{1}'.format(element, arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # element errors - create

    def api_element_create_error_403_forbidden(self, element_json):
        multi_element = element_json["features"][0]["geometry"]["type"]
        element = by_multi_element_get_url_name(multi_element)

        # do a PUT call, sending a node to add in DB
        response = self.session.put(self.URL + '/api/{0}/create/'.format(element),
                                    data=dumps(element_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    def api_element_create_error_409_conflict(self, element_json):
        multi_element = element_json["features"][0]["geometry"]["type"]
        element = by_multi_element_get_url_name(multi_element)

        # do a PUT call, sending a node to add in DB
        response = self.session.put(self.URL + '/api/{0}/create/'.format(element),
                                    data=dumps(element_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 409)

    # element errors - delete

    def api_element_delete_error_400_bad_request(self, element, element_id):
        response = self.session.delete(self.URL + '/api/{0}/{1}'.format(element, element_id))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_element_delete_error_403_forbidden(self, element, element_id):
        response = self.session.delete(self.URL + '/api/{0}/{1}'.format(element, element_id))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_element_delete_error_404_not_found(self,  element, element_id):
        response = self.session.delete(self.URL + '/api/{0}/{1}'.format(element, element_id))

        self.ut_self.assertEqual(response.status_code, 404)

    # THEME TREE

    def api_theme_tree(self, expected):
        response = self.session.get(self.URL + '/api/theme_tree')

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

    # OTHERS

    def api_capabilities(self, expected):
        response = self.session.get(self.URL + '/api/capabilities/')

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(resulted, expected)

    def api_session_user(self, expected_at_least):
        response = self.session.get(self.URL + '/api/session/user')

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        # comparing the items in a isolated way

        # iterate in expected_at_least dict, because it contains the AT LEAST
        # that have to exist in result.
        # with these way, do not compare the "id" and "created_at" attributes, because
        # these attributes are created in a dynamic way
        for key in expected_at_least["user"]["properties"]:
            self.ut_self.assertEqual(resulted["user"]["properties"][key],
                                     expected_at_least["user"]["properties"][key])
        # self.ut_self.assertEqual(resulted["user"]["tags"], expected_at_least["user"]["tags"])
        self.ut_self.assertEqual(resulted["user"]["type"], expected_at_least["user"]["type"])

    def api_session_user_error_404_not_found(self):
        response = self.session.get(self.URL + '/api/session/user')

        self.ut_self.assertEqual(response.status_code, 404)

    # auxiliar methods

    def compare_sets(self, expected_at_least, resulted):
        """
        Test Case: When log with a fake login, a new user is created, because of this,
        the result returned may be larger than the expected.
        """

        """ Explanation: Generator creating booleans by looping through list
            'expected_at_least["features"]', checking if that item is in list 'resulted["features"]'.
            all() returns True if every item is truthy, else False.
            https://stackoverflow.com/questions/16579085/python-verifying-if-one-list-is-a-subset-of-the-other
        """
        __set__ = resulted["features"]  # set returned
        __subset__ = expected_at_least["features"]  # subset expected

        # verify if the elements of a subset is in a set, if OK, return True, else False
        resulted_bool = all(element in __set__ for element in __subset__)

        self.ut_self.assertTrue(resulted_bool)

    ##################################################
    # METHODS
    ##################################################

    def get_session_user(self):
        response = self.session.get(self.URL + '/api/session/user')

        resulted = loads(response.text)  # convert string to dict/JSON

        return resulted
