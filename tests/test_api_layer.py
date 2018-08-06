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
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'description': '', 'name': 'Addresses in 1869', 'reference': [1001, 1002],
                                   'layer_id': 1001, 'f_table_name': 'layer_1001', 'source_description': '',
                                   'created_at': '2017-01-01 00:00:00', 'keyword': [1001, 1041]},
                    'type': 'Layer'
                },
                {
                    'properties': {'description': '', 'name': 'Robberies between 1880 to 1900', 'reference': [1005],
                                   'layer_id': 1002, 'f_table_name': 'layer_1002', 'source_description': '',
                                   'created_at': '2017-03-05 00:00:00', 'keyword': [1010]},
                    'type': 'Layer'
                },
                {
                    'properties': {'description': '', 'name': 'Streets in 1930', 'reference': [1010],
                                   'layer_id': 1003, 'f_table_name': 'layer_1003', 'source_description': '',
                                   'created_at': '2017-04-10 00:00:00', 'keyword': [1001, 1040]},
                    'type': 'Layer'
                },
                {
                    'properties': {'description': 'streets', 'name': 'Streets in 1920', 'reference': None, 'layer_id': 1004,
                                   'f_table_name': 'layer_1004', 'source_description': '',
                                   'created_at': '2017-06-15 00:00:00', 'keyword': [1040]},
                    'type': 'Layer'
                },
                {
                    'properties': {'description': 'some hospitals', 'name': 'Hospitals between 1800 to 1950', 'reference': None, 'layer_id': 1005,
                                   'f_table_name': 'layer_1005', 'source_description': None,
                                   'created_at': '2017-08-04 00:00:00', 'keyword': [1023]},
                    'type': 'Layer'
                },
                {
                    'properties': {'description': '', 'name': 'Cinemas between 1900 to 1950', 'reference': [1025],
                                   'layer_id': 1006, 'f_table_name': 'layer_1006', 'source_description': None,
                                   'created_at': '2017-09-04 00:00:00', 'keyword': [1031]},
                    'type': 'Layer'
                }
            ]
        }

        self.tester.api_layer(expected)

    def test_get_api_layer_return_layer_by_layer_id(self):
        expected = {
            'features': [
                {
                    'properties': {'description': '', 'name': 'Addresses in 1869', 'reference': [1001, 1002],
                                   'layer_id': 1001, 'f_table_name': 'layer_1001', 'source_description': '',
                                   'created_at': '2017-01-01 00:00:00', 'keyword': [1001, 1041]},
                    'type': 'Layer'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, layer_id="1001")

    def test_get_api_layer_return_layer_by_f_table_name(self):
        expected = {
            'features': [
                {
                    'properties': {'description': '', 'name': 'Streets in 1930', 'reference': [1010],
                                   'layer_id': 1003, 'f_table_name': 'layer_1003', 'source_description': '',
                                   'created_at': '2017-04-10 00:00:00', 'keyword': [1001, 1040]},
                    'type': 'Layer'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer(expected, f_table_name="1003")

    def test_get_api_layer_return_layer_by_keyword_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'description': '', 'name': 'Addresses in 1869', 'reference': [1001, 1002],
                                   'layer_id': 1001, 'f_table_name': 'layer_1001', 'source_description': '',
                                   'created_at': '2017-01-01 00:00:00', 'keyword': [1001, 1041]},
                    'type': 'Layer'
                },
                {
                    'properties': {'description': '', 'name': 'Streets in 1930', 'reference': [1010],
                                   'layer_id': 1003, 'f_table_name': 'layer_1003', 'source_description': '',
                                   'created_at': '2017-04-10 00:00:00', 'keyword': [1001, 1040]},
                    'type': 'Layer'
                }
            ]
        }

        self.tester.api_layer(expected, keyword_id="1001")

    # layer - create, update and delete

    def test_api_layer_create_update_and_delete(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create a layer
        ##################################################
        resource = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': 'addresses_1930', 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [1050, 1052], 'keyword': [1001, 1041]}
        }
        resource = self.tester.api_layer_create(resource)

        ##################################################
        # update the layer
        ##################################################
        resource["properties"]["name"] = "Some addresses"
        resource["properties"]["description"] = "Addresses"
        self.tester.api_layer_update(resource)

        ##################################################
        # verify if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_layer(expected_at_least=expected_resource, layer_id=resource["properties"]["layer_id"])

        ##################################################
        # delete the layer
        ##################################################
        # get the id of layer to SEARCH AND REMOVE it
        resource_id = resource["properties"]["layer_id"]

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(resource_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_layer_error_404_not_found(layer_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_api_layer_create_but_update_and_delete_with_admin(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930'

        ##################################################
        # create a layer
        ##################################################
        resource = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': f_table_name, 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [1050, 1052], 'keyword': [1001, 1041]}
        }
        resource = self.tester.api_layer_create(resource)

        # update and delete with admin user
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # update the layer
        ##################################################
        resource["properties"]["name"] = "Some addresses"
        resource["properties"]["description"] = "Addresses"
        self.tester.api_layer_update(resource)

        ##################################################
        # verify if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_layer(expected_at_least=expected_resource, layer_id=resource["properties"]["layer_id"])

        ##################################################
        # delete the layer
        ##################################################
        # get the id of layer to SEARCH AND REMOVE it
        resource_id = resource["properties"]["layer_id"]

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

    def test_post_api_layer_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer (without f_table_name)
        resource = {
            'properties': {'description': '', 'name': 'Addresses in 1869', 'reference': [1001, 1002],
                           'source_description': '', 'keyword': [1001, 1041]},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # try to create a layer (without name)
        resource = {
            'properties': {'description': '', 'reference': [1001, 1002],
                           'f_table_name': 'address', 'source_description': '', 'keyword': [1001, 1041]},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # try to create a layer (without description)
        resource = {
            'properties': {'name': 'Addresses in 1869', 'reference': [1001, 1002],
                           'f_table_name': 'address', 'source_description': '', 'keyword': [1001, 1041]},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # try to create a layer (without source_description)
        resource = {
            'properties': {'description': '', 'name': 'Addresses in 1869', 'reference': [1001, 1002],
                           'f_table_name': 'address', 'keyword': [1001, 1041]},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # try to create a layer (without reference)
        resource = {
            'properties': {'description': '', 'name': 'Addresses in 1869',
                           'f_table_name': 'address', 'source_description': '', 'keyword': [1001, 1041]},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # try to create a layer (without keyword)
        resource = {
            'properties': {'description': '', 'name': 'Addresses in 1869', 'reference': [1001, 1002],
                           'f_table_name': 'address', 'source_description': ''},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_layer_create_error_401_unauthorized(self):
        feature = {
            'properties': {'name': 'Addresses in 1869', 'table_name': 'new_layer', 'source': '',
                           'description': '', 'fk_keyword_id': 1041},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_401_unauthorized(feature)

    def test_post_api_layer_create_error_409_conflict(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to create a layer with f_table_name of a table that already exist
        resource = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': 'reference', 'name': '',
                           'description': '', 'source_description': '',
                           'reference': [], 'keyword': []}
        }
        self.tester.api_layer_create_error_409_conflict(resource)

        # try to create a layer with f_table_name of a table that already exist
        resource = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': 'changeset', 'name': '',
                           'description': '', 'source_description': '',
                           'reference': [], 'keyword': []}
        }
        self.tester.api_layer_create_error_409_conflict(resource)

        # try to create a layer with f_table_name of a table that already exist
        resource = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': 'spatial_ref_sys', 'name': '',
                           'description': '', 'source_description': '',
                           'reference': [], 'keyword': []}
        }
        self.tester.api_layer_create_error_409_conflict(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # layer errors - update

    def test_put_api_layer_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to update a layer (without layer_id)
        resource = {
            'properties': {'f_table_name': 'layer_1003', 'name': 'Streets in 1930',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'reference': [1010], 'keyword': [1001, 1040]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # try to update a layer (without name)
        resource = {
            'properties': {'layer_id': 1003, 'f_table_name': 'layer_1003',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'reference': [1010], 'keyword': [1001, 1040]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # try to update a layer (without description)
        resource = {
            'properties': {'layer_id': 1003, 'f_table_name': 'layer_1003', 'name': 'Streets in 1930',
                           'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'reference': [1010], 'keyword': [1001, 1040]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # try to update a layer (without source_description)
        resource = {
            'properties': {'layer_id': 1003, 'f_table_name': 'layer_1003', 'name': 'Streets in 1930',
                           'description': '', 'created_at': '2017-04-10 00:00:00',
                           'reference': [1010], 'keyword': [1001, 1040]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # try to update a layer (without reference)
        resource = {
            'properties': {'layer_id': 1003, 'f_table_name': 'layer_1003', 'name': 'Streets in 1930',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'keyword': [1001, 1040]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # try to update a layer (without keyword)
        resource = {
            'properties': {'layer_id': 1003, 'f_table_name': 'layer_1003', 'name': 'Streets in 1930',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'reference': [1010]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_layer_error_401_unauthorized_user_is_not_logged(self):
        feature = {
            'properties': {'reference_id': 1001, 'description': 'BookA'},
            'type': 'Reference'
        }
        self.tester.api_layer_update_error_401_unauthorized(feature)

    def test_put_api_layer_error_403_forbidden_invalid_user_tries_to_manage(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # gabriel tries to update one reference that doesn't belong to him
        ##################################################
        resource = {
            'properties': {'layer_id': 1001, 'f_table_name': 'layer_1001', 'name': 'Streets in 1930',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'reference': [1010], 'keyword': [1001, 1040]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_403_forbidden(resource)

        # DO LOGOUT
        self.tester.auth_logout()

    def test_put_api_layer_error_404_not_found(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        resource = {
            'properties': {'layer_id': 999, 'f_table_name': 'layer_1006', 'name': 'Streets in 1930',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'reference': [1010], 'keyword': [1001, 1040]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_404_not_found(resource)

        # DO LOGOUT
        self.tester.auth_logout()

    # layer errors - delete

    def test_delete_api_layer_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_layer_delete_error_400_bad_request("abc")
        self.tester.api_layer_delete_error_400_bad_request(0)
        self.tester.api_layer_delete_error_400_bad_request(-1)
        self.tester.api_layer_delete_error_400_bad_request("-1")
        self.tester.api_layer_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_layer_error_401_unauthorized_user_without_login(self):
        self.tester.api_layer_delete_error_401_unauthorized("abc")
        self.tester.api_layer_delete_error_401_unauthorized(0)
        self.tester.api_layer_delete_error_401_unauthorized(-1)
        self.tester.api_layer_delete_error_401_unauthorized("-1")
        self.tester.api_layer_delete_error_401_unauthorized("0")
        self.tester.api_layer_delete_error_401_unauthorized("1001")

    def test_delete_api_layer_error_403_forbidden_user_forbidden_to_delete(self):
        self.tester.auth_login("miguel@admin.com", "miguel")

        ########################################
        # try to delete a layer with user miguel
        ########################################

        # TRY TO REMOVE THE LAYER
        self.tester.api_layer_delete_error_403_forbidden(1001)

        # logout with user rodrigo
        self.tester.auth_logout()

    def test_delete_api_layer_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_layer_delete_error_404_not_found("5000")
        self.tester.api_layer_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
