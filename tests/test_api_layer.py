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

    def test_get_api_layer_return_zero_resources(self):
        expected = {'type': 'FeatureCollection', 'features': []}

        self.tester.api_layer(expected, layer_id="999")
        self.tester.api_layer(expected, layer_id="998")

    # layer - create, update and delete

    def test_api_layer_create_update_and_delete(self):
        ##################################################
        # log in with a normal user
        ##################################################
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # get creator user id
        ##################################################
        user = self.tester.function_api_user_by_token()
        creator_user_id = user["properties"]["user_id"]

        ##################################################
        # create a layer with a normal user
        ##################################################
        resource = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': 'addresses_1930', 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [1050, 1052], 'keyword': [1001, 1041]}
        }
        resource = self.tester.api_layer_create(resource)

        # get the layer id
        resource_id = resource["properties"]["layer_id"]

        ##################################################
        # creator user updates the layer
        ##################################################
        resource["properties"]["name"] = "Some addresses"
        resource["properties"]["description"] = "Addresses"
        self.tester.api_layer_update(resource)

        # check if the resource was modified
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_layer(expected_at_least=expected_resource, layer_id=resource_id)

        ##################################################
        # add a collaborator
        ##################################################
        user_id_collaborator = 1004

        user_layer = {
            'properties': {'user_id': user_id_collaborator, 'layer_id': resource_id},
            'type': 'UserLayer'
        }
        self.tester.api_user_layer_create(user_layer)

        ##################################################
        # check if the creator and collaborator users have started to follow the created layer automatically
        ##################################################
        # creator user
        expected_at_least = {
            'features': [
                {
                    'properties': {'layer_id': resource_id, 'user_id': creator_user_id},
                    'type': 'LayerFollower'
                },
            ],
            'type': 'FeatureCollection'
        }
        self.tester.api_layer_follower(expected_at_least=expected_at_least,
                                       user_id=creator_user_id, layer_id=resource_id)

        # collaborator user
        expected_at_least = {
            'features': [
                {
                    'properties': {'layer_id': resource_id, 'user_id': user_id_collaborator},
                    'type': 'LayerFollower'
                },
            ],
            'type': 'FeatureCollection'
        }
        self.tester.api_layer_follower(expected_at_least=expected_at_least,
                                       user_id=user_id_collaborator, layer_id=resource_id)

        ##################################################
        # check if the collaborator user can update the layer, but he can not delete it
        ##################################################
        # log in with the collaborator user
        self.tester.auth_logout()
        self.tester.auth_login("rafael@admin.com", "rafael")

        # collaborator user updates the layer
        resource["properties"]["name"] = "New addresses"
        resource["properties"]["description"] = "New addresses"
        self.tester.api_layer_update(resource)

        # collaborator user tries to delete the layer, but a 403 error is raised
        self.tester.api_layer_delete_error_403_forbidden(resource_id)

        ##################################################
        # delete the layer in the final with the creator user
        ##################################################
        # log in the creator user again
        self.tester.auth_logout()
        self.tester.auth_login("miguel@admin.com", "miguel")

        self.tester.api_layer_delete(resource_id)

        ##################################################
        # final validations
        ##################################################

        # finding the layer that just deleted is not possible
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_layer(expected, layer_id=resource_id)

        # finding a user in a layer that just deleted (creator user) is not possible
        expected = {'features': [], 'type': 'FeatureCollection'}
        self.tester.api_user_layer(expected, user_id=creator_user_id, layer_id=resource_id)

        # check if the creator user stopped automatically of following the layer
        expected = {'features': [], 'type': 'FeatureCollection'}
        self.tester.api_layer_follower(expected, user_id=creator_user_id, layer_id=resource_id)

        # finding a user in a layer that just deleted (collaborator user) is not possible
        expected = {'features': [], 'type': 'FeatureCollection'}
        self.tester.api_user_layer(expected, user_id=user_id_collaborator, layer_id=resource_id)

        # check if the collaborator user has stopped automatically of following the layer
        expected = {'features': [], 'type': 'FeatureCollection'}
        self.tester.api_layer_follower(expected, user_id=user_id_collaborator, layer_id=resource_id)

        ##################################################
        # log out the user after the test case be executed
        ##################################################
        self.tester.auth_logout()

    def test_api_layer_create_but_update_and_delete_with_admin(self):
        # login a normal user
        self.tester.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930'

        ##################################################
        # create a layer with a normal user
        ##################################################
        resource = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': f_table_name, 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [1050, 1052], 'keyword': [1001, 1041]}
        }
        resource = self.tester.api_layer_create(resource)

        # get the layer id
        resource_id = resource["properties"]["layer_id"]

        ##################################################
        # log in with an admin user in order to check if he can update and delete the layer
        ##################################################
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # admin user updates the layer
        ##################################################
        resource["properties"]["name"] = "Some addresses"
        resource["properties"]["description"] = "Addresses"
        self.tester.api_layer_update(resource)

        # check if the resource was modified
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_layer(expected_at_least=expected_resource, layer_id=resource_id)

        ##################################################
        # admin user deletes the layer
        ##################################################
        self.tester.api_layer_delete(resource_id)

        # finding the layer that just deleted is not possible
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_layer(expected, layer_id=resource_id)

        # log out the admin user
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

    def test_post_api_layer_create_error_400_bad_request_f_table_name_has_special_chars_or_it_starts_with_number(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer with invalid f_table_name
        list_invalid_f_table_name = [
            "*)new_layer", "new_lay+-er", "new_layer_(/", "837_new_layer", "0_new_layer",
            " new_layer", "new_layer ", "new layer"
        ]

        for invalid_f_table_name in list_invalid_f_table_name:
            resource = {
                'properties': {'f_table_name': invalid_f_table_name, 'description': '', 'name': 'Addresses in 1869',
                               'reference': [1001, 1002], 'source_description': '', 'keyword': [1001, 1041]},
                'type': 'Layer'
            }
            self.tester.api_layer_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_layer_create_error__400_bad_request__f_table_name_is_less_than_5_chars(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        resource = {
            'properties': {'f_table_name': 'abcd', 'description': '', 'name': 'Addresses in 1869',
                            'reference': [1001, 1002], 'source_description': '', 'keyword': [1001, 1041]},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_layer_create_error__400_bad_request__f_table_name_is_greater_than_63_chars(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        resource = {
            'properties': {'f_table_name': 'lorem_ipsum_dolor_sit_amet_consectetur_adipiscing_elit__sed_do_e',
                            'description': '', 'name': 'Addresses in 1869',
                            'reference': [1001, 1002], 'source_description': '', 'keyword': [1001, 1041]},
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

    def test_post_api_layer_create_error_404_not_found_non_existing_user(self):
        ##################################################
        # fake log in with a non-existing user
        ##################################################
        self.tester.auth_login_non_existing_user()

        ##################################################
        # try to handle the layer with the fake user
        ##################################################
        self.tester.api_layer_create_error_404_not_found({
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': 'addresses_1930', 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [1050, 1052], 'keyword': [1001, 1041]}
        })

        self.tester.auth_logout()

    def test_post_api_layer_create_error_409_conflict_f_table_name_already_exist_or_reserved_name(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to create a layer with f_table_name that table that already exist or with reserved name
        list_invalid_f_table_name = ["reference", "changeset", "spatial_ref_sys", "abort", "access"]

        for invalid_f_table_name in list_invalid_f_table_name:
            resource = {
                'type': 'Layer',
                'properties': {'layer_id': -1, 'f_table_name': invalid_f_table_name, 'name': '',
                               'description': '', 'source_description': '',
                               'reference': [], 'keyword': []}
            }
            self.tester.api_layer_create_error_409_conflict(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_layer_create_error_409_conflict_maximum_of_keywords_are_5(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        resource = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': "new_table", 'name': '',
                           'description': '', 'source_description': '',
                           'reference': [], 'keyword': [1001, 1002, 1003, 1004, 1005, 1006]}
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
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # miguel tries to update one reference that doesn't belong to him
        ##################################################
        resource = {
            'properties': {'layer_id': 1001, 'f_table_name': 'layer_1001', 'name': 'Streets in 1930',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'reference': [1010], 'keyword': [1001, 1040]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_403_forbidden(resource)

        self.tester.auth_logout()

    def test_put_api_layer_error_404_not_found_not_found_layer_x(self):
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

    def test_put_api_layer_error_409_conflict_maximum_of_keywords_are_5(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        resource = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': "new_table", 'name': '',
                           'description': '', 'source_description': '',
                           'reference': [], 'keyword': [1001, 1002, 1003, 1004, 1005, 1006]}
        }
        self.tester.api_layer_update_error_409_conflict(resource)

        # DO LOGOUT AFTER THE TESTS
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
        # miguel tries to delete a layer that does not belong to him
        ########################################
        self.tester.api_layer_delete_error_403_forbidden(1001)

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


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
