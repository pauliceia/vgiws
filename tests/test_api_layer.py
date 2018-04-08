#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester

"""
# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPILayer(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # layer - get

    def test_get_api_layer_return_all_layers(self):
        expected = {
            'features': [
                {
                    'properties': {'removed_at': None, 'created_at': '2017-11-20 00:00:00',
                                   'fk_user_id': 1001, 'id': 1001},
                    'tags': {'description': 'default layer', 'name': 'default', 'theme': 'generic'},
                    'type': 'Layer'
                },
                {
                    'properties': {'removed_at': None, 'created_at': '2017-10-12 00:00:00',
                                   'fk_user_id': 1002, 'id': 1002},
                    'tags': {'description': 'test_layer', 'name': 'test_layer', 'theme': 'crime'},
                    'type': 'Layer'
                },
                {
                    'properties': {'removed_at': None, 'created_at': '2017-12-23 00:00:00',
                                   'fk_user_id': 1002, 'id': 1003},
                    'tags': {'description': 'test_layer', 'name': 'layer 3', 'theme': 'addresses'},
                    'type': 'Layer'
                },
                {
                    'properties': {'removed_at': None, 'created_at': '2017-09-11 00:00:00',
                                   'fk_user_id': 1003, 'id': 1004},
                    'tags': {'description': 'test_layer', 'name': 'layer 4'},
                    'type': 'Layer'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected)

    def test_get_api_layer_return_layer_by_layer_id(self):
        expected = {
            'features': [
                {
                    'properties': {'removed_at': None, 'created_at': '2017-11-20 00:00:00',
                                   'fk_user_id': 1001, 'id': 1001},
                    'tags': {'description': 'default layer', 'name': 'default', 'theme': 'generic'},
                    'type': 'Layer'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, layer_id="1001")

    def test_get_api_layer_return_layer_by_user_id(self):
        expected = {
            'features': [
                {
                    'properties': {'removed_at': None, 'created_at': '2017-10-12 00:00:00',
                                   'fk_user_id': 1002, 'id': 1002},
                    'tags': {'description': 'test_layer', 'name': 'test_layer', 'theme': 'crime'},
                    'type': 'Layer'
                },
                {
                    'properties': {'removed_at': None, 'created_at': '2017-12-23 00:00:00',
                                   'fk_user_id': 1002, 'id': 1003},
                    'tags': {'description': 'test_layer', 'name': 'layer 3', 'theme': 'addresses'},
                    'type': 'Layer'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, user_id="1002")

    # layer - create and delete

    def test_get_api_layer_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login_fake()

        # create a layer
        feature = {
            'tags': {'created_by': 'test_api', 'description': 'description of the layer', 'name': 'layer of data'},
            'properties': {'id': -1, 'fk_project_id': 1001},
            'type': 'Layer'
        }
        feature = self.tester.api_layer_create(feature)

        # get the id of layer to REMOVE it
        feature_id = feature["properties"]["id"]

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(feature_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPILayerErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # layer errors - get

    def test_get_api_layer_error_400_bad_request(self):
        self.tester.api_layer_error_400_bad_request(layer_id="abc")
        self.tester.api_layer_error_400_bad_request(layer_id=0)
        self.tester.api_layer_error_400_bad_request(layer_id=-1)
        self.tester.api_layer_error_400_bad_request(layer_id="-1")
        self.tester.api_layer_error_400_bad_request(layer_id="0")

    def test_get_api_layer_error_404_not_found(self):
        self.tester.api_layer_error_404_not_found(layer_id="999")
        self.tester.api_layer_error_404_not_found(layer_id="998")

    # layer errors - create

    def test_put_api_layer_create_error_403_forbidden(self):
        feature = {
            'tags': [{'k': 'created_by', 'v': 'test_api'},
                     {'k': 'description', 'v': 'description of the layer'},
                     {'k': 'name', 'v': 'layer of data'}],
            'properties': {'id': -1},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_403_forbidden(feature)

    # layer errors - delete

    def test_delete_api_layer_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login_fake()

        self.tester.api_layer_delete_error_400_bad_request("abc")
        self.tester.api_layer_delete_error_400_bad_request(0)
        self.tester.api_layer_delete_error_400_bad_request(-1)
        self.tester.api_layer_delete_error_400_bad_request("-1")
        self.tester.api_layer_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_layer_error_403_forbidden(self):
        self.tester.api_layer_delete_error_403_forbidden("abc")
        self.tester.api_layer_delete_error_403_forbidden(0)
        self.tester.api_layer_delete_error_403_forbidden(-1)
        self.tester.api_layer_delete_error_403_forbidden("-1")
        self.tester.api_layer_delete_error_403_forbidden("0")
        self.tester.api_layer_delete_error_403_forbidden("1001")

    def test_delete_api_layer_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login_fake()

        self.tester.api_layer_delete_error_404_not_found("5000")
        self.tester.api_layer_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

"""
# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
