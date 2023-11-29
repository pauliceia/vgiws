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
                                   'user_id': 1001, 'region': 'amaro'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1001, 'region': 'azure'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1002, 'region': 'belondres'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-02-22 00:00:00', 'keyword_id': 1010,
                                   'user_id': 1003, 'region': 'jorge'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-15 00:00:00', 'keyword_id': 1020,
                                   'user_id': 1003, 'region': 'centro'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-02-20 00:00:00', 'keyword_id': 1003,
                                   'user_id': 1004, 'region': 'são francisco'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-02-22 00:00:00', 'keyword_id': 1010,
                                   'user_id': 1005, 'region': 'são bento'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-03-24 00:00:00', 'keyword_id': 1021,
                                   'user_id': 1006, 'region': 'avenida rodônia'},
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
                                   'user_id': 1003, 'region': 'jorge'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-15 00:00:00', 'keyword_id': 1020,
                                   'user_id': 1003, 'region': 'centro'},
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
                                   'user_id': 1001, 'region': 'azure'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1002, 'region': 'belondres'},
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
                                   'user_id': 1004, 'region': 'são francisco'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-02-22 00:00:00', 'keyword_id': 1010,
                                   'user_id': 1005, 'region': 'são bento'},
                    'type': 'Curator'
                }
            ]
        }

        self.tester.api_curator(expected, region="São")

    def test_get_api_curator_return_curator_by_user_id_and_keyword_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1002, 'region': 'belondres'},
                    'type': 'Curator'
                }
            ]
        }

        self.tester.api_curator(expected, user_id="1002", keyword_id="1002")

    def test_get_api_curator_return_zero_resources(self):
        expected = {'type': 'FeatureCollection', 'features': []}

        self.tester.api_curator(expected, keyword_id="999")
        self.tester.api_curator(expected, keyword_id="998")

        self.tester.api_curator(expected, user_id="999")
        self.tester.api_curator(expected, user_id="998")

    # curator - create, update and delete

    def test_api_curator_create_update_and_delete(self):
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
        # check if the resource was modified
        ##################################################
        p = resource["properties"]
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_curator(expected_at_least=expected_resource, user_id=p["user_id"], keyword_id=p["keyword_id"])

        ##################################################
        # remove curator
        ##################################################
        # get the id of layer to REMOVE it
        user_id = resource["properties"]["user_id"]
        keyword_id = resource["properties"]["keyword_id"]

        # remove the user in layer
        self.tester.api_curator_delete(user_id=user_id, keyword_id=keyword_id)

        # it is not possible to find the layer that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_curator(expected, user_id=user_id, keyword_id=keyword_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIUserCuratorErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # curator errors - get

    def test_get_api_curator_error_400_bad_request(self):
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

    # curator errors - create

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
            'properties': {'user_id': 1003, 'region': 'joana'},
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
        self.tester.auth_login("miguel@admin.com", "miguel")

        # add a user in a layer
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_create_error_403_forbidden(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # curator errors - update

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
            'properties': {'user_id': 1003, 'region': 'joana'},
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
        self.tester.auth_login("miguel@admin.com", "miguel")

        # add a user in a layer
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_update_error_403_forbidden(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_curator_error_404_not_found_user_or_keyword(self):
        # DO LOGIN
        self.tester.auth_login("admin@admin.com", "admin")

        # not found a user
        resource = {
            'properties': {'user_id': 999, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_update_error_404_not_found(resource)

        # not found a keyword
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 999, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_update_error_404_not_found(resource)

        # not found a user or keyword
        resource = {
            'properties': {'user_id': 999, 'keyword_id': 999, 'region': 'joana'},
            'type': 'Curator'
        }
        self.tester.api_curator_update_error_404_not_found(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # curator errors - delete

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
        self.tester.auth_login("miguel@admin.com", "miguel")

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


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
