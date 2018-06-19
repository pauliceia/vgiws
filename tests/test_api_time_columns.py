#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/


class TestAPITimeColumns(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # time_columns - get
    
    def test_get_api_time_columns_return_all_time_columns(self):
        expected = {
            'features': [
                {
                    'properties': {'start_date': '1870-01-01', 'end_date': '1900-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1001',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
                {
                    'properties': {'start_date': '1890-01-01', 'end_date': '1900-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1002',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
                {
                    'properties': {'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1003',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
                {
                    'properties': {'start_date': '1910-01-01', 'end_date': '1920-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1004',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
                {
                    'properties': {'start_date': '1920-01-01', 'end_date': '1930-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1005',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
                {
                    'properties': {'start_date': '1900-01-01', 'end_date': '1930-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1006',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_time_columns(expected)

    def test_get_api_time_columns_return_time_columns_by_f_table_name(self):
        expected = {
            'features': [
                {
                    'properties': {'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1003',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_time_columns(expected, f_table_name="1003")

    def test_get_api_time_columns_return_time_columns_by_temporal_bounding_box(self):
        expected = {
            'features': [
                {
                    'properties': {'start_date': '1890-01-01', 'end_date': '1900-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1002',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
                {
                    'properties': {'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1003',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
                {
                    'properties': {'start_date': '1910-01-01', 'end_date': '1920-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1004',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_time_columns(expected, start_date_gte='1890-01-01', end_date_lte='1920-12-31')

    def test_get_api_time_columns_return_time_columns_by_start_date_greater_than_or_equal(self):
        expected = {
            'features': [
                {
                    'properties': {'start_date': '1910-01-01', 'end_date': '1920-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1004',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
                {
                    'properties': {'start_date': '1920-01-01', 'end_date': '1930-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1005',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_time_columns(expected, start_date_gte="1910-01-01")

    def test_get_api_time_columns_return_time_columns_by_end_date_less_than_or_equal(self):
        expected = {
            'features': [
                {
                    'properties': {'start_date': '1870-01-01', 'end_date': '1900-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1001',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
                {
                    'properties': {'start_date': '1890-01-01', 'end_date': '1900-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1002',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
                {
                    'properties': {'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1003',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
                {
                    'properties': {'start_date': '1910-01-01', 'end_date': '1920-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1004',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_time_columns(expected, end_date_lte="1920-12-31")

    def test_get_api_time_columns_return_time_columns_by_start_date(self):
        expected = {
            'features': [
                {
                    'properties': {'start_date': '1910-01-01', 'end_date': '1920-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1004',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_time_columns(expected, start_date="1910-01-01")

    def test_get_api_time_columns_return_time_columns_by_end_date(self):
        expected = {
            'features': [
                {
                    'properties': {'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1003',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                },
                {
                    'properties': {'start_date': '1910-01-01', 'end_date': '1920-12-31',
                                   'end_date_column_name': 'end_date', 'f_table_name': 'layer_1004',
                                   'start_date_column_name': 'start_date'},
                    'type': 'TimeColumns'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_time_columns(expected, end_date="1920-12-31")
   
    # time_columns - create, update and delete
    """ 
    def test_api_time_columns_create_update_and_delete(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # create curator
        ##################################################
        resource = {
            'properties': {'user_id': 1002, 'keyword_id': 1003, 'region': 'jorge'},
            'type': 'Curator'
        }
        self.tester.api_curator_create(resource)

        ##################################################
        # update curator
        ##################################################
        resource["properties"]["region"] = "cabral"
        self.tester.api_curator_update(resource)

        ##################################################
        # remove curator
        ##################################################
        # get the id of layer to REMOVE it
        user_id = resource["properties"]["user_id"]
        keyword_id = resource["properties"]["keyword_id"]

        # remove the user in layer
        self.tester.api_curator_delete(user_id=user_id, keyword_id=keyword_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_curator_error_404_not_found(user_id=user_id, keyword_id=keyword_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
    """

class TestAPIUserTimeColumnsErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # time_columns errors - get

    def test_get_api_time_columns_error_400_bad_request_invalid_date_format(self):
        self.tester.api_time_columns_error_400_bad_request(start_date="1910/01-01")
        self.tester.api_time_columns_error_400_bad_request(end_date="1910-01/01")
        self.tester.api_time_columns_error_400_bad_request(start_date_gte="1910/01=01")
        self.tester.api_time_columns_error_400_bad_request(end_date_lte="1910-01)01")
    
    # time_columns errors - create
    """
    def test_post_api_curator_create_error_400_bad_request_attribute_already_exist(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to insert a curator with user_id and keyword_id that already exist
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
    
    def test_post_api_curator_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a curator (without user_id)
        resource = {
            'properties': {'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_create_error_400_bad_request(resource)

        # try to create a curator (without keyword_id)
        resource = {
            'properties': {'keyword_id': 1010, 'region': 'joana'},
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
    
    def test_post_api_curator_create_error_401_unauthorized_without_authorization_header(self):
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_create_error_401_unauthorized(resource)

    def test_post_api_curator_create_error_403_forbidden_invalid_user_tries_to_create_a_curator(self):
        # DO LOGIN
        self.tester.auth_login("gabriel@admin.com", "gabriel")

        # add a user in a layer
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_create_error_403_forbidden(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # time_columns errors - update

    def test_put_api_curator_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a curator (without user_id)
        resource = {
            'properties': {'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_update_error_400_bad_request(resource)

        # try to create a curator (without keyword_id)
        resource = {
            'properties': {'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_update_error_400_bad_request(resource)

        # try to create a curator (without region)
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010},
            'type': 'Curator'
        }
        self.tester.api_curator_update_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_curator_error_401_unauthorized_without_authorization_header(self):
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_update_error_401_unauthorized(resource)

    def test_put_api_curator_error_403_forbidden_invalid_user_tries_to_create_a_curator(self):
        # DO LOGIN
        self.tester.auth_login("gabriel@admin.com", "gabriel")

        # add a user in a layer
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_update_error_403_forbidden(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # time_columns errors - delete

    def test_delete_api_curator_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_curator_delete_error_400_bad_request(user_id="abc", keyword_id="abc")
        self.tester.api_curator_delete_error_400_bad_request(user_id=0, keyword_id=0)
        self.tester.api_curator_delete_error_400_bad_request(user_id=-1, keyword_id=-1)
        self.tester.api_curator_delete_error_400_bad_request(user_id="-1", keyword_id="-1")
        self.tester.api_curator_delete_error_400_bad_request(user_id="0", keyword_id="0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
    
    def test_delete_api_curator_error_401_unauthorized_user_without_login(self):
        self.tester.api_curator_delete_error_401_unauthorized(user_id=1001, keyword_id=1001)
        self.tester.api_curator_delete_error_401_unauthorized(user_id=1001, keyword_id="1001")
        self.tester.api_curator_delete_error_401_unauthorized(user_id=0, keyword_id=-1)
        self.tester.api_curator_delete_error_401_unauthorized(user_id="0", keyword_id="-1")
    
    def test_delete_api_curator_error_403_forbidden_user_forbidden_to_delete_user_in_layer(self):
        # login with user who is not an admin
        self.tester.auth_login("gabriel@admin.com", "gabriel")

        # try to remove the user in layer
        self.tester.api_curator_delete_error_403_forbidden(user_id=1001, keyword_id=1001)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_curator_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_curator_delete_error_404_not_found(user_id=1001, keyword_id=5000)
        self.tester.api_curator_delete_error_404_not_found(user_id=5001, keyword_id=1001)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
    """

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
