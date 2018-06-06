#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

"""
class TestAPICurator(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # curator - get

    def test_get_api_curator_return_all_curators(self):
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

        self.tester.api_curator(expected)

    
    def test_get_api_curator_return_user_layer_by_layer_id(self):
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

    def test_get_api_curator_return_user_layer_by_user_id(self):
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

    def test_get_api_curator_return_user_layer_by_user_id_and_layer_id(self):
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

    def test_get_api_curator_return_all_user_layer_by_user_id_and_is_the_creator(self):
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

    def test_api_curator_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # create a layer
        layer = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': 'new_layer', 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [1050], 'keyword': [1041]},
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
"""

"""
class TestAPIUserCuratorErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # layer errors - get

    def test_get_api_user_layer_error_400_bad_request(self):
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

    def test_get_api_user_layer_error_404_not_found(self):
        self.tester.api_user_layer_error_404_not_found(layer_id="999")
        self.tester.api_user_layer_error_404_not_found(layer_id="998")

        self.tester.api_user_layer_error_404_not_found(user_id="999")
        self.tester.api_user_layer_error_404_not_found(user_id="998")

    # layer errors - create

    def test_put_api_user_layer_create_error_400_bad_request_attribute_already_exist(self):
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

        ##################################################
        # main test
        ##################################################

        # add a user in a layer
        user_layer = {
            'properties': {'is_the_creator': True, 'user_id': 1004, 'layer_id': layer_id},
            'type': 'UserLayer'
        }
        self.tester.api_user_layer_create(user_layer)

        ##################################################
        # try to add the user in layer again and raise an error
        ##################################################
        self.tester.api_user_layer_create_error_400_bad_request(user_layer)

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

    def test_put_api_user_layer_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
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

        ##################################################
        # main test
        ##################################################

        # try to add a user in a layer (without is_the_creator)
        user_layer = {
            'properties': {'user_id': 1004, 'layer_id': layer_id},
            'type': 'UserLayer'
        }
        # try to add the user in layer again and raise an error
        self.tester.api_user_layer_create_error_400_bad_request(user_layer)

        # try to add a user in a layer (without user_id)
        user_layer = {
            'properties': {'is_the_creator': True, 'layer_id': layer_id},
            'type': 'UserLayer'
        }
        # try to add the user in layer again and raise an error
        self.tester.api_user_layer_create_error_400_bad_request(user_layer)

        # try to add a user in a layer (without layer_id)
        user_layer = {
            'properties': {'is_the_creator': True, 'user_id': 1004},
            'type': 'UserLayer'
        }
        # try to add the user in layer again and raise an error
        self.tester.api_user_layer_create_error_400_bad_request(user_layer)

        ##################################################

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(layer_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_layer_error_404_not_found(layer_id=layer_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_user_layer_create_error_401_unauthorized_without_authorization_header(self):
        resource = {
            'properties': {'is_the_creator': True, 'user_id': 1004, 'layer_id': 1001},
            'type': 'UserLayer'
        }
        self.tester.api_user_layer_create_error_401_unauthorized_without_authorization_header(resource)

    def test_put_api_user_layer_create_error_403_forbidden_invalid_user_tries_to_add_user_in_layer(self):
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

        # logout with rodrigo
        self.tester.auth_logout()

        # login with other user (admin) and he tries to add a user in the layer of rodrigo
        self.tester.auth_login("admin@admin.com", "admin")

        ##################################################
        # main test
        ##################################################

        # add a user in a layer
        user_layer = {
            'properties': {'is_the_creator': True, 'user_id': 1004, 'layer_id': layer_id},
            'type': 'UserLayer'
        }
        self.tester.api_user_layer_create_error_403_forbidden_invalid_user_tries_to_add_user_in_layer(user_layer)

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
