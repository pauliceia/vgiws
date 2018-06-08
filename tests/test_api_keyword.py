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
                    'properties': {'parent_id': None, 'name': 'generic', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1001},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1001, 'name': 'event', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1002},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1002, 'name': 'crime', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1003},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1003, 'name': 'assault', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1004},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1003, 'name': 'robbery', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1005},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1002, 'name': 'disease', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1010},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1001, 'name': 'object', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1020},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1020, 'name': 'building', 'user_id_creator': 1003,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1021},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1021, 'name': 'school', 'user_id_creator': 1003,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1022},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1021, 'name': 'hospital', 'user_id_creator': 1003,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1023},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1020, 'name': 'cultural place', 'user_id_creator': 1003,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1030},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1030, 'name': 'cinema', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1031},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1020, 'name': 'street', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1040},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1020, 'name': 'address', 'user_id_creator': 1001,
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
                    'properties': {'parent_id': 1002, 'name': 'crime', 'user_id_creator': 1002,
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
                    'properties': {'parent_id': None, 'name': 'generic', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1001},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1001, 'name': 'event', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1002},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1002, 'name': 'disease', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1010},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1001, 'name': 'object', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1020},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1030, 'name': 'cinema', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1031},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1020, 'name': 'street', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1040},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1020, 'name': 'address', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1041},
                    'type': 'Keyword'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_keyword(expected, user_id_creator="1001")

    def test_get_api_keyword_return_keyword_by_parent_id(self):
        expected = {
            'features': [
                {
                    'properties': {'parent_id': None, 'name': 'generic', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1001},
                    'type': 'Keyword'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_keyword(expected, parent_id="NULL")

        expected = {
            'features': [
                {
                    'properties': {'parent_id': 1003, 'name': 'assault', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1004},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1003, 'name': 'robbery', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1005},
                    'type': 'Keyword'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_keyword(expected, parent_id="1003")

    def test_get_api_keyword_return_keyword_by_name(self):
        expected = {
            'features': [
                {
                    'properties': {'parent_id': 1003, 'name': 'assault', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1004},
                    'type': 'Keyword'
                },
                {
                    'properties': {'parent_id': 1002, 'name': 'disease', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'keyword_id': 1010},
                    'type': 'Keyword'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_keyword(expected, name="As")

    # keyword - create, update and delete

    # user create/update/delete his/her keyword (it is not possible, because just admin can update/delete keywords
    # def test_api_keyword_create_update_and_delete(self):
    #     # DO LOGIN
    #     self.tester.auth_login("rafael@admin.com", "rafael")
    #
    #     ##################################################
    #     # create a keyword with parent_id = None
    #     ##################################################
    #     resource = {
    #         'properties': {'keyword_id': -1, 'name': 'newkeyword', 'parent_id': None},
    #         'type': 'Keyword'
    #     }
    #     resource = self.tester.api_keyword_create(resource)
    #
    #     ##################################################
    #     # update the keyword
    #     ##################################################
    #     resource["properties"]["name"] = 'nova_keyword'
    #     self.tester.api_keyword_update(resource)
    #
    #     ##################################################
    #     # remove the keyword
    #     ##################################################
    #     # get the id of layer to REMOVE it
    #     resource_id = resource["properties"]["keyword_id"]
    #
    #     # remove the resource
    #     self.tester.api_keyword_delete(resource_id)
    #
    #     # it is not possible to find the resource that just deleted
    #     self.tester.api_keyword_error_404_not_found(keyword_id=resource_id)
    #
    #     ##################################################
    #     # create a keyword with parent_id = 1003
    #     ##################################################
    #     resource = {
    #         'properties': {'keyword_id': -1, 'name': 'newkeyword', 'parent_id': 1003},
    #         'type': 'Keyword'
    #     }
    #     resource = self.tester.api_keyword_create(resource)
    #
    #     ##################################################
    #     # update the keyword
    #     ##################################################
    #     resource["properties"]["parent_id"] = 1004
    #     self.tester.api_keyword_update(resource)
    #
    #     ##################################################
    #     # remove the keyword
    #     ##################################################
    #     # get the id of layer to REMOVE it
    #     resource_id = resource["properties"]["keyword_id"]
    #
    #     # remove the resource
    #     self.tester.api_keyword_delete(resource_id)
    #
    #     # it is not possible to find the resource that just deleted
    #     self.tester.api_keyword_error_404_not_found(keyword_id=resource_id)
    #
    #     # DO LOGOUT AFTER THE TESTS
    #     self.tester.auth_logout()

    def test_api_keyword_create_but_update_and_delete_with_admin_user(self):
        # DO LOGIN
        self.tester.auth_login("gabriel@admin.com", "gabriel")

        ##################################################
        # create a keyword with user gabriel
        ##################################################
        resource = {
            'properties': {'keyword_id': -1, 'name': 'newkeyword', 'parent_id': 1003},
            'type': 'Keyword'
        }
        resource = self.tester.api_keyword_create(resource)

        # logout with gabriel and login with admin user
        self.tester.auth_logout()
        self.tester.auth_login("admin@admin.com", "admin")

        ##################################################
        # update the keyword with admin
        ##################################################
        resource["properties"]["parent_id"] = 1005
        self.tester.api_keyword_update(resource)

        ##################################################
        # remove the keyword with admin
        ##################################################
        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["keyword_id"]

        # remove the resource
        self.tester.api_keyword_delete(resource_id)

        # it is not possible to find the resource that just deleted
        self.tester.api_keyword_error_404_not_found(keyword_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIKeywordErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # keyword errors - get

    def test_get_api_keyword_error_400_bad_request(self):
        self.tester.api_keyword_error_400_bad_request(keyword_id="abc")
        self.tester.api_keyword_error_400_bad_request(keyword_id=0)
        self.tester.api_keyword_error_400_bad_request(keyword_id=-1)
        self.tester.api_keyword_error_400_bad_request(keyword_id="-1")
        self.tester.api_keyword_error_400_bad_request(keyword_id="0")

        self.tester.api_keyword_error_400_bad_request(parent_id="abc")
        self.tester.api_keyword_error_400_bad_request(parent_id=0)
        self.tester.api_keyword_error_400_bad_request(parent_id=-1)
        self.tester.api_keyword_error_400_bad_request(parent_id="-1")
        self.tester.api_keyword_error_400_bad_request(parent_id="0")

        self.tester.api_keyword_error_400_bad_request(user_id_creator="abc")
        self.tester.api_keyword_error_400_bad_request(user_id_creator=0)
        self.tester.api_keyword_error_400_bad_request(user_id_creator=-1)
        self.tester.api_keyword_error_400_bad_request(user_id_creator="-1")
        self.tester.api_keyword_error_400_bad_request(user_id_creator="0")

    def test_get_api_keyword_error_404_not_found(self):
        self.tester.api_keyword_error_404_not_found(keyword_id="999")
        self.tester.api_keyword_error_404_not_found(keyword_id="998")

        self.tester.api_keyword_error_404_not_found(parent_id="999")
        self.tester.api_keyword_error_404_not_found(parent_id="998")

        self.tester.api_keyword_error_404_not_found(user_id_creator="999")
        self.tester.api_keyword_error_404_not_found(user_id_creator="998")

    # keyword errors - create

    def test_post_api_keyword_create_error_400_bad_request_attribute_already_exist(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # create a layer
        resource = {
            'properties': {'name': 'newkeyword', 'parent_id': 1003},
            'type': 'Keyword'
        }
        resource = self.tester.api_keyword_create(resource)

        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["keyword_id"]

        ##################################################
        # try to insert the keyword again, raising the 400
        ##################################################
        self.tester.api_keyword_create_error_400_bad_request(resource)

        # remove the resource after the tests
        self.tester.api_keyword_delete(resource_id)

        # it is not possible to find the resource that just deleted
        self.tester.api_keyword_error_404_not_found(keyword_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_keyword_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer (without name)
        resource = {
            'properties': {'parent_id': 1003},
            'type': 'Keyword'
        }
        self.tester.api_keyword_create_error_400_bad_request(resource)

        # try to create a layer (without parent_id)
        resource = {
            'properties': {'name': 'newkeyword'},
            'type': 'Keyword'
        }
        self.tester.api_keyword_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_keyword_create_error_401_unauthorized(self):
        resource = {
            'properties': {'keyword_id': -1, 'name': 'newkeyword', 'parent_id': 1003},
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
            'properties': {'keyword_id': 1003, 'name': 'street', 'parent_id': 1002},
            'type': 'Keyword'
        }
        self.tester.api_keyword_update_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_keyword_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # try to update the keyword without a keyword_id, raising the 400
        ##################################################
        resource = {
            'properties': {'name': 'newkeyword', 'parent_id': 1003},
            'type': 'Keyword'
        }
        self.tester.api_keyword_update_error_400_bad_request(resource)

        ##################################################
        # try to update the keyword without a name, raising the 400
        ##################################################
        resource = {
            'properties': {'keyword_id': 1003, 'parent_id': 1003},
            'type': 'Keyword'
        }
        self.tester.api_keyword_update_error_400_bad_request(resource)

        ##################################################
        # try to update the keyword without a parent_id, raising the 400
        ##################################################
        resource = {
            'properties': {'keyword_id': 1003, 'name': 'newkeyword'},
            'type': 'Keyword'
        }
        self.tester.api_keyword_update_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_keyword_error_401_unauthorized(self):
        resource = {
            'properties': {'keyword_id': 1001, 'name': 'newkeyword', 'parent_id': 1003},
            'type': 'Keyword'
        }
        self.tester.api_keyword_update_error_401_unauthorized(resource)

    def test_put_api_keyword_error_403_forbidden_user_forbidden_to_update(self):
        # DO LOGIN
        self.tester.auth_login("gabriel@admin.com", "gabriel")

        ##################################################
        # gabriel tries to update one keyword that doesn't belong to him
        ##################################################
        resource = {
            'properties': {'keyword_id': 1003, 'name': 'street', 'parent_id': 1002},
            'type': 'Keyword'
        }
        self.tester.api_keyword_update_error_403_forbidden(resource)

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

    def test_delete_api_keyword_error_401_unauthorized_user_without_login(self):
        self.tester.api_keyword_delete_error_401_unauthorized("abc")
        self.tester.api_keyword_delete_error_401_unauthorized(0)
        self.tester.api_keyword_delete_error_401_unauthorized(-1)
        self.tester.api_keyword_delete_error_401_unauthorized("-1")
        self.tester.api_keyword_delete_error_401_unauthorized("0")
        self.tester.api_keyword_delete_error_401_unauthorized("1001")

    def test_delete_api_keyword_error_403_forbidden_user_forbidden_to_delete(self):
        ########################################
        # create a keyword with user admin
        ########################################

        self.tester.auth_login("admin@admin.com", "admin")

        # create a layer
        resource = {
            'properties': {'keyword_id': -1, 'name': 'newkeyword', 'parent_id': None},
            'type': 'Keyword'
        }
        resource = self.tester.api_keyword_create(resource)

        # logout with admin and login with gabriel
        self.tester.auth_logout()
        self.tester.auth_login("gabriel@admin.com", "gabriel")

        ########################################
        # try to delete the keyword with user gabriel
        ########################################
        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["keyword_id"]

        # TRY TO REMOVE THE LAYER
        self.tester.api_keyword_delete_error_403_forbidden(resource_id)

        # logout with user rodrigo
        self.tester.auth_logout()

        ########################################
        # really delete the layer with user admin
        ########################################
        self.tester.auth_login("admin@admin.com", "admin")

        # delete the layer
        self.tester.api_keyword_delete(resource_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_keyword_error_404_not_found(keyword_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
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

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
