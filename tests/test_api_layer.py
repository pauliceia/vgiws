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
                    'type': 'Layer',
                    'properties': {'source': ["book1", "article2"], 'removed_at': None, 'name': 'Addresses in 1869',
                                   'fk_theme_id': 1041, 'table_name': 'layer_1001',
                                   'created_at': '2017-01-01 00:00:00', 'fk_user_id': 1001,
                                   'id': 1001, 'description': ''}
                },
                {
                    'type': 'Layer',
                    'properties': {'source': ['http://link_to_document'], 'removed_at': None,
                                   'name': 'Robberies between 1880 to 1900', 'fk_theme_id': 1010,
                                   'table_name': 'layer_1002', 'created_at': '2017-03-05 00:00:00',
                                   'fk_user_id': 1003, 'id': 1002, 'description': ''}
                },
                {
                    'type': 'Layer',
                    'properties': {'source': ['http://link_to_document'], 'removed_at': None,
                                   'name': 'Streets in 1930', 'fk_theme_id': 1040,
                                   'table_name': 'layer_1003', 'created_at': '2017-04-10 00:00:00',
                                   'fk_user_id': 1005, 'id': 1003, 'description': ''}
                },
                {
                    'type': 'Layer',
                    'properties': {'source': [], 'removed_at': None, 'name': 'Hospitals between 1800 to 1950',
                                   'fk_theme_id': 1023, 'table_name': 'layer_1005',
                                   'created_at': '2017-08-04 00:00:00', 'fk_user_id': 1007,
                                   'id': 1005, 'description': 'some hospitals'}
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
                    'properties': {'source': ["book1", "article2"], 'removed_at': None, 'name': 'Addresses in 1869',
                                   'fk_theme_id': 1041, 'table_name': 'layer_1001',
                                   'created_at': '2017-01-01 00:00:00', 'fk_user_id': 1001,
                                   'id': 1001, 'description': ''}
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, layer_id="1001")

    def test_get_api_layer_return_layer_by_user_id(self):
        expected = {
            'features': [
                {
                    'type': 'Layer',
                    'properties': {'source': ['http://link_to_document'], 'removed_at': None,
                                   'name': 'Robberies between 1880 to 1900', 'fk_theme_id': 1010,
                                   'table_name': 'layer_1002', 'created_at': '2017-03-05 00:00:00',
                                   'fk_user_id': 1003, 'id': 1002, 'description': ''}
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, user_id="1003")

    # layer - create and delete

    def test_get_api_layer_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login_fake()

        # create a layer
        resource = {
            # 'tags': {'created_by': 'test_api', 'description': 'description of the layer', 'name': 'layer of data'},
            # 'properties': {'id': -1, 'fk_project_id': 1001},
            # 'type': 'Layer',
            'type': 'Layer',
            'properties': {'name': 'Addresses in 1869', 'table_name': 'new_layer', 'source': [],
                           'description': '', 'fk_theme_id': 1041}
        }
        resource = self.tester.api_layer_create(resource)

        # create the feature table for the layer
        feature_table = {
            'type': 'FeatureTable',
            'table_name': 'new_layer',
            'properties': {'name': 'text', 'start_date': 'text', 'end_date': 'text'},
            'geometry': {"type": "MultiPoint"}
        }
        self.tester.api_feature_table_create(feature_table)

        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["id"]

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(resource_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_layer_error_404_not_found(layer_id=resource_id)

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

    def test_put_api_layer_create_error_400_bad_request(self):
        # DO LOGIN
        self.tester.auth_login_fake()

        # create a layer
        resource = {
            'type': 'Layer',
            'properties': {'name': 'Addresses in 1869', 'table_name': 'new_layer', 'source': '',
                           'description': '', 'fk_theme_id': 1041}
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_layer_create_error_403_forbidden(self):
        feature = {
            'properties': {'name': 'Addresses in 1869', 'table_name': 'new_layer', 'source': '',
                           'description': '', 'fk_theme_id': 1041},
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


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
