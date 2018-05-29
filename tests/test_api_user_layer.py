#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase, skip
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPIUserLayer(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # user_layer - get

    def test_get_api_user_layer_return_all_users_in_layers(self):
        expected = {
            'features': [
                {
                    'properties': {'is_the_creator': True, 'user_id': 1001, 'layer_id': 1001,
                                   'created_at': '2017-01-02 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': False, 'user_id': 1002, 'layer_id': 1001,
                                   'created_at': '2017-01-03 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': True, 'user_id': 1001, 'layer_id': 1002,
                                   'created_at': '2017-03-05 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': False, 'user_id': 1004, 'layer_id': 1002,
                                   'created_at': '2017-03-05 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': False, 'user_id': 1001, 'layer_id': 1003,
                                   'created_at': '2017-04-11 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': True, 'user_id': 1005, 'layer_id': 1003,
                                   'created_at': '2017-04-10 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': False, 'user_id': 1006, 'layer_id': 1003,
                                   'created_at': '2017-04-11 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': False, 'user_id': 1007, 'layer_id': 1003,
                                   'created_at': '2017-04-11 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': True, 'user_id': 1005, 'layer_id': 1004,
                                   'created_at': '2017-06-15 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': False, 'user_id': 1007, 'layer_id': 1004,
                                   'created_at': '2017-06-20 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': False, 'user_id': 1008, 'layer_id': 1004,
                                   'created_at': '2017-06-27 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': True, 'user_id': 1007, 'layer_id': 1005,
                                   'created_at': '2017-08-04 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': True, 'user_id': 1007, 'layer_id': 1006,
                                   'created_at': '2017-09-04 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': False, 'user_id': 1008, 'layer_id': 1006,
                                   'created_at': '2017-09-10 00:00:00'},
                    'type': 'UserLayer'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_user_layer(expected)

    def test_get_api_user_layer_return_user_layer_by_layer_id(self):
        expected = {
            'features': [
                {
                    'properties': {'is_the_creator': True, 'user_id': 1001, 'layer_id': 1001,
                                   'created_at': '2017-01-02 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': False, 'user_id': 1002, 'layer_id': 1001,
                                   'created_at': '2017-01-03 00:00:00'},
                    'type': 'UserLayer'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_user_layer(expected, layer_id="1001")

    def test_get_api_user_layer_return_user_layer_by_user_id(self):
        expected = {
            'features': [
                {
                    'properties': {'is_the_creator': True, 'user_id': 1005, 'layer_id': 1003,
                                   'created_at': '2017-04-10 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': True, 'user_id': 1005, 'layer_id': 1004,
                                   'created_at': '2017-06-15 00:00:00'},
                    'type': 'UserLayer'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_user_layer(expected, user_id="1005")

    def test_get_api_user_layer_return_user_layer_by_user_id_and_layer_id(self):
        expected = {
            'features': [
                {
                    'properties': {'is_the_creator': True, 'user_id': 1005, 'layer_id': 1003,
                                   'created_at': '2017-04-10 00:00:00'},
                    'type': 'UserLayer'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_user_layer(expected, user_id="1005", layer_id="1003")

    def test_get_api_user_layer_return_all_user_layer_by_user_id_and_is_the_creator(self):
        expected = {
            'features': [
                {
                    'properties': {'is_the_creator': True, 'user_id': 1001, 'layer_id': 1001,
                                   'created_at': '2017-01-02 00:00:00'},
                    'type': 'UserLayer'
                },
                {
                    'properties': {'is_the_creator': True, 'user_id': 1001, 'layer_id': 1002,
                                   'created_at': '2017-03-05 00:00:00'},
                    'type': 'UserLayer'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_user_layer(expected, user_id="1001", is_the_creator="TRUE")

        expected = {
            'features': [
                {
                    'properties': {'is_the_creator': False, 'user_id': 1001, 'layer_id': 1003,
                                   'created_at': '2017-04-11 00:00:00'},
                    'type': 'UserLayer'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_user_layer(expected, user_id="1001", is_the_creator="FALSE")

    # layer - create and delete

    def test_api_user_layer_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # create a layer
        layer = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': 'new_layer', 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [], 'keyword': [{'keyword_id': 1041}]},
            'feature_table': {
                'properties': {'name': 'text', 'start_date': 'text', 'end_date': 'text'},
                'geometry': {"type": "MultiPoint"}
            }
        }
        layer = self.tester.api_layer_create(layer)

        # get the id of layer to use in test and after the testes, remove it
        layer_id = layer["properties"]["layer_id"]

        ##################################################
        # main test
        ##################################################

        # add a user in a layer
        user_layer = {
            'properties': {'is_the_creator': True, 'user_id': 1004, 'layer_id': layer_id},
            'type': 'UserLayer'
        }
        self.tester.api_user_layer_create(user_layer)

        # get the id of layer to REMOVE it
        user_id = user_layer["properties"]["user_id"]

        # remove the user in layer
        self.tester.api_user_layer_delete(user_id=user_id, layer_id=layer_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_user_layer_error_404_not_found(user_id=user_id, layer_id=layer_id)

        ##################################################

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(layer_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_layer_error_404_not_found(layer_id=layer_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIUserLayerErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # layer errors - get

    def test_get_api_layer_error_400_bad_request(self):
        self.tester.api_user_layer_error_400_bad_request(layer_id="abc")
        self.tester.api_user_layer_error_400_bad_request(layer_id=0)
        self.tester.api_user_layer_error_400_bad_request(layer_id=-1)
        self.tester.api_user_layer_error_400_bad_request(layer_id="-1")
        self.tester.api_user_layer_error_400_bad_request(layer_id="0")

        self.tester.api_user_layer_error_400_bad_request(user_id="abc")
        self.tester.api_user_layer_error_400_bad_request(user_id=0)
        self.tester.api_user_layer_error_400_bad_request(user_id=-1)
        self.tester.api_user_layer_error_400_bad_request(user_id="-1")
        self.tester.api_user_layer_error_400_bad_request(user_id="0")

        self.tester.api_user_layer_error_400_bad_request(is_the_creator="abc")
        self.tester.api_user_layer_error_400_bad_request(is_the_creator=0)
        self.tester.api_user_layer_error_400_bad_request(is_the_creator=-1)
        self.tester.api_user_layer_error_400_bad_request(is_the_creator="0")
        self.tester.api_user_layer_error_400_bad_request(is_the_creator="-1")

    def test_get_api_layer_error_404_not_found(self):
        self.tester.api_user_layer_error_404_not_found(layer_id="999")
        self.tester.api_user_layer_error_404_not_found(layer_id="998")

        self.tester.api_user_layer_error_404_not_found(user_id="999")
        self.tester.api_user_layer_error_404_not_found(user_id="998")


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
