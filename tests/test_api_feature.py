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

    def test_get_api_feature_return_all_features_by_f_table_name(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'end_date': '1869-12-31T00:00:00', 'version': 1, 'address': 'R. São José',
                                   'id': 1001, 'start_date': '1869-01-01T00:00:00', 'changeset_id': 1001},
                    'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
                    'type': 'Feature'
                },
                {
                    'properties': {'end_date': '1869-12-31T00:00:00', 'version': 1, 'address': 'R. Marechal Deodoro',
                                   'id': 1002, 'start_date': '1869-01-01T00:00:00', 'changeset_id': 1001},
                    'geometry': {'coordinates': [[-46.6498716962487, -23.5482894062877]], 'type': 'MultiPoint'},
                    'type': 'Feature'
                },
                {
                    'properties': {'end_date': '1875-12-31T00:00:00', 'version': 1, 'address': None, 'id': 1003,
                                   'start_date': '1875-01-01T00:00:00', 'changeset_id': 1001},
                    'geometry': {'coordinates': [[-46.6468896156385, -23.5494865576549]], 'type': 'MultiPoint'},
                    'type': 'Feature'
                }
            ]
        }

        self.tester.api_feature(expected, f_table_name="layer_1001")

    def test_get_api_feature_return_all_features_by_f_table_name_and_feature_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'end_date': '1869-12-31T00:00:00', 'version': 1, 'address': 'R. São José',
                                   'id': 1001, 'start_date': '1869-01-01T00:00:00', 'changeset_id': 1001},
                    'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
                    'type': 'Feature'
                }
            ]
        }

        self.tester.api_feature(expected, f_table_name="layer_1001", feature_id="1001")

    # feature - create, update and delete

    def test_api_feature_create_update_and_delete(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        ####################################################################################################
        # create a changeset to create a feature
        ##################################################

        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1003, 'description': 'Inserting feature in layer_1003'},
            'type': 'Changeset'
        }
        changeset = self.tester.api_changeset_create(changeset)
        changeset_id = changeset["properties"]["changeset_id"]

        ##################################################
        # create a feature with user miguel
        ##################################################

        f_table_name = "layer_1002"

        feature = {
            'f_table_name': f_table_name,
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': changeset_id},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        feature = self.tester.api_feature_create(feature)

        ####################################################################################################
        # update the feature with admin
        ##################################################
        # resource["properties"]["parent_id"] = 1005
        # self.tester.api_feature_update(resource)

        ##################################################
        # verify if the resource was modified
        ##################################################
        # expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        # self.tester.api_feature(expected_at_least=expected_resource, feature_id=resource["properties"]["feature_id"])

        ##################################################
        # remove the feature
        ##################################################
        # get the id of the feature to REMOVE it
        feature_id = feature["properties"]["id"]

        # remove the resource
        self.tester.api_feature_delete(f_table_name=f_table_name, feature_id=feature_id, changeset_id=changeset_id)

        # it is not possible to find the resource that just deleted
        self.tester.api_feature_error_404_not_found(f_table_name=f_table_name, feature_id=feature_id)

        # CLOSE THE CHANGESET
        self.tester.api_changeset_close(changeset_id=changeset_id)

        ####################################################################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        ####################################################################################################

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIFeatureFeature(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # feature errors - get

    def test_get_api_feature_error_400_bad_request(self):
        self.tester.api_feature_error_400_bad_request(f_table_name="layer_1001", feature_id="abc")
        self.tester.api_feature_error_400_bad_request(f_table_name="layer_1001", feature_id=0)
        self.tester.api_feature_error_400_bad_request(f_table_name="layer_1001", feature_id=-1)
        self.tester.api_feature_error_400_bad_request(f_table_name="layer_1001", feature_id="-1")
        self.tester.api_feature_error_400_bad_request(f_table_name="layer_1001", feature_id="0")

        self.tester.api_feature_error_400_bad_request(feature_id="abc")
        self.tester.api_feature_error_400_bad_request(feature_id=0)
        self.tester.api_feature_error_400_bad_request(feature_id=-1)
        self.tester.api_feature_error_400_bad_request(feature_id="-1")
        self.tester.api_feature_error_400_bad_request(feature_id="0")

    def test_get_api_feature_error_404_not_found(self):
        self.tester.api_feature_error_404_not_found(f_table_name="layer_1001", feature_id="999")
        self.tester.api_feature_error_404_not_found(f_table_name="layer_1001", feature_id="998")

        self.tester.api_feature_error_404_not_found(f_table_name="layer_999")
        self.tester.api_feature_error_404_not_found(f_table_name="layer_998")

    # feature errors - create

    def test_post_api_feature_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        # try to create a layer (without f_table_name)
        resource = {
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1002},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # try to create a layer (without properties)
        resource = {
            'f_table_name': 'layer_1002',
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # try to create a layer (without geometry)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1002},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # try to create a layer (without start_date)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1002},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # try to create a layer (without address)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'changeset_id': 1002},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # try to create a layer (without changeset_id)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José'},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_create_error_401_unauthorized_user_is_not_logged(self):
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1001},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_401_unauthorized(resource)
    """
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
