#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase, skip
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
                    'properties': {
                        'fk_user_id_published_by': 1001, 'source_author_name': '', 'table_name': '_1001_layer_1001',
                        'created_at': '2017-01-01 00:00:00', 'reference': [{'description': 'book1', 'id': 1001},
                                                                           {'description': 'article2', 'id': 1002}],
                        'removed_at': None, 'fk_user_id_author': 1001, 'description': '', 'is_published': True,
                        'id': 1001, 'name': 'Addresses in 1869'
                    },
                    'type': 'Layer'
                },
                {
                    'properties': {
                        'fk_user_id_published_by': 1003, 'source_author_name': '', 'table_name': '_1003_layer_1002',
                        'created_at': '2017-03-05 00:00:00', 'reference': [{'description': 'http://link_to_document',
                                                                            'id': 1005}],
                        'removed_at': None, 'fk_user_id_author': 1003, 'description': '', 'is_published': True,
                        'id': 1002, 'name': 'Robberies between 1880 to 1900'
                    },
                    'type': 'Layer'
                },
                {
                    'properties': {
                        'fk_user_id_published_by': None, 'source_author_name': '', 'table_name': '_1005_layer_1003',
                        'created_at': '2017-04-10 00:00:00', 'reference': [{'description': 'http://link_to_document',
                                                                            'id': 1010}],
                        'removed_at': None, 'fk_user_id_author': 1005, 'description': '',
                        'is_published': False, 'id': 1003, 'name': 'Streets in 1930'
                    },
                    'type': 'Layer'
                },
                {
                    'properties': {
                        'fk_user_id_published_by': None, 'source_author_name': None, 'table_name': '_1007_layer_1005',
                        'created_at': '2017-08-04 00:00:00', 'reference': None, 'removed_at': None,
                        'fk_user_id_author': 1007, 'description': 'some hospitals', 'is_published': False, 'id': 1005,
                        'name': 'Hospitals between 1800 to 1950'
                    },
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
                    'properties': {
                        'fk_user_id_published_by': 1001, 'source_author_name': '', 'table_name': '_1001_layer_1001',
                        'created_at': '2017-01-01 00:00:00', 'reference': [{'description': 'book1', 'id': 1001},
                                                                           {'description': 'article2', 'id': 1002}],
                        'removed_at': None, 'fk_user_id_author': 1001, 'description': '', 'is_published': True,
                        'id': 1001, 'name': 'Addresses in 1869'
                    },
                    'type': 'Layer'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, layer_id="1001")

    def test_get_api_layer_return_layer_by_user_id_author(self):
        expected = {
            'features': [
                {
                    'properties': {
                        'fk_user_id_published_by': 1003, 'source_author_name': '', 'table_name': '_1003_layer_1002',
                        'created_at': '2017-03-05 00:00:00', 'reference': [{'description': 'http://link_to_document',
                                                                            'id': 1005}],
                        'removed_at': None, 'fk_user_id_author': 1003, 'description': '', 'is_published': True,
                        'id': 1002, 'name': 'Robberies between 1880 to 1900'
                    },
                    'type': 'Layer'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, user_id_author="1003")

    def test_get_api_layer_return_layer_by_is_published(self):
        expected = {
            'features': [
                {
                    'properties': {
                        'id': 1001, 'table_name': '_1001_layer_1001', 'source_author_name': '', 'reference': [{'id': 1001, 'description': 'book1'},
                                                                                                        {'id': 1002, 'description': 'article2'}],
                        'description': '', 'fk_user_id_author': 1001, 'name': 'Addresses in 1869', 'removed_at': None,
                        'created_at': '2017-01-01 00:00:00', 'is_published': True, 'fk_user_id_published_by': 1001,
                    },
                    'type': 'Layer'
                },
                {
                    'properties': {
                        'id': 1002, 'table_name': '_1003_layer_1002', 'source_author_name': '', 'reference': [{'id': 1005, 'description': 'http://link_to_document'}],
                        'description': '', 'fk_user_id_author': 1003, 'name': 'Robberies between 1880 to 1900',
                        'created_at': '2017-03-05 00:00:00', 'is_published': True, 'fk_user_id_published_by': 1003,
                        'removed_at': None
                    },
                    'type': 'Layer'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, is_published="TRUE")

        expected = {
            'features': [
                {
                    'type': 'Layer',
                    'properties': {
                        'removed_at': None, 'fk_user_id_published_by': None, 'reference': [{'description': 'http://link_to_document', 'id': 1010}],
                        'description': '', 'id': 1003, 'source_author_name': '', 'fk_user_id_author': 1005,
                        'is_published': False, 'created_at': '2017-04-10 00:00:00', 'table_name': '_1005_layer_1003',
                        'name': 'Streets in 1930'
                    }
                },
                {
                    'type': 'Layer',
                    'properties': {
                        'removed_at': None, 'fk_user_id_published_by': None, 'reference': None, 'description': 'some hospitals',
                        'id': 1005, 'source_author_name': None, 'fk_user_id_author': 1007, 'is_published': False,
                        'created_at': '2017-08-04 00:00:00', 'table_name': '_1007_layer_1005',
                        'name': 'Hospitals between 1800 to 1950'
                    }
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, is_published="FALSE")

    def test_get_api_layer_return_layer_by_table_name(self):
        expected = {
            'features': [
                {
                    'properties': {
                        'fk_user_id_published_by': None, 'source_author_name': '', 'table_name': '_1005_layer_1003',
                        'created_at': '2017-04-10 00:00:00', 'reference': [{'description': 'http://link_to_document',
                                                                            'id': 1010}],
                        'removed_at': None, 'fk_user_id_author': 1005, 'description': '',
                        'is_published': False, 'id': 1003, 'name': 'Streets in 1930'
                    },
                    'type': 'Layer'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, table_name="_1005_layer_1003")

    # layer - create and delete

    def test_get_api_layer_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login_fake()

        user_session = self.tester.get_session_user()
        user_id = user_session["user"]["properties"]["id"]

        # create the standard to save the table_name ( _<user_id>_<table_name> )
        table_name = "_" + str(user_id) + "_new_layer"

        # create a layer
        resource = {
            'type': 'Layer',
            'properties': {'name': 'Addresses in 1930', 'table_name': table_name, 'reference': [],
                           'description': '', 'fk_theme_id': 1041},
            'feature_table': {
                'properties': {'name': 'text', 'start_date': 'text', 'end_date': 'text'},
                'geometry': {"type": "MultiPoint"}
            }
        }
        resource = self.tester.api_layer_create(resource)

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
