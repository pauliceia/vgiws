#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


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
                    'properties': {'removed_at': None, 'create_at': '2017-11-20 00:00:00', 'fk_user_id_owner': 1001, 'id': 1001},
                    'tags': [{'k': 'name', 'v': 'default'}, {'k': 'description', 'v': 'default layer'}],
                    'type': 'Layer'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-10-12 00:00:00', 'fk_user_id_owner': 1002, 'id': 1002},
                    'tags': [{'k': 'name', 'v': 'test_layer'}, {'k': 'description', 'v': 'test_layer'}],
                    'type': 'Layer'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-12-23 00:00:00', 'fk_user_id_owner': 1002, 'id': 1003},
                    'tags': [{'k': 'name', 'v': 'layer 3'}, {'k': 'description', 'v': 'test_layer'}],
                    'type': 'Layer'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-09-11 00:00:00', 'fk_user_id_owner': 1003, 'id': 1004},
                    'tags': [{'k': 'name', 'v': 'layer 4'}, {'k': 'description', 'v': 'test_layer'}],
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
                    'type': 'Layer',
                    'tags': [{'k': 'name', 'v': 'default'},
                             {'k': 'description', 'v': 'default layer'}],
                    'properties': {'removed_at': None, 'fk_user_id_owner': 1001,
                                   'id': 1001, 'create_at': '2017-11-20 00:00:00'}
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, layer_id="1001")

    def test_get_api_layer_return_layer_by_user_id(self):
        expected = {
            'features': [
                {
                    'properties': {'removed_at': None, 'create_at': '2017-10-12 00:00:00',
                                   'fk_user_id_owner': 1002,'id': 1002},
                    'tags': [{'k': 'name', 'v': 'test_layer'},
                             {'k': 'description', 'v': 'test_layer'}],
                    'type': 'Layer'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-12-23 00:00:00',
                                   'fk_user_id_owner': 1002, 'id': 1003},
                    'tags': [{'k': 'name', 'v': 'layer 3'},
                             {'k': 'description', 'v': 'test_layer'}],
                    'type': 'Layer'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, user_id="1002")

    # layer - create and delete

    def test_get_api_layer_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login()

        # create a layer
        layer = {
            'layer': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'name', 'v': 'layer of data'},
                         {'k': 'description', 'v': 'description of the layer'}],
                'properties': {'id': -1}
            }
        }
        self.layer = self.tester.api_layer_create(layer)

        # get the id of layer to REMOVE it
        layer_id = self.layer["layer"]["properties"]["id"]

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(layer_id)

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
        layer = {
            'layer': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'name', 'v': 'layer of data'},
                         {'k': 'description', 'v': 'description of the layer'}],
                'properties': {'id': -1}
            }
        }
        self.tester.api_layer_create_error_403_forbidden(layer)

    # layer errors - delete

    def test_delete_api_layer_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

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
        self.tester.auth_login()

        self.tester.api_layer_delete_error_404_not_found("5000")
        self.tester.api_layer_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
