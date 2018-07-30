#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy
from unittest import TestCase

from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPIFeature(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # feature - get
    """
    def test_get_api_feature_return_all_features_by_f_table_name(self):
        expected = {
            'features': [
                {
                    'properties': {'parent_id': None, 'name': 'generic', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1001},
                    'type': 'feature'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_feature(expected, f_table_name="layer_1001")

    def test_get_api_feature_return_feature_by_feature_id(self):
        expected = {
            'features': [
                {
                    'properties': {'parent_id': 1002, 'name': 'crime', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1003},
                    'type': 'feature'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_feature(expected, feature_id="1003")

    def test_get_api_feature_return_feature_by_user_id_creator(self):
        expected = {
            'features': [
                {
                    'properties': {'parent_id': None, 'name': 'generic', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1001},
                    'type': 'feature'
                },
                {
                    'properties': {'parent_id': 1001, 'name': 'event', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1002},
                    'type': 'feature'
                },
                {
                    'properties': {'parent_id': 1002, 'name': 'disease', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1010},
                    'type': 'feature'
                },
                {
                    'properties': {'parent_id': 1001, 'name': 'object', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1020},
                    'type': 'feature'
                },
                {
                    'properties': {'parent_id': 1030, 'name': 'cinema', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1031},
                    'type': 'feature'
                },
                {
                    'properties': {'parent_id': 1020, 'name': 'street', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1040},
                    'type': 'feature'
                },
                {
                    'properties': {'parent_id': 1020, 'name': 'address', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1041},
                    'type': 'feature'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_feature(expected, user_id_creator="1001")

    def test_get_api_feature_return_feature_by_parent_id(self):
        expected = {
            'features': [
                {
                    'properties': {'parent_id': None, 'name': 'generic', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1001},
                    'type': 'feature'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_feature(expected, parent_id="NULL")

        expected = {
            'features': [
                {
                    'properties': {'parent_id': 1003, 'name': 'assault', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1004},
                    'type': 'feature'
                },
                {
                    'properties': {'parent_id': 1003, 'name': 'robbery', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1005},
                    'type': 'feature'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_feature(expected, parent_id="1003")

    def test_get_api_feature_return_feature_by_name(self):
        expected = {
            'features': [
                {
                    'properties': {'parent_id': 1003, 'name': 'assault', 'user_id_creator': 1002,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1004},
                    'type': 'feature'
                },
                {
                    'properties': {'parent_id': 1002, 'name': 'disease', 'user_id_creator': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'feature_id': 1010},
                    'type': 'feature'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_feature(expected, name="As")

    # feature - create, update and delete

    def test_api_feature_create_but_update_and_delete_with_admin_user(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create a feature with user gabriel
        ##################################################
        resource = {
            'properties': {'feature_id': -1, 'name': 'newfeature', 'parent_id': 1003},
            'type': 'feature'
        }
        resource = self.tester.api_feature_create(resource)

        # logout with gabriel and login with admin user
        self.tester.auth_logout()
        self.tester.auth_login("admin@admin.com", "admin")

        ##################################################
        # update the feature with admin
        ##################################################
        resource["properties"]["parent_id"] = 1005
        self.tester.api_feature_update(resource)

        ##################################################
        # verify if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_feature(expected_at_least=expected_resource, feature_id=resource["properties"]["feature_id"])

        ##################################################
        # remove the feature with admin
        ##################################################
        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["feature_id"]

        # remove the resource
        self.tester.api_feature_delete(resource_id)

        # it is not possible to find the resource that just deleted
        self.tester.api_feature_error_404_not_found(feature_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
    """

"""
class TestAPIfeatureFeature(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # feature errors - get

    def test_get_api_feature_error_400_bad_request(self):
        self.tester.api_feature_error_400_bad_request(feature_id="abc")
        self.tester.api_feature_error_400_bad_request(feature_id=0)
        self.tester.api_feature_error_400_bad_request(feature_id=-1)
        self.tester.api_feature_error_400_bad_request(feature_id="-1")
        self.tester.api_feature_error_400_bad_request(feature_id="0")

        self.tester.api_feature_error_400_bad_request(parent_id="abc")
        self.tester.api_feature_error_400_bad_request(parent_id=0)
        self.tester.api_feature_error_400_bad_request(parent_id=-1)
        self.tester.api_feature_error_400_bad_request(parent_id="-1")
        self.tester.api_feature_error_400_bad_request(parent_id="0")

        self.tester.api_feature_error_400_bad_request(user_id_creator="abc")
        self.tester.api_feature_error_400_bad_request(user_id_creator=0)
        self.tester.api_feature_error_400_bad_request(user_id_creator=-1)
        self.tester.api_feature_error_400_bad_request(user_id_creator="-1")
        self.tester.api_feature_error_400_bad_request(user_id_creator="0")

    def test_get_api_feature_error_404_not_found(self):
        self.tester.api_feature_error_404_not_found(feature_id="999")
        self.tester.api_feature_error_404_not_found(feature_id="998")

        self.tester.api_feature_error_404_not_found(parent_id="999")
        self.tester.api_feature_error_404_not_found(parent_id="998")

        self.tester.api_feature_error_404_not_found(user_id_creator="999")
        self.tester.api_feature_error_404_not_found(user_id_creator="998")

    # feature errors - create

    def test_post_api_feature_create_error_400_bad_request_attribute_already_exist(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a feature with a name that already exist
        resource = {
            'properties': {'name': 'event', 'parent_id': 1003},
            'type': 'feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer (without name)
        resource = {
            'properties': {'parent_id': 1003},
            'type': 'feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # try to create a layer (without parent_id)
        resource = {
            'properties': {'name': 'newfeature'},
            'type': 'feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_create_error_401_unauthorized_user_is_not_logged(self):
        resource = {
            'properties': {'feature_id': -1, 'name': 'newfeature', 'parent_id': 1003},
            'type': 'feature'
        }
        self.tester.api_feature_create_error_401_unauthorized(resource)

    # feature errors - update

    def test_put_api_feature_error_400_bad_request_attribute_already_exist(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # try to update the feature with a name that already exist, raising the 400
        ##################################################
        resource = {
            'properties': {'feature_id': 1003, 'name': 'street', 'parent_id': 1002},
            'type': 'feature'
        }
        self.tester.api_feature_update_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_feature_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # try to update the feature without a feature_id, raising the 400
        ##################################################
        resource = {
            'properties': {'name': 'newfeature', 'parent_id': 1003},
            'type': 'feature'
        }
        self.tester.api_feature_update_error_400_bad_request(resource)

        ##################################################
        # try to update the feature without a name, raising the 400
        ##################################################
        resource = {
            'properties': {'feature_id': 1003, 'parent_id': 1003},
            'type': 'feature'
        }
        self.tester.api_feature_update_error_400_bad_request(resource)

        ##################################################
        # try to update the feature without a parent_id, raising the 400
        ##################################################
        resource = {
            'properties': {'feature_id': 1003, 'name': 'newfeature'},
            'type': 'feature'
        }
        self.tester.api_feature_update_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_feature_error_401_unauthorized_user_is_not_logged(self):
        resource = {
            'properties': {'feature_id': 1001, 'name': 'newfeature', 'parent_id': 1003},
            'type': 'feature'
        }
        self.tester.api_feature_update_error_401_unauthorized(resource)

    def test_put_api_feature_error_403_forbidden_invalid_user_tries_to_manage(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # gabriel tries to update one feature that doesn't belong to him
        ##################################################
        resource = {
            'properties': {'feature_id': 1003, 'name': 'street', 'parent_id': 1002},
            'type': 'feature'
        }
        self.tester.api_feature_update_error_403_forbidden(resource)

        # DO LOGOUT
        self.tester.auth_logout()

    def test_put_api_feature_error_404_not_found(self):
        # DO LOGIN
        self.tester.auth_login("admin@admin.com", "admin")

        resource = {
            'properties': {'feature_id': 999, 'name': 'street', 'parent_id': 1002},
            'type': 'feature'
        }
        self.tester.api_feature_update_error_404_not_found(resource)

        # DO LOGOUT
        self.tester.auth_logout()

    # feature errors - delete

    def test_delete_api_feature_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_feature_delete_error_400_bad_request("abc")
        self.tester.api_feature_delete_error_400_bad_request(0)
        self.tester.api_feature_delete_error_400_bad_request(-1)
        self.tester.api_feature_delete_error_400_bad_request("-1")
        self.tester.api_feature_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_feature_error_401_unauthorized_user_is_not_logged(self):
        self.tester.api_feature_delete_error_401_unauthorized("abc")
        self.tester.api_feature_delete_error_401_unauthorized(0)
        self.tester.api_feature_delete_error_401_unauthorized(-1)
        self.tester.api_feature_delete_error_401_unauthorized("-1")
        self.tester.api_feature_delete_error_401_unauthorized("0")
        self.tester.api_feature_delete_error_401_unauthorized("1001")

    def test_delete_api_feature_error_403_forbidden_invalid_user_tries_to_manage(self):
        self.tester.auth_login("miguel@admin.com", "miguel")

        ########################################
        # try to delete the feature with user miguel
        ########################################
        # TRY TO REMOVE THE LAYER
        self.tester.api_feature_delete_error_403_forbidden(1001)

        # logout with user rodrigo
        self.tester.auth_logout()

    def test_delete_api_feature_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_feature_delete_error_404_not_found("5000")
        self.tester.api_feature_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
"""

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
