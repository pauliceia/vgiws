#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy
from unittest import TestCase

from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPIKeyword(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # keyword - get

    def test_get_api_keyword_return_all_keywords(self):
        expected = {
            'features': [
                {
                    'properties': {'name': 'generic', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1001},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'event', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1002},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'crime', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1003},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'assault', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1004},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'robbery', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1005},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'disease', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1010},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'object', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1020},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'building', 'user_id_creator': 1003,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1021},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'school', 'user_id_creator': 1003,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1022},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'hospital', 'user_id_creator': 1003,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1023},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'cultural place', 'user_id_creator': 1003,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1030},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'cinema', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1031},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'street', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1040},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'address', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1041},
                    'type': 'Keyword'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_keyword(expected)

    def test_get_api_keyword_return_keyword_by_keyword_id(self):
        expected = {
            'features': [
                {
                    'properties': {'name': 'crime', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1003},
                    'type': 'Keyword'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_keyword(expected, keyword_id="1003")

    def test_get_api_keyword_return_keyword_by_user_id_creator(self):
        expected = {
            'features': [
                {
                    'properties': {'name': 'generic', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1001},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'event', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1002},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'disease', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1010},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'object', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1020},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'cinema', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1031},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'street', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1040},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'address', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1041},
                    'type': 'Keyword'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_keyword(expected, user_id_creator="1001")

    def test_get_api_keyword_return_keyword_by_name(self):
        expected = {
            'features': [
                {
                    'properties': {'name': 'assault', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1004},
                    'type': 'Keyword'
                },
                {
                    'properties': {'name': 'disease', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1010},
                    'type': 'Keyword'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_keyword(expected, name="As")

    def test_get_api_keyword_return_zero_resources(self):
        expected = {'features': [], 'type': 'FeatureCollection'}

        self.tester.api_keyword(expected, keyword_id="999")
        self.tester.api_keyword(expected, keyword_id="998")

        self.tester.api_keyword(expected, user_id_creator="999")
        self.tester.api_keyword(expected, user_id_creator="998")

    # keyword - create, update and delete

    def test_api_keyword_create_but_update_and_delete_with_admin_user(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create a keyword with user gabriel
        ##################################################
        resource = {
            'properties': {'keyword_id': -1, 'name': 'newkeyword'},
            'type': 'Keyword'
        }
        resource = self.tester.api_keyword_create(resource)

        # logout with gabriel and login with admin user
        self.tester.auth_logout()
        self.tester.auth_login("admin@admin.com", "admin")

        ##################################################
        # update the keyword with admin
        ##################################################
        resource["properties"]["name"] = "newname"
        self.tester.api_keyword_update(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_keyword(expected_at_least=expected_resource, keyword_id=resource["properties"]["keyword_id"])

        ##################################################
        # remove the keyword with admin
        ##################################################
        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["keyword_id"]

        # remove the resource
        self.tester.api_keyword_delete(resource_id)

        # it is not possible to find the resource that just deleted
        expected = {'features': [], 'type': 'FeatureCollection'}
        self.tester.api_keyword(expected, keyword_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIKeywordErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # keyword errors - get

    def test_get_api_keyword_error_400_bad_request(self):
        # invalid parameter
        self.tester.api_keyword_error_400_bad_request(keyword_id="abc")
        self.tester.api_keyword_error_400_bad_request(keyword_id=0)
        self.tester.api_keyword_error_400_bad_request(keyword_id=-1)
        self.tester.api_keyword_error_400_bad_request(keyword_id="-1")
        self.tester.api_keyword_error_400_bad_request(keyword_id="0")

        self.tester.api_keyword_error_400_bad_request(user_id_creator="abc")
        self.tester.api_keyword_error_400_bad_request(user_id_creator=0)
        self.tester.api_keyword_error_400_bad_request(user_id_creator=-1)
        self.tester.api_keyword_error_400_bad_request(user_id_creator="-1")
        self.tester.api_keyword_error_400_bad_request(user_id_creator="0")

        # invalid argument
        self.tester.api_keyword_error_400_bad_request(parent_id=1001)
        self.tester.api_keyword_error_400_bad_request(usee_id=1001)
        self.tester.api_keyword_error_400_bad_request(keyboard_id=1001)

    # keyword errors - create

    def test_post_api_keyword_create_error_400_bad_request_attribute_already_exist(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a keyword with a name that already exist
        resource = {
            'properties': {'name': 'event'},
            'type': 'Keyword'
        }
        self.tester.api_keyword_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_keyword_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer (without name)
        resource = {
            'properties': {},
            'type': 'Keyword'
        }
        self.tester.api_keyword_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_keyword_create_error_401_unauthorized_user_is_not_logged(self):
        resource = {
            'properties': {'keyword_id': -1, 'name': 'newkeyword'},
            'type': 'Keyword'
        }
        self.tester.api_keyword_create_error_401_unauthorized(resource)

    # keyword errors - update

    def test_put_api_keyword_error_400_bad_request_attribute_already_exist(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # try to update the keyword with a name that already exist, raising the 400
        ##################################################
        resource = {
            'properties': {'keyword_id': 1003, 'name': 'street'},
            'type': 'Keyword'
        }
        self.tester.api_keyword_update_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_keyword_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to update the keyword without a keyword_id, raising the 400
        resource = {
            'properties': {'name': 'newkeyword'},
            'type': 'Keyword'
        }
        self.tester.api_keyword_update_error_400_bad_request(resource)

        # try to update the keyword without a name, raising the 400
        resource = {
            'properties': {'keyword_id': 1003},
            'type': 'Keyword'
        }
        self.tester.api_keyword_update_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_keyword_error_401_unauthorized_user_is_not_logged(self):
        resource = {
            'properties': {'keyword_id': 1001, 'name': 'newkeyword'},
            'type': 'Keyword'
        }
        self.tester.api_keyword_update_error_401_unauthorized(resource)

    def test_put_api_keyword_error_403_forbidden_invalid_user_tries_to_manage(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # gabriel tries to update one keyword that doesn't belong to him
        ##################################################
        resource = {
            'properties': {'keyword_id': 1003, 'name': 'street'},
            'type': 'Keyword'
        }
        self.tester.api_keyword_update_error_403_forbidden(resource)

        # DO LOGOUT
        self.tester.auth_logout()

    def test_put_api_keyword_error_404_not_found(self):
        # DO LOGIN
        self.tester.auth_login("admin@admin.com", "admin")

        resource = {
            'properties': {'keyword_id': 999, 'name': 'street'},
            'type': 'Keyword'
        }
        self.tester.api_keyword_update_error_404_not_found(resource)

        # DO LOGOUT
        self.tester.auth_logout()

    # keyword errors - delete

    def test_delete_api_keyword_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_keyword_delete_error_400_bad_request("abc")
        self.tester.api_keyword_delete_error_400_bad_request(0)
        self.tester.api_keyword_delete_error_400_bad_request(-1)
        self.tester.api_keyword_delete_error_400_bad_request("-1")
        self.tester.api_keyword_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_keyword_error_401_unauthorized_user_is_not_logged(self):
        self.tester.api_keyword_delete_error_401_unauthorized("abc")
        self.tester.api_keyword_delete_error_401_unauthorized(0)
        self.tester.api_keyword_delete_error_401_unauthorized(-1)
        self.tester.api_keyword_delete_error_401_unauthorized("-1")
        self.tester.api_keyword_delete_error_401_unauthorized("0")
        self.tester.api_keyword_delete_error_401_unauthorized("1001")

    def test_delete_api_keyword_error_403_forbidden_invalid_user_tries_to_manage(self):
        self.tester.auth_login("miguel@admin.com", "miguel")

        ########################################
        # try to delete the keyword with user miguel
        ########################################
        # TRY TO REMOVE THE LAYER
        self.tester.api_keyword_delete_error_403_forbidden(1001)

        # logout with user rodrigo
        self.tester.auth_logout()

    def test_delete_api_keyword_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_keyword_delete_error_404_not_found("5000")
        self.tester.api_keyword_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
