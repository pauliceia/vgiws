#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/


class TestAPICurator(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # curator - get
    
    def test_get_api_curator_return_all_curators(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'created_at': '2018-01-01 00:00:00', 'keyword_id': 1001,
                                   'user_id': 1001, 'region': 'Amaro'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1001, 'region': 'Azure'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1002, 'region': 'Belondres'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-02-22 00:00:00', 'keyword_id': 1010,
                                   'user_id': 1003, 'region': 'Jorge'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-15 00:00:00', 'keyword_id': 1020,
                                   'user_id': 1003, 'region': 'Centro'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-02-20 00:00:00', 'keyword_id': 1003,
                                   'user_id': 1004, 'region': 'São Francisco'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-02-22 00:00:00', 'keyword_id': 1010,
                                   'user_id': 1005, 'region': 'São Bento'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-03-24 00:00:00', 'keyword_id': 1021,
                                   'user_id': 1006, 'region': 'Avenida Rodônia'},
                    'type': 'Curator'
                }
            ]
        }

        self.tester.api_curator(expected)

    def test_get_api_curator_return_curator_by_user_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'created_at': '2018-02-22 00:00:00', 'keyword_id': 1010,
                                   'user_id': 1003, 'region': 'Jorge'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-15 00:00:00', 'keyword_id': 1020,
                                   'user_id': 1003, 'region': 'Centro'},
                    'type': 'Curator'
                }
            ]
        }

        self.tester.api_curator(expected, user_id="1003")

    def test_get_api_curator_return_curator_by_keyword_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1001, 'region': 'Azure'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1002, 'region': 'Belondres'},
                    'type': 'Curator'
                }
            ]
        }

        self.tester.api_curator(expected, keyword_id="1002")

    def test_get_api_curator_return_curator_by_region(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'created_at': '2018-02-20 00:00:00', 'keyword_id': 1003,
                                   'user_id': 1004, 'region': 'São Francisco'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-02-22 00:00:00', 'keyword_id': 1010,
                                   'user_id': 1005, 'region': 'São Bento'},
                    'type': 'Curator'
                }
            ]
        }

        self.tester.api_curator(expected, region="SÃo")

    def test_get_api_curator_return_curator_by_user_id_and_keyword_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1002, 'region': 'Belondres'},
                    'type': 'Curator'
                }
            ]
        }

        self.tester.api_curator(expected, user_id="1002", keyword_id="1002")
    
    # layer - create and delete

    def test_api_curator_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # add a user in a layer
        resource = {
            'properties': {'user_id': 1002, 'keyword_id': 1003, 'region': 'Jorge'},
            'type': 'Curator'
        }
        self.tester.api_curator_create(resource)

        # get the id of layer to REMOVE it
        user_id = resource["properties"]["user_id"]
        keyword_id = resource["properties"]["keyword_id"]

        # remove the user in layer
        self.tester.api_curator_delete(user_id=user_id, keyword_id=keyword_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_curator_error_404_not_found(user_id=user_id, keyword_id=keyword_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIUserCuratorErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # layer errors - get

    def test_get_api_user_layer_error_400_bad_request(self):
        self.tester.api_curator_error_400_bad_request(keyword_id="abc")
        self.tester.api_curator_error_400_bad_request(keyword_id=0)
        self.tester.api_curator_error_400_bad_request(keyword_id=-1)
        self.tester.api_curator_error_400_bad_request(keyword_id="-1")
        self.tester.api_curator_error_400_bad_request(keyword_id="0")

        self.tester.api_curator_error_400_bad_request(user_id="abc")
        self.tester.api_curator_error_400_bad_request(user_id=0)
        self.tester.api_curator_error_400_bad_request(user_id=-1)
        self.tester.api_curator_error_400_bad_request(user_id="-1")
        self.tester.api_curator_error_400_bad_request(user_id="0")

    def test_get_api_user_layer_error_404_not_found(self):
        self.tester.api_curator_error_404_not_found(keyword_id="999")
        self.tester.api_curator_error_404_not_found(keyword_id="998")

        self.tester.api_curator_error_404_not_found(user_id="999")
        self.tester.api_curator_error_404_not_found(user_id="998")
    
    # layer errors - create

    def test_put_api_user_layer_create_error_400_bad_request_attribute_already_exist(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to insert a curator with user_id and keyword_id that already exist
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'Joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
    
    def test_put_api_user_layer_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a curator (without user_id)
        resource = {
            'properties': {'keyword_id': 1010, 'region': 'Joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_create_error_400_bad_request(resource)

        # try to create a curator (without keyword_id)
        resource = {
            'properties': {'keyword_id': 1010, 'region': 'Joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_create_error_400_bad_request(resource)

        # try to create a curator (without region)
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010},
            'type': 'Curator'
        }
        self.tester.api_curator_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
    
    def test_put_api_user_layer_create_error_401_unauthorized_without_authorization_header(self):
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'Joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_create_error_401_unauthorized(resource)

    def test_put_api_user_layer_create_error_403_forbidden_invalid_user_tries_to_create_a_curator(self):
        # DO LOGIN
        self.tester.auth_login("gabriel@admin.com", "gabriel")

        # add a user in a layer
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'Joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_create_error_403_forbidden(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    """
    # layer errors - delete

    def test_delete_api_user_layer_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_user_layer_delete_error_400_bad_request(user_id="abc", layer_id="abc")
        self.tester.api_user_layer_delete_error_400_bad_request(user_id=0, layer_id=0)
        self.tester.api_user_layer_delete_error_400_bad_request(user_id=-1, layer_id=-1)
        self.tester.api_user_layer_delete_error_400_bad_request(user_id="-1", layer_id="-1")
        self.tester.api_user_layer_delete_error_400_bad_request(user_id="0", layer_id="0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_user_layer_error_401_unauthorized_user_without_login(self):
        self.tester.api_user_layer_delete_error_401_unauthorized(user_id=1001, layer_id=1001)
        self.tester.api_user_layer_delete_error_401_unauthorized(user_id=1001, layer_id="1001")
        self.tester.api_user_layer_delete_error_401_unauthorized(user_id=0, layer_id=-1)
        self.tester.api_user_layer_delete_error_401_unauthorized(user_id="0", layer_id="-1")

    def test_delete_api_user_layer_error_403_forbidden_user_forbidden_to_delete_user_in_layer(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # create a layer
        layer = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': 'new_layer', 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [], 'keyword': [1041]},
            'feature_table': {
                'properties': {'name': 'text', 'start_date': 'text', 'end_date': 'text'},
                'geometry': {"type": "MultiPoint"}
            }
        }
        layer = self.tester.api_layer_create(layer)

        # get the id of layer to use in test and after the testes, remove it
        layer_id = layer["properties"]["layer_id"]

        # add a user in a layer
        user_layer = {
            'properties': {'is_the_creator': True, 'user_id': 1004, 'layer_id': layer_id},
            'type': 'UserLayer'
        }
        self.tester.api_user_layer_create(user_layer)

        # get the id of layer to REMOVE it
        user_id = user_layer["properties"]["user_id"]

        # logout with rodrigo
        self.tester.auth_logout()

        ##################################################
        # main test
        ##################################################

        # login with other user (admin) and he tries to delete a user from a layer of rodrigo
        self.tester.auth_login("admin@admin.com", "admin")

        # try to remove the user in layer
        self.tester.api_user_layer_delete_error_403_forbidden(user_id=user_id, layer_id=layer_id)

        ##################################################

        # logout with admin
        self.tester.auth_logout()

        # login with rodrigo to delete the layer
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(layer_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_layer_error_404_not_found(layer_id=layer_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_user_layer_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_user_layer_delete_error_404_not_found(user_id=1001, layer_id=5000)
        self.tester.api_user_layer_delete_error_404_not_found(user_id=1001, layer_id=5001)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
    """
# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
